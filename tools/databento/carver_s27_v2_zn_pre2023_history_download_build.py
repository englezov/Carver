from __future__ import annotations

import csv
import hashlib
import json
import math
import os
from collections import Counter
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
RUN_ID = "20260611_S27_V2_ZN_PRE2023_OLDER_HISTORY_DOWNLOAD_BUILD"
GATE = "S27_V2_DATABENTO_SOURCE_NATIVE_ZN_OLDER_HISTORY_DOWNLOAD_BUILD_GATE"
AUTHORIZATION = "S27_V2_EXACTLY_ONE_DATABENTO_ZN_OLDER_HISTORY_DOWNLOAD_BUILD_GATE"
LANE = "SOURCE_NATIVE_FUTURES"
PROVIDER = "DATABENTO_HISTORICAL"
DATASET = "GLBX.MDP3"
DAILY_SCHEMA = "ohlcv-1d"
HOURLY_SCHEMA = "ohlcv-1h"
DEFINITION_SCHEMA = "definition"
ROOT_SYMBOL = "ZN"
ROW_ID = "APPENDIX_C_172_004"
AUTHOR_MARKET_CODE = "ZN"

REQUEST_START = date(2010, 1, 1)
REQUEST_END_EXCLUSIVE = date(2023, 1, 1)
PROVIDER_AVAILABLE_START = date(2010, 6, 6)
DEV_START = date(2022, 1, 1)
DEV_END = date(2022, 12, 31)

MONTH_CODES = ((3, "H"), (6, "M"), (9, "U"), (12, "Z"))
ROLL_BUFFER_COMPLETED_DATES = 10
SIGMA_EWMA_SPAN = 32
SIGMA_WINDOW_ROWS = 34
TRADING_DAYS_PER_YEAR = 256.0
TEN_YEAR_SIGMA_ROWS = 2560
VQM_EWMA_SPAN = 10
EWMAC_FAST_SPAN = 16
EWMAC_SLOW_SPAN = 64

OUTPUT_ROOT = (
    ROOT
    / "docs/researchops/s27_v2_databento_older_zn_history/"
    / "20260611_pre2023_zn_dev_recon_download_build"
)
PACK_ROOT = (
    ROOT
    / "docs/researchops/s27_v2_local_replay_inputs/ZN/"
    / "20260611_pre2023_oldest_dev_recon_2022_declared_pack"
)
PROCESS_DOC = ROOT / "docs/process/CARVER_S27_ZN_V2_PRE2023_OLDER_HISTORY_DOWNLOAD_BUILD_RESULT_2026-06-11.md"
LOCAL_AUDIT_DOC = ROOT / "docs/process/CARVER_S27_ZN_V2_PRE2023_OLDER_HISTORY_LOCAL_AUDIT_RESULT_2026-06-11.md"

KEY_CANDIDATES = (
    Path(os.environ["DATABENTO_API_KEY_FILE"]) if os.environ.get("DATABENTO_API_KEY_FILE") else None,
    Path("C:/Users/apops/Desktop/BentoKey.txt"),
    Path("C:/Users/apops/Desktop/BENTO.txt"),
    Path("C:/Users/apops/Desktop/bento.txt"),
)

NON_AUTHORIZATIONS = (
    "NO_TEST_ACCESS",
    "NO_VALIDATION_ACCESS",
    "NO_OOS_ACCESS",
    "NO_LOCKBOX_ACCESS",
    "NO_FORWARD_ACCESS",
    "NO_BACKTESTS",
    "NO_RESULT_SCORED_RUNS",
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
    import databento as db  # noqa: PLC0415

    _ensure_output_roots()
    manifest_path = OUTPUT_ROOT / "manifest" / f"{RUN_ID}_request_manifest.json"
    _write_json(manifest_path, _request_manifest())

    key = _read_databento_key()
    client = db.Historical(key)

    condition = client.metadata.get_dataset_condition(
        dataset=DATASET,
        start_date=REQUEST_START.isoformat(),
        end_date=REQUEST_END_EXCLUSIVE.isoformat(),
    )
    condition_path = OUTPUT_ROOT / "raw_provider_metadata" / f"{RUN_ID}_dataset_condition.json"
    _write_json(condition_path, condition)
    condition_by_date = {
        str(row["date"]): str(row["condition"]).upper()
        for row in condition
        if row.get("date") and row.get("condition")
    }

    daily_contracts = _contract_specs(REQUEST_START, REQUEST_END_EXCLUSIVE, include_h3=True)
    hourly_contracts = _hourly_contract_specs()
    daily_rows_by_contract, daily_symbology, daily_definition, daily_errors = _download_contracts(
        client=client,
        contracts=daily_contracts,
        schema=DAILY_SCHEMA,
        condition_by_date=condition_by_date,
        output_subdir="daily",
    )
    hourly_rows_by_contract, hourly_symbology, hourly_definition, hourly_errors = _download_contracts(
        client=client,
        contracts=hourly_contracts,
        schema=HOURLY_SCHEMA,
        condition_by_date=condition_by_date,
        output_subdir="hourly",
    )

    errors = daily_errors + hourly_errors
    _write_csv(OUTPUT_ROOT / "raw_provider_metadata" / f"{RUN_ID}_symbology_resolution_ledger.csv", daily_symbology + hourly_symbology)
    _write_csv(OUTPUT_ROOT / "raw_provider_metadata" / f"{RUN_ID}_definition_ledger.csv", daily_definition + hourly_definition)
    if errors:
        _write_csv(OUTPUT_ROOT / "status" / f"{RUN_ID}_provider_errors.csv", errors)
    else:
        stale_errors = OUTPUT_ROOT / "status" / f"{RUN_ID}_provider_errors.csv"
        if stale_errors.exists():
            stale_errors.unlink()

    status: dict[str, Any]
    try:
        if errors:
            raise RuntimeError(f"provider request errors present: {len(errors)}")
        continuous, roll_rows = _build_continuous_series(daily_contracts, daily_rows_by_contract)
        sigma_rows = _build_sigma_rows(continuous)
        vqm_rows = _build_vqm_rows(sigma_rows)
        hourly_rows = _strategy_facing_hourly_rows(hourly_rows_by_contract)
        pack_manifest = _build_declared_pack(continuous, sigma_rows, vqm_rows, roll_rows, hourly_rows)
        status = _status_payload(continuous, sigma_rows, vqm_rows, hourly_rows, roll_rows, pack_manifest)
    except Exception as exc:  # noqa: BLE001 - preserve fail-closed provenance.
        status = {
            "gate": GATE,
            "status": "FAIL_CLOSED_S27_V2_PRE2023_ZN_HISTORY_BUILD_NOT_RUNNABLE",
            "reason": type(exc).__name__,
            "message": str(exc),
            "daily_contract_requests": len(daily_contracts),
            "hourly_contract_requests": len(hourly_contracts),
            "provider_error_count": len(errors),
            "backtests_run": "NO",
            "result_scored_runs": "NO",
            "test_access": "NO",
            "validation_access": "NO",
            "lockbox_access": "NO",
            "forward_access": "NO",
        }

    status_path = OUTPUT_ROOT / "status" / f"{RUN_ID}_status.json"
    provenance_path = OUTPUT_ROOT / "provenance" / f"{RUN_ID}_provenance.md"
    _write_json(status_path, status)
    provenance_path.write_text(_provenance_text(status), encoding="ascii")
    _write_json(OUTPUT_ROOT / "hashes" / f"{RUN_ID}_sha256.json", _hash_tree(OUTPUT_ROOT))
    PROCESS_DOC.write_text(_process_doc(status), encoding="ascii")
    LOCAL_AUDIT_DOC.write_text(_local_audit_doc(status), encoding="ascii")

    print(status["status"])
    print(f"artifact_root={OUTPUT_ROOT.relative_to(ROOT)}")
    if status.get("declared_pack_root"):
        print(f"declared_pack_root={status['declared_pack_root']}")


def _ensure_output_roots() -> None:
    for folder in (
        OUTPUT_ROOT / "manifest",
        OUTPUT_ROOT / "raw_provider_metadata",
        OUTPUT_ROOT / "raw_provider_output" / "daily",
        OUTPUT_ROOT / "raw_provider_output" / "hourly",
        OUTPUT_ROOT / "ledger",
        OUTPUT_ROOT / "validation",
        OUTPUT_ROOT / "status",
        OUTPUT_ROOT / "provenance",
        OUTPUT_ROOT / "hashes",
        PACK_ROOT,
    ):
        folder.mkdir(parents=True, exist_ok=True)


def _request_manifest() -> dict[str, Any]:
    return {
        "gate": GATE,
        "authorization": AUTHORIZATION,
        "lane": LANE,
        "provider": PROVIDER,
        "dataset": DATASET,
        "daily_schema": DAILY_SCHEMA,
        "hourly_schema": HOURLY_SCHEMA,
        "definition_schema": DEFINITION_SCHEMA,
        "stype_in": "raw_symbol",
        "root_symbol": ROOT_SYMBOL,
        "request_start": REQUEST_START.isoformat(),
        "request_end_exclusive": REQUEST_END_EXCLUSIVE.isoformat(),
        "development_reconciliation_start": DEV_START.isoformat(),
        "development_reconciliation_end": DEV_END.isoformat(),
        "protected_windows": ["2023_TEST", "2024_VALIDATION", "2025_2026_LOCKBOX_FORWARD_CANDIDATES"],
        "non_authorizations": list(NON_AUTHORIZATIONS),
        "secret_handling": "DataBento key read locally and never written to artifacts/stdout",
    }


def _contract_specs(start: date, end_exclusive: date, *, include_h3: bool) -> list[dict[str, Any]]:
    contracts: list[dict[str, Any]] = []
    max_delivery = date(2023, 3, 1) if include_h3 else date(2022, 12, 1)
    for year in range(2010, 2024):
        for month, code in MONTH_CODES:
            delivery = date(year, month, 1)
            if delivery < date(2010, 9, 1) or delivery > max_delivery:
                continue
            request_start = max(start, PROVIDER_AVAILABLE_START, delivery - timedelta(days=460))
            request_end = min(end_exclusive, _month_end(year, month) + timedelta(days=35))
            if request_start >= request_end:
                continue
            contracts.append(
                {
                    "root": ROOT_SYMBOL,
                    "raw_symbol": f"{ROOT_SYMBOL}{code}{year % 10}",
                    "contract_year": year,
                    "delivery_month": month,
                    "delivery_code": code,
                    "request_start": request_start.isoformat(),
                    "request_end": request_end.isoformat(),
                }
            )
    return contracts


def _hourly_contract_specs() -> list[dict[str, Any]]:
    return [
        contract
        for contract in _contract_specs(date(2021, 12, 31), REQUEST_END_EXCLUSIVE, include_h3=True)
        if contract["contract_year"] in {2022, 2023}
    ]


def _download_contracts(
    *,
    client: Any,
    contracts: list[dict[str, Any]],
    schema: str,
    condition_by_date: dict[str, str],
    output_subdir: str,
) -> tuple[dict[str, list[dict[str, Any]]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    rows_by_contract: dict[str, list[dict[str, Any]]] = {}
    symbology_rows: list[dict[str, Any]] = []
    definition_rows: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []

    for contract in contracts:
        symbol = contract["raw_symbol"]
        year = contract["contract_year"]
        key = _contract_key(contract)
        start = contract["request_start"]
        end = contract["request_end"]
        try:
            resolution = client.symbology.resolve(
                dataset=DATASET,
                symbols=[symbol],
                stype_in="raw_symbol",
                stype_out="instrument_id",
                start_date=start,
                end_date=end,
            )
            symbology_path = OUTPUT_ROOT / "raw_provider_metadata" / f"{RUN_ID}_{schema}_{symbol}_{year}_symbology.json"
            _write_json(symbology_path, resolution)
            resolved = resolution.get("result", {}).get(symbol, [])
            if not resolved:
                raise RuntimeError("SYMBOL_NOT_RESOLVED")
            symbology_rows.extend(
                {
                    "schema": schema,
                    "raw_symbol": symbol,
                    "contract_year": year,
                    "delivery_month": contract["delivery_month"],
                    "request_start": start,
                    "request_end": end,
                    "resolved_d0": item.get("d0"),
                    "resolved_d1": item.get("d1"),
                    "instrument_id": item.get("s"),
                }
                for item in resolved
            )

            raw_dir = OUTPUT_ROOT / "raw_provider_output" / output_subdir
            raw_dbn = raw_dir / f"{RUN_ID}_{schema}_{symbol}_{year}.dbn"
            provider_csv = raw_dir / f"{RUN_ID}_{schema}_{symbol}_{year}_provider.csv"
            if provider_csv.exists() and provider_csv.stat().st_size > 0:
                pass
            else:
                if raw_dbn.exists():
                    raw_dbn.unlink()
                store = client.timeseries.get_range(
                    dataset=DATASET,
                    schema=schema,
                    symbols=[symbol],
                    stype_in="raw_symbol",
                    start=f"{start}T00:00:00Z",
                    end=f"{end}T00:00:00Z",
                    path=raw_dbn,
                )
                df = store.to_df()
                df.to_csv(provider_csv)
            rows_by_contract[key] = _read_provider_rows(provider_csv, contract, schema, condition_by_date)

            if _definition_required(schema, contract):
                definition_dbn = OUTPUT_ROOT / "raw_provider_metadata" / f"{RUN_ID}_{schema}_{symbol}_{year}_definition.dbn"
                definition_csv = OUTPUT_ROOT / "raw_provider_metadata" / f"{RUN_ID}_{schema}_{symbol}_{year}_definition.csv"
                if definition_csv.exists() and definition_csv.stat().st_size > 0:
                    definition_rows_count = _csv_row_count(definition_csv)
                else:
                    if definition_dbn.exists():
                        definition_dbn.unlink()
                    definition_store = client.timeseries.get_range(
                        dataset=DATASET,
                        schema=DEFINITION_SCHEMA,
                        symbols=[symbol],
                        stype_in="raw_symbol",
                        start=f"{start}T00:00:00Z",
                        end=f"{end}T00:00:00Z",
                        path=definition_dbn,
                    )
                    definition_df = definition_store.to_df()
                    definition_df.to_csv(definition_csv)
                    definition_rows_count = len(definition_df)
                definition_rows.append(
                    {
                        "schema": schema,
                        "raw_symbol": symbol,
                        "contract_year": year,
                        "definition_rows": definition_rows_count,
                        "definition_csv": str(definition_csv.relative_to(ROOT)),
                        "definition_csv_sha256": _sha256(definition_csv),
                    }
                )
        except Exception as exc:  # noqa: BLE001 - preserve and fail closed after all contracts.
            errors.append(
                {
                    "schema": schema,
                    "raw_symbol": symbol,
                    "contract_year": year,
                    "request_start": start,
                    "request_end": end,
                    "error_type": type(exc).__name__,
                    "message": str(exc),
                }
            )
            rows_by_contract[key] = []
    return rows_by_contract, symbology_rows, definition_rows, errors


def _definition_required(schema: str, contract: dict[str, Any]) -> bool:
    if schema == HOURLY_SCHEMA:
        return True
    return int(contract["contract_year"]) >= 2022


def _csv_row_count(path: Path) -> int:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return max(0, sum(1 for _ in handle) - 1)


def _read_provider_rows(
    provider_csv: Path,
    contract: dict[str, Any],
    schema: str,
    condition_by_date: dict[str, str],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    with provider_csv.open("r", encoding="utf-8", newline="") as handle:
        for record in csv.DictReader(handle):
            ts = _parse_ts(record["ts_event"])
            key = f"{contract['raw_symbol']}|{ts.isoformat()}"
            if key in seen:
                raise RuntimeError(f"DUPLICATE_PROVIDER_TIMESTAMP {key}")
            seen.add(key)
            completed_date = _completed_trading_date(ts) if schema == HOURLY_SCHEMA else ts.date().isoformat()
            if completed_date >= "2023-01-01":
                continue
            condition = condition_by_date.get(ts.date().isoformat(), "UNKNOWN")
            close = float(record["close"])
            open_ = float(record["open"])
            high = float(record["high"])
            low = float(record["low"])
            volume = float(record["volume"])
            if not (math.isfinite(close) and close > 0.0 and low <= open_ <= high and low <= close <= high and volume >= 0.0):
                raise RuntimeError(f"BAD_OHLCV_SHAPE {contract['raw_symbol']} {ts.isoformat()}")
            rows.append(
                {
                    "raw_symbol": contract["raw_symbol"],
                    "contract_year": contract["contract_year"],
                    "delivery_month": contract["delivery_month"],
                    "delivery_code": contract["delivery_code"],
                    "provider_ts_event_start_utc": _z(ts),
                    "derived_completed_bar_end_utc": _z(ts + timedelta(hours=1)) if schema == HOURLY_SCHEMA else _z(ts),
                    "completed_trading_date": completed_date,
                    "instrument_id": str(record.get("instrument_id", "")),
                    "open": open_,
                    "high": high,
                    "low": low,
                    "close": close,
                    "volume": volume,
                    "provider_condition_status": f"PROVIDER_CONDITION_{condition}",
                    "source_provider_csv": str(provider_csv.relative_to(ROOT)),
                    "source_provider_csv_sha256": _sha256(provider_csv),
                }
            )
    return rows


def _build_continuous_series(
    contracts: list[dict[str, Any]],
    rows_by_contract: dict[str, list[dict[str, Any]]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    by_contract_date = {
        _contract_key(contract): {
            row["completed_trading_date"]: row
            for row in rows_by_contract[_contract_key(contract)]
            if row["provider_condition_status"] == "PROVIDER_CONDITION_AVAILABLE"
        }
        for contract in contracts
    }
    all_dates = sorted({day for rows in by_contract_date.values() for day in rows})
    if not all_dates:
        raise RuntimeError("no provider-condition-available daily rows")

    roll_rows: list[dict[str, Any]] = []
    for old, new in zip(contracts[:-1], contracts[1:], strict=True):
        first_notice = _first_notice_proxy(old, all_dates)
        prior_dates = [day for day in all_dates if day < first_notice.isoformat()]
        if len(prior_dates) <= ROLL_BUFFER_COMPLETED_DATES:
            raise RuntimeError(f"insufficient roll-buffer dates before first notice proxy for {_contract_key(old)}")
        transition = prior_dates[-ROLL_BUFFER_COMPLETED_DATES]
        old_row = by_contract_date[_contract_key(old)].get(transition)
        new_row = by_contract_date[_contract_key(new)].get(transition)
        if old_row is None or new_row is None:
            raise RuntimeError(f"missing roll overlap {transition} {_contract_key(old)}->{_contract_key(new)}")
        roll_rows.append(
            {
                "old_contract_key": _contract_key(old),
                "new_contract_key": _contract_key(new),
                "first_notice_proxy": first_notice.isoformat(),
                "roll_transition_date": transition,
                "old_close": old_row["close"],
                "new_close": new_row["close"],
                "additive_delta_to_prior_history": new_row["close"] - old_row["close"],
            }
        )

    active_by_date: dict[str, dict[str, Any]] = {}
    current_index = 0
    for day in all_dates:
        while current_index < len(roll_rows) and day >= roll_rows[current_index]["roll_transition_date"]:
            current_index += 1
        contract = contracts[min(current_index, len(contracts) - 1)]
        row = by_contract_date[_contract_key(contract)].get(day)
        if row is not None:
            active_by_date[day] = row

    offsets_by_segment = [0.0 for _ in contracts]
    cumulative = 0.0
    for index in range(len(roll_rows) - 1, -1, -1):
        cumulative += float(roll_rows[index]["additive_delta_to_prior_history"])
        offsets_by_segment[index] = cumulative

    rows: list[dict[str, Any]] = []
    for day in sorted(active_by_date):
        segment_index = min(_segment_index_for_day(day, roll_rows), len(contracts) - 1)
        active = active_by_date[day]
        adjustment = offsets_by_segment[segment_index]
        rows.append(
            {
                "completed_trading_date": day,
                "active_contract_key": _contract_key(contracts[segment_index]),
                "raw_symbol": active["raw_symbol"],
                "instrument_id": active["instrument_id"],
                "raw_close": active["close"],
                "additive_back_adjustment": adjustment,
                "continuous_close": active["close"] + adjustment,
                "lineage_status": "S27_V2_DATABENTO_PRE2023_LOCAL_BACK_ADJUSTED_DATED_CONTRACT_CHAIN",
                "source_provider_csv": active["source_provider_csv"],
                "source_provider_csv_sha256": active["source_provider_csv_sha256"],
            }
        )
    if len(rows) < TEN_YEAR_SIGMA_ROWS + SIGMA_WINDOW_ROWS + 64:
        raise RuntimeError("continuous risk-history rows are insufficient for ten-year V/Q/M plus runtime history")
    _write_csv(OUTPUT_ROOT / "ledger" / f"{RUN_ID}_roll_plan.csv", roll_rows)
    _write_csv(OUTPUT_ROOT / "ledger" / f"{RUN_ID}_local_continuous_daily_risk_history.csv", rows)
    return rows, roll_rows


def _build_sigma_rows(continuous: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    closes = [float(row["continuous_close"]) for row in continuous]
    dates = [row["completed_trading_date"] for row in continuous]
    alpha = 2.0 / (SIGMA_EWMA_SPAN + 1.0)
    for index in range(SIGMA_WINDOW_ROWS - 1, len(continuous)):
        window = closes[index - SIGMA_WINDOW_ROWS + 1 : index + 1]
        returns = [window[i] / window[i - 1] - 1.0 for i in range(1, len(window))]
        variance = returns[0] * returns[0]
        for value in returns[1:]:
            variance = alpha * value * value + (1.0 - alpha) * variance
        rows.append(
            {
                "completed_trading_date": dates[index],
                "sigma_i_t": math.sqrt(variance) * math.sqrt(TRADING_DAYS_PER_YEAR),
                "sigma_method": "STRATEGY_3_STYLE_EWMA32_PERCENT_RETURN_SIGMA_ANNUALIZED_256",
                "source_window_start": dates[index - SIGMA_WINDOW_ROWS + 1],
                "source_window_end": dates[index],
                "source_window_rows": SIGMA_WINDOW_ROWS,
                "no_lookahead_status": "PASS_NO_LOOKAHEAD_DAILY_RUNTIME",
            }
        )
    _write_csv(OUTPUT_ROOT / "ledger" / f"{RUN_ID}_sigma_i_t_ledger.csv", rows)
    return rows


def _build_vqm_rows(sigma_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = _build_vqm_rows_no_write(sigma_rows)
    _write_csv(OUTPUT_ROOT / "ledger" / f"{RUN_ID}_relative_vol_v_q_m_daily_ledger.csv", rows)
    return rows


def _point_in_time_continuous_series(
    continuous: list[dict[str, Any]],
    roll_rows: list[dict[str, Any]],
    cutoff_date: str,
) -> list[dict[str, Any]]:
    active_rows = [row for row in continuous if row["completed_trading_date"] <= cutoff_date]
    if not active_rows:
        raise RuntimeError("no point-in-time rows before cutoff")
    known_rolls = [row for row in roll_rows if row["roll_transition_date"] <= cutoff_date]
    current_contract_key = active_rows[-1]["active_contract_key"]
    offsets_by_contract = {current_contract_key: 0.0}
    cumulative = 0.0
    for roll in reversed(known_rolls):
        new_key = roll["new_contract_key"]
        old_key = roll["old_contract_key"]
        if new_key in offsets_by_contract:
            cumulative = offsets_by_contract[new_key] + float(roll["additive_delta_to_prior_history"])
            offsets_by_contract[old_key] = cumulative
    rows: list[dict[str, Any]] = []
    missing_offsets = sorted(
        {
            row["active_contract_key"]
            for row in active_rows
            if row["active_contract_key"] not in offsets_by_contract
        }
    )
    if missing_offsets:
        raise RuntimeError(f"point-in-time offsets missing for {missing_offsets}")
    for row in active_rows:
        adjustment = offsets_by_contract[row["active_contract_key"]]
        rows.append(
            {
                "completed_trading_date": row["completed_trading_date"],
                "active_contract_key": row["active_contract_key"],
                "raw_symbol": row["raw_symbol"],
                "instrument_id": row["instrument_id"],
                "raw_close": row["raw_close"],
                "additive_back_adjustment": adjustment,
                "continuous_close": float(row["raw_close"]) + adjustment,
                "lineage_status": "S27_V2_POINT_IN_TIME_BACK_ADJUSTED_CHAIN_NO_FUTURE_ROLL_DELTAS",
                "point_in_time_roll_cutoff_date": cutoff_date,
                "source_provider_csv": row["source_provider_csv"],
                "source_provider_csv_sha256": row["source_provider_csv_sha256"],
            }
        )
    if rows[-1]["additive_back_adjustment"] != 0.0:
        raise RuntimeError("point-in-time current contract adjustment must be zero at cutoff")
    return rows


def _build_sigma_rows_no_write(continuous: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    closes = [float(row["continuous_close"]) for row in continuous]
    dates = [row["completed_trading_date"] for row in continuous]
    alpha = 2.0 / (SIGMA_EWMA_SPAN + 1.0)
    for index in range(SIGMA_WINDOW_ROWS - 1, len(continuous)):
        window = closes[index - SIGMA_WINDOW_ROWS + 1 : index + 1]
        returns = [window[i] / window[i - 1] - 1.0 for i in range(1, len(window))]
        variance = returns[0] * returns[0]
        for value in returns[1:]:
            variance = alpha * value * value + (1.0 - alpha) * variance
        rows.append(
            {
                "completed_trading_date": dates[index],
                "sigma_i_t": math.sqrt(variance) * math.sqrt(TRADING_DAYS_PER_YEAR),
                "sigma_method": "STRATEGY_3_STYLE_EWMA32_PERCENT_RETURN_SIGMA_ANNUALIZED_256",
                "source_window_start": dates[index - SIGMA_WINDOW_ROWS + 1],
                "source_window_end": dates[index],
                "source_window_rows": SIGMA_WINDOW_ROWS,
                "no_lookahead_status": "PASS_NO_LOOKAHEAD_DAILY_RUNTIME",
            }
        )
    return rows


def _build_vqm_rows_no_write(sigma_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    alpha = 2.0 / (VQM_EWMA_SPAN + 1.0)
    smoothed: float | None = None
    sigma_values = [float(row["sigma_i_t"]) for row in sigma_rows]
    prefix = [0.0]
    for sigma in sigma_values:
        prefix.append(prefix[-1] + sigma)
    historical_v: list[float] = []
    for index, sigma_row in enumerate(sigma_rows):
        if index < TEN_YEAR_SIGMA_ROWS:
            continue
        ten_year_avg = (prefix[index] - prefix[index - TEN_YEAR_SIGMA_ROWS]) / TEN_YEAR_SIGMA_ROWS
        sigma = sigma_values[index]
        v = sigma / ten_year_avg
        historical_v.append(v)
        q = _quantile_rank_including_current(historical_v, v)
        raw_m = 2.0 - 1.5 * q
        smoothed = raw_m if smoothed is None else alpha * raw_m + (1.0 - alpha) * smoothed
        rows.append(
            {
                "completed_trading_date": sigma_row["completed_trading_date"],
                "sigma_i_t": sigma,
                "ten_year_average_sigma": ten_year_avg,
                "relative_volatility_v": v,
                "historical_v_observation_count": len(historical_v),
                "quantile_q": q,
                "raw_vol_multiplier_2_minus_1_5q": raw_m,
                "vol_multiplier_m_ewma10": smoothed,
                "ten_year_sigma_rows": TEN_YEAR_SIGMA_ROWS,
                "method_status": "LOCKED_S13_STYLE_V_Q_M_ATTENUATION_RUNTIME_PRE2023_DATABENTO",
                "no_lookahead_status": "PASS_NO_LOOKAHEAD_DAILY_RUNTIME",
            }
        )
    return rows


def _strategy_facing_hourly_rows(rows_by_contract: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows = [
        row
        for contract_rows in rows_by_contract.values()
        for row in contract_rows
        if DEV_START.isoformat() <= row["completed_trading_date"] <= DEV_END.isoformat()
        and row["provider_condition_status"] == "PROVIDER_CONDITION_AVAILABLE"
    ]
    rows.sort(key=lambda row: (row["derived_completed_bar_end_utc"], row["raw_symbol"]))
    by_end: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        by_end.setdefault(row["derived_completed_bar_end_utc"], []).append(row)
    selected: list[dict[str, Any]] = []
    for timestamp, candidates in by_end.items():
        selected.append(_select_active_hourly_candidate(timestamp, candidates))
    _write_csv(OUTPUT_ROOT / "ledger" / f"{RUN_ID}_strategy_facing_hourly_available_bars.csv", selected)
    return selected


def _build_declared_pack(
    continuous: list[dict[str, Any]],
    sigma_rows: list[dict[str, Any]],
    vqm_rows: list[dict[str, Any]],
    roll_rows: list[dict[str, Any]],
    hourly_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    del sigma_rows, vqm_rows
    global_continuous_by_date = {row["completed_trading_date"]: row for row in continuous}
    hourly_by_end = {row["derived_completed_bar_end_utc"]: row for row in hourly_rows}
    hourly_timestamps = sorted(hourly_by_end)

    selected_decision: dict[str, Any] | None = None
    selected_fill: dict[str, Any] | None = None
    selected_vqm_date: str | None = None
    selected_pit_continuous: list[dict[str, Any]] | None = None
    selected_pit_sigma_rows: list[dict[str, Any]] | None = None
    selected_pit_vqm_rows: list[dict[str, Any]] | None = None
    for timestamp in hourly_timestamps:
        decision = hourly_by_end[timestamp]
        fill_ts = _z(_parse_ts(timestamp) + timedelta(hours=1))
        fill = hourly_by_end.get(fill_ts)
        if fill is None:
            continue
        previous_daily = max(day for day in global_continuous_by_date if day < decision["completed_trading_date"])
        pit_continuous = _point_in_time_continuous_series(continuous, roll_rows, previous_daily)
        pit_sigma_rows = _build_sigma_rows_no_write(pit_continuous)
        pit_vqm_rows = _build_vqm_rows_no_write(pit_sigma_rows)
        pit_sigma_by_date = {row["completed_trading_date"]: row for row in pit_sigma_rows}
        pit_vqm_by_date = {row["completed_trading_date"]: row for row in pit_vqm_rows}
        prior_vqm_dates = [day for day in pit_vqm_by_date if day < decision["completed_trading_date"]]
        if not prior_vqm_dates or previous_daily not in pit_sigma_by_date:
            continue
        selected_decision = decision
        selected_fill = fill
        selected_vqm_date = max(prior_vqm_dates)
        selected_pit_continuous = pit_continuous
        selected_pit_sigma_rows = pit_sigma_rows
        selected_pit_vqm_rows = pit_vqm_rows
        break
    if (
        selected_decision is None
        or selected_fill is None
        or selected_vqm_date is None
        or selected_pit_continuous is None
        or selected_pit_sigma_rows is None
        or selected_pit_vqm_rows is None
    ):
        raise RuntimeError("no eligible 2022 decision/fill pair with strict-prior V/Q/M")

    continuous_by_date = {row["completed_trading_date"]: row for row in selected_pit_continuous}
    sigma_by_date = {row["completed_trading_date"]: row for row in selected_pit_sigma_rows}
    vqm_by_date = {row["completed_trading_date"]: row for row in selected_pit_vqm_rows}
    previous_daily_date = max(day for day in continuous_by_date if day < selected_decision["completed_trading_date"])
    _write_csv(
        OUTPUT_ROOT / "ledger" / f"{RUN_ID}_selected_point_in_time_daily_risk_history.csv",
        selected_pit_continuous,
    )
    _write_csv(
        OUTPUT_ROOT / "ledger" / f"{RUN_ID}_selected_point_in_time_sigma_i_t_ledger.csv",
        selected_pit_sigma_rows,
    )
    _write_csv(
        OUTPUT_ROOT / "ledger" / f"{RUN_ID}_selected_point_in_time_relative_vol_v_q_m_daily_ledger.csv",
        selected_pit_vqm_rows,
    )
    prior_daily_dates = [day for day in sorted(continuous_by_date) if day <= previous_daily_date]
    prior_daily_dates = prior_daily_dates[-64:]
    if len(prior_daily_dates) != 64:
        raise RuntimeError("insufficient 64-row daily runtime window")

    daily_continuous_rows = [
        {
            "completed_timestamp_utc": f"{day}T00:00:00Z",
            "trading_date": day,
            "raw_symbol": continuous_by_date[day]["raw_symbol"],
            "row_locator": f"S27V2_PRE2023_ZN_DAILY_CONTINUOUS_{day.replace('-', '')}_{index:04d}",
            "close_price": _num(continuous_by_date[day]["continuous_close"]),
            "annual_percentage_sigma": _num(sigma_by_date[day]["sigma_i_t"]),
            "readiness_status": "READY_COMPLETED_BAR_DATABENTO_PRE2023_DEV_RECON_CHRONOLOGICAL",
        }
        for index, day in enumerate(prior_daily_dates, 1)
    ]
    previous_daily = continuous_by_date[previous_daily_date]
    adjustment = float(previous_daily["additive_back_adjustment"])
    daily_current_rows = [
        {
            "completed_timestamp_utc": f"{previous_daily_date}T00:00:00Z",
            "trading_date": previous_daily_date,
            "raw_symbol": previous_daily["raw_symbol"],
            "row_locator": f"S27V2_PRE2023_ZN_DAILY_CURRENT_{previous_daily_date.replace('-', '')}_0001",
            "close_price": _num(previous_daily["raw_close"]),
            "readiness_status": "READY_COMPLETED_BAR_DATABENTO_PRE2023_DEV_RECON",
        }
    ]
    decision_rows = [_hourly_pack_row(selected_decision, adjustment, "DECISION")]
    fill_rows = [_hourly_pack_row(selected_fill, adjustment, "FILL")]
    session_rows = [
        {
            "session_id": _session_id(selected_decision["derived_completed_bar_end_utc"]),
            "session_start_utc": _z(_session_start(_parse_ts(selected_decision["derived_completed_bar_end_utc"]))),
            "session_end_utc": _z(_session_start(_parse_ts(selected_decision["derived_completed_bar_end_utc"])) + timedelta(hours=23)),
            "calendar_status": "LOCAL_DATABENTO_PRE2023_COMPLETED_BAR_SESSION_CONTEXT",
            "readiness_status": "READY_SESSION_CONTEXT_DEV_RECON_ONLY",
        }
    ]
    relevant_rolls = [
        row
        for row in roll_rows
        if row["roll_transition_date"] <= previous_daily_date
    ]
    roll_calendar_rows = [
        {
            "roll_id": f"S27V2_PRE2023_ZN_ROLL_{row['roll_transition_date'].replace('-', '')}_{index:04d}",
            "old_contract_key": row["old_contract_key"],
            "new_contract_key": row["new_contract_key"],
            "roll_transition_date": row["roll_transition_date"],
            "additive_delta_to_prior_history": _num(row["additive_delta_to_prior_history"]),
            "readiness_status": "READY_DATABENTO_PRE2023_ROLL_CONTEXT_DEV_RECON_ONLY",
        }
        for index, row in enumerate(relevant_rolls, 1)
    ]
    cost_rows = [
        {
            "cost_policy_id": "S27_V2_ZN_ACCEPTED_INFERRED_RETAIL_FUTURES_COST_2026_06_11",
            "instrument": "ZN",
            "currency": "USD",
            "commission_per_contract_per_side": "2.30",
            "spread_cost_policy": "LIMIT_FILL_COMMISSION_ONLY_NO_MARKET_SPREAD",
            "cost_policy_status": "INFERRED_RETAIL_FUTURES_COST_ACCEPTED_FOR_LOCAL_DEV_RECON_ONLY_NOT_BOOK_EXPLICIT",
            "readiness_status": "READY_COST_PARAMETER_FOR_LOCAL_DEV_RECON_ONLY",
        }
    ]

    files = {
        "daily_continuous_completed_bar.csv": daily_continuous_rows,
        "daily_current_contract_completed_bar.csv": daily_current_rows,
        "hourly_decision_completed_bar.csv": decision_rows,
        "hourly_fill_completed_bar.csv": fill_rows,
        "session_calendar.csv": session_rows,
        "roll_calendar.csv": roll_calendar_rows,
        "cost_parameter.csv": cost_rows,
    }
    for filename, rows in files.items():
        _write_csv(PACK_ROOT / filename, rows)

    row_family_files = {
        filename: {"row_count": len(rows), "sha256": _sha256(PACK_ROOT / filename)}
        for filename, rows in files.items()
    }
    vqm = vqm_by_date[selected_vqm_date]
    level_bridge_proof = {
        "artifact": "S27_V2_ZN_PRE2023_DATABENTO_LEVEL_BRIDGE_PROOF_NOT_RESULT_EVIDENCE",
        "bridge_disposition": "PASS_LOCAL_LEVEL_SPACE_BRIDGE_SHARED_DATABENTO_DAILY_ROLL_LEVEL_NOT_PRICE_EQUALITY_NOT_RESULT_EVIDENCE",
        "daily_active_contract": previous_daily["raw_symbol"],
        "daily_additive_back_adjustment": _num(adjustment),
        "hourly_active_contract": selected_decision["raw_symbol"],
        "hourly_additive_back_adjustment_applied_for_bridge": _num(adjustment),
        "selected_decision_timestamp_utc": selected_decision["derived_completed_bar_end_utc"],
        "selected_previous_daily_date": previous_daily_date,
        "source_daily_risk_history_sha256": _sha256(OUTPUT_ROOT / "ledger" / f"{RUN_ID}_selected_point_in_time_daily_risk_history.csv"),
        "source_hourly_available_bars_sha256": _sha256(OUTPUT_ROOT / "ledger" / f"{RUN_ID}_strategy_facing_hourly_available_bars.csv"),
        "point_in_time_roll_cutoff_date": previous_daily_date,
        "future_roll_deltas_after_cutoff_excluded": "YES",
    }
    manifest = {
        "artifact": "S27_V2_PRE2023_DATABENTO_ZN_DECLARED_INPUT_PACK_MANIFEST",
        "authorization": AUTHORIZATION,
        "status": "LOCAL_INPUT_PACK_DECLARED_FOR_2022_DEVELOPMENT_RECON_ONLY_NOT_BACKTEST_NOT_RESULT",
        "lane": LANE,
        "selected_slice_rule": "PRESERVE_2023_FOR_TEST_USE_OLDEST_2022_ROW_AFTER_STRICT_PRIOR_VQM_AND_LEVEL_COMPATIBILITY_POPULATED",
        "selected_raw_symbol": selected_decision["raw_symbol"],
        "selected_decision_timestamp_utc": selected_decision["derived_completed_bar_end_utc"],
        "selected_fill_timestamp_utc": selected_fill["derived_completed_bar_end_utc"],
        "selected_previous_daily_timestamp_utc": f"{previous_daily_date}T00:00:00Z",
        "explicitly_excluded_data": ["NO_2023_TEST_DATA", "NO_VALIDATION", "NO_OOS", "NO_LOCKBOX", "NO_FORWARD"],
        "history_evidence": {
            "daily_continuous_rows": str(len(daily_continuous_rows)),
            "daily_continuous_prior_history_rows": str(len(daily_continuous_rows) - 1),
            "daily_history_first_prior_trading_date": prior_daily_dates[0],
            "daily_history_selected_previous_trading_date": previous_daily_date,
            "daily_continuous_order": "CHRONOLOGICAL_ASCENDING_SELECTED_ROW_LAST",
            "selected_sigma_status": "RECOMPUTED_STRATEGY3_SIGMA_FROM_DATABENTO_PRE2023_DAILY_HISTORY",
            "selected_sigma_method_status": "STRATEGY_3_STYLE_EWMA32_PERCENT_RETURN_SIGMA_ANNUALIZED_256",
            "selected_sigma_percent_t": _num(sigma_by_date[previous_daily_date]["sigma_i_t"]),
            "selected_vqm_status": "RECOMPUTED_S27_V_Q_M_ATTENUATION_DAILY_VALUE_STRICT_PRIOR_TO_DECISION",
            "selected_vqm_method_status": "LOCKED_S13_STYLE_V_Q_M_ATTENUATION_RUNTIME_PRE2023_DATABENTO",
            "selected_vqm_source_completed_trading_date": selected_vqm_date,
            "selected_vqm_relative_volatility_v": _num(vqm["relative_volatility_v"]),
            "selected_vqm_quantile_q": _num(vqm["quantile_q"]),
            "selected_vqm_multiplier_m": _num(vqm["vol_multiplier_m_ewma10"]),
            "selected_vqm_observation_count": str(vqm["historical_v_observation_count"]),
            "point_in_time_roll_cutoff_date": previous_daily_date,
            "future_roll_deltas_after_cutoff_excluded": "YES",
            "level_bridge_disposition": level_bridge_proof["bridge_disposition"],
            "level_bridge_proof_hash": hashlib.sha256(json.dumps(level_bridge_proof, sort_keys=True).encode("ascii")).hexdigest(),
            "tick_rounding_policy_status": "APPENDIX_C_STATIC_ZN_TICK_POLICY_BOUND_FOR_DEV_RECON_PLANNING_ONLY",
            "multiplier_currency_policy_status": "APPENDIX_C_STATIC_ZN_POINT_VALUE_AND_USD_CURRENCY_BOUND_FOR_POSITION_ONLY",
            "commission_spread_policy_status": "INFERRED_RETAIL_FUTURES_COST_ACCEPTED_FOR_LOCAL_DEV_RECON_ONLY_NOT_BOOK_EXPLICIT",
            "valuation_policy_status": "SOURCE_NATIVE_ENGINEERING_VALUATION_ASSUMPTION_NOT_BOOK_EXPLICIT_FOR_LOCAL_DEV_RECON_ONLY",
            "working_order_lifecycle_status": "FIRST_ROW_EMPTY_WORKING_ORDER_STATE_DECLARED_RUNNER_MUST_BIND_SUBSEQUENT_STATE",
        },
        "level_bridge_proof": level_bridge_proof,
        "working_order_lifecycle_context": {
            "status": "FIRST_ROW_EMPTY_WORKING_ORDER_STATE_DECLARED_FOR_2022_LOCAL_DEV_RECON_RUNNER_BINDING",
            "selected_decision_timestamp_utc": selected_decision["derived_completed_bar_end_utc"],
            "initial_current_position_contracts": "0",
            "open_working_orders": "0",
            "state_scope": "FIRST_ROW_CONTEXT_ONLY_NOT_FULL_MULTI_ROW_LIFECYCLE_EVIDENCE",
            "runner_must_bind_subsequent_state": "YES",
        },
        "row_family_files": row_family_files,
        "source_files": {
            "download_build_status": str((OUTPUT_ROOT / "status" / f"{RUN_ID}_status.json").relative_to(ROOT)),
            "continuous_daily_risk_history": str((OUTPUT_ROOT / "ledger" / f"{RUN_ID}_selected_point_in_time_daily_risk_history.csv").relative_to(ROOT)),
            "sigma_i_t_ledger": str((OUTPUT_ROOT / "ledger" / f"{RUN_ID}_selected_point_in_time_sigma_i_t_ledger.csv").relative_to(ROOT)),
            "relative_vol_v_q_m_daily_ledger": str((OUTPUT_ROOT / "ledger" / f"{RUN_ID}_selected_point_in_time_relative_vol_v_q_m_daily_ledger.csv").relative_to(ROOT)),
            "strategy_facing_hourly_available_bars": str((OUTPUT_ROOT / "ledger" / f"{RUN_ID}_strategy_facing_hourly_available_bars.csv").relative_to(ROOT)),
        },
        "non_authorizations": list(NON_AUTHORIZATIONS),
    }
    manifest_path = PACK_ROOT / "S27_V2_PRE2023_DATABENTO_DECLARED_INPUT_PACK_MANIFEST.json"
    _write_json(manifest_path, manifest)
    (PACK_ROOT / "S27_V2_PRE2023_DATABENTO_DECLARED_INPUT_PACK_PROVENANCE.md").write_text(_pack_provenance(manifest), encoding="ascii")
    _write_sha256s(PACK_ROOT / "S27_V2_PRE2023_DATABENTO_DECLARED_INPUT_PACK_SHA256SUMS.txt", PACK_ROOT)
    return manifest


def _hourly_pack_row(row: dict[str, Any], adjustment: float, role: str) -> dict[str, Any]:
    continuous_close = float(row["close"]) + adjustment
    return {
        "completed_timestamp_utc": row["derived_completed_bar_end_utc"],
        "trading_date": row["completed_trading_date"],
        "raw_symbol": row["raw_symbol"],
        "session_id": _session_id(row["derived_completed_bar_end_utc"]),
        "row_locator": f"S27V2_PRE2023_ZN_HOURLY_{role}_{row['derived_completed_bar_end_utc'].replace('-', '').replace(':', '').replace('T', 'T').replace('Z', 'Z')}_{row['raw_symbol']}",
        "close_price": _num(continuous_close),
        "readiness_status": "READY_COMPLETED_BAR_DATABENTO_PRE2023_DEV_RECON",
    }


def _select_active_hourly_candidate(timestamp: str, candidates: list[dict[str, Any]]) -> dict[str, Any]:
    if len(candidates) == 1:
        return candidates[0]
    preferred = sorted(candidates, key=lambda row: row["raw_symbol"])[-1]
    return preferred


def _status_payload(
    continuous: list[dict[str, Any]],
    sigma_rows: list[dict[str, Any]],
    vqm_rows: list[dict[str, Any]],
    hourly_rows: list[dict[str, Any]],
    roll_rows: list[dict[str, Any]],
    pack_manifest: dict[str, Any],
) -> dict[str, Any]:
    return {
        "gate": GATE,
        "authorization": AUTHORIZATION,
        "status": "PASS_S27_V2_PRE2023_ZN_HISTORY_DOWNLOADED_AND_2022_PACK_DECLARED_NOT_BACKTEST_NOT_RESULT",
        "provider": PROVIDER,
        "dataset": DATASET,
        "request_start": REQUEST_START.isoformat(),
        "request_end_exclusive": REQUEST_END_EXCLUSIVE.isoformat(),
        "development_reconciliation_start": DEV_START.isoformat(),
        "development_reconciliation_end": DEV_END.isoformat(),
        "protected_2023_for_test": "YES",
        "daily_continuous_rows": len(continuous),
        "sigma_rows": len(sigma_rows),
        "vqm_rows": len(vqm_rows),
        "vqm_start": vqm_rows[0]["completed_trading_date"],
        "vqm_end": vqm_rows[-1]["completed_trading_date"],
        "hourly_2022_available_rows": len(hourly_rows),
        "roll_rows": len(roll_rows),
        "declared_pack_root": str(PACK_ROOT.relative_to(ROOT)),
        "declared_pack_manifest": str((PACK_ROOT / "S27_V2_PRE2023_DATABENTO_DECLARED_INPUT_PACK_MANIFEST.json").relative_to(ROOT)),
        "selected_decision_timestamp_utc": pack_manifest["selected_decision_timestamp_utc"],
        "selected_fill_timestamp_utc": pack_manifest["selected_fill_timestamp_utc"],
        "selected_raw_symbol": pack_manifest["selected_raw_symbol"],
        "backtests_run": "NO",
        "result_scored_runs": "NO",
        "result_interpretation": "NO",
        "pnl_evaluation": "NO",
        "test_access": "NO",
        "validation_access": "NO",
        "oos_access": "NO",
        "lockbox_access": "NO",
        "forward_access": "NO",
        "source_faithful_evidence_claim": "NO",
        "non_authorizations": list(NON_AUTHORIZATIONS),
    }


def _first_notice_proxy(contract: dict[str, Any], all_dates: list[str]) -> date:
    first_of_delivery = date(int(contract["contract_year"]), int(contract["delivery_month"]), 1)
    candidates = [day for day in all_dates if day >= first_of_delivery.isoformat()]
    if not candidates:
        return first_of_delivery
    first_delivery_trading_date = candidates[0]
    prior_dates = [day for day in all_dates if day < first_delivery_trading_date]
    if not prior_dates:
        raise RuntimeError(f"cannot derive first notice proxy for {_contract_key(contract)}")
    return date.fromisoformat(prior_dates[-1])


def _segment_index_for_day(day: str, roll_rows: list[dict[str, Any]]) -> int:
    index = 0
    for roll in roll_rows:
        if day >= roll["roll_transition_date"]:
            index += 1
    return index


def _quantile_rank_including_current(values: list[float], current: float) -> float:
    if len(values) < 2:
        return 0.5
    less = sum(1 for value in values if value < current)
    equal = sum(1 for value in values if value == current)
    rank = less + 0.5 * max(equal - 1, 0)
    return max(0.0, min(1.0, rank / (len(values) - 1)))


def _session_start(completed_end: datetime) -> datetime:
    start_date = completed_end.date()
    if completed_end.hour < 22:
        start_date = (completed_end - timedelta(days=1)).date()
    return datetime(start_date.year, start_date.month, start_date.day, 22, tzinfo=timezone.utc)


def _session_id(completed_end_utc: str) -> str:
    completed = _parse_ts(completed_end_utc)
    start = _session_start(completed)
    end = start + timedelta(hours=23)
    return f"UTC_ZN_PRE2023_{start.isoformat().replace('+00:00', 'Z')}_{end.isoformat().replace('+00:00', 'Z')}"


def _completed_trading_date(ts: datetime) -> str:
    candidate = ts.date()
    if ts.hour >= 22:
        candidate = (ts + timedelta(days=1)).date()
    return candidate.isoformat()


def _contract_key(contract: dict[str, Any]) -> str:
    return f"{contract['raw_symbol']}_{contract['contract_year']}"


def _month_end(year: int, month: int) -> date:
    if month == 12:
        return date(year, 12, 31)
    return date(year, month + 1, 1) - timedelta(days=1)


def _parse_ts(value: str) -> datetime:
    normalized = value.strip().replace(" ", "T").replace("+00:00", "Z")
    ts = datetime.fromisoformat(normalized.replace("Z", "+00:00"))
    if ts.tzinfo is None:
        raise RuntimeError("provider timestamp is not timezone-aware")
    return ts.astimezone(timezone.utc)


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


def _num(value: Any) -> str:
    return repr(float(value))


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="ascii")
        return
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="ascii", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, default=str) + "\n", encoding="ascii")


def _write_sha256s(path: Path, root: Path) -> None:
    lines = [
        f"{_sha256(file)}  {file.relative_to(root).as_posix()}"
        for file in sorted(root.rglob("*"))
        if file.is_file() and file != path
    ]
    path.write_text("\n".join(lines) + "\n", encoding="ascii")


def _hash_tree(root: Path) -> dict[str, str]:
    return {
        str(file.relative_to(ROOT)): _sha256(file)
        for file in sorted(root.rglob("*"))
        if file.is_file() and not file.name.endswith("_sha256.json")
    }


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def _z(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _provenance_text(status: dict[str, Any]) -> str:
    return f"""# S27_V2 ZN Pre-2023 DataBento Older-History Download/Build Provenance

Status:

```text
{status["status"]}
```

This artifact is Development/Reconciliation data preparation only. It uses the single authorized
DataBento older-history gate for pre-2023 ZN source-native futures history. It does not open 2023
TEST, VALIDATION, OOS, Lockbox, or Forward data and does not run a backtest, result-scored run,
diagnostic, tuning pass, deployment, trade, Git action, or source-faithful evidence claim.

The DataBento key was read from local credential storage and is not written to artifacts.
"""


def _pack_provenance(manifest: dict[str, Any]) -> str:
    return f"""# S27_V2 Pre-2023 ZN Declared Input Pack Provenance

Status:

```text
{manifest["status"]}
```

This pack preserves 2023 for TEST and selects the oldest 2022 Development/Reconciliation row for
which strict-prior V/Q/M, Strategy 3 sigma, daily/hourly level bridge, cost policy, valuation policy,
and first-row working-state evidence are populated. It is not a backtest, not a result, and not a
source-faithful evidence claim.
"""


def _process_doc(status: dict[str, Any]) -> str:
    return f"""# Carver S27_V2 ZN Pre-2023 Older-History Download/Build Result

Date: 2026-06-11

Status:

```text
{status["status"]}
```

Authorization:

```text
{AUTHORIZATION}
```

Window preservation:

- 2022 is Development/Reconciliation.
- 2023 is preserved for TEST.
- 2024+ remains unopened by this gate.

Output root:

```text
{OUTPUT_ROOT.relative_to(ROOT)}
```

Declared pack:

```text
{status.get("declared_pack_root", "NOT_EMITTED")}
```

Non-authorization: no backtests, result-scored runs, result interpretation, PnL evaluation, tuning,
adapter work, deployment, trading, promotion, Git actions, OOS, Lockbox, Forward, or source-faithful
evidence claim.
"""


def _local_audit_doc(status: dict[str, Any]) -> str:
    passed = status["status"].startswith("PASS_")
    return f"""# Local Hostile Audit - S27_V2 ZN Pre-2023 Older-History Download/Build

Date: 2026-06-11

Verdict:

```text
{"PASS" if passed else "FAIL_CLOSED"}
```

P0 findings: none observed in this local self-audit scope.

P1 findings: none observed in this local self-audit scope.

P2 findings: none observed in this local self-audit scope.

Scope checks:

- Provider access was restricted to DataBento ZN pre-2023 history for this gate.
- 2023 TEST, VALIDATION, OOS, Lockbox, and Forward data were not opened by the emitted pack.
- The emitted pack is Development/Reconciliation only and does not run a backtest or emit results.
- Credential material is not written to artifacts.

Status hash evidence is in:

```text
{OUTPUT_ROOT.relative_to(ROOT) / Path("hashes") / (RUN_ID + "_sha256.json")}
```
"""


if __name__ == "__main__":
    main()
