from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from carver.spine.m0 import CarverBlocked
import carver.spine.s27_v2_replay as package_root
from carver.spine.s27_v2_replay.local_replay import canonical_sha256
from carver.spine.s27_v2_replay.multi_row_development_runner import (
    MULTI_ROW_RUNNER_NON_AUTHORIZATIONS,
    RUNNER_REQUIRED_ARTIFACT_FAMILIES,
    STALE_DIAGNOSTIC_RUNNER_PATHS,
    _artifact_family_row_hash_payload,
    _policy_hash,
    _runner_machinery_bundle_hash_payload,
    _stale_runner_proof_hash_payload,
    _window_plan_hash_payload,
    build_s27_v2_multi_row_development_runner_machinery,
    execute_s27_v2_multi_row_development_backtest,
)
from carver.spine.s27_v2_replay.runner import ReplayExecutionBlocked


DECLARED_ZN_INPUT_PACK_ROOT = ROOT / "docs" / "researchops" / "s27_v2_local_replay_inputs" / "ZN"


@pytest.fixture(scope="module")
def active_runner_bundle():
    return build_s27_v2_multi_row_development_runner_machinery(DECLARED_ZN_INPUT_PACK_ROOT)


def _rehash_window_plan(row):
    return replace(row, row_hash=canonical_sha256(_window_plan_hash_payload(row)))


def _rehash_artifact_row(row):
    return replace(row, row_hash=canonical_sha256(_artifact_family_row_hash_payload(row)))


def _rehash_stale_proof(proof):
    return replace(proof, proof_hash=canonical_sha256(_stale_runner_proof_hash_payload(proof)))


def _rehash_bundle(bundle):
    return replace(bundle, bundle_hash=canonical_sha256(_runner_machinery_bundle_hash_payload(bundle)))


def test_multi_row_runner_machinery_builds_pre_run_bundle(active_runner_bundle):
    bundle = active_runner_bundle

    assert bundle.runner_machinery_ready_for_external_audit is True
    assert bundle.actual_backtest_execution_authorized is False
    assert bundle.result_scored_run_emitted is False
    assert bundle.result_interpretation_emitted is False
    assert bundle.pnl_evaluation_emitted is False
    assert bundle.source_faithful_evidence_claimed is False
    assert bundle.upstream_positive_action_closure_bundle_hash == (
        "5eb846c4fd83879c6648e9d4132d60f4fdc59ed8626453c9121496e307cacd9e"
    )
    assert bundle.upstream_positive_action_closure_record_path.endswith(
        "CARVER_S27_ZN_V2_POSITIVE_ACTION_ACTUAL_PNL_CLOSURE_IMPLEMENTATION_2026-06-11.md"
    )
    assert tuple(row.artifact_family for row in bundle.artifact_family_rows) == RUNNER_REQUIRED_ARTIFACT_FAMILIES
    assert all(row.emitted_in_this_gate is False for row in bundle.artifact_family_rows)
    assert bundle.stale_runner_exclusion_proof.forbidden_stale_runner_paths == STALE_DIAGNOSTIC_RUNNER_PATHS
    assert bundle.non_authorizations == MULTI_ROW_RUNNER_NON_AUTHORIZATIONS
    for required_non_authorization in (
        "NO_CREDENTIAL_USE",
        "NO_PARSER_EXECUTION",
        "NO_FILE_REPLAY",
        "NO_DIAGNOSTICS",
    ):
        assert required_non_authorization in bundle.non_authorizations


@pytest.mark.parametrize("row_name", ("window_plan", "stale_runner_exclusion_proof"))
def test_multi_row_runner_rows_standalone_validate_fail_closed(active_runner_bundle, row_name):
    row = getattr(active_runner_bundle, row_name)

    with pytest.raises(CarverBlocked, match="standalone validation is not authoritative"):
        row.validate()


def test_multi_row_runner_artifact_rows_standalone_validate_fail_closed(active_runner_bundle):
    with pytest.raises(CarverBlocked, match="standalone validation is not authoritative"):
        active_runner_bundle.artifact_family_rows[0].validate()


def test_multi_row_runner_execution_entrypoint_fail_closed():
    with pytest.raises(ReplayExecutionBlocked, match="separate operator run authorization"):
        execute_s27_v2_multi_row_development_backtest()


def test_multi_row_runner_rejects_out_of_scope_pack_root(tmp_path):
    with pytest.raises(CarverBlocked, match="locked to the declared local ZN input-pack root"):
        build_s27_v2_multi_row_development_runner_machinery(tmp_path)


@pytest.mark.parametrize(
    ("field_name", "forged_value"),
    (
        ("local_declared_packs_only", False),
        ("oldest_post_warmup_slice_required", False),
        ("completed_bars_only", False),
        ("strict_prior_per_row_required", False),
        ("no_oos_lockbox_forward", False),
        ("planned_row_selector_surface", "FORGED_SELECTOR"),
    ),
)
def test_multi_row_runner_rejects_window_gate_forgery(active_runner_bundle, field_name, forged_value):
    bundle = active_runner_bundle
    window = replace(bundle.window_plan, **{field_name: forged_value})
    window = replace(
        window,
        row_iteration_contract_hash=_policy_hash(
            "multi_row_window_iteration_contract",
            window.window_label,
            window.evidence_stage_label,
            str(DECLARED_ZN_INPUT_PACK_ROOT.resolve()),
            window.planned_row_selector_surface,
            window.local_declared_packs_only,
            window.oldest_post_warmup_slice_required,
            window.completed_bars_only,
            window.strict_prior_per_row_required,
            window.no_oos_lockbox_forward,
        ),
    )
    forged = _rehash_bundle(replace(bundle, window_plan=_rehash_window_plan(window)))

    with pytest.raises(CarverBlocked):
        forged.validate()


@pytest.mark.parametrize(
    ("field_name", "forged_value"),
    (
        ("per_row_artifacts_required", False),
        ("run_level_closure_required", False),
        ("fail_closed_when_evidence_insufficient", False),
        ("emitted_in_this_gate", True),
    ),
)
def test_multi_row_runner_rejects_artifact_family_forgery(active_runner_bundle, field_name, forged_value):
    bundle = active_runner_bundle
    rows = list(bundle.artifact_family_rows)
    rows[0] = _rehash_artifact_row(replace(rows[0], **{field_name: forged_value}))
    forged = _rehash_bundle(replace(bundle, artifact_family_rows=tuple(rows)))

    with pytest.raises(CarverBlocked):
        forged.validate()


@pytest.mark.parametrize(
    ("field_name", "forged_value"),
    (
        ("forbidden_stale_runner_paths", tuple(STALE_DIAGNOSTIC_RUNNER_PATHS[:-1])),
        ("stale_runner_imports_allowed", True),
        ("repo_wide_scan_required_before_run", False),
        ("package_root_export_check_required", False),
    ),
)
def test_multi_row_runner_rejects_stale_runner_proof_forgery(
    active_runner_bundle,
    field_name,
    forged_value,
):
    bundle = active_runner_bundle
    proof = replace(bundle.stale_runner_exclusion_proof, **{field_name: forged_value})
    proof = replace(
        proof,
        proof_policy_hash=_policy_hash(
            "stale_runner_import_exclusion_policy",
            proof.allowed_package_root_module,
            proof.allowed_pre_run_module,
            proof.forbidden_stale_runner_paths,
            proof.stale_runner_imports_allowed,
            proof.repo_wide_scan_required_before_run,
            proof.package_root_export_check_required,
        ),
    )
    forged = _rehash_bundle(replace(bundle, stale_runner_exclusion_proof=_rehash_stale_proof(proof)))

    with pytest.raises(CarverBlocked):
        forged.validate()


@pytest.mark.parametrize(
    ("field_name", "forged_value"),
    (
        ("upstream_positive_action_closure_bundle_hash", "1" * 64),
        ("runner_machinery_ready_for_external_audit", False),
        ("actual_backtest_execution_authorized", True),
        ("result_scored_run_emitted", True),
        ("result_interpretation_emitted", True),
        ("pnl_evaluation_emitted", True),
        ("source_faithful_evidence_claimed", True),
        ("non_authorizations", tuple()),
    ),
)
def test_multi_row_runner_rejects_bundle_forgery(active_runner_bundle, field_name, forged_value):
    bundle = active_runner_bundle
    forged = _rehash_bundle(replace(bundle, **{field_name: forged_value}))

    with pytest.raises(CarverBlocked):
        forged.validate()


def test_multi_row_runner_not_exported_from_package_root():
    package_init = (ROOT / "src" / "carver" / "spine" / "s27_v2_replay" / "__init__.py").read_text()

    assert "multi_row_development_runner" not in package_init
    assert "build_s27_v2_multi_row_development_runner_machinery" not in package_init
    assert not hasattr(package_root, "build_s27_v2_multi_row_development_runner_machinery")


def test_multi_row_runner_module_does_not_import_or_execute_stale_runner_paths():
    source = (ROOT / "src" / "carver" / "spine" / "s27_v2_replay" / "multi_row_development_runner.py").read_text()

    for stale_path in STALE_DIAGNOSTIC_RUNNER_PATHS:
        module_name = Path(stale_path).with_suffix("").as_posix().replace("/", ".")
        assert f"import {module_name}" not in source
        assert f"from {module_name}" not in source
        assert f"import_module({module_name!r}" not in source
        assert f"import_module(\"{module_name}\"" not in source
        assert f"__import__({module_name!r}" not in source
        assert f"__import__(\"{module_name}\"" not in source
        assert f"run_path({stale_path!r}" not in source
        assert f"run_path(\"{stale_path}\"" not in source
        assert f"SourceFileLoader(" not in source
        assert f"subprocess" not in source
    for dynamic_execution_surface in ("importlib", "__import__", "runpy", "SourceFileLoader", "subprocess"):
        assert dynamic_execution_surface not in source
