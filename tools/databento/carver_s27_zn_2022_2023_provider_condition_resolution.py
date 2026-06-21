from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
RUN_ID = "20260531_S27_ZN_2022_2023_PROVIDER_CONDITION_OPTION_C"
SOURCE_RUN_ID = "20260531_S27_ZN_2022_2023_OHLCV_1H_ARCHIVE"
EFFECTIVE_START = "2022-01-04"
EFFECTIVE_END = "2023-12-31"
SOURCE_ROOT = (
    ROOT
    / "docs"
    / "researchops"
    / "s26_s27_backtest_readiness"
    / "ZN_S27_SINGLE_INSTRUMENT"
    / "2022-01-01_2023-12-31"
    / "hourly_archive_quarantine"
)
SOURCE_CSV = SOURCE_ROOT / "sanitized_hourly_bars" / f"{SOURCE_RUN_ID}_sanitized_quarantine_ohlcv_1h.csv"
SOURCE_STATUS = SOURCE_ROOT / "status" / f"{SOURCE_RUN_ID}_quarantine_intake_status.json"
OUTPUT_ROOT = SOURCE_ROOT / "provider_condition_resolution"


def main() -> None:
    _require_existing(SOURCE_CSV)
    _require_existing(SOURCE_STATUS)
    rows = _read_csv(SOURCE_CSV)
    if not rows:
        raise SystemExit("Fail closed: source quarantine CSV is empty")

    output_dirs = {
        "bars": OUTPUT_ROOT / "strategy_facing_hourly_bars",
        "ledger": OUTPUT_ROOT / "exclusion_ledger",
        "status": OUTPUT_ROOT / "status",
        "provenance": OUTPUT_ROOT / "provenance",
        "hashes": OUTPUT_ROOT / "hashes",
    }
    for folder in output_dirs.values():
        folder.mkdir(parents=True, exist_ok=True)

    selected_rows: list[dict[str, Any]] = []
    exclusion_rows: list[dict[str, Any]] = []
    for row in rows:
        date = row["completed_trading_date"]
        condition = row["provider_condition_status"]
        if date < EFFECTIVE_START:
            exclusion_rows.append(_exclusion_row(row, "EXCLUDED_BEFORE_EFFECTIVE_STRATEGY_WINDOW"))
            continue
        if date > EFFECTIVE_END:
            exclusion_rows.append(_exclusion_row(row, "EXCLUDED_AFTER_EFFECTIVE_STRATEGY_WINDOW"))
            continue
        if condition != "PROVIDER_CONDITION_AVAILABLE":
            exclusion_rows.append(_exclusion_row(row, "EXCLUDED_PROVIDER_CONDITION_NOT_AVAILABLE"))
            continue
        strategy_row = dict(row)
        strategy_row["strategy_use_status"] = (
            "STRATEGY_FACING_PROVIDER_CONDITION_AVAILABLE_EFFECTIVE_WINDOW_NOT_BACKTEST_AUTHORIZATION"
        )
        strategy_row["effective_strategy_window_start"] = EFFECTIVE_START
        strategy_row["effective_strategy_window_end"] = EFFECTIVE_END
        selected_rows.append(strategy_row)

    selected_rows.sort(key=lambda row: (row["raw_symbol"], row["provider_ts_event_start_utc"]))
    exclusion_rows.sort(key=lambda row: (row["raw_symbol"], row["provider_ts_event_start_utc"]))
    blocked_selected = [
        row for row in selected_rows if row["provider_condition_status"] != "PROVIDER_CONDITION_AVAILABLE"
    ]
    if blocked_selected:
        raise SystemExit(f"Fail closed: selected rows include {len(blocked_selected)} non-available provider rows")

    selected_csv = output_dirs["bars"] / f"{RUN_ID}_strategy_facing_available_ohlcv_1h.csv"
    exclusion_csv = output_dirs["ledger"] / f"{RUN_ID}_exclusion_ledger.csv"
    status_json = output_dirs["status"] / f"{RUN_ID}_status.json"
    provenance_json = output_dirs["provenance"] / f"{RUN_ID}_provenance.json"
    hashes_json = output_dirs["hashes"] / f"{RUN_ID}_sha256.json"

    _write_csv(selected_csv, selected_rows)
    _write_csv(exclusion_csv, exclusion_rows)
    status = _status_payload(rows, selected_rows, exclusion_rows, selected_csv, exclusion_csv)
    _write_json(status_json, status)
    _write_json(provenance_json, _provenance_payload(selected_csv, exclusion_csv, status_json))
    _write_json(
        hashes_json,
        {
            str(path.relative_to(ROOT)): _sha256(path)
            for path in (SOURCE_CSV, SOURCE_STATUS, selected_csv, exclusion_csv, status_json, provenance_json)
        },
    )

    print(status["status"])
    print(f"source_rows={len(rows)}")
    print(f"strategy_facing_rows={len(selected_rows)}")
    print(f"excluded_rows={len(exclusion_rows)}")


def _status_payload(
    source_rows: list[dict[str, Any]],
    selected_rows: list[dict[str, Any]],
    exclusion_rows: list[dict[str, Any]],
    selected_csv: Path,
    exclusion_csv: Path,
) -> dict[str, Any]:
    source_condition_counts = Counter(row["provider_condition_status"] for row in source_rows)
    selected_condition_counts = Counter(row["provider_condition_status"] for row in selected_rows)
    exclusion_reason_counts = Counter(row["exclusion_reason"] for row in exclusion_rows)
    excluded_dates = sorted({row["completed_trading_date"] for row in exclusion_rows})
    degraded_rows = [
        row for row in exclusion_rows if row["provider_condition_status"] == "PROVIDER_CONDITION_DEGRADED"
    ]
    return {
        "gate": "S27_ZN_PROVIDER_CONDITION_BLOCKER_RESOLUTION_OPTION_C",
        "status": "PASS_OPTION_C_EFFECTIVE_WINDOW_PROVIDER_CONDITION_AVAILABLE_NOT_BACKTEST_AUTHORIZATION",
        "source_archive_window_start": "2022-01-01",
        "source_archive_window_end": "2023-12-31",
        "effective_strategy_window_start": EFFECTIVE_START,
        "effective_strategy_window_end": EFFECTIVE_END,
        "source_quarantine_rows": len(source_rows),
        "strategy_facing_rows": len(selected_rows),
        "excluded_rows": len(exclusion_rows),
        "source_provider_condition_status_counts": dict(sorted(source_condition_counts.items())),
        "strategy_facing_provider_condition_status_counts": dict(sorted(selected_condition_counts.items())),
        "exclusion_reason_counts": dict(sorted(exclusion_reason_counts.items())),
        "excluded_completed_trading_dates": excluded_dates,
        "degraded_provider_condition_rows_excluded": len(degraded_rows),
        "degraded_provider_condition_completed_trading_dates": sorted(
            {row["completed_trading_date"] for row in degraded_rows}
        ),
        "selected_csv": str(selected_csv.relative_to(ROOT)),
        "exclusion_ledger_csv": str(exclusion_csv.relative_to(ROOT)),
        "policy": "OPTION_C_REDUCE_BACKTEST_START_AFTER_PROVIDER_CONDITION_BLOCKER",
        "zero_silent_row_skip": "PASS_EXCLUSIONS_EXPLICITLY_LEDGERED",
        "provider_api_access": "NO",
        "new_data_download": "NO",
        "diagnostics_run": "NO",
        "backtests_run": "NO",
        "forecasts_run": "NO",
        "positions_run": "NO",
        "costs_run": "NO",
        "oos_access": "NO",
        "lockbox_access": "NO",
        "forward_access": "NO",
        "promotion": "NO",
        "next_required_gate": "S27_ZN_2022_2023_DEV_RECON_BACKTEST_EXECUTION_GATE_RETARGETED_EFFECTIVE_WINDOW",
    }


def _provenance_payload(selected_csv: Path, exclusion_csv: Path, status_json: Path) -> dict[str, Any]:
    return {
        "gate": "S27_ZN_PROVIDER_CONDITION_BLOCKER_RESOLUTION_OPTION_C",
        "created_at_utc": _z(datetime.now(timezone.utc)),
        "source_csv": str(SOURCE_CSV.relative_to(ROOT)),
        "source_status": str(SOURCE_STATUS.relative_to(ROOT)),
        "selected_csv": str(selected_csv.relative_to(ROOT)),
        "exclusion_ledger_csv": str(exclusion_csv.relative_to(ROOT)),
        "status_json": str(status_json.relative_to(ROOT)),
        "decision": "Retain the full quarantine archive but set strategy-facing effective window to 2022-01-04 through 2023-12-31.",
        "degraded_row_policy": "Provider-condition degraded rows remain preserved in quarantine and excluded from the strategy-facing layer.",
        "non_authorization": [
            "NO_PROVIDER_API_ACCESS",
            "NO_NEW_DATA_DOWNLOAD",
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


def _exclusion_row(row: dict[str, Any], reason: str) -> dict[str, Any]:
    return {
        "lane_class": row["lane_class"],
        "strategy_context": row["strategy_context"],
        "provider": row["provider"],
        "dataset": row["dataset"],
        "schema": row["schema"],
        "row_id": row["row_id"],
        "author_market_code": row["author_market_code"],
        "raw_symbol": row["raw_symbol"],
        "instrument_id": row["instrument_id"],
        "provider_ts_event_start_utc": row["provider_ts_event_start_utc"],
        "derived_completed_bar_end_utc": row["derived_completed_bar_end_utc"],
        "completed_trading_date": row["completed_trading_date"],
        "provider_condition_status": row["provider_condition_status"],
        "source_strategy_use_status": row["strategy_use_status"],
        "exclusion_reason": reason,
        "effective_strategy_window_start": EFFECTIVE_START,
        "effective_strategy_window_end": EFFECTIVE_END,
        "strategy_use_status": "EXCLUDED_FROM_STRATEGY_FACING_LAYER_NOT_SILENT_NOT_BACKTEST_AUTHORIZATION",
    }


def _read_csv(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def _require_existing(path: Path) -> None:
    if not path.exists():
        raise SystemExit(f"Fail closed: missing required input {path}")


def _z(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    main()
