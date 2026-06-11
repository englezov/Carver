from __future__ import annotations

import csv
import json
from dataclasses import replace
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from carver.spine.m0 import CarverBlocked
import carver.spine.s27_v2_replay as package_root
from carver.spine.s27_v2_replay.development_recon_run import (
    CONTROLLED_RUN_RELATIVE_PATH,
    PNL_BLOCKED_STATUS,
    RESULT_STATUS,
    RUN_NON_AUTHORIZATIONS,
    _run_bundle_payload,
    run_s27_v2_controlled_pre2023_development_recon,
)
from carver.spine.s27_v2_replay.local_replay import canonical_sha256


RUN_ROOT = ROOT / CONTROLLED_RUN_RELATIVE_PATH
PACK_ROOT = (
    ROOT
    / "docs/researchops/s27_v2_local_replay_inputs/ZN/"
    "20260611_pre2023_oldest_dev_recon_2022_declared_pack"
)


@pytest.fixture(scope="module")
def controlled_bundle():
    return run_s27_v2_controlled_pre2023_development_recon(PACK_ROOT, RUN_ROOT)


def _rows(name: str) -> list[dict[str, str]]:
    with (RUN_ROOT / name).open(newline="", encoding="ascii") as handle:
        return list(csv.DictReader(handle))


def _json(name: str) -> dict[str, object]:
    return json.loads((RUN_ROOT / name).read_text(encoding="ascii"))


def _rehash_bundle(bundle):
    return replace(bundle, bundle_hash=canonical_sha256(_run_bundle_payload(bundle)))


def test_controlled_run_bundle_is_locked_to_pre2023_pack(controlled_bundle):
    assert Path(controlled_bundle.input_pack_path).resolve() == PACK_ROOT.resolve()
    assert controlled_bundle.selected_decision_timestamp_utc == "2022-01-03T01:00:00Z"
    assert controlled_bundle.selected_fill_timestamp_utc == "2022-01-03T02:00:00Z"
    assert controlled_bundle.raw_symbol == "ZNH2"
    assert controlled_bundle.non_authorizations == RUN_NON_AUTHORIZATIONS
    assert controlled_bundle.result_status == RESULT_STATUS
    assert controlled_bundle.pnl_status == PNL_BLOCKED_STATUS


def test_controlled_run_rejects_out_of_scope_input_pack(tmp_path):
    with pytest.raises(CarverBlocked, match="locked to the audited pre-2023 pack"):
        run_s27_v2_controlled_pre2023_development_recon(tmp_path, RUN_ROOT)


def test_controlled_run_rejects_out_of_scope_output_root(tmp_path):
    with pytest.raises(CarverBlocked, match="output root is locked"):
        run_s27_v2_controlled_pre2023_development_recon(PACK_ROOT, tmp_path)


def test_run_manifest_preserves_dev_recon_scope_and_protected_windows(controlled_bundle):
    manifest = _json("run_manifest.json")

    assert manifest["status"] == "S27_V2_CONTROLLED_DEV_RECON_RUN_EMITTED_NOT_RESULT_NOT_PROMOTION"
    assert manifest["selected_decision_timestamp_utc"] == "2022-01-03T01:00:00Z"
    assert manifest["selected_raw_symbol"] == "ZNH2"
    assert manifest["result_interpretation"] == "NO"
    assert manifest["source_faithful_evidence_claim"] == "NO"
    assert "NO_TEST_ACCESS" in manifest["non_authorizations"]
    assert "NO_VALIDATION_ACCESS" in manifest["non_authorizations"]
    assert "NO_OOS" in manifest["non_authorizations"]
    assert "NO_LOCKBOX" in manifest["non_authorizations"]
    assert "NO_FORWARD" in manifest["non_authorizations"]
    assert manifest["input_manifest_sha256"] == "CB8CCD4B2433BAB8255246BDE84D406F994495E5880099D2F5AD7BF766BB0504"
    assert controlled_bundle.run_manifest_hash == _sha256(RUN_ROOT / "run_manifest.json")


def test_runtime_forecast_and_position_arithmetic(controlled_bundle):
    runtime = _rows("runtime_history_ledger.csv")[0]
    forecast = _rows("forecast_replay_ledger.csv")[0]
    position = _rows("desired_position_ledger.csv")[0]

    assert int(runtime["observed_daily_rows"]) == 64
    assert forecast["trend_veto_decision"] == "PERMIT_MEAN_REVERSION"
    assert float(forecast["capped_forecast_value"]) == pytest.approx(4.894376401547715)
    assert float(position["base_position_contracts"]) == pytest.approx(16.432147617721743)
    assert float(position["desired_unrounded_contracts"]) == pytest.approx(8.04251155269258)
    assert int(position["desired_position_contracts"]) == 8
    assert int(position["position_change_contracts"]) == 8
    assert controlled_bundle.desired_position_contracts == 8


def test_buy_limit_fill_and_cost_are_mechanical_not_result(controlled_bundle):
    order = _rows("limit_order_ledger.csv")[0]
    fill = _rows("fill_ledger.csv")[0]
    commission = _rows("commission_ledger.csv")[0]
    spread = _rows("spread_cost_ledger.csv")[0]

    assert order["order_side"] == "BUY"
    assert int(order["order_quantity"]) == 8
    assert int(order["adjacent_target_position"]) == 1
    assert float(order["limit_order_price"]) == pytest.approx(130.421875)
    assert fill["fill_executed"] == "TRUE"
    assert fill["fill_price_provenance"] == "LIMIT_ORDER_PRICE_FROM_FILLED_ORDER"
    assert float(fill["fill_price"]) == pytest.approx(130.421875)
    assert int(fill["fill_quantity"]) == 8
    assert int(fill["position_after_fill"]) == 8
    assert float(commission["commission_amount"]) == pytest.approx(18.4)
    assert float(spread["spread_cost_amount"]) == pytest.approx(0.0)
    assert controlled_bundle.fill_executed is True
    assert controlled_bundle.commission_amount == pytest.approx(18.4)


def test_pnl_remains_fail_closed_without_post_fill_valuation_mark(controlled_bundle):
    pnl = _rows("pnl_ledger.csv")[0]
    validation = _rows("validation_ledger.csv")[0]
    trusted = _json("trusted_bundle.json")

    assert pnl["pnl_status"] == PNL_BLOCKED_STATUS
    assert pnl["valuation_mark_row_declared"] == "FALSE"
    assert pnl["actual_pnl_rows_emitted"] == "FALSE"
    assert validation["result_status"] == RESULT_STATUS
    assert validation["source_faithful_evidence_claimed"] == "FALSE"
    assert trusted["result_status"] == RESULT_STATUS
    assert trusted["source_faithful_evidence_claimed"] is False


def test_hash_artifacts_bind_written_files(controlled_bundle):
    evidence = _json("evidence_manifest.json")
    sha_rows = _rows("SHA256SUMS.csv")
    sha_by_path = {row["relative_path"]: row["sha256"] for row in sha_rows}

    assert controlled_bundle.evidence_manifest_hash == _sha256(RUN_ROOT / "evidence_manifest.json")
    assert controlled_bundle.trusted_bundle_hash == _sha256(RUN_ROOT / "trusted_bundle.json")
    for relative_path, digest in evidence["ledger_hashes"].items():
        assert digest == _sha256(RUN_ROOT / relative_path)
        assert sha_by_path[relative_path] == digest


@pytest.mark.parametrize(
    ("field_name", "forged_value"),
    (
        ("result_status", "FORGED_RESULT"),
        ("pnl_status", "FORGED_PNL_READY"),
        ("trusted_bundle_hash", "1" * 64),
        ("non_authorizations", tuple()),
    ),
)
def test_controlled_run_bundle_rejects_forged_boundaries(controlled_bundle, field_name, forged_value):
    forged = _rehash_bundle(replace(controlled_bundle, **{field_name: forged_value}))

    with pytest.raises(CarverBlocked):
        forged.validate()


def test_controlled_run_not_exported_from_package_root():
    package_init = (ROOT / "src" / "carver" / "spine" / "s27_v2_replay" / "__init__.py").read_text()

    assert "development_recon_run" not in package_init
    assert "run_s27_v2_controlled_pre2023_development_recon" not in package_init
    assert not hasattr(package_root, "run_s27_v2_controlled_pre2023_development_recon")


def test_controlled_run_module_does_not_import_stale_diagnostic_runners():
    source = (ROOT / "src" / "carver" / "spine" / "s27_v2_replay" / "development_recon_run.py").read_text()

    for forbidden in (
        "carver_s27_zn_2024_corrected_validation_backtest",
        "carver_s27_zn_2024_corrected_full_ladder_validation_backtest",
        "carver_s27_zn_2025_2026_corrected_test3_backtest",
        "carver_s27_zn_m1_ladder_dev_recon_backtest",
        "carver_s27_zn_ladder_attribution",
        "carver_s27_zn_lockbox_readiness",
    ):
        assert forbidden not in source
    for dynamic_execution_surface in ("importlib", "__import__", "runpy", "SourceFileLoader", "subprocess"):
        assert dynamic_execution_surface not in source


def _sha256(path: Path) -> str:
    import hashlib

    return hashlib.sha256(path.read_bytes()).hexdigest()
