from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PACK = (
    REPO_ROOT
    / "docs/researchops/s27_v2_local_replay_inputs/ZN/"
    "20260611_non_2026_oldest_dev_recon_znu3_20230522_declared_pack"
)
MANIFEST = PACK / "S27_V2_NON_2026_OLDEST_DECLARED_INPUT_PACK_MANIFEST.json"


ROW_FAMILIES = (
    "daily_continuous_completed_bar.csv",
    "daily_current_contract_completed_bar.csv",
    "hourly_decision_completed_bar.csv",
    "hourly_fill_completed_bar.csv",
    "session_calendar.csv",
    "roll_calendar.csv",
    "cost_parameter.csv",
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def _rows(name: str) -> list[dict[str, str]]:
    with (PACK / name).open(newline="", encoding="ascii") as handle:
        return list(csv.DictReader(handle))


def test_manifest_binds_non_2026_pack_and_authorization() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="ascii"))

    assert manifest["authorization"] == "S27_V2_NON_2026_OLDEST_LOCAL_DEVELOPMENT_PACK_BUILD_GATE"
    assert manifest["status"] == (
        "LOCAL_INPUT_PACK_DECLARED_FOR_NON_2026_DEVELOPMENT_RECON_ONLY_NOT_BACKTEST_NOT_RESULT"
    )
    assert manifest["selected_raw_symbol"] == "ZNU3"
    assert manifest["selected_decision_timestamp_utc"] == "2023-05-22T00:00:00Z"
    assert manifest["selected_fill_timestamp_utc"] == "2023-05-22T01:00:00Z"
    assert manifest["selected_previous_daily_timestamp_utc"] == "2023-05-21T00:00:00Z"
    assert "NO_2026_DATA" in manifest["explicitly_excluded_data"]
    assert "NO_2026_DATA" in manifest["non_authorizations"]
    assert "NO_BACKTESTS" in manifest["non_authorizations"]
    assert "NO_SOURCE_FAITHFUL_EVIDENCE_CLAIM" in manifest["non_authorizations"]


def test_row_family_hashes_and_counts_match_manifest() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="ascii"))

    for name in ROW_FAMILIES:
        rows = _rows(name)
        recorded = manifest["row_family_files"][name]
        assert int(recorded["row_count"]) == len(rows)
        assert recorded["sha256"] == _sha256(PACK / name)

    assert len(_rows("daily_continuous_completed_bar.csv")) == 64
    assert len(_rows("daily_current_contract_completed_bar.csv")) == 1
    assert len(_rows("hourly_decision_completed_bar.csv")) == 1
    assert len(_rows("hourly_fill_completed_bar.csv")) == 1


def test_row_families_contain_no_2026_selected_data() -> None:
    for name in ROW_FAMILIES:
        text = (PACK / name).read_text(encoding="ascii")
        assert "2026-" not in text
        assert "ZNM6" not in text


def test_strict_prior_vqm_and_level_bridge_arithmetic() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="ascii"))
    evidence = manifest["history_evidence"]
    proof = manifest["level_bridge_proof"]

    assert evidence["selected_vqm_source_completed_trading_date"] == "2023-05-21"
    assert evidence["selected_vqm_multiplier_m"] == "1.2747933884297518"
    assert evidence["selected_vqm_quantile_q"] == "0.0"
    assert evidence["accepted_ten_year_roll_level_adjustment"] == "2.28125"
    assert evidence["rejected_hourly_lineage_adjustment"] == "0.84375"
    assert proof["bridge_disposition"] == (
        "PASS_LOCAL_LEVEL_SPACE_BRIDGE_SHARED_TEN_YEAR_ROLL_LEVEL_NOT_PRICE_EQUALITY_NOT_RESULT_EVIDENCE"
    )
    assert proof["daily_additive_back_adjustment"] == "2.28125"
    assert proof["hourly_additive_back_adjustment_applied_for_bridge"] == "2.28125"

    daily_rows = _rows("daily_continuous_completed_bar.csv")
    daily_dates = [row["trading_date"] for row in daily_rows]
    assert daily_dates == sorted(daily_dates)
    assert daily_dates[-1] == "2023-05-21"

    daily_continuous = daily_rows[-1]
    daily_current = _rows("daily_current_contract_completed_bar.csv")[0]
    decision = _rows("hourly_decision_completed_bar.csv")[0]
    fill = _rows("hourly_fill_completed_bar.csv")[0]

    assert daily_current["close_price"] == "114.546875"
    assert daily_continuous["close_price"] == "116.828125"
    assert decision["close_price"] == "116.828125"
    assert fill["close_price"] == "116.921875"


def test_first_row_working_order_context_is_declared_not_full_lifecycle() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="ascii"))
    evidence = manifest["history_evidence"]
    context = manifest["working_order_lifecycle_context"]

    assert evidence["daily_continuous_order"] == "CHRONOLOGICAL_ASCENDING_SELECTED_ROW_LAST"
    assert evidence["working_order_lifecycle_status"] == (
        "FIRST_ROW_EMPTY_WORKING_ORDER_STATE_DECLARED_RUNNER_MUST_BIND_SUBSEQUENT_STATE"
    )
    assert context["status"] == "FIRST_ROW_EMPTY_WORKING_ORDER_STATE_DECLARED_FOR_LOCAL_DEV_RECON_RUNNER_BINDING"
    assert context["initial_current_position_contracts"] == "0"
    assert context["open_working_orders"] == "0"
    assert context["state_scope"] == "FIRST_ROW_CONTEXT_ONLY_NOT_FULL_MULTI_ROW_LIFECYCLE_EVIDENCE"
    assert context["runner_must_bind_subsequent_state"] == "YES"


def test_pack_is_not_a_run_or_result_surface() -> None:
    manifest_text = MANIFEST.read_text(encoding="ascii")
    provenance_text = (PACK / "S27_V2_NON_2026_OLDEST_DECLARED_INPUT_PACK_PROVENANCE.md").read_text(
        encoding="ascii"
    )

    assert "NO_BACKTESTS" in manifest_text
    assert "NO_RESULT_SCORED_RUNS" in manifest_text
    assert "NO_RESULT_INTERPRETATION" in manifest_text
    assert "NO_PNL_EVALUATION" in manifest_text
    assert "No provider/API access" in provenance_text
    assert "not a backtest" in provenance_text
