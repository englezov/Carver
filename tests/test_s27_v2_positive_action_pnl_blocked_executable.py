from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from carver.spine.m0 import CarverBlocked
from carver.spine.s27_v2_replay.local_replay import canonical_sha256
import carver.spine.s27_v2_replay.positive_action_pnl_blocked_executable as pnl_blocked_module
from carver.spine.s27_v2_replay.positive_action_cost_executable import _cost_bundle_hash_payload
from carver.spine.s27_v2_replay.positive_action_pnl_blocked_executable import (
    ACTUAL_PNL_LEDGER_STATUS,
    BACKTEST_RESULT_STATUS,
    PNL_ACCOUNTING_REQUIRED_LABEL,
    PNL_BLOCKED_NON_AUTHORIZATIONS,
    PNL_BLOCKED_ROW_STATUS,
    RESULT_EMISSION_STATUS,
    S27_V2_POSITIVE_ACTION_PNL_BLOCKED_AUTHORIZATION,
    S27_V2_POSITIVE_ACTION_PNL_BLOCKED_STATUS,
    VALUATION_END_MARK_POLICY_STATUS,
    _pnl_blocked_bundle_hash_payload,
    _pnl_blocked_row_hash_payload,
    _policy_hash,
    build_positive_action_pnl_blocked_metadata,
)


POSITIVE_ACTION_PACK_PATH = (
    ROOT
    / "docs"
    / "researchops"
    / "s27_v2_local_replay_inputs"
    / "ZN"
    / "20260609_positive_action_recon_znm6_20260413T13_declared_pack"
)


@pytest.fixture(scope="module")
def active_pnl_blocked_bundle():
    return build_positive_action_pnl_blocked_metadata(POSITIVE_ACTION_PACK_PATH)


def _rehash_row(row):
    return replace(row, row_hash=canonical_sha256(_pnl_blocked_row_hash_payload(row)))


def _rehash_bundle(bundle):
    return replace(bundle, bundle_hash=canonical_sha256(_pnl_blocked_bundle_hash_payload(bundle)))


def test_positive_action_pnl_blocked_builds_metadata_only(active_pnl_blocked_bundle):
    bundle = active_pnl_blocked_bundle
    row = bundle.pnl_blocked_row

    assert bundle.status == S27_V2_POSITIVE_ACTION_PNL_BLOCKED_STATUS
    assert bundle.authorization_label == S27_V2_POSITIVE_ACTION_PNL_BLOCKED_AUTHORIZATION
    assert row.row_status == PNL_BLOCKED_ROW_STATUS
    assert row.raw_symbol == "ZNM6"
    assert row.selected_fill_timestamp_utc == "2026-04-13T14:00:00Z"
    assert row.fill_quantity == 1
    assert row.fill_price == pytest.approx(111.046875)
    assert row.position_before_fill == 0
    assert row.position_after_fill == -1
    assert row.pnl_accounting_required_label == PNL_ACCOUNTING_REQUIRED_LABEL
    assert row.pnl_accounting_required_by_filled_position is True
    assert row.numeric_cost_policy_status == "FAIL_CLOSED_NUMERIC_ZN_COMMISSION_POLICY_UNRESOLVED"
    assert row.inferred_retail_cost_status == "NOT_AUTHORIZED_INFERRED_RETAIL_FUTURES_COST_REQUIRES_OPERATOR_ACCEPTANCE"
    assert row.actual_cost_ledger_status == "FAIL_CLOSED_ACTUAL_COST_LEDGER_NOT_EMITTED_NUMERIC_COST_POLICY_UNRESOLVED"
    assert row.actual_cost_rows_emitted is False
    assert row.valuation_end_mark_policy_status == VALUATION_END_MARK_POLICY_STATUS
    assert row.actual_pnl_ledger_status == ACTUAL_PNL_LEDGER_STATUS
    assert row.actual_pnl_rows_emitted is False
    assert row.pnl_rows_emitted is False
    assert row.result_emission_status == RESULT_EMISSION_STATUS
    assert row.result_rows_emitted is False
    assert row.backtest_result_status == BACKTEST_RESULT_STATUS
    assert row.backtest_result_emitted is False
    assert row.result_interpretation_emitted is False
    assert row.pnl_evaluation_emitted is False
    assert row.source_faithful_evidence_claimed is False
    assert row.pnl_amount == "NOT_APPLICABLE"
    assert row.pnl_currency == "NOT_APPLICABLE"

    assert bundle.pnl_blocked_metadata_rows_emitted is True
    assert bundle.actual_cost_rows_emitted is False
    assert bundle.actual_pnl_rows_emitted is False
    assert bundle.result_rows_emitted is False
    assert bundle.backtest_result_emitted is False
    assert bundle.result_interpretation_emitted is False
    assert bundle.pnl_evaluation_emitted is False
    assert bundle.source_faithful_evidence_claimed is False
    assert bundle.non_authorizations == PNL_BLOCKED_NON_AUTHORIZATIONS


def test_positive_action_pnl_blocked_row_is_not_standalone_authority(active_pnl_blocked_bundle):
    with pytest.raises(CarverBlocked, match="standalone validation is not authoritative"):
        active_pnl_blocked_bundle.pnl_blocked_row.validate()


def test_positive_action_pnl_blocked_rejects_out_of_scope_pack(tmp_path):
    with pytest.raises(CarverBlocked, match="locked to the declared positive-action pack"):
        build_positive_action_pnl_blocked_metadata(tmp_path)


def test_positive_action_pnl_blocked_rejects_forged_cost_bundle(active_pnl_blocked_bundle):
    cost_bundle = replace(active_pnl_blocked_bundle.cost_bundle, source_faithful_evidence_claimed=True)
    cost_bundle = replace(cost_bundle, bundle_hash=canonical_sha256(_cost_bundle_hash_payload(cost_bundle)))
    forged = _rehash_bundle(replace(active_pnl_blocked_bundle, cost_bundle=cost_bundle))

    with pytest.raises(CarverBlocked):
        forged.validate()


@pytest.mark.parametrize(
    ("field_name", "forged_value"),
    (
        ("cost_bundle_hash", "1" * 64),
        ("cost_evidence_row_hash", "2" * 64),
        ("fill_bundle_hash", "3" * 64),
        ("limit_fill_row_hash", "4" * 64),
        ("fill_quantity", 2),
        ("fill_price", 111.09375),
        ("position_before_fill", 1),
        ("position_after_fill", 0),
        ("pnl_accounting_required_label", "FORGED_NO_PNL_ACCOUNTING"),
        ("pnl_accounting_required_by_filled_position", False),
        ("numeric_cost_policy_status", "PASS_FORGED_NUMERIC_COST"),
        ("inferred_retail_cost_status", "PASS_FORGED_INFERRED_RETAIL_COST_ACCEPTED"),
        ("actual_cost_ledger_status", "PASS_FORGED_COST_LEDGER"),
        ("actual_cost_rows_emitted", True),
        ("valuation_end_mark_policy_status", "PASS_FORGED_VALUATION_END_MARK_POLICY"),
        ("actual_pnl_ledger_status", "PASS_FORGED_PNL_LEDGER"),
        ("actual_pnl_rows_emitted", True),
        ("pnl_rows_emitted", True),
        ("result_emission_status", "PASS_FORGED_RESULT_ROW"),
        ("result_rows_emitted", True),
        ("backtest_result_status", "PASS_FORGED_BACKTEST_RESULT"),
        ("backtest_result_emitted", True),
        ("result_interpretation_emitted", True),
        ("pnl_evaluation_emitted", True),
        ("source_faithful_evidence_claimed", True),
        ("pnl_amount", "12.34"),
        ("pnl_currency", "USD"),
    ),
)
def test_positive_action_pnl_blocked_rejects_self_consistent_row_forgery(
    active_pnl_blocked_bundle,
    field_name,
    forged_value,
):
    row = replace(active_pnl_blocked_bundle.pnl_blocked_row, **{field_name: forged_value})
    row = replace(
        row,
        pnl_blocked_policy_hash=_policy_hash(
            "positive_action_pnl_blocked_policy",
            row.pnl_accounting_required_label,
            row.pnl_accounting_required_by_filled_position,
            row.numeric_cost_policy_status,
            row.inferred_retail_cost_status,
            row.actual_cost_ledger_status,
            row.actual_cost_rows_emitted,
            row.valuation_end_mark_policy_status,
            row.actual_pnl_ledger_status,
            row.result_emission_status,
            row.backtest_result_status,
            row.pnl_amount,
            row.pnl_currency,
        ),
    )
    forged = _rehash_bundle(replace(active_pnl_blocked_bundle, pnl_blocked_row=_rehash_row(row)))

    with pytest.raises(CarverBlocked):
        forged.validate()


@pytest.mark.parametrize(
    "flag_name",
    (
        "actual_cost_rows_emitted",
        "actual_pnl_rows_emitted",
        "result_rows_emitted",
        "backtest_result_emitted",
        "result_interpretation_emitted",
        "pnl_evaluation_emitted",
        "source_faithful_evidence_claimed",
    ),
)
def test_positive_action_pnl_blocked_rejects_forbidden_downstream_flags(
    active_pnl_blocked_bundle,
    flag_name,
):
    forged = _rehash_bundle(replace(active_pnl_blocked_bundle, **{flag_name: True}))

    with pytest.raises(CarverBlocked, match="cannot emit cost/PnL/result/evidence"):
        forged.validate()


def test_positive_action_pnl_blocked_requires_metadata_emission_flag(active_pnl_blocked_bundle):
    forged = _rehash_bundle(replace(active_pnl_blocked_bundle, pnl_blocked_metadata_rows_emitted=False))

    with pytest.raises(CarverBlocked, match="must emit only authorized metadata"):
        forged.validate()


def test_positive_action_pnl_blocked_rejects_mutated_active_cost_status(monkeypatch, active_pnl_blocked_bundle):
    cost_row = replace(
        active_pnl_blocked_bundle.cost_bundle.cost_evidence_row,
        numeric_cost_policy_status="PASS_FORGED_NUMERIC_COST",
    )
    cost_row = replace(cost_row, row_hash=cost_row.row_hash)
    cost_bundle = replace(active_pnl_blocked_bundle.cost_bundle, cost_evidence_row=cost_row)
    cost_bundle = replace(cost_bundle, bundle_hash=canonical_sha256(_cost_bundle_hash_payload(cost_bundle)))
    monkeypatch.setattr(
        pnl_blocked_module,
        "build_positive_action_cost_executable",
        lambda _pack_path: cost_bundle,
    )

    with pytest.raises(CarverBlocked):
        active_pnl_blocked_bundle.validate()


def test_positive_action_pnl_blocked_result_backtest_status_constants_are_fail_closed():
    assert RESULT_EMISSION_STATUS == "FAIL_CLOSED_RESULT_ROW_NOT_EMITTED_NOT_AUTHORIZED"
    assert BACKTEST_RESULT_STATUS == "FAIL_CLOSED_BACKTEST_RESULT_NOT_EMITTED_NOT_AUTHORIZED"
