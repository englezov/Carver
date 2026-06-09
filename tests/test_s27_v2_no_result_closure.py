from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from carver.spine.m0 import CarverBlocked
from carver.spine.s27_v2_replay.local_replay import canonical_sha256
import carver.spine.s27_v2_replay.no_result_closure as closure_module
from carver.spine.s27_v2_replay.no_result_closure import (
    FAIL_CLOSED_RESULT_GATE_STATUS,
    METADATA_NOT_SOURCE_FAITHFUL_EVIDENCE,
    S27_V2_NO_RESULT_CLOSURE_AUTHORIZATION,
    S27_V2_NO_RESULT_CLOSURE_STATUS,
    _evidence_row_hash_payload,
    _policy_hash,
    _provenance_row_hash_payload,
    _trusted_bundle_hash_payload,
    _validation_row_hash_payload,
    build_no_result_closure_metadata,
)
from carver.spine.s27_v2_replay.no_pnl_executable import (
    _no_pnl_bundle_hash_payload,
    _no_pnl_row_hash_payload,
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
def active_closure_bundle():
    return build_no_result_closure_metadata(REMEDIATION_PACK_PATH)


def _patch_active_no_pnl(monkeypatch, bundle):
    monkeypatch.setattr(
        closure_module,
        "build_no_pnl_executable_metadata",
        lambda _pack_path: bundle.no_pnl_bundle,
    )


def _rehash_validation_row(row):
    return replace(row, row_hash=canonical_sha256(_validation_row_hash_payload(row)))


def _rehash_provenance_row(row):
    return replace(row, row_hash=canonical_sha256(_provenance_row_hash_payload(row)))


def _rehash_evidence_row(row):
    return replace(row, row_hash=canonical_sha256(_evidence_row_hash_payload(row)))


def _rehash_bundle(bundle):
    return replace(bundle, bundle_hash=canonical_sha256(_trusted_bundle_hash_payload(bundle)))


def test_no_result_closure_builds_metadata_only(active_closure_bundle):
    bundle = active_closure_bundle

    assert bundle.status == S27_V2_NO_RESULT_CLOSURE_STATUS
    assert bundle.authorization_label == S27_V2_NO_RESULT_CLOSURE_AUTHORIZATION
    assert bundle.no_pnl_bundle.no_pnl_row.order_kind == "NO_ORDER"
    assert bundle.no_pnl_bundle.no_pnl_row.order_quantity == 0
    assert bundle.validation_metadata_rows_emitted is True
    assert bundle.provenance_metadata_rows_emitted is True
    assert bundle.evidence_manifest_metadata_rows_emitted is True
    assert bundle.trusted_bundle_metadata_emitted is True
    assert bundle.actual_fill_rows_emitted is False
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
def test_no_result_closure_rows_standalone_validate_fail_closed(active_closure_bundle, row_name):
    row = getattr(active_closure_bundle, row_name)

    with pytest.raises(CarverBlocked, match="standalone validation is not authoritative"):
        row.validate()


def test_no_result_closure_rejects_out_of_scope_pack(tmp_path):
    with pytest.raises(CarverBlocked, match="locked to the audited remediation pack"):
        build_no_result_closure_metadata(tmp_path)


def test_no_result_closure_rejects_forged_no_pnl_bundle_even_with_hashes(monkeypatch, active_closure_bundle):
    bundle = active_closure_bundle
    _patch_active_no_pnl(monkeypatch, bundle)
    no_pnl_row = replace(bundle.no_pnl_bundle.no_pnl_row, pnl_rows_emitted=True)
    no_pnl_row = replace(no_pnl_row, row_hash=canonical_sha256(_no_pnl_row_hash_payload(no_pnl_row)))
    no_pnl_bundle = replace(bundle.no_pnl_bundle, no_pnl_row=no_pnl_row)
    no_pnl_bundle = replace(
        no_pnl_bundle,
        bundle_hash=canonical_sha256(_no_pnl_bundle_hash_payload(no_pnl_bundle)),
    )
    forged = _rehash_bundle(replace(bundle, no_pnl_bundle=no_pnl_bundle))

    with pytest.raises(CarverBlocked):
        forged.validate()


def test_no_result_closure_rejects_forged_external_synthesis_hash(monkeypatch, active_closure_bundle):
    bundle = active_closure_bundle
    _patch_active_no_pnl(monkeypatch, bundle)
    hashes = list(bundle.validation_row.external_pass_synthesis_hashes)
    hashes[-1] = "1" * 64
    row = replace(bundle.validation_row, external_pass_synthesis_hashes=tuple(hashes))
    row = replace(
        row,
        no_result_policy_hash=_policy_hash(
            "no_result_validation_policy",
            row.externally_passed_gate_labels,
            row.externally_passed_gate_status,
            row.external_pass_synthesis_hashes,
            row.fail_closed_result_gate_labels,
            row.fail_closed_result_gate_status,
        ),
    )
    row = _rehash_validation_row(row)
    forged = _rehash_bundle(replace(bundle, validation_row=row))

    with pytest.raises(CarverBlocked):
        forged.validate()


@pytest.mark.parametrize(
    ("field_name", "forged_value"),
    (
        ("actual_fill_ledger_emitted", True),
        ("actual_cost_ledger_emitted", True),
        ("actual_pnl_ledger_emitted", True),
        ("result_rows_emitted", True),
        ("backtest_result_emitted", True),
        ("result_interpretation_emitted", True),
        ("source_faithful_evidence_claimed", True),
    ),
)
def test_no_result_closure_rejects_forged_validation_row_flags(
    monkeypatch,
    active_closure_bundle,
    field_name,
    forged_value,
):
    bundle = active_closure_bundle
    _patch_active_no_pnl(monkeypatch, bundle)
    row = _rehash_validation_row(replace(bundle.validation_row, **{field_name: forged_value}))
    forged = _rehash_bundle(replace(bundle, validation_row=row))

    with pytest.raises(CarverBlocked):
        forged.validate()


@pytest.mark.parametrize(
    ("field_name", "forged_value"),
    (
        ("forecast_bundle_hash", "2" * 64),
        ("desired_position_bundle_hash", "3" * 64),
        ("order_transition_bundle_hash", "4" * 64),
        ("no_fill_bundle_hash", "5" * 64),
        ("no_cost_bundle_hash", "6" * 64),
        ("no_pnl_bundle_hash", "7" * 64),
        ("forecast_row_hash", "8" * 64),
        ("desired_position_row_hash", "9" * 64),
        ("order_intent_row_hash", "a" * 64),
        ("order_transition_row_hash", "b" * 64),
        ("no_fill_row_hash", "c" * 64),
        ("no_cost_row_hash", "d" * 64),
        ("no_pnl_row_hash", "e" * 64),
    ),
)
def test_no_result_closure_rejects_forged_provenance_hash_chain(
    monkeypatch,
    active_closure_bundle,
    field_name,
    forged_value,
):
    bundle = active_closure_bundle
    _patch_active_no_pnl(monkeypatch, bundle)
    row = _rehash_provenance_row(replace(bundle.provenance_row, **{field_name: forged_value}))
    forged = _rehash_bundle(replace(bundle, provenance_row=row))

    with pytest.raises(CarverBlocked):
        forged.validate()


@pytest.mark.parametrize(
    ("field_name", "forged_value"),
    (
        ("actual_fill_evidence_status", "PASS_FORGED_FILL"),
        ("actual_cost_evidence_status", "PASS_FORGED_COST"),
        ("actual_pnl_evidence_status", "PASS_FORGED_PNL"),
        ("result_evidence_status", "PASS_FORGED_RESULT"),
        ("source_faithful_evidence_status", "PASS_FORGED_SOURCE_FAITHFUL"),
        ("source_faithful_evidence_claimed", True),
    ),
)
def test_no_result_closure_rejects_forged_evidence_manifest_metadata(
    monkeypatch,
    active_closure_bundle,
    field_name,
    forged_value,
):
    bundle = active_closure_bundle
    _patch_active_no_pnl(monkeypatch, bundle)
    row = replace(bundle.evidence_row, **{field_name: forged_value})
    if field_name != "source_faithful_evidence_claimed":
        row = replace(
            row,
            no_result_evidence_policy_hash=_policy_hash(
                "no_result_evidence_manifest_policy",
                row.metadata_evidence_status,
                row.actual_fill_evidence_status,
                row.actual_cost_evidence_status,
                row.actual_pnl_evidence_status,
                row.result_evidence_status,
                row.source_faithful_evidence_status,
            ),
        )
    row = _rehash_evidence_row(row)
    forged = _rehash_bundle(replace(bundle, evidence_row=row))

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
def test_no_result_closure_requires_all_metadata_rows(monkeypatch, active_closure_bundle, flag_name):
    bundle = active_closure_bundle
    _patch_active_no_pnl(monkeypatch, bundle)
    forged = _rehash_bundle(replace(bundle, **{flag_name: False}))

    with pytest.raises(CarverBlocked, match="must emit all closure metadata rows"):
        forged.validate()


@pytest.mark.parametrize(
    "flag_name",
    (
        "actual_fill_rows_emitted",
        "actual_cost_rows_emitted",
        "actual_pnl_rows_emitted",
        "result_rows_emitted",
        "backtest_result_emitted",
        "result_interpretation_emitted",
        "pnl_evaluation_emitted",
        "source_faithful_evidence_claimed",
    ),
)
def test_no_result_closure_rejects_forbidden_bundle_flags(monkeypatch, active_closure_bundle, flag_name):
    bundle = active_closure_bundle
    _patch_active_no_pnl(monkeypatch, bundle)
    forged = _rehash_bundle(replace(bundle, **{flag_name: True}))

    with pytest.raises(CarverBlocked, match="cannot emit result/PnL/backtest/evidence"):
        forged.validate()


def test_no_result_closure_rejects_non_authorization_drift(monkeypatch, active_closure_bundle):
    bundle = active_closure_bundle
    _patch_active_no_pnl(monkeypatch, bundle)
    forged = _rehash_bundle(replace(bundle, non_authorizations=tuple()))

    with pytest.raises(CarverBlocked, match="preserve non-authorizations"):
        forged.validate()


def test_no_result_closure_not_exported_from_package_root():
    package_init = (ROOT / "src" / "carver" / "spine" / "s27_v2_replay" / "__init__.py").read_text()

    assert "no_result_closure" not in package_init
    assert "build_no_result_closure_metadata" not in package_init
