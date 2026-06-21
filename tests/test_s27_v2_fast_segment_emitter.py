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
from carver.spine.s27_v2_replay.fast_segment_emitter import (
    EMISSION_MODE,
    STATUS,
    SOURCE_MODE,
    _artifact_bundle_payload,
    build_fast_segment_artifacts,
    write_fast_segment_artifacts,
)
from carver.spine.s27_v2_replay.local_replay import canonical_sha256
from carver.spine.s27_v2_replay.test_incremental_runner import (
    DEFAULT_SEGMENT_END_ROW_INDEX,
    DEFAULT_SEGMENT_START_ROW_INDEX,
    DEFAULT_TERMINAL_FAIL_ROW_INDEX,
    _segment_bundle_payload,
    _segment_manifest_payload,
)


def test_fast_segment_artifacts_materialize_rows_before_writing(tmp_path):
    artifacts, segment, execution = build_fast_segment_artifacts()

    assert artifacts.status == STATUS
    assert artifacts.emission_mode == EMISSION_MODE
    assert artifacts.source_mode == SOURCE_MODE
    assert artifacts.segment_bundle_hash == segment.bundle_hash
    assert artifacts.execution_state_verification_hash == execution.verification_hash
    assert artifacts.segment_start_row_index == DEFAULT_SEGMENT_START_ROW_INDEX
    assert artifacts.segment_end_row_index == DEFAULT_SEGMENT_END_ROW_INDEX
    assert artifacts.terminal_fail_row_index == DEFAULT_TERMINAL_FAIL_ROW_INDEX
    assert len(artifacts.segment_rows_by_ledger["pnl_ledger.csv"]) == 675
    assert artifacts.segment_rows_by_ledger["pnl_ledger.csv"][0]["row_index"] == "704"
    assert artifacts.segment_rows_by_ledger["pnl_ledger.csv"][-1]["row_index"] == "1378"
    assert artifacts.terminal_fail_row["row_index"] == "0"
    assert artifacts.terminal_fail_row["fail_closed_reason"] == "NO_FAIL_CLOSED_BLOCKER_DECLARED_PACK_EXHAUSTED_NOT_RESULT"

    write_fast_segment_artifacts(
        artifacts,
        segment_bundle=segment,
        execution_state_verification=execution,
        output_root=tmp_path,
    )

    assert (tmp_path / "fast_segment_artifacts_manifest.json").exists()
    assert (tmp_path / "segment_manifest.json").exists()
    assert (tmp_path / "pnl_ledger_segment.csv").exists()
    assert (tmp_path / "fail_closed_ledger_terminal.csv").exists()
    with (tmp_path / "pnl_ledger_segment.csv").open(newline="", encoding="ascii") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 675
    assert rows[0]["row_index"] == "704"
    assert rows[-1]["row_index"] == "1378"


def test_fast_segment_artifact_row_mutation_rejects_before_write(tmp_path):
    artifacts, segment, execution = build_fast_segment_artifacts()
    mutated_rows = {name: tuple(dict(row) for row in rows) for name, rows in artifacts.segment_rows_by_ledger.items()}
    pnl_rows = [dict(row) for row in mutated_rows["pnl_ledger.csv"]]
    pnl_rows[-1]["row_net_pnl_amount"] = "999.0"
    mutated_rows["pnl_ledger.csv"] = tuple(pnl_rows)
    forged = replace(artifacts, segment_rows_by_ledger=mutated_rows)
    forged = replace(forged, bundle_hash=canonical_sha256(_artifact_bundle_payload(forged)))

    with pytest.raises(CarverBlocked, match="row hash drift for pnl_ledger.csv"):
        write_fast_segment_artifacts(
            forged,
            segment_bundle=segment,
            execution_state_verification=execution,
            output_root=tmp_path,
        )
    assert not (tmp_path / "pnl_ledger_segment.csv").exists()


def test_fast_segment_artifact_terminal_fail_mutation_rejects():
    artifacts, segment, execution = build_fast_segment_artifacts()
    terminal = dict(artifacts.terminal_fail_row)
    terminal["row_hash"] = "0" * 64
    forged = replace(artifacts, terminal_fail_row=terminal)
    forged = replace(forged, bundle_hash=canonical_sha256(_artifact_bundle_payload(forged)))

    with pytest.raises(CarverBlocked, match="terminal fail hash drift"):
        forged.validate(segment_bundle=segment, execution_state_verification=execution)


def test_fast_segment_artifact_terminal_fail_content_mutation_rejects():
    artifacts, segment, execution = build_fast_segment_artifacts()
    terminal = dict(artifacts.terminal_fail_row)
    terminal["market_order_required"] = "FALSE"
    forged = replace(artifacts, terminal_fail_row=terminal)
    forged = replace(forged, bundle_hash=canonical_sha256(_artifact_bundle_payload(forged)))

    with pytest.raises(CarverBlocked, match="terminal fail content drift"):
        forged.validate(segment_bundle=segment, execution_state_verification=execution)


def test_fast_segment_artifact_execution_binding_rejects():
    artifacts, segment, execution = build_fast_segment_artifacts()
    forged = replace(artifacts, execution_state_verification_hash="0" * 64)
    forged = replace(forged, bundle_hash=canonical_sha256(_artifact_bundle_payload(forged)))

    with pytest.raises(CarverBlocked, match="execution-state binding drift"):
        forged.validate(segment_bundle=segment, execution_state_verification=execution)


def test_fast_segment_writer_rejects_self_consistent_forged_segment_bundle(tmp_path):
    artifacts, segment, execution = build_fast_segment_artifacts()
    forged_segment = replace(segment, terminal_fail_reason="FORGED_FAIL_REASON_NOT_ACTIVE")
    forged_segment = replace(
        forged_segment,
        segment_manifest_hash=canonical_sha256(_segment_manifest_payload(forged_segment)),
    )
    forged_segment = replace(
        forged_segment,
        bundle_hash=canonical_sha256(_segment_bundle_payload(forged_segment)),
    )
    forged_artifacts = replace(artifacts, segment_bundle_hash=forged_segment.bundle_hash)
    forged_artifacts = replace(
        forged_artifacts,
        bundle_hash=canonical_sha256(_artifact_bundle_payload(forged_artifacts)),
    )

    with pytest.raises(CarverBlocked, match="pack exhaustion"):
        write_fast_segment_artifacts(
            forged_artifacts,
            segment_bundle=forged_segment,
            execution_state_verification=execution,
            output_root=tmp_path,
        )
    assert not (tmp_path / "segment_manifest.json").exists()


def test_fast_segment_emitter_is_not_exported_from_package_root():
    assert "build_fast_segment_artifacts" not in package_root.__all__
