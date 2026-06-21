from __future__ import annotations

import inspect
import time
from dataclasses import replace
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from carver.spine.m0 import CarverBlocked
import carver.spine.s27_v2_replay as package_root
from carver.spine.s27_v2_replay.fast_test_runner import (
    FAST_MODE,
    PROOF_MODE,
    SEGMENT_MODE,
    ENGINE_STAGE,
    ARTIFACT_FAMILY_PLAN,
    FastRunnerRequest,
    _result_payload,
    run_2023_test_fast_runner,
)
from carver.spine.s27_v2_replay.fast_validation_profiles import (
    OPERATIONAL_VALIDATION_PROFILE,
)
import carver.spine.s27_v2_replay.fast_test_runner as fast_runner_module
import carver.spine.s27_v2_replay.fast_row_engine as fast_row_engine_module
import carver.spine.s27_v2_replay.fast_execution_state as fast_execution_state_module
import carver.spine.s27_v2_replay.test_incremental_runner as incremental_runner_module
from carver.spine.s27_v2_replay.local_replay import canonical_sha256
from carver.spine.s27_v2_replay.replay_artifact_cache import CacheSnapshot, Sha256ArtifactCache
from carver.spine.s27_v2_replay.test_incremental_runner import _segment_bundle_payload


def test_sha256_cache_invalidates_by_file_bytes(tmp_path):
    csv_path = tmp_path / "rows.csv"
    csv_path.write_text("row_index,value\n1,old\n", encoding="ascii")
    cache = Sha256ArtifactCache()

    first = cache.read_csv_rows(csv_path)
    first_ref = cache.file_ref(csv_path)
    csv_path.write_text("row_index,value\n1,new\n", encoding="ascii")
    second = cache.read_csv_rows(csv_path)
    second_ref = cache.file_ref(csv_path)

    assert first == [{"row_index": "1", "value": "old"}]
    assert second == [{"row_index": "1", "value": "new"}]
    assert first_ref.sha256 != second_ref.sha256
    assert cache.snapshot().cache_key


def test_json_cache_returns_deep_copy(tmp_path):
    json_path = tmp_path / "payload.json"
    json_path.write_text('{"outer":{"value":"old"}}\n', encoding="ascii")
    cache = Sha256ArtifactCache()

    first = cache.read_json(json_path)
    first["outer"]["value"] = "poisoned"
    second = cache.read_json(json_path)

    assert second["outer"]["value"] == "old"


@pytest.mark.parametrize("mode", [SEGMENT_MODE, FAST_MODE])
def test_fast_runner_modes_validate_segment_without_proof_replay(mode):
    result = run_2023_test_fast_runner(FastRunnerRequest(mode=mode))

    assert result.mode == mode
    assert result.validation_profile == OPERATIONAL_VALIDATION_PROFILE
    assert result.engine_stage == ENGINE_STAGE
    assert result.primitive_engine_bundle.row_count == 1378
    assert result.primitive_parity_report.parity_row_indexes == (1, 2, 303, 304, 547, 1374)
    assert result.execution_state_verification.segment_row_count == 675
    assert result.execution_state_verification.ending_position_contracts == 3
    assert result.generated_segment_assembly.assembly_mode == "GENERATED_PRIMITIVE_ORDER_DOWNSTREAM_ROWS_NOT_LEGACY_SLICE_COPY"
    assert result.generated_segment_assembly.segment_bundle_hash == result.segment_bundle.bundle_hash
    assert result.segment_bundle.baseline_checkpoint.row_index == 703
    assert result.segment_bundle.terminal_fail_row_index == 0
    assert result.segment_bundle.terminal_fail_reason == "NO_FAIL_CLOSED_BLOCKER_DECLARED_PACK_EXHAUSTED_NOT_RESULT"
    assert result.tbbo_batch_plan.missing_requirement_count == 0
    assert "checkpoint_manifest.json" in result.artifact_family_plan
    result.validate()


def test_fast_runner_operational_profile_finishes_segment_without_proof_replay():
    start = time.perf_counter()
    result = run_2023_test_fast_runner()
    elapsed_seconds = time.perf_counter() - start

    assert result.validation_profile == OPERATIONAL_VALIDATION_PROFILE
    assert result.segment_bundle.segment_row_count >= 500
    assert elapsed_seconds < 30.0


def test_fast_runner_operational_profile_does_not_call_active_file_replay(monkeypatch):
    def fail_if_called(self):  # noqa: ANN001 - pytest monkeypatch guard
        raise AssertionError("operational fast runner called validate_against_active_files")

    monkeypatch.setattr(
        incremental_runner_module.IncrementalSegmentBundle,
        "validate_against_active_files",
        fail_if_called,
    )

    result = run_2023_test_fast_runner()

    assert result.validation_profile == OPERATIONAL_VALIDATION_PROFILE


def test_fast_runner_rejects_unknown_validation_profile():
    with pytest.raises(CarverBlocked, match="validation profile is not recognized"):
        run_2023_test_fast_runner(FastRunnerRequest(validation_profile="UNKNOWN_PROFILE"))


def test_fast_runner_rejects_unlocked_segment_windows():
    with pytest.raises(CarverBlocked, match="row 1378"):
        run_2023_test_fast_runner(FastRunnerRequest(segment_end_row_index=1376))

    with pytest.raises(CarverBlocked, match="pack exhaustion"):
        run_2023_test_fast_runner(FastRunnerRequest(terminal_fail_row_index=1379))


def test_fast_runner_rejects_unlocked_roots_before_reading(tmp_path):
    with pytest.raises(CarverBlocked, match="pack root is locked"):
        run_2023_test_fast_runner(FastRunnerRequest(pack_root=str(tmp_path)))

    with pytest.raises(CarverBlocked, match="run root is locked"):
        run_2023_test_fast_runner(FastRunnerRequest(run_root=str(tmp_path)))

    with pytest.raises(CarverBlocked, match="TBBO requirements root is locked"):
        run_2023_test_fast_runner(FastRunnerRequest(requirements_root=str(tmp_path)))


def test_self_consistent_forged_fast_runner_metadata_rejects():
    result = run_2023_test_fast_runner()
    forged = replace(
        result,
        artifact_family_plan=tuple(item for item in ARTIFACT_FAMILY_PLAN if item != "fail_closed_ledger_terminal.csv"),
    )
    forged = replace(forged, bundle_hash=canonical_sha256(_result_payload(forged)))

    with pytest.raises(CarverBlocked, match="artifact family plan drift"):
        forged.validate()


def test_cache_snapshot_forgery_rejects():
    result = run_2023_test_fast_runner()
    forged_snapshot = replace(result.cache_snapshot, cached_file_refs=tuple())
    forged = replace(result, cache_snapshot=forged_snapshot)
    forged = replace(forged, bundle_hash=canonical_sha256(_result_payload(forged)))

    with pytest.raises(CarverBlocked, match="cache snapshot"):
        forged.validate()


def test_self_consistent_cache_ref_forgery_rejects():
    result = run_2023_test_fast_runner()
    first_ref = result.cache_snapshot.cached_file_refs[0]
    forged_ref = replace(first_ref, sha256="0" * 64)
    forged_refs = (forged_ref, *result.cache_snapshot.cached_file_refs[1:])
    forged_snapshot = CacheSnapshot(
        status=result.cache_snapshot.status,
        cached_file_refs=forged_refs,
        cache_key=canonical_sha256({"cached_file_refs": forged_refs}),
    )
    forged = replace(result, cache_snapshot=forged_snapshot)
    forged = replace(forged, bundle_hash=canonical_sha256(_result_payload(forged)))

    with pytest.raises(CarverBlocked, match="cache snapshot byte hash drift"):
        forged.validate()


def test_standalone_segment_validate_rejects_forged_window():
    result = run_2023_test_fast_runner()
    forged = replace(
        result.segment_bundle,
        segment_start_row_index=705,
        segment_row_count=result.segment_bundle.segment_row_count - 1,
    )
    forged = replace(forged, segment_manifest_hash=canonical_sha256(incremental_runner_module._segment_manifest_payload(forged)))
    forged = replace(forged, bundle_hash=canonical_sha256(_segment_bundle_payload(forged)))

    with pytest.raises(CarverBlocked, match="segment start must be row 704"):
        forged.validate()


def test_proof_mode_is_explicitly_fail_closed():
    with pytest.raises(CarverBlocked, match="PROOF_MODE_REQUIRES_SEPARATE_EXPLICIT_CHECKPOINT_GATE"):
        run_2023_test_fast_runner(FastRunnerRequest(mode=PROOF_MODE))


def test_fast_runner_does_not_import_or_call_proof_heavy_runner():
    source = (
        inspect.getsource(fast_runner_module)
        + inspect.getsource(fast_row_engine_module)
        + inspect.getsource(fast_execution_state_module)
        + inspect.getsource(incremental_runner_module)
    )

    assert "test_mechanical_run" not in source
    assert "run_2023_test_mechanical_artifacts" not in source


def test_fast_runner_is_not_exported_from_package_root():
    assert "run_2023_test_fast_runner" not in package_root.__all__
