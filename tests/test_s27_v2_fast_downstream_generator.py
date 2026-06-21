from __future__ import annotations

import hashlib
import json
from dataclasses import replace
import inspect
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from carver.spine.m0 import CarverBlocked
import carver.spine.s27_v2_replay as package_root
import carver.spine.s27_v2_replay.fast_downstream_generator as downstream_module
from carver.spine.s27_v2_replay.fast_downstream_generator import (
    COMBINED_TBBO_REGISTRY_MANIFEST_NAME,
    GENERATOR_MODE,
    STATUS,
    _load_downstream_source,
    _generation_bundle_payload,
    build_fast_downstream_generation,
    build_fast_downstream_policy_registry,
)
from carver.spine.s27_v2_replay.fast_order_generator import (
    build_fast_order_generation,
    build_fast_order_policy_registry,
)
from carver.spine.s27_v2_replay.fast_row_engine import build_fast_primitive_engine
from carver.spine.s27_v2_replay.fast_segment_emitter import build_fast_segment_artifacts
from carver.spine.s27_v2_replay.local_replay import canonical_sha256


def _build_downstream_generation():
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
    bundle, rows = build_fast_downstream_generation(
        primitive_bundle=primitive_bundle,
        segment_bundle=segment,
        artifacts=artifacts,
        order_policy_registry=order_registry,
        order_bundle=order_bundle,
        order_rows=order_rows,
        downstream_policy_registry=downstream_registry,
    )
    return primitive_bundle, artifacts, segment, order_registry, order_bundle, order_rows, downstream_registry, bundle, rows


def test_fast_downstream_generator_recreates_segment_downstream_rows_with_hash_parity():
    primitive_bundle, artifacts, segment, _order_registry, order_bundle, _order_rows, registry, bundle, rows = (
        _build_downstream_generation()
    )

    assert bundle.status == STATUS
    assert bundle.generator_mode == GENERATOR_MODE
    assert bundle.primitive_engine_bundle_hash == primitive_bundle.bundle_hash
    assert bundle.segment_bundle_hash == segment.bundle_hash
    assert bundle.segment_artifacts_hash == artifacts.bundle_hash
    assert bundle.order_generation_bundle_hash == order_bundle.bundle_hash
    assert bundle.downstream_policy_registry_hash == registry.registry_hash
    assert bundle.generated_row_count == 675
    assert len(rows.transition_rows) == 675
    assert len(rows.fill_rows) == 675
    assert len(rows.cost_rows) == 675
    assert len(rows.pnl_rows) == 675
    assert len(rows.validation_rows) == 675
    assert len(rows.market_fill_metadata_rows) > 0
    assert rows.fill_rows[0]["row_index"] == "704"
    assert rows.fill_rows[-1]["row_index"] == "1378"
    assert rows.market_fill_metadata_rows[-1]["row_index"] == "1378"


def test_fast_downstream_generator_rejects_generated_row_mutation():
    primitive_bundle, artifacts, segment, order_registry, order_bundle, order_rows, registry, bundle, rows = (
        _build_downstream_generation()
    )
    mutated_fill = [dict(row) for row in rows.fill_rows]
    mutated_fill[-1]["position_after_fill"] = "999"
    forged_rows = replace(rows, fill_rows=tuple(mutated_fill))

    with pytest.raises(CarverBlocked, match="fill rows hash drift"):
        bundle.validate(
            primitive_bundle=primitive_bundle,
            segment_bundle=segment,
            artifacts=artifacts,
            order_policy_registry=order_registry,
            order_bundle=order_bundle,
            order_rows=order_rows,
            downstream_policy_registry=registry,
            rows=forged_rows,
        )


def test_fast_downstream_generator_rejects_self_consistent_generated_row_mutation():
    primitive_bundle, artifacts, segment, order_registry, order_bundle, order_rows, registry, bundle, rows = (
        _build_downstream_generation()
    )
    mutated_fill = [dict(row) for row in rows.fill_rows]
    mutated_fill[-1]["position_after_fill"] = "999"
    forged_rows = replace(rows, fill_rows=tuple(mutated_fill))
    forged = replace(
        bundle,
        fill_rows_hash=canonical_sha256(forged_rows.fill_rows),
        parity_report_hash="0" * 64,
        coherence_report_hash="0" * 64,
    )
    forged = replace(forged, bundle_hash=canonical_sha256(_generation_bundle_payload(forged)))

    with pytest.raises(CarverBlocked, match="parity drift|transition/fill position drift|pnl/fill position drift"):
        forged.validate(
            primitive_bundle=primitive_bundle,
            segment_bundle=segment,
            artifacts=artifacts,
            order_policy_registry=order_registry,
            order_bundle=order_bundle,
            order_rows=order_rows,
            downstream_policy_registry=registry,
            rows=forged_rows,
        )


def test_fast_downstream_generator_rejects_duplicate_dense_row_index_forgery():
    primitive_bundle, artifacts, segment, order_registry, order_bundle, order_rows, registry, bundle, rows = (
        _build_downstream_generation()
    )
    forged_rows = replace(rows, fill_rows=rows.fill_rows + (dict(rows.fill_rows[-1]),))
    forged = replace(
        bundle,
        fill_rows_hash=canonical_sha256(forged_rows.fill_rows),
        bundle_hash="0" * 64,
    )
    forged = replace(forged, bundle_hash=canonical_sha256(_generation_bundle_payload(forged)))

    with pytest.raises(CarverBlocked, match="fill row count drift"):
        forged.validate(
            primitive_bundle=primitive_bundle,
            segment_bundle=segment,
            artifacts=artifacts,
            order_policy_registry=order_registry,
            order_bundle=order_bundle,
            order_rows=order_rows,
            downstream_policy_registry=registry,
            rows=forged_rows,
        )


def test_fast_downstream_generator_rejects_duplicate_sparse_market_fill_row_index_forgery():
    primitive_bundle, artifacts, segment, order_registry, order_bundle, order_rows, registry, bundle, rows = (
        _build_downstream_generation()
    )
    forged_rows = replace(rows, market_fill_metadata_rows=rows.market_fill_metadata_rows + (dict(rows.market_fill_metadata_rows[-1]),))
    forged = replace(
        bundle,
        market_fill_metadata_row_count=len(forged_rows.market_fill_metadata_rows),
        market_fill_metadata_rows_hash=canonical_sha256(forged_rows.market_fill_metadata_rows),
    )
    forged = replace(forged, bundle_hash=canonical_sha256(_generation_bundle_payload(forged)))

    with pytest.raises(CarverBlocked, match="duplicate row index drift"):
        forged.validate(
            primitive_bundle=primitive_bundle,
            segment_bundle=segment,
            artifacts=artifacts,
            order_policy_registry=order_registry,
            order_bundle=order_bundle,
            order_rows=order_rows,
            downstream_policy_registry=registry,
            rows=forged_rows,
        )


def test_fast_downstream_generator_rejects_policy_registry_binding_drift():
    primitive_bundle, artifacts, segment, order_registry, order_bundle, order_rows, registry, bundle, rows = (
        _build_downstream_generation()
    )
    forged = replace(bundle, downstream_policy_registry_hash="0" * 64)
    forged = replace(forged, bundle_hash=canonical_sha256(_generation_bundle_payload(forged)))

    with pytest.raises(CarverBlocked, match="policy binding drift"):
        forged.validate(
            primitive_bundle=primitive_bundle,
            segment_bundle=segment,
            artifacts=artifacts,
            order_policy_registry=order_registry,
            order_bundle=order_bundle,
            order_rows=order_rows,
            downstream_policy_registry=registry,
            rows=rows,
        )


def test_fast_downstream_registry_rejects_forged_artifact_authority():
    _primitive_bundle, artifacts, _segment, _order_registry, order_bundle, order_rows, registry, _bundle, _rows = (
        _build_downstream_generation()
    )
    forged_ledgers = {name: tuple(dict(row) for row in ledger_rows) for name, ledger_rows in artifacts.segment_rows_by_ledger.items()}
    forged_fill = [dict(row) for row in forged_ledgers["fill_ledger.csv"]]
    forged_fill[0]["position_after_fill"] = "999"
    forged_ledgers["fill_ledger.csv"] = tuple(forged_fill)
    forged_artifacts = replace(artifacts, segment_rows_by_ledger=forged_ledgers)

    with pytest.raises(CarverBlocked, match="fast segment artifacts row hash drift"):
        registry.validate(
            artifacts=forged_artifacts,
            primitive_bundle=_primitive_bundle,
            segment_bundle=_segment,
            order_policy_registry=_order_registry,
            order_bundle=order_bundle,
            order_rows=order_rows,
        )


def test_fast_downstream_registry_rejects_forged_order_bundle_authority():
    primitive_bundle, artifacts, segment, order_registry, order_bundle, order_rows, registry, _bundle, _rows = (
        _build_downstream_generation()
    )
    forged_order_bundle = replace(order_bundle, status="FORGED_READY")
    forged_order_bundle = replace(
        forged_order_bundle,
        bundle_hash=canonical_sha256(
            {k: v for k, v in forged_order_bundle.__dict__.items() if k != "bundle_hash"}
        ),
    )

    with pytest.raises(CarverBlocked, match="order bundle binding drift|order generation status mismatch"):
        registry.validate(
            artifacts=artifacts,
            primitive_bundle=primitive_bundle,
            segment_bundle=segment,
            order_policy_registry=order_registry,
            order_bundle=forged_order_bundle,
            order_rows=order_rows,
        )


def test_fast_downstream_generator_rejects_market_fill_metadata_binding_drift():
    primitive_bundle, artifacts, segment, order_registry, order_bundle, order_rows, registry, bundle, rows = (
        _build_downstream_generation()
    )
    mutated_market_fill = [dict(row) for row in rows.market_fill_metadata_rows]
    mutated_market_fill[-1]["order_side"] = "BUY" if mutated_market_fill[-1]["order_side"] == "SELL" else "SELL"
    forged_rows = replace(rows, market_fill_metadata_rows=tuple(mutated_market_fill))
    forged = replace(
        bundle,
        market_fill_metadata_rows_hash=canonical_sha256(forged_rows.market_fill_metadata_rows),
        parity_report_hash="0" * 64,
        coherence_report_hash="0" * 64,
    )
    forged = replace(forged, bundle_hash=canonical_sha256(_generation_bundle_payload(forged)))

    with pytest.raises(CarverBlocked, match="parity drift|market-fill side drift"):
        forged.validate(
            primitive_bundle=primitive_bundle,
            segment_bundle=segment,
            artifacts=artifacts,
            order_policy_registry=order_registry,
            order_bundle=order_bundle,
            order_rows=order_rows,
            downstream_policy_registry=registry,
            rows=forged_rows,
        )


def test_fast_downstream_policy_registry_rejects_self_consistent_row_hash_drift():
    _primitive_bundle, artifacts, _segment, _order_registry, order_bundle, order_rows, registry, _bundle, _rows = (
        _build_downstream_generation()
    )
    forged = replace(registry, policy_rows_hash="0" * 64)
    forged = replace(forged, registry_hash=canonical_sha256({k: v for k, v in forged.__dict__.items() if k != "registry_hash"}))

    with pytest.raises(CarverBlocked, match="row hash drift"):
        forged.validate(
            artifacts=artifacts,
            primitive_bundle=_primitive_bundle,
            segment_bundle=_segment,
            order_policy_registry=_order_registry,
            order_bundle=order_bundle,
            order_rows=order_rows,
        )


def test_fast_downstream_generator_rejects_forged_artifact_authority():
    primitive_bundle, artifacts, segment, order_registry, order_bundle, order_rows, registry, bundle, rows = (
        _build_downstream_generation()
    )
    forged_ledgers = {name: tuple(dict(row) for row in ledger_rows) for name, ledger_rows in artifacts.segment_rows_by_ledger.items()}
    forged_fill = [dict(row) for row in forged_ledgers["fill_ledger.csv"]]
    forged_fill[0]["position_after_fill"] = "999"
    forged_ledgers["fill_ledger.csv"] = tuple(forged_fill)
    forged_artifacts = replace(artifacts, segment_rows_by_ledger=forged_ledgers)

    with pytest.raises(CarverBlocked, match="fast segment artifacts row hash drift"):
        bundle.validate(
            primitive_bundle=primitive_bundle,
            segment_bundle=segment,
            artifacts=forged_artifacts,
            order_policy_registry=order_registry,
            order_bundle=order_bundle,
            order_rows=order_rows,
            downstream_policy_registry=registry,
            rows=rows,
        )


def test_fast_downstream_generator_is_not_exported_from_package_root():
    assert "build_fast_downstream_generation" not in package_root.__all__


def test_fast_downstream_generator_policy_registry_does_not_embed_full_downstream_rows():
    source = inspect.getsource(downstream_module)
    forbidden_fragments = (
        '"transition_row": dict(',
        '"fill_row": dict(',
        '"market_fill_metadata_row": dict(',
        '"cost_row": dict(',
        '"pnl_row": dict(',
        '"validation_row": dict(',
        'policy["transition_row"]',
        'policy["fill_row"]',
        'policy["cost_row"]',
        'policy["pnl_row"]',
        'policy["validation_row"]',
    )
    for fragment in forbidden_fragments:
        assert fragment not in source


def test_fast_downstream_policy_builder_does_not_read_downstream_artifact_ledgers():
    source = inspect.getsource(downstream_module._build_policy_rows)
    assert "segment_rows_by_ledger" not in source
    for ledger_name in (
        "working_order_transition_ledger.csv",
        "fill_ledger.csv",
        "market_fill_metadata_ledger.csv",
        "cost_ledger.csv",
        "pnl_ledger.csv",
        "validation_ledger.csv",
    ):
        assert ledger_name not in source


def test_fast_downstream_source_loader_rejects_forged_tbbo_manifest_hash(tmp_path):
    pack_root = tmp_path / "pack"
    tbbo_root = tmp_path / "tbbo"
    pack_root.mkdir()
    tbbo_root.mkdir()
    row_files = {
        "hourly_decision_completed_bar.csv": "row_index,raw_symbol,session_id,close_price\n1,ZNM3,S1,100.0\n",
        "hourly_fill_completed_bar.csv": (
            "row_index,completed_timestamp_utc,raw_symbol,session_id,close_price,source_row_hash\n"
            "1,2023-01-01T01:00:00Z,ZNM3,S1,100.0,SOURCE\n"
        ),
        "valuation_mark_completed_bar.csv": "row_index,raw_symbol,session_id,close_price\n1,ZNM3,S1,100.0\n",
        "cost_parameter.csv": "cost_policy_id,currency\nCOST,USD\n",
    }
    manifest = {"row_family_files": {}}
    for filename, content in row_files.items():
        (pack_root / filename).write_text(content, encoding="utf-8", newline="")
        manifest["row_family_files"][filename] = {"sha256": hashlib.sha256(content.encode("utf-8")).hexdigest()}
    (pack_root / "S27_V2_2023_TEST_DECLARED_INPUT_PACK_MANIFEST.json").write_text(
        json.dumps(manifest, sort_keys=True),
        encoding="utf-8",
    )
    tbbo_content = (
        "row_index,fill_timestamp_utc,raw_symbol,market_order_side,selected_executable_market_fill_price,"
        "bid_px_00,ask_px_00,spread_points,spread_cost_usd_per_contract,row_hash,selected_quote_ts_event\n"
        "1,2023-01-01T01:00:00Z,ZNM3,SELL,100.0,100.0,100.015625,0.015625,15.625,HASH,2023-01-01T00:59:59Z\n"
    )
    (tbbo_root / "combined_market_order_tbbo_registry.csv").write_text(tbbo_content, encoding="utf-8", newline="")
    (tbbo_root / COMBINED_TBBO_REGISTRY_MANIFEST_NAME).write_text(
        json.dumps(
            {
                "registry": "combined_market_order_tbbo_registry.csv",
                "registry_sha256": "0" * 64,
            },
            sort_keys=True,
        ),
        encoding="utf-8",
    )

    with pytest.raises(CarverBlocked, match="TBBO registry manifest hash drift"):
        _load_downstream_source(pack_root=pack_root, tbbo_root=tbbo_root)
