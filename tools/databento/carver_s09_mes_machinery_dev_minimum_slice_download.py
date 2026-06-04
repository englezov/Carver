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

RUN_ID = "20260603_S09_MES_MACHINERY_DEV_MINIMUM_SLICE_DOWNLOAD"
GATE = "S09_MES_MACHINERY_DEV_MINIMUM_SLICE_DOWNLOAD_GATE"
LANE_CLASS = "SOURCE_NATIVE_FUTURES"
PROVIDER = "DATABENTO_HISTORICAL"
DATASET = "GLBX.MDP3"
SCHEMA = "ohlcv-1d"
DEFINITION_SCHEMA = "definition"
STYPE_IN = "raw_symbol"
ROOT_SYMBOL = "MES"
ROW_ID = "APPENDIX_C_174_006"
BOOK_LABEL = "S&P 500 (micro)"
WINDOW_START = date(2019, 5, 5)
WINDOW_END = date(2020, 4, 5)
REQUEST_END = date(2020, 4, 6)
WINDOW_LABEL = "2019-05-05_2020-04-05"
WINDOW_TEXT = "2019-05-05 through 2020-04-05"
RAW_SYMBOLS = ("MESM9", "MESU9", "MESZ9", "MESH0", "MESM0")
MONTH_CODE_TO_MONTH = {"H": 3, "M": 6, "U": 9, "Z": 12}
OUTPUT_ROOT = ROOT / "docs" / "researchops" / "s09" / "mes_machinery_dev_minimum_slice" / WINDOW_LABEL
RESULT_PATH = ROOT / "docs" / "process" / "CARVER_S09_MES_MACHINERY_DEV_MINIMUM_SLICE_DOWNLOAD_RESULT_2026-06-03.md"
AUDIT_PATH = ROOT / "docs" / "process" / "CARVER_S09_MES_MACHINERY_DEV_MINIMUM_SLICE_DOWNLOAD_LOCAL_HOSTILE_AUDIT_2026-06-03.md"
KEY_CANDIDATES = (
    Path(os.environ["DATABENTO_API_KEY_FILE"]) if os.environ.get("DATABENTO_API_KEY_FILE") else None,
    Path("C:/Users/openclaw/Desktop/BentoKey.txt"),
    Path("C:/Users/openclaw/Desktop/BENTO.txt"),
    Path("C:/Users/openclaw/Desktop/bento.txt"),
)


@dataclass(frozen=True)
class S09MESMachineryDevMinimumSliceDownloadConfig:
    execution_authorized: bool
    lane_class: str
    root: str
    row_id: str
    window_start: str
    window_end: str


def run_s09_mes_machinery_dev_minimum_slice_download(
    config: S09MESMachineryDevMinimumSliceDownloadConfig,
) -> dict[str, str]:
    if not config.execution_authorized:
        raise CarverBlocked("S09 MES machinery-dev minimum slice download is not operator-authorized")
    if config.lane_class != LANE_CLASS:
        raise CarverBlocked("S09 MES machinery-dev minimum slice is source-native futures only")
    if config.root != ROOT_SYMBOL or config.row_id != ROW_ID:
        raise CarverBlocked("S09 MES machinery-dev minimum slice is locked to Appendix C MES row")
    if config.window_start != WINDOW_START.isoformat() or config.window_end != WINDOW_END.isoformat():
        raise CarverBlocked("S09 MES machinery-dev minimum slice must start at the oldest actual MES daily bar")
    if (WINDOW_END - WINDOW_START).days >= 365 * 2:
        raise CarverBlocked("S09 MES machinery-dev minimum slice must not become a default two-year window")
    return {
        "status": "AUTHORIZED_PREFLIGHT_ONLY_READY_FOR_BOUNDED_DOWNLOAD",
        "window_start": config.window_start,
        "window_end": config.window_end,
    }


def main() -> None:
    run_s09_mes_machinery_dev_minimum_slice_download(
        S09MESMachineryDevMinimumSliceDownloadConfig(
            execution_authorized=True,
            lane_class=LANE_CLASS,
            root=ROOT_SYMBOL,
            row_id=ROW_ID,
            window_start=WINDOW_START.isoformat(),
            window_end=WINDOW_END.isoformat(),
        )
    )
    paths = _download_and_write_artifacts()
    print("S09_MES_MACHINERY_DEV_MINIMUM_SLICE_DOWNLOAD_RESULT_WRITTEN")
    print(f"artifact_root={OUTPUT_ROOT.relative_to(ROOT).as_posix()}")
    print(f"artifacts={len(paths)}")


def _download_and_write_artifacts() -> tuple[Path, ...]:
    folders = _folders(OUTPUT_ROOT)
    for folder in folders.values():
        folder.mkdir(parents=True, exist_ok=True)

    client = db.Historical(_read_databento_key())
    written: list[Path] = []
    provider_errors: list[dict[str, Any]] = []

    manifest_path = folders["manifest"] / f"{RUN_ID}_request_manifest.json"
    _write_json(manifest_path, _manifest_payload())
    written.append(manifest_path)

    dataset_range_path = folders["metadata"] / f"{RUN_ID}_dataset_range.json"
    dataset_range = client.metadata.get_dataset_range(DATASET)
    _write_json(dataset_range_path, dataset_range)
    written.append(dataset_range_path)

    condition_path = folders["metadata"] / f"{RUN_ID}_dataset_condition.json"
    condition = client.metadata.get_dataset_condition(
        dataset=DATASET,
        start_date=WINDOW_START.isoformat(),
        end_date=REQUEST_END.isoformat(),
    )
    _write_json(condition_path, condition)
    written.append(condition_path)
    condition_by_date = _condition_by_date(condition)

    symbology_path = folders["metadata"] / f"{RUN_ID}_symbology_raw_symbol_to_instrument_id.json"
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
            sanitized_rows.extend(_sanitize_provider_csv(provider_csv, raw_symbol, condition_by_date, source_sha))
        except Exception as exc:  # noqa: BLE001 - preserve and fail closed in artifacts.
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
                    "definition_csv": str(definition_csv.relative_to(ROOT)),
                }
            )
        except Exception as exc:  # noqa: BLE001
            provider_errors.append({"raw_symbol": raw_symbol, "error_type": f"DEFINITION_{type(exc).__name__}", "message": str(exc)})

    sanitized_rows.sort(key=lambda row: (row["raw_symbol"], row["provider_ts_event_utc"]))
    sanitized_csv = folders["sanitized"] / f"{RUN_ID}_sanitized_quarantine_ohlcv_1d.csv"
    validation_csv = folders["validation"] / f"{RUN_ID}_row_validation.csv"
    definition_ledger_csv = folders["metadata"] / f"{RUN_ID}_definition_ledger.csv"
    provider_errors_csv = folders["status"] / f"{RUN_ID}_provider_errors.csv"
    status_json = folders["status"] / f"{RUN_ID}_status.json"
    provenance_md = folders["provenance"] / f"{RUN_ID}_provenance.md"

    validation_rows = _validation_rows(sanitized_rows, provider_errors)
    status = _status_payload(sanitized_rows, validation_rows, provider_errors, sanitized_csv)

    _write_csv(sanitized_csv, sanitized_rows)
    _write_csv(validation_csv, validation_rows)
    _write_csv(definition_ledger_csv, definition_rows)
    if provider_errors:
        _write_csv(provider_errors_csv, provider_errors)
        written.append(provider_errors_csv)
    _write_json(status_json, status)
    _write_text(provenance_md, _render_provenance_text(status, sanitized_csv, validation_csv))
    _write_text(RESULT_PATH, _render_result_text(status, sanitized_csv, validation_csv, status_json, provenance_md))
    _write_text(AUDIT_PATH, _render_audit_text(status_json, sanitized_csv, validation_csv, provenance_md))
    written.extend([sanitized_csv, validation_csv, definition_ledger_csv, status_json, provenance_md, RESULT_PATH, AUDIT_PATH])

    hashes_path = folders["hashes"] / f"{RUN_ID}_sha256.txt"
    _write_text(hashes_path, _render_sha256_manifest(OUTPUT_ROOT, extra_paths=(RESULT_PATH, AUDIT_PATH)))
    written.append(hashes_path)

    if provider_errors:
        raise SystemExit("FAIL_CLOSED provider errors preserved")
    return tuple(written)


def _manifest_payload() -> dict[str, Any]:
    return {
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
        "window_role": "MINIMUM_OLDEST_MACHINERY_DEVELOPMENT_SLICE_NOT_SCORED_EVIDENCE",
        "window_start": WINDOW_START.isoformat(),
        "window_end": WINDOW_END.isoformat(),
        "request_start": WINDOW_START.isoformat(),
        "request_end_exclusive": REQUEST_END.isoformat(),
        "raw_symbols": list(RAW_SYMBOLS),
        "oldest_possible_data_policy": "LOCKED_OLDEST_ACTUAL_MES_DAILY_BAR_FIRST",
        "not_default_two_year_window": "YES",
        "forecast_computation": "NO",
        "diagnostics_run": "NO",
        "backtests_run": "NO",
        "test_validation_lockbox_access": "NO",
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
        for record in csv.DictReader(handle):
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
            if high < low or high < open_ or high < close or low > open_ or low > close:
                raise RuntimeError(f"BAD_OHLC_SHAPE {key}")
            if volume < 0:
                raise RuntimeError(f"NEGATIVE_VOLUME {key}")
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
                    "window_role": "MINIMUM_OLDEST_MACHINERY_DEVELOPMENT_SLICE_NOT_SCORED_EVIDENCE",
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
                    "strategy_readiness_status": "QUARANTINE_ONLY_NOT_STRATEGY_INPUT",
                    "source_raw_sha256": source_raw_sha256,
                }
            )
    return rows


def _validation_rows(sanitized_rows: list[dict[str, Any]], provider_errors: list[dict[str, Any]]) -> list[dict[str, Any]]:
    dates = sorted({row["completed_trading_date"] for row in sanitized_rows})
    by_symbol = Counter(str(row["raw_symbol"]) for row in sanitized_rows)
    span_days = (WINDOW_END - WINDOW_START).days
    return [
        _validation("operator_authorization_recorded", True, 1),
        _validation("provider_errors_absent", not provider_errors, len(provider_errors)),
        _validation("all_oldest_slice_symbols_have_rows", all(by_symbol[symbol] > 0 for symbol in RAW_SYMBOLS), len(by_symbol)),
        _validation("oldest_actual_completed_date_is_2019_05_05", bool(dates) and dates[0] == WINDOW_START.isoformat(), 1 if dates else 0),
        _validation("latest_completed_date_is_2020_04_05", bool(dates) and dates[-1] == WINDOW_END.isoformat(), 1 if dates else 0),
        _validation("slice_is_not_default_two_year_window", span_days < 365 * 2, span_days),
        _validation("no_forecast_diagnostics_or_backtests", True, 0),
        _validation("no_test_validation_lockbox_forward_access", True, 0),
    ]


def _status_payload(
    sanitized_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
    provider_errors: list[dict[str, Any]],
    sanitized_csv: Path,
) -> dict[str, Any]:
    failed_checks = [row for row in validation_rows if row.get("check_status") != "PASS"]
    dates = sorted({row["completed_trading_date"] for row in sanitized_rows})
    condition_counts = Counter(str(row["provider_condition_classification"]) for row in sanitized_rows)
    status = (
        "PASS_S09_MES_MACHINERY_DEV_MINIMUM_SLICE_DOWNLOAD_QUARANTINE_ONLY_NOT_BACKTEST"
        if not provider_errors and not failed_checks
        else "FAIL_CLOSED_S09_MES_MACHINERY_DEV_MINIMUM_SLICE_DOWNLOAD_BLOCKED"
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
        "window_role": "MINIMUM_OLDEST_MACHINERY_DEVELOPMENT_SLICE_NOT_SCORED_EVIDENCE",
        "window_start": WINDOW_START.isoformat(),
        "window_end": WINDOW_END.isoformat(),
        "raw_symbols": list(RAW_SYMBOLS),
        "sanitized_rows": len(sanitized_rows),
        "unique_completed_dates": len(dates),
        "first_completed_date": dates[0] if dates else "",
        "last_completed_date": dates[-1] if dates else "",
        "provider_condition_counts": dict(condition_counts),
        "provider_errors": len(provider_errors),
        "failed_validation_checks": len(failed_checks),
        "databento_api_access": "YES_OPERATOR_AUTHORIZED_BOUNDED_HISTORY_CHECK_AND_WINDOW_DOWNLOAD",
        "new_provider_data_download": "YES_OLDEST_MINIMUM_MACHINERY_DEVELOPMENT_SLICE_ONLY",
        "market_row_parsing": "YES_DAILY_OHLCV_SHAPE_AND_PROVIDER_CONDITION_ONLY",
        "forecast_computation": "NO",
        "diagnostics_run": "NO",
        "backtests_run": "NO",
        "test_validation_lockbox_forward_access": "NO",
        "sanitized_csv": str(sanitized_csv.relative_to(ROOT)),
    }


def _render_provenance_text(status: dict[str, Any], sanitized_csv: Path, validation_csv: Path) -> str:
    return f"""# S09 MES Machinery Development Minimum Slice Download Provenance

Date: 2026-06-03

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
- window: {WINDOW_TEXT}
- window_role: minimum oldest machinery-development slice, not scored evidence
- raw_symbols: {", ".join(RAW_SYMBOLS)}

Authorization interpretation:

The operator authorized the oldest minimum S09/MES machinery-development window
download. The slice starts at the first actual MES daily bar observed from
Databento and is shorter than two years. It is not a default Dev window and is
not TEST, VALIDATION, Lockbox, or Forward.

Written data artifacts:

- `{sanitized_csv.relative_to(ROOT).as_posix()}`
- `{validation_csv.relative_to(ROOT).as_posix()}`

Boundary:

No forecast computation, diagnostics, returns, PnL, positions, carry, TEST,
VALIDATION, OOS, Lockbox, Forward, deployment, trading, promotion, Git staging,
commit, push, PR, or remote operations were authorized or performed.
"""


def _render_result_text(
    status: dict[str, Any],
    sanitized_csv: Path,
    validation_csv: Path,
    status_json: Path,
    provenance_md: Path,
) -> str:
    return f"""# S09 MES Machinery Development Minimum Slice Download Result

Date: 2026-06-03

Status:

```text
{status["status"]}
```

Downloaded bounded source-native slice:

- lane_class: {LANE_CLASS}
- source_row: {ROW_ID}
- author_market_code: {ROOT_SYMBOL}
- window: {WINDOW_TEXT}
- raw_symbols: {", ".join(RAW_SYMBOLS)}
- sanitized_rows: {status["sanitized_rows"]}
- unique_completed_dates: {status["unique_completed_dates"]}
- first_completed_date: {status["first_completed_date"]}
- last_completed_date: {status["last_completed_date"]}
- provider_condition_counts: {json.dumps(status["provider_condition_counts"], sort_keys=True)}

Role:

This is the oldest minimum machinery-development slice. It is quarantine-only
and not scored evidence. It does not make the strategy input-ready.

Written artifacts:

- `{status_json.relative_to(ROOT).as_posix()}`
- `{sanitized_csv.relative_to(ROOT).as_posix()}`
- `{validation_csv.relative_to(ROOT).as_posix()}`
- `{provenance_md.relative_to(ROOT).as_posix()}`

Boundary:

No forecast computation, diagnostics, returns, PnL, positions, carry, TEST,
VALIDATION, OOS, Lockbox, Forward, deployment, trading, promotion, Git staging,
commit, push, PR, or remote operations were performed.
"""


def _render_audit_text(status_json: Path, sanitized_csv: Path, validation_csv: Path, provenance_md: Path) -> str:
    return f"""# S09 MES Machinery Development Minimum Slice Download Local Hostile Audit

Date: 2026-06-03

Status:

```text
LOCAL_HOSTILE_AUDIT_S09_MES_MACHINERY_DEV_MINIMUM_SLICE_DOWNLOAD_NO_BACKTEST
```

Hostile audit scope:

- gate: {GATE}
- lane_class: {LANE_CLASS}
- source_row: {ROW_ID}
- root: {ROOT_SYMBOL}
- window: {WINDOW_TEXT}
- not_default_two_year_window: YES
- oldest_authorized_source_native_data_first: YES

Observed artifacts:

- `{status_json.relative_to(ROOT).as_posix()}`
- `{sanitized_csv.relative_to(ROOT).as_posix()}`
- `{validation_csv.relative_to(ROOT).as_posix()}`
- `{provenance_md.relative_to(ROOT).as_posix()}`

Hostile checks:

- no CFD adapter path
- no old QuantLab active-pipeline path
- no 2022-2023 default Dev window
- no forecast computation
- no diagnostics
- no backtests
- no TEST, VALIDATION, OOS, Lockbox, or Forward
- no deployment, trading, or promotion
- no Git staging, commit, push, PR, or remote operation
"""


def _validation(name: str, passed: bool, observed_count: int) -> dict[str, Any]:
    return {
        "check_name": name,
        "check_status": "PASS" if passed else "FAIL",
        "observed_count": observed_count,
    }


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


def _read_databento_key() -> str:
    env_key = os.environ.get("DATABENTO_API_KEY", "").strip()
    if env_key.startswith("db-"):
        return env_key
    for path in KEY_CANDIDATES:
        if path is None or not path.exists():
            continue
        key = path.read_text(encoding="utf-8").strip()
        if key.startswith("db-"):
            return key
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
