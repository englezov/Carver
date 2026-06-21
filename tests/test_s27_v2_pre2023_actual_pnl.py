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
from carver.spine.s27_v2_replay.local_replay import canonical_sha256
import carver.spine.s27_v2_replay.pre2023_development_recon_actual_pnl as pnl_module
from carver.spine.s27_v2_replay.pre2023_development_recon_actual_pnl import (
    ACTUAL_PNL_NON_AUTHORIZATIONS,
    ACTUAL_PNL_REASON_CODE,
    ACTUAL_PNL_ROW_STATUS,
    BACKTEST_STATUS,
    EXPECTED_FILL_TIMESTAMP,
    EXPECTED_RAW_SYMBOL,
    EXPECTED_VALUATION_MARK_TIMESTAMP,
    PNL_DIRECTION_LABEL,
    PNL_EVALUATION_STATUS,
    PRE2023_ACTUAL_PNL_OUTPUT_RELATIVE_PATH,
    RESULT_STATUS,
    S27_V2_PRE2023_ACTUAL_PNL_AUTHORIZATION,
    S27_V2_PRE2023_ACTUAL_PNL_STATUS,
    VALUATION_CONVENTION_LABEL,
    VALUATION_CONVENTION_NAME,
    _actual_pnl_bundle_hash_payload,
    _actual_pnl_row_hash_payload,
    _policy_hash,
    build_pre2023_development_recon_actual_pnl,
)


OUTPUT_ROOT = ROOT / PRE2023_ACTUAL_PNL_OUTPUT_RELATIVE_PATH


@pytest.fixture(scope="module")
def actual_pnl_bundle():
    return build_pre2023_development_recon_actual_pnl()


def _rows(name: str) -> list[dict[str, str]]:
    with (OUTPUT_ROOT / name).open(newline="", encoding="ascii") as handle:
        return list(csv.DictReader(handle))


def _json(name: str) -> dict[str, object]:
    return json.loads((OUTPUT_ROOT / name).read_text(encoding="ascii"))


def _sha256(path: Path) -> str:
    import hashlib

    return hashlib.sha256(path.read_bytes()).hexdigest()


def _rehash_row(row):
    return replace(row, row_hash=canonical_sha256(_actual_pnl_row_hash_payload(row)))


def _rehash_bundle(bundle):
    return replace(bundle, bundle_hash=canonical_sha256(_actual_pnl_bundle_hash_payload(bundle)))


def test_pre2023_actual_pnl_builds_mechanical_row(actual_pnl_bundle):
    bundle = actual_pnl_bundle
    row = bundle.actual_pnl_row

    assert bundle.status == S27_V2_PRE2023_ACTUAL_PNL_STATUS
    assert bundle.authorization_label == S27_V2_PRE2023_ACTUAL_PNL_AUTHORIZATION
    assert row.row_status == ACTUAL_PNL_ROW_STATUS
    assert row.reason_code == ACTUAL_PNL_REASON_CODE
    assert row.raw_symbol == EXPECTED_RAW_SYMBOL
    assert row.selected_fill_timestamp_utc == EXPECTED_FILL_TIMESTAMP
    assert row.valuation_mark_completed_timestamp_utc == EXPECTED_VALUATION_MARK_TIMESTAMP
    assert row.filled_order_side == "BUY"
    assert row.fill_quantity == 8
    assert row.position_after_fill == 8
    assert row.fill_price == pytest.approx(130.421875)
    assert row.valuation_mark_close_price == pytest.approx(130.296875)
    assert row.contract_point_value == pytest.approx(1000.0)
    assert row.contract_point_value_currency == "USD"
    assert row.valuation_convention_label == VALUATION_CONVENTION_LABEL
    assert row.valuation_convention_name == VALUATION_CONVENTION_NAME
    assert row.pnl_direction_label == PNL_DIRECTION_LABEL
    assert row.gross_pnl_amount == pytest.approx(-1000.0)
    assert row.commission_cost_amount == pytest.approx(18.4)
    assert row.spread_cost_amount == pytest.approx(0.0)
    assert row.total_cost_amount == pytest.approx(18.4)
    assert row.net_pnl_amount == pytest.approx(-1018.4)
    assert row.pnl_currency == "USD"
    assert row.result_status == RESULT_STATUS
    assert row.backtest_status == BACKTEST_STATUS
    assert row.pnl_evaluation_status == PNL_EVALUATION_STATUS
    assert row.result_rows_emitted is False
    assert row.result_scored_run_emitted is False
    assert row.result_interpretation_emitted is False
    assert row.pnl_evaluation_emitted is False
    assert row.source_faithful_evidence_claimed is False
    assert bundle.actual_pnl_rows_emitted is True
    assert bundle.result_rows_emitted is False
    assert bundle.non_authorizations == ACTUAL_PNL_NON_AUTHORIZATIONS


def test_pre2023_actual_pnl_row_is_not_standalone_authority(actual_pnl_bundle):
    with pytest.raises(CarverBlocked, match="standalone validation is not authoritative"):
        actual_pnl_bundle.actual_pnl_row.validate()


def test_pre2023_actual_pnl_rejects_out_of_scope_output_root(tmp_path):
    with pytest.raises(CarverBlocked, match="output root is locked"):
        build_pre2023_development_recon_actual_pnl(tmp_path)


def test_pre2023_actual_pnl_writes_bound_metadata_artifacts(actual_pnl_bundle):
    ledger = _rows("actual_pnl_ledger.csv")
    validation = _rows("validation_metadata_ledger.csv")[0]
    provenance = _rows("provenance_hash_metadata_ledger.csv")[0]
    evidence = _json("evidence_manifest.json")
    trusted = _json("trusted_bundle.json")
    sha_rows = _rows("SHA256SUMS.csv")
    sha_by_path = {row["relative_path"]: row["sha256"] for row in sha_rows}

    assert len(ledger) == 1
    assert ledger[0]["row_hash"] == actual_pnl_bundle.actual_pnl_row.row_hash
    assert validation["actual_pnl_bundle_hash"] == actual_pnl_bundle.bundle_hash
    assert provenance["actual_pnl_row_hash"] == actual_pnl_bundle.actual_pnl_row.row_hash
    assert evidence["actual_pnl_bundle_hash"] == actual_pnl_bundle.bundle_hash
    assert trusted["actual_pnl_bundle_hash"] == actual_pnl_bundle.bundle_hash
    assert trusted["result_rows_emitted"] is False
    assert trusted["source_faithful_evidence_claimed"] is False
    for relative_path, digest in sha_by_path.items():
        assert digest == _sha256(OUTPUT_ROOT / relative_path)


@pytest.mark.parametrize(
    ("field_name", "forged_value"),
    (
        ("controlled_run_bundle_hash", "1" * 64),
        ("fill_row_hash", "2" * 64),
        ("commission_row_hash", "3" * 64),
        ("spread_row_hash", "4" * 64),
        ("valuation_mark_manifest_sha256", "5" * 64),
        ("valuation_mark_csv_sha256", "6" * 64),
        ("valuation_mark_local_audit_sha256", "7" * 64),
        ("selected_fill_timestamp_utc", "2022-01-03T03:00:00Z"),
        ("valuation_mark_completed_timestamp_utc", "2022-01-03T02:00:00Z"),
        ("raw_symbol", "ZNU2"),
        ("filled_order_side", "SELL"),
        ("fill_quantity", 1),
        ("position_after_fill", 1),
        ("fill_price", 130.0),
        ("valuation_mark_close_price", 130.5),
        ("contract_point_value", 2147483647.0),
        ("contract_point_value_currency", "EUR"),
        ("valuation_convention_label", "BOOK_EXPLICIT_VALUATION"),
        ("valuation_convention_name", "SAME_BAR_CLOSE"),
        ("pnl_direction_label", "SHORT_FILL_MINUS_MARK"),
        ("gross_pnl_amount", 12.5),
        ("commission_cost_amount", 0.0),
        ("spread_cost_amount", 0.25),
        ("total_cost_amount", 0.25),
        ("net_pnl_amount", 12.25),
        ("pnl_currency", "EUR"),
        ("result_status", "PASS_RESULT_READY"),
        ("backtest_status", "PASS_BACKTEST_READY"),
        ("pnl_evaluation_status", "PASS_PNL_EVALUATED"),
        ("result_rows_emitted", True),
        ("result_scored_run_emitted", True),
        ("result_interpretation_emitted", True),
        ("pnl_evaluation_emitted", True),
        ("source_faithful_evidence_claimed", True),
    ),
)
def test_pre2023_actual_pnl_rejects_self_consistent_row_forgery(
    actual_pnl_bundle,
    field_name,
    forged_value,
):
    row = replace(actual_pnl_bundle.actual_pnl_row, **{field_name: forged_value})
    row = replace(
        row,
        valuation_convention_hash=_policy_hash(
            "valuation_convention",
            row.valuation_convention_label,
            row.valuation_convention_name,
            row.valuation_mark_manifest_sha256,
            row.valuation_mark_csv_sha256,
            row.valuation_mark_local_audit_sha256,
        ),
        pnl_formula_hash=_policy_hash(
            "actual_pnl_formula",
            row.pnl_direction_label,
            row.fill_price,
            row.valuation_mark_close_price,
            row.fill_quantity,
            row.contract_point_value,
            row.gross_pnl_amount,
            row.total_cost_amount,
            row.net_pnl_amount,
            row.pnl_currency,
        ),
    )
    forged = _rehash_bundle(replace(actual_pnl_bundle, actual_pnl_row=_rehash_row(row)))

    with pytest.raises(CarverBlocked):
        forged.validate()


@pytest.mark.parametrize(
    ("flag_name", "forged_value"),
    (
        ("actual_pnl_rows_emitted", False),
        ("validation_metadata_rows_emitted", False),
        ("provenance_metadata_rows_emitted", False),
        ("evidence_manifest_metadata_emitted", False),
        ("trusted_bundle_metadata_emitted", False),
        ("result_rows_emitted", True),
        ("result_scored_run_emitted", True),
        ("result_interpretation_emitted", True),
        ("pnl_evaluation_emitted", True),
        ("source_faithful_evidence_claimed", True),
    ),
)
def test_pre2023_actual_pnl_rejects_bundle_flag_forgery(actual_pnl_bundle, flag_name, forged_value):
    forged = _rehash_bundle(replace(actual_pnl_bundle, **{flag_name: forged_value}))

    with pytest.raises(CarverBlocked):
        forged.validate()


def test_pre2023_actual_pnl_rejects_unpinned_controlled_run(monkeypatch):
    monkeypatch.setattr(pnl_module, "_EXPECTED_CONTROLLED_RUN_BUNDLE_SHA256", "0" * 64)

    with pytest.raises(CarverBlocked, match="controlled-run bundle byte hash is not pinned"):
        build_pre2023_development_recon_actual_pnl()


def test_pre2023_actual_pnl_rejects_unpinned_valuation_mark(monkeypatch):
    monkeypatch.setattr(pnl_module, "_EXPECTED_VALUATION_MARK_MANIFEST_SHA256", "0" * 64)

    with pytest.raises(CarverBlocked, match="valuation manifest byte hash is not pinned"):
        build_pre2023_development_recon_actual_pnl()


def test_pre2023_actual_pnl_is_not_package_root_exported():
    assert "build_pre2023_development_recon_actual_pnl" not in getattr(package_root, "__all__", ())
    assert not hasattr(package_root, "build_pre2023_development_recon_actual_pnl")
