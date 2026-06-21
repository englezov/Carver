from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACK = (
    ROOT
    / "docs/researchops/s27_v2_local_replay_inputs/ZN/"
    "20260611_pre2023_dev_recon_valuation_mark_znh2_20220103T03_declared_pack"
)
MANIFEST = PACK / "S27_V2_PRE2023_VALUATION_MARK_DECLARED_INPUT_PACK_MANIFEST.json"
SOURCE_LEDGER = (
    ROOT
    / "docs/researchops/s27_v2_databento_older_zn_history/"
    "20260611_pre2023_zn_dev_recon_download_build/ledger/"
    "20260611_S27_V2_ZN_PRE2023_OLDER_HISTORY_DOWNLOAD_BUILD_strategy_facing_hourly_available_bars.csv"
)
SOURCE_PROVIDER = (
    ROOT
    / "docs/researchops/s27_v2_databento_older_zn_history/"
    "20260611_pre2023_zn_dev_recon_download_build/raw_provider_output/hourly/"
    "20260611_S27_V2_ZN_PRE2023_OLDER_HISTORY_DOWNLOAD_BUILD_ohlcv-1h_ZNH2_2022_provider.csv"
)
CONTROLLED_RUN = (
    ROOT
    / "docs/researchops/s27_v2_local_replay_runs/ZN/"
    "20260611_pre2023_oldest_dev_recon_2022_controlled_run"
)


def _manifest() -> dict[str, object]:
    return json.loads(MANIFEST.read_text(encoding="ascii"))


def _rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="ascii") as handle:
        return list(csv.DictReader(handle))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def _line_hash(path: Path, line_number: int) -> str:
    return hashlib.sha256(path.read_bytes().splitlines(keepends=True)[line_number - 1]).hexdigest().upper()


def test_manifest_declares_local_only_mark_after_fill() -> None:
    manifest = _manifest()

    assert manifest["authorization"] == "S27_V2_PRE2023_DEVELOPMENT_RECON_POST_FILL_VALUATION_MARK_ROW_DECLARATION_GATE"
    assert manifest["status"] == "LOCAL_PRE2023_VALUATION_MARK_ROW_DECLARED_NOT_PNL_NOT_RESULT"
    assert manifest["source_fill_timestamp_utc"] == "2022-01-03T02:00:00Z"
    assert manifest["valuation_mark_completed_timestamp_utc"] == "2022-01-03T03:00:00Z"
    assert manifest["valuation_mark_completed_timestamp_utc"] > manifest["source_fill_timestamp_utc"]
    assert manifest["valuation_mark_is_strictly_after_fill"] == "YES"
    assert manifest["raw_symbol"] == "ZNH2"
    assert manifest["valuation_convention_label"] == "SOURCE_NATIVE_ENGINEERING_VALUATION_ASSUMPTION_NOT_BOOK_EXPLICIT"


def test_mark_row_is_single_completed_znh2_row() -> None:
    rows = _rows(PACK / "valuation_mark_completed_bar.csv")

    assert len(rows) == 1
    row = rows[0]
    assert row["completed_timestamp_utc"] == "2022-01-03T03:00:00Z"
    assert row["trading_date"] == "2022-01-03"
    assert row["raw_symbol"] == "ZNH2"
    assert row["instrument_id"] == "768155"
    assert row["close_price"] == "130.296875"
    assert row["readiness_status"] == "READY_COMPLETED_BAR_LOCAL_PRE2023_DEV_RECON_VALUATION_MARK_ONLY"


def test_manifest_binds_pack_file_hashes_and_sha_sums() -> None:
    manifest = _manifest()
    declared = manifest["row_family_files"]["valuation_mark_completed_bar.csv"]

    assert declared["row_count"] == 1
    assert declared["sha256"] == _sha256(PACK / "valuation_mark_completed_bar.csv")

    sha_rows = _rows(PACK / "S27_V2_PRE2023_VALUATION_MARK_DECLARED_INPUT_PACK_SHA256SUMS.csv")
    sha_by_path = {row["relative_path"]: row["sha256"] for row in sha_rows}
    for relative_path, digest in sha_by_path.items():
        assert digest == _sha256(PACK / relative_path)


def test_source_ledger_and_provider_row_byte_hashes_are_bound() -> None:
    manifest = _manifest()
    ledger = manifest["source_files"]["strategy_facing_hourly_available_bars"]
    provider = manifest["source_files"]["raw_provider_hourly_csv"]

    assert ledger["path"].replace("\\", "/") == SOURCE_LEDGER.relative_to(ROOT).as_posix()
    assert provider["path"].replace("\\", "/") == SOURCE_PROVIDER.relative_to(ROOT).as_posix()
    assert ledger["sha256"] == _sha256(SOURCE_LEDGER)
    assert provider["sha256"] == _sha256(SOURCE_PROVIDER)
    assert ledger["selected_line_number"] == 4
    assert provider["selected_line_number"] == 27
    assert ledger["selected_line_sha256"] == _line_hash(SOURCE_LEDGER, 4)
    assert provider["selected_line_sha256"] == _line_hash(SOURCE_PROVIDER, 27)


def test_selected_source_and_provider_rows_match() -> None:
    manifest = _manifest()
    source = manifest["selected_source_row"]
    provider = manifest["selected_provider_row"]

    assert source["derived_completed_bar_end_utc"] == "2022-01-03T03:00:00Z"
    assert source["provider_ts_event_start_utc"] == "2022-01-03T02:00:00Z"
    assert provider["ts_event"] == "2022-01-03 02:00:00+00:00"
    assert source["provider_condition_status"] == "PROVIDER_CONDITION_AVAILABLE"
    assert source["instrument_id"] == provider["instrument_id"] == "768155"
    assert source["open"] == provider["open"] == "130.328125"
    assert source["high"] == provider["high"] == "130.328125"
    assert source["low"] == provider["low"] == "130.296875"
    assert source["close"] == provider["close"] == "130.296875"


def test_controlled_run_binding_and_non_authorizations() -> None:
    manifest = _manifest()

    assert manifest["source_controlled_run_bundle_sha256"] == _sha256(CONTROLLED_RUN / "run_bundle.json")
    assert manifest["source_controlled_run_trusted_bundle_sha256"] == _sha256(CONTROLLED_RUN / "trusted_bundle.json")
    for required in (
        "NO_PROVIDER_API",
        "NO_DOWNLOADS",
        "NO_NEW_DATA_ACQUISITION",
        "NO_TEST_ACCESS",
        "NO_VALIDATION_ACCESS",
        "NO_OOS",
        "NO_LOCKBOX",
        "NO_FORWARD",
        "NO_RESULT_INTERPRETATION",
        "NO_PNL_EVALUATION",
        "NO_GIT_ACTIONS",
        "NO_SOURCE_FAITHFUL_EVIDENCE_CLAIM",
    ):
        assert required in manifest["non_authorizations"]


def test_no_protected_window_or_result_surface_in_pack() -> None:
    combined = "\n".join(path.read_text(encoding="ascii") for path in PACK.iterdir() if path.is_file())

    assert "2023-" not in combined
    assert "2024-" not in combined
    assert "2025-" not in combined
    assert "2026-" not in combined
    assert "RESULT_ROW_EMITTED" not in combined
    assert "SOURCE_FAITHFUL_EVIDENCE_CLAIMED" not in combined
