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
from carver.spine.s27_v2_replay.fast_evidence_planner import (
    FastTBBORequirementRow,
    MISSING_STATUS,
    PLANNER_MODE,
    STATUS,
    _plan_payload,
    build_fast_tbbo_requirement_plan,
    write_fast_tbbo_requirement_plan,
)
from carver.spine.s27_v2_replay.fast_segment_emitter import build_fast_segment_artifacts
from carver.spine.s27_v2_replay.local_replay import canonical_sha256


def _fake_missing_requirement_row(**changes):
    payload = {
        "row_index": 999,
        "decision_timestamp_utc": "2023-03-31T00:00:00Z",
        "fill_candidate_timestamp_utc": "2023-03-31T01:00:00Z",
        "raw_symbol": "ZNM3",
        "order_side": "SELL",
        "order_quantity": 1,
        "requirement_status": MISSING_STATUS,
        "source_ledger": "cost_ledger.csv",
        "source_row_hash": "1" * 64,
    }
    payload.update(changes)
    return FastTBBORequirementRow(row_hash=canonical_sha256(payload), **payload)


def test_fast_tbbo_requirement_plan_derives_terminal_blocker_without_legacy_requirements_ledger(tmp_path):
    artifacts, segment, execution = build_fast_segment_artifacts()

    plan = build_fast_tbbo_requirement_plan(
        artifacts=artifacts,
        segment_bundle=segment,
        execution_state_verification=execution,
    )

    assert plan.status == STATUS
    assert plan.planner_mode == PLANNER_MODE
    assert plan.supported_market_order_count > 0
    assert plan.missing_requirement_count == 0
    assert plan.first_missing_row_index is None
    assert plan.last_missing_row_index is None
    assert plan.requirement_rows == ()
    plan.validate(artifacts=artifacts, segment_bundle=segment, execution_state_verification=execution)

    write_fast_tbbo_requirement_plan(
        plan,
        artifacts=artifacts,
        segment_bundle=segment,
        execution_state_verification=execution,
        output_root=tmp_path,
    )
    assert (tmp_path / "fast_tbbo_requirement_plan.json").exists()
    with (tmp_path / "fast_tbbo_requirements.csv").open(newline="", encoding="ascii") as handle:
        rows = list(csv.DictReader(handle))
    assert rows == []


def test_fast_tbbo_requirement_plan_rejects_forged_requirement_row_hash():
    artifacts, segment, execution = build_fast_segment_artifacts()
    plan = build_fast_tbbo_requirement_plan(
        artifacts=artifacts,
        segment_bundle=segment,
        execution_state_verification=execution,
    )
    forged_row = replace(_fake_missing_requirement_row(), row_hash="0" * 64)
    forged = replace(plan, requirement_rows=(forged_row,), missing_requirement_count=1, first_missing_row_index=999, last_missing_row_index=999)
    forged = replace(forged, plan_hash=canonical_sha256(_plan_payload(forged)))

    with pytest.raises(CarverBlocked, match="requirement row hash drift"):
        forged.validate(artifacts=artifacts, segment_bundle=segment, execution_state_verification=execution)


def test_fast_tbbo_requirement_plan_rejects_self_consistent_forged_requirement_row():
    artifacts, segment, execution = build_fast_segment_artifacts()
    plan = build_fast_tbbo_requirement_plan(
        artifacts=artifacts,
        segment_bundle=segment,
        execution_state_verification=execution,
    )
    forged_row = _fake_missing_requirement_row(order_quantity=99)
    forged = replace(
        plan,
        requirement_rows=(forged_row,),
        missing_requirement_count=1,
        first_missing_row_index=999,
        last_missing_row_index=999,
    )
    forged = replace(forged, plan_hash=canonical_sha256(_plan_payload(forged)))

    with pytest.raises(CarverBlocked, match="active requirement derivation drift"):
        forged.validate(artifacts=artifacts, segment_bundle=segment, execution_state_verification=execution)


def test_fast_tbbo_requirement_writer_rejects_self_consistent_forged_plan_before_write(tmp_path):
    artifacts, segment, execution = build_fast_segment_artifacts()
    plan = build_fast_tbbo_requirement_plan(
        artifacts=artifacts,
        segment_bundle=segment,
        execution_state_verification=execution,
    )
    forged_row = _fake_missing_requirement_row()
    forged = replace(
        plan,
        requirement_rows=(forged_row,),
        missing_requirement_count=1,
        first_missing_row_index=999,
        last_missing_row_index=999,
    )
    forged = replace(forged, plan_hash=canonical_sha256(_plan_payload(forged)))

    with pytest.raises(CarverBlocked, match="active requirement derivation drift"):
        write_fast_tbbo_requirement_plan(
            forged,
            artifacts=artifacts,
            segment_bundle=segment,
            execution_state_verification=execution,
            output_root=tmp_path,
        )
    assert not (tmp_path / "fast_tbbo_requirements.csv").exists()


def test_fast_tbbo_requirement_plan_rejects_artifact_binding_drift():
    artifacts, segment, execution = build_fast_segment_artifacts()
    plan = build_fast_tbbo_requirement_plan(
        artifacts=artifacts,
        segment_bundle=segment,
        execution_state_verification=execution,
    )
    forged = replace(plan, fast_segment_artifacts_hash="0" * 64)
    forged = replace(forged, plan_hash=canonical_sha256(_plan_payload(forged)))

    with pytest.raises(CarverBlocked, match="artifacts binding drift"):
        forged.validate(artifacts=artifacts, segment_bundle=segment, execution_state_verification=execution)


def test_fast_tbbo_requirement_plan_rejects_non_2023_requirement_timestamp():
    artifacts, segment, execution = build_fast_segment_artifacts()
    plan = build_fast_tbbo_requirement_plan(
        artifacts=artifacts,
        segment_bundle=segment,
        execution_state_verification=execution,
    )
    forged_row = replace(_fake_missing_requirement_row(), fill_candidate_timestamp_utc="2024-01-01T00:00:00Z")
    forged_row = replace(forged_row, row_hash=canonical_sha256({k: v for k, v in forged_row.__dict__.items() if k != "row_hash"}))
    forged = replace(
        plan,
        requirement_rows=(forged_row,),
        missing_requirement_count=1,
        first_missing_row_index=999,
        last_missing_row_index=999,
    )
    forged = replace(forged, plan_hash=canonical_sha256(_plan_payload(forged)))

    with pytest.raises(CarverBlocked, match="outside 2023 TEST window"):
        forged.validate(artifacts=artifacts, segment_bundle=segment, execution_state_verification=execution)


def test_fast_evidence_planner_is_not_exported_from_package_root():
    assert "build_fast_tbbo_requirement_plan" not in package_root.__all__
