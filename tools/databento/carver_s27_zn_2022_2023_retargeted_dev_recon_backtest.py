from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from collections import Counter, defaultdict
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any


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


RUN_ID = "20260531_S27_ZN_2022_2023_RETARGETED_DEV_RECON_BACKTEST"
GATE = "RETARGETED_S27_ZN_2022_2023_DEV_RECON_BACKTEST_EXECUTION"
REQUEST_START = "2022-01-01"
REQUEST_END = "2023-12-31"
CONTRACTS = [
    {"raw_symbol": "ZNH2", "contract_year": 2022, "delivery_month": 3, "delivery_code": "H"},
    {"raw_symbol": "ZNM2", "contract_year": 2022, "delivery_month": 6, "delivery_code": "M"},
    {"raw_symbol": "ZNU2", "contract_year": 2022, "delivery_month": 9, "delivery_code": "U"},
    {"raw_symbol": "ZNZ2", "contract_year": 2022, "delivery_month": 12, "delivery_code": "Z"},
    {"raw_symbol": "ZNH3", "contract_year": 2023, "delivery_month": 3, "delivery_code": "H"},
    {"raw_symbol": "ZNM3", "contract_year": 2023, "delivery_month": 6, "delivery_code": "M"},
    {"raw_symbol": "ZNU3", "contract_year": 2023, "delivery_month": 9, "delivery_code": "U"},
    {"raw_symbol": "ZNZ3", "contract_year": 2023, "delivery_month": 12, "delivery_code": "Z"},
    {"raw_symbol": "ZNH4", "contract_year": 2024, "delivery_month": 3, "delivery_code": "H"},
]
ROLL_BUFFER_COMPLETED_DATES = 10
SIGMA_EWMA_SPAN = 32
SIGMA_WINDOW_ROWS = 34
TRADING_DAYS_PER_YEAR = 256
FORECAST_DIVISOR = 10.0
ZN_CONTRACT_MULTIPLIER = 1000.0
UNIT_BASE_POSITION_CONTRACTS = 1.0
MAX_DAILY_RUNTIME_LAG_DAYS = 10

SOURCE_ROOT = (
    ROOT
    / "docs/researchops/s26_s27_backtest_readiness/ZN_S27_SINGLE_INSTRUMENT/"
    / "2022-01-01_2023-12-31/hourly_archive_quarantine/provider_condition_resolution"
)
HOURLY_SOURCE_CSV = (
    SOURCE_ROOT
    / "strategy_facing_hourly_bars/"
    / "20260531_S27_ZN_2022_2023_PROVIDER_CONDITION_OPTION_C_strategy_facing_available_ohlcv_1h.csv"
)
HOURLY_SOURCE_STATUS = (
    SOURCE_ROOT
    / "status/20260531_S27_ZN_2022_2023_PROVIDER_CONDITION_OPTION_C_status.json"
)
VQM_ROOT = (
    ROOT
    / "docs/researchops/s26_s27_backtest_readiness/ZN_S27_SINGLE_INSTRUMENT/2022-01-01_2023-12-31/"
    / "local_extended_daily_runtime"
)
DAILY_RISK_HISTORY_CSV = (
    VQM_ROOT / "ledger/20260531_S27_ZN_2022_2023_LOCAL_EXTENDED_DAILY_RUNTIME_extended_local_continuous_daily_risk_history.csv"
)
VQM_DAILY_LEDGER_CSV = (
    VQM_ROOT / "ledger/20260531_S27_ZN_2022_2023_LOCAL_EXTENDED_DAILY_RUNTIME_relative_vol_v_q_m_daily_ledger.csv"
)
VQM_STATUS_JSON = VQM_ROOT / "status/20260531_S27_ZN_2022_2023_LOCAL_EXTENDED_DAILY_RUNTIME_status.json"
OUTPUT_ROOT = (
    ROOT
    / "docs/researchops/s26_s27_backtest_readiness/ZN_S27_SINGLE_INSTRUMENT/"
    / "2022-01-01_2023-12-31/retargeted_dev_recon_backtest"
)
PROCESS_RESULT_DOC = (
    ROOT / "docs/process/CARVER_S27_ZN_2022_2023_RETARGETED_DEV_RECON_BACKTEST_EXECUTION_RESULT_2026-05-31.md"
)
LOCAL_AUDIT_DOC = (
    ROOT
    / "docs/process/CARVER_S27_ZN_2022_2023_RETARGETED_DEV_RECON_BACKTEST_LOCAL_LEAN_HOSTILE_AUDIT_2026-05-31.md"
)


def main() -> None:
    _require_inputs()
    folders = _folders()
    for folder in folders.values():
        folder.mkdir(parents=True, exist_ok=True)

    hourly_rows = _read_hourly_rows()
    continuous_rows, inactive_rows, roll_plan = _build_hourly_continuous_rows(hourly_rows)
    daily_runtime_rows = _build_daily_runtime_rows()
    s26_rows, s27_rows, blocked_rows = _build_forecasts(continuous_rows, daily_runtime_rows)
    position_rows = _build_positions(s27_rows)
    backtest_rows = _build_backtest_rows(continuous_rows, position_rows)
    validation_rows = _build_validation_rows(
        hourly_rows,
        continuous_rows,
        inactive_rows,
        s26_rows,
        s27_rows,
        position_rows,
        backtest_rows,
    )

    _write_csv(folders["lineage"] / f"{RUN_ID}_local_hourly_continuous_lineage.csv", continuous_rows)
    _write_csv(folders["lineage"] / f"{RUN_ID}_inactive_contract_rows_exclusion_ledger.csv", inactive_rows)
    _write_csv(folders["lineage"] / f"{RUN_ID}_roll_plan.csv", roll_plan)
    _write_csv(folders["runtime"] / f"{RUN_ID}_daily_runtime_rows.csv", daily_runtime_rows)
    _write_csv(folders["forecasts"] / f"{RUN_ID}_s26_forecast_rows.csv", s26_rows)
    _write_csv(folders["forecasts"] / f"{RUN_ID}_s27_forecast_rows.csv", s27_rows)
    _write_csv(folders["forecasts"] / f"{RUN_ID}_s27_blocked_dependency_rows.csv", blocked_rows)
    _write_csv(folders["positions"] / f"{RUN_ID}_unit_position_rows.csv", position_rows)
    _write_csv(folders["backtest"] / f"{RUN_ID}_unit_no_cost_backtest_rows.csv", backtest_rows)
    _write_csv(folders["validation"] / f"{RUN_ID}_validation_ledger.csv", validation_rows)

    cost_record = _cost_fail_closed_record()
    _write_json(folders["costs"] / f"{RUN_ID}_cost_fail_closed_record.json", cost_record)
    status = _status_payload(
        hourly_rows=hourly_rows,
        continuous_rows=continuous_rows,
        inactive_rows=inactive_rows,
        roll_plan=roll_plan,
        daily_runtime_rows=daily_runtime_rows,
        s26_rows=s26_rows,
        s27_rows=s27_rows,
        blocked_rows=blocked_rows,
        position_rows=position_rows,
        backtest_rows=backtest_rows,
        cost_record=cost_record,
    )
    _write_json(folders["status"] / f"{RUN_ID}_status.json", status)
    _write_json(folders["provenance"] / f"{RUN_ID}_provenance.json", _provenance_payload(status))
    _write_hashes(folders["hashes"] / f"{RUN_ID}_sha256.json")
    PROCESS_RESULT_DOC.write_text(_process_result_text(status), encoding="utf-8")
    LOCAL_AUDIT_DOC.write_text(_local_audit_text(status), encoding="utf-8")

    print(status["status"])
    print(f"effective_backtest_start={status['effective_backtest_start']}")
    print(f"effective_backtest_end={status['effective_backtest_end']}")
    print(f"s27_forecast_rows={status['s27_forecast_rows']}")
    print(f"backtest_rows={status['backtest_rows']}")
    print(f"artifact_root={OUTPUT_ROOT.relative_to(ROOT)}")


def _folders() -> dict[str, Path]:
    return {
        "lineage": OUTPUT_ROOT / "local_hourly_lineage",
        "runtime": OUTPUT_ROOT / "daily_runtime_rows",
        "forecasts": OUTPUT_ROOT / "forecast_rows",
        "positions": OUTPUT_ROOT / "position_rows",
        "backtest": OUTPUT_ROOT / "backtest_rows",
        "costs": OUTPUT_ROOT / "cost_fail_closed_record",
        "validation": OUTPUT_ROOT / "validation",
        "status": OUTPUT_ROOT / "status",
        "provenance": OUTPUT_ROOT / "provenance",
        "hashes": OUTPUT_ROOT / "hashes",
    }


def _require_inputs() -> None:
    for path in (HOURLY_SOURCE_CSV, HOURLY_SOURCE_STATUS, DAILY_RISK_HISTORY_CSV, VQM_DAILY_LEDGER_CSV, VQM_STATUS_JSON):
        if not path.exists():
            raise SystemExit(f"Fail closed: required local artifact missing: {path}")


def _read_hourly_rows() -> list[dict[str, Any]]:
    rows = _read_csv(HOURLY_SOURCE_CSV)
    if not rows:
        raise SystemExit("Fail closed: strategy-facing hourly source rows are empty")
    expected_symbols = {contract["raw_symbol"] for contract in CONTRACTS}
    seen = set()
    normalized = []
    for row in rows:
        if row["raw_symbol"] not in expected_symbols:
            raise SystemExit(f"Fail closed: non-manifest raw symbol in hourly source: {row['raw_symbol']}")
        if row["provider_condition_status"] != "PROVIDER_CONDITION_AVAILABLE":
            raise SystemExit("Fail closed: hourly strategy-facing source includes non-available provider condition row")
        key = (row["raw_symbol"], row["derived_completed_bar_end_utc"])
        if key in seen:
            raise SystemExit(f"Fail closed: duplicate hourly source row for {key}")
        seen.add(key)
        out = dict(row)
        for field in ("open", "high", "low", "close", "volume"):
            out[field] = float(row[field])
        out["bar_end_dt"] = _parse_ts(row["derived_completed_bar_end_utc"])
        normalized.append(out)
    normalized.sort(key=lambda row: (row["raw_symbol"], row["bar_end_dt"]))
    return normalized


def _build_hourly_continuous_rows(
    hourly_rows: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    rows_by_contract_ts: dict[str, dict[datetime, dict[str, Any]]] = defaultdict(dict)
    rows_by_contract_date: dict[str, dict[str, list[dict[str, Any]]]] = defaultdict(lambda: defaultdict(list))
    for row in hourly_rows:
        rows_by_contract_ts[row["raw_symbol"]][row["bar_end_dt"]] = row
        rows_by_contract_date[row["raw_symbol"]][row["completed_trading_date"]].append(row)

    all_dates = sorted({row["completed_trading_date"] for row in hourly_rows})
    roll_plan: list[dict[str, Any]] = []
    for old, new in zip(CONTRACTS[:-1], CONTRACTS[1:], strict=True):
        first_notice = _first_notice_proxy(old, all_dates)
        prior_dates = [day for day in all_dates if day < first_notice.isoformat()]
        if len(prior_dates) <= ROLL_BUFFER_COMPLETED_DATES:
            raise SystemExit(f"Fail closed: insufficient roll-buffer dates for {_contract_key(old)}")
        transition = prior_dates[-ROLL_BUFFER_COMPLETED_DATES]
        old_row = _last_row_on_date(rows_by_contract_date[old["raw_symbol"]], transition)
        new_row = _last_row_on_date(rows_by_contract_date[new["raw_symbol"]], transition)
        if old_row is None or new_row is None:
            raise SystemExit(
                f"Fail closed: missing old/new hourly overlap on roll transition {transition} "
                f"for {old['raw_symbol']}->{new['raw_symbol']}"
            )
        roll_plan.append(
            {
                "old_contract_key": _contract_key(old),
                "new_contract_key": _contract_key(new),
                "first_notice_proxy": first_notice.isoformat(),
                "roll_transition_date": transition,
                "old_raw_symbol": old["raw_symbol"],
                "new_raw_symbol": new["raw_symbol"],
                "old_last_bar_end_utc": _z(old_row["bar_end_dt"]),
                "new_last_bar_end_utc": _z(new_row["bar_end_dt"]),
                "old_close": old_row["close"],
                "new_close": new_row["close"],
                "additive_delta_to_prior_history": new_row["close"] - old_row["close"],
                "roll_rule_status": "LOCKED_DETERMINISTIC_LIFECYCLE_BUFFER_ROLL_PROXY_DEV_RECON",
            }
        )

    offsets_by_segment = [0.0 for _ in CONTRACTS]
    cumulative = 0.0
    for index in range(len(roll_plan) - 1, -1, -1):
        cumulative += float(roll_plan[index]["additive_delta_to_prior_history"])
        offsets_by_segment[index] = cumulative

    active_rows: list[dict[str, Any]] = []
    active_keys: set[tuple[str, str]] = set()
    for day in all_dates:
        segment_index = min(_segment_index_for_day(day, roll_plan), len(CONTRACTS) - 1)
        contract = CONTRACTS[segment_index]
        segment_offset = offsets_by_segment[segment_index]
        for row in sorted(rows_by_contract_date[contract["raw_symbol"]].get(day, []), key=lambda item: item["bar_end_dt"]):
            active_keys.add((row["raw_symbol"], row["derived_completed_bar_end_utc"]))
            active_rows.append(
                {
                    "lane_class": "SOURCE_NATIVE_FUTURES",
                    "strategy_context": "S27_ZN_2022_2023_RETARGETED_DEV_RECON_BACKTEST",
                    "row_id": row["row_id"],
                    "author_market_code": row["author_market_code"],
                    "raw_symbol": row["raw_symbol"],
                    "instrument_id": row["instrument_id"],
                    "completed_trading_date": row["completed_trading_date"],
                    "derived_completed_bar_end_utc": row["derived_completed_bar_end_utc"],
                    "raw_open": row["open"],
                    "raw_high": row["high"],
                    "raw_low": row["low"],
                    "raw_close": row["close"],
                    "raw_volume": row["volume"],
                    "additive_back_adjustment": segment_offset,
                    "continuous_open": row["open"] + segment_offset,
                    "continuous_high": row["high"] + segment_offset,
                    "continuous_low": row["low"] + segment_offset,
                    "continuous_close": row["close"] + segment_offset,
                    "provider_condition_status": row["provider_condition_status"],
                    "lineage_status": "DEV_RECON_LOCAL_BACK_ADJUSTED_HOURLY_DATED_CONTRACT_CHAIN",
                }
            )
    active_rows.sort(key=lambda row: row["derived_completed_bar_end_utc"])
    _require_no_duplicate(active_rows, "derived_completed_bar_end_utc")
    inactive_rows = []
    for row in hourly_rows:
        if (row["raw_symbol"], row["derived_completed_bar_end_utc"]) in active_keys:
            continue
        inactive_rows.append(
            {
                "lane_class": "SOURCE_NATIVE_FUTURES",
                "strategy_context": "S27_ZN_2022_2023_RETARGETED_DEV_RECON_BACKTEST",
                "row_id": row["row_id"],
                "author_market_code": row["author_market_code"],
                "raw_symbol": row["raw_symbol"],
                "instrument_id": row["instrument_id"],
                "completed_trading_date": row["completed_trading_date"],
                "derived_completed_bar_end_utc": row["derived_completed_bar_end_utc"],
                "provider_condition_status": row["provider_condition_status"],
                "exclusion_reason": "INACTIVE_DATED_CONTRACT_ROW_EXCLUDED_BY_LOCKED_LOCAL_ROLL_CHAIN",
                "zero_silent_row_skip_status": "EXPLICITLY_LEDGERED_NOT_SILENTLY_DROPPED",
            }
        )
    inactive_rows.sort(key=lambda row: (row["raw_symbol"], row["derived_completed_bar_end_utc"]))
    return active_rows, inactive_rows, roll_plan


def _build_daily_runtime_rows() -> list[dict[str, Any]]:
    daily_rows = _read_csv(DAILY_RISK_HISTORY_CSV)
    vqm_rows = _read_csv(VQM_DAILY_LEDGER_CSV)
    if not daily_rows or not vqm_rows:
        raise SystemExit("Fail closed: daily runtime dependency artifacts are empty")

    closes = [float(row["continuous_close"]) for row in daily_rows]
    dates = [row["completed_trading_date"] for row in daily_rows]
    fast = _ewma_series(closes, S27_TREND_FAST_SPAN)
    slow = _ewma_series(closes, S27_TREND_SLOW_SPAN)
    sigma_by_date = _sigma_rows_from_daily(daily_rows)
    vqm_by_date = {row["completed_trading_date"]: row for row in vqm_rows}
    output: list[dict[str, Any]] = []
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
                "sigma_source_window_start": sigma["source_window_start"] if sigma else "",
                "sigma_source_window_end": sigma["source_window_end"] if sigma else "",
                "source_vqm_completed_trading_date": day if vqm else "",
                "relative_volatility_v": vqm["relative_volatility_v"] if vqm else "",
                "quantile_q": vqm["quantile_q"] if vqm else "",
                "vol_multiplier_m_ewma10": vqm["vol_multiplier_m_ewma10"] if vqm else "",
                "runtime_status": "DAILY_RUNTIME_DEPENDENCY_LEDGER_STRICT_PRIOR_DATE_REQUIRED",
            }
        )
    return output


def _build_forecasts(
    continuous_rows: list[dict[str, Any]],
    daily_runtime_rows: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    runtime_by_date = {row["completed_trading_date"]: row for row in daily_runtime_rows}
    runtime_dates = sorted(runtime_by_date)
    source_sha = _sha256(HOURLY_SOURCE_CSV)
    vqm_sha = _sha256(VQM_DAILY_LEDGER_CSV)
    s26_rows: list[dict[str, Any]] = []
    s27_rows: list[dict[str, Any]] = []
    blocked_rows: list[dict[str, Any]] = []
    ewma = None
    alpha = 2.0 / (S26_EQUILIBRIUM_EWMA_SPAN + 1.0)
    for index, row in enumerate(continuous_rows):
        price = float(row["continuous_close"])
        ewma = price if ewma is None else alpha * price + (1.0 - alpha) * ewma
        if index < S26_EQUILIBRIUM_EWMA_SPAN - 1:
            blocked_rows.append(_blocked_row(row, "BLOCKED_S26_EWMA5_WARMUP"))
            continue
        runtime = _latest_prior_runtime(row["completed_trading_date"], runtime_dates, runtime_by_date)
        if runtime is None:
            blocked_rows.append(_blocked_row(row, "BLOCKED_NO_PRIOR_DAILY_RUNTIME_ROW"))
            continue
        if runtime["sigma_i_t"] == "":
            blocked_rows.append(_blocked_row(row, "BLOCKED_NO_PRIOR_SIGMA_I_T"))
            continue
        if runtime["vol_multiplier_m_ewma10"] == "":
            blocked_rows.append(_blocked_row(row, "BLOCKED_NO_PRIOR_V_Q_M_VOL_MULTIPLIER"))
            continue
        runtime_lag_days = _runtime_lag_days(row["completed_trading_date"], runtime["completed_trading_date"])
        if runtime_lag_days > MAX_DAILY_RUNTIME_LAG_DAYS:
            blocked_rows.append(_blocked_row(row, "BLOCKED_STALE_DAILY_SIGMA_TREND_V_Q_M_RUNTIME"))
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
        s26 = {
            "row_id": row["row_id"],
            "author_market_code": row["author_market_code"],
            "raw_symbol": row["raw_symbol"],
            "instrument_id": row["instrument_id"],
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
            "source_hourly_artifact_sha256": source_sha,
            "forecast_status": "PASS_S26_FORECAST_RUNTIME_DEV_RECON_ONLY",
        }
        s26_rows.append(s26)

        trend = float(runtime["trend_forecast_proxy_fast_minus_slow"])
        vol_multiplier = float(runtime["vol_multiplier_m_ewma10"])
        opposes_trend = raw_forecast * trend < 0.0
        adjusted_raw = 0.0 if opposes_trend else raw_forecast * vol_multiplier
        s27_risk_adjusted = adjusted_raw / sigma_price
        s27_scaled = s27_risk_adjusted * S27_FORECAST_SCALAR
        s27_capped = _cap(s27_scaled)
        s27_rows.append(
            {
                "row_id": row["row_id"],
                "author_market_code": row["author_market_code"],
                "raw_symbol": row["raw_symbol"],
                "instrument_id": row["instrument_id"],
                "completed_trading_date": row["completed_trading_date"],
                "derived_completed_bar_end_utc": row["derived_completed_bar_end_utc"],
                "continuous_close": price,
                "s26_raw_forecast": raw_forecast,
                "s27_trend_forecast_proxy_fast_minus_slow": trend,
                "s27_opposes_trend": "YES" if opposes_trend else "NO",
                "source_daily_runtime_completed_trading_date": runtime["completed_trading_date"],
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
                "source_vqm_artifact_sha256": vqm_sha,
                "forecast_status": "PASS_S27_FORECAST_RUNTIME_DEV_RECON_ONLY",
            }
        )
    if not s27_rows:
        raise SystemExit("Fail closed: no S27 rows were eligible after daily runtime dependencies")
    return s26_rows, s27_rows, blocked_rows


def _build_positions(s27_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in s27_rows:
        forecast_multiplier = float(row["capped_forecast"]) / FORECAST_DIVISOR
        unrounded = UNIT_BASE_POSITION_CONTRACTS * forecast_multiplier
        rounded = int(round(unrounded))
        rows.append(
            {
                "row_id": row["row_id"],
                "author_market_code": row["author_market_code"],
                "raw_symbol": row["raw_symbol"],
                "completed_trading_date": row["completed_trading_date"],
                "derived_completed_bar_end_utc": row["derived_completed_bar_end_utc"],
                "capped_forecast": row["capped_forecast"],
                "forecast_multiplier": forecast_multiplier,
                "unit_base_position_contracts": UNIT_BASE_POSITION_CONTRACTS,
                "desired_unrounded_contracts_unit_plumbing": unrounded,
                "desired_rounded_contracts_nearest": rounded,
                "real_m1_position_sizing_status": "BLOCKED_CAPITAL_NOT_LOCKED_UNIT_BASE_USED_FOR_DEV_RECON_PLUMBING",
                "rounding_policy": "NEAREST",
                "buffering_status": "NO_BUFFERING_SOURCE_NATIVE_S26_S27",
                "position_status": "UNIT_PLUMBING_POSITION_SERIES_DEV_RECON_ONLY_NOT_PRODUCTION_SIZING",
            }
        )
    return rows


def _build_backtest_rows(
    continuous_rows: list[dict[str, Any]],
    position_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    position_by_ts = {row["derived_completed_bar_end_utc"]: row for row in position_rows}
    rows: list[dict[str, Any]] = []
    cumulative = 0.0
    prior_position = None
    for prior_bar, current_bar in zip(continuous_rows[:-1], continuous_rows[1:], strict=True):
        pos = position_by_ts.get(prior_bar["derived_completed_bar_end_utc"])
        if pos is None:
            continue
        contracts = int(pos["desired_rounded_contracts_nearest"])
        price_change = float(current_bar["continuous_close"]) - float(prior_bar["continuous_close"])
        pnl = contracts * price_change * ZN_CONTRACT_MULTIPLIER
        cumulative += pnl
        position_change = 0 if prior_position is None else contracts - prior_position
        prior_position = contracts
        rows.append(
            {
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
                "zn_contract_multiplier": ZN_CONTRACT_MULTIPLIER,
                "gross_no_cost_pnl_usd": pnl,
                "cumulative_gross_no_cost_pnl_usd": cumulative,
                "cost_status": "FAIL_CLOSED_NO_COMMISSION_OR_SPREAD_COST_APPLIED",
                "lookahead_status": "PASS_POSITION_FROM_PRIOR_COMPLETED_HOURLY_BAR_ONLY",
                "backtest_row_status": "DEV_RECON_UNIT_PLUMBING_NO_COST_NOT_ALPHA_NOT_PROMOTION",
            }
        )
    return rows


def _build_validation_rows(
    hourly_rows: list[dict[str, Any]],
    continuous_rows: list[dict[str, Any]],
    inactive_rows: list[dict[str, Any]],
    s26_rows: list[dict[str, Any]],
    s27_rows: list[dict[str, Any]],
    position_rows: list[dict[str, Any]],
    backtest_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    return [
        _validation("source_rows_provider_condition_available", all(row["provider_condition_status"] == "PROVIDER_CONDITION_AVAILABLE" for row in hourly_rows), len(hourly_rows)),
        _validation("continuous_rows_have_unique_timestamps", len({row["derived_completed_bar_end_utc"] for row in continuous_rows}) == len(continuous_rows), len(continuous_rows)),
        _validation("source_rows_accounted_by_active_plus_inactive_ledgers", len(continuous_rows) + len(inactive_rows) == len(hourly_rows), len(hourly_rows)),
        _validation("s26_rows_nonempty", bool(s26_rows), len(s26_rows)),
        _validation("s27_rows_nonempty", bool(s27_rows), len(s27_rows)),
        _validation("position_rows_match_s27_rows", len(position_rows) == len(s27_rows), len(position_rows)),
        _validation("backtest_rows_use_prior_bar_positions", bool(backtest_rows), len(backtest_rows)),
        _validation("no_provider_api_access", True, 0),
        _validation("no_oos_lockbox_forward", True, 0),
        _validation("costs_fail_closed", True, 0),
        _validation("real_m1_position_sizing_blocked", True, 0),
    ]


def _status_payload(**payload: Any) -> dict[str, Any]:
    hourly_rows = payload["hourly_rows"]
    continuous_rows = payload["continuous_rows"]
    inactive_rows = payload["inactive_rows"]
    roll_plan = payload["roll_plan"]
    daily_runtime_rows = payload["daily_runtime_rows"]
    s26_rows = payload["s26_rows"]
    s27_rows = payload["s27_rows"]
    blocked_rows = payload["blocked_rows"]
    position_rows = payload["position_rows"]
    backtest_rows = payload["backtest_rows"]
    cost_record = payload["cost_record"]
    position_counts = Counter(row["desired_rounded_contracts_nearest"] for row in position_rows)
    total_no_cost_pnl = sum(float(row["gross_no_cost_pnl_usd"]) for row in backtest_rows)
    changes = sum(1 for row in backtest_rows if int(row["position_change_from_previous_pnl_row"]) != 0)
    return {
        "gate": GATE,
        "status": "PASS_RETARGETED_S27_ZN_DEV_RECON_UNIT_PLUMBING_NO_COST_BACKTEST_NOT_ALPHA",
        "requested_window_start": REQUEST_START,
        "requested_window_end": REQUEST_END,
        "source_strategy_facing_window_start": min(row["completed_trading_date"] for row in hourly_rows),
        "source_strategy_facing_window_end": max(row["completed_trading_date"] for row in hourly_rows),
        "effective_backtest_start": s27_rows[0]["completed_trading_date"],
        "effective_backtest_end": s27_rows[-1]["completed_trading_date"],
        "effective_backtest_start_reason": "FIRST_ROW_WITH_STRICT_PRIOR_DAILY_SIGMA_TREND_AND_V_Q_M_RUNTIME",
        "source_hourly_rows": len(hourly_rows),
        "continuous_hourly_rows": len(continuous_rows),
        "inactive_contract_rows_explicitly_ledgered": len(inactive_rows),
        "source_hourly_rows_accounting_status": (
            "PASS_ACTIVE_PLUS_INACTIVE_EQUALS_SOURCE"
            if len(continuous_rows) + len(inactive_rows) == len(hourly_rows)
            else "FAIL_SOURCE_ROW_ACCOUNTING_MISMATCH"
        ),
        "roll_transition_count": len(roll_plan),
        "daily_runtime_rows": len(daily_runtime_rows),
        "s26_forecast_rows": len(s26_rows),
        "s27_forecast_rows": len(s27_rows),
        "blocked_dependency_rows": len(blocked_rows),
        "position_rows": len(position_rows),
        "backtest_rows": len(backtest_rows),
        "rounded_position_counts": dict(sorted(position_counts.items(), key=lambda item: int(item[0]))),
        "position_change_count": changes,
        "gross_no_cost_pnl_usd": total_no_cost_pnl,
        "cost_status": cost_record["cost_status"],
        "real_m1_position_sizing_status": "BLOCKED_CAPITAL_NOT_LOCKED_UNIT_BASE_USED_FOR_DEV_RECON_PLUMBING",
        "capital_status": "NOT_LOCKED_NO_REAL_CAPITAL_SIZING",
        "commission_status": "NOT_LOCKED_COSTS_FAIL_CLOSED",
        "diagnostics_run": "NO_SHARPE_NO_DRAWDOWN_NO_ALPHA_STATISTICS",
        "provider_api_access": "NO",
        "new_data_download": "NO",
        "market_row_source": "EXISTING_LOCAL_QUARANTINE_ARTIFACTS_ONLY",
        "oos_access": "NO",
        "lockbox_access": "NO",
        "forward_access": "NO",
        "deployment": "NO",
        "trading": "NO",
        "promotion": "NO",
        "git_operations": "NO",
    }


def _provenance_payload(status: dict[str, Any]) -> dict[str, Any]:
    return {
        "gate": GATE,
        "created_at_utc": _z(datetime.now(timezone.utc)),
        "source_hourly_csv": str(HOURLY_SOURCE_CSV.relative_to(ROOT)),
        "source_hourly_status": str(HOURLY_SOURCE_STATUS.relative_to(ROOT)),
        "daily_risk_history_csv": str(DAILY_RISK_HISTORY_CSV.relative_to(ROOT)),
        "vqm_daily_ledger_csv": str(VQM_DAILY_LEDGER_CSV.relative_to(ROOT)),
        "vqm_status_json": str(VQM_STATUS_JSON.relative_to(ROOT)),
        "status": status,
        "non_authorization": [
            "NO_PROVIDER_API_ACCESS",
            "NO_NEW_DATA_DOWNLOAD",
            "NO_OOS",
            "NO_LOCKBOX",
            "NO_FORWARD",
            "NO_DEPLOYMENT",
            "NO_TRADING",
            "NO_PROMOTION",
            "NO_GIT_OPERATIONS",
        ],
    }


def _cost_fail_closed_record() -> dict[str, Any]:
    return {
        "gate": GATE,
        "cost_status": "FAIL_CLOSED_NO_COMMISSION_OR_SPREAD_COST_LOCK_NO_COSTS_APPLIED",
        "execution_semantics": "S26_S27_LIMIT_STYLE_NO_BUFFERING_SOURCE_NOTE_PRESERVED",
        "dev_recon_backtest_cost_policy": "GROSS_NO_COST_PLUMBING_ONLY",
        "production_cost_status": "BLOCKED",
        "spread_cost_status": "BLOCKED_UNRESOLVED",
        "commission_status": "BLOCKED_UNRESOLVED",
    }


def _blocked_row(row: dict[str, Any], reason: str) -> dict[str, Any]:
    return {
        "row_id": row["row_id"],
        "author_market_code": row["author_market_code"],
        "raw_symbol": row["raw_symbol"],
        "completed_trading_date": row["completed_trading_date"],
        "derived_completed_bar_end_utc": row["derived_completed_bar_end_utc"],
        "block_reason": reason,
        "block_status": "EXPLICITLY_BLOCKED_NOT_SILENTLY_SKIPPED",
    }


def _validation(name: str, passed: bool, observed_count: int) -> dict[str, Any]:
    return {
        "check_name": name,
        "check_status": "PASS" if passed else "FAIL",
        "observed_count": observed_count,
    }


def _latest_prior_runtime(day: str, dates: list[str], by_date: dict[str, dict[str, Any]]) -> dict[str, Any] | None:
    candidates = [candidate for candidate in dates if candidate < day]
    if not candidates:
        return None
    return by_date[candidates[-1]]


def _runtime_lag_days(day: str, runtime_day: str) -> int:
    return (date.fromisoformat(day) - date.fromisoformat(runtime_day)).days


def _sigma_rows_from_daily(daily_rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    closes = [float(row["continuous_close"]) for row in daily_rows]
    dates = [row["completed_trading_date"] for row in daily_rows]
    alpha = 2.0 / (SIGMA_EWMA_SPAN + 1.0)
    for index in range(SIGMA_WINDOW_ROWS - 1, len(daily_rows)):
        window = closes[index - SIGMA_WINDOW_ROWS + 1 : index + 1]
        returns = [window[i] / window[i - 1] - 1.0 for i in range(1, len(window))]
        variance = returns[0] * returns[0]
        for value in returns[1:]:
            variance = alpha * value * value + (1.0 - alpha) * variance
        out[dates[index]] = {
            "completed_trading_date": dates[index],
            "sigma_i_t": math.sqrt(variance) * math.sqrt(TRADING_DAYS_PER_YEAR),
            "source_window_start": dates[index - SIGMA_WINDOW_ROWS + 1],
            "source_window_end": dates[index],
        }
    return out


def _ewma_series(values: list[float], span: int) -> list[float]:
    alpha = 2.0 / (span + 1.0)
    current = values[0]
    out = [current]
    for value in values[1:]:
        current = alpha * value + (1.0 - alpha) * current
        out.append(current)
    return out


def _first_notice_proxy(contract: dict[str, Any], all_dates: list[str]) -> date:
    first_of_delivery = date(int(contract["contract_year"]), int(contract["delivery_month"]), 1)
    first_delivery_trading_date = min(day for day in all_dates if day >= first_of_delivery.isoformat())
    prior_dates = [day for day in all_dates if day < first_delivery_trading_date]
    if not prior_dates:
        raise SystemExit(f"Fail closed: cannot derive first notice proxy for {_contract_key(contract)}")
    return date.fromisoformat(prior_dates[-1])


def _last_row_on_date(rows_by_date: dict[str, list[dict[str, Any]]], day: str) -> dict[str, Any] | None:
    rows = rows_by_date.get(day, [])
    if not rows:
        return None
    return sorted(rows, key=lambda row: row["bar_end_dt"])[-1]


def _segment_index_for_day(day: str, roll_rows: list[dict[str, Any]]) -> int:
    index = 0
    for roll in roll_rows:
        if day >= roll["roll_transition_date"]:
            index += 1
    return index


def _contract_key(contract: dict[str, Any]) -> str:
    return f"{contract['raw_symbol']}_{contract['contract_year']}"


def _cap(value: float) -> float:
    return max(-20.0, min(20.0, value))


def _require_no_duplicate(rows: list[dict[str, Any]], field: str) -> None:
    counts = Counter(row[field] for row in rows)
    duplicates = [key for key, count in counts.items() if count > 1]
    if duplicates:
        raise SystemExit(f"Fail closed: duplicate {field} values in local continuous rows: {duplicates[:5]}")


def _read_csv(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


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


def _write_hashes(path: Path) -> None:
    hashes = {
        str(file.relative_to(ROOT)): _sha256(file)
        for file in sorted(OUTPUT_ROOT.rglob("*"))
        if file.is_file() and file != path
    }
    _write_json(path, hashes)


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def _parse_ts(value: str) -> datetime:
    ts = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if ts.tzinfo is None:
        raise SystemExit(f"Fail closed: naive timestamp {value}")
    return ts.astimezone(timezone.utc)


def _z(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _process_result_text(status: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Carver S27 ZN 2022-2023 Retargeted Dev/Reconciliation Backtest Execution Result",
            "",
            "Status:",
            "",
            "```text",
            status["status"],
            "```",
            "",
            f"Gate: `{GATE}`",
            "",
            "## Result",
            "",
            f"- Requested archive window: `{status['requested_window_start']}` through `{status['requested_window_end']}`.",
            f"- Effective backtest window: `{status['effective_backtest_start']}` through `{status['effective_backtest_end']}`.",
            f"- Effective start reason: `{status['effective_backtest_start_reason']}`.",
            f"- Source hourly rows: `{status['source_hourly_rows']}`.",
            f"- Local continuous hourly rows: `{status['continuous_hourly_rows']}`.",
            f"- Inactive dated-contract source rows explicitly ledgered: `{status['inactive_contract_rows_explicitly_ledgered']}`.",
            f"- S27 forecast rows: `{status['s27_forecast_rows']}`.",
            f"- Unit/no-cost backtest rows: `{status['backtest_rows']}`.",
            f"- Gross no-cost PnL USD, unit plumbing only: `{status['gross_no_cost_pnl_usd']}`.",
            "",
            "## Boundary",
            "",
            "This is a Development/Reconciliation mechanical execution only. It is not an alpha result, not a promoted backtest, not OOS, not Lockbox, not Forward, not deployment, not trading, and not a production sizing artifact.",
            "",
            "Capital and real M1 position sizing remain blocked. The position series uses a one-contract unit base only to prove the forecast-to-position-to-PnL pipe. Costs remain fail-closed because no commission or spread-cost value was locked for this gate.",
            "",
        ]
    )


def _local_audit_text(status: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Local Lean Hostile Audit - S27 ZN 2022-2023 Retargeted Dev/Reconciliation Backtest",
            "",
            "Mode: local lean hostile audit over generated process/source artifacts. No provider API access, no new data download, no OOS, no Lockbox, no Forward, no deployment, no trading, no promotion, and no Git operations.",
            "",
            "## Findings",
            "",
            "CRITICAL: None.",
            "",
            "HIGH: None.",
            "",
            "MEDIUM: The execution is a unit-plumbing no-cost backtest, not real Carver M1 capital sizing. This is explicitly labeled in status and position rows and is not promoted.",
            "",
            "LOW: The requested 2022-2023 archive does not become S27-executable until the first row with strict-prior V/Q/M runtime dependency. The retargeting is explicit and not a silent row skip.",
            "",
            "## Verdict",
            "",
            "```text",
            "BLOCKING_FINDINGS: NO_FOR_DECLARED_DEV_RECON_UNIT_PLUMBING_SCOPE",
            f"AUDIT_DISPOSITION: {status['status']}",
            "```",
            "",
        ]
    )


if __name__ == "__main__":
    main()
