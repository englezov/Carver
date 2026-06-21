from __future__ import annotations

import csv
from dataclasses import replace
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from carver.spine.m0 import CarverBlocked
import carver.spine.s27_v2_replay as package_root
from carver.spine.s27_v2_replay.local_replay import canonical_sha256
from carver.spine.s27_v2_replay.test_incremental_runner import (
    DEFAULT_BASELINE_ROW_INDEX,
    DEFAULT_SEGMENT_END_ROW_INDEX,
    DEFAULT_SEGMENT_START_ROW_INDEX,
    DEFAULT_TERMINAL_FAIL_ROW_INDEX,
    SOURCE_MODE,
    VALIDATION_MODE,
    _immutable_file_refs,
    _segment_bundle_payload,
    _segment_manifest_payload,
    _validate_dense_segment_continuity,
    _validate_segment_rows,
    _validate_timestamp_boundaries,
    build_incremental_checkpoint,
    build_incremental_segment_from_existing_artifacts,
    build_missing_tbbo_batch_plan,
    write_segment_metadata,
)


def _self_consistent_bundle_mutation(bundle, **changes):
    candidate = replace(bundle, **changes)
    manifest_hash = canonical_sha256(_segment_manifest_payload(candidate))
    candidate = replace(candidate, segment_manifest_hash=manifest_hash)
    bundle_hash = canonical_sha256(_segment_bundle_payload(candidate))
    return replace(candidate, bundle_hash=bundle_hash)


def test_incremental_checkpoint_binds_row_703_without_full_replay():
    checkpoint = build_incremental_checkpoint()

    assert checkpoint.row_index == DEFAULT_BASELINE_ROW_INDEX
    assert checkpoint.ending_position_contracts == "0"
    assert checkpoint.pnl_row_hash == "7130d2599a5571567ae416b38af0e81f19b72cf9c5237490c306568705dd85da"
    assert checkpoint.cumulative_commission_amount == "1545.5999999999995"
    checkpoint.validate()


def test_incremental_segment_validates_appended_rows_and_terminal_blocker():
    bundle = build_incremental_segment_from_existing_artifacts()

    assert bundle.validation_mode == VALIDATION_MODE
    assert bundle.source_mode == SOURCE_MODE
    assert bundle.segment_start_row_index == DEFAULT_SEGMENT_START_ROW_INDEX
    assert bundle.segment_end_row_index == DEFAULT_SEGMENT_END_ROW_INDEX
    assert bundle.segment_row_count == 675
    assert bundle.terminal_fail_row_index == DEFAULT_TERMINAL_FAIL_ROW_INDEX
    assert bundle.terminal_fail_reason == "NO_FAIL_CLOSED_BLOCKER_DECLARED_PACK_EXHAUSTED_NOT_RESULT"
    assert bundle.ledger_row_counts["pnl_ledger.csv"] == 675
    assert {704, 1374, 1378}.issubset(set(bundle.parity_rows_verified))
    bundle.validate_against_active_files()


def test_incremental_metadata_writer_emits_checkpoint_and_segment_manifests(tmp_path):
    bundle = build_incremental_segment_from_existing_artifacts()

    write_segment_metadata(bundle, tmp_path)

    assert (tmp_path / "checkpoint_manifest.json").exists()
    assert (tmp_path / "segment_manifest.json").exists()
    assert (tmp_path / "segment_ledger_hashes.json").exists()
    assert (tmp_path / "pnl_ledger_segment.csv").exists()
    assert (tmp_path / "fail_closed_ledger_terminal.csv").exists()
    with (tmp_path / "pnl_ledger_segment.csv").open(newline="", encoding="ascii") as handle:
        pnl_rows = list(csv.DictReader(handle))
    with (tmp_path / "fail_closed_ledger_terminal.csv").open(newline="", encoding="ascii") as handle:
        fail_rows = list(csv.DictReader(handle))
    assert len(pnl_rows) == 675
    assert pnl_rows[0]["row_index"] == "704"
    assert pnl_rows[-1]["row_index"] == "1378"
    assert fail_rows[0]["row_index"] == "0"
    assert fail_rows[0]["fail_closed_reason"] == "NO_FAIL_CLOSED_BLOCKER_DECLARED_PACK_EXHAUSTED_NOT_RESULT"


def test_forged_checkpoint_hash_rejects():
    checkpoint = build_incremental_checkpoint()
    forged = replace(checkpoint, trusted_checkpoint_hash="0" * 64)

    with pytest.raises(CarverBlocked, match="checkpoint hash drift"):
        forged.validate()


def test_non_row_703_checkpoint_rejects():
    with pytest.raises(CarverBlocked, match="row 703 trust baseline"):
        build_incremental_checkpoint(row_index=704)

    with pytest.raises(CarverBlocked, match="row 703 trust baseline"):
        build_incremental_segment_from_existing_artifacts(baseline_row_index=704)


def test_self_consistent_forged_segment_hash_rejects_against_active_files():
    bundle = build_incremental_segment_from_existing_artifacts()
    forged_hashes = dict(bundle.segment_ledger_hashes)
    forged_hashes["pnl_ledger.csv"] = "0" * 64
    forged = _self_consistent_bundle_mutation(bundle, segment_ledger_hashes=forged_hashes)

    with pytest.raises(CarverBlocked, match="does not match active local files"):
        forged.validate_against_active_files()


def test_dense_segment_continuity_rejects_missing_rows():
    with pytest.raises(CarverBlocked, match="dense segment rows are not contiguous"):
        _validate_dense_segment_continuity(
            "pnl_ledger.csv",
            [{"row_index": "704"}, {"row_index": "706"}],
            704,
            706,
        )


def test_segment_row_index_duplicates_reject_even_for_sparse_ledgers():
    with pytest.raises(CarverBlocked, match="row_index is duplicated"):
        _validate_segment_rows(
            "market_order_ledger.csv",
            [
                {"row_index": "1374", "row_hash": "a"},
                {"row_index": "1374", "row_hash": "b"},
            ],
        )


@pytest.mark.parametrize("timestamp", ["2022-12-31T23:00:00Z", "2024-01-01T00:00:00Z", "not-a-timestamp"])
def test_non_2023_timestamps_reject(timestamp):
    with pytest.raises(CarverBlocked, match="outside the 2023 TEST window"):
        _validate_timestamp_boundaries("pnl_ledger.csv", {"valuation_mark_timestamp_utc": timestamp})


def test_missing_immutable_file_refs_reject(tmp_path):
    run_root = ROOT / "docs/researchops/s27_v2_local_replay_runs/ZN/20260612_2023_test_mechanical_artifact_run"

    with pytest.raises(CarverBlocked, match="Missing hash-bound artifact"):
        _immutable_file_refs(tmp_path, run_root)


def test_result_or_source_faithful_flag_mutation_rejects():
    bundle = build_incremental_segment_from_existing_artifacts()
    forged = _self_consistent_bundle_mutation(
        bundle,
        non_authorizations=tuple(value for value in bundle.non_authorizations if value != "NO_SOURCE_FAITHFUL_EVIDENCE_CLAIM"),
    )

    with pytest.raises(CarverBlocked, match="non-authorizations drift"):
        forged.validate_against_active_files()


def test_missing_tbbo_batch_plan_is_deterministic_and_grouped():
    plan = build_missing_tbbo_batch_plan()

    assert plan.missing_requirement_count == 0
    assert plan.first_missing_row_index is None
    assert plan.last_missing_row_index is None
    assert plan.grouped_missing_row_indexes_by_symbol == {}
    plan.validate()


def test_incremental_runner_is_not_exported_from_package_root():
    assert "build_incremental_segment_from_existing_artifacts" not in package_root.__all__
