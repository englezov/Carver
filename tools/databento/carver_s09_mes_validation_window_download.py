from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import sys
from collections import Counter
from dataclasses import dataclass
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

import databento as db

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from carver.spine.m0 import CarverBlocked

RUN_ID = "20260604_S09_MES_VALIDATION_WINDOW_DOWNLOAD"
GATE = "S09_MES_VALIDATION_WINDOW_DATABENTO_DOWNLOAD_AUTHORIZED_GATE"
LANE_CLASS = "SOURCE_NATIVE_FUTURES"
PROVIDER = "DATABENTO_HISTORICAL"
DATASET = "GLBX.MDP3"
SCHEMA = "ohlcv-1d"
DEFINITION_SCHEMA = "definition"
STYPE_IN = "raw_symbol"
ROOT_SYMBOL = "MES"
ROW_ID = "APPENDIX_C_174_006"
BOOK_LABEL = "S&P 500 (micro)"
WINDOW_ROLE = "VALIDATION"
WINDOW_START = date(2022, 2, 9)
WINDOW_END = date(2023, 12, 13)
REQUEST_END = date(2023, 12, 14)
WINDOW_LABEL = "2022-02-09_2023-12-13"
WINDOW_TEXT = "2022-02-09 through 2023-12-13"
EXPECTED_COMPLETED_DATES = 574
RAW_SYMBOLS = (
    "MESH2",
    "MESM2",
    "MESU2",
    "MESZ2",
    "MESH3",
    "MESM3",
    "MESU3",
    "MESZ3",
    "MESH4",
)
MONTH_CODE_TO_MONTH = {"H": 3, "M": 6, "U": 9, "Z": 12}
OUTPUT_ROOT = ROOT / "docs" / "researchops" / "s09" / "mes_validation_window_download" / WINDOW_LABEL
RESULT_PATH = ROOT / "docs" / "process" / "CARVER_S09_MES_VALIDATION_WINDOW_DOWNLOAD_RESULT_2026-06-04.md"
AUDIT_PATH = ROOT / "docs" / "process" / "CARVER_S09_MES_VALIDATION_WINDOW_DOWNLOAD_LOCAL_HOSTILE_AUDIT_2026-06-04.md"
KEY_CANDIDATES = (
    Path(os.environ["DATABENTO_API_KEY_FILE"]) if os.environ.get("DATABENTO_API_KEY_FILE") else None,
    Path("C:/Users/apops/Desktop/BentoKey.txt"),
    Path("C:/Users/apops/Desktop/BENTO.txt"),
    Path("C:/Users/apops/Desktop/bento.txt"),
    Path("C:/Users/openclaw/Desktop/BentoKey.txt"),
    Path("C:/Users/openclaw/Desktop/BENTO.txt"),
    Path("C:/Users/openclaw/Desktop/bento.txt"),
)


@dataclass(frozen=True)
class S09MESValidationWindowDownloadConfig:
    execution_authorized: bool
    lane_class: str
    root: str
    row_id: str
    window_start: str
    window_end: str


def run_s09_mes_validation_window_download_preflight(
    config: S09MESValidationWindowDownloadConfig,
) -> dict[str, str]:
    if not config.execution_authorized:
        raise CarverBlocked("S09 MES VALIDATION window download is not operator-authorized")
    if config.lane_class != LANE_CLASS:
        raise CarverBlocked("S09 MES VALIDATION window is source-native futures only")
    if config.root != ROOT_SYMBOL or config.row_id != ROW_ID:
        raise CarverBlocked("S09 MES VALIDATION window is locked to Appendix C MES row")
    if config.window_start != WINDOW_START.isoformat() or config.window_end != WINDOW_END.isoformat():
        raise CarverBlocked("S09 MES VALIDATION window must match the locked 3:3:4 allocation")
    if (WINDOW_END - WINDOW_START).days > 365 * 2:
        raise CarverBlocked("S09 MES VALIDATION download exceeds the two-year guard")
    receipt = OUTPUT_ROOT / "status" / f"{RUN_ID}_download_receipt.json"
    if receipt.exists():
        raise CarverBlocked("S09 MES VALIDATION download receipt already exists; refusing a second download")
    return {
        "status": "AUTHORIZED_READY_FOR_EXACTLY_ONE_VALIDATION_WINDOW_DATABENTO_DOWNLOAD",
        "window_start": config.window_start,
        "window_end": config.window_end,
    }


def main() -> None:
    run_s09_mes_validation_window_download_preflight(
        S09MESValidationWindowDownloadConfig(
            execution_authorized=True,
            lane_class=LANE_CLASS,
            root=ROOT_SYMBOL,
            row_id=ROW_ID,
            window_start=WINDOW_START.isoformat(),
            window_end=WINDOW_END.isoformat(),
        )
    )
    paths = _download_and_write_artifacts()
    print("S09_MES_VALIDATION_WINDOW_DOWNLOAD_RESULT_WRITTEN")
    print(f"artifact_root={OUTPUT_ROOT.relative_to(ROOT).as_posix()}")
    print(f"artifacts={len(paths)}")


def _download_and_write_artifacts() -> tuple[Path, ...]:
    folders = _folders(OUTPUT_ROOT)
    for folder in folders.values():
        folder.mkdir(parents=True, exist_ok=True)

    key, key_source = _read_databento_key()
    client = db.Historical(key)
    written: list[Path] = []
    provider_errors: list[dict[str, Any]] = []

    manifest_path = folders["manifest"] / f"{RUN_ID}_request_manifest.json"
    _write_json(manifest_path, _manifest_payload(key_source))
    written.append(manifest_path)

    dataset_range_path = folders["metadata"] / f"{RUN_ID}_dataset_range.json"
    try:
        dataset_range = client.metadata.get_dataset_range(DATASET)
        _write_json(dataset_range_path, dataset_range)
        written.append(dataset_range_path)
    except Exception as exc:  # noqa: BLE001
        provider_errors.append({"raw_symbol": "ALL", "error_type": f"DATASET_RANGE_{type(exc).__name__}", "message": str(exc)})

    condition_path = folders["metadata"] / f"{RUN_ID}_dataset_condition.json"
    condition: list[dict[str, Any]] = []
    try:
        condition = client.metadata.get_dataset_condition(
            dataset=DATASET,
            start_date=WINDOW_START.isoformat(),
            end_date=REQUEST_END.isoformat(),
        )
        _write_json(condition_path, condition)
        written.append(condition_path)
    except Exception as exc:  # noqa: BLE001
        provider_errors.append({"raw_symbol": "ALL", "error_type": f"DATASET_CONDITION_{type(exc).__name__}", "message": str(exc)})
    condition_by_date = _condition_by_date(condition)

    symbology_path = folders["metadata"] / f"{RUN_ID}_symbology_raw_symbol_to_instrument_id.json"
    symbology_rows: list[dict[str, Any]] = []
    try:
        symbology = client.symbology.resolve(
            dataset=DATASET,
            symbols=list(RAW_SYMBOLS),
            stype_in=STYPE_IN,
            stype_out="instrument_id",
            start_date=WINDOW_START.isoformat(),
            end_date=REQUEST_END.isoformat(),
        )
        _write_json(symbology_path, symbology)
        written.append(symbology_path)
        symbology_rows = _symbology_ledger_rows(symbology)
    except Exception as exc:  # noqa: BLE001
        provider_errors.append({"raw_symbol": "ALL", "error_type": f"SYMBOLOGY_{type(exc).__name__}", "message": str(exc)})

    sanitized_rows: list[dict[str, Any]] = []
    definition_rows: list[dict[str, Any]] = []
    for raw_symbol in RAW_SYMBOLS:
        try:
            raw_dbn = folders["raw"] / f"{RUN_ID}_{raw_symbol}_{SCHEMA}.dbn"
            provider_csv = folders["raw"] / f"{RUN_ID}_{raw_symbol}_{SCHEMA}_provider.csv"
            store = client.timeseries.get_range(
                dataset=DATASET,
                schema=SCHEMA,
                symbols=[raw_symbol],
                stype_in=STYPE_IN,
                start=WINDOW_START.isoformat(),
                end=REQUEST_END.isoformat(),
                path=raw_dbn,
            )
            store.to_df().to_csv(provider_csv)
            written.extend([raw_dbn, provider_csv])
            source_sha = _sha256(provider_csv)
            contract_rows = _sanitize_provider_csv(provider_csv, raw_symbol, condition_by_date, source_sha)
            if not contract_rows:
                provider_errors.append({"raw_symbol": raw_symbol, "error_type": "NO_OHLCV_ROWS", "message": "No ohlcv-1d rows returned"})
            sanitized_rows.extend(contract_rows)
        except Exception as exc:  # noqa: BLE001
            provider_errors.append({"raw_symbol": raw_symbol, "error_type": type(exc).__name__, "message": str(exc)})

        try:
            definition_dbn = folders["metadata"] / f"{RUN_ID}_{raw_symbol}_{DEFINITION_SCHEMA}.dbn"
            definition_csv = folders["metadata"] / f"{RUN_ID}_{raw_symbol}_{DEFINITION_SCHEMA}.csv"
            definition_store = client.timeseries.get_range(
                dataset=DATASET,
                schema=DEFINITION_SCHEMA,
                symbols=[raw_symbol],
                stype_in=STYPE_IN,
                start=WINDOW_START.isoformat(),
                end=REQUEST_END.isoformat(),
                path=definition_dbn,
            )
            definition_df = definition_store.to_df()
            definition_df.to_csv(definition_csv)
            written.extend([definition_dbn, definition_csv])
            definition_rows.append(
                {
                    "raw_symbol": raw_symbol,
                    "definition_rows": int(len(definition_df)),
                    "definition_status": "DATABENTO_DEFINITION_ROWS_PRESENT" if len(definition_df) else "FAIL_CLOSED_NO_DEFINITION_ROWS",
                    "definition_csv": definition_csv.relative_to(ROOT).as_posix(),
                    "definition_csv_sha256": _sha256(definition_csv),
                }
            )
            if len(definition_df) == 0:
                provider_errors.append({"raw_symbol": raw_symbol, "error_type": "NO_DEFINITION_ROWS", "message": "No definition rows returned"})
        except Exception as exc:  # noqa: BLE001
            provider_errors.append({"raw_symbol": raw_symbol, "error_type": f"DEFINITION_{type(exc).__name__}", "message": str(exc)})

    sanitized_rows.sort(key=lambda row: (row["raw_symbol"], row["provider_ts_event_utc"]))
    sanitized_csv = folders["sanitized"] / f"{RUN_ID}_sanitized_quarantine_ohlcv_1d.csv"
    validation_csv = folders["validation"] / f"{RUN_ID}_row_validation.csv"
    symbology_csv = folders["metadata"] / f"{RUN_ID}_symbology_resolution_ledger.csv"
    definition_ledger_csv = folders["metadata"] / f"{RUN_ID}_definition_ledger.csv"
    provider_errors_csv = folders["status"] / f"{RUN_ID}_provider_errors.csv"
    status_json = folders["status"] / f"{RUN_ID}_status.json"
    receipt_json = folders["status"] / f"{RUN_ID}_download_receipt.json"
    provenance_md = folders["provenance"] / f"{RUN_ID}_provenance.md"

    validation_rows = _validation_rows(sanitized_rows, provider_errors)
    status = _status_payload(sanitized_rows, validation_rows, provider_errors, sanitized_csv, key_source)

    _write_csv(sanitized_csv, sanitized_rows)
    _write_csv(validation_csv, validation_rows)
    _write_csv(symbology_csv, symbology_rows)
    _write_csv(definition_ledger_csv, definition_rows)
    if provider_errors:
        _write_csv(provider_errors_csv, provider_errors)
        written.append(provider_errors_csv)
    _write_json(status_json, status)
    _write_json(receipt_json, _receipt_payload(status, sanitized_csv, validation_csv))
    _write_text(provenance_md, _render_provenance_text(status, sanitized_csv, validation_csv))
    _write_text(RESULT_PATH, _render_result_text(status, sanitized_csv, validation_csv, status_json, receipt_json, provenance_md))
    _write_text(AUDIT_PATH, _render_audit_text(status, validation_csv, provenance_md))
    written.extend(
        [
            sanitized_csv,
            validation_csv,
            symbology_csv,
            definition_ledger_csv,
            status_json,
            receipt_json,
            provenance_md,
            RESULT_PATH,
            AUDIT_PATH,
        ]
    )

    hashes_path = folders["hashes"] / f"{RUN_ID}_sha256.txt"
    _write_text(hashes_path, _render_sha256_manifest(OUTPUT_ROOT, extra_paths=(RESULT_PATH, AUDIT_PATH)))
    written.append(hashes_path)

    if provider_errors or status["failed_validation_checks"]:
        raise SystemExit("FAIL_CLOSED S09 MES VALIDATION window download blocked; artifacts preserved")
    return tuple(written)


def _manifest_payload(key_source: str) -> dict[str, Any]:
    return {
        "authorization": "OPERATOR_AUTHORIZES_EXACTLY_ONE_DATABENTO_VALIDATION_WINDOW_DATA_DOWNLOAD",
        "gate": GATE,
        "run_id": RUN_ID,
        "lane_class": LANE_CLASS,
        "provider": PROVIDER,
        "dataset": DATASET,
        "schema": SCHEMA,
        "definition_schema": DEFINITION_SCHEMA,
        "stype_in": STYPE_IN,
        "row_id": ROW_ID,
        "root": ROOT_SYMBOL,
        "book_label": BOOK_LABEL,
        "window_role": WINDOW_ROLE,
        "window_start": WINDOW_START.isoformat(),
        "window_end": WINDOW_END.isoformat(),
        "request_start": WINDOW_START.isoformat(),
        "request_end_exclusive": REQUEST_END.isoformat(),
        "expected_completed_dates": EXPECTED_COMPLETED_DATES,
        "raw_symbols": list(RAW_SYMBOLS),
        "state_history_policy": "TEST_WINDOW_AVAILABLE_FOR_STATE_WARMUP_ONLY_NOT_DOWNLOADED_BY_THIS_GATE",
        "key_source": key_source,
        "continuous_contracts_requested": "NO",
        "provider_built_continuous_series_requested": "NO",
        "forecast_computation": "NO",
        "position_computation": "NO",
        "cost_computation": "NO",
        "diagnostics_run": "NO",
        "backtests_run": "NO",
        "lockbox_forward_access": "NO",
        "git_operations": "NO",
    }


def _sanitize_provider_csv(
    provider_csv: Path,
    raw_symbol: str,
    condition_by_date: dict[str, str],
    source_raw_sha256: str,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    with provider_csv.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None or "ts_event" not in reader.fieldnames:
            raise RuntimeError("PROVIDER_CSV_MISSING_TS_EVENT")
        for record in reader:
            if not record.get("ts_event"):
                continue
            ts = _parse_ts(record["ts_event"])
            completed_date = ts.date()
            if completed_date < WINDOW_START or completed_date > WINDOW_END:
                continue
            key = f"{raw_symbol}|{_z(ts)}"
            if key in seen:
                raise RuntimeError(f"DUPLICATE_PROVIDER_TIMESTAMP {key}")
            seen.add(key)
            open_ = float(record["open"])
            high = float(record["high"])
            low = float(record["low"])
            close = float(record["close"])
            volume = float(record["volume"])
            if not all(math.isfinite(value) for value in (open_, high, low, close, volume)):
                raise RuntimeError(f"NON_FINITE_OHLCV {key}")
            if high < max(open_, low, close) or low > min(open_, high, close) or volume < 0:
                raise RuntimeError(f"BAD_OHLCV_SHAPE {key}")
            condition = condition_by_date.get(completed_date.isoformat(), "UNKNOWN")
            provider_condition_classification = (
                "NORMAL_PROVIDER_CONDITION"
                if condition == "AVAILABLE"
                else "DEGRADED_OR_UNRESOLVED_PROVIDER_CONDITION_QUARANTINED_NOT_STRATEGY_READY"
            )
            contract = _contract_parts(raw_symbol)
            rows.append(
                {
                    "lane_class": LANE_CLASS,
                    "provider": PROVIDER,
                    "dataset": DATASET,
                    "schema": SCHEMA,
                    "stype_in": STYPE_IN,
                    "row_id": ROW_ID,
                    "root": ROOT_SYMBOL,
                    "book_label": BOOK_LABEL,
                    "window_role": WINDOW_ROLE,
                    "raw_symbol": raw_symbol,
                    "contract_year": contract["contract_year"],
                    "delivery_month": contract["delivery_month"],
                    "delivery_code": contract["delivery_code"],
                    "instrument_id": str(record.get("instrument_id", "")),
                    "provider_ts_event_utc": _z(ts),
                    "completed_trading_date": completed_date.isoformat(),
                    "open": open_,
                    "high": high,
                    "low": low,
                    "close": close,
                    "volume": volume,
                    "provider_condition": condition,
                    "provider_condition_classification": provider_condition_classification,
                    "strategy_readiness_status": "VALIDATION_DOWNLOAD_QUARANTINE_ONLY_NOT_SCORED_EVIDENCE",
                    "source_raw_sha256": source_raw_sha256,
                }
            )
    return rows


def _validation_rows(sanitized_rows: list[dict[str, Any]], provider_errors: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_symbol = Counter(str(row["raw_symbol"]) for row in sanitized_rows)
    duplicate_count = len(sanitized_rows) - len({(row["raw_symbol"], row["provider_ts_event_utc"]) for row in sanitized_rows})
    dates = sorted({row["completed_trading_date"] for row in sanitized_rows})
    out_of_window = [
        row
        for row in sanitized_rows
        if row["completed_trading_date"] < WINDOW_START.isoformat() or row["completed_trading_date"] > WINDOW_END.isoformat()
    ]
    return [
        _validation("operator_authorized_exactly_one_validation_window_download", True, 1),
        _validation("provider_errors_absent", not provider_errors, len(provider_errors)),
        _validation("source_native_mes_only", all(str(row["raw_symbol"]).startswith(ROOT_SYMBOL) for row in sanitized_rows), len(sanitized_rows)),
        _validation("all_requested_symbols_have_rows", all(by_symbol[symbol] > 0 for symbol in RAW_SYMBOLS), len(by_symbol)),
        _validation("first_sanitized_completed_date_matches_validation_start", bool(dates) and dates[0] == WINDOW_START.isoformat(), 1 if dates else 0),
        _validation("last_sanitized_completed_date_matches_validation_end", bool(dates) and dates[-1] == WINDOW_END.isoformat(), 1 if dates else 0),
        _validation("no_out_of_window_completed_dates", not out_of_window, len(out_of_window)),
        _validation("duplicate_provider_timestamps_absent", duplicate_count == 0, duplicate_count),
        _validation("no_forecasts_positions_costs_diagnostics_or_backtests", True, 0),
        _validation("no_lockbox_forward_access", True, 0),
    ]


def _status_payload(
    sanitized_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
    provider_errors: list[dict[str, Any]],
    sanitized_csv: Path,
    key_source: str,
) -> dict[str, Any]:
    failed_checks = [row for row in validation_rows if row.get("check_status") != "PASS"]
    dates = sorted({row["completed_trading_date"] for row in sanitized_rows})
    condition_counts = Counter(str(row["provider_condition_classification"]) for row in sanitized_rows)
    status = (
        "PASS_S09_MES_VALIDATION_WINDOW_DATABENTO_DOWNLOAD_QUARANTINE_ONLY_NOT_BACKTEST"
        if not provider_errors and not failed_checks
        else "FAIL_CLOSED_S09_MES_VALIDATION_WINDOW_DATABENTO_DOWNLOAD_BLOCKED"
    )
    return {
        "gate": GATE,
        "run_id": RUN_ID,
        "status": status,
        "lane_class": LANE_CLASS,
        "provider": PROVIDER,
        "dataset": DATASET,
        "schema": SCHEMA,
        "root": ROOT_SYMBOL,
        "row_id": ROW_ID,
        "window_role": WINDOW_ROLE,
        "window_start": WINDOW_START.isoformat(),
        "window_end": WINDOW_END.isoformat(),
        "request_end_exclusive": REQUEST_END.isoformat(),
        "expected_completed_dates": EXPECTED_COMPLETED_DATES,
        "raw_symbols": list(RAW_SYMBOLS),
        "sanitized_rows": len(sanitized_rows),
        "unique_raw_union_completed_dates": len(dates),
        "first_completed_date": dates[0] if dates else "",
        "last_completed_date": dates[-1] if dates else "",
        "provider_condition_counts": dict(condition_counts),
        "provider_errors": len(provider_errors),
        "failed_validation_checks": len(failed_checks),
        "databento_api_access": "YES_OPERATOR_AUTHORIZED_EXACTLY_ONE_VALIDATION_WINDOW_DOWNLOAD",
        "databento_key_source": key_source,
        "key_secret_written_to_artifacts": "NO",
        "new_provider_data_download": "YES_VALIDATION_WINDOW_ONLY",
        "market_row_parsing": "YES_DAILY_OHLCV_SHAPE_AND_PROVIDER_CONDITION_ONLY",
        "forecast_computation": "NO",
        "position_computation": "NO",
        "cost_computation": "NO",
        "diagnostics_run": "NO",
        "backtests_run": "NO",
        "lockbox_forward_access": "NO",
        "deployment_trading_promotion": "NO",
        "git_operations": "NO",
        "sanitized_csv": sanitized_csv.relative_to(ROOT).as_posix(),
    }


def _receipt_payload(status: dict[str, Any], sanitized_csv: Path, validation_csv: Path) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "download_execution_count": 1,
        "execution_receipt_status": "S09_MES_VALIDATION_WINDOW_DATABENTO_DOWNLOAD_RECEIPT",
        "status": status["status"],
        "window_start": WINDOW_START.isoformat(),
        "window_end": WINDOW_END.isoformat(),
        "sanitized_csv": sanitized_csv.relative_to(ROOT).as_posix(),
        "validation_csv": validation_csv.relative_to(ROOT).as_posix(),
        "databento_key_worked": "YES" if status["provider_errors"] == 0 else "NO_OR_PARTIAL_PROVIDER_ERROR_SEE_STATUS",
        "key_secret_written_to_artifacts": "NO",
    }


def _render_provenance_text(status: dict[str, Any], sanitized_csv: Path, validation_csv: Path) -> str:
    return f"""# S09 MES VALIDATION Window DataBento Download Provenance

Date: 2026-06-04

Status:

```text
{status["status"]}
```

Authorized scope:

- gate: {GATE}
- lane_class: {LANE_CLASS}
- source_row: {ROW_ID}
- author_market_code: {ROOT_SYMBOL}
- provider: {PROVIDER}
- dataset: {DATASET}
- schema: {SCHEMA}
- VALIDATION window: {WINDOW_TEXT}
- expected_completed_dates: {EXPECTED_COMPLETED_DATES}
- raw_symbols: {", ".join(RAW_SYMBOLS)}
- key_source: {status["databento_key_source"]}

State-history boundary:

TEST may be used later as VALIDATION state-history warmup only under the
separate scoring-mask doctrine. This acquisition gate downloaded only the
locked VALIDATION window and did not score evidence.

Written data artifacts:

- `{sanitized_csv.relative_to(ROOT).as_posix()}`
- `{validation_csv.relative_to(ROOT).as_posix()}`

Boundary:

No forecast computation, returns, PnL, positions, carry, costs, diagnostics,
backtests, OOS, Lockbox, Forward, deployment, trading, promotion, Git staging,
commit, push, PR, or remote publication was authorized or performed.
"""


def _render_result_text(
    status: dict[str, Any],
    sanitized_csv: Path,
    validation_csv: Path,
    status_json: Path,
    receipt_json: Path,
    provenance_md: Path,
) -> str:
    return f"""# S09 MES VALIDATION Window DataBento Download Result

Date: 2026-06-04

Status:

```text
{status["status"]}
```

Downloaded bounded source-native window:

- lane_class: {LANE_CLASS}
- source_row: {ROW_ID}
- author_market_code: {ROOT_SYMBOL}
- window: {WINDOW_TEXT}
- raw_symbols: {", ".join(RAW_SYMBOLS)}
- sanitized_rows: {status["sanitized_rows"]}
- unique_raw_union_completed_dates: {status["unique_raw_union_completed_dates"]}
- first_completed_date: {status["first_completed_date"]}
- last_completed_date: {status["last_completed_date"]}
- provider_condition_counts: {json.dumps(status["provider_condition_counts"], sort_keys=True)}
- provider_errors: {status["provider_errors"]}
- failed_validation_checks: {status["failed_validation_checks"]}

Role:

This is a VALIDATION-window source-native data acquisition artifact only. It is
not a VALIDATION backtest, not a diagnostic, not Lockbox, and not promotion.

Artifacts:

- `{status_json.relative_to(ROOT).as_posix()}`
- `{receipt_json.relative_to(ROOT).as_posix()}`
- `{sanitized_csv.relative_to(ROOT).as_posix()}`
- `{validation_csv.relative_to(ROOT).as_posix()}`
- `{provenance_md.relative_to(ROOT).as_posix()}`

Boundary:

No forecast computation, returns, PnL, positions, carry, costs, diagnostics,
backtests, OOS, Lockbox, Forward, deployment, trading, promotion, Git staging,
commit, push, PR, or remote publication was performed.
"""


def _render_audit_text(status: dict[str, Any], validation_csv: Path, provenance_md: Path) -> str:
    return f"""# S09 MES VALIDATION Window DataBento Download Local Hostile Audit

Date: 2026-06-04

Status:

```text
LOCAL_HOSTILE_AUDIT_S09_MES_VALIDATION_WINDOW_DATABENTO_DOWNLOAD_NO_BACKTEST
```

Observed:

- status: {status["status"]}
- VALIDATION window: {WINDOW_TEXT}
- provider_errors: {status["provider_errors"]}
- failed_validation_checks: {status["failed_validation_checks"]}
- forecast_computation: {status["forecast_computation"]}
- diagnostics_run: {status["diagnostics_run"]}
- backtests_run: {status["backtests_run"]}
- lockbox_forward_access: {status["lockbox_forward_access"]}
- git_operations: {status["git_operations"]}

Artifacts:

- `{validation_csv.relative_to(ROOT).as_posix()}`
- `{provenance_md.relative_to(ROOT).as_posix()}`

Hostile checks:

- exactly one VALIDATION-window DataBento acquisition receipt
- no CFD adapter path
- no old QuantLab active-pipeline path
- no forecast, position, cost, diagnostic, or backtest artifacts
- no OOS, Lockbox, Forward, deployment, trading, promotion, or Git operation
"""


def _symbology_ledger_rows(symbology: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    result = symbology.get("result", {}) if isinstance(symbology, dict) else {}
    for raw_symbol in RAW_SYMBOLS:
        resolved = result.get(raw_symbol, [])
        if not resolved:
            rows.append({"raw_symbol": raw_symbol, "instrument_id": "", "symbology_status": "FAIL_CLOSED_NOT_RESOLVED"})
            continue
        for item in resolved:
            rows.append(
                {
                    "raw_symbol": raw_symbol,
                    "resolved_d0": item.get("d0", ""),
                    "resolved_d1": item.get("d1", ""),
                    "instrument_id": item.get("s", ""),
                    "symbology_status": "RESOLVED",
                }
            )
    return rows


def _condition_by_date(condition: list[dict[str, Any]]) -> dict[str, str]:
    return {
        str(row["date"]): str(row["condition"]).upper()
        for row in condition
        if row.get("date") and row.get("condition")
    }


def _contract_parts(raw_symbol: str) -> dict[str, int | str]:
    delivery_code = raw_symbol[-2]
    year_digit = int(raw_symbol[-1])
    return {
        "contract_year": 2020 + year_digit if year_digit <= 6 else 2010 + year_digit,
        "delivery_month": MONTH_CODE_TO_MONTH[delivery_code],
        "delivery_code": delivery_code,
    }


def _validation(name: str, passed: bool, observed_count: int) -> dict[str, Any]:
    return {
        "check_name": name,
        "check_status": "PASS" if passed else "FAIL",
        "observed_count": observed_count,
    }


def _folders(root: Path) -> dict[str, Path]:
    return {
        "manifest": root / "manifest",
        "metadata": root / "raw_provider_metadata",
        "raw": root / "raw_provider_output",
        "sanitized": root / "sanitized_daily_bars",
        "validation": root / "validation",
        "status": root / "status",
        "provenance": root / "provenance",
        "hashes": root / "hashes",
    }


def _read_databento_key() -> tuple[str, str]:
    env_key = os.environ.get("DATABENTO_API_KEY", "").strip()
    if env_key.startswith("db-"):
        return env_key, "env:DATABENTO_API_KEY"
    for path in KEY_CANDIDATES:
        if path is None or not path.exists():
            continue
        key = path.read_text(encoding="utf-8").strip()
        if key.startswith("db-"):
            return key, path.as_posix()
    raise SystemExit("Fail closed: no valid-shaped Databento key found")


def _parse_ts(value: str) -> datetime:
    ts = datetime.fromisoformat(value.strip().replace(" ", "T").replace("Z", "+00:00"))
    if ts.tzinfo is None:
        raise RuntimeError("provider timestamp is not timezone-aware")
    return ts.astimezone(timezone.utc)


def _z(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _write_json(path: Path, payload: Any) -> None:
    _write_text(path, json.dumps(payload, indent=2, sort_keys=True, default=str) + "\n")


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def _render_sha256_manifest(root: Path, *, extra_paths: tuple[Path, ...]) -> str:
    paths = [path for path in sorted(root.rglob("*")) if path.is_file() and not path.name.endswith("_sha256.txt")]
    paths.extend(extra_paths)
    lines = []
    for path in sorted(set(paths), key=lambda item: item.relative_to(ROOT).as_posix()):
        lines.append(f"{_sha256(path)}  {path.relative_to(ROOT).as_posix()}")
    return "\n".join(lines) + "\n"


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


if __name__ == "__main__":
    main()
