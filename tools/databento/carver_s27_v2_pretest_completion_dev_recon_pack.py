from __future__ import annotations

import csv
import hashlib
import json
import math
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
RUN_ID = "20260611_S27_V2_PRETEST_DEV_RECON_FILLED_SELL_COMPLETION"
AUTHORIZATION = "S27_V2_PRE_TEST_DEVELOPMENT_RECONCILIATION_COMPLETION_GATE"
STATUS = "LOCAL_PRETEST_DEV_RECON_FILLED_SELL_COMPLETION_PACK_DECLARED_NOT_RESULT"
VALUATION_CONVENTION_LABEL = "SOURCE_NATIVE_ENGINEERING_VALUATION_ASSUMPTION_NOT_BOOK_EXPLICIT"

SOURCE_ROOT = (
    ROOT
    / "docs/researchops/s27_v2_databento_older_zn_history/"
    "20260611_pre2023_zn_dev_recon_download_build"
)
LEDGER_ROOT = SOURCE_ROOT / "ledger"
SOURCE_CONTINUOUS_LEDGER = (
    LEDGER_ROOT / "20260611_S27_V2_ZN_PRE2023_OLDER_HISTORY_DOWNLOAD_BUILD_local_continuous_daily_risk_history.csv"
)
SOURCE_ROLL_LEDGER = LEDGER_ROOT / "20260611_S27_V2_ZN_PRE2023_OLDER_HISTORY_DOWNLOAD_BUILD_roll_plan.csv"
SOURCE_HOURLY_LEDGER = (
    LEDGER_ROOT / "20260611_S27_V2_ZN_PRE2023_OLDER_HISTORY_DOWNLOAD_BUILD_strategy_facing_hourly_available_bars.csv"
)

OUTPUT_PACK = (
    ROOT
    / "docs/researchops/s27_v2_local_replay_inputs/ZN/"
    "20260611_pretest_dev_recon_2022_filled_sell_completion_declared_pack"
)
PROCESS_DOC = (
    ROOT / "docs/process/CARVER_S27_ZN_V2_PRETEST_DEV_RECON_FILLED_SELL_COMPLETION_PACK_BUILD_RESULT_2026-06-11.md"
)

SIGMA_EWMA_SPAN = 32
SIGMA_WINDOW_ROWS = 34
TRADING_DAYS_PER_YEAR = 256.0
TEN_YEAR_SIGMA_ROWS = 2560
VQM_EWMA_SPAN = 10
FORECAST_SCALAR_VALUE = 20.0
FORECAST_CAP_VALUE = 20.0
FORECAST_TO_POSITION_DIVISOR = 10.0
CAPITAL_ACCOUNT_VALUE = 500_000.0
ANNUAL_TARGET_RISK = 0.20
CONTRACT_POINT_VALUE = 1000.0
ZN_TICK_SIZE = 0.015625

NON_AUTHORIZATIONS = (
    "NO_PROVIDER_API",
    "NO_DOWNLOADS",
    "NO_NEW_DATA_ACQUISITION",
    "NO_TEST_ACCESS",
    "NO_VALIDATION_ACCESS",
    "NO_OOS",
    "NO_LOCKBOX",
    "NO_FORWARD",
    "NO_RESULT_SCORED_RUN",
    "NO_RESULT_INTERPRETATION",
    "NO_PNL_EVALUATION_BEYOND_MECHANICAL_ROW_CONSTRUCTION",
    "NO_TUNING",
    "NO_ADAPTER_WORK",
    "NO_DEPLOYMENT",
    "NO_TRADING",
    "NO_PROMOTION",
    "NO_GIT_ACTIONS",
    "NO_SOURCE_FAITHFUL_EVIDENCE_CLAIM",
)


def main() -> None:
    continuous = _read_csv(SOURCE_CONTINUOUS_LEDGER)
    rolls = _read_csv(SOURCE_ROLL_LEDGER)
    hourly = [
        row
        for row in _read_csv(SOURCE_HOURLY_LEDGER)
        if row["provider_condition_status"] == "PROVIDER_CONDITION_AVAILABLE"
        and "2022-01-01T00:00:00Z" <= row["derived_completed_bar_end_utc"] < "2023-01-01T00:00:00Z"
    ]
    selection = _select_until_first_filled_sell(continuous, rolls, hourly)
    OUTPUT_PACK.mkdir(parents=True, exist_ok=True)
    _write_pack(selection, rolls)
    manifest = _manifest(selection, rolls)
    _write_json(OUTPUT_PACK / "S27_V2_PRETEST_DEV_RECON_FILLED_SELL_COMPLETION_DECLARED_INPUT_PACK_MANIFEST.json", manifest)
    _write_sha256s(OUTPUT_PACK / "S27_V2_PRETEST_DEV_RECON_FILLED_SELL_COMPLETION_DECLARED_INPUT_PACK_SHA256SUMS.txt", OUTPUT_PACK)
    PROCESS_DOC.write_text(_process_doc(selection, manifest), encoding="ascii")
    print(STATUS)
    print(f"declared_pack={OUTPUT_PACK.relative_to(ROOT)}")
    print(f"row_count={len(selection)}")
    print(f"filled_sell_timestamp={selection[-1]['decision']['derived_completed_bar_end_utc']}")


def _select_until_first_filled_sell(
    continuous: list[dict[str, str]],
    rolls: list[dict[str, str]],
    hourly: list[dict[str, str]],
) -> list[dict[str, Any]]:
    continuous_by_date = {row["completed_trading_date"]: row for row in continuous}
    hourly_by_symbol_ts = {
        (row["raw_symbol"], row["derived_completed_bar_end_utc"]): row for row in hourly
    }
    hourly_by_symbol = _group_hourly_by_symbol(hourly)
    cache: dict[str, tuple[list[dict[str, Any]], dict[str, Any], dict[str, Any]]] = {}
    current_position = 0
    selected: list[dict[str, Any]] = []
    for decision in sorted(hourly, key=lambda row: (row["derived_completed_bar_end_utc"], row["raw_symbol"])):
        decision_ts = decision["derived_completed_bar_end_utc"]
        raw_symbol = decision["raw_symbol"]
        fill_ts = _z(_parse_ts(decision_ts) + timedelta(hours=1))
        fill = hourly_by_symbol_ts.get((raw_symbol, fill_ts))
        if fill is None:
            continue
        mark = _next_same_symbol_row_after(hourly_by_symbol[raw_symbol], fill_ts)
        if mark is None:
            continue
        previous_dates = [day for day in continuous_by_date if day < decision["completed_trading_date"]]
        if not previous_dates:
            continue
        previous_daily_date = max(previous_dates)
        if previous_daily_date not in cache:
            pit = _point_in_time_continuous_series(continuous, rolls, previous_daily_date)
            sigma_rows = _build_sigma_rows(pit)
            vqm_rows = _build_vqm_rows(sigma_rows)
            sigma_by_date = {row["completed_trading_date"]: row for row in sigma_rows}
            vqm_by_date = {row["completed_trading_date"]: row for row in vqm_rows}
            cache[previous_daily_date] = (pit, sigma_by_date, vqm_by_date)
        pit, sigma_by_date, vqm_by_date = cache[previous_daily_date]
        prior_vqm_dates = [day for day in vqm_by_date if day < decision["completed_trading_date"]]
        if previous_daily_date not in sigma_by_date or not prior_vqm_dates:
            continue
        runtime = _runtime_evidence(
            pit=pit,
            sigma=sigma_by_date[previous_daily_date],
            vqm=vqm_by_date[max(prior_vqm_dates)],
            decision=decision,
            row_index=len(selected) + 1,
        )
        computed = _row_mechanics(
            row_index=len(selected) + 1,
            current_position=current_position,
            decision=decision,
            fill=fill,
            runtime=runtime,
        )
        if computed["formula_status"] != "PASS_FORMULA_SUPPORTED":
            continue
        current_position += int(computed["signed_fill_quantity"])
        selected.append(
            {
                "decision": decision,
                "fill": fill,
                "mark": mark,
                "runtime": runtime,
                "mechanics": computed,
            }
        )
        if computed["order_side"] == "SELL" and computed["fill_executed"] is True:
            return selected
    raise SystemExit("fail closed: no organic filled sell-side reduction found in already-local 2022 ZN evidence")


def _runtime_evidence(
    pit: list[dict[str, Any]],
    sigma: dict[str, Any],
    vqm: dict[str, Any],
    decision: dict[str, str],
    row_index: int,
) -> dict[str, Any]:
    previous_daily = pit[-1]
    window = pit[-64:]
    if len(window) != 64:
        raise SystemExit("fail closed: insufficient 64-row strict-prior daily history")
    closes = tuple(float(row["continuous_close"]) for row in window)
    adjustment = float(previous_daily["additive_back_adjustment"])
    row = {
        "row_index": row_index,
        "decision_timestamp_utc": decision["derived_completed_bar_end_utc"],
        "decision_trading_date": decision["completed_trading_date"],
        "previous_daily_trading_date": previous_daily["completed_trading_date"],
        "point_in_time_roll_cutoff_date": previous_daily["completed_trading_date"],
        "daily_window_start": window[0]["completed_trading_date"],
        "daily_window_end": window[-1]["completed_trading_date"],
        "daily_window_row_count": 64,
        "previous_daily_raw_symbol": previous_daily["raw_symbol"],
        "previous_daily_raw_close": _num(previous_daily["raw_close"]),
        "previous_daily_additive_back_adjustment": _num(adjustment),
        "ewma5_equilibrium": _num(_ewma(closes, 5)),
        "ewmac16_64_trend": _num(_ewma(closes, 16) - _ewma(closes, 64)),
        "annual_percentage_sigma": _num(sigma["sigma_i_t"]),
        "relative_volatility_v": _num(vqm["relative_volatility_v"]),
        "quantile_q": _num(vqm["quantile_q"]),
        "vol_multiplier_m": _num(vqm["vol_multiplier_m_ewma10"]),
        "runtime_status": "PASS_ROLLING_STRICT_PRIOR_DAILY_EVIDENCE_PRETEST_DEV_RECON_NOT_RESULT",
        "no_lookahead_status": "PASS_PRETEST_SELECTED_ROW_STRICT_PRIOR_DAILY_EVIDENCE",
    }
    row["row_hash"] = _row_hash("S27_V2_PRETEST_RUNTIME_EVIDENCE_ROW", row)
    return row


def _row_mechanics(
    row_index: int,
    current_position: int,
    decision: dict[str, str],
    fill: dict[str, str],
    runtime: dict[str, Any],
) -> dict[str, Any]:
    adjustment = float(runtime["previous_daily_additive_back_adjustment"])
    decision_price = float(decision["close"]) + adjustment
    fill_close = float(fill["close"]) + adjustment
    ewma5 = float(runtime["ewma5_equilibrium"])
    trend = float(runtime["ewmac16_64_trend"])
    sigma = float(runtime["annual_percentage_sigma"])
    m = float(runtime["vol_multiplier_m"])
    sigma_price = float(runtime["previous_daily_raw_close"]) * sigma / 16.0
    risk_before_veto = (ewma5 - decision_price) / sigma_price
    risk_after_veto = 0.0 if risk_before_veto * trend < 0.0 else risk_before_veto
    capped_forecast = _clamp(risk_after_veto * m * FORECAST_SCALAR_VALUE, -FORECAST_CAP_VALUE, FORECAST_CAP_VALUE)
    base_position = CAPITAL_ACCOUNT_VALUE * ANNUAL_TARGET_RISK / (decision_price * CONTRACT_POINT_VALUE * sigma)
    desired_position = _round_half_away_from_zero(base_position * capped_forecast / FORECAST_TO_POSITION_DIVISOR)
    position_change = desired_position - current_position
    side = "BUY" if position_change > 0 else "SELL" if position_change < 0 else "NONE"
    adjacent_target = current_position + (1 if position_change > 0 else -1 if position_change < 0 else 0)
    formula_limit = _formula_limit(adjacent_target, base_position, ewma5, sigma_price, m, trend) if side != "NONE" else 0.0
    if formula_limit is None:
        return {
            "row_index": row_index,
            "formula_status": "FAIL_CLOSED_LIMIT_FORMULA_UNSUPPORTED_FOR_PRETEST_SELECTED_ROW",
            "order_side": side,
            "fill_executed": False,
            "signed_fill_quantity": 0,
        }
    limit_price = _round_limit(formula_limit, side) if side != "NONE" else 0.0
    fill_executed = _limit_fill(side, fill_close, limit_price)
    fill_quantity = abs(position_change) if fill_executed else 0
    signed_fill_quantity = fill_quantity if side == "BUY" else -fill_quantity if side == "SELL" else 0
    return {
        "row_index": row_index,
        "formula_status": "PASS_FORMULA_SUPPORTED",
        "starting_position_contracts": current_position,
        "desired_position_contracts": desired_position,
        "position_change_contracts": position_change,
        "order_side": side,
        "order_quantity": abs(position_change),
        "adjacent_target_position": adjacent_target,
        "formula_limit_price": formula_limit,
        "limit_order_price": limit_price,
        "fill_candidate_close": fill_close,
        "fill_executed": fill_executed,
        "fill_quantity": fill_quantity,
        "signed_fill_quantity": signed_fill_quantity,
    }


def _group_hourly_by_symbol(hourly: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    grouped: dict[str, list[dict[str, str]]] = {}
    for row in sorted(hourly, key=lambda item: item["derived_completed_bar_end_utc"]):
        grouped.setdefault(row["raw_symbol"], []).append(row)
    return grouped


def _next_same_symbol_row_after(hourly_rows: list[dict[str, str]], completed_ts: str) -> dict[str, str] | None:
    for row in hourly_rows:
        if row["derived_completed_bar_end_utc"] > completed_ts:
            return row
    return None


def _write_pack(selection: list[dict[str, Any]], rolls: list[dict[str, str]]) -> None:
    _write_csv(OUTPUT_PACK / "runtime_evidence_ledger.csv", [row["runtime"] for row in selection])
    _write_csv(OUTPUT_PACK / "hourly_decision_completed_bar.csv", [_hourly_pack_row(row["decision"], row["runtime"], "DECISION", index) for index, row in enumerate(selection, 1)])
    _write_csv(OUTPUT_PACK / "hourly_fill_completed_bar.csv", [_hourly_pack_row(row["fill"], row["runtime"], "FILL", index) for index, row in enumerate(selection, 1)])
    _write_csv(OUTPUT_PACK / "valuation_mark_completed_bar.csv", [_valuation_row(row["mark"], row["runtime"], index) for index, row in enumerate(selection, 1)])
    _write_csv(OUTPUT_PACK / "daily_continuous_completed_bar.csv", _daily_summary_rows(selection))
    _write_csv(OUTPUT_PACK / "daily_current_contract_completed_bar.csv", _daily_current_rows(selection))
    _write_csv(OUTPUT_PACK / "session_calendar.csv", _session_rows(selection))
    _write_csv(OUTPUT_PACK / "roll_calendar.csv", _roll_rows(rolls, selection[-1]["runtime"]["previous_daily_trading_date"]))
    _write_csv(OUTPUT_PACK / "cost_parameter.csv", _cost_rows())


def _manifest(selection: list[dict[str, Any]], rolls: list[dict[str, str]]) -> dict[str, Any]:
    del rolls
    row_family_files = {
        path.name: {"row_count": _csv_row_count(path), "sha256": _sha256(path)}
        for path in sorted(OUTPUT_PACK.glob("*.csv"))
    }
    final = selection[-1]["mechanics"]
    plan = []
    for index, row in enumerate(selection, 1):
        plan.append(
            {
                "row_index": index,
                "decision_timestamp_utc": row["decision"]["derived_completed_bar_end_utc"],
                "fill_timestamp_utc": row["fill"]["derived_completed_bar_end_utc"],
                "valuation_mark_timestamp_utc": row["mark"]["derived_completed_bar_end_utc"],
                "raw_symbol": row["decision"]["raw_symbol"],
                "previous_daily_trading_date": row["runtime"]["previous_daily_trading_date"],
                "runtime_evidence_row_hash": row["runtime"]["row_hash"],
                "selected_for_formula_status": row["mechanics"]["formula_status"],
                "order_side": row["mechanics"]["order_side"],
                "fill_executed": "YES" if row["mechanics"]["fill_executed"] else "NO",
            }
        )
    return {
        "artifact": "S27_V2_PRETEST_DEV_RECON_FILLED_SELL_COMPLETION_DECLARED_INPUT_PACK_MANIFEST",
        "authorization": AUTHORIZATION,
        "status": STATUS,
        "lane": "SOURCE_NATIVE_FUTURES",
        "selected_slice_rule": "EARLIEST_ALREADY_LOCAL_2022_ORGANIC_FILLED_SELL_REDUCTION_AFTER_STRICT_PRIOR_WARMUPS_PRESERVE_2023_FOR_TEST",
        "source_continuous_daily_ledger": str(SOURCE_CONTINUOUS_LEDGER.relative_to(ROOT)),
        "source_roll_ledger": str(SOURCE_ROLL_LEDGER.relative_to(ROOT)),
        "source_hourly_ledger": str(SOURCE_HOURLY_LEDGER.relative_to(ROOT)),
        "decision_fill_mark_plan": plan,
        "row_family_files": row_family_files,
        "filled_sell_completion": {
            "row_index": final["row_index"],
            "decision_timestamp_utc": selection[-1]["decision"]["derived_completed_bar_end_utc"],
            "fill_timestamp_utc": selection[-1]["fill"]["derived_completed_bar_end_utc"],
            "raw_symbol": selection[-1]["decision"]["raw_symbol"],
            "starting_position_contracts": final["starting_position_contracts"],
            "desired_position_contracts": final["desired_position_contracts"],
            "position_change_contracts": final["position_change_contracts"],
            "order_side": final["order_side"],
            "order_quantity": final["order_quantity"],
            "limit_order_price": _num(final["limit_order_price"]),
            "fill_candidate_close": _num(final["fill_candidate_close"]),
            "fill_executed": "YES",
        },
        "history_evidence": {
            "rolling_strict_prior_daily_evidence": "PASS_RECOMPUTED_PER_SELECTED_ROW_FROM_ALREADY_LOCAL_PRE2023_SOURCE_LEDGERS",
            "point_in_time_roll_offsets": "PASS_NO_FUTURE_ROLL_DELTAS_PER_SELECTED_ROW_CUTOFF",
            "cost_policy_status": "ACCEPTED_INFERRED_RETAIL_FUTURES_COST_FOR_LOCAL_DEV_RECON_ONLY_NOT_BOOK_EXPLICIT",
            "valuation_policy_status": VALUATION_CONVENTION_LABEL,
            "working_order_lifecycle_status": "UNFILLED_LIMIT_ORDERS_NOT_CARRIED_FAIL_CLOSED_CURRENT_MECHANICS",
        },
        "explicitly_excluded_data": ["NO_2023_TEST_DATA", "NO_VALIDATION", "NO_OOS", "NO_LOCKBOX", "NO_FORWARD"],
        "non_authorizations": list(NON_AUTHORIZATIONS),
    }


def _hourly_pack_row(row: dict[str, str], runtime: dict[str, Any], role: str, index: int) -> dict[str, Any]:
    adjustment = float(runtime["previous_daily_additive_back_adjustment"])
    packed = {
        "row_index": index,
        "completed_timestamp_utc": row["derived_completed_bar_end_utc"],
        "trading_date": row["completed_trading_date"],
        "raw_symbol": row["raw_symbol"],
        "session_id": _session_id(row["derived_completed_bar_end_utc"]),
        "row_locator": f"{RUN_ID}_{role}_{index:04d}_{row['derived_completed_bar_end_utc'].replace('-', '').replace(':', '')}_{row['raw_symbol']}",
        "close_price": _num(float(row["close"]) + adjustment),
        "source_provider_csv": row["source_provider_csv"],
        "source_provider_csv_sha256": row["source_provider_csv_sha256"],
        "source_row_hash": _row_hash("strategy_facing_hourly_available_bars", row),
        "readiness_status": "READY_COMPLETED_BAR_DATABENTO_PRETEST_DEV_RECON",
    }
    packed["row_hash"] = _row_hash(f"S27_V2_PRETEST_{role}_ROW", packed)
    return packed


def _valuation_row(row: dict[str, str], runtime: dict[str, Any], index: int) -> dict[str, Any]:
    packed = _hourly_pack_row(row, runtime, "VALUATION_MARK", index)
    packed["valuation_convention_label"] = VALUATION_CONVENTION_LABEL
    packed["readiness_status"] = "READY_COMPLETED_BAR_DATABENTO_PRETEST_VALUATION_MARK_DEV_RECON"
    packed["row_hash"] = _row_hash("S27_V2_PRETEST_VALUATION_MARK_ROW", packed)
    return packed


def _daily_summary_rows(selection: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: dict[str, dict[str, Any]] = {}
    for row in selection:
        runtime = row["runtime"]
        seen[runtime["previous_daily_trading_date"]] = {
            "completed_timestamp_utc": f"{runtime['previous_daily_trading_date']}T00:00:00Z",
            "trading_date": runtime["previous_daily_trading_date"],
            "raw_symbol": runtime["previous_daily_raw_symbol"],
            "row_locator": f"{RUN_ID}_DAILY_CONTINUOUS_{runtime['previous_daily_trading_date'].replace('-', '')}",
            "close_price": _num(float(runtime["previous_daily_raw_close"]) + float(runtime["previous_daily_additive_back_adjustment"])),
            "annual_percentage_sigma": runtime["annual_percentage_sigma"],
            "runtime_evidence_row_hash": runtime["row_hash"],
            "readiness_status": "READY_ROLLING_STRICT_PRIOR_DAILY_EVIDENCE_SUMMARY",
        }
    return list(seen.values())


def _daily_current_rows(selection: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for index, row in enumerate(selection, 1):
        runtime = row["runtime"]
        rows.append(
            {
                "row_index": index,
                "completed_timestamp_utc": f"{runtime['previous_daily_trading_date']}T00:00:00Z",
                "trading_date": runtime["previous_daily_trading_date"],
                "raw_symbol": runtime["previous_daily_raw_symbol"],
                "row_locator": f"{RUN_ID}_DAILY_CURRENT_{index:04d}_{runtime['previous_daily_trading_date'].replace('-', '')}",
                "close_price": runtime["previous_daily_raw_close"],
                "runtime_evidence_row_hash": runtime["row_hash"],
                "readiness_status": "READY_ROLLING_STRICT_PRIOR_CURRENT_CONTRACT_DAILY_EVIDENCE",
            }
        )
    return rows


def _session_rows(selection: list[dict[str, Any]]) -> list[dict[str, str]]:
    rows: dict[str, dict[str, str]] = {}
    for selected in selection:
        for role in ("decision", "fill", "mark"):
            ts = selected[role]["derived_completed_bar_end_utc"]
            sid = _session_id(ts)
            start, end = _session_bounds(ts)
            rows[sid] = {
                "session_id": sid,
                "session_start_utc": start,
                "session_end_utc": end,
                "calendar_status": "LOCAL_DATABENTO_PRE2023_COMPLETED_BAR_SESSION_CONTEXT",
                "readiness_status": "READY_SESSION_CONTEXT_DEV_RECON_ONLY",
            }
    return list(rows.values())


def _roll_rows(rolls: list[dict[str, str]], cutoff: str) -> list[dict[str, str]]:
    rows = []
    for index, row in enumerate([roll for roll in rolls if roll["roll_transition_date"] <= cutoff], 1):
        rows.append(
            {
                "roll_id": f"{RUN_ID}_ROLL_{index:04d}_{row['roll_transition_date'].replace('-', '')}",
                "old_contract_key": row["old_contract_key"],
                "new_contract_key": row["new_contract_key"],
                "roll_transition_date": row["roll_transition_date"],
                "additive_delta_to_prior_history": row["additive_delta_to_prior_history"],
                "readiness_status": "READY_DATABENTO_PRE2023_ROLL_CONTEXT_DEV_RECON_ONLY",
            }
        )
    return rows


def _cost_rows() -> list[dict[str, str]]:
    return [
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


def _point_in_time_continuous_series(
    continuous: list[dict[str, str]],
    rolls: list[dict[str, str]],
    cutoff_date: str,
) -> list[dict[str, Any]]:
    active_rows = [row for row in continuous if row["completed_trading_date"] <= cutoff_date]
    known_rolls = [row for row in rolls if row["roll_transition_date"] <= cutoff_date]
    current_contract_key = active_rows[-1]["active_contract_key"]
    offsets_by_contract = {current_contract_key: 0.0}
    for roll in reversed(known_rolls):
        if roll["new_contract_key"] in offsets_by_contract:
            offsets_by_contract[roll["old_contract_key"]] = (
                offsets_by_contract[roll["new_contract_key"]] + float(roll["additive_delta_to_prior_history"])
            )
    rows = []
    for row in active_rows:
        if row["active_contract_key"] not in offsets_by_contract:
            raise SystemExit(f"fail closed: point-in-time offset missing for {row['active_contract_key']}")
        adjustment = offsets_by_contract[row["active_contract_key"]]
        rows.append(
            {
                **row,
                "additive_back_adjustment": adjustment,
                "continuous_close": float(row["raw_close"]) + adjustment,
                "point_in_time_roll_cutoff_date": cutoff_date,
            }
        )
    return rows


def _build_sigma_rows(continuous: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    closes = [float(row["continuous_close"]) for row in continuous]
    dates = [row["completed_trading_date"] for row in continuous]
    alpha = 2.0 / (SIGMA_EWMA_SPAN + 1.0)
    for index in range(SIGMA_WINDOW_ROWS - 1, len(continuous)):
        window = closes[index - SIGMA_WINDOW_ROWS + 1 : index + 1]
        returns = [window[i] / window[i - 1] - 1.0 for i in range(1, len(window))]
        variance = returns[0] * returns[0]
        for value in returns[1:]:
            variance = alpha * value * value + (1.0 - alpha) * variance
        rows.append({"completed_trading_date": dates[index], "sigma_i_t": math.sqrt(variance) * math.sqrt(TRADING_DAYS_PER_YEAR)})
    return rows


def _build_vqm_rows(sigma_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    alpha = 2.0 / (VQM_EWMA_SPAN + 1.0)
    smoothed = None
    sigma_values = [float(row["sigma_i_t"]) for row in sigma_rows]
    prefix = [0.0]
    for sigma in sigma_values:
        prefix.append(prefix[-1] + sigma)
    historical_v = []
    for index, sigma_row in enumerate(sigma_rows):
        if index < TEN_YEAR_SIGMA_ROWS:
            continue
        ten_year_avg = (prefix[index] - prefix[index - TEN_YEAR_SIGMA_ROWS]) / TEN_YEAR_SIGMA_ROWS
        sigma = sigma_values[index]
        v = sigma / ten_year_avg
        historical_v.append(v)
        q = sum(1 for value in historical_v if value <= v) / len(historical_v)
        raw_m = 2.0 - 1.5 * q
        smoothed = raw_m if smoothed is None else alpha * raw_m + (1.0 - alpha) * smoothed
        rows.append(
            {
                "completed_trading_date": sigma_row["completed_trading_date"],
                "sigma_i_t": sigma,
                "relative_volatility_v": v,
                "quantile_q": q,
                "vol_multiplier_m_ewma10": smoothed,
            }
        )
    return rows


def _ewma(values: tuple[float, ...], span: int) -> float:
    alpha = 2.0 / (span + 1.0)
    current = values[0]
    for value in values[1:]:
        current = alpha * value + (1.0 - alpha) * current
    return current


def _formula_limit(target_position: int, base_position: float, ewma5: float, sigma_price: float, multiplier_m: float, trend: float) -> float | None:
    if target_position <= 0 or trend <= 0.0:
        return None
    target_capped = target_position / base_position * FORECAST_TO_POSITION_DIVISOR
    target_risk = target_capped / FORECAST_SCALAR_VALUE
    pre_vol_risk = target_risk / multiplier_m
    return ewma5 - pre_vol_risk * sigma_price


def _round_limit(price: float, side: str) -> float:
    if side == "BUY":
        return math.floor((price + 1e-12) / ZN_TICK_SIZE) * ZN_TICK_SIZE
    if side == "SELL":
        return math.ceil((price - 1e-12) / ZN_TICK_SIZE) * ZN_TICK_SIZE
    return 0.0


def _limit_fill(side: str, close_price: float, limit_price: float) -> bool:
    return (side == "BUY" and close_price <= limit_price) or (side == "SELL" and close_price >= limit_price)


def _round_half_away_from_zero(value: float) -> int:
    magnitude = math.floor(abs(value) + 0.5)
    return magnitude if value >= 0.0 else -magnitude


def _clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def _session_id(timestamp: str) -> str:
    start, end = _session_bounds(timestamp)
    return f"UTC_ZN_PRE2023_{start}_{end}"


def _session_bounds(timestamp: str) -> tuple[str, str]:
    completed = _parse_ts(timestamp)
    if completed.hour >= 22:
        start = completed.replace(hour=22, minute=0, second=0, microsecond=0)
        end = start + timedelta(hours=23)
    else:
        end = completed.replace(hour=21, minute=0, second=0, microsecond=0)
        start = end - timedelta(hours=23)
    return _z(start), _z(end)


def _parse_ts(timestamp: str) -> datetime:
    return datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def _z(value: datetime) -> str:
    return value.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise SystemExit(f"fail closed: refusing empty CSV {path}")
    fields = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="ascii") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows([{key: _csv_value(value) for key, value in row.items()} for row in rows])


def _write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="ascii")


def _write_sha256s(path: Path, root: Path) -> None:
    lines = [
        f"{_sha256(file)}  {file.relative_to(root).as_posix()}"
        for file in sorted(root.iterdir())
        if file.is_file() and file != path
    ]
    path.write_text("\n".join(lines) + "\n", encoding="ascii")


def _csv_row_count(path: Path) -> int:
    with path.open(newline="", encoding="ascii") as handle:
        return len(list(csv.DictReader(handle)))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def _row_hash(label: str, row: dict[str, Any]) -> str:
    return hashlib.sha256(
        json.dumps({"artifact": label, "row": row}, sort_keys=True, separators=(",", ":")).encode("ascii")
    ).hexdigest().upper()


def _num(value: Any) -> str:
    return format(float(value), ".17g")


def _csv_value(value: Any) -> str:
    if isinstance(value, bool):
        return "TRUE" if value else "FALSE"
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(value, sort_keys=True, separators=(",", ":"))
    return str(value)


def _process_doc(selection: list[dict[str, Any]], manifest: dict[str, Any]) -> str:
    final = manifest["filled_sell_completion"]
    return f"""# S27_V2 Pre-TEST Development/Reconciliation Filled Sell Completion Pack Build Result

Date: 2026-06-11

Status:

```text
{STATUS}
```

Declared pack:

```text
{OUTPUT_PACK.relative_to(ROOT)}
```

This pack is local-only, pre-2023, and built only from already-local ZN source
ledgers. It selects the earliest 2022 organic filled sell-side reduction found
after strict-prior warmups/evidence are populated. The pack preserves 2023 for
TEST and emits no result interpretation, no promotion evidence, and no
source-faithful evidence claim.

Selected row count:

```text
{len(selection)}
```

Filled sell completion:

```text
row_index = {final['row_index']}
decision_timestamp_utc = {final['decision_timestamp_utc']}
fill_timestamp_utc = {final['fill_timestamp_utc']}
raw_symbol = {final['raw_symbol']}
starting_position_contracts = {final['starting_position_contracts']}
desired_position_contracts = {final['desired_position_contracts']}
position_change_contracts = {final['position_change_contracts']}
order_side = {final['order_side']}
order_quantity = {final['order_quantity']}
limit_order_price = {final['limit_order_price']}
fill_candidate_close = {final['fill_candidate_close']}
fill_executed = {final['fill_executed']}
```

Rolling strict-prior evidence:

```text
{manifest['history_evidence']['rolling_strict_prior_daily_evidence']}
{manifest['history_evidence']['point_in_time_roll_offsets']}
```

Non-authorizations:

```text
{chr(10).join(NON_AUTHORIZATIONS)}
```
"""


if __name__ == "__main__":
    main()
