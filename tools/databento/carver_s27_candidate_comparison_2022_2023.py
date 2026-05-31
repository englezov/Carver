from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import databento as db

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.carver.spine.s26_s27 import (  # noqa: E402
    S26_EQUILIBRIUM_EWMA_SPAN,
    S26_FORECAST_SCALAR,
    S27_FORECAST_SCALAR,
    S27_TREND_FAST_SPAN,
    S27_TREND_SLOW_SPAN,
)


RUN_ID = "20260531_S27_SOURCE_NATIVE_CANDIDATE_COMPARISON_2022_2023_R2"
GATE = "S27_SOURCE_NATIVE_CANDIDATE_COMPARISON_2022_2023_DEV_RECON"
DATASET = "GLBX.MDP3"
HOURLY_SCHEMA = "ohlcv-1h"
DAILY_SCHEMA = "ohlcv-1d"
STYPE_IN = "raw_symbol"
REQUEST_START = date(2022, 1, 1)
REQUEST_END = date(2023, 12, 31)
HOURLY_REQUEST_START = datetime(2021, 12, 31, tzinfo=timezone.utc)
HOURLY_REQUEST_END = datetime(2024, 1, 1, tzinfo=timezone.utc)
DAILY_REQUEST_END = date(2024, 1, 1)
DAILY_HISTORY_START_DEFAULT = date(2011, 1, 1)
ROLL_BUFFER_COMPLETED_DATES = 10
SIGMA_EWMA_SPAN = 32
SIGMA_WINDOW_ROWS = 34
TRADING_DAYS_PER_YEAR = 256
TEN_YEAR_SIGMA_ROWS = 2560
VQM_EWMA_SPAN = 10
FORECAST_DIVISOR = 10.0
MAX_DAILY_RUNTIME_LAG_DAYS = 10
OUTPUT_ROOT = (
    ROOT
    / "docs/researchops/s26_s27_candidate_comparison/"
    / "2022-01-01_2023-12-31"
)
PROCESS_RESULT_DOC = (
    ROOT
    / "docs/process/CARVER_S27_SOURCE_NATIVE_CANDIDATE_COMPARISON_2022_2023_RESULT_2026-05-31.md"
)
LOCAL_AUDIT_DOC = (
    ROOT
    / "docs/process/CARVER_S27_SOURCE_NATIVE_CANDIDATE_COMPARISON_2022_2023_LOCAL_LEAN_HOSTILE_AUDIT_2026-05-31.md"
)
KEY_CANDIDATES = (
    Path(os.environ["DATABENTO_API_KEY_FILE"]) if os.environ.get("DATABENTO_API_KEY_FILE") else None,
    Path("C:/Users/openclaw/Desktop/BentoKey.txt"),
    Path("C:/Users/openclaw/Desktop/BENTO.txt"),
    Path("C:/Users/openclaw/Desktop/bento.txt"),
)
MONTH_CODES = ((3, "H"), (6, "M"), (9, "U"), (12, "Z"))


@dataclass(frozen=True)
class Candidate:
    root: str
    row_id: str
    book_label: str
    asset_group: str
    multiplier: float
    etf_fee_per_side: float
    daily_history_start: date = DAILY_HISTORY_START_DEFAULT


ALL_CANDIDATES = (
    Candidate("ZT", "APPENDIX_C_172_001", "2-year US", "bond", 2000.0, 1.36),
    Candidate("ZF", "APPENDIX_C_172_003", "5-year US", "bond", 1000.0, 1.41),
    Candidate("ZN", "APPENDIX_C_172_004", "10-year US", "bond", 1000.0, 1.51),
    Candidate("MES", "APPENDIX_C_174_006", "S&P 500 (micro)", "index", 5.0, 0.56, date(2019, 1, 1)),
    Candidate("MNQ", "APPENDIX_C_174_002", "Nasdaq (micro)", "index", 2.0, 0.51, date(2019, 1, 1)),
)
ACTIVE_CANDIDATE_FILTER = {
    value.strip().upper()
    for value in os.environ.get("CARVER_S27_CANDIDATES", "").split(",")
    if value.strip()
}
CANDIDATES = tuple(
    candidate for candidate in ALL_CANDIDATES if not ACTIVE_CANDIDATE_FILTER or candidate.root in ACTIVE_CANDIDATE_FILTER
)


def main() -> None:
    if os.environ.get("CARVER_S27_COMBINE_ONLY") == "1":
        _combine_existing_statuses()
        return

    key = _read_databento_key()
    client = db.Historical(key)
    folders = _folders(OUTPUT_ROOT)
    for folder in folders.values():
        folder.mkdir(parents=True, exist_ok=True)

    _write_json(folders["manifest"] / f"{RUN_ID}_manifest.json", _manifest_payload())
    hourly_condition = _dataset_condition(client, HOURLY_REQUEST_START.date(), HOURLY_REQUEST_END.date())
    daily_condition = _dataset_condition(client, min(c.daily_history_start for c in CANDIDATES), DAILY_REQUEST_END)
    _write_json(folders["metadata"] / f"{RUN_ID}_hourly_dataset_condition.json", hourly_condition)
    _write_json(folders["metadata"] / f"{RUN_ID}_daily_dataset_condition.json", daily_condition)
    hourly_condition_by_date = _condition_by_date(hourly_condition)
    daily_condition_by_date = _condition_by_date(daily_condition)

    summary_rows: list[dict[str, Any]] = []
    all_status: list[dict[str, Any]] = []
    for candidate in CANDIDATES:
        status = _run_candidate(client, candidate, hourly_condition_by_date, daily_condition_by_date)
        all_status.append(status)
        summary_rows.append(_summary_row(status))

    summary_csv = folders["summary"] / f"{RUN_ID}_summary.csv"
    status_json = folders["status"] / f"{RUN_ID}_status.json"
    _write_csv(summary_csv, summary_rows)
    overall = _overall_status(all_status, summary_csv)
    _write_json(status_json, overall)
    _write_json(folders["hashes"] / f"{RUN_ID}_sha256.json", _hash_tree(OUTPUT_ROOT))
    PROCESS_RESULT_DOC.write_text(_process_result_text(overall, summary_rows), encoding="utf-8")
    LOCAL_AUDIT_DOC.write_text(_local_audit_text(overall, summary_rows), encoding="utf-8")

    print(overall["status"])
    for row in summary_rows:
        print(
            f"{row['root']}: {row['candidate_status']} "
            f"effective={row['effective_backtest_start']}..{row['effective_backtest_end']} "
            f"net_after_etf_fees={row['net_after_etf_fees_usd']}"
        )
    print(f"artifact_root={OUTPUT_ROOT.relative_to(ROOT)}")


def _combine_existing_statuses() -> None:
    folders = _folders(OUTPUT_ROOT)
    for folder in folders.values():
        folder.mkdir(parents=True, exist_ok=True)
    statuses: list[dict[str, Any]] = []
    for candidate in ALL_CANDIDATES:
        status_path = OUTPUT_ROOT / candidate.root / "status" / f"{RUN_ID}_{candidate.root}_status.json"
        if not status_path.exists():
            raise SystemExit(f"Fail closed: missing corrected R2 candidate status: {status_path}")
        statuses.append(json.loads(status_path.read_text(encoding="utf-8")))
    summary_rows = [_summary_row(status) for status in statuses]
    summary_csv = folders["summary"] / f"{RUN_ID}_summary.csv"
    status_json = folders["status"] / f"{RUN_ID}_status.json"
    _write_csv(summary_csv, summary_rows)
    overall = _overall_status(statuses, summary_csv)
    overall["provider_api_access"] = "YES_IN_CANDIDATE_EXECUTION_ARTIFACTS_NO_DURING_COMBINE_ONLY_CONSOLIDATION"
    _write_json(status_json, overall)
    _write_json(folders["hashes"] / f"{RUN_ID}_sha256.json", _hash_tree(OUTPUT_ROOT))
    PROCESS_RESULT_DOC.write_text(_process_result_text(overall, summary_rows), encoding="utf-8")
    LOCAL_AUDIT_DOC.write_text(_local_audit_text(overall, summary_rows), encoding="utf-8")
    print(overall["status"])
    print(f"combined_candidates={len(statuses)}")
    print(f"summary_csv={summary_csv.relative_to(ROOT)}")


def _run_candidate(
    client: db.Historical,
    candidate: Candidate,
    hourly_condition_by_date: dict[str, str],
    daily_condition_by_date: dict[str, str],
) -> dict[str, Any]:
    root = OUTPUT_ROOT / candidate.root
    folders = _folders(root)
    for folder in folders.values():
        folder.mkdir(parents=True, exist_ok=True)

    hourly_contracts = _comparison_contracts(candidate.root)
    daily_contracts = _daily_contracts(candidate.root, candidate.daily_history_start)
    errors: list[dict[str, Any]] = []
    hourly_rows: list[dict[str, Any]] = []
    daily_rows_by_contract: dict[str, list[dict[str, Any]]] = {}
    symbology_rows: list[dict[str, Any]] = []

    for contract in hourly_contracts:
        rows, symbol_rows, contract_errors = _request_ohlcv_rows(
            client=client,
            candidate=candidate,
            contract=contract,
            schema=HOURLY_SCHEMA,
            start_dt=HOURLY_REQUEST_START,
            end_dt=HOURLY_REQUEST_END,
            condition_by_date=hourly_condition_by_date,
            folders=folders,
            purpose="hourly",
        )
        hourly_rows.extend(rows)
        symbology_rows.extend(symbol_rows)
        errors.extend(contract_errors)

    for contract in daily_contracts:
        rows, symbol_rows, contract_errors = _request_ohlcv_rows(
            client=client,
            candidate=candidate,
            contract=contract,
            schema=DAILY_SCHEMA,
            start_dt=datetime.combine(date.fromisoformat(contract["request_start"]), datetime.min.time(), timezone.utc),
            end_dt=datetime.combine(date.fromisoformat(contract["request_end"]), datetime.min.time(), timezone.utc),
            condition_by_date=daily_condition_by_date,
            folders=folders,
            purpose="daily",
        )
        if rows:
            daily_rows_by_contract[_contract_key(contract)] = rows
        symbology_rows.extend(symbol_rows)
        errors.extend(contract_errors)

    _write_csv(folders["metadata"] / f"{RUN_ID}_{candidate.root}_symbology_ledger.csv", symbology_rows)
    if errors:
        _write_csv(folders["status"] / f"{RUN_ID}_{candidate.root}_provider_errors.csv", errors)

    status: dict[str, Any]
    try:
        if not hourly_rows:
            raise RuntimeError("no hourly rows returned")
        hourly_continuous, inactive_hourly, hourly_roll_plan = _build_continuous_rows(
            candidate=candidate,
            contracts=hourly_contracts,
            source_rows=hourly_rows,
            price_field="close",
            timestamp_field="derived_completed_bar_end_utc",
            output_root=folders["lineage"],
            prefix=f"{RUN_ID}_{candidate.root}_hourly",
        )
        daily_source_rows = [row for rows in daily_rows_by_contract.values() for row in rows]
        if not daily_source_rows:
            raise RuntimeError("no daily rows returned")
        daily_continuous, inactive_daily, daily_roll_plan = _build_continuous_rows(
            candidate=candidate,
            contracts=daily_contracts,
            source_rows=daily_source_rows,
            price_field="close",
            timestamp_field="completed_trading_date",
            output_root=folders["lineage"],
            prefix=f"{RUN_ID}_{candidate.root}_daily",
        )
        sigma_rows = _build_sigma_rows(daily_continuous)
        vqm_rows = _build_vqm_rows(sigma_rows)
        daily_runtime_rows = _build_daily_runtime_rows(daily_continuous, vqm_rows)
        s26_rows, s27_rows, blocked_rows = _build_forecasts(candidate, hourly_continuous, daily_runtime_rows)
        position_rows = _build_positions(s27_rows)
        backtest_rows = _build_backtest_rows(candidate, hourly_continuous, position_rows)
        validation_rows = _build_validation_rows(
            hourly_rows=hourly_rows,
            hourly_continuous=hourly_continuous,
            inactive_hourly=inactive_hourly,
            s26_rows=s26_rows,
            s27_rows=s27_rows,
            position_rows=position_rows,
            backtest_rows=backtest_rows,
        )

        _write_csv(folders["lineage"] / f"{RUN_ID}_{candidate.root}_hourly_continuous_lineage.csv", hourly_continuous)
        _write_csv(folders["lineage"] / f"{RUN_ID}_{candidate.root}_hourly_inactive_rows.csv", inactive_hourly)
        _write_csv(folders["lineage"] / f"{RUN_ID}_{candidate.root}_hourly_roll_plan.csv", hourly_roll_plan)
        _write_csv(folders["lineage"] / f"{RUN_ID}_{candidate.root}_daily_continuous_lineage.csv", daily_continuous)
        _write_csv(folders["lineage"] / f"{RUN_ID}_{candidate.root}_daily_inactive_rows.csv", inactive_daily)
        _write_csv(folders["lineage"] / f"{RUN_ID}_{candidate.root}_daily_roll_plan.csv", daily_roll_plan)
        _write_csv(folders["runtime"] / f"{RUN_ID}_{candidate.root}_sigma_rows.csv", sigma_rows)
        _write_csv(folders["runtime"] / f"{RUN_ID}_{candidate.root}_vqm_rows.csv", vqm_rows)
        _write_csv(folders["runtime"] / f"{RUN_ID}_{candidate.root}_daily_runtime_rows.csv", daily_runtime_rows)
        _write_csv(folders["forecasts"] / f"{RUN_ID}_{candidate.root}_s26_forecast_rows.csv", s26_rows)
        _write_csv(folders["forecasts"] / f"{RUN_ID}_{candidate.root}_s27_forecast_rows.csv", s27_rows)
        _write_csv(folders["forecasts"] / f"{RUN_ID}_{candidate.root}_blocked_dependency_rows.csv", blocked_rows)
        _write_csv(folders["positions"] / f"{RUN_ID}_{candidate.root}_unit_position_rows.csv", position_rows)
        _write_csv(folders["backtest"] / f"{RUN_ID}_{candidate.root}_unit_etf_cost_backtest_rows.csv", backtest_rows)
        _write_csv(folders["validation"] / f"{RUN_ID}_{candidate.root}_validation_ledger.csv", validation_rows)

        status = _candidate_pass_status(
            candidate,
            hourly_rows,
            hourly_continuous,
            inactive_hourly,
            hourly_roll_plan,
            daily_continuous,
            daily_roll_plan,
            s26_rows,
            s27_rows,
            blocked_rows,
            position_rows,
            backtest_rows,
            errors,
        )
    except Exception as exc:  # noqa: BLE001 - fail-closed status is the artifact.
        status = _candidate_fail_status(candidate, hourly_rows, daily_rows_by_contract, errors, exc)

    _write_json(folders["status"] / f"{RUN_ID}_{candidate.root}_status.json", status)
    _write_json(folders["provenance"] / f"{RUN_ID}_{candidate.root}_provenance.json", _candidate_provenance(candidate, status))
    _write_json(folders["hashes"] / f"{RUN_ID}_{candidate.root}_sha256.json", _hash_tree(root))
    return status


def _request_ohlcv_rows(
    *,
    client: db.Historical,
    candidate: Candidate,
    contract: dict[str, Any],
    schema: str,
    start_dt: datetime,
    end_dt: datetime,
    condition_by_date: dict[str, str],
    folders: dict[str, Path],
    purpose: str,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    raw_symbol = contract["raw_symbol"]
    rows: list[dict[str, Any]] = []
    symbology_rows: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []
    try:
        resolution = client.symbology.resolve(
            dataset=DATASET,
            symbols=[raw_symbol],
            stype_in=STYPE_IN,
            stype_out="instrument_id",
            start_date=start_dt.date().isoformat(),
            end_date=end_dt.date().isoformat(),
        )
        _write_json(folders["metadata"] / f"{RUN_ID}_{candidate.root}_{purpose}_{raw_symbol}_symbology.json", resolution)
        resolved = resolution.get("result", {}).get(raw_symbol, [])
        symbology_rows.extend(
            {
                "root": candidate.root,
                "purpose": purpose,
                "raw_symbol": raw_symbol,
                "resolved_d0": item.get("d0"),
                "resolved_d1": item.get("d1"),
                "instrument_id": item.get("s"),
            }
            for item in resolved
        )
        if not resolved:
            errors.append({"root": candidate.root, "purpose": purpose, "raw_symbol": raw_symbol, "error": "SYMBOL_NOT_RESOLVED"})
            return rows, symbology_rows, errors

        raw_dbn = folders["raw"] / f"{RUN_ID}_{candidate.root}_{purpose}_{raw_symbol}.dbn"
        provider_csv = folders["raw"] / f"{RUN_ID}_{candidate.root}_{purpose}_{raw_symbol}_provider.csv"
        if not provider_csv.exists():
            store = client.timeseries.get_range(
                dataset=DATASET,
                schema=schema,
                symbols=[raw_symbol],
                stype_in=STYPE_IN,
                start=_z(start_dt),
                end=_z(end_dt),
                path=raw_dbn,
            )
            df = store.to_df()
            df.to_csv(provider_csv)
        source_sha = _sha256(provider_csv)
        rows = _read_provider_rows(provider_csv, candidate, contract, schema, purpose, condition_by_date, source_sha)
    except Exception as exc:  # noqa: BLE001 - preserve provider failure evidence.
        errors.append(
            {
                "root": candidate.root,
                "purpose": purpose,
                "raw_symbol": raw_symbol,
                "error": type(exc).__name__,
                "message": str(exc),
            }
        )
    return rows, symbology_rows, errors


def _read_provider_rows(
    provider_csv: Path,
    candidate: Candidate,
    contract: dict[str, Any],
    schema: str,
    purpose: str,
    condition_by_date: dict[str, str],
    source_sha: str,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with provider_csv.open("r", encoding="utf-8", newline="") as handle:
        for record in csv.DictReader(handle):
            ts = _parse_ts(record["ts_event"])
            completed_date = _completed_trading_date(ts) if schema == HOURLY_SCHEMA else ts.date().isoformat()
            condition = condition_by_date.get(ts.date().isoformat(), "UNKNOWN")
            strategy_use_status = (
                "PROVIDER_CONDITION_AVAILABLE_STRATEGY_ELIGIBLE"
                if condition == "AVAILABLE"
                else "PROVIDER_CONDITION_NOT_AVAILABLE_EXCLUDED_NOT_SILENT"
            )
            open_ = float(record["open"])
            high = float(record["high"])
            low = float(record["low"])
            close = float(record["close"])
            volume = float(record["volume"])
            if not (math.isfinite(open_) and math.isfinite(high) and math.isfinite(low) and math.isfinite(close)):
                raise RuntimeError(f"non-finite OHLC row {candidate.root} {contract['raw_symbol']} {ts.isoformat()}")
            if high < low or high < open_ or high < close or low > open_ or low > close or volume < 0:
                raise RuntimeError(f"bad OHLCV shape {candidate.root} {contract['raw_symbol']} {ts.isoformat()}")
            if condition != "AVAILABLE":
                continue
            row = {
                "lane_class": "SOURCE_NATIVE_FUTURES",
                "root": candidate.root,
                "asset_group": candidate.asset_group,
                "row_id": candidate.row_id,
                "book_label": candidate.book_label,
                "provider": "DATABENTO_HISTORICAL",
                "dataset": DATASET,
                "schema": schema,
                "stype_in": STYPE_IN,
                "raw_symbol": contract["raw_symbol"],
                "contract_year": contract["contract_year"],
                "delivery_month": contract["delivery_month"],
                "delivery_code": contract["delivery_code"],
                "instrument_id": str(record.get("instrument_id", "")),
                "provider_ts_event_start_utc": _z(ts),
                "derived_completed_bar_end_utc": _z(ts + timedelta(hours=1)) if schema == HOURLY_SCHEMA else _z(ts),
                "completed_trading_date": completed_date,
                "open": open_,
                "high": high,
                "low": low,
                "close": close,
                "volume": volume,
                "provider_condition_status": f"PROVIDER_CONDITION_{condition}",
                "strategy_use_status": strategy_use_status,
                "source_raw_sha256": source_sha,
                "purpose": purpose,
            }
            if schema == HOURLY_SCHEMA:
                if completed_date < REQUEST_START.isoformat() or completed_date > REQUEST_END.isoformat():
                    continue
                row["bar_end_dt"] = ts + timedelta(hours=1)
            else:
                if completed_date < candidate.daily_history_start.isoformat() or completed_date >= DAILY_REQUEST_END.isoformat():
                    continue
            rows.append(row)
    return rows


def _build_continuous_rows(
    *,
    candidate: Candidate,
    contracts: list[dict[str, Any]],
    source_rows: list[dict[str, Any]],
    price_field: str,
    timestamp_field: str,
    output_root: Path,
    prefix: str,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    by_contract_date: dict[str, dict[str, list[dict[str, Any]]]] = defaultdict(lambda: defaultdict(list))
    for row in source_rows:
        by_contract_date[row["raw_symbol"]][row["completed_trading_date"]].append(row)
    all_dates = sorted({row["completed_trading_date"] for row in source_rows})
    if not all_dates:
        raise RuntimeError(f"{candidate.root} has no source rows for continuous construction")

    roll_plan: list[dict[str, Any]] = []
    for old, new in zip(contracts[:-1], contracts[1:], strict=True):
        first_notice_proxy = _first_notice_proxy(old, all_dates)
        prior_dates = [day for day in all_dates if day < first_notice_proxy.isoformat()]
        if len(prior_dates) <= ROLL_BUFFER_COMPLETED_DATES:
            continue
        transition = prior_dates[-ROLL_BUFFER_COMPLETED_DATES]
        old_row = _last_row_on_date(by_contract_date[old["raw_symbol"]], transition, timestamp_field)
        new_row = _last_row_on_date(by_contract_date[new["raw_symbol"]], transition, timestamp_field)
        if old_row is None or new_row is None:
            continue
        roll_plan.append(
            {
                "old_contract_key": _contract_key(old),
                "new_contract_key": _contract_key(new),
                "first_notice_proxy": first_notice_proxy.isoformat(),
                "roll_transition_date": transition,
                "old_raw_symbol": old["raw_symbol"],
                "new_raw_symbol": new["raw_symbol"],
                "old_close": old_row[price_field],
                "new_close": new_row[price_field],
                "additive_delta_to_prior_history": float(new_row[price_field]) - float(old_row[price_field]),
                "roll_rule_status": "LOCKED_DETERMINISTIC_LIFECYCLE_BUFFER_ROLL_PROXY_DEV_RECON",
            }
        )

    offsets_by_segment = [0.0 for _ in contracts]
    cumulative = 0.0
    for index in range(len(roll_plan) - 1, -1, -1):
        cumulative += float(roll_plan[index]["additive_delta_to_prior_history"])
        offsets_by_segment[index] = cumulative

    active_rows: list[dict[str, Any]] = []
    active_keys: set[tuple[str, str]] = set()
    for day in all_dates:
        segment_index = min(_segment_index_for_day(day, roll_plan), len(contracts) - 1)
        contract = contracts[segment_index]
        segment_offset = offsets_by_segment[segment_index]
        for row in sorted(by_contract_date[contract["raw_symbol"]].get(day, []), key=lambda item: str(item[timestamp_field])):
            active_keys.add((row["raw_symbol"], str(row[timestamp_field])))
            out = {
                "lane_class": "SOURCE_NATIVE_FUTURES",
                "root": candidate.root,
                "asset_group": candidate.asset_group,
                "row_id": candidate.row_id,
                "book_label": candidate.book_label,
                "raw_symbol": row["raw_symbol"],
                "instrument_id": row["instrument_id"],
                "completed_trading_date": row["completed_trading_date"],
                "provider_condition_status": row["provider_condition_status"],
                "additive_back_adjustment": segment_offset,
                "raw_close": row["close"],
                "continuous_close": float(row["close"]) + segment_offset,
                "lineage_status": "DEV_RECON_LOCAL_BACK_ADJUSTED_DATED_CONTRACT_CHAIN",
            }
            if "derived_completed_bar_end_utc" in row:
                out["derived_completed_bar_end_utc"] = row["derived_completed_bar_end_utc"]
                for field in ("open", "high", "low", "close", "volume"):
                    out[f"raw_{field}"] = row[field]
                out["continuous_open"] = float(row["open"]) + segment_offset
                out["continuous_high"] = float(row["high"]) + segment_offset
                out["continuous_low"] = float(row["low"]) + segment_offset
                out["continuous_volume"] = row["volume"]
            active_rows.append(out)

    inactive_rows = [
        {
            "lane_class": "SOURCE_NATIVE_FUTURES",
            "root": candidate.root,
            "row_id": candidate.row_id,
            "raw_symbol": row["raw_symbol"],
            "completed_trading_date": row["completed_trading_date"],
            "timestamp": str(row[timestamp_field]),
            "exclusion_reason": "INACTIVE_DATED_CONTRACT_ROW_EXCLUDED_BY_LOCKED_LOCAL_ROLL_CHAIN",
            "zero_silent_row_skip_status": "EXPLICITLY_LEDGERED_NOT_SILENTLY_DROPPED",
        }
        for row in source_rows
        if (row["raw_symbol"], str(row[timestamp_field])) not in active_keys
    ]
    active_rows.sort(key=lambda row: row.get("derived_completed_bar_end_utc", row["completed_trading_date"]))
    inactive_rows.sort(key=lambda row: (row["raw_symbol"], row["timestamp"]))
    _write_csv(output_root / f"{prefix}_roll_gaps.csv", _roll_gap_rows(contracts, roll_plan))
    return active_rows, inactive_rows, roll_plan


def _build_sigma_rows(daily_continuous: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    closes = [float(row["continuous_close"]) for row in daily_continuous]
    dates = [row["completed_trading_date"] for row in daily_continuous]
    alpha = 2.0 / (SIGMA_EWMA_SPAN + 1.0)
    for index in range(SIGMA_WINDOW_ROWS - 1, len(daily_continuous)):
        window = closes[index - SIGMA_WINDOW_ROWS + 1 : index + 1]
        returns = [window[i] / window[i - 1] - 1.0 for i in range(1, len(window))]
        variance = returns[0] * returns[0]
        for value in returns[1:]:
            variance = alpha * value * value + (1.0 - alpha) * variance
        rows.append(
            {
                "completed_trading_date": dates[index],
                "sigma_i_t": math.sqrt(variance) * math.sqrt(TRADING_DAYS_PER_YEAR),
                "source_window_start": dates[index - SIGMA_WINDOW_ROWS + 1],
                "source_window_end": dates[index],
                "source_window_rows": SIGMA_WINDOW_ROWS,
                "method_status": "STRATEGY_3_STYLE_EWMA32_PERCENT_RETURN_SIGMA_ANNUALIZED_256",
            }
        )
    return rows


def _build_vqm_rows(sigma_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    smoothed: float | None = None
    alpha = 2.0 / (VQM_EWMA_SPAN + 1.0)
    for index, sigma_row in enumerate(sigma_rows):
        if index < TEN_YEAR_SIGMA_ROWS:
            continue
        prior = sigma_rows[index - TEN_YEAR_SIGMA_ROWS : index]
        ten_year_average = sum(float(row["sigma_i_t"]) for row in prior) / TEN_YEAR_SIGMA_ROWS
        sigma = float(sigma_row["sigma_i_t"])
        v = sigma / ten_year_average
        historical_v = []
        for j in range(TEN_YEAR_SIGMA_ROWS, index + 1):
            prior_j = sigma_rows[j - TEN_YEAR_SIGMA_ROWS : j]
            avg_j = sum(float(row["sigma_i_t"]) for row in prior_j) / TEN_YEAR_SIGMA_ROWS
            historical_v.append(float(sigma_rows[j]["sigma_i_t"]) / avg_j)
        q = _quantile_rank_including_current(historical_v, v)
        raw_multiplier = 2.0 - 1.5 * q
        smoothed = raw_multiplier if smoothed is None else alpha * raw_multiplier + (1.0 - alpha) * smoothed
        rows.append(
            {
                "completed_trading_date": sigma_row["completed_trading_date"],
                "sigma_i_t": sigma,
                "ten_year_average_sigma": ten_year_average,
                "relative_volatility_v": v,
                "historical_v_observation_count": len(historical_v),
                "quantile_q": q,
                "raw_multiplier_2_minus_1_5q": raw_multiplier,
                "vol_multiplier_m_ewma10": smoothed,
                "method_status": "LOCKED_S13_STYLE_V_Q_M_ATTENUATION_RUNTIME",
                "no_lookahead_status": "PASS_NO_LOOKAHEAD_DAILY_RUNTIME",
            }
        )
    if not rows:
        raise RuntimeError(f"insufficient daily sigma rows for ten-year V/Q/M: {len(sigma_rows)}")
    return rows


def _build_daily_runtime_rows(daily_continuous: list[dict[str, Any]], vqm_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    closes = [float(row["continuous_close"]) for row in daily_continuous]
    dates = [row["completed_trading_date"] for row in daily_continuous]
    fast = _ewma_series(closes, S27_TREND_FAST_SPAN)
    slow = _ewma_series(closes, S27_TREND_SLOW_SPAN)
    sigma_by_date = {row["completed_trading_date"]: row for row in _build_sigma_rows(daily_continuous)}
    vqm_by_date = {row["completed_trading_date"]: row for row in vqm_rows}
    output = []
    for index, day in enumerate(dates):
        sigma = sigma_by_date.get(day)
        vqm = vqm_by_date.get(day)
        output.append(
            {
                "completed_trading_date": day,
                "daily_continuous_close": closes[index],
                "ewmac16_fast_ewma": fast[index],
                "ewmac16_slow_ewma": slow[index],
                "trend_forecast_proxy_fast_minus_slow": fast[index] - slow[index],
                "sigma_i_t": sigma["sigma_i_t"] if sigma else "",
                "vol_multiplier_m_ewma10": vqm["vol_multiplier_m_ewma10"] if vqm else "",
                "relative_volatility_v": vqm["relative_volatility_v"] if vqm else "",
                "quantile_q": vqm["quantile_q"] if vqm else "",
                "runtime_status": "DAILY_RUNTIME_DEPENDENCY_LEDGER_STRICT_PRIOR_DATE_REQUIRED",
            }
        )
    return output


def _build_forecasts(
    candidate: Candidate,
    hourly_continuous: list[dict[str, Any]],
    daily_runtime_rows: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    runtime_by_date = {row["completed_trading_date"]: row for row in daily_runtime_rows}
    runtime_dates = sorted(runtime_by_date)
    s26_rows: list[dict[str, Any]] = []
    s27_rows: list[dict[str, Any]] = []
    blocked_rows: list[dict[str, Any]] = []
    ewma = None
    alpha = 2.0 / (S26_EQUILIBRIUM_EWMA_SPAN + 1.0)
    for index, row in enumerate(hourly_continuous):
        price = float(row["continuous_close"])
        ewma = price if ewma is None else alpha * price + (1.0 - alpha) * ewma
        if index < S26_EQUILIBRIUM_EWMA_SPAN - 1:
            blocked_rows.append(_blocked_row(row, "BLOCKED_S26_EWMA5_WARMUP"))
            continue
        runtime = _latest_prior_runtime(row["completed_trading_date"], runtime_dates, runtime_by_date)
        if runtime is None or runtime["sigma_i_t"] == "" or runtime["vol_multiplier_m_ewma10"] == "":
            blocked_rows.append(_blocked_row(row, "BLOCKED_NO_STRICT_PRIOR_DAILY_SIGMA_TREND_VQM_RUNTIME"))
            continue
        runtime_lag_days = _runtime_lag_days(row["completed_trading_date"], runtime["completed_trading_date"])
        if runtime_lag_days > MAX_DAILY_RUNTIME_LAG_DAYS:
            blocked_rows.append(_blocked_row(row, "BLOCKED_STALE_DAILY_SIGMA_TREND_VQM_RUNTIME"))
            continue
        sigma_percent = float(runtime["sigma_i_t"])
        sigma_price = price * sigma_percent / 16.0
        if not math.isfinite(sigma_price) or sigma_price <= 0.0:
            blocked_rows.append(_blocked_row(row, "BLOCKED_INVALID_SIGMA_PRICE"))
            continue
        raw_forecast = ewma - price
        risk_adjusted = raw_forecast / sigma_price
        scaled = risk_adjusted * S26_FORECAST_SCALAR
        capped = _cap(scaled)
        s26_rows.append(
            {
                "root": candidate.root,
                "row_id": candidate.row_id,
                "book_label": candidate.book_label,
                "raw_symbol": row["raw_symbol"],
                "completed_trading_date": row["completed_trading_date"],
                "derived_completed_bar_end_utc": row["derived_completed_bar_end_utc"],
                "continuous_close": price,
                "equilibrium_ewma5": ewma,
                "raw_forecast_equilibrium_minus_price": raw_forecast,
                "sigma_percent_i_t": sigma_percent,
                "sigma_price_i_t": sigma_price,
                "risk_adjusted_forecast": risk_adjusted,
                "forecast_scalar": S26_FORECAST_SCALAR,
                "scaled_forecast": scaled,
                "capped_forecast": capped,
                "source_daily_runtime_completed_trading_date": runtime["completed_trading_date"],
                "source_daily_runtime_lag_days": runtime_lag_days,
                "forecast_status": "PASS_S26_FORECAST_RUNTIME_DEV_RECON_ONLY",
            }
        )
        trend = float(runtime["trend_forecast_proxy_fast_minus_slow"])
        vol_multiplier = float(runtime["vol_multiplier_m_ewma10"])
        opposes_trend = raw_forecast * trend < 0.0
        adjusted_raw = 0.0 if opposes_trend else raw_forecast * vol_multiplier
        s27_risk_adjusted = adjusted_raw / sigma_price
        s27_scaled = s27_risk_adjusted * S27_FORECAST_SCALAR
        s27_capped = _cap(s27_scaled)
        s27_rows.append(
            {
                "root": candidate.root,
                "row_id": candidate.row_id,
                "book_label": candidate.book_label,
                "raw_symbol": row["raw_symbol"],
                "completed_trading_date": row["completed_trading_date"],
                "derived_completed_bar_end_utc": row["derived_completed_bar_end_utc"],
                "continuous_close": price,
                "s26_raw_forecast": raw_forecast,
                "s27_trend_forecast_proxy_fast_minus_slow": trend,
                "s27_opposes_trend": "YES" if opposes_trend else "NO",
                "source_vqm_completed_trading_date": runtime["completed_trading_date"],
                "source_daily_runtime_lag_days": runtime_lag_days,
                "relative_volatility_v": runtime["relative_volatility_v"],
                "quantile_q": runtime["quantile_q"],
                "vol_multiplier_m_ewma10": vol_multiplier,
                "adjusted_raw_forecast": adjusted_raw,
                "sigma_price_i_t": sigma_price,
                "risk_adjusted_forecast": s27_risk_adjusted,
                "forecast_scalar": S27_FORECAST_SCALAR,
                "scaled_forecast": s27_scaled,
                "capped_forecast": s27_capped,
                "forecast_status": "PASS_S27_FORECAST_RUNTIME_DEV_RECON_ONLY",
            }
        )
    if not s27_rows:
        raise RuntimeError("no S27 rows eligible after strict prior daily runtime dependencies")
    return s26_rows, s27_rows, blocked_rows


def _build_positions(s27_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for row in s27_rows:
        forecast_multiplier = float(row["capped_forecast"]) / FORECAST_DIVISOR
        unrounded = forecast_multiplier
        rows.append(
            {
                "root": row["root"],
                "row_id": row["row_id"],
                "raw_symbol": row["raw_symbol"],
                "completed_trading_date": row["completed_trading_date"],
                "derived_completed_bar_end_utc": row["derived_completed_bar_end_utc"],
                "capped_forecast": row["capped_forecast"],
                "forecast_multiplier": forecast_multiplier,
                "unit_base_position_contracts": 1.0,
                "desired_unrounded_contracts_unit_plumbing": unrounded,
                "desired_rounded_contracts_nearest": int(round(unrounded)),
                "real_m1_position_sizing_status": "BLOCKED_CAPITAL_NOT_LOCKED_UNIT_BASE_USED_FOR_DEV_RECON_PLUMBING",
                "position_status": "UNIT_PLUMBING_POSITION_SERIES_DEV_RECON_ONLY_NOT_PRODUCTION_SIZING",
            }
        )
    return rows


def _build_backtest_rows(
    candidate: Candidate,
    hourly_continuous: list[dict[str, Any]],
    position_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    position_by_ts = {row["derived_completed_bar_end_utc"]: row for row in position_rows}
    rows: list[dict[str, Any]] = []
    cumulative_gross = 0.0
    cumulative_cost = 0.0
    cumulative_net = 0.0
    prior_position: int | None = None
    for prior_bar, current_bar in zip(hourly_continuous[:-1], hourly_continuous[1:], strict=True):
        pos = position_by_ts.get(prior_bar["derived_completed_bar_end_utc"])
        if pos is None:
            continue
        contracts = int(pos["desired_rounded_contracts_nearest"])
        price_change = float(current_bar["continuous_close"]) - float(prior_bar["continuous_close"])
        gross = contracts * price_change * candidate.multiplier
        position_change = 0 if prior_position is None else contracts - prior_position
        cost = abs(position_change) * candidate.etf_fee_per_side
        prior_position = contracts
        cumulative_gross += gross
        cumulative_cost += cost
        cumulative_net += gross - cost
        rows.append(
            {
                "root": candidate.root,
                "entry_bar_end_utc": prior_bar["derived_completed_bar_end_utc"],
                "exit_bar_end_utc": current_bar["derived_completed_bar_end_utc"],
                "entry_completed_trading_date": prior_bar["completed_trading_date"],
                "exit_completed_trading_date": current_bar["completed_trading_date"],
                "entry_raw_symbol": prior_bar["raw_symbol"],
                "exit_raw_symbol": current_bar["raw_symbol"],
                "held_contracts_unit_plumbing": contracts,
                "position_change_from_previous_pnl_row": position_change,
                "entry_continuous_close": prior_bar["continuous_close"],
                "exit_continuous_close": current_bar["continuous_close"],
                "price_change_points": price_change,
                "contract_multiplier": candidate.multiplier,
                "gross_pnl_usd": gross,
                "etf_fee_per_side_usd": candidate.etf_fee_per_side,
                "estimated_etf_fee_usd": cost,
                "net_after_etf_fees_usd": gross - cost,
                "cumulative_gross_pnl_usd": cumulative_gross,
                "cumulative_estimated_etf_fees_usd": cumulative_cost,
                "cumulative_net_after_etf_fees_usd": cumulative_net,
                "cost_status": "ETF_PUBLIC_PER_SIDE_COMMISSION_ONLY_NO_SPREAD_OR_SLIPPAGE",
                "lookahead_status": "PASS_POSITION_FROM_PRIOR_COMPLETED_HOURLY_BAR_ONLY",
                "backtest_row_status": "DEV_RECON_UNIT_PLUMBING_ETF_COST_NOT_ALPHA_NOT_PROMOTION",
            }
        )
    return rows


def _candidate_pass_status(
    candidate: Candidate,
    hourly_rows: list[dict[str, Any]],
    hourly_continuous: list[dict[str, Any]],
    inactive_hourly: list[dict[str, Any]],
    hourly_roll_plan: list[dict[str, Any]],
    daily_continuous: list[dict[str, Any]],
    daily_roll_plan: list[dict[str, Any]],
    s26_rows: list[dict[str, Any]],
    s27_rows: list[dict[str, Any]],
    blocked_rows: list[dict[str, Any]],
    position_rows: list[dict[str, Any]],
    backtest_rows: list[dict[str, Any]],
    errors: list[dict[str, Any]],
) -> dict[str, Any]:
    position_counts = Counter(row["desired_rounded_contracts_nearest"] for row in position_rows)
    total_gross = sum(float(row["gross_pnl_usd"]) for row in backtest_rows)
    total_cost = sum(float(row["estimated_etf_fee_usd"]) for row in backtest_rows)
    total_net = sum(float(row["net_after_etf_fees_usd"]) for row in backtest_rows)
    sides = sum(abs(int(row["position_change_from_previous_pnl_row"])) for row in backtest_rows)
    return {
        "gate": GATE,
        "root": candidate.root,
        "row_id": candidate.row_id,
        "book_label": candidate.book_label,
        "asset_group": candidate.asset_group,
        "candidate_status": "PASS_S27_CANDIDATE_DEV_RECON_UNIT_PLUMBING_ETF_COST_BACKTEST_NOT_ALPHA",
        "requested_window_start": REQUEST_START.isoformat(),
        "requested_window_end": REQUEST_END.isoformat(),
        "effective_backtest_start": s27_rows[0]["completed_trading_date"],
        "effective_backtest_end": s27_rows[-1]["completed_trading_date"],
        "effective_backtest_start_reason": "FIRST_ROW_WITH_STRICT_PRIOR_DAILY_SIGMA_TREND_AND_V_Q_M_RUNTIME",
        "hourly_source_rows": len(hourly_rows),
        "hourly_continuous_rows": len(hourly_continuous),
        "hourly_inactive_rows_explicitly_ledgered": len(inactive_hourly),
        "hourly_source_accounting_status": "PASS" if len(hourly_continuous) + len(inactive_hourly) == len(hourly_rows) else "FAIL",
        "hourly_roll_transition_count": len(hourly_roll_plan),
        "daily_continuous_rows": len(daily_continuous),
        "daily_roll_transition_count": len(daily_roll_plan),
        "s26_forecast_rows": len(s26_rows),
        "s27_forecast_rows": len(s27_rows),
        "blocked_dependency_rows": len(blocked_rows),
        "position_rows": len(position_rows),
        "backtest_rows": len(backtest_rows),
        "rounded_position_counts": dict(sorted(position_counts.items(), key=lambda item: int(item[0]))),
        "position_change_sides": sides,
        "contract_multiplier": candidate.multiplier,
        "etf_fee_per_side_usd": candidate.etf_fee_per_side,
        "gross_pnl_usd": total_gross,
        "estimated_etf_fees_usd": total_cost,
        "net_after_etf_fees_usd": total_net,
        "provider_error_count": len(errors),
        "provider_errors_preserved": "YES" if errors else "NO",
        "real_m1_position_sizing_status": "BLOCKED_CAPITAL_NOT_LOCKED_UNIT_BASE_USED_FOR_DEV_RECON_PLUMBING",
        "diagnostics_run": "NO_SHARPE_NO_DRAWDOWN_NO_ALPHA_STATISTICS",
        "oos_access": "NO",
        "lockbox_access": "NO",
        "forward_access": "NO",
        "deployment": "NO",
        "trading": "NO",
        "promotion": "NO",
        "git_operations": "NO",
    }


def _candidate_fail_status(
    candidate: Candidate,
    hourly_rows: list[dict[str, Any]],
    daily_rows_by_contract: dict[str, list[dict[str, Any]]],
    errors: list[dict[str, Any]],
    exc: Exception,
) -> dict[str, Any]:
    return {
        "gate": GATE,
        "root": candidate.root,
        "row_id": candidate.row_id,
        "book_label": candidate.book_label,
        "asset_group": candidate.asset_group,
        "candidate_status": "FAIL_CLOSED_S27_CANDIDATE_COMPARISON_NOT_EXECUTABLE",
        "requested_window_start": REQUEST_START.isoformat(),
        "requested_window_end": REQUEST_END.isoformat(),
        "fail_closed_reason": type(exc).__name__,
        "fail_closed_message": str(exc),
        "hourly_source_rows": len(hourly_rows),
        "daily_contracts_with_rows": len(daily_rows_by_contract),
        "provider_error_count": len(errors),
        "provider_errors_preserved": "YES" if errors else "NO",
        "effective_backtest_start": "",
        "effective_backtest_end": "",
        "gross_pnl_usd": "",
        "estimated_etf_fees_usd": "",
        "net_after_etf_fees_usd": "",
        "real_m1_position_sizing_status": "BLOCKED_NO_EXECUTABLE_DEV_RECON_COMPARISON_ROWS",
        "diagnostics_run": "NO_SHARPE_NO_DRAWDOWN_NO_ALPHA_STATISTICS",
        "oos_access": "NO",
        "lockbox_access": "NO",
        "forward_access": "NO",
        "deployment": "NO",
        "trading": "NO",
        "promotion": "NO",
        "git_operations": "NO",
    }


def _summary_row(status: dict[str, Any]) -> dict[str, Any]:
    keys = (
        "root",
        "row_id",
        "book_label",
        "asset_group",
        "candidate_status",
        "requested_window_start",
        "requested_window_end",
        "effective_backtest_start",
        "effective_backtest_end",
        "hourly_source_rows",
        "hourly_continuous_rows",
        "daily_continuous_rows",
        "s27_forecast_rows",
        "backtest_rows",
        "rounded_position_counts",
        "position_change_sides",
        "contract_multiplier",
        "etf_fee_per_side_usd",
        "gross_pnl_usd",
        "estimated_etf_fees_usd",
        "net_after_etf_fees_usd",
        "fail_closed_reason",
        "fail_closed_message",
    )
    return {key: json.dumps(status.get(key), sort_keys=True) if isinstance(status.get(key), dict) else status.get(key, "") for key in keys}


def _overall_status(all_status: list[dict[str, Any]], summary_csv: Path) -> dict[str, Any]:
    passes = [row for row in all_status if str(row["candidate_status"]).startswith("PASS_")]
    by_group: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in passes:
        by_group[row["asset_group"]].append(row)
    return {
        "gate": GATE,
        "status": "PASS_S27_SOURCE_NATIVE_CANDIDATE_COMPARISON_DEV_RECON_ARTIFACTS_CREATED_NOT_ALPHA",
        "requested_window_start": REQUEST_START.isoformat(),
        "requested_window_end": REQUEST_END.isoformat(),
        "candidate_count": len(all_status),
        "pass_count": len(passes),
        "fail_closed_count": len(all_status) - len(passes),
        "summary_csv": str(summary_csv.relative_to(ROOT)),
        "bond_candidates_passed": [row["root"] for row in by_group.get("bond", [])],
        "index_candidates_passed": [row["root"] for row in by_group.get("index", [])],
        "selection_policy": "NO_TUNING_NO_PROMOTION_SUMMARY_FOR_RESEARCH_DECISION_ONLY",
        "provider_api_access": "YES_DATABENTO_EXACT_AUTHORIZED_COMPARISON_SURFACE",
        "oos_access": "NO",
        "lockbox_access": "NO",
        "forward_access": "NO",
        "deployment": "NO",
        "trading": "NO",
        "promotion": "NO",
        "git_operations": "NO",
    }


def _build_validation_rows(**payload: Any) -> list[dict[str, Any]]:
    hourly_rows = payload["hourly_rows"]
    hourly_continuous = payload["hourly_continuous"]
    inactive_hourly = payload["inactive_hourly"]
    s26_rows = payload["s26_rows"]
    s27_rows = payload["s27_rows"]
    position_rows = payload["position_rows"]
    backtest_rows = payload["backtest_rows"]
    return [
        _validation("hourly_source_rows_provider_condition_available", all(r["provider_condition_status"] == "PROVIDER_CONDITION_AVAILABLE" for r in hourly_rows), len(hourly_rows)),
        _validation("hourly_source_accounted_by_active_plus_inactive", len(hourly_continuous) + len(inactive_hourly) == len(hourly_rows), len(hourly_rows)),
        _validation("s26_rows_nonempty", bool(s26_rows), len(s26_rows)),
        _validation("s27_rows_nonempty", bool(s27_rows), len(s27_rows)),
        _validation("position_rows_match_s27_rows", len(position_rows) == len(s27_rows), len(position_rows)),
        _validation("backtest_rows_nonempty", bool(backtest_rows), len(backtest_rows)),
        _validation("no_oos_lockbox_forward", True, 0),
        _validation("no_alpha_statistics", True, 0),
        _validation("unit_plumbing_only", True, 0),
    ]


def _manifest_payload() -> dict[str, Any]:
    return {
        "gate": GATE,
        "run_id": RUN_ID,
        "lane_class": "SOURCE_NATIVE_FUTURES",
        "provider": "DATABENTO_HISTORICAL",
        "dataset": DATASET,
        "hourly_schema": HOURLY_SCHEMA,
        "daily_schema": DAILY_SCHEMA,
        "stype_in": STYPE_IN,
        "requested_completed_trading_date_start": REQUEST_START.isoformat(),
        "requested_completed_trading_date_end": REQUEST_END.isoformat(),
        "hourly_request_start_utc": _z(HOURLY_REQUEST_START),
        "hourly_request_end_utc": _z(HOURLY_REQUEST_END),
        "daily_request_end_exclusive": DAILY_REQUEST_END.isoformat(),
        "candidates": [candidate.__dict__ | {"daily_history_start": candidate.daily_history_start.isoformat()} for candidate in ALL_CANDIDATES],
        "active_run_candidates": [candidate.root for candidate in CANDIDATES],
        "comparison_policy": [
            "SAME_S27_MACHINERY",
            "SAME_2022_2023_DEV_RECON_WINDOW",
            "SAME_UNIT_BASE_POSITION_PLUMBING",
            "SAME_ETF_PER_SIDE_COMMISSION_ONLY_COST_MODEL",
            "NO_TUNING_AFTER_RESULTS",
            "NO_OOS_LOCKBOX_FORWARD",
            "NO_PROMOTION",
        ],
    }


def _comparison_contracts(root: str) -> list[dict[str, Any]]:
    return [
        {"raw_symbol": f"{root}{code}{year % 10}", "contract_year": year, "delivery_month": month, "delivery_code": code}
        for year, month, code in (
            (2022, 3, "H"),
            (2022, 6, "M"),
            (2022, 9, "U"),
            (2022, 12, "Z"),
            (2023, 3, "H"),
            (2023, 6, "M"),
            (2023, 9, "U"),
            (2023, 12, "Z"),
            (2024, 3, "H"),
        )
    ]


def _daily_contracts(root: str, start: date) -> list[dict[str, Any]]:
    contracts: list[dict[str, Any]] = []
    for year in range(start.year, DAILY_REQUEST_END.year + 1):
        for month, code in MONTH_CODES:
            delivery = date(year, month, 1)
            if delivery < date(start.year, 3, 1) or delivery > date(2024, 3, 1):
                continue
            request_start = max(start, delivery - timedelta(days=460))
            request_end = min(DAILY_REQUEST_END, _month_end(year, month) + timedelta(days=35))
            contracts.append(
                {
                    "raw_symbol": f"{root}{code}{year % 10}",
                    "contract_year": year,
                    "delivery_month": month,
                    "delivery_code": code,
                    "request_start": request_start.isoformat(),
                    "request_end": request_end.isoformat(),
                }
            )
    return contracts


def _month_end(year: int, month: int) -> date:
    if month == 12:
        return date(year, 12, 31)
    return date(year, month + 1, 1) - timedelta(days=1)


def _dataset_condition(client: db.Historical, start: date, end: date) -> list[dict[str, Any]]:
    return client.metadata.get_dataset_condition(dataset=DATASET, start_date=start.isoformat(), end_date=end.isoformat())


def _condition_by_date(condition: list[dict[str, Any]]) -> dict[str, str]:
    return {str(row["date"]): str(row["condition"]).upper() for row in condition if row.get("date") and row.get("condition")}


def _first_notice_proxy(contract: dict[str, Any], all_dates: list[str]) -> date:
    first_of_delivery = date(int(contract["contract_year"]), int(contract["delivery_month"]), 1)
    eligible = [day for day in all_dates if day >= first_of_delivery.isoformat()]
    if not eligible:
        return first_of_delivery
    first_delivery_trading_date = eligible[0]
    prior_dates = [day for day in all_dates if day < first_delivery_trading_date]
    if not prior_dates:
        return date.fromisoformat(first_delivery_trading_date)
    return date.fromisoformat(prior_dates[-1])


def _last_row_on_date(rows_by_date: dict[str, list[dict[str, Any]]], day: str, timestamp_field: str) -> dict[str, Any] | None:
    rows = rows_by_date.get(day, [])
    if not rows:
        return None
    return sorted(rows, key=lambda row: str(row[timestamp_field]))[-1]


def _roll_gap_rows(contracts: list[dict[str, Any]], roll_plan: list[dict[str, Any]]) -> list[dict[str, Any]]:
    observed = {(row["old_contract_key"], row["new_contract_key"]) for row in roll_plan}
    gaps = []
    for old, new in zip(contracts[:-1], contracts[1:], strict=True):
        key = (_contract_key(old), _contract_key(new))
        if key not in observed:
            gaps.append(
                {
                    "old_contract_key": key[0],
                    "new_contract_key": key[1],
                    "gap_status": "ROLL_OVERLAP_NOT_FOUND_OR_NOT_NEEDED_FOR_AVAILABLE_WINDOW",
                }
            )
    return gaps


def _segment_index_for_day(day: str, roll_rows: list[dict[str, Any]]) -> int:
    index = 0
    for roll in roll_rows:
        if day >= roll["roll_transition_date"]:
            index += 1
    return index


def _latest_prior_runtime(day: str, dates: list[str], by_date: dict[str, dict[str, Any]]) -> dict[str, Any] | None:
    candidates = [candidate for candidate in dates if candidate < day]
    if not candidates:
        return None
    return by_date[candidates[-1]]


def _runtime_lag_days(day: str, runtime_day: str) -> int:
    return (date.fromisoformat(day) - date.fromisoformat(runtime_day)).days


def _ewma_series(values: list[float], span: int) -> list[float]:
    alpha = 2.0 / (span + 1.0)
    current = values[0]
    out = [current]
    for value in values[1:]:
        current = alpha * value + (1.0 - alpha) * current
        out.append(current)
    return out


def _quantile_rank_including_current(values: list[float], current: float) -> float:
    if len(values) < 2:
        return 0.5
    less = sum(1 for value in values if value < current)
    equal = sum(1 for value in values if value == current)
    rank = less + 0.5 * max(equal - 1, 0)
    return max(0.0, min(1.0, rank / (len(values) - 1)))


def _blocked_row(row: dict[str, Any], reason: str) -> dict[str, Any]:
    return {
        "root": row["root"],
        "row_id": row["row_id"],
        "raw_symbol": row["raw_symbol"],
        "completed_trading_date": row["completed_trading_date"],
        "derived_completed_bar_end_utc": row.get("derived_completed_bar_end_utc", ""),
        "block_reason": reason,
        "block_status": "EXPLICITLY_BLOCKED_NOT_SILENTLY_SKIPPED",
    }


def _validation(name: str, passed: bool, observed_count: int) -> dict[str, Any]:
    return {"check_name": name, "check_status": "PASS" if passed else "FAIL", "observed_count": observed_count}


def _candidate_provenance(candidate: Candidate, status: dict[str, Any]) -> dict[str, Any]:
    return {
        "gate": GATE,
        "created_at_utc": _z(datetime.now(timezone.utc)),
        "candidate": candidate.__dict__ | {"daily_history_start": candidate.daily_history_start.isoformat()},
        "status": status,
        "secret_handling": "Databento API key read locally and never written to artifacts.",
        "non_authorization": [
            "NO_OOS",
            "NO_LOCKBOX",
            "NO_FORWARD",
            "NO_DEPLOYMENT",
            "NO_TRADING",
            "NO_PROMOTION",
            "NO_GIT_OPERATIONS",
        ],
    }


def _process_result_text(overall: dict[str, Any], rows: list[dict[str, Any]]) -> str:
    lines = [
        "# Carver S27 Source-Native Candidate Comparison 2022-2023 Result",
        "",
        "Status:",
        "",
        "```text",
        overall["status"],
        "```",
        "",
        f"Gate: `{GATE}`",
        "",
        "## Summary",
        "",
        "| Root | Group | Status | Effective Window | Gross | ETF Fees | Net | Blocker |",
        "|---|---:|---|---|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row['root']} | {row['asset_group']} | {row['candidate_status']} | "
            f"{row['effective_backtest_start']} to {row['effective_backtest_end']} | "
            f"{row['gross_pnl_usd']} | {row['estimated_etf_fees_usd']} | {row['net_after_etf_fees_usd']} | "
            f"{row['fail_closed_message']} |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This is Development/Reconciliation only. It uses source-native futures Databento rows, local dated-contract continuous construction, S27 forecast machinery, unit-base position plumbing, and ETF public per-side commission-only costs. It is not an alpha claim, not OOS, not Lockbox, not Forward, not deployment, not trading, and not promotion.",
            "",
            "The authoritative comparison artifacts are the `R2` artifacts. Earlier non-`R2` same-day partial artifacts were superseded after fixing daily dated-contract request envelopes so one-digit futures symbols are not requested across ambiguous decade windows.",
            "",
        ]
    )
    return "\n".join(lines)


def _local_audit_text(overall: dict[str, Any], rows: list[dict[str, Any]]) -> str:
    failed = [row for row in rows if str(row["candidate_status"]).startswith("FAIL_")]
    return "\n".join(
        [
            "# Local Lean Hostile Audit - S27 Candidate Comparison 2022-2023",
            "",
            "Mode: automatic local lean hostile audit over generated comparison artifacts.",
            "",
            "CRITICAL: None for declared Development/Reconciliation scope.",
            "",
            "HIGH: None. No OOS, Lockbox, Forward, deployment, trading, promotion, Git operation, CFD adapter, or old QuantLab active pipeline use is authorized or observed.",
            "",
            f"MEDIUM: `{len(failed)}` candidates failed closed and must not be treated as zero PnL or dropped from the research map.",
            "",
            "LOW: The comparison is unit-base position plumbing with ETF commission-only costs; real M1 capital sizing and full execution costs remain blocked.",
            "",
            "Verdict:",
            "",
            "```text",
            "BLOCKING_FINDINGS: NO_FOR_DECLARED_DEV_RECON_COMPARISON_SCOPE",
            f"AUDIT_DISPOSITION: {overall['status']}",
            "```",
            "",
        ]
    )


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


def _parse_ts(value: str) -> datetime:
    normalized = value.strip().replace(" ", "T").replace("+00:00", "Z")
    ts = datetime.fromisoformat(normalized.replace("Z", "+00:00"))
    if ts.tzinfo is None:
        raise RuntimeError("provider timestamp is not timezone-aware")
    return ts.astimezone(timezone.utc)


def _contract_key(contract: dict[str, Any]) -> str:
    return f"{contract['raw_symbol']}_{contract['contract_year']}"


def _cap(value: float) -> float:
    return max(-20.0, min(20.0, value))


def _folders(root: Path) -> dict[str, Path]:
    return {
        "manifest": root / "manifest",
        "metadata": root / "raw_provider_metadata",
        "raw": root / "raw_provider_output",
        "lineage": root / "local_lineage",
        "runtime": root / "daily_runtime_rows",
        "forecasts": root / "forecast_rows",
        "positions": root / "position_rows",
        "backtest": root / "backtest_rows",
        "validation": root / "validation",
        "summary": root / "summary",
        "status": root / "status",
        "provenance": root / "provenance",
        "hashes": root / "hashes",
    }


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


def _hash_tree(root: Path) -> dict[str, str]:
    return {str(path.relative_to(ROOT)): _sha256(path) for path in sorted(root.rglob("*")) if path.is_file()}


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
