from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PACK = (
    REPO_ROOT
    / "docs/researchops/s27_v2_local_replay_inputs/ZN/"
    "20260611_pre2023_oldest_dev_recon_2022_declared_pack"
)
MANIFEST = PACK / "S27_V2_PRE2023_DATABENTO_DECLARED_INPUT_PACK_MANIFEST.json"
STATUS = (
    REPO_ROOT
    / "docs/researchops/s27_v2_databento_older_zn_history/"
    "20260611_pre2023_zn_dev_recon_download_build/status/"
    "20260611_S27_V2_ZN_PRE2023_OLDER_HISTORY_DOWNLOAD_BUILD_status.json"
)

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


def _manifest() -> dict[str, object]:
    return json.loads(MANIFEST.read_text(encoding="ascii"))


def test_status_preserves_2023_for_test_and_no_result_surface() -> None:
    status = json.loads(STATUS.read_text(encoding="ascii"))

    assert status["status"] == "PASS_S27_V2_PRE2023_ZN_HISTORY_DOWNLOADED_AND_2022_PACK_DECLARED_NOT_BACKTEST_NOT_RESULT"
    assert status["development_reconciliation_start"] == "2022-01-01"
    assert status["development_reconciliation_end"] == "2022-12-31"
    assert status["protected_2023_for_test"] == "YES"
    assert status["test_access"] == "NO"
    assert status["validation_access"] == "NO"
    assert status["oos_access"] == "NO"
    assert status["lockbox_access"] == "NO"
    assert status["backtests_run"] == "NO"
    assert status["result_scored_runs"] == "NO"
    assert status["source_faithful_evidence_claim"] == "NO"


def test_manifest_binds_oldest_2022_selected_row_and_strict_prior_vqm() -> None:
    manifest = _manifest()
    evidence = manifest["history_evidence"]

    assert manifest["authorization"] == "S27_V2_EXACTLY_ONE_DATABENTO_ZN_OLDER_HISTORY_DOWNLOAD_BUILD_GATE"
    assert manifest["status"] == "LOCAL_INPUT_PACK_DECLARED_FOR_2022_DEVELOPMENT_RECON_ONLY_NOT_BACKTEST_NOT_RESULT"
    assert manifest["selected_raw_symbol"] == "ZNH2"
    assert manifest["selected_decision_timestamp_utc"] == "2022-01-03T01:00:00Z"
    assert manifest["selected_fill_timestamp_utc"] == "2022-01-03T02:00:00Z"
    assert manifest["selected_previous_daily_timestamp_utc"] == "2021-12-31T00:00:00Z"
    assert evidence["selected_vqm_source_completed_trading_date"] == "2021-12-31"
    assert evidence["selected_vqm_method_status"] == "LOCKED_S13_STYLE_V_Q_M_ATTENUATION_RUNTIME_PRE2023_DATABENTO"
    assert evidence["daily_continuous_order"] == "CHRONOLOGICAL_ASCENDING_SELECTED_ROW_LAST"
    assert "NO_2023_TEST_DATA" in manifest["explicitly_excluded_data"]


def test_row_family_hashes_and_counts_match_manifest() -> None:
    manifest = _manifest()

    for name in ROW_FAMILIES:
        rows = _rows(name)
        recorded = manifest["row_family_files"][name]
        assert int(recorded["row_count"]) == len(rows)
        assert recorded["sha256"] == _sha256(PACK / name)

    assert len(_rows("daily_continuous_completed_bar.csv")) == 64
    assert len(_rows("daily_current_contract_completed_bar.csv")) == 1
    assert len(_rows("hourly_decision_completed_bar.csv")) == 1
    assert len(_rows("hourly_fill_completed_bar.csv")) == 1
    assert len(_rows("roll_calendar.csv")) >= 1


def test_row_families_do_not_contain_2023_or_later_selected_data() -> None:
    for name in ROW_FAMILIES:
        text = (PACK / name).read_text(encoding="ascii")
        assert "2023-" not in text
        assert "2024-" not in text
        assert "2025-" not in text
        assert "2026-" not in text


def test_daily_window_is_chronological_and_level_bridge_matches() -> None:
    manifest = _manifest()
    proof = manifest["level_bridge_proof"]
    daily_rows = _rows("daily_continuous_completed_bar.csv")
    current_row = _rows("daily_current_contract_completed_bar.csv")[0]
    roll_rows = _rows("roll_calendar.csv")
    daily_dates = [row["trading_date"] for row in daily_rows]

    assert daily_dates == sorted(daily_dates)
    assert daily_dates[0] == "2021-10-17"
    assert daily_dates[-1] == "2021-12-31"
    assert daily_rows[-1]["close_price"] == current_row["close_price"] == "130.34375"
    assert proof["daily_active_contract"] == "ZNH2"
    assert proof["hourly_active_contract"] == "ZNH2"
    assert proof["daily_additive_back_adjustment"] == "0.0"
    assert proof["hourly_additive_back_adjustment_applied_for_bridge"] == "0.0"
    assert proof["daily_additive_back_adjustment"] == proof["hourly_additive_back_adjustment_applied_for_bridge"]
    assert proof["point_in_time_roll_cutoff_date"] == "2021-12-31"
    assert proof["future_roll_deltas_after_cutoff_excluded"] == "YES"
    assert proof["bridge_disposition"] == (
        "PASS_LOCAL_LEVEL_SPACE_BRIDGE_SHARED_DATABENTO_DAILY_ROLL_LEVEL_NOT_PRICE_EQUALITY_NOT_RESULT_EVIDENCE"
    )
    assert max(row["roll_transition_date"] for row in roll_rows) <= "2021-12-31"
    assert "2022-02-16" not in {row["roll_transition_date"] for row in roll_rows}
    assert "ZNH3_2023" not in {row["new_contract_key"] for row in roll_rows}


def test_first_row_working_state_is_declared_not_full_lifecycle() -> None:
    manifest = _manifest()
    context = manifest["working_order_lifecycle_context"]

    assert context["initial_current_position_contracts"] == "0"
    assert context["open_working_orders"] == "0"
    assert context["state_scope"] == "FIRST_ROW_CONTEXT_ONLY_NOT_FULL_MULTI_ROW_LIFECYCLE_EVIDENCE"
    assert context["runner_must_bind_subsequent_state"] == "YES"
