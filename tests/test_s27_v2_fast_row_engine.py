from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from carver.spine.m0 import CarverBlocked
from carver.spine.s27_v2_replay.fast_row_engine import (
    DEFAULT_PARITY_ROWS,
    PRIMITIVE_ENGINE_STAGE,
    FastPrimitiveRows,
    _primitive_bundle_payload,
    build_fast_primitive_engine,
    validate_fast_primitive_parity,
)
from carver.spine.s27_v2_replay.local_replay import canonical_sha256


def test_fast_primitive_engine_builds_declared_pack_rows():
    bundle, rows = build_fast_primitive_engine()

    assert bundle.engine_stage == PRIMITIVE_ENGINE_STAGE
    assert bundle.row_count == 1378
    assert len(rows.runtime_rows) == 1378
    assert len(rows.forecast_rows) == 1378
    assert len(rows.desired_absolute_rows) == 1378
    assert rows.forecast_rows[0]["raw_forecast"] == pytest.approx(0.029727635124984886)
    assert rows.forecast_rows[1]["capped_forecast"] == 0.0
    assert rows.desired_absolute_rows[0]["desired_position_contracts"] == 2
    bundle.validate()


def test_fast_primitive_engine_parity_against_existing_ledgers():
    bundle, rows = build_fast_primitive_engine()
    report = validate_fast_primitive_parity(bundle, rows)

    assert report.parity_row_indexes == DEFAULT_PARITY_ROWS
    report.validate(bundle)


def test_fast_primitive_engine_rejects_unlocked_pack_root(tmp_path):
    with pytest.raises(CarverBlocked, match="input pack is locked"):
        build_fast_primitive_engine(pack_root=tmp_path)


def test_fast_primitive_engine_bundle_forgery_rejects():
    bundle, _ = build_fast_primitive_engine()
    forged = replace(bundle, row_count=1377)
    forged = replace(forged, bundle_hash=canonical_sha256(_primitive_bundle_payload(forged)))

    with pytest.raises(CarverBlocked, match="row count drift"):
        forged.validate()


def test_fast_primitive_parity_rows_are_locked():
    bundle, rows = build_fast_primitive_engine()

    with pytest.raises(CarverBlocked, match="parity rows are locked"):
        validate_fast_primitive_parity(bundle, rows, parity_row_indexes=(1, 2))


def test_fast_primitive_parity_rejects_rows_not_bound_to_bundle():
    bundle, rows = build_fast_primitive_engine()
    forged_forecast = [dict(row) for row in rows.forecast_rows]
    forged_forecast[0]["raw_forecast"] = 999.0
    forged_rows = FastPrimitiveRows(
        runtime_rows=rows.runtime_rows,
        forecast_rows=tuple(forged_forecast),
        desired_absolute_rows=rows.desired_absolute_rows,
    )

    with pytest.raises(CarverBlocked, match="forecast rows do not match bundle hash"):
        validate_fast_primitive_parity(bundle, forged_rows)


def test_fast_primitive_parity_rejects_unlocked_run_root(tmp_path):
    bundle, rows = build_fast_primitive_engine()

    with pytest.raises(CarverBlocked, match="run root is locked"):
        validate_fast_primitive_parity(bundle, rows, run_root=tmp_path)
