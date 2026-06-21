from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from carver.spine.m0 import CarverBlocked
import carver.spine.s27_v2_replay.no_fill_executable as no_fill_module
from carver.spine.s27_v2_replay.local_replay import canonical_sha256
from carver.spine.s27_v2_replay.no_fill_executable import (
    ACTUAL_FILL_LEDGER_STATUS,
    NOT_APPLICABLE,
    NO_FILL_METADATA_ROW_STATUS,
    S27_V2_NO_FILL_AUTHORIZATION,
    S27_V2_NO_FILL_STATUS,
    _no_fill_bundle_hash_payload,
    _no_fill_row_hash_payload,
    _policy_hash,
    build_no_fill_executable_metadata,
)
from carver.spine.s27_v2_replay.order_transition_executable import (
    NO_ORDER_KIND,
    NO_POSITION_CHANGE_TRANSITION_KIND,
    _order_intent_row_hash_payload,
    _order_transition_bundle_hash_payload,
    _order_transition_row_hash_payload,
)


REMEDIATION_PACK_PATH = (
    ROOT
    / "docs"
    / "researchops"
    / "s27_v2_local_replay_inputs"
    / "ZN"
    / "20260609_runtime_evidence_recon_znm6_20260413_declared_pack"
)


@pytest.fixture(scope="module")
def active_no_fill_bundle():
    return build_no_fill_executable_metadata(REMEDIATION_PACK_PATH)


def _patch_active_order_transition(monkeypatch, bundle):
    monkeypatch.setattr(
        no_fill_module,
        "build_order_transition_executable_ledger",
        lambda _pack_path: bundle.order_transition_bundle,
    )


def test_no_fill_executable_builds_non_result_no_fill_metadata(active_no_fill_bundle):
    bundle = active_no_fill_bundle
    row = bundle.no_fill_row

    assert bundle.status == S27_V2_NO_FILL_STATUS
    assert bundle.authorization_label == S27_V2_NO_FILL_AUTHORIZATION
    assert row.row_status == NO_FILL_METADATA_ROW_STATUS
    assert row.raw_symbol == "ZNM6"
    assert row.order_kind == NO_ORDER_KIND
    assert row.order_quantity == 0
    assert row.transition_kind == NO_POSITION_CHANGE_TRANSITION_KIND
    assert row.fill_required is False
    assert row.fill_rows_emitted is False
    assert row.actual_fill_ledger_emitted is False
    assert row.actual_fill_ledger_status == ACTUAL_FILL_LEDGER_STATUS
    assert row.filled_order_hash == NOT_APPLICABLE
    assert row.fill_price == NOT_APPLICABLE
    assert row.fill_quantity == 0
    assert row.fill_price_provenance == NOT_APPLICABLE
    assert bundle.no_fill_metadata_rows_emitted is True
    assert bundle.actual_fill_rows_emitted is False
    assert bundle.cost_rows_emitted is False
    assert bundle.pnl_rows_emitted is False
    assert bundle.result_scored_run_emitted is False
    assert bundle.source_faithful_evidence_claimed is False


def test_no_fill_row_standalone_validate_is_not_authoritative(active_no_fill_bundle):
    row = active_no_fill_bundle.no_fill_row

    with pytest.raises(CarverBlocked, match="standalone validation is not authoritative"):
        row.validate()


def test_no_fill_rejects_out_of_scope_pack(tmp_path):
    with pytest.raises(CarverBlocked, match="locked to the audited remediation pack"):
        build_no_fill_executable_metadata(tmp_path)


def test_no_fill_rejects_forged_order_transition_bundle_even_with_hashes(monkeypatch, active_no_fill_bundle):
    bundle = active_no_fill_bundle
    _patch_active_order_transition(monkeypatch, bundle)
    intent = replace(bundle.order_transition_bundle.order_intent_row, order_quantity=1)
    intent = replace(intent, row_hash=canonical_sha256(_order_intent_row_hash_payload(intent)))
    order_transition = replace(bundle.order_transition_bundle, order_intent_row=intent)
    order_transition = replace(
        order_transition,
        bundle_hash=canonical_sha256(_order_transition_bundle_hash_payload(order_transition)),
    )
    forged = replace(bundle, order_transition_bundle=order_transition)
    forged = replace(forged, bundle_hash=canonical_sha256(_no_fill_bundle_hash_payload(forged)))

    with pytest.raises(CarverBlocked):
        forged.validate()


def test_no_fill_rejects_active_transition_fill_flag_forgery(monkeypatch, active_no_fill_bundle):
    bundle = active_no_fill_bundle
    _patch_active_order_transition(monkeypatch, bundle)
    transition = replace(bundle.order_transition_bundle.order_transition_row, fill_rows_emitted=True)
    transition = replace(transition, row_hash=canonical_sha256(_order_transition_row_hash_payload(transition)))
    order_transition = replace(bundle.order_transition_bundle, order_transition_row=transition)
    order_transition = replace(
        order_transition,
        bundle_hash=canonical_sha256(_order_transition_bundle_hash_payload(order_transition)),
    )
    forged = replace(bundle, order_transition_bundle=order_transition)
    forged = replace(forged, bundle_hash=canonical_sha256(_no_fill_bundle_hash_payload(forged)))

    with pytest.raises(CarverBlocked):
        forged.validate()


@pytest.mark.parametrize(
    ("field_name", "forged_value"),
    (
        ("fill_required", True),
        ("fill_rows_emitted", True),
        ("actual_fill_ledger_emitted", True),
        ("actual_fill_ledger_status", "PASS_FORGED_ACTUAL_FILL"),
        ("filled_order_hash", "a" * 64),
        ("fill_price", "110.25"),
        ("fill_quantity", 1),
        ("fill_price_provenance", "MARKET_PRICE_FROM_NEXT_COMPLETED_CLOSE"),
    ),
)
def test_no_fill_rejects_self_consistent_no_fill_row_forgery(
    monkeypatch,
    active_no_fill_bundle,
    field_name,
    forged_value,
):
    bundle = active_no_fill_bundle
    _patch_active_order_transition(monkeypatch, bundle)
    row = replace(bundle.no_fill_row, **{field_name: forged_value})
    if field_name in {"fill_required", "actual_fill_ledger_status"}:
        row = replace(
            row,
            no_fill_policy_hash=_policy_hash(
                "no_fill_policy",
                row.order_kind,
                row.order_quantity,
                row.transition_kind,
                row.fill_required,
                row.actual_fill_ledger_status,
            ),
        )
    row = replace(row, row_hash=canonical_sha256(_no_fill_row_hash_payload(row)))
    forged = replace(bundle, no_fill_row=row)
    forged = replace(forged, bundle_hash=canonical_sha256(_no_fill_bundle_hash_payload(forged)))

    with pytest.raises(CarverBlocked):
        forged.validate()


@pytest.mark.parametrize(
    "flag_name",
    (
        "actual_fill_rows_emitted",
        "cost_rows_emitted",
        "pnl_rows_emitted",
        "result_scored_run_emitted",
        "source_faithful_evidence_claimed",
    ),
)
def test_no_fill_rejects_forbidden_downstream_flags(monkeypatch, active_no_fill_bundle, flag_name):
    bundle = active_no_fill_bundle
    _patch_active_order_transition(monkeypatch, bundle)
    forged = replace(bundle, **{flag_name: True})
    forged = replace(forged, bundle_hash=canonical_sha256(_no_fill_bundle_hash_payload(forged)))

    with pytest.raises(CarverBlocked, match="cannot emit fill/cost/PnL/result/evidence"):
        forged.validate()


def test_no_fill_requires_metadata_row_emission_flag(monkeypatch, active_no_fill_bundle):
    bundle = active_no_fill_bundle
    _patch_active_order_transition(monkeypatch, bundle)
    forged = replace(bundle, no_fill_metadata_rows_emitted=False)
    forged = replace(forged, bundle_hash=canonical_sha256(_no_fill_bundle_hash_payload(forged)))

    with pytest.raises(CarverBlocked, match="must emit no-fill metadata"):
        forged.validate()
