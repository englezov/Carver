from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from carver.spine.m0 import CarverBlocked
from carver.spine.s27_v2_replay.local_replay import canonical_sha256
import carver.spine.s27_v2_replay.positive_action_actual_pnl_closure as closure_module
from carver.spine.s27_v2_replay.positive_action_actual_pnl_closure import (
    ACTUAL_PNL_CLOSURE_NON_AUTHORIZATIONS,
    FAIL_CLOSED_RESULT_GATE_STATUS,
    MECHANICAL_PNL_LEDGER_STATUS,
    METADATA_NOT_SOURCE_FAITHFUL_EVIDENCE,
    S27_V2_POSITIVE_ACTION_ACTUAL_PNL_CLOSURE_AUTHORIZATION,
    S27_V2_POSITIVE_ACTION_ACTUAL_PNL_CLOSURE_STATUS,
    _evidence_row_hash_payload,
    _policy_hash,
    _provenance_row_hash_payload,
    _trusted_bundle_hash_payload,
    _validation_row_hash_payload,
    build_positive_action_actual_pnl_closure_metadata,
)
from carver.spine.s27_v2_replay.positive_action_actual_pnl_executable import _actual_pnl_bundle_hash_payload


POSITIVE_ACTION_PACK_PATH = (
    ROOT
    / "docs"
    / "researchops"
    / "s27_v2_local_replay_inputs"
    / "ZN"
    / "20260609_positive_action_recon_znm6_20260413T13_declared_pack"
)


@pytest.fixture(scope="module")
def active_closure_bundle():
    return build_positive_action_actual_pnl_closure_metadata(POSITIVE_ACTION_PACK_PATH)


def _patch_active_actual_pnl(monkeypatch, bundle):
    monkeypatch.setattr(
        closure_module,
        "build_positive_action_actual_pnl_executable",
        lambda: bundle.actual_pnl_bundle,
    )


def _rehash_validation_row(row):
    return replace(row, row_hash=canonical_sha256(_validation_row_hash_payload(row)))


def _rehash_provenance_row(row):
    return replace(row, row_hash=canonical_sha256(_provenance_row_hash_payload(row)))


def _rehash_evidence_row(row):
    return replace(row, row_hash=canonical_sha256(_evidence_row_hash_payload(row)))


def _rehash_bundle(bundle):
    return replace(bundle, bundle_hash=canonical_sha256(_trusted_bundle_hash_payload(bundle)))


def test_positive_action_actual_pnl_closure_builds_metadata_only(active_closure_bundle):
    bundle = active_closure_bundle

    assert bundle.status == S27_V2_POSITIVE_ACTION_ACTUAL_PNL_CLOSURE_STATUS
    assert bundle.authorization_label == S27_V2_POSITIVE_ACTION_ACTUAL_PNL_CLOSURE_AUTHORIZATION
    assert bundle.actual_pnl_bundle.actual_pnl_row.net_pnl_amount == pytest.approx(-2.30)
    assert bundle.validation_metadata_rows_emitted is True
    assert bundle.provenance_metadata_rows_emitted is True
    assert bundle.evidence_manifest_metadata_rows_emitted is True
    assert bundle.trusted_bundle_metadata_emitted is True
    assert bundle.actual_pnl_rows_emitted is True
    assert bundle.result_rows_emitted is False
    assert bundle.backtest_result_emitted is False
    assert bundle.result_interpretation_emitted is False
    assert bundle.pnl_evaluation_emitted is False
    assert bundle.source_faithful_evidence_claimed is False
    assert bundle.evidence_row.metadata_evidence_status == METADATA_NOT_SOURCE_FAITHFUL_EVIDENCE
    assert bundle.evidence_row.actual_pnl_ledger_status == MECHANICAL_PNL_LEDGER_STATUS
    assert bundle.evidence_row.result_evidence_status == FAIL_CLOSED_RESULT_GATE_STATUS
    assert bundle.evidence_row.backtest_evidence_status == FAIL_CLOSED_RESULT_GATE_STATUS
    assert bundle.evidence_row.pnl_evaluation_status == FAIL_CLOSED_RESULT_GATE_STATUS
    assert bundle.non_authorizations == ACTUAL_PNL_CLOSURE_NON_AUTHORIZATIONS


@pytest.mark.parametrize("row_name", ("validation_row", "provenance_row", "evidence_row"))
def test_positive_action_actual_pnl_closure_rows_standalone_validate_fail_closed(active_closure_bundle, row_name):
    row = getattr(active_closure_bundle, row_name)

    with pytest.raises(CarverBlocked, match="standalone validation is not authoritative"):
        row.validate()


def test_positive_action_actual_pnl_closure_rejects_out_of_scope_pack(tmp_path):
    with pytest.raises(CarverBlocked, match="locked to the positive-action pack"):
        build_positive_action_actual_pnl_closure_metadata(tmp_path)


def test_positive_action_actual_pnl_closure_rejects_forged_actual_pnl_bundle(monkeypatch, active_closure_bundle):
    bundle = active_closure_bundle
    _patch_active_actual_pnl(monkeypatch, bundle)
    actual_pnl = replace(bundle.actual_pnl_bundle, source_faithful_evidence_claimed=True)
    actual_pnl = replace(actual_pnl, bundle_hash=canonical_sha256(_actual_pnl_bundle_hash_payload(actual_pnl)))
    forged = _rehash_bundle(replace(bundle, actual_pnl_bundle=actual_pnl))

    with pytest.raises(CarverBlocked):
        forged.validate()


@pytest.mark.parametrize(
    ("field_name", "forged_value"),
    (
        ("actual_pnl_bundle_hash", "1" * 64),
        ("actual_pnl_row_hash", "2" * 64),
        ("passed_gate_status", "FORGED_PASS"),
        ("fail_closed_gate_status", "FORGED_RESULT_PASS"),
        ("actual_pnl_local_audit_record_sha256", "3" * 64),
        ("actual_pnl_ledger_emitted", False),
        ("result_rows_emitted", True),
        ("backtest_result_emitted", True),
        ("result_interpretation_emitted", True),
        ("pnl_evaluation_emitted", True),
        ("source_faithful_evidence_claimed", True),
    ),
)
def test_positive_action_actual_pnl_closure_rejects_forged_validation_row(
    monkeypatch,
    active_closure_bundle,
    field_name,
    forged_value,
):
    bundle = active_closure_bundle
    _patch_active_actual_pnl(monkeypatch, bundle)
    row = replace(bundle.validation_row, **{field_name: forged_value})
    row = replace(
        row,
        validation_policy_hash=_policy_hash(
            "actual_pnl_closure_validation_policy",
            row.actual_pnl_bundle_hash,
            row.actual_pnl_row_hash,
            row.passed_gate_labels,
            row.passed_gate_status,
            row.fail_closed_gate_labels,
            row.fail_closed_gate_status,
            row.actual_pnl_local_audit_record_sha256,
            row.actual_pnl_ledger_emitted,
        ),
    )
    forged = _rehash_bundle(replace(bundle, validation_row=_rehash_validation_row(row)))

    with pytest.raises(CarverBlocked):
        forged.validate()


@pytest.mark.parametrize(
    "field_name",
    (
        "positive_action_bundle_hash",
        "positive_action_row_hash",
        "forecast_component_hash",
        "desired_position_component_hash",
        "order_plan_bundle_hash",
        "limit_order_row_hash",
        "transition_plan_row_hash",
        "fill_bundle_hash",
        "fill_decision_row_hash",
        "limit_fill_row_hash",
        "actual_cost_bundle_hash",
        "actual_cost_row_hash",
        "actual_pnl_bundle_hash",
        "actual_pnl_row_hash",
        "valuation_mark_manifest_sha256",
        "valuation_mark_csv_sha256",
        "valuation_mark_local_audit_sha256",
        "actual_pnl_local_audit_record_sha256",
    ),
)
def test_positive_action_actual_pnl_closure_rejects_forged_provenance_hash_chain(
    monkeypatch,
    active_closure_bundle,
    field_name,
):
    bundle = active_closure_bundle
    _patch_active_actual_pnl(monkeypatch, bundle)
    row = _rehash_provenance_row(replace(bundle.provenance_row, **{field_name: "a" * 64}))
    forged = _rehash_bundle(replace(bundle, provenance_row=row))

    with pytest.raises(CarverBlocked):
        forged.validate()


@pytest.mark.parametrize(
    ("field_name", "forged_value"),
    (
        ("metadata_evidence_status", "FORGED_SOURCE_FAITHFUL_METADATA"),
        ("actual_pnl_ledger_status", "FORGED_RESULT_READY_PNL"),
        ("result_evidence_status", "PASS_FORGED_RESULT"),
        ("backtest_evidence_status", "PASS_FORGED_BACKTEST"),
        ("pnl_evaluation_status", "PASS_FORGED_PNL_EVAL"),
        ("source_faithful_evidence_status", "PASS_FORGED_SOURCE_FAITHFUL"),
        ("source_faithful_evidence_claimed", True),
    ),
)
def test_positive_action_actual_pnl_closure_rejects_forged_evidence_manifest(
    monkeypatch,
    active_closure_bundle,
    field_name,
    forged_value,
):
    bundle = active_closure_bundle
    _patch_active_actual_pnl(monkeypatch, bundle)
    row = replace(bundle.evidence_row, **{field_name: forged_value})
    row = replace(
        row,
        evidence_policy_hash=_policy_hash(
            "actual_pnl_closure_evidence_policy",
            row.metadata_evidence_status,
            row.actual_pnl_ledger_status,
            row.result_evidence_status,
            row.backtest_evidence_status,
            row.pnl_evaluation_status,
            row.source_faithful_evidence_status,
            row.source_faithful_evidence_claimed,
        ),
    )
    forged = _rehash_bundle(replace(bundle, evidence_row=_rehash_evidence_row(row)))

    with pytest.raises(CarverBlocked):
        forged.validate()


@pytest.mark.parametrize(
    "flag_name",
    (
        "validation_metadata_rows_emitted",
        "provenance_metadata_rows_emitted",
        "evidence_manifest_metadata_rows_emitted",
        "trusted_bundle_metadata_emitted",
        "actual_pnl_rows_emitted",
    ),
)
def test_positive_action_actual_pnl_closure_requires_required_rows(monkeypatch, active_closure_bundle, flag_name):
    bundle = active_closure_bundle
    _patch_active_actual_pnl(monkeypatch, bundle)
    forged = _rehash_bundle(replace(bundle, **{flag_name: False}))

    with pytest.raises(CarverBlocked, match="must emit actual-PnL and closure metadata rows"):
        forged.validate()


@pytest.mark.parametrize(
    "flag_name",
    (
        "result_rows_emitted",
        "backtest_result_emitted",
        "result_interpretation_emitted",
        "pnl_evaluation_emitted",
        "source_faithful_evidence_claimed",
    ),
)
def test_positive_action_actual_pnl_closure_rejects_forbidden_bundle_flags(
    monkeypatch,
    active_closure_bundle,
    flag_name,
):
    bundle = active_closure_bundle
    _patch_active_actual_pnl(monkeypatch, bundle)
    forged = _rehash_bundle(replace(bundle, **{flag_name: True}))

    with pytest.raises(CarverBlocked, match="cannot emit result/backtest/evaluation/source-faithful evidence"):
        forged.validate()


def test_positive_action_actual_pnl_closure_rejects_non_authorization_drift(monkeypatch, active_closure_bundle):
    bundle = active_closure_bundle
    _patch_active_actual_pnl(monkeypatch, bundle)
    forged = _rehash_bundle(replace(bundle, non_authorizations=tuple()))

    with pytest.raises(CarverBlocked, match="preserve non-authorizations"):
        forged.validate()


def test_positive_action_actual_pnl_closure_rejects_mutated_local_audit_record(monkeypatch, tmp_path):
    forged_record = tmp_path / "forged_actual_pnl_audit.md"
    forged_record.write_text("LOCAL_HOSTILE_AUDIT_PASS_POSITIVE_ACTION_ACTUAL_PNL_LEDGER\nFORGED\n", encoding="utf-8")
    monkeypatch.setattr(closure_module, "_ACTUAL_PNL_LOCAL_AUDIT_RECORD_PATH", forged_record)

    with pytest.raises(CarverBlocked, match="local audit record hash is not pinned"):
        build_positive_action_actual_pnl_closure_metadata(POSITIVE_ACTION_PACK_PATH)


def test_positive_action_actual_pnl_closure_not_exported_from_package_root():
    package_init = (ROOT / "src" / "carver" / "spine" / "s27_v2_replay" / "__init__.py").read_text()

    assert "positive_action_actual_pnl_closure" not in package_init
    assert "build_positive_action_actual_pnl_closure_metadata" not in package_init
