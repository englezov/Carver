from __future__ import annotations

import csv
import hashlib
import json
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
    S26QuarantinedHourlyForecastResult,
    S26QuarantinedHourlyForecastSeriesResult,
    S27RealHourlySourceLocks,
    S27QuarantinedHourlyForecastSeriesRequest,
    S27TrendOverlayRuntimeValue,
    S27VolAttenuationRuntimeValue,
    s27_forecast_series_only_from_s26_forecast_series,
)


RUN_ID = "20260531_ZN_S27_FORECAST_SERIES_ONLY"
GATE = "S27_ZN_REAL_HOURLY_FORECAST_SERIES_ONLY_EXECUTION_NOT_TEST"
S26_FORECAST_CSV = (
    ROOT
    / "docs/researchops/s26_s27_hourly_bridge/ZN_S26_WORKED_EXAMPLE/2026-04-13_2026-05-22/"
    / "forecast_series_only_output/2026-05-31/forecast_rows/"
    / "20260531_G_R1E_ZN_S26_EXTENDED_SIGMA_AND_FORECAST_SERIES_forecast_series_only.csv"
)
TREND_RUNTIME_CSV = (
    ROOT
    / "docs/researchops/s26_s27_hourly_bridge/ZN_S27_EWMAC16_TREND_DEPENDENCY/"
    / "ewmac16_trend_runtime_ledger_2026-05-31/runtime_rows/"
    / "20260531_ZN_S27_EWMAC16_TREND_RUNTIME_LEDGER_runtime_rows.csv"
)
VQM_RUNTIME_CSV = (
    ROOT
    / "docs/researchops/s26_s27_hourly_bridge/ZN_S27_V_Q_M_VOL_ATTENUATION/"
    / "ten_year_vol_history_runtime_2026-05-31/runtime_rows/"
    / "20260531_ZN_S27_V_Q_M_TEN_YEAR_VOL_RUNTIME_runtime_rows.csv"
)
OUTPUT_ROOT = (
    ROOT
    / "docs/researchops/s26_s27_hourly_bridge/ZN_S27_FORECAST_SERIES_ONLY/2026-05-31"
)


def main() -> None:
    folders = {
        "forecast": OUTPUT_ROOT / "forecast_rows",
        "status": OUTPUT_ROOT / "status",
        "provenance": OUTPUT_ROOT / "provenance",
        "hashes": OUTPUT_ROOT / "hashes",
    }
    for folder in folders.values():
        folder.mkdir(parents=True, exist_ok=True)

    s26_rows = tuple(_read_s26_forecast_rows())
    trend_runtimes = tuple(_read_trend_runtimes())
    vol_runtimes = tuple(_read_vol_runtimes())
    s26_series = S26QuarantinedHourlyForecastSeriesResult(
        row_id=s26_rows[0].row_id,
        author_market_code=s26_rows[0].author_market_code,
        instrument_id=s26_rows[0].instrument_id,
        raw_symbol=s26_rows[0].raw_symbol,
        first_forecast_as_of=s26_rows[0].derived_completed_bar_end_utc,
        last_forecast_as_of=s26_rows[-1].derived_completed_bar_end_utc,
        input_hourly_rows=len(s26_rows) + 4,
        forecast_rows=s26_rows,
    )
    result = s27_forecast_series_only_from_s26_forecast_series(
        request=S27QuarantinedHourlyForecastSeriesRequest(
            s26_forecast_series=s26_series,
            trend_runtimes=trend_runtimes,
            vol_runtimes=vol_runtimes,
            source_locks=S27RealHourlySourceLocks(
                s26_forecast_row_status=SourceRuleStatus.LOCKED,
                trend_overlay_runtime_status=SourceRuleStatus.LOCKED,
                vol_attenuation_runtime_status=SourceRuleStatus.LOCKED,
                inherited_scalar_cap_status=SourceRuleStatus.LOCKED,
                no_fdm_status=SourceRuleStatus.LOCKED,
                no_buffering_status=SourceRuleStatus.LOCKED,
                output_boundary_status=SourceRuleStatus.LOCKED,
            ),
            lane_class=LaneClass.SOURCE_NATIVE_FUTURES,
        )
    )

    forecast_csv = folders["forecast"] / f"{RUN_ID}_forecast_series_only.csv"
    status_json = folders["status"] / f"{RUN_ID}_status.json"
    provenance_md = folders["provenance"] / f"{RUN_ID}_provenance.md"
    hashes_json = folders["hashes"] / f"{RUN_ID}_sha256.json"

    forecast_rows = [_forecast_row_dict(row) for row in result.forecast_rows]
    _write_csv(forecast_csv, forecast_rows)
    _write_json(
        status_json,
        {
            "gate": GATE,
            "status": "PASS_S27_ZN_REAL_HOURLY_FORECAST_SERIES_ONLY_NOT_TEST",
            "series_output_status": result.series_output_status,
            "input_s26_forecast_rows": result.input_s26_forecast_rows,
            "trend_runtime_rows": len(trend_runtimes),
            "vqm_runtime_rows": len(vol_runtimes),
            "forecast_rows": len(result.forecast_rows),
            "first_forecast_as_of": _z(result.first_forecast_as_of),
            "last_forecast_as_of": _z(result.last_forecast_as_of),
            "diagnostics_run": "NO",
            "backtests_run": "NO",
            "positions_run": "NO",
            "costs_run": "NO",
            "carry_run": "NO",
            "strategy_test_run": "NO",
        },
    )
    provenance_md.write_text(_provenance_text(result.input_s26_forecast_rows), encoding="utf-8")
    _write_json(
        hashes_json,
        {
            str(path.relative_to(ROOT)): _sha256(path)
            for path in (forecast_csv, status_json, provenance_md)
        },
    )
    print("PASS_S27_ZN_REAL_HOURLY_FORECAST_SERIES_ONLY_NOT_TEST")
    print(f"forecast_rows={len(result.forecast_rows)}")
    print(f"artifact_root={OUTPUT_ROOT.relative_to(ROOT)}")


def _read_s26_forecast_rows() -> list[S26QuarantinedHourlyForecastResult]:
    rows = []
    with S26_FORECAST_CSV.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            rows.append(
                S26QuarantinedHourlyForecastResult(
                    row_id=row["row_id"],
                    author_market_code=row["author_market_code"],
                    instrument_id=int(row["instrument_id"]),
                    raw_symbol=row["raw_symbol"],
                    provider_ts_event_start_utc=_parse_utc(row["provider_ts_event_start_utc"]),
                    derived_completed_bar_end_utc=_parse_utc(row["derived_completed_bar_end_utc"]),
                    completed_trading_date=row["completed_trading_date"],
                    price_close=float(row["price_close"]),
                    equilibrium_ewma_5=float(row["equilibrium_ewma_5"]),
                    raw_forecast=float(row["raw_forecast"]),
                    sigma_percent=float(row["sigma_percent"]),
                    sigma_price=float(row["sigma_price"]),
                    risk_adjusted_forecast=float(row["risk_adjusted_forecast"]),
                    forecast_scalar=float(row["forecast_scalar"]),
                    scaled_forecast=float(row["scaled_forecast"]),
                    capped_forecast=float(row["capped_forecast"]),
                    source_locks_status=row["source_locks_status"],
                )
            )
    if len(rows) != 686:
        raise SystemExit("Fail closed: S26 forecast input row count is not 686")
    return rows


def _read_trend_runtimes() -> list[S27TrendOverlayRuntimeValue]:
    rows = []
    with TREND_RUNTIME_CSV.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            rows.append(
                S27TrendOverlayRuntimeValue(
                    row_id=row["row_id"],
                    author_market_code=row["author_market_code"],
                    instrument_id=int(row["instrument_id"]),
                    raw_symbol=row["raw_symbol"],
                    as_of=_parse_utc(row["as_of"]),
                    trend_fast_ewma=float(row["trend_fast_ewma"]),
                    trend_slow_ewma=float(row["trend_slow_ewma"]),
                    trend_forecast=float(row["trend_forecast"]),
                    runtime_status=row["runtime_status"],
                    method_status=row["method_status"],
                    no_lookahead_status=row["no_lookahead_status"],
                    source_artifact_sha256=row["source_artifact_sha256"],
                )
            )
    if len(rows) != 686:
        raise SystemExit("Fail closed: S27 trend runtime row count is not 686")
    return rows


def _read_vol_runtimes() -> list[S27VolAttenuationRuntimeValue]:
    rows = []
    with VQM_RUNTIME_CSV.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            rows.append(
                S27VolAttenuationRuntimeValue(
                    row_id=row["row_id"],
                    author_market_code=row["author_market_code"],
                    instrument_id=int(row["instrument_id"]),
                    raw_symbol=row["raw_symbol"],
                    as_of=_parse_utc(row["as_of"]),
                    vol_multiplier=float(row["vol_multiplier"]),
                    runtime_status=row["runtime_status"],
                    method_status=row["method_status"],
                    no_lookahead_status=row["no_lookahead_status"],
                    source_artifact_sha256=row["source_artifact_sha256"],
                )
            )
    if len(rows) != 686:
        raise SystemExit("Fail closed: S27 V/Q/M runtime row count is not 686")
    return rows


def _forecast_row_dict(row: Any) -> dict[str, Any]:
    payload = asdict(row)
    payload["as_of"] = _z(row.as_of)
    return payload


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise SystemExit(f"Fail closed: no rows for {path.name}")
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


def _provenance_text(row_count: int) -> str:
    return "\n".join(
        [
            "# Carver S27 ZN Forecast-Series-Only Provenance",
            "",
            "Status:",
            "",
            "```text",
            "PASS_S27_ZN_REAL_HOURLY_FORECAST_SERIES_ONLY_NOT_TEST",
            "```",
            "",
            f"Gate: `{GATE}`",
            "",
            "Inputs:",
            "",
            f"- S26 forecast-series-only rows: `{S26_FORECAST_CSV.relative_to(ROOT)}`",
            f"- S27 EWMAC16 trend runtime rows: `{TREND_RUNTIME_CSV.relative_to(ROOT)}`",
            f"- S27 V/Q/M volatility runtime rows: `{VQM_RUNTIME_CSV.relative_to(ROOT)}`",
            "",
            f"Rows: `{row_count}`",
            "",
            "Boundary:",
            "",
            "Forecast-series-only artifact. No diagnostics, backtests, returns/PnL metrics, positions, orders, fills, costs, carry, strategy test, OOS, Lockbox, Forward, deployment, trading, promotion, Git, or remote repository operations.",
            "",
        ]
    )


if __name__ == "__main__":
    main()
