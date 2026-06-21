from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from carver.spine.m0 import CarverBlocked
from carver.spine.s27_v2_replay.local_replay import canonical_sha256
from carver.spine.s27_v2_replay.positive_action_executable import _positive_action_bundle_hash_payload
import carver.spine.s27_v2_replay.positive_action_order_plan_executable as order_plan
from carver.spine.s27_v2_replay.positive_action_order_plan_executable import (
    LIMIT_ORDER_PLAN_ROW_STATUS,
    NORMAL_TRANSITION_PLAN_ROW_STATUS,
    NO_MARKET_ORDER_PROOF_LABEL,
    ORDER_PLAN_NON_AUTHORIZATIONS,
    SELL_TICK_ROUNDING_DIRECTION,
    S27_V2_POSITIVE_ACTION_ORDER_PLAN_AUTHORIZATION,
    S27_V2_POSITIVE_ACTION_ORDER_PLAN_STATUS,
    TICK_ROUNDING_POLICY_LABEL,
    ZN_TICK_SIZE,
    _limit_order_row_hash_payload,
    _order_plan_bundle_hash_payload,
    _round_limit_price_to_executable_tick,
    _transition_plan_row_hash_payload,
    build_positive_action_limit_order_plan,
)


POSITIVE_ACTION_PACK_PATH = (
    ROOT
    / "docs"
    / "researchops"
    / "s27_v2_local_replay_inputs"
    / "ZN"
    / "20260609_positive_action_recon_znm6_20260413T13_declared_pack"
)


def test_positive_action_order_plan_builds_sell_limit_order_without_downstream_rows():
    bundle = build_positive_action_limit_order_plan(POSITIVE_ACTION_PACK_PATH)
    row = bundle.limit_order_row
    transition = bundle.transition_plan_row

    assert bundle.status == S27_V2_POSITIVE_ACTION_ORDER_PLAN_STATUS
    assert bundle.authorization_label == S27_V2_POSITIVE_ACTION_ORDER_PLAN_AUTHORIZATION
    assert row.row_status == LIMIT_ORDER_PLAN_ROW_STATUS
    assert row.selected_decision_timestamp_utc == "2026-04-13T13:00:00Z"
    assert row.selected_fill_timestamp_utc == "2026-04-13T14:00:00Z"
    assert row.raw_symbol == "ZNM6"
    assert row.current_position_before_order == 0
    assert row.target_position_after_fill == -1
    assert row.position_change_contracts == -1
    assert row.order_required is True
    assert row.order_kind == "LIMIT"
    assert row.order_side == "SELL"
    assert row.order_quantity == 1
    assert row.formula_implied_limit_price > bundle.positive_action_bundle.positive_action_row.hourly_current_price_value
    assert row.executable_tick_limit_price >= row.formula_implied_limit_price
    assert row.executable_tick_limit_price == pytest.approx(
        _round_limit_price_to_executable_tick(row.formula_implied_limit_price, "SELL", ZN_TICK_SIZE)
    )
    assert row.tick_size == ZN_TICK_SIZE
    assert row.tick_value == 15.625
    assert row.tick_rounding_policy_label == TICK_ROUNDING_POLICY_LABEL
    assert row.tick_rounding_direction == SELL_TICK_ROUNDING_DIRECTION
    assert row.no_market_order_proof_label == NO_MARKET_ORDER_PROOF_LABEL
    assert row.provider_contract_multiplier_field_value == "2147483647"
    assert row.contract_point_value == 1000.0
    assert row.actual_market_order_rows_emitted is False
    assert row.actual_fill_rows_emitted is False
    assert row.actual_cost_rows_emitted is False
    assert row.actual_pnl_rows_emitted is False

    assert transition.row_status == NORMAL_TRANSITION_PLAN_ROW_STATUS
    assert transition.limit_order_hash == row.limit_order_hash
    assert transition.order_plan_hash == row.order_plan_hash
    assert transition.session_proof_label == "PASS_LOCAL_SAME_SESSION_DECISION_FILL_CANDIDATE"
    assert transition.roll_proof_label == "PASS_LOCAL_NO_ROLL_BOUNDARY_ON_SELECTED_TRADING_DATE"
    assert transition.fill_rows_emitted is False
    assert transition.actual_fill_ledger_status == "FAIL_CLOSED_ACTUAL_FILL_LEDGER_NOT_EMITTED"

    assert bundle.limit_order_rows_emitted is True
    assert bundle.market_order_rows_emitted is False
    assert bundle.transition_metadata_rows_emitted is True
    assert bundle.fill_rows_emitted is False
    assert bundle.cost_rows_emitted is False
    assert bundle.pnl_rows_emitted is False
    assert bundle.result_scored_run_emitted is False
    assert bundle.source_faithful_evidence_claimed is False
    assert bundle.non_authorizations == ORDER_PLAN_NON_AUTHORIZATIONS


def test_positive_action_order_plan_formula_matches_active_positive_row():
    bundle = build_positive_action_limit_order_plan(POSITIVE_ACTION_PACK_PATH)
    active = bundle.positive_action_bundle.positive_action_row
    row = bundle.limit_order_row

    target_capped_forecast = -1 / active.base_unrounded_contracts * 10.0
    expected_formula = (
        active.ewma5_equilibrium_value
        - (target_capped_forecast / 20.0 / active.ewma10_multiplier_m_value) * active.sigma_price_value
    )

    assert row.formula_implied_limit_price == pytest.approx(expected_formula)
    assert row.executable_tick_limit_price % ZN_TICK_SIZE == pytest.approx(0.0)


@pytest.mark.parametrize(
    ("price", "side", "expected"),
    (
        (100.001, "SELL", 100.015625),
        (100.015625, "SELL", 100.015625),
        (100.014, "BUY", 100.0),
        (100.015625, "BUY", 100.015625),
    ),
)
def test_executable_tick_rounding_policy(price, side, expected):
    assert _round_limit_price_to_executable_tick(price, side, ZN_TICK_SIZE) == pytest.approx(expected)


def test_positive_action_order_plan_rejects_out_of_scope_pack(tmp_path):
    with pytest.raises(CarverBlocked, match="locked to the declared positive-action pack"):
        build_positive_action_limit_order_plan(tmp_path)


def test_positive_action_order_plan_rows_are_not_standalone_authority():
    bundle = build_positive_action_limit_order_plan(POSITIVE_ACTION_PACK_PATH)

    with pytest.raises(CarverBlocked, match="standalone validation is not authoritative"):
        bundle.limit_order_row.validate()
    with pytest.raises(CarverBlocked, match="standalone validation is not authoritative"):
        bundle.transition_plan_row.validate()


def test_positive_action_order_plan_rejects_forged_positive_action_bundle():
    bundle = build_positive_action_limit_order_plan(POSITIVE_ACTION_PACK_PATH)
    positive = replace(bundle.positive_action_bundle, source_faithful_evidence_claimed=True)
    positive = replace(positive, bundle_hash=canonical_sha256(_positive_action_bundle_hash_payload(positive)))
    forged = replace(bundle, positive_action_bundle=positive)
    forged = replace(forged, bundle_hash=canonical_sha256(_order_plan_bundle_hash_payload(forged)))

    with pytest.raises(CarverBlocked):
        forged.validate()


@pytest.mark.parametrize(
    ("field_name", "forged_value"),
    (
        ("target_position_after_fill", 0),
        ("order_side", "BUY"),
        ("order_quantity", 2),
        ("formula_implied_limit_price", 100.0),
        ("executable_tick_limit_price", 100.0),
        ("tick_size", 0.03125),
        ("tick_rounding_direction", "ROUND_DOWN_TO_NEAREST_ZN_TICK_FOR_SELL_LIMIT"),
        ("provider_contract_multiplier_field_value", "1000"),
        ("actual_market_order_rows_emitted", True),
        ("actual_fill_rows_emitted", True),
        ("actual_cost_rows_emitted", True),
        ("actual_pnl_rows_emitted", True),
    ),
)
def test_positive_action_order_plan_rejects_self_consistent_limit_row_forgery(field_name, forged_value):
    bundle = build_positive_action_limit_order_plan(POSITIVE_ACTION_PACK_PATH)
    row = replace(bundle.limit_order_row, **{field_name: forged_value})
    row = replace(
        row,
        order_plan_hash=order_plan._order_plan_hash(row),
        limit_order_hash=order_plan._limit_order_hash(row),
    )
    row = replace(row, row_hash=canonical_sha256(_limit_order_row_hash_payload(row)))
    forged = replace(bundle, limit_order_row=row)
    forged = replace(forged, bundle_hash=canonical_sha256(_order_plan_bundle_hash_payload(forged)))

    with pytest.raises(CarverBlocked):
        forged.validate()


@pytest.mark.parametrize(
    "flag_name",
    (
        "market_order_rows_emitted",
        "fill_rows_emitted",
        "cost_rows_emitted",
        "pnl_rows_emitted",
        "result_scored_run_emitted",
        "source_faithful_evidence_claimed",
    ),
)
def test_positive_action_order_plan_rejects_forbidden_downstream_flags(flag_name):
    bundle = build_positive_action_limit_order_plan(POSITIVE_ACTION_PACK_PATH)
    forged = replace(bundle, **{flag_name: True})
    forged = replace(forged, bundle_hash=canonical_sha256(_order_plan_bundle_hash_payload(forged)))

    with pytest.raises(CarverBlocked, match="cannot emit market/fill/cost/PnL/result/evidence"):
        forged.validate()


def test_positive_action_order_plan_rejects_missing_limit_emission_flag():
    bundle = build_positive_action_limit_order_plan(POSITIVE_ACTION_PACK_PATH)
    forged = replace(bundle, limit_order_rows_emitted=False)
    forged = replace(forged, bundle_hash=canonical_sha256(_order_plan_bundle_hash_payload(forged)))

    with pytest.raises(CarverBlocked, match="must emit only authorized order metadata surfaces"):
        forged.validate()


def test_positive_action_order_plan_rejects_transition_session_proof_forgery():
    bundle = build_positive_action_limit_order_plan(POSITIVE_ACTION_PACK_PATH)
    transition = replace(bundle.transition_plan_row, session_proof_label="FORGED_SESSION_PASS")
    transition = replace(transition, row_hash=canonical_sha256(_transition_plan_row_hash_payload(transition)))
    forged = replace(bundle, transition_plan_row=transition)
    forged = replace(forged, bundle_hash=canonical_sha256(_order_plan_bundle_hash_payload(forged)))

    with pytest.raises(CarverBlocked):
        forged.validate()


def test_positive_action_order_plan_rejects_transition_fill_emission_forgery():
    bundle = build_positive_action_limit_order_plan(POSITIVE_ACTION_PACK_PATH)
    transition = replace(
        bundle.transition_plan_row,
        fill_rows_emitted=True,
        actual_fill_ledger_status="PASS_FORGED_FILL",
    )
    transition = replace(transition, row_hash=canonical_sha256(_transition_plan_row_hash_payload(transition)))
    forged = replace(bundle, transition_plan_row=transition)
    forged = replace(forged, bundle_hash=canonical_sha256(_order_plan_bundle_hash_payload(forged)))

    with pytest.raises(CarverBlocked):
        forged.validate()


def test_positive_action_order_plan_rejects_non_authorization_mutation():
    bundle = build_positive_action_limit_order_plan(POSITIVE_ACTION_PACK_PATH)
    forged = replace(bundle, non_authorizations=bundle.non_authorizations[:-1])
    forged = replace(forged, bundle_hash=canonical_sha256(_order_plan_bundle_hash_payload(forged)))

    with pytest.raises(CarverBlocked, match="preserve non-authorizations"):
        forged.validate()


def test_positive_action_order_plan_rejects_static_tick_mutation(monkeypatch):
    static_row = dict(order_plan._locked_static_zn_row())
    static_row["official_tick_size"] = "0.03125"
    monkeypatch.setattr(order_plan, "_locked_static_zn_row", lambda: static_row)

    with pytest.raises(CarverBlocked):
        build_positive_action_limit_order_plan(POSITIVE_ACTION_PACK_PATH)


def test_positive_action_order_plan_rejects_session_change(monkeypatch):
    session_row = dict(order_plan._locked_session_row())
    session_row["raw_symbol"] = "ZNU6"
    monkeypatch.setattr(order_plan, "_locked_session_row", lambda: session_row)

    with pytest.raises(CarverBlocked, match="session row must bind ZNM6"):
        build_positive_action_limit_order_plan(POSITIVE_ACTION_PACK_PATH)
