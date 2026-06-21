from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from carver.spine.m0 import CarverBlocked
from carver.spine.s27_v2_replay.local_replay import canonical_sha256
from carver.spine.s27_v2_replay.no_cost_executable import (
    ACTUAL_COST_LEDGER_STATUS,
    _no_cost_bundle_hash_payload,
    _no_cost_row_hash_payload,
)
from carver.spine.s27_v2_replay.no_fill_executable import ACTUAL_FILL_LEDGER_STATUS, NOT_APPLICABLE
import carver.spine.s27_v2_replay.no_pnl_executable as no_pnl_module
from carver.spine.s27_v2_replay.no_pnl_executable import (
    ACTUAL_PNL_LEDGER_STATUS,
    NO_PNL_METADATA_ROW_STATUS,
    NO_PNL_PROVENANCE,
    S27_V2_NO_PNL_AUTHORIZATION,
    S27_V2_NO_PNL_STATUS,
    _no_pnl_bundle_hash_payload,
    _no_pnl_row_hash_payload,
    _policy_hash,
    build_no_pnl_executable_metadata,
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
def active_no_pnl_bundle():
    return build_no_pnl_executable_metadata(REMEDIATION_PACK_PATH)


def _patch_active_no_cost(monkeypatch, bundle):
    monkeypatch.setattr(
        no_pnl_module,
        "build_no_cost_executable_metadata",
        lambda _pack_path: bundle.no_cost_bundle,
    )


def test_no_pnl_executable_builds_non_result_no_pnl_metadata(active_no_pnl_bundle):
    bundle = active_no_pnl_bundle
    row = bundle.no_pnl_row

    assert bundle.status == S27_V2_NO_PNL_STATUS
    assert bundle.authorization_label == S27_V2_NO_PNL_AUTHORIZATION
    assert row.row_status == NO_PNL_METADATA_ROW_STATUS
    assert row.raw_symbol == "ZNM6"
    assert row.order_kind == NO_ORDER_KIND
    assert row.order_quantity == 0
    assert row.transition_kind == NO_POSITION_CHANGE_TRANSITION_KIND
    assert row.fill_required is False
    assert row.actual_fill_ledger_emitted is False
    assert row.actual_fill_ledger_status == ACTUAL_FILL_LEDGER_STATUS
    assert row.cost_required is False
    assert row.actual_cost_ledger_emitted is False
    assert row.actual_cost_ledger_status == ACTUAL_COST_LEDGER_STATUS
    assert row.pnl_required is False
    assert row.pnl_rows_emitted is False
    assert row.actual_pnl_ledger_emitted is False
    assert row.actual_pnl_ledger_status == ACTUAL_PNL_LEDGER_STATUS
    assert row.actual_result_row_emitted is False
    assert row.actual_backtest_result_emitted is False
    assert row.result_interpretation_emitted is False
    assert row.pnl_amount == NOT_APPLICABLE
    assert row.pnl_currency == NOT_APPLICABLE
    assert row.pnl_provenance == NO_PNL_PROVENANCE
    assert bundle.no_pnl_metadata_rows_emitted is True
    assert bundle.actual_pnl_rows_emitted is False
    assert bundle.actual_result_rows_emitted is False
    assert bundle.actual_backtest_result_emitted is False
    assert bundle.result_interpretation_emitted is False
    assert bundle.source_faithful_evidence_claimed is False


def test_no_pnl_row_standalone_validate_is_not_authoritative(active_no_pnl_bundle):
    row = active_no_pnl_bundle.no_pnl_row

    with pytest.raises(CarverBlocked, match="standalone validation is not authoritative"):
        row.validate()


def test_no_pnl_rejects_out_of_scope_pack(tmp_path):
    with pytest.raises(CarverBlocked, match="locked to the audited remediation pack"):
        build_no_pnl_executable_metadata(tmp_path)


def test_no_pnl_rejects_forged_no_cost_bundle_even_with_hashes(monkeypatch, active_no_pnl_bundle):
    bundle = active_no_pnl_bundle
    _patch_active_no_cost(monkeypatch, bundle)
    no_cost_row = replace(bundle.no_cost_bundle.no_cost_row, actual_cost_ledger_emitted=True)
    no_cost_row = replace(no_cost_row, row_hash=canonical_sha256(_no_cost_row_hash_payload(no_cost_row)))
    no_cost_bundle = replace(bundle.no_cost_bundle, no_cost_row=no_cost_row)
    no_cost_bundle = replace(
        no_cost_bundle,
        bundle_hash=canonical_sha256(_no_cost_bundle_hash_payload(no_cost_bundle)),
    )
    forged = replace(bundle, no_cost_bundle=no_cost_bundle)
    forged = replace(forged, bundle_hash=canonical_sha256(_no_pnl_bundle_hash_payload(forged)))

    with pytest.raises(CarverBlocked):
        forged.validate()


@pytest.mark.parametrize(
    ("field_name", "forged_value"),
    (
        ("pnl_required", True),
        ("pnl_rows_emitted", True),
        ("actual_pnl_ledger_emitted", True),
        ("actual_pnl_ledger_status", "PASS_FORGED_ACTUAL_PNL"),
        ("actual_result_row_emitted", True),
        ("actual_backtest_result_emitted", True),
        ("result_interpretation_emitted", True),
        ("pnl_amount", "12.34"),
        ("pnl_currency", "USD"),
        ("pnl_provenance", "FORGED_PNL_FROM_NO_COST"),
    ),
)
def test_no_pnl_rejects_self_consistent_no_pnl_row_forgery(
    monkeypatch,
    active_no_pnl_bundle,
    field_name,
    forged_value,
):
    bundle = active_no_pnl_bundle
    _patch_active_no_cost(monkeypatch, bundle)
    row = replace(bundle.no_pnl_row, **{field_name: forged_value})
    if field_name in {
        "pnl_required",
        "actual_pnl_ledger_status",
        "pnl_amount",
        "pnl_currency",
        "pnl_provenance",
    }:
        row = replace(
            row,
            no_pnl_policy_hash=_policy_hash(
                "no_pnl_policy",
                row.order_kind,
                row.order_quantity,
                row.transition_kind,
                row.fill_required,
                row.actual_fill_ledger_status,
                row.cost_required,
                row.actual_cost_ledger_status,
                row.pnl_required,
                row.actual_pnl_ledger_status,
                row.pnl_amount,
                row.pnl_currency,
                row.pnl_provenance,
            ),
        )
    row = replace(row, row_hash=canonical_sha256(_no_pnl_row_hash_payload(row)))
    forged = replace(bundle, no_pnl_row=row)
    forged = replace(forged, bundle_hash=canonical_sha256(_no_pnl_bundle_hash_payload(forged)))

    with pytest.raises(CarverBlocked):
        forged.validate()


@pytest.mark.parametrize(
    "flag_name",
    (
        "actual_pnl_rows_emitted",
        "actual_result_rows_emitted",
        "actual_backtest_result_emitted",
        "result_interpretation_emitted",
        "source_faithful_evidence_claimed",
    ),
)
def test_no_pnl_rejects_forbidden_downstream_flags(monkeypatch, active_no_pnl_bundle, flag_name):
    bundle = active_no_pnl_bundle
    _patch_active_no_cost(monkeypatch, bundle)
    forged = replace(bundle, **{flag_name: True})
    forged = replace(forged, bundle_hash=canonical_sha256(_no_pnl_bundle_hash_payload(forged)))

    with pytest.raises(CarverBlocked, match="cannot emit PnL/result/evidence"):
        forged.validate()


def test_no_pnl_requires_metadata_row_emission_flag(monkeypatch, active_no_pnl_bundle):
    bundle = active_no_pnl_bundle
    _patch_active_no_cost(monkeypatch, bundle)
    forged = replace(bundle, no_pnl_metadata_rows_emitted=False)
    forged = replace(forged, bundle_hash=canonical_sha256(_no_pnl_bundle_hash_payload(forged)))

    with pytest.raises(CarverBlocked, match="must emit no-PnL metadata"):
        forged.validate()
