from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from carver.spine.m0 import CarverBlocked
from carver.spine.s27_v2_replay.local_replay import canonical_sha256
import carver.spine.s27_v2_replay.positive_action_fill_executable as fill_module
from carver.spine.s27_v2_replay.positive_action_fill_executable import (
    FILL_CONDITION_LABEL,
    FILL_DECISION_ROW_STATUS,
    FILL_NON_AUTHORIZATIONS,
    FILL_PRICE_PROVENANCE,
    LIMIT_FILL_COST_STATUS,
    LIMIT_FILL_ROW_STATUS,
    ONE_HOUR_LAG_PROOF_LABEL,
    S27_V2_POSITIVE_ACTION_FILL_AUTHORIZATION,
    S27_V2_POSITIVE_ACTION_FILL_STATUS,
    _fill_bundle_hash_payload,
    _fill_decision_row_hash_payload,
    _limit_fill_hash,
    _limit_fill_row_hash_payload,
    _policy_hash,
    build_positive_action_fill_executable,
)
from carver.spine.s27_v2_replay.positive_action_order_plan_executable import (
    _order_plan_bundle_hash_payload,
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
def active_fill_bundle():
    return build_positive_action_fill_executable(POSITIVE_ACTION_PACK_PATH)


def test_positive_action_fill_builds_actual_limit_fill_without_cost_pnl_result(active_fill_bundle):
    bundle = active_fill_bundle
    decision = bundle.fill_decision_row
    fill = bundle.limit_fill_row

    assert bundle.status == S27_V2_POSITIVE_ACTION_FILL_STATUS
    assert bundle.authorization_label == S27_V2_POSITIVE_ACTION_FILL_AUTHORIZATION
    assert decision.row_status == FILL_DECISION_ROW_STATUS
    assert decision.selected_decision_timestamp_utc == "2026-04-13T13:00:00Z"
    assert decision.selected_fill_timestamp_utc == "2026-04-13T14:00:00Z"
    assert decision.raw_symbol == "ZNM6"
    assert decision.order_side == "SELL"
    assert decision.order_quantity == 1
    assert decision.executable_tick_limit_price == pytest.approx(111.046875)
    assert decision.next_completed_close_price == pytest.approx(111.09375)
    assert decision.next_completed_close_price >= decision.executable_tick_limit_price
    assert decision.one_hour_lag_proof_label == ONE_HOUR_LAG_PROOF_LABEL
    assert decision.fill_condition_label == FILL_CONDITION_LABEL
    assert decision.fill_executed is True
    assert decision.fill_price == pytest.approx(111.046875)
    assert decision.fill_quantity == 1
    assert decision.fill_price_provenance == FILL_PRICE_PROVENANCE

    assert fill.row_status == LIMIT_FILL_ROW_STATUS
    assert fill.fill_decision_row_hash == decision.row_hash
    assert fill.limit_order_hash == bundle.order_plan_bundle.limit_order_row.limit_order_hash
    assert fill.filled_order_side == "SELL"
    assert fill.filled_order_quantity == 1
    assert fill.fill_price == pytest.approx(decision.fill_price)
    assert fill.position_before_fill == 0
    assert fill.position_after_fill == -1
    assert fill.cost_ledger_status == LIMIT_FILL_COST_STATUS
    assert fill.cost_rows_emitted is False
    assert fill.pnl_rows_emitted is False
    assert fill.result_scored_run_emitted is False
    assert fill.source_faithful_evidence_claimed is False

    assert bundle.fill_decision_metadata_rows_emitted is True
    assert bundle.actual_limit_fill_rows_emitted is True
    assert bundle.actual_market_fill_rows_emitted is False
    assert bundle.cost_rows_emitted is False
    assert bundle.pnl_rows_emitted is False
    assert bundle.result_scored_run_emitted is False
    assert bundle.source_faithful_evidence_claimed is False
    assert bundle.non_authorizations == FILL_NON_AUTHORIZATIONS


def test_positive_action_fill_rows_are_not_standalone_authority(active_fill_bundle):
    with pytest.raises(CarverBlocked, match="standalone validation is not authoritative"):
        active_fill_bundle.fill_decision_row.validate()
    with pytest.raises(CarverBlocked, match="standalone validation is not authoritative"):
        active_fill_bundle.limit_fill_row.validate()


def test_positive_action_fill_rejects_out_of_scope_pack(tmp_path):
    with pytest.raises(CarverBlocked, match="locked to the declared positive-action pack"):
        build_positive_action_fill_executable(tmp_path)


def test_positive_action_fill_rejects_forged_order_plan_bundle(active_fill_bundle):
    order_plan = replace(active_fill_bundle.order_plan_bundle, fill_rows_emitted=True)
    order_plan = replace(order_plan, bundle_hash=canonical_sha256(_order_plan_bundle_hash_payload(order_plan)))
    forged = replace(active_fill_bundle, order_plan_bundle=order_plan)
    forged = replace(forged, bundle_hash=canonical_sha256(_fill_bundle_hash_payload(forged)))

    with pytest.raises(CarverBlocked):
        forged.validate()


@pytest.mark.parametrize(
    ("field_name", "forged_value"),
    (
        ("order_side", "BUY"),
        ("order_quantity", 2),
        ("executable_tick_limit_price", 111.03125),
        ("next_completed_close_price", 111.0),
        ("hourly_fill_row_hash", "a" * 64),
        ("fill_condition_label", "FORGED_FILL_CONDITION"),
        ("fill_executed", False),
        ("fill_price", 111.09375),
        ("fill_quantity", 2),
        ("fill_price_provenance", "MARKET_PRICE_FROM_NEXT_COMPLETED_CLOSE"),
    ),
)
def test_positive_action_fill_rejects_self_consistent_decision_forgery(
    active_fill_bundle,
    field_name,
    forged_value,
):
    row = replace(active_fill_bundle.fill_decision_row, **{field_name: forged_value})
    row = replace(
        row,
        one_hour_lag_proof_hash=_policy_hash(
            "one_hour_lag_proof",
            row.one_hour_lag_proof_label,
            row.selected_decision_timestamp_utc,
            row.selected_fill_timestamp_utc,
            row.hourly_fill_row_hash,
        ),
        fill_condition_hash=_policy_hash(
            "close_only_sell_limit_fill_condition",
            row.fill_condition_label,
            row.limit_order_hash,
            row.executable_tick_limit_price,
            row.next_completed_close_price,
            row.hourly_fill_row_hash,
        ),
    )
    row = replace(row, row_hash=canonical_sha256(_fill_decision_row_hash_payload(row)))
    forged = replace(active_fill_bundle, fill_decision_row=row)
    forged = replace(forged, bundle_hash=canonical_sha256(_fill_bundle_hash_payload(forged)))

    with pytest.raises(CarverBlocked):
        forged.validate()


@pytest.mark.parametrize(
    ("field_name", "forged_value"),
    (
        ("filled_order_side", "BUY"),
        ("filled_order_quantity", 2),
        ("fill_price", 111.09375),
        ("position_before_fill", 1),
        ("position_after_fill", 0),
        ("working_order_state_before_fill_hash", "b" * 64),
        ("cost_ledger_status", "PASS_FORGED_COST_READY"),
        ("cost_rows_emitted", True),
        ("pnl_rows_emitted", True),
        ("result_scored_run_emitted", True),
        ("source_faithful_evidence_claimed", True),
    ),
)
def test_positive_action_fill_rejects_self_consistent_limit_fill_forgery(
    active_fill_bundle,
    field_name,
    forged_value,
):
    row = replace(active_fill_bundle.limit_fill_row, **{field_name: forged_value})
    row = replace(row, fill_ledger_hash=_limit_fill_hash(row))
    row = replace(row, row_hash=canonical_sha256(_limit_fill_row_hash_payload(row)))
    forged = replace(active_fill_bundle, limit_fill_row=row)
    forged = replace(forged, bundle_hash=canonical_sha256(_fill_bundle_hash_payload(forged)))

    with pytest.raises(CarverBlocked):
        forged.validate()


@pytest.mark.parametrize(
    "flag_name",
    (
        "actual_market_fill_rows_emitted",
        "cost_rows_emitted",
        "pnl_rows_emitted",
        "result_scored_run_emitted",
        "source_faithful_evidence_claimed",
    ),
)
def test_positive_action_fill_rejects_forbidden_downstream_flags(active_fill_bundle, flag_name):
    forged = replace(active_fill_bundle, **{flag_name: True})
    forged = replace(forged, bundle_hash=canonical_sha256(_fill_bundle_hash_payload(forged)))

    with pytest.raises(CarverBlocked, match="cannot emit market/cost/PnL/result/evidence"):
        forged.validate()


def test_positive_action_fill_rejects_missing_limit_fill_emission_flag(active_fill_bundle):
    forged = replace(active_fill_bundle, actual_limit_fill_rows_emitted=False)
    forged = replace(forged, bundle_hash=canonical_sha256(_fill_bundle_hash_payload(forged)))

    with pytest.raises(CarverBlocked, match="must emit only authorized fill metadata/surface"):
        forged.validate()


def test_positive_action_fill_rejects_mutated_active_fill_candidate(monkeypatch):
    active_row = dict(fill_module._locked_hourly_fill_row(POSITIVE_ACTION_PACK_PATH))
    active_row["close_price"] = "111.0"
    monkeypatch.setattr(fill_module, "_locked_hourly_fill_row", lambda _pack_path: active_row)

    with pytest.raises(CarverBlocked, match="sell limit is not crossed"):
        build_positive_action_fill_executable(POSITIVE_ACTION_PACK_PATH)
