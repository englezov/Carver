from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from carver.spine.m0 import CarverBlocked
from carver.spine.s27_v2_replay.fast_execution_state import (
    DEFAULT_EXECUTION_PARITY_ROWS,
    ENGINE_STAGE,
    SUPPORTED_POLICY_CLASSES,
    _read_rows_by_index,
    _read_segment_ledgers,
    _reduce_segment,
    build_fast_execution_state_verification,
)
from carver.spine.s27_v2_replay.local_replay import canonical_sha256
from carver.spine.s27_v2_replay.test_incremental_runner import (
    DEFAULT_OUTPUT_RELATIVE_PATH,
    _segment_bundle_payload,
    build_incremental_segment_from_existing_artifacts,
)


RUN_ROOT = ROOT / DEFAULT_OUTPUT_RELATIVE_PATH


def _mutable_segment_rows(segment):
    rows = _read_segment_ledgers(RUN_ROOT, segment.segment_start_row_index, segment.segment_end_row_index)
    return {
        ledger_name: {row_index: dict(row) for row_index, row in rows_by_index.items()}
        for ledger_name, rows_by_index in rows.items()
    }


def test_fast_execution_state_verifies_incremental_segment_without_full_replay():
    verification, rows = build_fast_execution_state_verification()

    assert verification.engine_stage == ENGINE_STAGE
    assert verification.segment_start_row_index == 704
    assert verification.segment_end_row_index == 1378
    assert verification.segment_row_count == 675
    assert verification.starting_position_contracts == 0
    assert verification.ending_position_contracts == 3
    assert verification.supported_policy_classes == SUPPORTED_POLICY_CLASSES
    assert verification.parity_row_indexes == DEFAULT_EXECUTION_PARITY_ROWS
    assert len(rows.state_transition_rows) == 675
    assert len(rows.intent_classification_rows) == 675
    rows.validate(verification)


def test_fast_execution_state_rejects_rows_not_bound_to_verification_hashes():
    verification, rows = build_fast_execution_state_verification()
    forged_state_rows = [dict(row) for row in rows.state_transition_rows]
    forged_state_rows[0]["ending_position_contracts"] = 99
    forged_rows = replace(rows, state_transition_rows=tuple(forged_state_rows))

    with pytest.raises(CarverBlocked, match="transition rows hash drift"):
        forged_rows.validate(verification)


def test_fast_execution_state_rejects_forged_segment_binding():
    segment = build_incremental_segment_from_existing_artifacts()
    forged_segment = replace(segment, segment_end_row_index=1376)
    forged_segment = replace(
        forged_segment,
        bundle_hash=canonical_sha256(_segment_bundle_payload(forged_segment)),
    )

    with pytest.raises(CarverBlocked, match="segment end must be row 1378"):
        build_fast_execution_state_verification(segment_bundle=forged_segment)


def test_fast_execution_state_rejects_cumulative_pnl_roll_forward_mutation():
    segment = build_incremental_segment_from_existing_artifacts()
    rows = _mutable_segment_rows(segment)
    rows["pnl_ledger.csv"][704]["cumulative_net_pnl_amount"] = "0.0"

    with pytest.raises(CarverBlocked, match="cumulative net drift"):
        _reduce_segment(segment, rows)


def test_fast_execution_state_rejects_market_fill_metadata_price_mutation():
    segment = build_incremental_segment_from_existing_artifacts()
    rows = _mutable_segment_rows(segment)
    rows["market_fill_metadata_ledger.csv"][1374]["fill_price"] = "999.0"

    with pytest.raises(CarverBlocked, match="market fill price drift"):
        _reduce_segment(segment, rows)


def test_fast_execution_state_rejects_market_fill_metadata_timestamp_mutation():
    segment = build_incremental_segment_from_existing_artifacts()
    rows = _mutable_segment_rows(segment)
    rows["market_fill_metadata_ledger.csv"][1374]["fill_timestamp_utc"] = "2023-03-30T18:00:01Z"

    with pytest.raises(CarverBlocked, match="market fill timestamp drift"):
        _reduce_segment(segment, rows)


def test_fast_execution_state_rejects_market_fill_metadata_source_hash_mutation():
    segment = build_incremental_segment_from_existing_artifacts()
    rows = _mutable_segment_rows(segment)
    rows["market_fill_metadata_ledger.csv"][1374]["fill_source_row_hash"] = "0" * 64

    with pytest.raises(CarverBlocked, match="market fill source row hash drift"):
        _reduce_segment(segment, rows)


def test_fast_execution_state_rejects_unexpected_market_fill_metadata_for_non_market_row():
    segment = build_incremental_segment_from_existing_artifacts()
    rows = _mutable_segment_rows(segment)
    rows["market_fill_metadata_ledger.csv"][704] = dict(rows["market_fill_metadata_ledger.csv"][1374])
    rows["market_fill_metadata_ledger.csv"][704]["row_index"] = "704"

    with pytest.raises(CarverBlocked, match="unexpected market fill metadata"):
        _reduce_segment(segment, rows)


def test_fast_execution_state_rejects_duplicate_sparse_row_indexes(tmp_path):
    ledger = tmp_path / "market_order_ledger.csv"
    ledger.write_text("row_index,row_hash\n1374,a\n1374,b\n", encoding="ascii")

    with pytest.raises(CarverBlocked, match="duplicate row_index"):
        _read_rows_by_index(ledger, 704, 1378)


def test_fast_execution_state_rejects_unlocked_run_root(tmp_path):
    with pytest.raises(CarverBlocked, match="run root is locked"):
        build_fast_execution_state_verification(run_root=tmp_path)
