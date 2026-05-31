from __future__ import annotations

import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
RUN_ID = "20260531_ZN_S27_EWMAC16_TREND_RUNTIME_LEDGER"
S26_FORECAST_CSV = (
    ROOT
    / "docs"
    / "researchops"
    / "s26_s27_hourly_bridge"
    / "ZN_S26_WORKED_EXAMPLE"
    / "2026-04-13_2026-05-22"
    / "forecast_series_only_output"
    / "2026-05-31"
    / "forecast_rows"
    / "20260531_G_R1E_ZN_S26_EXTENDED_SIGMA_AND_FORECAST_SERIES_forecast_series_only.csv"
)
CONTINUOUS_DAILY_CSV = (
    ROOT
    / "docs"
    / "researchops"
    / "s26_s27_hourly_bridge"
    / "ZN_S27_EWMAC16_TREND_DEPENDENCY"
    / "local_continuous_daily_lineage_2026-05-31"
    / "ledger"
    / "20260531_ZN_S27_EWMAC16_LOCAL_CONTINUOUS_DAILY_LIFECYCLE_REPAIR_series_dev_recon_only.csv"
)
OUTPUT_ROOT = (
    ROOT
    / "docs"
    / "researchops"
    / "s26_s27_hourly_bridge"
    / "ZN_S27_EWMAC16_TREND_DEPENDENCY"
    / "ewmac16_trend_runtime_ledger_2026-05-31"
)

FAST_SPAN = 16
SLOW_SPAN = 64
RUNTIME_STATUS = "PREVALIDATED_S27_EWMAC16_TREND_RUNTIME_VALUE"
METHOD_STATUS = "LOCKED_EWMAC16_TREND_OVERLAY_RUNTIME"


def main() -> None:
    folders = {
        "runtime_rows": OUTPUT_ROOT / "runtime_rows",
        "status": OUTPUT_ROOT / "status",
        "provenance": OUTPUT_ROOT / "provenance",
        "hashes": OUTPUT_ROOT / "hashes",
    }
    for folder in folders.values():
        folder.mkdir(parents=True, exist_ok=True)

    s26_rows = _read_rows(S26_FORECAST_CSV)
    daily_rows = _read_rows(CONTINUOUS_DAILY_CSV)
    s26_sha = _sha256(S26_FORECAST_CSV)
    continuous_sha = _sha256(CONTINUOUS_DAILY_CSV)
    daily_by_date = {row["continuous_row_date"]: float(row["adjusted_close"]) for row in daily_rows}
    sorted_dates = sorted(daily_by_date)

    runtime_rows: list[dict[str, str]] = []
    for row in s26_rows:
        completed_date = row["completed_trading_date"]
        eligible_dates = [date for date in sorted_dates if date < completed_date]
        if len(eligible_dates) < SLOW_SPAN:
            raise SystemExit(f"Fail closed: fewer than {SLOW_SPAN} no-lookahead daily rows before {completed_date}")
        values = tuple(daily_by_date[date] for date in eligible_dates)
        fast = _ewma(values, FAST_SPAN)
        slow = _ewma(values, SLOW_SPAN)
        runtime_rows.append(
            {
                "row_id": row["row_id"],
                "author_market_code": row["author_market_code"],
                "instrument_id": row["instrument_id"],
                "raw_symbol": row["raw_symbol"],
                "as_of": row["derived_completed_bar_end_utc"],
                "completed_trading_date": completed_date,
                "trend_fast_ewma": f"{fast:.12f}",
                "trend_slow_ewma": f"{slow:.12f}",
                "trend_forecast": f"{fast - slow:.12f}",
                "runtime_status": RUNTIME_STATUS,
                "method_status": METHOD_STATUS,
                "no_lookahead_status": "PASS_NO_LOOKAHEAD",
                "no_lookahead_policy": "DAILY_ROWS_STRICTLY_BEFORE_FORECAST_COMPLETED_TRADING_DATE",
                "source_artifact_sha256": continuous_sha,
                "s26_source_artifact_sha256": s26_sha,
                "daily_rows_used": str(len(eligible_dates)),
                "first_daily_row_used": eligible_dates[0],
                "last_daily_row_used": eligible_dates[-1],
                "trend_runtime_output_boundary": "RUNTIME_LEDGER_ONLY_NOT_S27_NOT_DIAGNOSTIC_NOT_BACKTEST",
            }
        )

    _assert_runtime_alignment(s26_rows, runtime_rows)

    runtime_csv = folders["runtime_rows"] / f"{RUN_ID}_runtime_rows.csv"
    status_json = folders["status"] / f"{RUN_ID}_status.json"
    provenance_json = folders["provenance"] / f"{RUN_ID}_provenance.json"
    hashes_json = folders["hashes"] / f"{RUN_ID}_sha256.json"

    _write_csv(runtime_csv, runtime_rows)
    _write_json(
        status_json,
        {
            "run_id": RUN_ID,
            "status": "PASS_S27_EWMAC16_TREND_RUNTIME_LEDGER_REAL_ZN_DEV_RECON_ONLY",
            "runtime_rows": len(runtime_rows),
            "s26_forecast_rows": len(s26_rows),
            "continuous_daily_rows": len(daily_rows),
            "fast_span_days": FAST_SPAN,
            "slow_span_days": SLOW_SPAN,
            "no_lookahead_policy": "Use only local continuous daily rows with continuous_row_date strictly before the S26 hourly row completed_trading_date.",
            "trend_computed": "YES_EWMAC16_RUNTIME_ONLY",
            "s27_computed": "NO",
            "diagnostics_run": "NO",
            "backtests_run": "NO",
            "positions_run": "NO",
            "strategy_test_run": "NO",
        },
    )
    _write_json(
        provenance_json,
        {
            "run_id": RUN_ID,
            "created_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "lane_class": "SOURCE_NATIVE_FUTURES",
            "s26_forecast_csv": str(S26_FORECAST_CSV.relative_to(ROOT)),
            "s26_forecast_sha256": s26_sha,
            "continuous_daily_csv": str(CONTINUOUS_DAILY_CSV.relative_to(ROOT)),
            "continuous_daily_sha256": continuous_sha,
            "source_method": "EWMAC(16,64) over local back-adjusted ZN daily close lineage for S27 trend overlay runtime only.",
            "boundary": [
                "NO_PROVIDER_API_ACCESS",
                "NO_NEW_DATA_DOWNLOAD",
                "NO_MARKET_ROW_EXPANSION",
                "NO_S27_FORECAST_COMPUTATION",
                "NO_DIAGNOSTICS",
                "NO_BACKTESTS",
                "NO_POSITIONS",
                "NO_COSTS",
                "NO_CARRY",
                "NO_TRADING",
                "NO_PROMOTION",
            ],
        },
    )
    hashes = {
        str(path.relative_to(ROOT)): _sha256(path)
        for path in (
            runtime_csv,
            status_json,
            provenance_json,
        )
    }
    _write_json(hashes_json, hashes)

    print("PASS_S27_EWMAC16_TREND_RUNTIME_LEDGER_REAL_ZN_DEV_RECON_ONLY")
    print(f"runtime_rows={len(runtime_rows)}")
    print(f"artifact_root={OUTPUT_ROOT.relative_to(ROOT)}")


def _assert_runtime_alignment(s26_rows: list[dict[str, str]], runtime_rows: list[dict[str, str]]) -> None:
    if len(s26_rows) != len(runtime_rows):
        raise SystemExit("Fail closed: S27 trend runtime row count differs from S26 forecast rows")
    seen: set[str] = set()
    for s26, runtime in zip(s26_rows, runtime_rows):
        if runtime["as_of"] in seen:
            raise SystemExit("Fail closed: duplicate trend runtime as_of")
        seen.add(runtime["as_of"])
        for key in ("row_id", "author_market_code", "instrument_id", "raw_symbol"):
            if runtime[key] != s26[key]:
                raise SystemExit(f"Fail closed: S27 trend runtime identity mismatch on {key}")
        if runtime["as_of"] != s26["derived_completed_bar_end_utc"]:
            raise SystemExit("Fail closed: S27 trend runtime timestamp does not match S26 forecast row")


def _ewma(values: tuple[float, ...], span: int) -> float:
    alpha = 2.0 / (span + 1.0)
    smoothed = values[0]
    for value in values[1:]:
        smoothed = alpha * value + (1.0 - alpha) * smoothed
    return smoothed


def _read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        raise SystemExit(f"Fail closed: no rows for {path.name}")
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


if __name__ == "__main__":
    main()
