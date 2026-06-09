from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from carver.spine.m0 import CarverBlocked
from carver.spine.s27_v2_replay.desired_position_executable import (
    _desired_position_bundle_hash_payload,
    _desired_position_row_hash_payload,
)
from carver.spine.s27_v2_replay.local_replay import canonical_sha256
from carver.spine.s27_v2_replay.order_transition_executable import (
    FAIL_CLOSED_UNRESOLVED_NOT_EMITTED,
    NO_ORDER_KIND,
    NO_ORDER_SIDE,
    NO_POSITION_CHANGE_TRANSITION_KIND,
    ORDER_INTENT_LEDGER_ROW_STATUS,
    ORDER_TRANSITION_LEDGER_ROW_STATUS,
    PASS_ZERO_DELTA_NO_ORDER,
    S27_V2_ORDER_TRANSITION_AUTHORIZATION,
    S27_V2_ORDER_TRANSITION_STATUS,
    _check_hash,
    _evidence_check_bundle_hash,
    _order_intent_row_hash_payload,
    _order_transition_bundle_hash_payload,
    _order_transition_row_hash_payload,
    build_order_transition_executable_ledger,
)


REMEDIATION_PACK_PATH = (
    ROOT
    / "docs"
    / "researchops"
    / "s27_v2_local_replay_inputs"
    / "ZN"
    / "20260609_runtime_evidence_recon_znm6_20260413_declared_pack"
)


def test_order_transition_executable_builds_zero_delta_no_order_rows():
    bundle = build_order_transition_executable_ledger(REMEDIATION_PACK_PATH)
    intent = bundle.order_intent_row
    transition = bundle.order_transition_row

    assert bundle.status == S27_V2_ORDER_TRANSITION_STATUS
    assert bundle.authorization_label == S27_V2_ORDER_TRANSITION_AUTHORIZATION
    assert intent.row_status == ORDER_INTENT_LEDGER_ROW_STATUS
    assert transition.row_status == ORDER_TRANSITION_LEDGER_ROW_STATUS
    assert intent.raw_symbol == "ZNM6"
    assert intent.current_position_before_order == 0
    assert intent.desired_rounded_position == 0
    assert intent.position_change_contracts == 0
    assert intent.order_required is False
    assert intent.order_kind == NO_ORDER_KIND
    assert intent.order_side == NO_ORDER_SIDE
    assert intent.order_quantity == 0
    assert transition.transition_required is False
    assert transition.transition_kind == NO_POSITION_CHANGE_TRANSITION_KIND
    assert transition.ending_position_without_fill == 0
    assert transition.fill_rows_emitted is False
    assert bundle.order_intent_rows_emitted is True
    assert bundle.order_transition_rows_emitted is True
    assert bundle.limit_order_rows_emitted is False
    assert bundle.market_order_rows_emitted is False
    assert bundle.fill_rows_emitted is False
    assert bundle.cost_rows_emitted is False
    assert bundle.pnl_rows_emitted is False
    assert bundle.result_scored_run_emitted is False
    assert bundle.source_faithful_evidence_claimed is False


def test_order_transition_evidence_checks_preserve_fail_closed_execution_policy():
    checks = {
        check.label: check
        for check in build_order_transition_executable_ledger(REMEDIATION_PACK_PATH).evidence_checks
    }

    assert checks["POSITION_CHANGE_CALCULATION"].status == PASS_ZERO_DELTA_NO_ORDER
    assert checks["ADJACENT_LIMIT_ORDER_POLICY"].status == FAIL_CLOSED_UNRESOLVED_NOT_EMITTED
    assert checks["MARKET_FALLBACK_POLICY"].status == FAIL_CLOSED_UNRESOLVED_NOT_EMITTED
    assert checks["TICK_ROUNDING_POLICY"].status == FAIL_CLOSED_UNRESOLVED_NOT_EMITTED
    assert checks["WORKING_ORDER_LIFECYCLE"].status == FAIL_CLOSED_UNRESOLVED_NOT_EMITTED


def test_order_transition_rows_standalone_validate_are_not_authoritative():
    bundle = build_order_transition_executable_ledger(REMEDIATION_PACK_PATH)

    with pytest.raises(CarverBlocked, match="standalone validation is not authoritative"):
        bundle.order_intent_row.validate()
    with pytest.raises(CarverBlocked, match="standalone validation is not authoritative"):
        bundle.order_transition_row.validate()


def test_order_transition_rejects_out_of_scope_pack(tmp_path):
    with pytest.raises(CarverBlocked, match="locked to the audited remediation pack"):
        build_order_transition_executable_ledger(tmp_path)


def test_order_transition_rejects_forged_desired_position_bundle_even_with_hashes():
    bundle = build_order_transition_executable_ledger(REMEDIATION_PACK_PATH)
    desired_row = replace(bundle.desired_position_bundle.desired_position_row, desired_rounded_contracts=1)
    desired_row = replace(
        desired_row,
        row_hash=canonical_sha256(_desired_position_row_hash_payload(desired_row)),
    )
    desired_bundle = replace(bundle.desired_position_bundle, desired_position_row=desired_row)
    desired_bundle = replace(
        desired_bundle,
        bundle_hash=canonical_sha256(_desired_position_bundle_hash_payload(desired_bundle)),
    )
    forged = replace(bundle, desired_position_bundle=desired_bundle)
    forged = replace(forged, bundle_hash=canonical_sha256(_order_transition_bundle_hash_payload(forged)))

    with pytest.raises(CarverBlocked):
        forged.validate()


def test_order_transition_rejects_self_consistent_order_intent_forgery():
    bundle = build_order_transition_executable_ledger(REMEDIATION_PACK_PATH)
    intent = replace(
        bundle.order_intent_row,
        desired_rounded_position=1,
        position_change_contracts=1,
        order_required=True,
        order_kind="MARKET",
        order_side="BUY",
        order_quantity=1,
    )
    intent = replace(intent, row_hash=canonical_sha256(_order_intent_row_hash_payload(intent)))
    forged = replace(bundle, order_intent_row=intent)
    forged = replace(forged, bundle_hash=canonical_sha256(_order_transition_bundle_hash_payload(forged)))

    with pytest.raises(CarverBlocked):
        forged.validate()


def test_order_transition_rejects_self_consistent_transition_forgery():
    bundle = build_order_transition_executable_ledger(REMEDIATION_PACK_PATH)
    transition = replace(
        bundle.order_transition_row,
        desired_position_after_transition=1,
        ending_position_without_fill=1,
        position_change_contracts=1,
        transition_required=True,
    )
    transition = replace(
        transition,
        row_hash=canonical_sha256(_order_transition_row_hash_payload(transition)),
    )
    forged = replace(bundle, order_transition_row=transition)
    forged = replace(forged, bundle_hash=canonical_sha256(_order_transition_bundle_hash_payload(forged)))

    with pytest.raises(CarverBlocked):
        forged.validate()


def test_order_transition_rejects_promoted_execution_policy_check():
    bundle = build_order_transition_executable_ledger(REMEDIATION_PACK_PATH)
    checks = list(bundle.evidence_checks)
    index = [check.label for check in checks].index("ADJACENT_LIMIT_ORDER_POLICY")
    check = replace(
        checks[index],
        status="PASS_FORGED_ADJACENT_LIMIT_POLICY",
        summary="forged adjacent limit ladder",
    )
    check = replace(
        check,
        check_hash=_check_hash(check.label, check.status, check.summary, check.observed_value_hash),
    )
    checks[index] = check
    forged = replace(bundle, evidence_checks=tuple(checks))
    intent = replace(
        forged.order_intent_row,
        evidence_check_bundle_hash=_evidence_check_bundle_hash(forged.evidence_checks),
    )
    intent = replace(intent, row_hash=canonical_sha256(_order_intent_row_hash_payload(intent)))
    forged = replace(forged, order_intent_row=intent)
    forged = replace(forged, bundle_hash=canonical_sha256(_order_transition_bundle_hash_payload(forged)))

    with pytest.raises(CarverBlocked):
        forged.validate()


@pytest.mark.parametrize(
    "flag_name",
    (
        "limit_order_rows_emitted",
        "market_order_rows_emitted",
        "fill_rows_emitted",
        "cost_rows_emitted",
        "pnl_rows_emitted",
        "result_scored_run_emitted",
        "source_faithful_evidence_claimed",
    ),
)
def test_order_transition_rejects_forbidden_downstream_flags(flag_name):
    bundle = build_order_transition_executable_ledger(REMEDIATION_PACK_PATH)
    forged = replace(bundle, **{flag_name: True})
    forged = replace(forged, bundle_hash=canonical_sha256(_order_transition_bundle_hash_payload(forged)))

    with pytest.raises(CarverBlocked, match="cannot emit limit/market/fill/cost/PnL/result/evidence"):
        forged.validate()


@pytest.mark.parametrize("flag_name", ("order_intent_rows_emitted", "order_transition_rows_emitted"))
def test_order_transition_requires_authorized_non_result_rows(flag_name):
    bundle = build_order_transition_executable_ledger(REMEDIATION_PACK_PATH)
    forged = replace(bundle, **{flag_name: False})
    forged = replace(forged, bundle_hash=canonical_sha256(_order_transition_bundle_hash_payload(forged)))

    with pytest.raises(CarverBlocked, match="must emit order-intent and transition rows"):
        forged.validate()
