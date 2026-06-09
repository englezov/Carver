from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from carver.spine.m0 import CarverBlocked
import carver.spine.s27_v2_replay.no_cost_executable as no_cost_module
from carver.spine.s27_v2_replay.local_replay import canonical_sha256
from carver.spine.s27_v2_replay.no_cost_executable import (
    ACTUAL_COST_LEDGER_STATUS,
    NO_COST_METADATA_ROW_STATUS,
    NO_COST_PROVENANCE,
    S27_V2_NO_COST_AUTHORIZATION,
    S27_V2_NO_COST_STATUS,
    _no_cost_bundle_hash_payload,
    _no_cost_row_hash_payload,
    _policy_hash,
    build_no_cost_executable_metadata,
)
from carver.spine.s27_v2_replay.no_fill_executable import (
    ACTUAL_FILL_LEDGER_STATUS,
    NOT_APPLICABLE,
    _no_fill_bundle_hash_payload,
    _no_fill_row_hash_payload,
)
from carver.spine.s27_v2_replay.order_transition_executable import (
    NO_ORDER_KIND,
    NO_POSITION_CHANGE_TRANSITION_KIND,
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
def active_no_cost_bundle():
    return build_no_cost_executable_metadata(REMEDIATION_PACK_PATH)


def _patch_active_no_fill(monkeypatch, bundle):
    monkeypatch.setattr(
        no_cost_module,
        "build_no_fill_executable_metadata",
        lambda _pack_path: bundle.no_fill_bundle,
    )


def test_no_cost_executable_builds_non_result_no_cost_metadata(active_no_cost_bundle):
    bundle = active_no_cost_bundle
    row = bundle.no_cost_row

    assert bundle.status == S27_V2_NO_COST_STATUS
    assert bundle.authorization_label == S27_V2_NO_COST_AUTHORIZATION
    assert row.row_status == NO_COST_METADATA_ROW_STATUS
    assert row.raw_symbol == "ZNM6"
    assert row.order_kind == NO_ORDER_KIND
    assert row.order_quantity == 0
    assert row.transition_kind == NO_POSITION_CHANGE_TRANSITION_KIND
    assert row.fill_required is False
    assert row.actual_fill_ledger_emitted is False
    assert row.actual_fill_ledger_status == ACTUAL_FILL_LEDGER_STATUS
    assert row.cost_required is False
    assert row.cost_rows_emitted is False
    assert row.actual_commission_ledger_emitted is False
    assert row.actual_spread_cost_ledger_emitted is False
    assert row.actual_cost_ledger_emitted is False
    assert row.actual_cost_ledger_status == ACTUAL_COST_LEDGER_STATUS
    assert row.commission_amount == 0.0
    assert row.spread_amount == 0.0
    assert row.spread_cost_amount == 0.0
    assert row.total_cost_amount == 0.0
    assert row.total_cost_currency == NOT_APPLICABLE
    assert row.cost_provenance == NO_COST_PROVENANCE
    assert bundle.no_cost_metadata_rows_emitted is True
    assert bundle.actual_cost_rows_emitted is False
    assert bundle.actual_commission_rows_emitted is False
    assert bundle.actual_spread_cost_rows_emitted is False
    assert bundle.pnl_rows_emitted is False
    assert bundle.result_scored_run_emitted is False
    assert bundle.source_faithful_evidence_claimed is False


def test_no_cost_row_standalone_validate_is_not_authoritative(active_no_cost_bundle):
    row = active_no_cost_bundle.no_cost_row

    with pytest.raises(CarverBlocked, match="standalone validation is not authoritative"):
        row.validate()


def test_no_cost_rejects_out_of_scope_pack(tmp_path):
    with pytest.raises(CarverBlocked, match="locked to the audited remediation pack"):
        build_no_cost_executable_metadata(tmp_path)


def test_no_cost_rejects_forged_no_fill_bundle_even_with_hashes(monkeypatch, active_no_cost_bundle):
    bundle = active_no_cost_bundle
    _patch_active_no_fill(monkeypatch, bundle)
    no_fill_row = replace(bundle.no_fill_bundle.no_fill_row, order_quantity=1)
    no_fill_row = replace(no_fill_row, row_hash=canonical_sha256(_no_fill_row_hash_payload(no_fill_row)))
    no_fill_bundle = replace(bundle.no_fill_bundle, no_fill_row=no_fill_row)
    no_fill_bundle = replace(
        no_fill_bundle,
        bundle_hash=canonical_sha256(_no_fill_bundle_hash_payload(no_fill_bundle)),
    )
    forged = replace(bundle, no_fill_bundle=no_fill_bundle)
    forged = replace(forged, bundle_hash=canonical_sha256(_no_cost_bundle_hash_payload(forged)))

    with pytest.raises(CarverBlocked):
        forged.validate()


@pytest.mark.parametrize(
    ("field_name", "forged_value"),
    (
        ("cost_required", True),
        ("cost_rows_emitted", True),
        ("actual_commission_ledger_emitted", True),
        ("actual_spread_cost_ledger_emitted", True),
        ("actual_cost_ledger_emitted", True),
        ("actual_cost_ledger_status", "PASS_FORGED_ACTUAL_COST"),
        ("commission_amount", 1.25),
        ("spread_amount", 0.015625),
        ("spread_cost_amount", 15.625),
        ("total_cost_amount", 16.875),
        ("total_cost_currency", "USD"),
        ("cost_provenance", "FORGED_COST_FROM_NO_FILL"),
    ),
)
def test_no_cost_rejects_self_consistent_no_cost_row_forgery(
    monkeypatch,
    active_no_cost_bundle,
    field_name,
    forged_value,
):
    bundle = active_no_cost_bundle
    _patch_active_no_fill(monkeypatch, bundle)
    row = replace(bundle.no_cost_row, **{field_name: forged_value})
    if field_name in {
        "cost_required",
        "actual_cost_ledger_status",
        "total_cost_amount",
    }:
        row = replace(
            row,
            no_cost_policy_hash=_policy_hash(
                "no_cost_policy",
                row.order_kind,
                row.order_quantity,
                row.transition_kind,
                row.fill_required,
                row.actual_fill_ledger_status,
                row.cost_required,
                row.actual_cost_ledger_status,
                row.total_cost_amount,
            ),
        )
    row = replace(row, row_hash=canonical_sha256(_no_cost_row_hash_payload(row)))
    forged = replace(bundle, no_cost_row=row)
    forged = replace(forged, bundle_hash=canonical_sha256(_no_cost_bundle_hash_payload(forged)))

    with pytest.raises(CarverBlocked):
        forged.validate()


@pytest.mark.parametrize(
    "flag_name",
    (
        "actual_cost_rows_emitted",
        "actual_commission_rows_emitted",
        "actual_spread_cost_rows_emitted",
        "pnl_rows_emitted",
        "result_scored_run_emitted",
        "source_faithful_evidence_claimed",
    ),
)
def test_no_cost_rejects_forbidden_downstream_flags(monkeypatch, active_no_cost_bundle, flag_name):
    bundle = active_no_cost_bundle
    _patch_active_no_fill(monkeypatch, bundle)
    forged = replace(bundle, **{flag_name: True})
    forged = replace(forged, bundle_hash=canonical_sha256(_no_cost_bundle_hash_payload(forged)))

    with pytest.raises(CarverBlocked, match="cannot emit cost/PnL/result/evidence"):
        forged.validate()


def test_no_cost_requires_metadata_row_emission_flag(monkeypatch, active_no_cost_bundle):
    bundle = active_no_cost_bundle
    _patch_active_no_fill(monkeypatch, bundle)
    forged = replace(bundle, no_cost_metadata_rows_emitted=False)
    forged = replace(forged, bundle_hash=canonical_sha256(_no_cost_bundle_hash_payload(forged)))

    with pytest.raises(CarverBlocked, match="must emit no-cost metadata"):
        forged.validate()
