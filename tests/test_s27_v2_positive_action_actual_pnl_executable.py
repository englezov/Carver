from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from carver.spine.m0 import CarverBlocked
import carver.spine.s27_v2_replay as package_root
import carver.spine.s27_v2_replay.positive_action_actual_pnl_executable as pnl_module
from carver.spine.s27_v2_replay.local_replay import canonical_sha256
from carver.spine.s27_v2_replay.positive_action_actual_cost_executable import _actual_cost_bundle_hash_payload
from carver.spine.s27_v2_replay.positive_action_actual_pnl_executable import (
    ACTUAL_PNL_NON_AUTHORIZATIONS,
    ACTUAL_PNL_REASON_CODE,
    ACTUAL_PNL_ROW_STATUS,
    BACKTEST_STATUS,
    PNL_DIRECTION_LABEL,
    PNL_EVALUATION_STATUS,
    RESULT_STATUS,
    S27_V2_POSITIVE_ACTION_ACTUAL_PNL_AUTHORIZATION,
    S27_V2_POSITIVE_ACTION_ACTUAL_PNL_STATUS,
    VALUATION_CONVENTION_LABEL,
    VALUATION_CONVENTION_NAME,
    _actual_pnl_bundle_hash_payload,
    _actual_pnl_row_hash_payload,
    _policy_hash,
    build_positive_action_actual_pnl_executable,
)


POSITIVE_ACTION_PACK_PATH = (
    ROOT
    / "docs"
    / "researchops"
    / "s27_v2_local_replay_inputs"
    / "ZN"
    / "20260609_positive_action_recon_znm6_20260413T13_declared_pack"
)

VALUATION_MARK_PACK_PATH = (
    ROOT
    / "docs"
    / "researchops"
    / "s27_v2_local_replay_inputs"
    / "ZN"
    / "20260609_positive_action_valuation_mark_znm6_20260413T15_declared_pack"
)


@pytest.fixture(scope="module")
def active_actual_pnl_bundle():
    return build_positive_action_actual_pnl_executable(POSITIVE_ACTION_PACK_PATH, VALUATION_MARK_PACK_PATH)


def _rehash_row(row):
    return replace(row, row_hash=canonical_sha256(_actual_pnl_row_hash_payload(row)))


def _rehash_bundle(bundle):
    return replace(bundle, bundle_hash=canonical_sha256(_actual_pnl_bundle_hash_payload(bundle)))


def test_positive_action_actual_pnl_builds_single_mechanical_row(active_actual_pnl_bundle):
    bundle = active_actual_pnl_bundle
    row = bundle.actual_pnl_row

    assert bundle.status == S27_V2_POSITIVE_ACTION_ACTUAL_PNL_STATUS
    assert bundle.authorization_label == S27_V2_POSITIVE_ACTION_ACTUAL_PNL_AUTHORIZATION
    assert row.row_status == ACTUAL_PNL_ROW_STATUS
    assert row.reason_code == ACTUAL_PNL_REASON_CODE
    assert row.raw_symbol == "ZNM6"
    assert row.selected_fill_timestamp_utc == "2026-04-13T14:00:00Z"
    assert row.valuation_mark_completed_timestamp_utc == "2026-04-13T15:00:00Z"
    assert row.filled_order_side == "SELL"
    assert row.fill_quantity == 1
    assert row.position_after_fill == -1
    assert row.fill_price == pytest.approx(111.046875)
    assert row.valuation_mark_close_price == pytest.approx(111.046875)
    assert row.contract_point_value == pytest.approx(1000.0)
    assert row.contract_point_value_currency == "USD"
    assert row.valuation_convention_label == VALUATION_CONVENTION_LABEL
    assert row.valuation_convention_name == VALUATION_CONVENTION_NAME
    assert row.pnl_direction_label == PNL_DIRECTION_LABEL
    assert row.gross_pnl_amount == pytest.approx(0.0)
    assert row.commission_cost_amount == pytest.approx(2.30)
    assert row.spread_cost_amount == pytest.approx(0.0)
    assert row.total_cost_amount == pytest.approx(2.30)
    assert row.net_pnl_amount == pytest.approx(-2.30)
    assert row.pnl_currency == "USD"
    assert row.result_status == RESULT_STATUS
    assert row.backtest_status == BACKTEST_STATUS
    assert row.pnl_evaluation_status == PNL_EVALUATION_STATUS
    assert row.result_rows_emitted is False
    assert row.result_scored_run_emitted is False
    assert row.result_interpretation_emitted is False
    assert row.pnl_evaluation_emitted is False
    assert row.source_faithful_evidence_claimed is False

    assert bundle.actual_cost_rows_emitted is True
    assert bundle.actual_pnl_rows_emitted is True
    assert bundle.result_rows_emitted is False
    assert bundle.result_scored_run_emitted is False
    assert bundle.result_interpretation_emitted is False
    assert bundle.pnl_evaluation_emitted is False
    assert bundle.source_faithful_evidence_claimed is False
    assert bundle.non_authorizations == ACTUAL_PNL_NON_AUTHORIZATIONS


def test_positive_action_actual_pnl_row_is_not_standalone_authority(active_actual_pnl_bundle):
    with pytest.raises(CarverBlocked, match="standalone validation is not authoritative"):
        active_actual_pnl_bundle.actual_pnl_row.validate()


def test_positive_action_actual_pnl_rejects_out_of_scope_pack(tmp_path):
    with pytest.raises(CarverBlocked, match="locked to the declared positive-action pack"):
        build_positive_action_actual_pnl_executable(tmp_path, VALUATION_MARK_PACK_PATH)


def test_positive_action_actual_pnl_rejects_out_of_scope_mark_pack(tmp_path):
    with pytest.raises(CarverBlocked, match="locked to the declared valuation mark pack"):
        build_positive_action_actual_pnl_executable(POSITIVE_ACTION_PACK_PATH, tmp_path)


def test_positive_action_actual_pnl_rejects_forged_actual_cost_bundle(active_actual_pnl_bundle):
    cost_bundle = replace(active_actual_pnl_bundle.actual_cost_bundle, source_faithful_evidence_claimed=True)
    cost_bundle = replace(cost_bundle, bundle_hash=canonical_sha256(_actual_cost_bundle_hash_payload(cost_bundle)))
    forged = _rehash_bundle(replace(active_actual_pnl_bundle, actual_cost_bundle=cost_bundle))

    with pytest.raises(CarverBlocked):
        forged.validate()


@pytest.mark.parametrize(
    ("field_name", "forged_value"),
    (
        ("actual_cost_bundle_hash", "1" * 64),
        ("actual_cost_row_hash", "2" * 64),
        ("fill_bundle_hash", "3" * 64),
        ("limit_fill_row_hash", "4" * 64),
        ("valuation_mark_manifest_sha256", "5" * 64),
        ("valuation_mark_csv_sha256", "6" * 64),
        ("valuation_mark_local_audit_sha256", "7" * 64),
        ("selected_fill_timestamp_utc", "2026-04-13T15:00:00Z"),
        ("valuation_mark_completed_timestamp_utc", "2026-04-13T14:00:00Z"),
        ("raw_symbol", "ZNU6"),
        ("filled_order_side", "BUY"),
        ("fill_quantity", 2),
        ("position_after_fill", 1),
        ("fill_price", 111.0),
        ("valuation_mark_close_price", 111.125),
        ("contract_point_value", 2147483647.0),
        ("contract_point_value_currency", "EUR"),
        ("valuation_convention_label", "BOOK_EXPLICIT_VALUATION"),
        ("valuation_convention_name", "SAME_BAR_CLOSE"),
        ("valuation_mark_source_row_text_sha256", "8" * 64),
        ("valuation_mark_source_row_canonical_json_sha256", "9" * 64),
        ("pnl_direction_label", "LONG_MARK_MINUS_FILL"),
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
def test_positive_action_actual_pnl_rejects_self_consistent_row_forgery(
    active_actual_pnl_bundle,
    field_name,
    forged_value,
):
    row = replace(active_actual_pnl_bundle.actual_pnl_row, **{field_name: forged_value})
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
    forged = _rehash_bundle(replace(active_actual_pnl_bundle, actual_pnl_row=_rehash_row(row)))

    with pytest.raises(CarverBlocked):
        forged.validate()


@pytest.mark.parametrize(
    ("flag_name", "forged_value"),
    (
        ("actual_cost_rows_emitted", False),
        ("actual_pnl_rows_emitted", False),
        ("validation_metadata_rows_emitted", False),
        ("provenance_metadata_rows_emitted", False),
        ("trusted_bundle_metadata_emitted", False),
        ("result_rows_emitted", True),
        ("result_scored_run_emitted", True),
        ("result_interpretation_emitted", True),
        ("pnl_evaluation_emitted", True),
        ("source_faithful_evidence_claimed", True),
    ),
)
def test_positive_action_actual_pnl_rejects_bundle_flag_forgery(
    active_actual_pnl_bundle,
    flag_name,
    forged_value,
):
    forged = _rehash_bundle(replace(active_actual_pnl_bundle, **{flag_name: forged_value}))

    with pytest.raises(CarverBlocked):
        forged.validate()


def test_positive_action_actual_pnl_rejects_unpinned_valuation_mark_manifest(monkeypatch):
    monkeypatch.setattr(pnl_module, "_EXPECTED_VALUATION_MARK_MANIFEST_SHA256", "0" * 64)

    with pytest.raises(CarverBlocked, match="valuation mark manifest byte hash is not pinned"):
        build_positive_action_actual_pnl_executable(POSITIVE_ACTION_PACK_PATH, VALUATION_MARK_PACK_PATH)


def test_positive_action_actual_pnl_rejects_unpinned_local_audit(monkeypatch):
    monkeypatch.setattr(pnl_module, "_EXPECTED_VALUATION_MARK_LOCAL_AUDIT_SHA256", "0" * 64)

    with pytest.raises(CarverBlocked, match="valuation mark local audit record byte hash is not pinned"):
        build_positive_action_actual_pnl_executable(POSITIVE_ACTION_PACK_PATH, VALUATION_MARK_PACK_PATH)


def test_positive_action_actual_pnl_is_not_package_root_exported():
    assert "build_positive_action_actual_pnl_executable" not in getattr(package_root, "__all__", ())
    assert not hasattr(package_root, "build_positive_action_actual_pnl_executable")
