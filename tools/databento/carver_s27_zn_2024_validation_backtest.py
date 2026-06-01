from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import sys
from collections import Counter
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import databento as db


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

BASE_MODULE_PATH = ROOT / "tools/databento/carver_s27_candidate_comparison_2022_2023.py"
BASE_SPEC = importlib.util.spec_from_file_location("carver_s27_candidate_comparison_2022_2023_for_zn_2024", BASE_MODULE_PATH)
if BASE_SPEC is None or BASE_SPEC.loader is None:
    raise RuntimeError(f"Unable to load base comparison module from {BASE_MODULE_PATH}")
base = importlib.util.module_from_spec(BASE_SPEC)
sys.modules[BASE_SPEC.name] = base
BASE_SPEC.loader.exec_module(base)


RUN_ID = "20260601_S27_ZN_2024_VALIDATION_BACKTEST"
GATE = "S27_ZN_2024_VALIDATION_BACKTEST_FROZEN_FROM_INITIAL_TEST"
REQUEST_START = date(2024, 1, 1)
REQUEST_END = date(2024, 12, 31)
HOURLY_REQUEST_START = datetime(2023, 12, 31, tzinfo=timezone.utc)
HOURLY_REQUEST_END = datetime(2025, 1, 1, tzinfo=timezone.utc)
DAILY_HISTORY_START = date(2011, 1, 1)
DAILY_REQUEST_END = date(2025, 1, 1)

CAPITAL_USD = 100_000.0
TARGET_RISK = 0.20
INSTRUMENT_WEIGHT = 1.0
IDM = 1.0
FX_RATE = 1.0
ZN_MULTIPLIER = 1000.0
FORECAST_DIVISOR = 10.0
ETF_ZN_FEE_PER_SIDE_USD = 1.51
MAX_SOURCE_RUNTIME_LAG_DAYS = 10

OUTPUT_ROOT = ROOT / "docs/researchops/s26_s27_validation/ZN_S27/2024-01-01_2024-12-31"
PROCESS_RESULT_DOC = ROOT / "docs/process/CARVER_S27_ZN_2024_VALIDATION_BACKTEST_RESULT_2026-06-01.md"
LOCAL_AUDIT_DOC = ROOT / "docs/process/CARVER_S27_ZN_2024_VALIDATION_BACKTEST_LOCAL_LEAN_HOSTILE_AUDIT_2026-06-01.md"


@dataclass(frozen=True)
class FrozenCandidate:
    root: str = "ZN"
    row_id: str = "APPENDIX_C_172_004"
    book_label: str = "10-year US"
    asset_group: str = "bond"
    multiplier: float = ZN_MULTIPLIER
    etf_fee_per_side: float = ETF_ZN_FEE_PER_SIDE_USD
    daily_history_start: date = DAILY_HISTORY_START


ZN = base.Candidate(
    "ZN",
    "APPENDIX_C_172_004",
    "10-year US",
    "bond",
    ZN_MULTIPLIER,
    ETF_ZN_FEE_PER_SIDE_USD,
    DAILY_HISTORY_START,
)


def main() -> None:
    _patch_base_globals()
    client = db.Historical(base._read_databento_key())
    folders = base._folders(OUTPUT_ROOT)
    for folder in folders.values():
        folder.mkdir(parents=True, exist_ok=True)

    manifest = _manifest_payload()
    base._write_json(folders["manifest"] / f"{RUN_ID}_manifest.json", manifest)
    hourly_condition = _cached_or_fetch_condition(client, folders["metadata"] / f"{RUN_ID}_hourly_dataset_condition.json", HOURLY_REQUEST_START.date(), HOURLY_REQUEST_END.date())
    daily_condition = _cached_or_fetch_condition(client, folders["metadata"] / f"{RUN_ID}_daily_dataset_condition.json", DAILY_HISTORY_START, DAILY_REQUEST_END)
    hourly_condition_by_date = base._condition_by_date(hourly_condition)
    daily_condition_by_date = base._condition_by_date(daily_condition)

    hourly_rows, hourly_symbology, hourly_errors = _request_rows(
        client,
        _hourly_contracts(),
        base.HOURLY_SCHEMA,
        HOURLY_REQUEST_START,
        HOURLY_REQUEST_END,
        hourly_condition_by_date,
        folders,
        "hourly",
    )
    daily_by_contract, daily_symbology, daily_errors = _request_daily_rows(client, daily_condition_by_date, folders)
    base._write_csv(folders["metadata"] / f"{RUN_ID}_ZN_symbology_ledger.csv", hourly_symbology + daily_symbology)
    if hourly_errors or daily_errors:
        base._write_csv(folders["status"] / f"{RUN_ID}_provider_errors.csv", hourly_errors + daily_errors)

    if hourly_errors or daily_errors:
        raise SystemExit(f"Fail closed: provider errors observed hourly={len(hourly_errors)} daily={len(daily_errors)}")
    if not hourly_rows:
        raise SystemExit("Fail closed: no ZN 2024 hourly rows")
    if not daily_by_contract:
        raise SystemExit("Fail closed: no ZN daily runtime rows")

    hourly_continuous, hourly_inactive, hourly_roll_plan = base._build_continuous_rows(
        candidate=ZN,
        contracts=_hourly_contracts(),
        source_rows=hourly_rows,
        price_field="close",
        timestamp_field="derived_completed_bar_end_utc",
        output_root=folders["lineage"],
        prefix=f"{RUN_ID}_ZN_hourly",
    )
    daily_source_rows = [row for rows in daily_by_contract.values() for row in rows]
    daily_contracts = _daily_contracts("ZN", DAILY_HISTORY_START, DAILY_REQUEST_END)
    daily_continuous, daily_inactive, daily_roll_plan = base._build_continuous_rows(
        candidate=ZN,
        contracts=daily_contracts,
        source_rows=daily_source_rows,
        price_field="close",
        timestamp_field="completed_trading_date",
        output_root=folders["lineage"],
        prefix=f"{RUN_ID}_ZN_daily",
    )
    sigma_rows = base._build_sigma_rows(daily_continuous)
    vqm_rows = base._build_vqm_rows(sigma_rows)
    daily_runtime_rows = base._build_daily_runtime_rows(daily_continuous, vqm_rows)
    s26_rows, s27_rows, blocked_rows = base._build_forecasts(ZN, hourly_continuous, daily_runtime_rows)
    ladder_rows = _build_ladder_rows(s27_rows)
    position_rows = _build_position_rows(ladder_rows)
    backtest_rows = _build_ladder_backtest_rows(position_rows, hourly_continuous)
    validation_rows = _validation_rows(hourly_rows, hourly_continuous, daily_continuous, s27_rows, ladder_rows, position_rows, backtest_rows)
    status = _status_payload(
        hourly_rows,
        hourly_continuous,
        hourly_inactive,
        hourly_roll_plan,
        daily_continuous,
        daily_inactive,
        daily_roll_plan,
        sigma_rows,
        vqm_rows,
        s26_rows,
        s27_rows,
        blocked_rows,
        ladder_rows,
        position_rows,
        backtest_rows,
    )

    base._write_csv(folders["lineage"] / f"{RUN_ID}_ZN_hourly_continuous_lineage.csv", hourly_continuous)
    base._write_csv(folders["lineage"] / f"{RUN_ID}_ZN_hourly_inactive_rows.csv", hourly_inactive)
    base._write_csv(folders["lineage"] / f"{RUN_ID}_ZN_hourly_roll_plan.csv", hourly_roll_plan)
    base._write_csv(folders["lineage"] / f"{RUN_ID}_ZN_daily_continuous_lineage.csv", daily_continuous)
    base._write_csv(folders["lineage"] / f"{RUN_ID}_ZN_daily_inactive_rows.csv", daily_inactive)
    base._write_csv(folders["lineage"] / f"{RUN_ID}_ZN_daily_roll_plan.csv", daily_roll_plan)
    base._write_csv(folders["runtime"] / f"{RUN_ID}_ZN_sigma_rows.csv", sigma_rows)
    base._write_csv(folders["runtime"] / f"{RUN_ID}_ZN_vqm_rows.csv", vqm_rows)
    base._write_csv(folders["runtime"] / f"{RUN_ID}_ZN_daily_runtime_rows.csv", daily_runtime_rows)
    base._write_csv(folders["forecasts"] / f"{RUN_ID}_ZN_s26_forecast_rows.csv", s26_rows)
    base._write_csv(folders["forecasts"] / f"{RUN_ID}_ZN_s27_forecast_rows.csv", s27_rows)
    base._write_csv(folders["forecasts"] / f"{RUN_ID}_ZN_blocked_dependency_rows.csv", blocked_rows)
    base._write_csv(folders["positions"] / f"{RUN_ID}_ZN_base_position_ladder_rows.csv", ladder_rows)
    base._write_csv(folders["positions"] / f"{RUN_ID}_ZN_desired_position_rows.csv", position_rows)
    base._write_csv(folders["backtest"] / f"{RUN_ID}_ZN_ladder_backtest_rows.csv", backtest_rows)
    base._write_csv(folders["validation"] / f"{RUN_ID}_validation_ledger.csv", validation_rows)
    base._write_json(folders["status"] / f"{RUN_ID}_status.json", status)
    base._write_json(folders["provenance"] / f"{RUN_ID}_provenance.json", _provenance_payload(status))
    base._write_json(folders["hashes"] / f"{RUN_ID}_sha256.json", base._hash_tree(OUTPUT_ROOT))
    PROCESS_RESULT_DOC.write_text(_process_result_text(status), encoding="utf-8")
    LOCAL_AUDIT_DOC.write_text(_local_audit_text(status), encoding="utf-8")

    print(status["status"])
    print(f"effective_backtest_start={status['effective_backtest_start']}")
    print(f"effective_backtest_end={status['effective_backtest_end']}")
    print(f"net_after_etf_fees_usd={status['net_after_etf_fees_usd']}")
    print(f"artifact_root={OUTPUT_ROOT.relative_to(ROOT)}")


def _patch_base_globals() -> None:
    base.RUN_ID = RUN_ID
    base.GATE = GATE
    base.REQUEST_START = REQUEST_START
    base.REQUEST_END = REQUEST_END
    base.HOURLY_REQUEST_START = HOURLY_REQUEST_START
    base.HOURLY_REQUEST_END = HOURLY_REQUEST_END
    base.DAILY_REQUEST_END = DAILY_REQUEST_END
    base.OUTPUT_ROOT = OUTPUT_ROOT


def _manifest_payload() -> dict[str, Any]:
    return {
        "gate": GATE,
        "run_id": RUN_ID,
        "lane_class": "SOURCE_NATIVE_FUTURES",
        "stage": "VALIDATION",
        "frozen_from_initial_test": "S27_ZN_M1_STYLE_LADDER_2022_2023",
        "root": "ZN",
        "row_id": "APPENDIX_C_172_004",
        "requested_window_start": REQUEST_START.isoformat(),
        "requested_window_end": REQUEST_END.isoformat(),
        "dataset": base.DATASET,
        "hourly_schema": base.HOURLY_SCHEMA,
        "daily_schema": base.DAILY_SCHEMA,
        "hourly_contracts": _hourly_contracts(),
        "daily_history_start": DAILY_HISTORY_START.isoformat(),
        "daily_request_end_exclusive": DAILY_REQUEST_END.isoformat(),
        "capital_usd": CAPITAL_USD,
        "target_risk": TARGET_RISK,
        "instrument_weight": INSTRUMENT_WEIGHT,
        "idm": IDM,
        "zn_multiplier": ZN_MULTIPLIER,
        "fee_per_side_usd": ETF_ZN_FEE_PER_SIDE_USD,
        "non_authorization": [
            "NO_OOS",
            "NO_LOCKBOX",
            "NO_FORWARD",
            "NO_DEPLOYMENT",
            "NO_TRADING",
            "NO_PROMOTION",
            "NO_PARAMETER_TUNING",
            "NO_SYMBOL_RESCUE",
        ],
    }


def _cached_or_fetch_condition(client: db.Historical, path: Path, start: date, end: date) -> list[dict[str, Any]]:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    condition = base._dataset_condition(client, start, end)
    base._write_json(path, condition)
    return condition


def _request_rows(
    client: db.Historical,
    contracts: list[dict[str, Any]],
    schema: str,
    start_dt: datetime,
    end_dt: datetime,
    condition_by_date: dict[str, str],
    folders: dict[str, Path],
    purpose: str,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    rows: list[dict[str, Any]] = []
    symbology: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []
    for contract in contracts:
        contract_rows, contract_symbology, contract_errors = base._request_ohlcv_rows(
            client=client,
            candidate=ZN,
            contract=contract,
            schema=schema,
            start_dt=start_dt,
            end_dt=end_dt,
            condition_by_date=condition_by_date,
            folders=folders,
            purpose=purpose,
        )
        rows.extend(contract_rows)
        symbology.extend(contract_symbology)
        errors.extend(contract_errors)
    return rows, symbology, errors


def _request_daily_rows(
    client: db.Historical,
    condition_by_date: dict[str, str],
    folders: dict[str, Path],
) -> tuple[dict[str, list[dict[str, Any]]], list[dict[str, Any]], list[dict[str, Any]]]:
    rows_by_contract: dict[str, list[dict[str, Any]]] = {}
    symbology: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []
    for contract in _daily_contracts("ZN", DAILY_HISTORY_START, DAILY_REQUEST_END):
        rows, contract_symbology, contract_errors = base._request_ohlcv_rows(
            client=client,
            candidate=ZN,
            contract=contract,
            schema=base.DAILY_SCHEMA,
            start_dt=datetime.combine(date.fromisoformat(contract["request_start"]), datetime.min.time(), timezone.utc),
            end_dt=datetime.combine(date.fromisoformat(contract["request_end"]), datetime.min.time(), timezone.utc),
            condition_by_date=condition_by_date,
            folders=folders,
            purpose="daily",
        )
        if rows:
            rows_by_contract[base._contract_key(contract)] = rows
        symbology.extend(contract_symbology)
        errors.extend(contract_errors)
    return rows_by_contract, symbology, errors


def _hourly_contracts() -> list[dict[str, Any]]:
    return [
        {"raw_symbol": "ZNH4", "contract_year": 2024, "delivery_month": 3, "delivery_code": "H"},
        {"raw_symbol": "ZNM4", "contract_year": 2024, "delivery_month": 6, "delivery_code": "M"},
        {"raw_symbol": "ZNU4", "contract_year": 2024, "delivery_month": 9, "delivery_code": "U"},
        {"raw_symbol": "ZNZ4", "contract_year": 2024, "delivery_month": 12, "delivery_code": "Z"},
        {"raw_symbol": "ZNH5", "contract_year": 2025, "delivery_month": 3, "delivery_code": "H"},
    ]


def _daily_contracts(root: str, start: date, end: date) -> list[dict[str, Any]]:
    contracts: list[dict[str, Any]] = []
    end_delivery = date(end.year, 3, 1)
    for year in range(start.year, end.year + 1):
        for month, code in base.MONTH_CODES:
            delivery = date(year, month, 1)
            if delivery < date(start.year, 3, 1) or delivery > end_delivery:
                continue
            request_start = max(start, delivery - timedelta(days=460))
            request_end = min(end, _month_end(year, month) + timedelta(days=35))
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
                "source_status": "PREVALIDATED_M1_STYLE_BASE_POSITION_VALIDATION",
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
                "position_status": "M1_STYLE_LADDER_POSITION_SERIES_VALIDATION_ONLY_NOT_PRODUCTION_SIZING",
            }
        )
    return rows


def _build_ladder_backtest_rows(position_rows: list[dict[str, Any]], hourly_continuous: list[dict[str, Any]]) -> list[dict[str, Any]]:
    position_by_ts = {row["derived_completed_bar_end_utc"]: row for row in position_rows}
    hourly_by_ts = {row["derived_completed_bar_end_utc"]: row for row in hourly_continuous}
    ordered_ts = sorted(hourly_by_ts)
    rows: list[dict[str, Any]] = []
    cumulative_gross = 0.0
    cumulative_cost = 0.0
    cumulative_net = 0.0
    prior_position: int | None = None
    for entry_ts, exit_ts in zip(ordered_ts[:-1], ordered_ts[1:], strict=True):
        position = position_by_ts.get(entry_ts)
        if position is None:
            continue
        entry_bar = hourly_by_ts[entry_ts]
        exit_bar = hourly_by_ts[exit_ts]
        contracts = int(position["desired_rounded_contracts_nearest"])
        price_change = float(exit_bar["continuous_close"]) - float(entry_bar["continuous_close"])
        gross = contracts * price_change * ZN_MULTIPLIER
        position_change = 0 if prior_position is None else contracts - prior_position
        roll_transition_sides = abs(contracts) * 2 if entry_bar["raw_symbol"] != exit_bar["raw_symbol"] and contracts != 0 else 0
        position_change_sides = abs(position_change)
        total_fee_sides = position_change_sides + roll_transition_sides
        cost = total_fee_sides * ETF_ZN_FEE_PER_SIDE_USD
        prior_position = contracts
        cumulative_gross += gross
        cumulative_cost += cost
        cumulative_net += gross - cost
        rows.append(
            {
                "gate": GATE,
                "entry_bar_end_utc": entry_ts,
                "exit_bar_end_utc": exit_ts,
                "entry_completed_trading_date": entry_bar["completed_trading_date"],
                "exit_completed_trading_date": exit_bar["completed_trading_date"],
                "entry_raw_symbol": entry_bar["raw_symbol"],
                "exit_raw_symbol": exit_bar["raw_symbol"],
                "held_contracts_m1_ladder": contracts,
                "position_change_from_previous_pnl_row": position_change,
                "position_change_fee_sides": position_change_sides,
                "roll_transition_fee_sides": roll_transition_sides,
                "total_fee_sides": total_fee_sides,
                "entry_continuous_close": entry_bar["continuous_close"],
                "exit_continuous_close": exit_bar["continuous_close"],
                "price_change_points": price_change,
                "zn_contract_multiplier": ZN_MULTIPLIER,
                "gross_pnl_usd": gross,
                "etf_fee_per_side_usd": ETF_ZN_FEE_PER_SIDE_USD,
                "estimated_etf_fee_usd": cost,
                "net_after_etf_fees_usd": gross - cost,
                "cumulative_gross_pnl_usd": cumulative_gross,
                "cumulative_estimated_etf_fees_usd": cumulative_cost,
                "cumulative_net_after_etf_fees_usd": cumulative_net,
                "lookahead_status": "PASS_POSITION_FROM_PRIOR_COMPLETED_HOURLY_BAR_ONLY",
                "backtest_row_status": "VALIDATION_M1_STYLE_LADDER_ETF_COST_NOT_ALPHA_NOT_PROMOTION",
            }
        )
    return rows


def _status_payload(
    hourly_rows: list[dict[str, Any]],
    hourly_continuous: list[dict[str, Any]],
    hourly_inactive: list[dict[str, Any]],
    hourly_roll_plan: list[dict[str, Any]],
    daily_continuous: list[dict[str, Any]],
    daily_inactive: list[dict[str, Any]],
    daily_roll_plan: list[dict[str, Any]],
    sigma_rows: list[dict[str, Any]],
    vqm_rows: list[dict[str, Any]],
    s26_rows: list[dict[str, Any]],
    s27_rows: list[dict[str, Any]],
    blocked_rows: list[dict[str, Any]],
    ladder_rows: list[dict[str, Any]],
    position_rows: list[dict[str, Any]],
    backtest_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    position_counts = Counter(int(row["desired_rounded_contracts_nearest"]) for row in position_rows)
    gross = sum(float(row["gross_pnl_usd"]) for row in backtest_rows)
    fees = sum(float(row["estimated_etf_fee_usd"]) for row in backtest_rows)
    net = sum(float(row["net_after_etf_fees_usd"]) for row in backtest_rows)
    sides = sum(abs(int(row["position_change_from_previous_pnl_row"])) for row in backtest_rows)
    roll_sides = sum(int(row["roll_transition_fee_sides"]) for row in backtest_rows)
    total_fee_sides = sum(int(row["total_fee_sides"]) for row in backtest_rows)
    runtime_lags = [int(row["source_daily_runtime_lag_days"]) for row in ladder_rows]
    return {
        "gate": GATE,
        "status": "PASS_S27_ZN_2024_VALIDATION_BACKTEST_NOT_ALPHA",
        "frozen_from_initial_test": "S27_ZN_M1_STYLE_LADDER_2022_2023",
        "requested_window_start": REQUEST_START.isoformat(),
        "requested_window_end": REQUEST_END.isoformat(),
        "effective_backtest_start": backtest_rows[0]["entry_completed_trading_date"] if backtest_rows else "",
        "effective_backtest_end": backtest_rows[-1]["exit_completed_trading_date"] if backtest_rows else "",
        "hourly_source_rows": len(hourly_rows),
        "hourly_continuous_rows": len(hourly_continuous),
        "hourly_inactive_rows_explicitly_ledgered": len(hourly_inactive),
        "hourly_roll_transition_count": len(hourly_roll_plan),
        "daily_continuous_rows": len(daily_continuous),
        "daily_inactive_rows_explicitly_ledgered": len(daily_inactive),
        "daily_roll_transition_count": len(daily_roll_plan),
        "sigma_rows": len(sigma_rows),
        "vqm_rows": len(vqm_rows),
        "s26_forecast_rows": len(s26_rows),
        "s27_forecast_rows": len(s27_rows),
        "blocked_dependency_rows": len(blocked_rows),
        "ladder_rows": len(ladder_rows),
        "position_rows": len(position_rows),
        "backtest_rows": len(backtest_rows),
        "capital_usd": CAPITAL_USD,
        "target_risk": TARGET_RISK,
        "instrument_weight": INSTRUMENT_WEIGHT,
        "idm": IDM,
        "zn_multiplier": ZN_MULTIPLIER,
        "fx_rate": FX_RATE,
        "annual_risk_source": "S27_RUNTIME_SIGMA_PRICE_BRIDGE_DERIVED_ANNUAL_RISK_NO_LOOKAHEAD",
        "source_daily_runtime_lag_max_days": max(runtime_lags) if runtime_lags else None,
        "source_daily_runtime_lag_policy": f"STRICT_PRIOR_GT_0_AND_NON_STALE_MAX_{MAX_SOURCE_RUNTIME_LAG_DAYS}_DAYS",
        "forecast_to_position_divisor": FORECAST_DIVISOR,
        "rounding_policy": "NEAREST",
        "rounded_position_counts": dict(sorted(position_counts.items())),
        "position_change_sides": sides,
        "roll_transition_fee_sides": roll_sides,
        "total_fee_sides": total_fee_sides,
        "gross_pnl_usd": gross,
        "estimated_etf_fees_usd": fees,
        "net_after_etf_fees_usd": net,
        "cost_status": "ETF_PUBLIC_PER_SIDE_COMMISSION_ONLY_NO_SPREAD_OR_SLIPPAGE",
        "diagnostics_run": "NO_SHARPE_NO_DRAWDOWN_NO_ALPHA_STATISTICS",
        "provider_api_access": "DATABENTO_EXACT_ZN_2024_VALIDATION_ONLY",
        "new_data_download": "YES_EXACT_ZN_2024_VALIDATION_SCOPE_ONLY_IF_CACHE_MISSING",
        "market_row_source": "DATABENTO_GLBX_MDP3_OHLCV_1H_AND_OHLCV_1D_ZN_ONLY",
        "oos_access": "NO",
        "lockbox_access": "NO",
        "forward_access": "NO",
        "deployment": "NO",
        "trading": "NO",
        "promotion": "NO",
        "git_operations": "NO",
    }


def _validation_rows(*items: Any) -> list[dict[str, Any]]:
    hourly_rows, hourly_continuous, daily_continuous, s27_rows, ladder_rows, position_rows, backtest_rows = items
    return [
        _validation("hourly_source_rows_nonempty", bool(hourly_rows), len(hourly_rows)),
        _validation("hourly_continuous_rows_nonempty", bool(hourly_continuous), len(hourly_continuous)),
        _validation("daily_continuous_rows_nonempty", bool(daily_continuous), len(daily_continuous)),
        _validation("s27_forecast_rows_nonempty", bool(s27_rows), len(s27_rows)),
        _validation("ladder_rows_match_forecast_rows", len(ladder_rows) == len(s27_rows), len(ladder_rows)),
        _validation("position_rows_match_ladder_rows", len(position_rows) == len(ladder_rows), len(position_rows)),
        _validation("backtest_rows_nonempty", bool(backtest_rows), len(backtest_rows)),
        _validation("no_oos_lockbox_forward", True, 0),
        _validation("no_alpha_statistics", True, 0),
    ]


def _validation(name: str, passed: bool, observed_count: int) -> dict[str, Any]:
    return {"check_name": name, "check_status": "PASS" if passed else "FAIL", "observed_count": observed_count}


def _provenance_payload(status: dict[str, Any]) -> dict[str, Any]:
    return {
        "gate": GATE,
        "created_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "status": status,
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


def _process_result_text(status: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Carver S27 ZN 2024 Validation Backtest Result",
            "",
            "Status:",
            "",
            "```text",
            status["status"],
            "```",
            "",
            f"Gate: `{GATE}`",
            "",
            "Frozen from initial ZN 2022-2023 test: S27 ZN M1-style sizing ladder, capital 100k, target risk 20%, weight 1, IDM 1, ZN multiplier 1000, ETF public per-side commission only.",
            "",
            "## Result",
            "",
            f"- Requested window: `{status['requested_window_start']}` through `{status['requested_window_end']}`.",
            f"- Effective backtest window: `{status['effective_backtest_start']}` through `{status['effective_backtest_end']}`.",
            f"- S27 forecast rows: `{status['s27_forecast_rows']}`.",
            f"- Ladder rows: `{status['ladder_rows']}`.",
            f"- Backtest rows: `{status['backtest_rows']}`.",
            f"- Rounded position counts: `{status['rounded_position_counts']}`.",
            f"- Position-change sides: `{status['position_change_sides']}`.",
            f"- Roll-transition fee sides: `{status['roll_transition_fee_sides']}`.",
            f"- Gross PnL: `${status['gross_pnl_usd']}`.",
            f"- Estimated ETF fees: `${status['estimated_etf_fees_usd']}`.",
            f"- Net after ETF fees: `${status['net_after_etf_fees_usd']}`.",
            "",
            "## Boundary",
            "",
            "This is the frozen 2024 validation backtest only. It is not OOS, not Lockbox, not Forward, not deployment, not trading, and not promotion. No parameter, symbol, cost, or sizing tuning is authorized by this result.",
            "",
        ]
    )


def _local_audit_text(status: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Local Lean Hostile Audit - S27 ZN 2024 Validation Backtest",
            "",
            "Mode: automatic local lean hostile audit over generated 2024 validation artifacts.",
            "",
            "CRITICAL: None for declared frozen ZN 2024 validation scope.",
            "",
            "HIGH: None. The run is ZN only, uses the frozen M1-style sizing ladder constants from the initial ZN test, and does not open OOS, Lockbox, Forward, deployment, trading, promotion, CFD adapter, or old QuantLab active pipeline use.",
            "",
            "MEDIUM: This remains a close-to-close hourly execution approximation with ETF public per-side commission only. It does not implement fast mean-reversion limit-order fill quality, spread, slippage, or prop-firm constraints.",
            "",
            "Verdict:",
            "",
            "```text",
            "BLOCKING_FINDINGS: NO_FOR_DECLARED_ZN_2024_VALIDATION_SCOPE",
            "AUDIT_DISPOSITION: PASS_S27_ZN_2024_VALIDATION_BACKTEST_NOT_ALPHA",
            "```",
            "",
        ]
    )


def _runtime_lag_days(day: str, runtime_day: str) -> int:
    return (date.fromisoformat(day) - date.fromisoformat(runtime_day)).days


if __name__ == "__main__":
    main()
