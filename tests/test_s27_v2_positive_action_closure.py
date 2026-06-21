from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from carver.spine.m0 import CarverBlocked
from carver.spine.s27_v2_replay.local_replay import canonical_sha256
import carver.spine.s27_v2_replay.positive_action_closure as closure_module
from carver.spine.s27_v2_replay.positive_action_closure import (
    DEFERRED_COST_PACKET_LIST_HASH,
    DEFERRED_COST_PACKET_STATUS,
    EXPECTED_DEFERRED_COST_PACKET_RECORD_SHA256,
    FAIL_CLOSED_RESULT_GATE_STATUS,
    METADATA_NOT_SOURCE_FAITHFUL_EVIDENCE,
    S27_V2_POSITIVE_ACTION_CLOSURE_AUTHORIZATION,
    S27_V2_POSITIVE_ACTION_CLOSURE_STATUS,
    _evidence_row_hash_payload,
    _policy_hash,
    _provenance_row_hash_payload,
    _trusted_bundle_hash_payload,
    _validation_row_hash_payload,
    build_positive_action_closure_metadata,
)
from carver.spine.s27_v2_replay.positive_action_pnl_blocked_executable import (
    _pnl_blocked_bundle_hash_payload,
    _pnl_blocked_row_hash_payload,
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
def active_closure_bundle():
    return build_positive_action_closure_metadata(POSITIVE_ACTION_PACK_PATH)


def _patch_active_pnl_blocked(monkeypatch, bundle):
    monkeypatch.setattr(
        closure_module,
        "build_positive_action_pnl_blocked_metadata",
        lambda _pack_path: bundle.pnl_blocked_bundle,
    )


def _rehash_validation_row(row):
    return replace(row, row_hash=canonical_sha256(_validation_row_hash_payload(row)))


def _rehash_provenance_row(row):
    return replace(row, row_hash=canonical_sha256(_provenance_row_hash_payload(row)))


def _rehash_evidence_row(row):
    return replace(row, row_hash=canonical_sha256(_evidence_row_hash_payload(row)))


def _rehash_bundle(bundle):
    return replace(bundle, bundle_hash=canonical_sha256(_trusted_bundle_hash_payload(bundle)))


def test_positive_action_closure_builds_metadata_only(active_closure_bundle):
    bundle = active_closure_bundle

    assert bundle.status == S27_V2_POSITIVE_ACTION_CLOSURE_STATUS
    assert bundle.authorization_label == S27_V2_POSITIVE_ACTION_CLOSURE_AUTHORIZATION
    assert bundle.pnl_blocked_bundle.pnl_blocked_row.pnl_accounting_required_by_filled_position is True
    assert bundle.validation_row.deferred_cost_packet_status == DEFERRED_COST_PACKET_STATUS
    assert bundle.validation_row.deferred_cost_packet_list_hash == DEFERRED_COST_PACKET_LIST_HASH
    assert bundle.validation_metadata_rows_emitted is True
    assert bundle.provenance_metadata_rows_emitted is True
    assert bundle.evidence_manifest_metadata_rows_emitted is True
    assert bundle.trusted_bundle_metadata_emitted is True
    assert bundle.actual_cost_rows_emitted is False
    assert bundle.actual_pnl_rows_emitted is False
    assert bundle.result_rows_emitted is False
    assert bundle.backtest_result_emitted is False
    assert bundle.result_interpretation_emitted is False
    assert bundle.pnl_evaluation_emitted is False
    assert bundle.source_faithful_evidence_claimed is False
    assert bundle.evidence_row.metadata_evidence_status == METADATA_NOT_SOURCE_FAITHFUL_EVIDENCE
    assert bundle.evidence_row.actual_pnl_evidence_status == FAIL_CLOSED_RESULT_GATE_STATUS


@pytest.mark.parametrize("row_name", ("validation_row", "provenance_row", "evidence_row"))
def test_positive_action_closure_rows_standalone_validate_fail_closed(active_closure_bundle, row_name):
    row = getattr(active_closure_bundle, row_name)

    with pytest.raises(CarverBlocked, match="standalone validation is not authoritative"):
        row.validate()


def test_positive_action_closure_rejects_out_of_scope_pack(tmp_path):
    with pytest.raises(CarverBlocked, match="locked to the positive-action pack"):
        build_positive_action_closure_metadata(tmp_path)


def test_positive_action_closure_rejects_forged_pnl_blocked_bundle_even_with_hashes(
    monkeypatch,
    active_closure_bundle,
):
    bundle = active_closure_bundle
    _patch_active_pnl_blocked(monkeypatch, bundle)
    pnl_row = replace(bundle.pnl_blocked_bundle.pnl_blocked_row, result_rows_emitted=True)
    pnl_row = replace(pnl_row, row_hash=canonical_sha256(_pnl_blocked_row_hash_payload(pnl_row)))
    pnl_bundle = replace(bundle.pnl_blocked_bundle, pnl_blocked_row=pnl_row)
    pnl_bundle = replace(pnl_bundle, bundle_hash=canonical_sha256(_pnl_blocked_bundle_hash_payload(pnl_bundle)))
    forged = _rehash_bundle(replace(bundle, pnl_blocked_bundle=pnl_bundle))

    with pytest.raises(CarverBlocked):
        forged.validate()


@pytest.mark.parametrize(
    ("field_name", "forged_value"),
    (
        ("deferred_cost_packet_status", "FORGED_EXTERNAL_COST_PASS"),
        ("deferred_cost_packet_list_hash", "1" * 64),
        ("deferred_cost_packet_record_sha256", "2" * 64),
        ("actual_cost_ledger_emitted", True),
        ("actual_pnl_ledger_emitted", True),
        ("result_rows_emitted", True),
        ("backtest_result_emitted", True),
        ("result_interpretation_emitted", True),
        ("pnl_evaluation_emitted", True),
        ("source_faithful_evidence_claimed", True),
    ),
)
def test_positive_action_closure_rejects_forged_validation_row(
    monkeypatch,
    active_closure_bundle,
    field_name,
    forged_value,
):
    bundle = active_closure_bundle
    _patch_active_pnl_blocked(monkeypatch, bundle)
    row = replace(bundle.validation_row, **{field_name: forged_value})
    row = replace(
        row,
        positive_action_validation_policy_hash=_policy_hash(
            "positive_action_validation_policy",
            row.passed_gate_labels,
            row.passed_gate_status,
            row.fail_closed_gate_labels,
            row.fail_closed_gate_status,
            row.deferred_cost_packet_status,
            row.deferred_cost_packet_list_hash,
            row.deferred_cost_packet_record_sha256,
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
        "cost_bundle_hash",
        "cost_evidence_row_hash",
        "pnl_blocked_bundle_hash",
        "pnl_blocked_row_hash",
        "deferred_cost_packet_record_sha256",
    ),
)
def test_positive_action_closure_rejects_forged_provenance_hash_chain(
    monkeypatch,
    active_closure_bundle,
    field_name,
):
    bundle = active_closure_bundle
    _patch_active_pnl_blocked(monkeypatch, bundle)
    row = _rehash_provenance_row(replace(bundle.provenance_row, **{field_name: "a" * 64}))
    forged = _rehash_bundle(replace(bundle, provenance_row=row))

    with pytest.raises(CarverBlocked):
        forged.validate()


@pytest.mark.parametrize(
    ("field_name", "forged_value"),
    (
        ("actual_cost_evidence_status", "PASS_FORGED_COST"),
        ("actual_pnl_evidence_status", "PASS_FORGED_PNL"),
        ("result_evidence_status", "PASS_FORGED_RESULT"),
        ("backtest_evidence_status", "PASS_FORGED_BACKTEST"),
        ("pnl_evaluation_status", "PASS_FORGED_PNL_EVAL"),
        ("source_faithful_evidence_status", "PASS_FORGED_SOURCE_FAITHFUL"),
        ("source_faithful_evidence_claimed", True),
        ("deferred_cost_packet_status", "FORGED_EXTERNAL_COST_PASS"),
    ),
)
def test_positive_action_closure_rejects_forged_evidence_manifest(
    monkeypatch,
    active_closure_bundle,
    field_name,
    forged_value,
):
    bundle = active_closure_bundle
    _patch_active_pnl_blocked(monkeypatch, bundle)
    row = replace(bundle.evidence_row, **{field_name: forged_value})
    if field_name != "source_faithful_evidence_claimed":
        row = replace(
            row,
            positive_action_evidence_policy_hash=_policy_hash(
                "positive_action_evidence_manifest_policy",
                row.metadata_evidence_status,
                row.actual_cost_evidence_status,
                row.actual_pnl_evidence_status,
                row.result_evidence_status,
                row.backtest_evidence_status,
                row.pnl_evaluation_status,
                row.source_faithful_evidence_status,
                row.deferred_cost_packet_status,
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
    ),
)
def test_positive_action_closure_requires_all_metadata_rows(monkeypatch, active_closure_bundle, flag_name):
    bundle = active_closure_bundle
    _patch_active_pnl_blocked(monkeypatch, bundle)
    forged = _rehash_bundle(replace(bundle, **{flag_name: False}))

    with pytest.raises(CarverBlocked, match="must emit all closure metadata rows"):
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
def test_positive_action_closure_rejects_forbidden_bundle_flags(monkeypatch, active_closure_bundle, flag_name):
    bundle = active_closure_bundle
    _patch_active_pnl_blocked(monkeypatch, bundle)
    forged = _rehash_bundle(replace(bundle, **{flag_name: True}))

    with pytest.raises(CarverBlocked, match="cannot emit cost/PnL/result/backtest/evidence"):
        forged.validate()


def test_positive_action_closure_rejects_non_authorization_drift(monkeypatch, active_closure_bundle):
    bundle = active_closure_bundle
    _patch_active_pnl_blocked(monkeypatch, bundle)
    forged = _rehash_bundle(replace(bundle, non_authorizations=tuple()))

    with pytest.raises(CarverBlocked, match="preserve non-authorizations"):
        forged.validate()


def test_positive_action_closure_rejects_mutated_deferred_cost_packet_bytes(monkeypatch, tmp_path):
    forged_record = tmp_path / "forged_handoff.md"
    forged_record.write_text(
        "\n".join(
            (
                "# Forged cost packet handoff",
                DEFERRED_COST_PACKET_STATUS,
                DEFERRED_COST_PACKET_LIST_HASH,
                "FORGED_EXTERNAL_COST_PASS_CLAIM",
            )
        ),
        encoding="utf-8",
    )
    assert closure_module.sha256(forged_record.read_bytes()).hexdigest() != EXPECTED_DEFERRED_COST_PACKET_RECORD_SHA256
    monkeypatch.setattr(closure_module, "_DEFERRED_COST_PACKET_RECORD_PATH", forged_record)

    with pytest.raises(CarverBlocked, match="record hash is not pinned"):
        build_positive_action_closure_metadata(POSITIVE_ACTION_PACK_PATH)


def test_positive_action_closure_not_exported_from_package_root():
    package_init = (ROOT / "src" / "carver" / "spine" / "s27_v2_replay" / "__init__.py").read_text()

    assert "positive_action_closure" not in package_init
    assert "build_positive_action_closure_metadata" not in package_init
