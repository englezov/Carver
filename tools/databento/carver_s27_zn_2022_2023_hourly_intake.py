from __future__ import annotations

import csv
import hashlib
import json
import os
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import databento as db

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.carver.spine.s26_s27 import (
    S26_ZN_DATABENTO_DATASET,
    S26_ZN_DATABENTO_PROVIDER,
    S26_ZN_DATABENTO_SCHEMA,
    S26_ZN_WORKED_EXAMPLE_AUTHOR_MARKET_CODE,
    S26_ZN_WORKED_EXAMPLE_ROW_ID,
    S27_ZN_BACKTEST_HOURLY_ARCHIVE_OUTPUT_ROOT,
    S27_ZN_BACKTEST_HOURLY_ARCHIVE_REQUEST_END_UTC,
    S27_ZN_BACKTEST_HOURLY_ARCHIVE_REQUEST_START_UTC,
    S27_ZN_BACKTEST_HOURLY_ARCHIVE_REQUIRED_RAW_SYMBOLS,
    S27_ZN_BACKTEST_TARGET_COMPLETED_TRADING_DATE_END,
    S27_ZN_BACKTEST_TARGET_COMPLETED_TRADING_DATE_START,
    build_s27_zn_backtest_hourly_archive_window_manifest,
    validate_s27_zn_backtest_hourly_archive_window_manifest,
)


RUN_ID = "20260531_S27_ZN_2022_2023_OHLCV_1H_ARCHIVE"
GATE = "S27_ZN_2022_2023_DATABENTO_OHLCV_1H_QUARANTINE_INTAKE"
STRATEGY_CONTEXT = "S27_SAFER_FAST_MEAN_REVERSION_ZN_2022_2023_DEV_RECON"
KEY_CANDIDATES = (
    Path(os.environ["DATABENTO_API_KEY_FILE"]) if os.environ.get("DATABENTO_API_KEY_FILE") else None,
    Path("C:/Users/openclaw/Desktop/BentoKey.txt"),
    Path("C:/Users/openclaw/Desktop/BENTO.txt"),
    Path("C:/Users/openclaw/Desktop/bento.txt"),
)


def main() -> None:
    manifest = validate_s27_zn_backtest_hourly_archive_window_manifest(
        build_s27_zn_backtest_hourly_archive_window_manifest()
    )
    key = _read_databento_key()
    output_root = ROOT / Path(S27_ZN_BACKTEST_HOURLY_ARCHIVE_OUTPUT_ROOT)
    folders = _folders(output_root)
    for folder in folders.values():
        folder.mkdir(parents=True, exist_ok=True)

    client = db.Historical(key)
    _write_json(folders["manifest"] / f"{RUN_ID}_request_manifest.json", _manifest_payload(manifest))

    condition = client.metadata.get_dataset_condition(
        dataset=manifest.dataset,
        start_date=manifest.request_start_utc.date().isoformat(),
        end_date=manifest.request_end_utc.date().isoformat(),
    )
    condition_json = folders["metadata"] / f"{RUN_ID}_dataset_condition.json"
    _write_json(condition_json, condition)
    condition_by_date = {
        str(row["date"]): str(row["condition"]).upper()
        for row in condition
        if row.get("date") and row.get("condition")
    }

    all_sanitized_rows: list[dict[str, Any]] = []
    symbology_rows: list[dict[str, Any]] = []
    definition_rows: list[dict[str, Any]] = []
    provider_errors: list[dict[str, Any]] = []
    raw_paths: list[Path] = [condition_json, folders["manifest"] / f"{RUN_ID}_request_manifest.json"]

    for raw_symbol in manifest.required_raw_symbols:
        try:
            symbology_json = folders["metadata"] / f"{RUN_ID}_{raw_symbol}_symbology_raw_symbol_to_instrument_id.json"
            symbology = client.symbology.resolve(
                dataset=manifest.dataset,
                symbols=[raw_symbol],
                stype_in="raw_symbol",
                stype_out="instrument_id",
                start_date=manifest.request_start_utc.date().isoformat(),
                end_date=manifest.request_end_utc.date().isoformat(),
            )
            _write_json(symbology_json, symbology)
            raw_paths.append(symbology_json)
            resolved = symbology.get("result", {}).get(raw_symbol, [])
            if not resolved:
                raise RuntimeError("SYMBOL_NOT_RESOLVED")
            symbology_rows.extend(
                {
                    "raw_symbol": raw_symbol,
                    "resolved_d0": item.get("d0"),
                    "resolved_d1": item.get("d1"),
                    "instrument_id": item.get("s"),
                }
                for item in resolved
            )

            raw_dbn = folders["raw"] / f"{RUN_ID}_{raw_symbol}.dbn"
            provider_csv = folders["raw"] / f"{RUN_ID}_{raw_symbol}_provider.csv"
            store = client.timeseries.get_range(
                dataset=manifest.dataset,
                schema=manifest.schema,
                symbols=[raw_symbol],
                stype_in=manifest.stype_in,
                start=_z(manifest.request_start_utc),
                end=_z(manifest.request_end_utc),
                path=raw_dbn,
            )
            provider_df = store.to_df()
            provider_df.to_csv(provider_csv)
            raw_paths.extend([raw_dbn, provider_csv])

            definition_dbn = folders["metadata"] / f"{RUN_ID}_{raw_symbol}_definition.dbn"
            definition_csv = folders["metadata"] / f"{RUN_ID}_{raw_symbol}_definition.csv"
            definition_store = client.timeseries.get_range(
                dataset=manifest.dataset,
                schema="definition",
                symbols=[raw_symbol],
                stype_in=manifest.stype_in,
                start=_z(manifest.request_start_utc),
                end=_z(manifest.request_end_utc),
                path=definition_dbn,
            )
            definition_df = definition_store.to_df()
            definition_df.to_csv(definition_csv)
            raw_paths.extend([definition_dbn, definition_csv])
            definition_rows.append(
                {
                    "raw_symbol": raw_symbol,
                    "definition_rows": len(definition_df),
                    "definition_csv": str(definition_csv.relative_to(ROOT)),
                }
            )

            source_sha = _sha256(provider_csv)
            rows = _sanitize_provider_csv(
                provider_csv=provider_csv,
                raw_symbol=raw_symbol,
                source_raw_sha256=source_sha,
                condition_by_date=condition_by_date,
            )
            if not rows:
                raise RuntimeError("NO_TARGET_WINDOW_ROWS")
            all_sanitized_rows.extend(rows)
        except Exception as exc:  # noqa: BLE001 - preserve provider failure as data evidence.
            provider_errors.append(
                {
                    "raw_symbol": raw_symbol,
                    "error_type": type(exc).__name__,
                    "message": str(exc),
                }
            )

    symbology_csv = folders["metadata"] / f"{RUN_ID}_symbology_resolution_ledger.csv"
    definition_ledger_csv = folders["metadata"] / f"{RUN_ID}_definition_ledger.csv"
    provider_errors_csv = folders["status"] / f"{RUN_ID}_provider_errors.csv"
    _write_csv(symbology_csv, symbology_rows)
    _write_csv(definition_ledger_csv, definition_rows)
    raw_paths.extend([symbology_csv, definition_ledger_csv])
    if provider_errors:
        _write_csv(provider_errors_csv, provider_errors)
        raw_paths.append(provider_errors_csv)

    sanitized_csv = folders["sanitized"] / f"{RUN_ID}_sanitized_quarantine_ohlcv_1h.csv"
    validation_json = folders["validation"] / f"{RUN_ID}_row_validation.json"
    status_json = folders["status"] / f"{RUN_ID}_quarantine_intake_status.json"
    provenance_json = folders["provenance"] / f"{RUN_ID}_provenance.json"
    hashes_json = folders["hashes"] / f"{RUN_ID}_sha256.json"

    all_sanitized_rows.sort(key=lambda row: (row["raw_symbol"], row["provider_ts_event_start_utc"]))
    _write_csv(sanitized_csv, all_sanitized_rows)
    validation = _validation_payload(all_sanitized_rows, provider_errors)
    _write_json(validation_json, validation)
    status = _status_payload(all_sanitized_rows, provider_errors, validation, sanitized_csv, validation_json)
    _write_json(status_json, status)
    _write_json(provenance_json, _provenance_payload(sanitized_csv, validation_json, status_json))
    raw_paths.extend([sanitized_csv, validation_json, status_json, provenance_json])
    _write_json(hashes_json, {str(path.relative_to(ROOT)): _sha256(path) for path in raw_paths if path.exists()})

    if provider_errors:
        raise SystemExit(f"FAIL_CLOSED provider_errors={len(provider_errors)} artifact_root={output_root.relative_to(ROOT)}")
    print(status["status"])
    print(f"accepted_quarantine_rows={len(all_sanitized_rows)}")
    print(f"artifact_root={output_root.relative_to(ROOT)}")


def _folders(output_root: Path) -> dict[str, Path]:
    return {
        "manifest": output_root / "manifest",
        "raw": output_root / "raw_provider_output",
        "metadata": output_root / "raw_provider_metadata",
        "sanitized": output_root / "sanitized_hourly_bars",
        "validation": output_root / "validation",
        "status": output_root / "status",
        "provenance": output_root / "provenance",
        "hashes": output_root / "hashes",
    }


def _manifest_payload(manifest: Any) -> dict[str, Any]:
    return {
        "gate": GATE,
        "provider": manifest.provider,
        "dataset": manifest.dataset,
        "schema": manifest.schema,
        "stype_in": manifest.stype_in,
        "row_id": manifest.row_id,
        "author_market_code": manifest.author_market_code,
        "request_start_utc": _z(manifest.request_start_utc),
        "request_end_utc": _z(manifest.request_end_utc),
        "target_completed_trading_date_start": manifest.target_completed_trading_date_start,
        "target_completed_trading_date_end": manifest.target_completed_trading_date_end,
        "required_raw_symbols": list(manifest.required_raw_symbols),
        "local_continuous_policy": manifest.local_continuous_policy,
        "provider_condition_policy": manifest.provider_condition_policy,
        "non_authorization": [
            "NO_DIAGNOSTICS",
            "NO_BACKTESTS",
            "NO_FORECASTS",
            "NO_POSITIONS",
            "NO_COSTS",
            "NO_OOS",
            "NO_LOCKBOX",
            "NO_FORWARD",
            "NO_DEPLOYMENT",
            "NO_TRADING",
            "NO_PROMOTION",
            "NO_GIT_OPERATIONS",
        ],
    }


def _sanitize_provider_csv(
    *,
    provider_csv: Path,
    raw_symbol: str,
    source_raw_sha256: str,
    condition_by_date: dict[str, str],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    with provider_csv.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for record in reader:
            ts = _parse_provider_ts(record["ts_event"])
            key = f"{raw_symbol}|{ts.isoformat()}"
            if key in seen:
                raise RuntimeError(f"DUPLICATE_TS_EVENT {key}")
            seen.add(key)
            completed_date = _completed_trading_date(ts)
            if completed_date < S27_ZN_BACKTEST_TARGET_COMPLETED_TRADING_DATE_START:
                continue
            if completed_date > S27_ZN_BACKTEST_TARGET_COMPLETED_TRADING_DATE_END:
                continue
            symbol_value = str(record.get("symbol", "")).strip()
            if symbol_value and symbol_value not in {raw_symbol, str(record.get("instrument_id", "")).strip()}:
                raise RuntimeError(f"SYMBOL_DRIFT {raw_symbol} got {symbol_value}")
            open_ = float(record["open"])
            high = float(record["high"])
            low = float(record["low"])
            close = float(record["close"])
            volume = float(record["volume"])
            if not (low <= open_ <= high and low <= close <= high and volume >= 0.0):
                raise RuntimeError(f"BAD_OHLCV_SHAPE {raw_symbol} {ts.isoformat()}")
            condition_status = f"PROVIDER_CONDITION_{condition_by_date.get(ts.date().isoformat(), 'UNRESOLVED')}"
            strategy_use_status = (
                "QUARANTINE_ONLY_PROVIDER_CONDITION_AVAILABLE_NOT_BACKTEST_READY"
                if condition_status == "PROVIDER_CONDITION_AVAILABLE"
                else "QUARANTINE_PRESERVED_PROVIDER_CONDITION_BLOCKED_NOT_BACKTEST_READY"
            )
            rows.append(
                {
                    "lane_class": "SOURCE_NATIVE_FUTURES",
                    "strategy_context": STRATEGY_CONTEXT,
                    "provider": S26_ZN_DATABENTO_PROVIDER,
                    "dataset": S26_ZN_DATABENTO_DATASET,
                    "schema": S26_ZN_DATABENTO_SCHEMA,
                    "stype_in": "raw_symbol",
                    "row_id": S26_ZN_WORKED_EXAMPLE_ROW_ID,
                    "author_market_code": S26_ZN_WORKED_EXAMPLE_AUTHOR_MARKET_CODE,
                    "raw_symbol": raw_symbol,
                    "instrument_id": int(record["instrument_id"]),
                    "provider_ts_event_start_utc": _z(ts),
                    "derived_completed_bar_end_utc": _z(ts + timedelta(hours=1)),
                    "completed_trading_date": completed_date,
                    "open": open_,
                    "high": high,
                    "low": low,
                    "close": close,
                    "volume": volume,
                    "provider_condition_status": condition_status,
                    "row_shape_status": "PASS_OHLCV_1H_ROW_SHAPE",
                    "source_raw_sha256": source_raw_sha256,
                    "strategy_use_status": strategy_use_status,
                }
            )
    return rows


def _validation_payload(rows: list[dict[str, Any]], provider_errors: list[dict[str, Any]]) -> dict[str, Any]:
    by_symbol = Counter(row["raw_symbol"] for row in rows)
    by_condition = Counter(row["provider_condition_status"] for row in rows)
    by_symbol_date: dict[str, Counter[str]] = defaultdict(Counter)
    seen = set()
    duplicates = []
    for row in rows:
        key = (row["raw_symbol"], row["provider_ts_event_start_utc"])
        if key in seen:
            duplicates.append({"raw_symbol": key[0], "provider_ts_event_start_utc": key[1]})
        seen.add(key)
        by_symbol_date[row["raw_symbol"]][row["completed_trading_date"]] += 1
    missing_symbols = [symbol for symbol in S27_ZN_BACKTEST_HOURLY_ARCHIVE_REQUIRED_RAW_SYMBOLS if by_symbol[symbol] == 0]
    provider_condition_blocked_rows = sum(
        count for condition, count in by_condition.items() if condition != "PROVIDER_CONDITION_AVAILABLE"
    )
    status = "PASS_S27_ZN_2022_2023_OHLCV_1H_QUARANTINE_INTAKE_NOT_BACKTEST_READY"
    if provider_errors or duplicates or missing_symbols:
        status = "FAIL_CLOSED_S27_ZN_2022_2023_OHLCV_1H_QUARANTINE_INTAKE"
    elif provider_condition_blocked_rows:
        status = "FAIL_CLOSED_PROVIDER_CONDITION_BLOCKERS_PRESENT_NOT_BACKTEST_READY"
    return {
        "gate": GATE,
        "validation_status": status,
        "row_count": len(rows),
        "raw_symbol_row_counts": dict(sorted(by_symbol.items())),
        "provider_condition_status_counts": dict(sorted(by_condition.items())),
        "provider_condition_blocked_rows": provider_condition_blocked_rows,
        "completed_trading_date_counts_by_raw_symbol": {
            symbol: dict(sorted(counts.items())) for symbol, counts in sorted(by_symbol_date.items())
        },
        "missing_raw_symbols": missing_symbols,
        "duplicate_count": len(duplicates),
        "duplicates": duplicates,
        "provider_error_count": len(provider_errors),
        "provider_errors": provider_errors,
        "completed_bar_policy": "provider ts_event interval start preserved; derived_completed_bar_end_utc = ts_event + 1 hour",
        "completed_trading_date_policy": "UTC hour >=22 maps to next completed trading date, otherwise same UTC date",
        "diagnostics_run": "NO",
        "backtests_run": "NO",
        "forecasts_run": "NO",
        "positions_run": "NO",
        "costs_run": "NO",
    }


def _status_payload(
    rows: list[dict[str, Any]],
    provider_errors: list[dict[str, Any]],
    validation: dict[str, Any],
    sanitized_csv: Path,
    validation_json: Path,
) -> dict[str, Any]:
    status = validation["validation_status"]
    return {
        "gate": GATE,
        "status": status,
        "provider": S26_ZN_DATABENTO_PROVIDER,
        "dataset": S26_ZN_DATABENTO_DATASET,
        "schema": S26_ZN_DATABENTO_SCHEMA,
        "request_start_utc": _z(S27_ZN_BACKTEST_HOURLY_ARCHIVE_REQUEST_START_UTC),
        "request_end_utc": _z(S27_ZN_BACKTEST_HOURLY_ARCHIVE_REQUEST_END_UTC),
        "target_completed_trading_date_start": S27_ZN_BACKTEST_TARGET_COMPLETED_TRADING_DATE_START,
        "target_completed_trading_date_end": S27_ZN_BACKTEST_TARGET_COMPLETED_TRADING_DATE_END,
        "raw_symbols": list(S27_ZN_BACKTEST_HOURLY_ARCHIVE_REQUIRED_RAW_SYMBOLS),
        "accepted_quarantine_rows": len(rows),
        "provider_error_count": len(provider_errors),
        "sanitized_csv": str(sanitized_csv.relative_to(ROOT)),
        "validation_json": str(validation_json.relative_to(ROOT)),
        "next_required_gate": "S27_ZN_2022_2023_DEV_RECON_BACKTEST_EXECUTION_GATE",
        "diagnostics_run": "NO",
        "backtests_run": "NO",
        "forecasts_run": "NO",
        "positions_run": "NO",
        "costs_run": "NO",
        "oos_access": "NO",
        "lockbox_access": "NO",
        "forward_access": "NO",
        "promotion": "NO",
    }


def _provenance_payload(sanitized_csv: Path, validation_json: Path, status_json: Path) -> dict[str, Any]:
    return {
        "gate": GATE,
        "created_at_utc": _z(datetime.now(timezone.utc)),
        "provider": S26_ZN_DATABENTO_PROVIDER,
        "dataset": S26_ZN_DATABENTO_DATASET,
        "schema": S26_ZN_DATABENTO_SCHEMA,
        "stype_in": "raw_symbol",
        "row_id": S26_ZN_WORKED_EXAMPLE_ROW_ID,
        "author_market_code": S26_ZN_WORKED_EXAMPLE_AUTHOR_MARKET_CODE,
        "raw_symbols": list(S27_ZN_BACKTEST_HOURLY_ARCHIVE_REQUIRED_RAW_SYMBOLS),
        "request_start_utc": _z(S27_ZN_BACKTEST_HOURLY_ARCHIVE_REQUEST_START_UTC),
        "request_end_utc": _z(S27_ZN_BACKTEST_HOURLY_ARCHIVE_REQUEST_END_UTC),
        "target_completed_trading_date_start": S27_ZN_BACKTEST_TARGET_COMPLETED_TRADING_DATE_START,
        "target_completed_trading_date_end": S27_ZN_BACKTEST_TARGET_COMPLETED_TRADING_DATE_END,
        "sanitized_csv": str(sanitized_csv.relative_to(ROOT)),
        "validation_json": str(validation_json.relative_to(ROOT)),
        "status_json": str(status_json.relative_to(ROOT)),
        "secret_handling": "API key read locally and not written to artifacts or stdout",
        "non_authorization": [
            "NO_DIAGNOSTICS",
            "NO_BACKTESTS",
            "NO_FORECASTS",
            "NO_POSITIONS",
            "NO_COSTS",
            "NO_OOS",
            "NO_LOCKBOX",
            "NO_FORWARD",
            "NO_DEPLOYMENT",
            "NO_TRADING",
            "NO_PROMOTION",
            "NO_GIT_OPERATIONS",
        ],
    }


def _read_databento_key() -> str:
    env_key = os.environ.get("DATABENTO_API_KEY", "").strip()
    if len(env_key) == 32 and env_key.startswith("db-"):
        return env_key
    for path in KEY_CANDIDATES:
        if path is None or not path.exists():
            continue
        key = path.read_text(encoding="utf-8").strip()
        if len(key) == 32 and key.startswith("db-"):
            return key
    raise SystemExit("Fail closed: no valid-shaped Databento key found")


def _completed_trading_date(ts: datetime) -> str:
    candidate = ts.date()
    if ts.hour >= 22:
        candidate = (ts + timedelta(days=1)).date()
    return candidate.isoformat()


def _parse_provider_ts(value: str) -> datetime:
    normalized = value.strip().replace(" ", "T").replace("+00:00", "Z")
    ts = datetime.fromisoformat(normalized.replace("Z", "+00:00"))
    if ts.tzinfo is None:
        raise RuntimeError("NAIVE_PROVIDER_TIMESTAMP")
    ts = ts.astimezone(timezone.utc)
    if ts.minute or ts.second or ts.microsecond:
        raise RuntimeError(f"NON_HOURLY_TIMESTAMP {ts.isoformat()}")
    return ts


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def _write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8")


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def _z(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    main()
