from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.carver.spine.m0 import LaneClass, SourceRuleStatus
from src.carver.spine.s26_s27 import (
    S26_EQUILIBRIUM_EWMA_SPAN,
    S26QuarantinedHourlyOHLCVBar,
    S26QuarantinedHourlyForecastSeriesRequest,
    S26QuarantinedHourlySourceLocks,
    S26SigmaPercentRuntimeValue,
    S26_ZN_DATABENTO_DATASET,
    S26_ZN_DATABENTO_PROVIDER,
    S26_ZN_DATABENTO_SCHEMA,
    S26_ZN_DATABENTO_STYPE_IN,
    S26_ZN_EXTENDED_HOURLY_REQUEST_OUTPUT_ROOT,
    S26_ZN_FORECAST_SERIES_STATUS,
    S26_ZN_HOURLY_QUARANTINE_STATUS,
    S26_ZN_SIGMA_RUNTIME_STATUS,
    S26_ZN_WORKED_EXAMPLE_AUTHOR_MARKET_CODE,
    S26_ZN_WORKED_EXAMPLE_DATABENTO_INSTRUMENT_ID,
    S26_ZN_WORKED_EXAMPLE_DATABENTO_RAW_SYMBOL,
    S26_ZN_WORKED_EXAMPLE_ROW_ID,
    s26_forecast_series_only_from_quarantined_zn_hourly_ohlcv_bars,
)


RUN_ID = "20260531_G_R1E_ZN_S26_EXTENDED_SIGMA_AND_FORECAST_SERIES"
GATE = "G_R1E_ZN_S26_EXTENDED_NO_LOOKAHEAD_SIGMA_RUNTIME_LEDGER_AND_FORECAST_SERIES_ONLY"
HOURLY_CSV = (
    ROOT
    / S26_ZN_EXTENDED_HOURLY_REQUEST_OUTPUT_ROOT
    / "sanitized_bars"
    / "20260531_G_R1D_ZN_S26_OHLCV_1H_EXTENDED_sanitized_quarantine_ohlcv_1h.csv"
)
DAILY_CSV = (
    ROOT
    / "docs/researchops/source_native_futures_daily_data_library/16_SYMBOL_FULL_DAILY_HISTORY/raw_provider_archive/"
    / "DATABENTO/20260530_DATED_CONTRACT_FULL_AVAILABLE_HISTORY_PER_SYMBOL_CURRENT_IDS/raw_provider_output/"
    / "databento_GLBX-MDP3_ohlcv-1d_ZNM6_42000661_full_available_provider.csv"
)
CANONICAL_MANIFEST = (
    ROOT
    / "docs/researchops/source_native_futures_daily_data_library/16_SYMBOL_DAILY_LIBRARY_PROMOTION_READINESS/manifest/"
    / "CARVER_16_SYMBOL_DATABENTO_DAILY_LIBRARY_CANONICAL_MANIFEST_2026-05-30.csv"
)
OUTPUT_ROOT = (
    ROOT
    / "docs/researchops/s26_s27_hourly_bridge/ZN_S26_WORKED_EXAMPLE/2026-04-13_2026-05-22/"
    / "forecast_series_only_output/2026-05-31"
)


def main() -> None:
    manifest_row = _load_zn_manifest_row()
    daily_sha = _sha256(DAILY_CSV)
    if daily_sha != manifest_row["raw_provider_csv_sha256"]:
        raise SystemExit("Fail closed: ZNM6 daily raw provider CSV hash does not match canonical manifest")

    hourly_bars = _load_hourly_bars()
    daily_rows = _load_normal_daily_rows(manifest_row)
    forecast_bars = hourly_bars[S26_EQUILIBRIUM_EWMA_SPAN - 1 :]
    if not forecast_bars:
        raise SystemExit("Fail closed: no eligible S26 forecast rows")

    source_window_rows = []
    runtime_seed_rows = []
    for bar in forecast_bars:
        window = _daily_window_before(daily_rows, bar.completed_trading_date)
        sigma = _short_run_ewma32_sigma_percent(window)
        source_window_rows.append(
            {
                "as_of": _z(bar.derived_completed_bar_end_utc),
                "completed_trading_date": bar.completed_trading_date,
                "source_window_start_completed_trading_date": window[0]["completed_trading_date"],
                "source_window_end_completed_trading_date": window[-1]["completed_trading_date"],
                "source_window_row_count": len(window),
                "source_window_return_count": len(window) - 1,
                "source_window_close_first": window[0]["close"],
                "source_window_close_last": window[-1]["close"],
                "sigma_percent_t": sigma,
                "method_detail": "SHORT_RUN_EWMA32_ANNUALIZED_PERCENT_RETURN_CURRENT_RISK_COMPONENT_FOR_S26_SIGMA_PRICE",
                "no_lookahead_status": "PASS_NO_LOOKAHEAD",
                "source_window_status": "PASS_SOURCE_WINDOW_PREVALIDATED",
                "provider_condition_policy": "ALL_SOURCE_WINDOW_ROWS_ROW_READY_PROVIDER_CONDITION_NORMAL",
            }
        )
        runtime_seed_rows.append((bar.derived_completed_bar_end_utc, sigma))

    folders = {
        "runtime": OUTPUT_ROOT / "sigma_runtime_ledger",
        "forecast": OUTPUT_ROOT / "forecast_rows",
        "provenance": OUTPUT_ROOT / "provenance",
        "hashes": OUTPUT_ROOT / "hashes",
    }
    for folder in folders.values():
        folder.mkdir(parents=True, exist_ok=True)

    source_window_csv = folders["runtime"] / f"{RUN_ID}_source_window_ledger.csv"
    _write_csv(source_window_csv, source_window_rows)
    source_window_sha = _sha256(source_window_csv)

    runtime_rows = [
        {
            "gate": GATE,
            "runtime_status": S26_ZN_SIGMA_RUNTIME_STATUS,
            "method_status": "LOCKED_TO_PART_ONE_S03_VARIABLE_RISK_FAMILY",
            "method_detail": "SHORT_RUN_EWMA32_ANNUALIZED_PERCENT_RETURN_CURRENT_RISK_COMPONENT_FOR_S26_SIGMA_PRICE; NOT_FULL_POSITION_SIZING_BLEND",
            "row_id": S26_ZN_WORKED_EXAMPLE_ROW_ID,
            "author_market_code": S26_ZN_WORKED_EXAMPLE_AUTHOR_MARKET_CODE,
            "instrument_id": S26_ZN_WORKED_EXAMPLE_DATABENTO_INSTRUMENT_ID,
            "raw_symbol": S26_ZN_WORKED_EXAMPLE_DATABENTO_RAW_SYMBOL,
            "as_of": _z(as_of),
            "sigma_percent_t": sigma,
            "no_lookahead_status": "PASS_NO_LOOKAHEAD",
            "source_window_status": "PASS_SOURCE_WINDOW_PREVALIDATED",
            "source_window_ledger_sha256": source_window_sha,
        }
        for as_of, sigma in runtime_seed_rows
    ]
    runtime_ledger_csv = folders["runtime"] / f"{RUN_ID}_runtime_ledger.csv"
    _write_csv(runtime_ledger_csv, runtime_rows)

    runtimes = tuple(
        S26SigmaPercentRuntimeValue(
            value=float(row["sigma_percent_t"]),
            as_of=_parse_utc(row["as_of"]),
            runtime_status=S26_ZN_SIGMA_RUNTIME_STATUS,
            method_status="LOCKED_TO_PART_ONE_S03_VARIABLE_RISK_FAMILY",
            no_lookahead_status="PASS_NO_LOOKAHEAD",
            source_artifact_sha256=source_window_sha,
            source_window_status="PASS_SOURCE_WINDOW_PREVALIDATED",
        )
        for row in runtime_rows
    )
    result = s26_forecast_series_only_from_quarantined_zn_hourly_ohlcv_bars(
        S26QuarantinedHourlyForecastSeriesRequest(
            bars=tuple(hourly_bars),
            sigma_runtimes=runtimes,
            source_locks=S26QuarantinedHourlySourceLocks(
                hourly_intake_status=SourceRuleStatus.LOCKED,
                session_mapping_status=SourceRuleStatus.LOCKED,
                provider_condition_status=SourceRuleStatus.LOCKED,
                sigma_percent_status=SourceRuleStatus.LOCKED,
                forecast_output_boundary_status=SourceRuleStatus.LOCKED,
                no_diagnostics_status=SourceRuleStatus.LOCKED,
                no_backtests_status=SourceRuleStatus.LOCKED,
                no_positions_status=SourceRuleStatus.LOCKED,
            ),
        )
    )

    forecast_rows = [_forecast_row_dict(row) for row in result.forecast_rows]
    forecast_csv = folders["forecast"] / f"{RUN_ID}_forecast_series_only.csv"
    _write_csv(forecast_csv, forecast_rows)

    status_json = folders["provenance"] / f"{RUN_ID}_status.json"
    provenance_md = folders["provenance"] / f"{RUN_ID}_provenance.md"
    hashes_txt = folders["hashes"] / f"{RUN_ID}_sha256.txt"

    _write_json(
        status_json,
        {
            "gate": GATE,
            "status": "PASS_G_R1E_S26_ZN_EXTENDED_SIGMA_RUNTIME_LEDGER_AND_FORECAST_SERIES_ONLY",
            "series_output_status": result.series_output_status,
            "input_hourly_rows": result.input_hourly_rows,
            "sigma_runtime_rows": len(runtimes),
            "forecast_rows": len(result.forecast_rows),
            "first_forecast_as_of": _z(result.first_forecast_as_of),
            "last_forecast_as_of": _z(result.last_forecast_as_of),
            "daily_source_rows_available_normal": len(daily_rows),
            "daily_source_window_rows_per_runtime": 34,
            "daily_source_returns_per_runtime": 33,
            "diagnostics_run": "NO",
            "backtests_run": "NO",
            "positions_run": "NO",
            "costs_run": "NO",
            "carry_run": "NO",
            "trend_run": "NO",
            "s27_run": "NO",
        },
    )
    provenance_md.write_text(
        "\n".join(
            [
                "# Carver S26 ZN Extended Sigma Runtime And Forecast-Series Provenance",
                "",
                "Status:",
                "",
                "```text",
                "PASS_G_R1E_S26_ZN_EXTENDED_SIGMA_RUNTIME_LEDGER_AND_FORECAST_SERIES_ONLY",
                "```",
                "",
                f"Gate: `{GATE}`",
                "",
                "Inputs:",
                "",
                f"- hourly quarantine CSV: `{HOURLY_CSV.relative_to(ROOT)}`",
                f"- daily provider CSV: `{DAILY_CSV.relative_to(ROOT)}`",
                f"- canonical manifest: `{CANONICAL_MANIFEST.relative_to(ROOT)}`",
                "",
                "Method:",
                "",
                "- one no-lookahead sigma runtime per emitted S26 forecast row;",
                "- latest 34 normal-provider-condition daily ZNM6 rows strictly before the forecast row's completed trading date;",
                "- percentage returns over that 34-row window;",
                "- EWMA(32) variance initialized from the first squared return and recursively updated;",
                "- annualized with multiplier 16;",
                "- S26 forecast fields only.",
                "",
                "Boundary:",
                "",
                "No diagnostics, backtests, returns, PnL, Sharpe, drawdown, positions, orders, fills, costs, carry, trend, S27 overlay, OOS, Lockbox, Forward, deployment, trading, promotion, Git operation, provider API access, or new data download.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    hash_paths = [source_window_csv, runtime_ledger_csv, forecast_csv, status_json, provenance_md]
    hashes_txt.write_text(
        "\n".join(f"{_sha256(path)}  {path.relative_to(ROOT)}" for path in hash_paths) + "\n",
        encoding="utf-8",
    )

    print("PASS_G_R1E_S26_ZN_EXTENDED_SIGMA_RUNTIME_LEDGER_AND_FORECAST_SERIES_ONLY")
    print(f"input_hourly_rows={result.input_hourly_rows}")
    print(f"sigma_runtime_rows={len(runtimes)}")
    print(f"forecast_rows={len(result.forecast_rows)}")
    print(f"artifact_root={OUTPUT_ROOT.relative_to(ROOT)}")


def _load_zn_manifest_row() -> dict[str, str]:
    with CANONICAL_MANIFEST.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row["row_id"] == S26_ZN_WORKED_EXAMPLE_ROW_ID and row["databento_raw_symbol"] == S26_ZN_WORKED_EXAMPLE_DATABENTO_RAW_SYMBOL:
                if row["provider_condition_policy"] != "EXCLUDE_DEGRADED_ROWS_FROM_STRATEGY_FACING_CANDIDATE_SET_KEEP_QUARANTINED_WITH_LABELS":
                    raise SystemExit("Fail closed: unexpected provider condition policy for ZNM6")
                return row
    raise SystemExit("Fail closed: ZNM6 row missing from canonical manifest")


def _load_hourly_bars() -> list[S26QuarantinedHourlyOHLCVBar]:
    bars: list[S26QuarantinedHourlyOHLCVBar] = []
    with HOURLY_CSV.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row["strategy_use_status"] != S26_ZN_HOURLY_QUARANTINE_STATUS:
                raise SystemExit("Fail closed: extended hourly input is not quarantine-only")
            bars.append(
                S26QuarantinedHourlyOHLCVBar(
                    lane_class=LaneClass.SOURCE_NATIVE_FUTURES,
                    strategy_context=row["strategy_context"],
                    provider=S26_ZN_DATABENTO_PROVIDER,
                    dataset=S26_ZN_DATABENTO_DATASET,
                    schema=S26_ZN_DATABENTO_SCHEMA,
                    stype_in=S26_ZN_DATABENTO_STYPE_IN,
                    row_id=S26_ZN_WORKED_EXAMPLE_ROW_ID,
                    author_market_code=S26_ZN_WORKED_EXAMPLE_AUTHOR_MARKET_CODE,
                    instrument_id=S26_ZN_WORKED_EXAMPLE_DATABENTO_INSTRUMENT_ID,
                    raw_symbol=S26_ZN_WORKED_EXAMPLE_DATABENTO_RAW_SYMBOL,
                    provider_ts_event_start_utc=_parse_utc(row["provider_ts_event_start_utc"]),
                    derived_completed_bar_end_utc=_parse_utc(row["derived_completed_bar_end_utc"]),
                    completed_trading_date=row["completed_trading_date"],
                    open=float(row["open"]),
                    high=float(row["high"]),
                    low=float(row["low"]),
                    close=float(row["close"]),
                    volume=float(row["volume"]),
                    provider_condition_status=row["provider_condition_status"],
                    row_shape_status=row["row_shape_status"],
                    source_raw_sha256=row["source_raw_sha256"],
                    strategy_use_status=row["strategy_use_status"],
                )
            )
    if len(bars) != 690:
        raise SystemExit("Fail closed: extended hourly input row count is not 690")
    return bars


def _load_normal_daily_rows(manifest_row: dict[str, str]) -> list[dict[str, Any]]:
    excluded = {item for item in manifest_row["excluded_completed_trading_dates"].split(";") if item}
    rows: list[dict[str, Any]] = []
    with DAILY_CSV.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if int(row["instrument_id"]) != S26_ZN_WORKED_EXAMPLE_DATABENTO_INSTRUMENT_ID:
                raise SystemExit("Fail closed: non-ZN instrument_id in daily source")
            if row["symbol"] != S26_ZN_WORKED_EXAMPLE_DATABENTO_RAW_SYMBOL:
                raise SystemExit("Fail closed: non-ZNM6 symbol in daily source")
            date = _parse_utc(row["ts_event"]).date().isoformat()
            if date in excluded:
                continue
            rows.append(
                {
                    "completed_trading_date": date,
                    "close": float(row["close"]),
                }
            )
    if len(rows) != int(manifest_row["provider_condition_normal_rows"]):
        raise SystemExit("Fail closed: normal daily row count does not match canonical manifest")
    return rows


def _daily_window_before(daily_rows: list[dict[str, Any]], completed_trading_date: str) -> list[dict[str, Any]]:
    eligible = [row for row in daily_rows if row["completed_trading_date"] < completed_trading_date]
    if len(eligible) < 34:
        raise SystemExit(f"Fail closed: insufficient no-lookahead daily rows before {completed_trading_date}")
    return eligible[-34:]


def _short_run_ewma32_sigma_percent(window: list[dict[str, Any]]) -> float:
    closes = [float(row["close"]) for row in window]
    returns = [closes[index] / closes[index - 1] - 1.0 for index in range(1, len(closes))]
    if len(returns) != 33:
        raise SystemExit("Fail closed: EWMA32 source window must produce 33 returns")
    alpha = 2.0 / 33.0
    variance = returns[0] * returns[0]
    for value in returns[1:]:
        variance = (1.0 - alpha) * variance + alpha * value * value
    sigma = math.sqrt(variance) * 16.0
    if not math.isfinite(sigma) or sigma <= 0:
        raise SystemExit("Fail closed: sigma runtime is not finite positive")
    return sigma


def _forecast_row_dict(row: Any) -> dict[str, Any]:
    payload = asdict(row)
    payload["provider_ts_event_start_utc"] = _z(row.provider_ts_event_start_utc)
    payload["derived_completed_bar_end_utc"] = _z(row.derived_completed_bar_end_utc)
    return payload


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise SystemExit(f"Fail closed: no rows to write for {path.name}")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def _write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8")


def _parse_utc(value: str) -> datetime:
    normalized = value.strip().replace(" ", "T").replace("+00:00", "Z")
    timestamp = datetime.fromisoformat(normalized.replace("Z", "+00:00"))
    if timestamp.tzinfo is None:
        raise SystemExit("Fail closed: timestamp is not timezone-aware")
    return timestamp.astimezone(timezone.utc)


def _z(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


if __name__ == "__main__":
    main()
