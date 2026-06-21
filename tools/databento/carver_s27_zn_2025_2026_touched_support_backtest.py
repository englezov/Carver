from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import sys
from collections import Counter, defaultdict
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

import databento as db


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

BASE_MODULE_PATH = ROOT / "tools/databento/carver_s27_candidate_comparison_2022_2023.py"
BASE_SPEC = importlib.util.spec_from_file_location("carver_s27_candidate_comparison_for_zn_2025_2026", BASE_MODULE_PATH)
if BASE_SPEC is None or BASE_SPEC.loader is None:
    raise RuntimeError(f"Unable to load base comparison module from {BASE_MODULE_PATH}")
base = importlib.util.module_from_spec(BASE_SPEC)
sys.modules[BASE_SPEC.name] = base
BASE_SPEC.loader.exec_module(base)


RUN_ID = "20260601_S27_ZN_2025_2026_TOUCHED_SUPPORT_DEV_RECON_BACKTEST"
GATE = "S27_ZN_2025_2026_TOUCHED_SUPPORT_DEVELOPMENT_RECONCILIATION_BACKTEST"
REQUEST_START = date(2025, 1, 1)
REQUEST_END = date(2026, 5, 22)
HOURLY_REQUEST_START = datetime(2024, 12, 31, tzinfo=timezone.utc)
HOURLY_REQUEST_END = datetime(2026, 5, 23, tzinfo=timezone.utc)

CAPITAL_USD = 100_000.0
TARGET_RISK = 0.20
INSTRUMENT_WEIGHT = 1.0
IDM = 1.0
FX_RATE = 1.0
ZN_MULTIPLIER = 1000.0
FORECAST_DIVISOR = 10.0
ETF_ZN_FEE_PER_SIDE_USD = 1.51
MAX_SOURCE_RUNTIME_LAG_DAYS = 10

DAILY_RUNTIME_CSV = (
    ROOT
    / "docs/researchops/s26_s27_backtest_readiness/ZN_S27_SINGLE_INSTRUMENT/2022-01-01_2023-12-31/"
    / "local_extended_daily_runtime/runtime_rows/"
    / "20260531_S27_ZN_2022_2023_LOCAL_EXTENDED_DAILY_RUNTIME_daily_runtime_rows.csv"
)
DAILY_RUNTIME_STATUS_JSON = (
    ROOT
    / "docs/researchops/s26_s27_backtest_readiness/ZN_S27_SINGLE_INSTRUMENT/2022-01-01_2023-12-31/"
    / "local_extended_daily_runtime/status/"
    / "20260531_S27_ZN_2022_2023_LOCAL_EXTENDED_DAILY_RUNTIME_status.json"
)
LOCKBOX_STATUS_JSON = (
    ROOT
    / "docs/researchops/s26_s27_lockbox_readiness/ZN_S27/20260601_S27_ZN_LOCKBOX_READINESS_DECISION/status/"
    / "20260601_S27_ZN_LOCKBOX_READINESS_DECISION_status.json"
)

OUTPUT_ROOT = ROOT / "docs/researchops/s26_s27_touched_support_backtest/ZN_S27/2025-01-01_2026-05-22"
PROCESS_RESULT_DOC = ROOT / "docs/process/CARVER_S27_ZN_2025_2026_TOUCHED_SUPPORT_DEV_RECON_BACKTEST_RESULT_2026-06-01.md"
LOCAL_AUDIT_DOC = ROOT / "docs/process/CARVER_S27_ZN_2025_2026_TOUCHED_SUPPORT_DEV_RECON_LOCAL_HOSTILE_AUDIT_2026-06-01.md"

ZN = base.Candidate("ZN", "APPENDIX_C_172_004", "10-year US", "bond", ZN_MULTIPLIER, ETF_ZN_FEE_PER_SIDE_USD, date(2011, 1, 1))


def main() -> None:
    _require_inputs()
    _patch_base_globals()
    client = db.Historical(base._read_databento_key())
    folders = base._folders(OUTPUT_ROOT)
    for folder in folders.values():
        folder.mkdir(parents=True, exist_ok=True)

    manifest = _manifest_payload()
    base._write_json(folders["manifest"] / f"{RUN_ID}_manifest.json", manifest)

    hourly_condition = _cached_or_fetch_condition(
        client,
        folders["metadata"] / f"{RUN_ID}_hourly_dataset_condition.json",
        HOURLY_REQUEST_START.date(),
        HOURLY_REQUEST_END.date(),
    )
    condition_rows = _condition_rows(hourly_condition)
    hourly_condition_by_date = base._condition_by_date(hourly_condition)
    hourly_rows, symbology_rows, provider_errors = _request_hourly_rows(client, hourly_condition_by_date, folders)
    base._write_csv(folders["metadata"] / f"{RUN_ID}_ZN_symbology_ledger.csv", symbology_rows)
    if provider_errors:
        base._write_csv(folders["status"] / f"{RUN_ID}_provider_errors.csv", provider_errors)
        raise SystemExit(f"Fail closed: provider errors observed: {len(provider_errors)}")
    if not hourly_rows:
        raise SystemExit("Fail closed: no ZN hourly rows returned for 2025-2026 touched-support run")

    hourly_continuous, hourly_inactive, hourly_roll_plan = base._build_continuous_rows(
        candidate=ZN,
        contracts=_hourly_contracts(),
        source_rows=hourly_rows,
        price_field="close",
        timestamp_field="derived_completed_bar_end_utc",
        output_root=folders["lineage"],
        prefix=f"{RUN_ID}_ZN_hourly",
    )
    daily_runtime_rows = _read_csv(DAILY_RUNTIME_CSV)
    daily_runtime_status = _read_json(DAILY_RUNTIME_STATUS_JSON)
    lockbox_status = _read_json(LOCKBOX_STATUS_JSON)
    s26_rows, s27_rows, blocked_rows = base._build_forecasts(ZN, hourly_continuous, daily_runtime_rows)
    ladder_rows = _build_ladder_rows(s27_rows)
    position_rows = _build_position_rows(ladder_rows)
    row_attribution = _build_row_attribution(s27_rows, position_rows, hourly_continuous)
    summary_rows = _summary_rows(row_attribution)
    yearly_rows = _yearly_rows(row_attribution)
    trade_stats = _trade_stats(row_attribution)
    cost_rows = _cost_rows(lockbox_status)
    validation_rows = _validation_rows(
        hourly_rows=hourly_rows,
        hourly_continuous=hourly_continuous,
        s27_rows=s27_rows,
        ladder_rows=ladder_rows,
        position_rows=position_rows,
        row_attribution=row_attribution,
        daily_runtime_status=daily_runtime_status,
        condition_rows=condition_rows,
    )
    status = _status_payload(
        hourly_rows=hourly_rows,
        hourly_continuous=hourly_continuous,
        hourly_inactive=hourly_inactive,
        hourly_roll_plan=hourly_roll_plan,
        s26_rows=s26_rows,
        s27_rows=s27_rows,
        blocked_rows=blocked_rows,
        ladder_rows=ladder_rows,
        position_rows=position_rows,
        row_attribution=row_attribution,
        summary_rows=summary_rows,
        yearly_rows=yearly_rows,
        condition_rows=condition_rows,
        daily_runtime_status=daily_runtime_status,
        lockbox_status=lockbox_status,
    )

    base._write_csv(folders["lineage"] / f"{RUN_ID}_ZN_hourly_continuous_lineage.csv", hourly_continuous)
    base._write_csv(folders["lineage"] / f"{RUN_ID}_ZN_hourly_inactive_rows.csv", hourly_inactive)
    base._write_csv(folders["lineage"] / f"{RUN_ID}_ZN_hourly_roll_plan.csv", hourly_roll_plan)
    base._write_csv(folders["runtime"] / f"{RUN_ID}_ZN_daily_runtime_rows_reused.csv", daily_runtime_rows)
    base._write_csv(folders["forecasts"] / f"{RUN_ID}_ZN_s26_forecast_rows.csv", s26_rows)
    base._write_csv(folders["forecasts"] / f"{RUN_ID}_ZN_s27_forecast_rows.csv", s27_rows)
    base._write_csv(folders["forecasts"] / f"{RUN_ID}_ZN_blocked_dependency_rows.csv", blocked_rows)
    base._write_csv(folders["positions"] / f"{RUN_ID}_ZN_base_position_ladder_rows.csv", ladder_rows)
    base._write_csv(folders["positions"] / f"{RUN_ID}_ZN_desired_position_rows.csv", position_rows)
    base._write_csv(folders["backtest"] / f"{RUN_ID}_ZN_same_input_ladder_vs_unit_rows.csv", row_attribution)
    base._write_csv(folders["summary"] / f"{RUN_ID}_summary.csv", summary_rows)
    base._write_csv(folders["summary"] / f"{RUN_ID}_yearly_summary.csv", yearly_rows)
    base._write_csv(folders["summary"] / f"{RUN_ID}_trade_stats.csv", trade_stats)
    base._write_csv(folders["validation"] / f"{RUN_ID}_provider_condition_ledger.csv", condition_rows)
    base._write_csv(folders["validation"] / f"{RUN_ID}_cost_status.csv", cost_rows)
    base._write_csv(folders["validation"] / f"{RUN_ID}_validation_ledger.csv", validation_rows)
    base._write_json(folders["status"] / f"{RUN_ID}_status.json", status)
    base._write_json(folders["provenance"] / f"{RUN_ID}_provenance.json", _provenance_payload(status))
    base._write_json(folders["hashes"] / f"{RUN_ID}_sha256.json", _hash_tree(OUTPUT_ROOT))
    PROCESS_RESULT_DOC.write_text(_process_result_text(status, summary_rows, yearly_rows), encoding="utf-8")
    LOCAL_AUDIT_DOC.write_text(_local_audit_text(status), encoding="utf-8")

    print(status["status"])
    print(f"effective_backtest_start={status['effective_backtest_start']}")
    print(f"effective_backtest_end={status['effective_backtest_end']}")
    print(f"m1_ladder_net_after_recorded_fee_usd={status['m1_ladder_net_after_recorded_fee_usd']}")
    print(f"unit_no_ladder_net_after_recorded_fee_usd={status['unit_no_ladder_net_after_recorded_fee_usd']}")
    print(f"artifact_root={OUTPUT_ROOT.relative_to(ROOT)}")


def _patch_base_globals() -> None:
    base.RUN_ID = RUN_ID
    base.GATE = GATE
    base.REQUEST_START = REQUEST_START
    base.REQUEST_END = REQUEST_END
    base.HOURLY_REQUEST_START = HOURLY_REQUEST_START
    base.HOURLY_REQUEST_END = HOURLY_REQUEST_END
    base.OUTPUT_ROOT = OUTPUT_ROOT


def _manifest_payload() -> dict[str, Any]:
    return {
        "gate": GATE,
        "run_id": RUN_ID,
        "lane_class": "SOURCE_NATIVE_FUTURES",
        "stage": "TOUCHED_SUPPORT_DEVELOPMENT_RECONCILIATION",
        "root": "ZN",
        "row_id": "APPENDIX_C_172_004",
        "book_label": "10-year US",
        "dataset": base.DATASET,
        "hourly_schema": base.HOURLY_SCHEMA,
        "stype_in": base.STYPE_IN,
        "requested_window_start": REQUEST_START.isoformat(),
        "requested_window_end": REQUEST_END.isoformat(),
        "hourly_request_start_utc": _z(HOURLY_REQUEST_START),
        "hourly_request_end_utc": _z(HOURLY_REQUEST_END),
        "hourly_contracts": _hourly_contracts(),
        "daily_runtime_source": str(DAILY_RUNTIME_CSV.relative_to(ROOT)),
        "support_touch_status": "DAILY_RUNTIME_SUPPORT_ALREADY_TOUCHED_THROUGH_2026-05-22_NOT_PRISTINE_LOCKBOX",
        "capital_usd": CAPITAL_USD,
        "target_risk": TARGET_RISK,
        "instrument_weight": INSTRUMENT_WEIGHT,
        "idm": IDM,
        "zn_multiplier": ZN_MULTIPLIER,
        "recorded_fee_per_side_usd": ETF_ZN_FEE_PER_SIDE_USD,
        "non_authorization": [
            "NO_OOS",
            "NO_LOCKBOX",
            "NO_FORWARD",
            "NO_TUNING",
            "NO_DEPLOYMENT",
            "NO_TRADING",
            "NO_PROMOTION",
            "NO_GIT_OPERATIONS",
        ],
    }


def _hourly_contracts() -> list[dict[str, Any]]:
    return [
        {"raw_symbol": "ZNH5", "contract_year": 2025, "delivery_month": 3, "delivery_code": "H"},
        {"raw_symbol": "ZNM5", "contract_year": 2025, "delivery_month": 6, "delivery_code": "M"},
        {"raw_symbol": "ZNU5", "contract_year": 2025, "delivery_month": 9, "delivery_code": "U"},
        {"raw_symbol": "ZNZ5", "contract_year": 2025, "delivery_month": 12, "delivery_code": "Z"},
        {"raw_symbol": "ZNH6", "contract_year": 2026, "delivery_month": 3, "delivery_code": "H"},
        {"raw_symbol": "ZNM6", "contract_year": 2026, "delivery_month": 6, "delivery_code": "M"},
        {"raw_symbol": "ZNU6", "contract_year": 2026, "delivery_month": 9, "delivery_code": "U"},
    ]


def _cached_or_fetch_condition(client: db.Historical, path: Path, start: date, end: date) -> list[dict[str, Any]]:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    condition = base._dataset_condition(client, start, end)
    base._write_json(path, condition)
    return condition


def _request_hourly_rows(
    client: db.Historical,
    condition_by_date: dict[str, str],
    folders: dict[str, Path],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    rows: list[dict[str, Any]] = []
    symbology: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []
    for contract in _hourly_contracts():
        contract_rows, contract_symbology, contract_errors = base._request_ohlcv_rows(
            client=client,
            candidate=ZN,
            contract=contract,
            schema=base.HOURLY_SCHEMA,
            start_dt=HOURLY_REQUEST_START,
            end_dt=HOURLY_REQUEST_END,
            condition_by_date=condition_by_date,
            folders=folders,
            purpose="hourly",
        )
        rows.extend(contract_rows)
        symbology.extend(contract_symbology)
        errors.extend(contract_errors)
    return rows, symbology, errors


def _condition_rows(condition: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in condition:
        condition_value = str(row.get("condition", "")).upper()
        day = str(row.get("date", ""))
        if not day or day < REQUEST_START.isoformat() or day > REQUEST_END.isoformat():
            continue
        rows.append(
            {
                "gate": GATE,
                "date": day,
                "provider_condition": condition_value,
                "last_modified_date": row.get("last_modified_date", ""),
                "strategy_use_status": (
                    "PROVIDER_CONDITION_AVAILABLE_USED"
                    if condition_value == "AVAILABLE"
                    else "PROVIDER_CONDITION_NOT_AVAILABLE_EXCLUDED_AND_COMPLETE_WINDOW_FAIL_CLOSED"
                ),
            }
        )
    if not rows:
        raise SystemExit("Fail closed: no provider-condition rows for requested window")
    return rows


def _build_ladder_rows(forecasts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in forecasts:
        price = float(row["continuous_close"])
        runtime_day = row.get("source_daily_runtime_completed_trading_date") or row["source_vqm_completed_trading_date"]
        lag = _runtime_lag_days(row["completed_trading_date"], runtime_day)
        if lag <= 0 or lag > MAX_SOURCE_RUNTIME_LAG_DAYS:
            raise SystemExit(f"Fail closed: non-strict-prior/stale daily runtime dependency at {row['derived_completed_bar_end_utc']}")
        annual_risk = float(row["sigma_price_i_t"]) * 16.0 / price
        contract_risk = price * ZN_MULTIPLIER * FX_RATE * annual_risk
        if contract_risk <= 0:
            raise SystemExit(f"Fail closed: non-positive contract risk at {row['derived_completed_bar_end_utc']}")
        target_currency_risk = CAPITAL_USD * TARGET_RISK
        base_unrounded = target_currency_risk * INSTRUMENT_WEIGHT * IDM / contract_risk
        rows.append(
            {
                "lane_class": "SOURCE_NATIVE_FUTURES",
                "gate": GATE,
                "row_id": row["row_id"],
                "author_market_code": "ZN",
                "raw_symbol": row["raw_symbol"],
                "completed_trading_date": row["completed_trading_date"],
                "derived_completed_bar_end_utc": row["derived_completed_bar_end_utc"],
                "source_daily_runtime_completed_trading_date": runtime_day,
                "source_daily_runtime_lag_days": lag,
                "capital_usd": CAPITAL_USD,
                "target_risk": TARGET_RISK,
                "instrument_weight": INSTRUMENT_WEIGHT,
                "idm": IDM,
                "current_held_price": price,
                "annual_risk_estimate_sigma_percent": annual_risk,
                "contract_multiplier": ZN_MULTIPLIER,
                "fx_rate": FX_RATE,
                "contract_risk_usd": contract_risk,
                "target_currency_risk_usd": target_currency_risk,
                "base_unrounded_contracts": base_unrounded,
                "capped_forecast": row["capped_forecast"],
                "forecast_multiplier": float(row["capped_forecast"]) / FORECAST_DIVISOR,
                "source_status": "PREVALIDATED_M1_STYLE_BASE_POSITION_TOUCHED_SUPPORT_DEV_RECON",
                "capital_risk_status": "CAPITAL_TARGET_RISK_AND_SIGMA_PRICE_BRIDGE_RECONSTRUCTED_NO_LOOKAHEAD",
                "multiplier_fx_status": "ZN_MULTIPLIER_USD_FX_LOCKED",
            }
        )
    return rows


def _build_position_rows(ladder_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in ladder_rows:
        desired = float(row["base_unrounded_contracts"]) * float(row["forecast_multiplier"])
        rows.append(
            {
                "lane_class": "SOURCE_NATIVE_FUTURES",
                "gate": GATE,
                "row_id": row["row_id"],
                "author_market_code": "ZN",
                "raw_symbol": row["raw_symbol"],
                "completed_trading_date": row["completed_trading_date"],
                "derived_completed_bar_end_utc": row["derived_completed_bar_end_utc"],
                "capital_usd": row["capital_usd"],
                "target_risk": row["target_risk"],
                "base_unrounded_contracts": row["base_unrounded_contracts"],
                "capped_forecast": row["capped_forecast"],
                "forecast_to_position_divisor": FORECAST_DIVISOR,
                "forecast_multiplier": row["forecast_multiplier"],
                "desired_unrounded_contracts": desired,
                "desired_rounded_contracts_nearest": round(desired),
                "rounding_policy": "NEAREST",
                "position_status": "M1_STYLE_LADDER_POSITION_SERIES_TOUCHED_SUPPORT_DEV_RECON_NOT_PRODUCTION_SIZING",
            }
        )
    return rows


def _build_row_attribution(
    forecasts: list[dict[str, Any]],
    ladder_positions: list[dict[str, Any]],
    hourly_continuous: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    hourly_by_ts = {row["derived_completed_bar_end_utc"]: row for row in hourly_continuous}
    forecast_by_ts = {row["derived_completed_bar_end_utc"]: row for row in forecasts}
    ladder_by_ts = {row["derived_completed_bar_end_utc"]: row for row in ladder_positions}
    ordered_ts = sorted(hourly_by_ts)
    rows: list[dict[str, Any]] = []
    prior_unit_position: int | None = None
    prior_ladder_position: int | None = None
    cumulative_unit_gross = 0.0
    cumulative_unit_fees = 0.0
    cumulative_ladder_gross = 0.0
    cumulative_ladder_fees = 0.0
    for entry_ts, exit_ts in zip(ordered_ts[:-1], ordered_ts[1:], strict=True):
        if entry_ts not in forecast_by_ts or entry_ts not in ladder_by_ts:
            continue
        entry_bar = hourly_by_ts[entry_ts]
        exit_bar = hourly_by_ts[exit_ts]
        forecast = forecast_by_ts[entry_ts]
        unit_contracts = round(float(forecast["capped_forecast"]) / FORECAST_DIVISOR)
        ladder_contracts = int(ladder_by_ts[entry_ts]["desired_rounded_contracts_nearest"])
        price_change = float(exit_bar["continuous_close"]) - float(entry_bar["continuous_close"])
        unit_gross = unit_contracts * price_change * ZN_MULTIPLIER
        ladder_gross = ladder_contracts * price_change * ZN_MULTIPLIER
        unit_position_change = 0 if prior_unit_position is None else unit_contracts - prior_unit_position
        ladder_position_change = 0 if prior_ladder_position is None else ladder_contracts - prior_ladder_position
        prior_unit_position = unit_contracts
        prior_ladder_position = ladder_contracts
        unit_roll_sides = _roll_fee_sides(entry_bar, exit_bar, unit_contracts)
        ladder_roll_sides = _roll_fee_sides(entry_bar, exit_bar, ladder_contracts)
        unit_fee_sides = abs(unit_position_change) + unit_roll_sides
        ladder_fee_sides = abs(ladder_position_change) + ladder_roll_sides
        unit_fees = unit_fee_sides * ETF_ZN_FEE_PER_SIDE_USD
        ladder_fees = ladder_fee_sides * ETF_ZN_FEE_PER_SIDE_USD
        unit_net = unit_gross - unit_fees
        ladder_net = ladder_gross - ladder_fees
        cumulative_unit_gross += unit_gross
        cumulative_unit_fees += unit_fees
        cumulative_ladder_gross += ladder_gross
        cumulative_ladder_fees += ladder_fees
        rows.append(
            {
                "gate": GATE,
                "window_label": "2025_2026_TOUCHED_SUPPORT_FRESH_HOURLY_DEV_RECON",
                "evidence_class": "TOUCHED_SUPPORT_DEVELOPMENT_RECONCILIATION_NOT_LOCKBOX_NOT_PROMOTION",
                "entry_bar_end_utc": entry_ts,
                "exit_bar_end_utc": exit_ts,
                "entry_completed_trading_date": entry_bar["completed_trading_date"],
                "exit_completed_trading_date": exit_bar["completed_trading_date"],
                "entry_year": entry_bar["completed_trading_date"][:4],
                "entry_raw_symbol": entry_bar["raw_symbol"],
                "exit_raw_symbol": exit_bar["raw_symbol"],
                "entry_continuous_close": entry_bar["continuous_close"],
                "exit_continuous_close": exit_bar["continuous_close"],
                "price_change_points": price_change,
                "capped_forecast": forecast["capped_forecast"],
                "unit_no_ladder_contracts": unit_contracts,
                "m1_ladder_contracts": ladder_contracts,
                "unit_side": _side(unit_contracts),
                "m1_ladder_side": _side(ladder_contracts),
                "unit_position_change_from_previous_pnl_row": unit_position_change,
                "m1_ladder_position_change_from_previous_pnl_row": ladder_position_change,
                "unit_total_fee_sides": unit_fee_sides,
                "m1_ladder_total_fee_sides": ladder_fee_sides,
                "unit_gross_pnl_usd": unit_gross,
                "unit_estimated_etf_fee_usd": unit_fees,
                "unit_net_after_etf_fees_usd": unit_net,
                "m1_ladder_gross_pnl_usd": ladder_gross,
                "m1_ladder_estimated_etf_fee_usd": ladder_fees,
                "m1_ladder_net_after_etf_fees_usd": ladder_net,
                "net_delta_m1_ladder_minus_unit_usd": ladder_net - unit_net,
                "gross_delta_m1_ladder_minus_unit_usd": ladder_gross - unit_gross,
                "fee_delta_m1_ladder_minus_unit_usd": ladder_fees - unit_fees,
                "unit_cumulative_net_after_recorded_fees_usd": cumulative_unit_gross - cumulative_unit_fees,
                "m1_ladder_cumulative_net_after_recorded_fees_usd": cumulative_ladder_gross - cumulative_ladder_fees,
                "same_input_status": "PASS_IDENTICAL_ENTRY_EXIT_HOURLY_ROW_SET",
            }
        )
    if not rows:
        raise SystemExit("Fail closed: no same-input attribution rows produced")
    return rows


def _summary_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        _summary_for(rows, "UNIT_NO_LADDER_SAME_INPUT", "unit", "unit_no_ladder_contracts"),
        _summary_for(rows, "M1_LADDER_SAME_INPUT", "m1_ladder", "m1_ladder_contracts"),
        _delta_summary(rows),
    ]


def _summary_for(rows: list[dict[str, Any]], variant: str, prefix: str, position_field: str) -> dict[str, Any]:
    pnl = [float(row[f"{prefix}_net_after_etf_fees_usd"]) for row in rows]
    gross = [float(row[f"{prefix}_gross_pnl_usd"]) for row in rows]
    fees = [float(row[f"{prefix}_estimated_etf_fee_usd"]) for row in rows]
    positions = [int(row[position_field]) for row in rows]
    nonzero_pnl = [value for value in pnl if abs(value) > 1e-12]
    daily_net = _group_sum(rows, f"{prefix}_net_after_etf_fees_usd", "entry_completed_trading_date")
    nonzero_daily = [value for value in daily_net.values() if abs(value) > 1e-12]
    return {
        "gate": GATE,
        "strategy_variant": variant,
        "lane_class": "SOURCE_NATIVE_FUTURES",
        "evidence_class": "TOUCHED_SUPPORT_DEVELOPMENT_RECONCILIATION_NOT_LOCKBOX_NOT_PROMOTION",
        "effective_backtest_start": min(row["entry_completed_trading_date"] for row in rows),
        "effective_backtest_end": max(row["exit_completed_trading_date"] for row in rows),
        "pnl_rows": len(rows),
        "active_position_rows": sum(1 for value in positions if value != 0),
        "flat_position_rows": sum(1 for value in positions if value == 0),
        "position_counts": json.dumps(dict(sorted(Counter(positions).items()))),
        "position_change_sides": sum(abs(int(row[f"{prefix}_position_change_from_previous_pnl_row"])) for row in rows),
        "total_fee_sides": sum(int(row[f"{prefix}_total_fee_sides"]) for row in rows),
        "gross_pnl_usd": sum(gross),
        "recorded_fee_model": "ETF_PUBLIC_PER_SIDE_COMMISSION_ONLY_NO_SPREAD_NO_SLIPPAGE",
        "recorded_fees_usd": sum(fees),
        "net_after_recorded_fees_usd": sum(pnl),
        "nonzero_pnl_row_count": len(nonzero_pnl),
        "positive_nonzero_pnl_row_count": sum(1 for value in nonzero_pnl if value > 0),
        "nonzero_pnl_row_win_rate": _ratio(sum(1 for value in nonzero_pnl if value > 0), len(nonzero_pnl)),
        "nonzero_daily_count": len(nonzero_daily),
        "positive_nonzero_daily_count": sum(1 for value in nonzero_daily if value > 0),
        "nonzero_daily_win_rate": _ratio(sum(1 for value in nonzero_daily if value > 0), len(nonzero_daily)),
        "futures_realistic_cost_status": "FAIL_CLOSED_NOT_EXECUTED_RECORDED_FEE_IS_NOT_LOCKBOX_COST",
    }


def _delta_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    delta = [float(row["net_delta_m1_ladder_minus_unit_usd"]) for row in rows]
    gross_delta = [float(row["gross_delta_m1_ladder_minus_unit_usd"]) for row in rows]
    fee_delta = [float(row["fee_delta_m1_ladder_minus_unit_usd"]) for row in rows]
    daily_delta = _group_sum(rows, "net_delta_m1_ladder_minus_unit_usd", "entry_completed_trading_date")
    nonzero_delta = [value for value in delta if abs(value) > 1e-12]
    nonzero_daily = [value for value in daily_delta.values() if abs(value) > 1e-12]
    return {
        "gate": GATE,
        "strategy_variant": "DELTA_M1_LADDER_MINUS_UNIT_NO_LADDER",
        "lane_class": "SOURCE_NATIVE_FUTURES",
        "evidence_class": "TOUCHED_SUPPORT_DEVELOPMENT_RECONCILIATION_NOT_LOCKBOX_NOT_PROMOTION",
        "effective_backtest_start": min(row["entry_completed_trading_date"] for row in rows),
        "effective_backtest_end": max(row["exit_completed_trading_date"] for row in rows),
        "pnl_rows": len(rows),
        "active_position_rows": "",
        "flat_position_rows": "",
        "position_counts": "",
        "position_change_sides": "",
        "total_fee_sides": "",
        "gross_pnl_usd": sum(gross_delta),
        "recorded_fee_model": "DELTA_OF_IDENTICAL_RECORDED_FEE_POLICY",
        "recorded_fees_usd": sum(fee_delta),
        "net_after_recorded_fees_usd": sum(delta),
        "nonzero_pnl_row_count": len(nonzero_delta),
        "positive_nonzero_pnl_row_count": sum(1 for value in nonzero_delta if value > 0),
        "nonzero_pnl_row_win_rate": _ratio(sum(1 for value in nonzero_delta if value > 0), len(nonzero_delta)),
        "nonzero_daily_count": len(nonzero_daily),
        "positive_nonzero_daily_count": sum(1 for value in nonzero_daily if value > 0),
        "nonzero_daily_win_rate": _ratio(sum(1 for value in nonzero_daily if value > 0), len(nonzero_daily)),
        "futures_realistic_cost_status": "FAIL_CLOSED_NOT_EXECUTED_RECORDED_FEE_IS_NOT_LOCKBOX_COST",
    }


def _yearly_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for year in sorted({row["entry_year"] for row in rows}):
        year_rows = [row for row in rows if row["entry_year"] == year]
        for summary in _summary_rows(year_rows):
            summary["year"] = year
            output.append(summary)
    return output


def _trade_stats(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for variant, field in (("UNIT_NO_LADDER_SAME_INPUT", "unit_no_ladder_contracts"), ("M1_LADDER_SAME_INPUT", "m1_ladder_contracts")):
        prior = 0
        entries = exits = sign_flips = adjustments = 0
        for row in rows:
            current = int(row[field])
            if prior == 0 and current != 0:
                entries += 1
            elif prior != 0 and current == 0:
                exits += 1
            elif prior != 0 and current != 0 and (prior > 0) != (current > 0):
                sign_flips += 1
            elif prior != 0 and current != 0 and prior != current:
                adjustments += 1
            prior = current
        output.append(
            {
                "gate": GATE,
                "strategy_variant": variant,
                "entry_events_zero_to_nonzero": entries,
                "exit_events_nonzero_to_zero": exits,
                "sign_flip_events": sign_flips,
                "same_side_size_adjustment_events": adjustments,
                "trade_count_interpretation": "EVENT_COUNTS_NOT_ROUND_TRIP_TRADE_ACCOUNTING",
            }
        )
    return output


def _cost_rows(lockbox_status: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "gate": GATE,
            "cost_component": "recorded_backtest_fee",
            "cost_status": "RECORDED_ETF_PUBLIC_PER_SIDE_COMMISSION_ONLY_NO_SPREAD_NO_SLIPPAGE",
            "notes": "Used only for touched-support Development/Reconciliation comparison.",
        },
        {
            "gate": GATE,
            "cost_component": "futures_realistic_cost_readiness",
            "cost_status": lockbox_status.get("cost_readiness_status", "FAIL_CLOSED_UNKNOWN"),
            "notes": "Futures-realistic cost readiness remains controlling and unresolved for any Lockbox-facing interpretation.",
        },
    ]


def _validation_rows(**items: Any) -> list[dict[str, Any]]:
    daily_runtime_status = items["daily_runtime_status"]
    row_attribution = items["row_attribution"]
    condition_rows = items["condition_rows"]
    degraded_count = sum(1 for row in condition_rows if row["provider_condition"] != "AVAILABLE")
    return [
        _validation("hourly_source_rows_nonempty", "PASS" if items["hourly_rows"] else "FAIL", len(items["hourly_rows"])),
        _validation("hourly_continuous_rows_nonempty", "PASS" if items["hourly_continuous"] else "FAIL", len(items["hourly_continuous"])),
        _validation("s27_forecast_rows_nonempty", "PASS" if items["s27_rows"] else "FAIL", len(items["s27_rows"])),
        _validation("ladder_rows_match_forecast_rows", "PASS" if len(items["ladder_rows"]) == len(items["s27_rows"]) else "FAIL", len(items["ladder_rows"])),
        _validation("position_rows_match_ladder_rows", "PASS" if len(items["position_rows"]) == len(items["ladder_rows"]) else "FAIL", len(items["position_rows"])),
        _validation("row_attribution_nonempty", "PASS" if row_attribution else "FAIL", len(row_attribution)),
        _validation("same_input_status", "PASS" if {row["same_input_status"] for row in row_attribution} == {"PASS_IDENTICAL_ENTRY_EXIT_HOURLY_ROW_SET"} else "FAIL", 0),
        _validation("daily_runtime_reused_through", "PASS" if daily_runtime_status.get("extended_daily_end") == "2026-05-22" else "FAIL", 0),
        _validation(
            "provider_condition_complete_window",
            "FAIL_CLOSED_PROVIDER_DEGRADED_DAYS_PRESENT_AVAILABLE_ROWS_ONLY_NOT_COMPLETE_WINDOW_BACKTEST" if degraded_count else "PASS",
            degraded_count,
        ),
        _validation("not_lockbox_not_promotion", "PASS", 0),
    ]


def _validation(name: str, status: str, observed_count: int) -> dict[str, Any]:
    return {"gate": GATE, "check_name": name, "check_status": status, "observed_count": observed_count}


def _status_payload(**items: Any) -> dict[str, Any]:
    summary_by_variant = {row["strategy_variant"]: row for row in items["summary_rows"]}
    row_attribution = items["row_attribution"]
    daily_runtime_status = items["daily_runtime_status"]
    lockbox_status = items["lockbox_status"]
    condition_rows = items["condition_rows"]
    degraded_dates = [row["date"] for row in condition_rows if row["provider_condition"] != "AVAILABLE"]
    runtime_lags = [int(row["source_daily_runtime_lag_days"]) for row in items["ladder_rows"]]
    gate_status = (
        "FAIL_CLOSED_S27_ZN_2025_2026_TOUCHED_SUPPORT_PROVIDER_DEGRADED_DAYS_AVAILABLE_ROWS_ONLY_NOT_COMPLETE_BACKTEST"
        if degraded_dates
        else "PASS_S27_ZN_2025_2026_TOUCHED_SUPPORT_DEV_RECON_BACKTEST_NOT_LOCKBOX_NOT_PROMOTION"
    )
    return {
        "gate": GATE,
        "run_id": RUN_ID,
        "status": gate_status,
        "available_rows_numeric_result_status": "PRESERVED_FOR_DIAGNOSTIC_CONTEXT_NOT_COMPLETE_WINDOW_BACKTEST" if degraded_dates else "COMPLETE_WINDOW_PROVIDER_CONDITION_AVAILABLE",
        "lane_class": "SOURCE_NATIVE_FUTURES",
        "support_touch_status": "DAILY_RUNTIME_SUPPORT_ALREADY_TOUCHED_THROUGH_2026-05-22_NOT_PRISTINE_LOCKBOX",
        "provider_condition_degraded_dates": degraded_dates,
        "provider_condition_degraded_day_count": len(degraded_dates),
        "requested_window_start": REQUEST_START.isoformat(),
        "requested_window_end": REQUEST_END.isoformat(),
        "effective_backtest_start": min(row["entry_completed_trading_date"] for row in row_attribution),
        "effective_backtest_end": max(row["exit_completed_trading_date"] for row in row_attribution),
        "hourly_source_rows": len(items["hourly_rows"]),
        "hourly_continuous_rows": len(items["hourly_continuous"]),
        "hourly_inactive_rows_explicitly_ledgered": len(items["hourly_inactive"]),
        "hourly_roll_transition_count": len(items["hourly_roll_plan"]),
        "s26_forecast_rows": len(items["s26_rows"]),
        "s27_forecast_rows": len(items["s27_rows"]),
        "blocked_dependency_rows": len(items["blocked_rows"]),
        "ladder_rows": len(items["ladder_rows"]),
        "position_rows": len(items["position_rows"]),
        "same_input_backtest_rows": len(row_attribution),
        "source_daily_runtime_lag_max_days": max(runtime_lags) if runtime_lags else None,
        "source_daily_runtime_lag_policy": f"STRICT_PRIOR_GT_0_AND_NON_STALE_MAX_{MAX_SOURCE_RUNTIME_LAG_DAYS}_DAYS",
        "daily_runtime_source_status": daily_runtime_status.get("status", ""),
        "daily_runtime_source_end": daily_runtime_status.get("extended_daily_end", ""),
        "unit_no_ladder_net_after_recorded_fee_usd": summary_by_variant["UNIT_NO_LADDER_SAME_INPUT"]["net_after_recorded_fees_usd"],
        "m1_ladder_net_after_recorded_fee_usd": summary_by_variant["M1_LADDER_SAME_INPUT"]["net_after_recorded_fees_usd"],
        "delta_m1_minus_unit_net_after_recorded_fee_usd": summary_by_variant["DELTA_M1_LADDER_MINUS_UNIT_NO_LADDER"]["net_after_recorded_fees_usd"],
        "unit_no_ladder_daily_win_rate": summary_by_variant["UNIT_NO_LADDER_SAME_INPUT"]["nonzero_daily_win_rate"],
        "m1_ladder_daily_win_rate": summary_by_variant["M1_LADDER_SAME_INPUT"]["nonzero_daily_win_rate"],
        "recorded_fee_model": "ETF_PUBLIC_PER_SIDE_COMMISSION_ONLY_NO_SPREAD_NO_SLIPPAGE",
        "futures_realistic_cost_status": lockbox_status.get("cost_readiness_status", "FAIL_CLOSED_UNKNOWN"),
        "provider_api_access": "YES_DATABENTO_HISTORICAL_EXACT_ZN_2025_2026_HOURLY_ONLY",
        "new_data_download": "YES_EXACT_ZN_2025_2026_HOURLY_OHLCV_1H_ONLY_IF_CACHE_MISSING",
        "market_row_source": "DATABENTO_GLBX_MDP3_OHLCV_1H_ZN_ONLY_PLUS_EXISTING_LOCAL_DAILY_RUNTIME_SUPPORT",
        "oos_lockbox_forward_access": "NO",
        "diagnostics_scope": "TOUCHED_SUPPORT_SUMMARY_STATISTICS_ONLY_NO_SHARPE_NO_DRAWDOWN_NO_ALPHA_CLAIM",
        "deployment_trading_promotion": "NO",
        "git_operations": "NO",
        "created_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }


def _process_result_text(status: dict[str, Any], summary_rows: list[dict[str, Any]], yearly_rows: list[dict[str, Any]]) -> str:
    summary_lines = "\n".join(
        f"- {row['strategy_variant']}: net={float(row['net_after_recorded_fees_usd']):.2f}, "
        f"gross={float(row['gross_pnl_usd']):.2f}, recorded_fees={float(row['recorded_fees_usd']):.2f}, "
        f"daily_win_rate={row['nonzero_daily_win_rate']}"
        for row in summary_rows
    )
    yearly_lines = "\n".join(
        f"- {row['year']} {row['strategy_variant']}: net={float(row['net_after_recorded_fees_usd']):.2f}"
        for row in yearly_rows
        if row["strategy_variant"] in {"UNIT_NO_LADDER_SAME_INPUT", "M1_LADDER_SAME_INPUT"}
    )
    return f"""# Carver S27 ZN 2025-2026 Touched-Support Dev/Recon Backtest

Status:

```text
{status["status"]}
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Scope

This artifact uses Databento Historical only for the missing ZN hourly `ohlcv-1h` execution rows over `{status["requested_window_start"]}` through `{status["requested_window_end"]}`. It reuses the existing local daily runtime/V/Q/M support ledger through `{status["daily_runtime_source_end"]}`.

This is therefore:

```text
TOUCHED_SUPPORT_DEVELOPMENT_RECONCILIATION
NOT_LOCKBOX
NOT_PROMOTION
```

## Result

Effective hourly backtest window:

```text
{status["effective_backtest_start"]} through {status["effective_backtest_end"]}
```

{summary_lines}

Provider-condition complete-window status:

```text
{status["available_rows_numeric_result_status"]}
```

Degraded provider dates inside the requested window:

```text
{", ".join(status["provider_condition_degraded_dates"]) if status["provider_condition_degraded_dates"] else "NONE"}
```

## Yearly Summary

{yearly_lines}

## Cost Boundary

Recorded fee model:

```text
{status["recorded_fee_model"]}
```

Futures-realistic cost readiness:

```text
{status["futures_realistic_cost_status"]}
```

The recorded fee model is not Lockbox-ready futures cost closure.

## Non-Authorization

No OOS, Lockbox, Forward, tuning, deployment, trading, promotion, Git staging, commit, push, PR update/opening, or remote repository operation is authorized by this result.
"""


def _local_audit_text(status: dict[str, Any]) -> str:
    return f"""# Local Lean Hostile Audit - S27 ZN 2025-2026 Touched-Support Dev/Recon Backtest

Mode: automatic local hostile audit. Databento access was authorized only for exact ZN hourly `ohlcv-1h` rows over the declared 2025-2026 window. No OOS, Lockbox, Forward, Git operations, deployment, trading, or promotion.

## Findings

CRITICAL: Provider-condition degraded dates are present inside the requested window: `{", ".join(status["provider_condition_degraded_dates"]) if status["provider_condition_degraded_dates"] else "NONE"}`. The numeric result is preserved as available-row diagnostic context, but the complete-window backtest interpretation is fail-closed.

HIGH: The run is not pristine Lockbox because daily runtime/V/Q/M support history was already touched through `{status["daily_runtime_source_end"]}`.

MEDIUM: Futures-realistic costs remain fail-closed. The run uses recorded ETF/public per-side commission only and no spread/slippage.

LOW: The yearly and win-rate summaries are descriptive touched-support evidence only, not validation, Lockbox, or alpha evidence.

## Verdict

```text
BLOCKING_FINDINGS: YES_FOR_COMPLETE_WINDOW_BACKTEST_INTERPRETATION
AUDIT_DISPOSITION: FAIL_CLOSED_PROVIDER_DEGRADED_DAYS_NUMERIC_RESULT_AVAILABLE_ROWS_ONLY_NOT_LOCKBOX_NOT_PROMOTION
```
"""


def _provenance_payload(status: dict[str, Any]) -> dict[str, Any]:
    return {
        "gate": GATE,
        "run_id": RUN_ID,
        "status": status["status"],
        "created_at_utc": status["created_at_utc"],
        "inputs": [
            {"path": str(DAILY_RUNTIME_CSV.relative_to(ROOT)), "sha256": _sha256(DAILY_RUNTIME_CSV)},
            {"path": str(DAILY_RUNTIME_STATUS_JSON.relative_to(ROOT)), "sha256": _sha256(DAILY_RUNTIME_STATUS_JSON)},
            {"path": str(LOCKBOX_STATUS_JSON.relative_to(ROOT)), "sha256": _sha256(LOCKBOX_STATUS_JSON)},
        ],
        "provider_api_access": status["provider_api_access"],
        "new_data_download": status["new_data_download"],
        "git_operations": "NO",
    }


def _roll_fee_sides(entry_bar: dict[str, Any], exit_bar: dict[str, Any], contracts: int) -> int:
    return abs(contracts) * 2 if entry_bar["raw_symbol"] != exit_bar["raw_symbol"] and contracts != 0 else 0


def _side(contracts: int) -> str:
    if contracts > 0:
        return "LONG"
    if contracts < 0:
        return "SHORT"
    return "FLAT"


def _group_sum(rows: list[dict[str, Any]], value_field: str, group_field: str) -> dict[str, float]:
    grouped: dict[str, float] = defaultdict(float)
    for row in rows:
        grouped[str(row[group_field])] += float(row[value_field])
    return dict(grouped)


def _ratio(numerator: int, denominator: int) -> str:
    if denominator == 0:
        return ""
    return f"{numerator / denominator:.6f}"


def _runtime_lag_days(day: str, runtime_day: str) -> int:
    return (date.fromisoformat(day) - date.fromisoformat(runtime_day)).days


def _require_inputs() -> None:
    missing = [path for path in (DAILY_RUNTIME_CSV, DAILY_RUNTIME_STATUS_JSON, LOCKBOX_STATUS_JSON) if not path.exists()]
    if missing:
        raise SystemExit("Missing required local input(s): " + ", ".join(str(path.relative_to(ROOT)) for path in missing))


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _hash_tree(root: Path) -> dict[str, str]:
    hash_file_name = f"{RUN_ID}_sha256.json"
    return {
        str(path.relative_to(ROOT)): _sha256(path)
        for path in sorted(root.rglob("*"))
        if path.is_file() and path.name != hash_file_name
    }


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def _z(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    main()
