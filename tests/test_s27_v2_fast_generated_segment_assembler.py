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
from carver.spine.s27_v2_replay.fast_downstream_generator import (
    build_fast_downstream_generation,
    build_fast_downstream_policy_registry,
)
from carver.spine.s27_v2_replay.fast_generated_segment_assembler import (
    ASSEMBLY_MODE,
    STATUS,
    _assembly_payload,
    build_fast_generated_segment_assembly,
    write_fast_generated_segment_artifacts,
)
from carver.spine.s27_v2_replay.fast_order_generator import (
    build_fast_order_generation,
    build_fast_order_policy_registry,
)
from carver.spine.s27_v2_replay.fast_row_engine import build_fast_primitive_engine
from carver.spine.s27_v2_replay.fast_segment_emitter import build_fast_segment_artifacts
from carver.spine.s27_v2_replay.local_replay import canonical_sha256
from carver.spine.s27_v2_replay.test_incremental_runner import RUN_LEDGER_FILES


def _build_generated_segment():
    primitive_bundle, primitive_rows = build_fast_primitive_engine()
    artifacts, segment, _execution = build_fast_segment_artifacts()
    order_registry = build_fast_order_policy_registry(artifacts=artifacts)
    order_bundle, order_rows = build_fast_order_generation(
        primitive_bundle=primitive_bundle,
        primitive_rows=primitive_rows,
        segment_bundle=segment,
        artifacts=artifacts,
        policy_registry=order_registry,
    )
    downstream_registry = build_fast_downstream_policy_registry(
        primitive_bundle=primitive_bundle,
        segment_bundle=segment,
        artifacts=artifacts,
        order_policy_registry=order_registry,
        order_bundle=order_bundle,
        order_rows=order_rows,
    )
    downstream_bundle, downstream_rows = build_fast_downstream_generation(
        primitive_bundle=primitive_bundle,
        segment_bundle=segment,
        artifacts=artifacts,
        order_policy_registry=order_registry,
        order_bundle=order_bundle,
        order_rows=order_rows,
        downstream_policy_registry=downstream_registry,
    )
    assembly = build_fast_generated_segment_assembly(
        primitive_bundle=primitive_bundle,
        primitive_rows=primitive_rows,
        segment_bundle=segment,
        active_artifacts=artifacts,
        order_policy_registry=order_registry,
        order_bundle=order_bundle,
        order_rows=order_rows,
        downstream_policy_registry=downstream_registry,
        downstream_bundle=downstream_bundle,
        downstream_rows=downstream_rows,
    )
    return (
        primitive_bundle,
        primitive_rows,
        artifacts,
        segment,
        order_registry,
        order_bundle,
        order_rows,
        downstream_registry,
        downstream_bundle,
        downstream_rows,
        assembly,
    )


def test_fast_generated_segment_assembler_builds_generated_compact_artifacts(tmp_path):
    (
        primitive_bundle,
        primitive_rows,
        artifacts,
        segment,
        order_registry,
        order_bundle,
        order_rows,
        downstream_registry,
        downstream_bundle,
        downstream_rows,
        assembly,
    ) = _build_generated_segment()

    assert assembly.status == STATUS
    assert assembly.assembly_mode == ASSEMBLY_MODE
    assert assembly.primitive_engine_bundle_hash == primitive_bundle.bundle_hash
    assert assembly.order_generation_bundle_hash == order_bundle.bundle_hash
    assert assembly.downstream_generation_bundle_hash == downstream_bundle.bundle_hash
    assert tuple(assembly.generated_rows_by_ledger.keys()) == RUN_LEDGER_FILES
    assert assembly.generated_rows_by_ledger["runtime_history_ledger.csv"][0]["row_index"] == 704
    assert assembly.generated_rows_by_ledger["pnl_ledger.csv"][-1]["row_index"] == "1378"
    assert assembly.terminal_fail_row["row_index"] == "0"
    assert assembly.terminal_fail_row["fail_closed_reason"] == "NO_FAIL_CLOSED_BLOCKER_DECLARED_PACK_EXHAUSTED_NOT_RESULT"
    assert assembly.generated_ledger_hashes["runtime_history_ledger.csv"] != segment.segment_ledger_hashes[
        "runtime_history_ledger.csv"
    ]

    write_fast_generated_segment_artifacts(
        assembly,
        primitive_bundle=primitive_bundle,
        primitive_rows=primitive_rows,
        segment_bundle=segment,
        active_artifacts=artifacts,
        order_policy_registry=order_registry,
        order_bundle=order_bundle,
        order_rows=order_rows,
        downstream_policy_registry=downstream_registry,
        downstream_bundle=downstream_bundle,
        downstream_rows=downstream_rows,
        output_root=tmp_path,
    )

    assert (tmp_path / "generated_segment_manifest.json").exists()
    assert (tmp_path / "generated_segment_ledger_hashes.json").exists()
    assert (tmp_path / "pnl_ledger_segment.csv").exists()
    with (tmp_path / "pnl_ledger_segment.csv").open(newline="", encoding="ascii") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 675
    assert rows[0]["row_index"] == "704"
    assert rows[-1]["row_index"] == "1378"


def test_fast_generated_segment_assembler_rejects_generated_row_mutation(tmp_path):
    (
        primitive_bundle,
        primitive_rows,
        artifacts,
        segment,
        order_registry,
        order_bundle,
        order_rows,
        downstream_registry,
        downstream_bundle,
        downstream_rows,
        assembly,
    ) = _build_generated_segment()
    mutated_rows = {name: tuple(dict(row) for row in rows) for name, rows in assembly.generated_rows_by_ledger.items()}
    pnl_rows = [dict(row) for row in mutated_rows["pnl_ledger.csv"]]
    pnl_rows[-1]["row_net_pnl_amount"] = "999.0"
    mutated_rows["pnl_ledger.csv"] = tuple(pnl_rows)
    forged = replace(assembly, generated_rows_by_ledger=mutated_rows)
    forged = replace(forged, assembly_hash=canonical_sha256(_assembly_payload(forged)))

    with pytest.raises(CarverBlocked, match="row content drift"):
        write_fast_generated_segment_artifacts(
            forged,
            primitive_bundle=primitive_bundle,
            primitive_rows=primitive_rows,
            segment_bundle=segment,
            active_artifacts=artifacts,
            order_policy_registry=order_registry,
            order_bundle=order_bundle,
            order_rows=order_rows,
            downstream_policy_registry=downstream_registry,
            downstream_bundle=downstream_bundle,
            downstream_rows=downstream_rows,
            output_root=tmp_path,
        )
    assert not (tmp_path / "pnl_ledger_segment.csv").exists()


def test_fast_generated_segment_assembler_rejects_terminal_fail_mutation():
    (
        primitive_bundle,
        primitive_rows,
        artifacts,
        segment,
        order_registry,
        order_bundle,
        order_rows,
        downstream_registry,
        downstream_bundle,
        downstream_rows,
        assembly,
    ) = _build_generated_segment()
    terminal = dict(assembly.terminal_fail_row)
    terminal["market_order_required"] = "FALSE"
    forged = replace(assembly, terminal_fail_row=terminal)
    forged = replace(forged, assembly_hash=canonical_sha256(_assembly_payload(forged)))

    with pytest.raises(CarverBlocked, match="terminal fail content drift"):
        forged.validate(
            primitive_bundle=primitive_bundle,
            primitive_rows=primitive_rows,
            segment_bundle=segment,
            active_artifacts=artifacts,
            order_policy_registry=order_registry,
            order_bundle=order_bundle,
            order_rows=order_rows,
            downstream_policy_registry=downstream_registry,
            downstream_bundle=downstream_bundle,
            downstream_rows=downstream_rows,
        )


def test_fast_generated_segment_assembler_rejects_active_artifact_binding_drift():
    (
        primitive_bundle,
        primitive_rows,
        artifacts,
        segment,
        order_registry,
        order_bundle,
        order_rows,
        downstream_registry,
        downstream_bundle,
        downstream_rows,
        assembly,
    ) = _build_generated_segment()
    forged = replace(assembly, active_segment_artifacts_hash="0" * 64)
    forged = replace(forged, assembly_hash=canonical_sha256(_assembly_payload(forged)))

    with pytest.raises(CarverBlocked, match="active artifact binding drift"):
        forged.validate(
            primitive_bundle=primitive_bundle,
            primitive_rows=primitive_rows,
            segment_bundle=segment,
            active_artifacts=artifacts,
            order_policy_registry=order_registry,
            order_bundle=order_bundle,
            order_rows=order_rows,
            downstream_policy_registry=downstream_registry,
            downstream_bundle=downstream_bundle,
            downstream_rows=downstream_rows,
        )


def test_fast_generated_segment_assembler_rejects_forged_primitive_bundle_hashes():
    (
        primitive_bundle,
        primitive_rows,
        artifacts,
        segment,
        order_registry,
        order_bundle,
        order_rows,
        downstream_registry,
        downstream_bundle,
        downstream_rows,
        assembly,
    ) = _build_generated_segment()
    forged_primitive = replace(primitive_bundle, runtime_rows_hash="0" * 64)
    forged_primitive = replace(
        forged_primitive,
        bundle_hash=canonical_sha256(
            {k: v for k, v in forged_primitive.__dict__.items() if k != "bundle_hash"}
        ),
    )

    with pytest.raises(CarverBlocked, match="primitive binding drift|runtime rows hash drift|manifest hash drift"):
        assembly.validate(
            primitive_bundle=forged_primitive,
            primitive_rows=primitive_rows,
            segment_bundle=segment,
            active_artifacts=artifacts,
            order_policy_registry=order_registry,
            order_bundle=order_bundle,
            order_rows=order_rows,
            downstream_policy_registry=downstream_registry,
            downstream_bundle=downstream_bundle,
            downstream_rows=downstream_rows,
        )


def test_fast_generated_segment_assembler_rejects_stale_primitive_row_hash_payload():
    (
        primitive_bundle,
        primitive_rows,
        artifacts,
        segment,
        order_registry,
        order_bundle,
        order_rows,
        downstream_registry,
        downstream_bundle,
        downstream_rows,
        assembly,
    ) = _build_generated_segment()
    runtime_rows = [dict(row) for row in primitive_rows.runtime_rows]
    runtime_rows[703]["ewma5"] = 999.0
    forged_primitives = replace(primitive_rows, runtime_rows=tuple(runtime_rows))
    forged_primitive_bundle = replace(
        primitive_bundle,
        runtime_rows_hash=canonical_sha256(forged_primitives.runtime_rows),
    )
    forged_primitive_bundle = replace(
        forged_primitive_bundle,
        bundle_hash=canonical_sha256(
            {k: v for k, v in forged_primitive_bundle.__dict__.items() if k != "bundle_hash"}
        ),
    )
    forged_assembly = replace(assembly, primitive_engine_bundle_hash=forged_primitive_bundle.bundle_hash)
    forged_assembly = replace(forged_assembly, assembly_hash=canonical_sha256(_assembly_payload(forged_assembly)))

    with pytest.raises(CarverBlocked, match="primitive row hash content drift"):
        forged_assembly.validate(
            primitive_bundle=forged_primitive_bundle,
            primitive_rows=forged_primitives,
            segment_bundle=segment,
            active_artifacts=artifacts,
            order_policy_registry=order_registry,
            order_bundle=order_bundle,
            order_rows=order_rows,
            downstream_policy_registry=downstream_registry,
            downstream_bundle=downstream_bundle,
            downstream_rows=downstream_rows,
        )


def test_fast_generated_segment_assembler_rejects_duplicate_row_index():
    (
        primitive_bundle,
        primitive_rows,
        artifacts,
        segment,
        order_registry,
        order_bundle,
        order_rows,
        downstream_registry,
        downstream_bundle,
        downstream_rows,
        assembly,
    ) = _build_generated_segment()
    mutated_rows = {name: tuple(dict(row) for row in rows) for name, rows in assembly.generated_rows_by_ledger.items()}
    mutated_rows["market_order_ledger.csv"] = mutated_rows["market_order_ledger.csv"] + (
        dict(mutated_rows["market_order_ledger.csv"][-1]),
    )
    generated_hashes = dict(assembly.generated_ledger_hashes)
    generated_hashes["market_order_ledger.csv"] = "0" * 64
    forged = replace(assembly, generated_rows_by_ledger=mutated_rows, generated_ledger_hashes=generated_hashes)
    forged = replace(forged, assembly_hash=canonical_sha256(_assembly_payload(forged)))

    with pytest.raises(CarverBlocked, match="row content drift|duplicate row index drift"):
        forged.validate(
            primitive_bundle=primitive_bundle,
            primitive_rows=primitive_rows,
            segment_bundle=segment,
            active_artifacts=artifacts,
            order_policy_registry=order_registry,
            order_bundle=order_bundle,
            order_rows=order_rows,
            downstream_policy_registry=downstream_registry,
            downstream_bundle=downstream_bundle,
            downstream_rows=downstream_rows,
        )


def test_fast_generated_segment_assembler_is_not_exported_from_package_root():
    assert "build_fast_generated_segment_assembly" not in package_root.__all__
