from __future__ import annotations

import csv
import hashlib
import json
import os
import sys
from collections import Counter
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
    S26_ZN_DATABENTO_STYPE_IN,
    S26_ZN_EXTENDED_HOURLY_REQUEST_END_UTC,
    S26_ZN_EXTENDED_HOURLY_REQUEST_OUTPUT_ROOT,
    S26_ZN_EXTENDED_HOURLY_REQUEST_START_UTC,
    S26_ZN_EXTENDED_TARGET_COMPLETED_TRADING_DATES,
    S26_ZN_HOURLY_QUARANTINE_STATUS,
    S26_ZN_WORKED_EXAMPLE_AUTHOR_MARKET_CODE,
    S26_ZN_WORKED_EXAMPLE_DATABENTO_INSTRUMENT_ID,
    S26_ZN_WORKED_EXAMPLE_DATABENTO_RAW_SYMBOL,
    S26_ZN_WORKED_EXAMPLE_ROW_ID,
    build_s26_zn_extended_hourly_forecast_only_coverage_manifest,
    validate_s26_zn_extended_hourly_forecast_only_coverage_manifest,
)


RUN_ID = "20260531_G_R1D_ZN_S26_OHLCV_1H_EXTENDED"
GATE = "G_R1D_ZN_S26_EXTENDED_DATABENTO_OHLCV_1H_FORECAST_ONLY_COVERAGE_QUARANTINE_INTAKE"
STRATEGY_CONTEXT = "S26_FAST_MEAN_REVERSION_ZN_WORKED_EXAMPLE_EXTENDED_COVERAGE"
KEY_CANDIDATES = (
    Path(os.environ["DATABENTO_API_KEY_FILE"]) if os.environ.get("DATABENTO_API_KEY_FILE") else None,
    Path("C:/Users/openclaw/Desktop/BentoKey.txt"),
    Path("C:/Users/openclaw/Desktop/BENTO.txt"),
    Path("C:/Users/openclaw/Desktop/bento.txt"),
)


def main() -> None:
    manifest = validate_s26_zn_extended_hourly_forecast_only_coverage_manifest(
        build_s26_zn_extended_hourly_forecast_only_coverage_manifest()
    )
    key = _read_databento_key()

    output_root = ROOT / Path(S26_ZN_EXTENDED_HOURLY_REQUEST_OUTPUT_ROOT)
    folders = {
        "raw_provider_output": output_root / "raw_provider_output",
        "raw_provider_metadata": output_root / "raw_provider_metadata",
        "sanitized_bars": output_root / "sanitized_bars",
        "validation": output_root / "validation",
        "status": output_root / "status",
        "provenance": output_root / "provenance",
        "hashes": output_root / "hashes",
    }
    for folder in folders.values():
        folder.mkdir(parents=True, exist_ok=True)

    raw_dbn = folders["raw_provider_output"] / f"{RUN_ID}.dbn"
    provider_csv = folders["raw_provider_output"] / f"{RUN_ID}_provider_dataframe.csv"
    parser_snapshot_csv = folders["raw_provider_output"] / f"{RUN_ID}_parser_snapshot.csv"
    definition_dbn = folders["raw_provider_metadata"] / f"{RUN_ID}_definition.dbn"
    definition_csv = folders["raw_provider_metadata"] / f"{RUN_ID}_definition_dataframe.csv"
    symbology_json = folders["raw_provider_metadata"] / f"{RUN_ID}_symbology_instrument_id_to_raw_symbol.json"
    condition_json = folders["raw_provider_metadata"] / f"{RUN_ID}_dataset_condition.json"
    sanitized_csv = folders["sanitized_bars"] / f"{RUN_ID}_sanitized_quarantine_ohlcv_1h.csv"
    validation_json = folders["validation"] / f"{RUN_ID}_row_validation.json"
    raw_status_json = folders["status"] / f"{RUN_ID}_raw_request_status.json"
    intake_status_json = folders["status"] / f"{RUN_ID}_quarantine_intake_status.json"
    provenance_json = folders["provenance"] / f"{RUN_ID}_request_provenance.json"
    hashes_json = folders["hashes"] / f"{RUN_ID}_sha256.json"

    client = db.Historical(key)
    store = client.timeseries.get_range(
        dataset=manifest.dataset,
        schema=manifest.schema,
        symbols=[S26_ZN_WORKED_EXAMPLE_DATABENTO_INSTRUMENT_ID],
        stype_in=manifest.stype_in,
        start=_z(manifest.request_start_utc),
        end=_z(manifest.request_end_utc),
        path=raw_dbn,
    )
    provider_df = store.to_df()
    provider_df.to_csv(provider_csv)
    provider_df.to_csv(parser_snapshot_csv)

    definition_store = client.timeseries.get_range(
        dataset=manifest.dataset,
        schema="definition",
        symbols=[S26_ZN_WORKED_EXAMPLE_DATABENTO_INSTRUMENT_ID],
        stype_in=manifest.stype_in,
        start=_z(manifest.request_start_utc),
        end=_z(manifest.request_end_utc),
        path=definition_dbn,
    )
    definition_store.to_df().to_csv(definition_csv)

    symbology = client.symbology.resolve(
        dataset=manifest.dataset,
        symbols=[str(S26_ZN_WORKED_EXAMPLE_DATABENTO_INSTRUMENT_ID)],
        stype_in=manifest.stype_in,
        stype_out="raw_symbol",
        start_date=manifest.request_start_utc.date().isoformat(),
        end_date=manifest.request_end_utc.date().isoformat(),
    )
    _write_json(symbology_json, symbology)

    condition = client.metadata.get_dataset_condition(
        dataset=manifest.dataset,
        start_date=manifest.request_start_utc.date().isoformat(),
        end_date=manifest.request_end_utc.date().isoformat(),
    )
    _write_json(condition_json, condition)

    provider_csv_sha = _sha256(provider_csv)
    condition_by_utc_date = {
        str(row["date"]): f"PROVIDER_CONDITION_{str(row['condition']).upper()}"
        for row in condition
        if row.get("date") and row.get("condition")
    }

    sanitized_rows = _build_sanitized_rows(
        provider_csv,
        provider_csv_sha,
        condition_by_utc_date,
        set(manifest.target_completed_trading_dates),
    )
    _write_sanitized_csv(sanitized_csv, sanitized_rows)

    completed_counts = Counter(row["completed_trading_date"] for row in sanitized_rows)
    provider_condition_counts = Counter(row["provider_condition_status"] for row in sanitized_rows)
    duplicate_status = "PASS_NO_DUPLICATES"
    expected_dates = tuple(S26_ZN_EXTENDED_TARGET_COMPLETED_TRADING_DATES)
    missing_dates = [day for day in expected_dates if completed_counts.get(day, 0) != 23]
    validation_status = (
        "PASS_ROW_SHAPE_COMPLETED_BAR_MAPPING_EXTENDED_QUARANTINE_ONLY_NOT_FORECAST_READY"
        if not missing_dates
        else "FAIL_CLOSED_EXTENDED_COMPLETED_TRADING_DATE_ROW_COUNT_MISMATCH"
    )
    if missing_dates:
        raise SystemExit(f"Fail closed: missing or non-23 row counts for {missing_dates}")

    _write_json(
        validation_json,
        {
            "gate": GATE,
            "validation_status": validation_status,
            "row_count": len(sanitized_rows),
            "completed_bar_policy": "provider ts_event interval start preserved; derived_completed_bar_end_utc = ts_event + 1 hour",
            "completed_trading_date_policy": "UTC hour >=22 maps to next completed trading date, otherwise same UTC date; all rows must map into the 30 locked extended target weekdays.",
            "completed_trading_date_counts": dict(sorted(completed_counts.items())),
            "provider_condition_status_counts": dict(sorted(provider_condition_counts.items())),
            "duplicate_ts_event_status": duplicate_status,
            "strategy_use_status": S26_ZN_HOURLY_QUARANTINE_STATUS,
            "forecast_ready": "NO",
            "diagnostics_run": "NO",
            "backtests_run": "NO",
            "forecasts_run": "NO",
            "positions_run": "NO",
        },
    )
    _write_json(
        raw_status_json,
        {
            "gate": GATE,
            "status": "RAW_DATABENTO_OHLCV_1H_EXTENDED_REQUEST_PRESERVED_VALIDATION_COMPLETE",
            "dataset": manifest.dataset,
            "schema": manifest.schema,
            "instrument_id": S26_ZN_WORKED_EXAMPLE_DATABENTO_INSTRUMENT_ID,
            "expected_raw_symbol": S26_ZN_WORKED_EXAMPLE_DATABENTO_RAW_SYMBOL,
            "start": _z(manifest.request_start_utc),
            "end": _z(manifest.request_end_utc),
            "row_count_provider_dataframe": len(provider_df),
            "definition_row_count": len(definition_store.to_df()),
            "diagnostics_run": "NO",
            "backtests_run": "NO",
            "forecasts_run": "NO",
            "positions_run": "NO",
        },
    )
    _write_json(
        intake_status_json,
        {
            "gate": GATE,
            "intake_status": "PASS_ZN_S26_EXTENDED_HOURLY_OHLCV_1H_QUARANTINE_ONLY_NOT_FORECAST_READY",
            "accepted_quarantine_rows": len(sanitized_rows),
            "target_completed_trading_dates": list(expected_dates),
            "next_required_gate": "ONE_PREVALIDATED_NO_LOOKAHEAD_SIGMA_RUNTIME_PER_FORECAST_ROW_REQUIRED",
            "blocked_before_forecast_reason": "Extended hourly rows remain quarantine-only until one prevalidated sigma_percent runtime exists per emitted forecast row.",
            "sanitized_bars_csv": str(sanitized_csv.relative_to(ROOT)),
            "row_validation_json": str(validation_json.relative_to(ROOT)),
            "diagnostics_run": "NO",
            "backtests_run": "NO",
            "forecasts_run": "NO",
            "positions_run": "NO",
        },
    )
    _write_json(
        provenance_json,
        {
            "gate": GATE,
            "created_at_utc": _z(datetime.now(timezone.utc)),
            "provider": S26_ZN_DATABENTO_PROVIDER,
            "dataset": S26_ZN_DATABENTO_DATASET,
            "schema": S26_ZN_DATABENTO_SCHEMA,
            "stype_in": S26_ZN_DATABENTO_STYPE_IN,
            "symbols": [S26_ZN_WORKED_EXAMPLE_DATABENTO_INSTRUMENT_ID],
            "row_id": S26_ZN_WORKED_EXAMPLE_ROW_ID,
            "author_market_code": S26_ZN_WORKED_EXAMPLE_AUTHOR_MARKET_CODE,
            "expected_raw_symbol": S26_ZN_WORKED_EXAMPLE_DATABENTO_RAW_SYMBOL,
            "request_start_utc": _z(S26_ZN_EXTENDED_HOURLY_REQUEST_START_UTC),
            "request_end_utc": _z(S26_ZN_EXTENDED_HOURLY_REQUEST_END_UTC),
            "target_completed_trading_dates": list(S26_ZN_EXTENDED_TARGET_COMPLETED_TRADING_DATES),
            "continuous_contracts_status": "CLOSED",
            "parent_symbols_status": "CLOSED",
            "raw_symbol_selector_status": "CLOSED_CROSS_CHECK_ONLY",
            "secret_handling": "API key read locally and not written to artifacts or stdout",
            "non_authorization": [
                "NO_DIAGNOSTICS",
                "NO_BACKTESTS",
                "NO_FORECASTS",
                "NO_POSITIONS",
                "NO_COSTS",
                "NO_CARRY",
                "NO_TREND",
                "NO_S27_OVERLAY",
                "NO_OOS",
                "NO_LOCKBOX",
                "NO_FORWARD",
                "NO_DEPLOYMENT",
                "NO_TRADING",
                "NO_PROMOTION",
                "NO_GIT_OPERATIONS",
            ],
        },
    )

    hashes = {
        str(path.relative_to(ROOT)): _sha256(path)
        for path in (
            raw_dbn,
            provider_csv,
            parser_snapshot_csv,
            definition_dbn,
            definition_csv,
            symbology_json,
            condition_json,
            sanitized_csv,
            validation_json,
            raw_status_json,
            intake_status_json,
            provenance_json,
        )
    }
    _write_json(hashes_json, hashes)

    print("PASS_ZN_S26_EXTENDED_HOURLY_OHLCV_1H_QUARANTINE_ONLY_NOT_FORECAST_READY")
    print(f"accepted_quarantine_rows={len(sanitized_rows)}")
    print(f"artifact_root={output_root.relative_to(ROOT)}")


def _read_databento_key() -> str:
    for path in KEY_CANDIDATES:
        if path is None or not path.exists():
            continue
        key = path.read_text(encoding="utf-8").strip()
        if len(key) == 32 and key.startswith("db-"):
            return key
    env_key = os.environ.get("DATABENTO_API_KEY", "").strip()
    if len(env_key) == 32 and env_key.startswith("db-"):
        return env_key
    raise SystemExit("Fail closed: no valid-shaped Databento key found in env or approved local key files")


def _build_sanitized_rows(
    provider_csv: Path,
    source_raw_sha256: str,
    condition_by_utc_date: dict[str, str],
    allowed_completed_dates: set[str],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    with provider_csv.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for record in reader:
            ts = _parse_provider_ts(record["ts_event"])
            if ts.isoformat() in seen:
                raise SystemExit(f"Fail closed: duplicate ts_event {ts.isoformat()}")
            seen.add(ts.isoformat())
            if int(record["instrument_id"]) != S26_ZN_WORKED_EXAMPLE_DATABENTO_INSTRUMENT_ID:
                raise SystemExit("Fail closed: non-manifest instrument_id returned")
            completed_date = _completed_trading_date(ts)
            if completed_date not in allowed_completed_dates:
                continue
            open_ = float(record["open"])
            high = float(record["high"])
            low = float(record["low"])
            close = float(record["close"])
            volume = float(record["volume"])
            if not (low <= open_ <= high and low <= close <= high and volume >= 0):
                raise SystemExit(f"Fail closed: invalid OHLCV row shape at {ts.isoformat()}")
            rows.append(
                {
                    "lane_class": "SOURCE_NATIVE_FUTURES",
                    "strategy_context": STRATEGY_CONTEXT,
                    "provider": S26_ZN_DATABENTO_PROVIDER,
                    "dataset": S26_ZN_DATABENTO_DATASET,
                    "schema": S26_ZN_DATABENTO_SCHEMA,
                    "stype_in": S26_ZN_DATABENTO_STYPE_IN,
                    "row_id": S26_ZN_WORKED_EXAMPLE_ROW_ID,
                    "author_market_code": S26_ZN_WORKED_EXAMPLE_AUTHOR_MARKET_CODE,
                    "instrument_id": S26_ZN_WORKED_EXAMPLE_DATABENTO_INSTRUMENT_ID,
                    "raw_symbol": S26_ZN_WORKED_EXAMPLE_DATABENTO_RAW_SYMBOL,
                    "provider_ts_event_start_utc": _z(ts),
                    "derived_completed_bar_end_utc": _z(ts + timedelta(hours=1)),
                    "completed_trading_date": completed_date,
                    "open": open_,
                    "high": high,
                    "low": low,
                    "close": close,
                    "volume": volume,
                    "provider_condition_status": condition_by_utc_date.get(ts.date().isoformat(), "PROVIDER_CONDITION_UNRESOLVED"),
                    "row_shape_status": "PASS_OHLCV_1H_ROW_SHAPE",
                    "source_raw_sha256": source_raw_sha256,
                    "strategy_use_status": S26_ZN_HOURLY_QUARANTINE_STATUS,
                }
            )
    return rows


def _write_sanitized_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise SystemExit("Fail closed: sanitized extended hourly row set is empty")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def _completed_trading_date(ts: datetime) -> str:
    candidate = ts.date()
    if ts.hour >= 22:
        candidate = (ts + timedelta(days=1)).date()
    return candidate.isoformat()


def _parse_provider_ts(value: str) -> datetime:
    normalized = value.strip().replace(" ", "T").replace("+00:00", "Z")
    ts = datetime.fromisoformat(normalized.replace("Z", "+00:00"))
    if ts.tzinfo is None:
        raise SystemExit("Fail closed: provider timestamp is not timezone-aware")
    ts = ts.astimezone(timezone.utc)
    if ts.minute or ts.second or ts.microsecond:
        raise SystemExit(f"Fail closed: non-hourly timestamp {ts.isoformat()}")
    return ts


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
