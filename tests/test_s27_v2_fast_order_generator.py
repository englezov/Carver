from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from carver.spine.m0 import CarverBlocked
import carver.spine.s27_v2_replay as package_root
from carver.spine.s27_v2_replay.fast_order_generator import (
    GENERATOR_MODE,
    STATUS,
    _generation_bundle_payload,
    build_fast_order_generation,
    build_fast_order_policy_registry,
)
from carver.spine.s27_v2_replay.fast_row_engine import build_fast_primitive_engine
from carver.spine.s27_v2_replay.fast_segment_emitter import build_fast_segment_artifacts
from carver.spine.s27_v2_replay.local_replay import canonical_sha256


def _build_order_generation():
    primitive_bundle, primitive_rows = build_fast_primitive_engine()
    artifacts, segment, _execution = build_fast_segment_artifacts()
    registry = build_fast_order_policy_registry(artifacts=artifacts)
    bundle, rows = build_fast_order_generation(
        primitive_bundle=primitive_bundle,
        primitive_rows=primitive_rows,
        segment_bundle=segment,
        artifacts=artifacts,
        policy_registry=registry,
    )
    return primitive_bundle, primitive_rows, artifacts, segment, registry, bundle, rows


def test_fast_order_generator_recreates_segment_order_intents_with_hash_parity():
    primitive_bundle, _primitive_rows, artifacts, segment, registry, bundle, rows = _build_order_generation()

    assert bundle.status == STATUS
    assert bundle.generator_mode == GENERATOR_MODE
    assert bundle.primitive_engine_bundle_hash == primitive_bundle.bundle_hash
    assert bundle.segment_bundle_hash == segment.bundle_hash
    assert bundle.segment_artifacts_hash == artifacts.bundle_hash
    assert bundle.policy_registry_hash == registry.registry_hash
    assert bundle.generated_row_count == 675
    assert len(rows.desired_position_rows) == 675
    assert len(rows.limit_order_rows) == 675
    assert len(rows.no_market_order_rows) == 675
    assert len(rows.market_order_rows) > 0
    assert rows.desired_position_rows[0]["row_index"] == 704
    assert rows.desired_position_rows[0]["desired_position_contracts"] == 0
    assert rows.market_order_rows[-1]["row_index"] == 1378
    assert rows.market_order_rows[-1]["order_side"] == "SELL"
    bundle.validate(
        primitive_bundle=primitive_bundle,
        segment_bundle=segment,
        artifacts=artifacts,
        policy_registry=registry,
        rows=rows,
    )


def test_fast_order_generator_rejects_generated_row_mutation():
    primitive_bundle, _primitive_rows, artifacts, segment, registry, bundle, rows = _build_order_generation()
    mutated_desired = [dict(row) for row in rows.desired_position_rows]
    mutated_desired[-1]["desired_position_contracts"] = 999
    forged_rows = replace(rows, desired_position_rows=tuple(mutated_desired))

    with pytest.raises(CarverBlocked, match="generated desired rows hash drift"):
        bundle.validate(
            primitive_bundle=primitive_bundle,
            segment_bundle=segment,
            artifacts=artifacts,
            policy_registry=registry,
            rows=forged_rows,
        )


def test_fast_order_generator_rejects_self_consistent_generated_row_mutation():
    primitive_bundle, _primitive_rows, artifacts, segment, registry, bundle, rows = _build_order_generation()
    mutated_desired = [dict(row) for row in rows.desired_position_rows]
    mutated_desired[-1]["desired_position_contracts"] = 999
    mutated_desired[-1]["row_hash"] = canonical_sha256(
        {k: v for k, v in mutated_desired[-1].items() if k != "row_hash"}
    )
    forged_rows = replace(rows, desired_position_rows=tuple(mutated_desired))
    forged = replace(
        bundle,
        desired_position_rows_hash=canonical_sha256(forged_rows.desired_position_rows),
        parity_report_hash="0" * 64,
    )
    forged = replace(forged, bundle_hash=canonical_sha256(_generation_bundle_payload(forged)))

    with pytest.raises(CarverBlocked, match="parity drift"):
        forged.validate(
            primitive_bundle=primitive_bundle,
            segment_bundle=segment,
            artifacts=artifacts,
            policy_registry=registry,
            rows=forged_rows,
        )


def test_fast_order_generator_rejects_stale_row_hash_payload_mutation():
    primitive_bundle, _primitive_rows, artifacts, segment, registry, bundle, rows = _build_order_generation()
    mutated_desired = [dict(row) for row in rows.desired_position_rows]
    mutated_desired[-1]["desired_position_contracts"] = 999
    forged_rows = replace(rows, desired_position_rows=tuple(mutated_desired))
    forged = replace(
        bundle,
        desired_position_rows_hash=canonical_sha256(forged_rows.desired_position_rows),
    )
    forged = replace(forged, bundle_hash=canonical_sha256(_generation_bundle_payload(forged)))

    with pytest.raises(CarverBlocked, match="row hash content drift"):
        forged.validate(
            primitive_bundle=primitive_bundle,
            segment_bundle=segment,
            artifacts=artifacts,
            policy_registry=registry,
            rows=forged_rows,
        )


def test_fast_order_generator_rejects_duplicate_dense_row_index_forgery():
    primitive_bundle, _primitive_rows, artifacts, segment, registry, bundle, rows = _build_order_generation()
    forged_rows = replace(rows, desired_position_rows=rows.desired_position_rows + (dict(rows.desired_position_rows[-1]),))
    forged = replace(
        bundle,
        desired_position_rows_hash=canonical_sha256(forged_rows.desired_position_rows),
        bundle_hash="0" * 64,
    )
    forged = replace(forged, bundle_hash=canonical_sha256(_generation_bundle_payload(forged)))

    with pytest.raises(CarverBlocked, match="desired row count drift"):
        forged.validate(
            primitive_bundle=primitive_bundle,
            segment_bundle=segment,
            artifacts=artifacts,
            policy_registry=registry,
            rows=forged_rows,
        )


def test_fast_order_generator_rejects_duplicate_sparse_market_row_index_forgery():
    primitive_bundle, _primitive_rows, artifacts, segment, registry, bundle, rows = _build_order_generation()
    forged_rows = replace(rows, market_order_rows=rows.market_order_rows + (dict(rows.market_order_rows[-1]),))
    forged = replace(
        bundle,
        market_order_row_count=len(forged_rows.market_order_rows),
        market_order_rows_hash=canonical_sha256(forged_rows.market_order_rows),
    )
    forged = replace(forged, bundle_hash=canonical_sha256(_generation_bundle_payload(forged)))

    with pytest.raises(CarverBlocked, match="duplicate row index drift"):
        forged.validate(
            primitive_bundle=primitive_bundle,
            segment_bundle=segment,
            artifacts=artifacts,
            policy_registry=registry,
            rows=forged_rows,
        )


def test_fast_order_generator_rejects_policy_registry_binding_drift():
    primitive_bundle, _primitive_rows, artifacts, segment, registry, bundle, rows = _build_order_generation()
    forged = replace(bundle, policy_registry_hash="0" * 64)
    forged = replace(forged, bundle_hash=canonical_sha256(_generation_bundle_payload(forged)))

    with pytest.raises(CarverBlocked, match="policy registry binding drift"):
        forged.validate(
            primitive_bundle=primitive_bundle,
            segment_bundle=segment,
            artifacts=artifacts,
            policy_registry=registry,
            rows=rows,
        )


def test_fast_order_policy_registry_rejects_artifact_binding_drift():
    _primitive_bundle, _primitive_rows, artifacts, _segment, registry, _bundle, _rows = _build_order_generation()
    forged = replace(registry, segment_artifacts_hash="0" * 64)
    forged = replace(forged, registry_hash=canonical_sha256({k: v for k, v in forged.__dict__.items() if k != "registry_hash"}))

    with pytest.raises(CarverBlocked, match="artifact binding drift"):
        forged.validate(artifacts)


def test_fast_order_policy_registry_rejects_self_consistent_row_hash_drift():
    _primitive_bundle, _primitive_rows, artifacts, _segment, registry, _bundle, _rows = _build_order_generation()
    forged = replace(registry, policy_rows_hash="0" * 64)
    forged = replace(forged, registry_hash=canonical_sha256({k: v for k, v in forged.__dict__.items() if k != "registry_hash"}))

    with pytest.raises(CarverBlocked, match="row hash drift"):
        forged.validate(artifacts)


def test_fast_order_generator_revalidates_artifacts_against_active_files():
    primitive_bundle, _primitive_rows, artifacts, segment, registry, bundle, rows = _build_order_generation()
    forged_ledgers = {name: tuple(dict(row) for row in ledger_rows) for name, ledger_rows in artifacts.segment_rows_by_ledger.items()}
    forged_desired = [dict(row) for row in forged_ledgers["desired_position_ledger.csv"]]
    forged_desired[0]["desired_position_contracts"] = "999"
    forged_ledgers["desired_position_ledger.csv"] = tuple(forged_desired)
    forged_artifacts = replace(artifacts, segment_rows_by_ledger=forged_ledgers)

    with pytest.raises(CarverBlocked, match="fast segment artifacts row hash drift"):
        bundle.validate(
            primitive_bundle=primitive_bundle,
            segment_bundle=segment,
            artifacts=forged_artifacts,
            policy_registry=registry,
            rows=rows,
        )


def test_fast_order_generator_is_not_exported_from_package_root():
    assert "build_fast_order_generation" not in package_root.__all__
