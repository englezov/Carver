from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
AUTHORIZATION = "S27_V2_PRE2023_DEVELOPMENT_RECON_POST_FILL_VALUATION_MARK_ROW_DECLARATION_GATE"
STATUS = "LOCAL_PRE2023_VALUATION_MARK_ROW_DECLARED_NOT_PNL_NOT_RESULT"
VALUATION_CONVENTION_LABEL = "SOURCE_NATIVE_ENGINEERING_VALUATION_ASSUMPTION_NOT_BOOK_EXPLICIT"

CONTROLLED_RUN_ROOT = (
    ROOT
    / "docs/researchops/s27_v2_local_replay_runs/ZN/"
    "20260611_pre2023_oldest_dev_recon_2022_controlled_run"
)
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
INPUT_PACK_ROOT = (
    ROOT
    / "docs/researchops/s27_v2_local_replay_inputs/ZN/"
    "20260611_pre2023_dev_recon_valuation_mark_znh2_20220103T03_declared_pack"
)
PROCESS_DOC = (
    ROOT
    / "docs/process/CARVER_S27_ZN_V2_PRE2023_VALUATION_MARK_DECLARED_PACK_RECORD_2026-06-11.md"
)

FILL_TIMESTAMP = "2022-01-03T02:00:00Z"
MARK_TIMESTAMP = "2022-01-03T03:00:00Z"
RAW_PROVIDER_TS_EVENT = "2022-01-03 02:00:00+00:00"
RAW_SYMBOL = "ZNH2"
EXPECTED_CLOSE = "130.296875"

NON_AUTHORIZATIONS = (
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
    "NO_TUNING",
    "NO_ADAPTER_WORK",
    "NO_DEPLOYMENT",
    "NO_TRADING",
    "NO_PROMOTION",
    "NO_GIT_ACTIONS",
    "NO_SOURCE_FAITHFUL_EVIDENCE_CLAIM",
)


def main() -> None:
    INPUT_PACK_ROOT.mkdir(parents=True, exist_ok=True)
    run_bundle = _read_json(CONTROLLED_RUN_ROOT / "run_bundle.json")
    if run_bundle["selected_fill_timestamp_utc"] != FILL_TIMESTAMP:
        raise SystemExit("fail closed: controlled run fill timestamp mismatch")
    ledger_row, ledger_line = _select_ledger_mark_row()
    provider_row, provider_line = _select_provider_mark_row()
    _validate_selected_rows(ledger_row, provider_row)

    mark_row = {
        "completed_timestamp_utc": MARK_TIMESTAMP,
        "trading_date": ledger_row["completed_trading_date"],
        "raw_symbol": RAW_SYMBOL,
        "instrument_id": ledger_row["instrument_id"],
        "row_locator": "S27V2_PRE2023_ZN_VALUATION_MARK_20220103T030000Z_ZNH2",
        "close_price": EXPECTED_CLOSE,
        "valuation_convention_label": VALUATION_CONVENTION_LABEL,
        "readiness_status": "READY_COMPLETED_BAR_LOCAL_PRE2023_DEV_RECON_VALUATION_MARK_ONLY",
    }
    _write_csv(INPUT_PACK_ROOT / "valuation_mark_completed_bar.csv", [mark_row])
    manifest = _manifest(run_bundle, ledger_row, ledger_line, provider_row, provider_line)
    _write_json(INPUT_PACK_ROOT / "S27_V2_PRE2023_VALUATION_MARK_DECLARED_INPUT_PACK_MANIFEST.json", manifest)
    provenance = _provenance_text(manifest, mark_row)
    (INPUT_PACK_ROOT / "S27_V2_PRE2023_VALUATION_MARK_DECLARED_INPUT_PACK_PROVENANCE.md").write_text(
        provenance,
        encoding="ascii",
    )
    _write_sha256s(INPUT_PACK_ROOT)
    PROCESS_DOC.write_text(_process_doc(manifest), encoding="ascii")
    print(STATUS)
    print(f"declared_pack={INPUT_PACK_ROOT.relative_to(ROOT)}")
    print(f"mark_timestamp={MARK_TIMESTAMP}")
    print(f"mark_close={EXPECTED_CLOSE}")


def _manifest(
    run_bundle: dict[str, Any],
    ledger_row: dict[str, str],
    ledger_line: int,
    provider_row: dict[str, str],
    provider_line: int,
) -> dict[str, Any]:
    valuation_csv = INPUT_PACK_ROOT / "valuation_mark_completed_bar.csv"
    ledger_line_bytes = _line_bytes(SOURCE_LEDGER, ledger_line)
    provider_line_bytes = _line_bytes(SOURCE_PROVIDER, provider_line)
    source_ledger_row_hash = _canonical_hash(
        {
            "artifact": "S27_V2_PRE2023_VALUATION_MARK_SOURCE_LEDGER_ROW",
            "line_number": ledger_line,
            "row": ledger_row,
        }
    )
    source_provider_row_hash = _canonical_hash(
        {
            "artifact": "S27_V2_PRE2023_VALUATION_MARK_PROVIDER_ROW",
            "line_number": provider_line,
            "row": provider_row,
        }
    )
    return {
        "artifact": "S27_V2_PRE2023_VALUATION_MARK_DECLARED_INPUT_PACK_MANIFEST",
        "authorization": AUTHORIZATION,
        "status": STATUS,
        "lane": "SOURCE_NATIVE_FUTURES",
        "strategy_id": "S27_V2_ZN",
        "instrument": "ZN",
        "source_controlled_run_root": str(CONTROLLED_RUN_ROOT.relative_to(ROOT)),
        "source_controlled_run_bundle_sha256": _sha256(CONTROLLED_RUN_ROOT / "run_bundle.json"),
        "source_controlled_run_trusted_bundle_sha256": _sha256(CONTROLLED_RUN_ROOT / "trusted_bundle.json"),
        "source_fill_timestamp_utc": FILL_TIMESTAMP,
        "valuation_mark_completed_timestamp_utc": MARK_TIMESTAMP,
        "valuation_mark_is_strictly_after_fill": "YES",
        "raw_symbol": RAW_SYMBOL,
        "valuation_convention_label": VALUATION_CONVENTION_LABEL,
        "valuation_convention_status": "ACCEPTED_ENGINEERING_ASSUMPTION_NOT_BOOK_EXPLICIT_FOR_LOCAL_DEV_RECON_ONLY",
        "row_family_files": {
            "valuation_mark_completed_bar.csv": {
                "row_count": 1,
                "sha256": _sha256(valuation_csv),
            }
        },
        "source_files": {
            "strategy_facing_hourly_available_bars": {
                "path": str(SOURCE_LEDGER.relative_to(ROOT)),
                "sha256": _sha256(SOURCE_LEDGER),
                "selected_line_number": ledger_line,
                "selected_line_sha256": _hash_bytes(ledger_line_bytes),
                "selected_row_hash": source_ledger_row_hash,
            },
            "raw_provider_hourly_csv": {
                "path": str(SOURCE_PROVIDER.relative_to(ROOT)),
                "sha256": _sha256(SOURCE_PROVIDER),
                "selected_line_number": provider_line,
                "selected_line_sha256": _hash_bytes(provider_line_bytes),
                "selected_row_hash": source_provider_row_hash,
            },
        },
        "selected_source_row": {
            "provider_ts_event_start_utc": ledger_row["provider_ts_event_start_utc"],
            "derived_completed_bar_end_utc": ledger_row["derived_completed_bar_end_utc"],
            "completed_trading_date": ledger_row["completed_trading_date"],
            "instrument_id": ledger_row["instrument_id"],
            "open": ledger_row["open"],
            "high": ledger_row["high"],
            "low": ledger_row["low"],
            "close": ledger_row["close"],
            "volume": ledger_row["volume"],
            "provider_condition_status": ledger_row["provider_condition_status"],
        },
        "selected_provider_row": {
            "ts_event": provider_row["ts_event"],
            "instrument_id": provider_row["instrument_id"],
            "open": provider_row["open"],
            "high": provider_row["high"],
            "low": provider_row["low"],
            "close": provider_row["close"],
            "volume": provider_row["volume"],
            "symbol": provider_row["symbol"],
        },
        "non_authorizations": NON_AUTHORIZATIONS,
    }


def _select_ledger_mark_row() -> tuple[dict[str, str], int]:
    candidates: list[tuple[dict[str, str], int]] = []
    with SOURCE_LEDGER.open(newline="", encoding="ascii") as handle:
        for line_number, row in enumerate(csv.DictReader(handle), start=2):
            if row["raw_symbol"] != RAW_SYMBOL:
                continue
            if row["derived_completed_bar_end_utc"] <= FILL_TIMESTAMP:
                continue
            candidates.append((row, line_number))
    if not candidates:
        raise SystemExit("fail closed: no local hourly mark row strictly after fill")
    row, line_number = min(candidates, key=lambda item: item[0]["derived_completed_bar_end_utc"])
    if row["derived_completed_bar_end_utc"] != MARK_TIMESTAMP:
        raise SystemExit("fail closed: first post-fill mark timestamp not locked")
    return row, line_number


def _select_provider_mark_row() -> tuple[dict[str, str], int]:
    with SOURCE_PROVIDER.open(newline="", encoding="ascii") as handle:
        for line_number, row in enumerate(csv.DictReader(handle), start=2):
            if row["symbol"] == RAW_SYMBOL and row["ts_event"] == RAW_PROVIDER_TS_EVENT:
                return row, line_number
    raise SystemExit("fail closed: provider row for valuation mark not found")


def _validate_selected_rows(ledger_row: dict[str, str], provider_row: dict[str, str]) -> None:
    if ledger_row["derived_completed_bar_end_utc"] != MARK_TIMESTAMP:
        raise SystemExit("fail closed: ledger mark timestamp mismatch")
    if ledger_row["provider_ts_event_start_utc"] != "2022-01-03T02:00:00Z":
        raise SystemExit("fail closed: ledger provider start mismatch")
    if provider_row["ts_event"] != RAW_PROVIDER_TS_EVENT:
        raise SystemExit("fail closed: provider ts_event mismatch")
    if ledger_row["provider_condition_status"] != "PROVIDER_CONDITION_AVAILABLE":
        raise SystemExit("fail closed: provider condition unavailable")
    for column in ("instrument_id", "open", "high", "low", "close"):
        if str(ledger_row[column]) != str(provider_row[column]):
            raise SystemExit(f"fail closed: ledger/provider {column} mismatch")
    if float(ledger_row["volume"]) != float(provider_row["volume"]):
        raise SystemExit("fail closed: ledger/provider volume mismatch")
    if ledger_row["close"] != EXPECTED_CLOSE:
        raise SystemExit("fail closed: mark close mismatch")


def _process_doc(manifest: dict[str, Any]) -> str:
    return f"""# S27_V2 Pre-2023 Valuation Mark Declared Pack Record

Date: 2026-06-11

Status:

```text
{STATUS}
```

Declared pack:

```text
{INPUT_PACK_ROOT.relative_to(ROOT)}
```

Selected mark row:

```text
raw_symbol = {RAW_SYMBOL}
fill_timestamp_utc = {FILL_TIMESTAMP}
valuation_mark_completed_timestamp_utc = {MARK_TIMESTAMP}
close_price = {EXPECTED_CLOSE}
valuation_convention_label = {VALUATION_CONVENTION_LABEL}
```

Source binding:

```text
strategy_facing_hourly_available_bars_sha256 = {manifest['source_files']['strategy_facing_hourly_available_bars']['sha256']}
strategy_facing_hourly_available_bars_line = {manifest['source_files']['strategy_facing_hourly_available_bars']['selected_line_number']}
strategy_facing_hourly_available_bars_line_sha256 = {manifest['source_files']['strategy_facing_hourly_available_bars']['selected_line_sha256']}
raw_provider_hourly_csv_sha256 = {manifest['source_files']['raw_provider_hourly_csv']['sha256']}
raw_provider_hourly_csv_line = {manifest['source_files']['raw_provider_hourly_csv']['selected_line_number']}
raw_provider_hourly_csv_line_sha256 = {manifest['source_files']['raw_provider_hourly_csv']['selected_line_sha256']}
valuation_mark_completed_bar_sha256 = {manifest['row_family_files']['valuation_mark_completed_bar.csv']['sha256']}
```

This is a local-only Development/Reconciliation valuation mark declaration. It
does not emit PnL, result rows, result interpretation, PnL evaluation,
promotion evidence, trading evidence, or source-faithful evidence claims.

Non-authorizations: no provider/API, downloads, new data acquisition, TEST,
VALIDATION, OOS, Lockbox, Forward, tuning, adapter work, deployment, trading,
promotion, Git actions, or source-faithful evidence claims.
"""


def _provenance_text(manifest: dict[str, Any], mark_row: dict[str, str]) -> str:
    return f"""# S27_V2 Pre-2023 Valuation Mark Pack Provenance

Status: `{STATUS}`

The declared mark row is the first completed local `ZNH2` hourly row strictly
after fill timestamp `{FILL_TIMESTAMP}`. The selected completed timestamp is
`{MARK_TIMESTAMP}` and close is `{mark_row['close_price']}`.

The valuation convention is `{VALUATION_CONVENTION_LABEL}`. It is not
book-explicit authority and not a source-faithful evidence claim.
"""


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", newline="", encoding="ascii") as handle:
        writer = csv.DictWriter(handle, fieldnames=tuple(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="ascii")


def _write_sha256s(folder: Path) -> None:
    rows = [
        {"relative_path": path.relative_to(folder).as_posix(), "sha256": _sha256(path)}
        for path in sorted(folder.iterdir())
        if path.is_file() and path.name != "S27_V2_PRE2023_VALUATION_MARK_DECLARED_INPUT_PACK_SHA256SUMS.csv"
    ]
    _write_csv(folder / "S27_V2_PRE2023_VALUATION_MARK_DECLARED_INPUT_PACK_SHA256SUMS.csv", rows)


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="ascii"))


def _line_bytes(path: Path, line_number: int) -> bytes:
    lines = path.read_bytes().splitlines(keepends=True)
    return lines[line_number - 1]


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def _hash_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest().upper()


def _canonical_hash(payload: dict[str, Any]) -> str:
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest().upper()


if __name__ == "__main__":
    main()
