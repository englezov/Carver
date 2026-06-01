from __future__ import annotations

import csv
import hashlib
import json
import math
import random
from collections import Counter
from dataclasses import dataclass
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
RUN_ID = "20260601_S27_ZN_2022_2024_PARITY_VERIFIER"
GATE = "S27_ZN_BACKTEST_PARITY_VERIFICATION_BEFORE_LOCKBOX"
OUTPUT_ROOT = ROOT / "docs/researchops/s26_s27_parity/ZN_S27/2022_2024"
PROCESS_RESULT_DOC = ROOT / "docs/process/CARVER_S27_ZN_BACKTEST_PARITY_VERIFICATION_RESULT_2026-06-01.md"
LOCAL_AUDIT_DOC = ROOT / "docs/process/CARVER_S27_ZN_BACKTEST_PARITY_VERIFICATION_LOCAL_HOSTILE_AUDIT_2026-06-01.md"

CAPITAL_USD = 100_000.0
TARGET_RISK = 0.20
INSTRUMENT_WEIGHT = 1.0
IDM = 1.0
FX_RATE = 1.0
ZN_MULTIPLIER = 1000.0
FORECAST_DIVISOR = 10.0
ETF_ZN_FEE_PER_SIDE_USD = 1.51
MAX_SOURCE_RUNTIME_LAG_DAYS = 10
EPSILON = 1e-8


@dataclass(frozen=True)
class PeriodArtifacts:
    label: str
    stage: str
    root: Path
    forecast_csv: Path
    hourly_csv: Path
    ladder_csv: Path
    position_csv: Path
    backtest_csv: Path
    status_json: Path


PERIODS = (
    PeriodArtifacts(
        label="ZN_2022_2023_INITIAL_TEST",
        stage="INITIAL_TEST",
        root=ROOT / "docs/researchops/s26_s27_m1_ladder/ZN_S27/2022-01-01_2023-12-31",
        forecast_csv=ROOT
        / "docs/researchops/s26_s27_backtest_readiness/ZN_S27_SINGLE_INSTRUMENT/2022-01-01_2023-12-31/retargeted_dev_recon_backtest/forecast_rows/20260531_S27_ZN_2022_2023_RETARGETED_DEV_RECON_BACKTEST_s27_forecast_rows.csv",
        hourly_csv=ROOT
        / "docs/researchops/s26_s27_backtest_readiness/ZN_S27_SINGLE_INSTRUMENT/2022-01-01_2023-12-31/retargeted_dev_recon_backtest/local_hourly_lineage/20260531_S27_ZN_2022_2023_RETARGETED_DEV_RECON_BACKTEST_local_hourly_continuous_lineage.csv",
        ladder_csv=ROOT
        / "docs/researchops/s26_s27_m1_ladder/ZN_S27/2022-01-01_2023-12-31/ladder_rows/20260531_S27_ZN_M1_LADDER_DEV_RECON_BACKTEST_base_position_ladder_rows.csv",
        position_csv=ROOT
        / "docs/researchops/s26_s27_m1_ladder/ZN_S27/2022-01-01_2023-12-31/position_rows/20260531_S27_ZN_M1_LADDER_DEV_RECON_BACKTEST_desired_position_rows.csv",
        backtest_csv=ROOT
        / "docs/researchops/s26_s27_m1_ladder/ZN_S27/2022-01-01_2023-12-31/backtest_rows/20260531_S27_ZN_M1_LADDER_DEV_RECON_BACKTEST_ladder_backtest_rows.csv",
        status_json=ROOT
        / "docs/researchops/s26_s27_m1_ladder/ZN_S27/2022-01-01_2023-12-31/status/20260531_S27_ZN_M1_LADDER_DEV_RECON_BACKTEST_status.json",
    ),
    PeriodArtifacts(
        label="ZN_2024_VALIDATION",
        stage="VALIDATION",
        root=ROOT / "docs/researchops/s26_s27_validation/ZN_S27/2024-01-01_2024-12-31",
        forecast_csv=ROOT
        / "docs/researchops/s26_s27_validation/ZN_S27/2024-01-01_2024-12-31/forecast_rows/20260601_S27_ZN_2024_VALIDATION_BACKTEST_ZN_s27_forecast_rows.csv",
        hourly_csv=ROOT
        / "docs/researchops/s26_s27_validation/ZN_S27/2024-01-01_2024-12-31/local_lineage/20260601_S27_ZN_2024_VALIDATION_BACKTEST_ZN_hourly_continuous_lineage.csv",
        ladder_csv=ROOT
        / "docs/researchops/s26_s27_validation/ZN_S27/2024-01-01_2024-12-31/position_rows/20260601_S27_ZN_2024_VALIDATION_BACKTEST_ZN_base_position_ladder_rows.csv",
        position_csv=ROOT
        / "docs/researchops/s26_s27_validation/ZN_S27/2024-01-01_2024-12-31/position_rows/20260601_S27_ZN_2024_VALIDATION_BACKTEST_ZN_desired_position_rows.csv",
        backtest_csv=ROOT
        / "docs/researchops/s26_s27_validation/ZN_S27/2024-01-01_2024-12-31/backtest_rows/20260601_S27_ZN_2024_VALIDATION_BACKTEST_ZN_ladder_backtest_rows.csv",
        status_json=ROOT
        / "docs/researchops/s26_s27_validation/ZN_S27/2024-01-01_2024-12-31/status/20260601_S27_ZN_2024_VALIDATION_BACKTEST_status.json",
    ),
)


def main() -> None:
    folders = _folders()
    for folder in folders.values():
        folder.mkdir(parents=True, exist_ok=True)

    all_period_summaries: list[dict[str, Any]] = []
    all_parity_rows: list[dict[str, Any]] = []
    all_replay_rows: list[dict[str, Any]] = []
    all_lookahead_rows: list[dict[str, Any]] = []
    all_lineage_rows: list[dict[str, Any]] = []
    all_null_rows: list[dict[str, Any]] = []

    for period in PERIODS:
        _require_period(period)
        result = _verify_period(period)
        all_period_summaries.append(result["summary"])
        all_parity_rows.extend(result["parity_rows"])
        all_replay_rows.extend(result["replay_rows"])
        all_lookahead_rows.extend(result["lookahead_rows"])
        all_lineage_rows.extend(result["lineage_rows"])
        all_null_rows.extend(result["null_rows"])

    overall = _overall_status(all_period_summaries, all_parity_rows, all_replay_rows, all_lookahead_rows, all_lineage_rows)
    _write_csv(folders["parity"] / f"{RUN_ID}_aggregate_parity_ledger.csv", all_parity_rows)
    _write_csv(folders["replay"] / f"{RUN_ID}_row_replay_ledger.csv", all_replay_rows)
    _write_csv(folders["lookahead"] / f"{RUN_ID}_lookahead_ledger.csv", all_lookahead_rows)
    _write_csv(folders["lineage"] / f"{RUN_ID}_lineage_ledger.csv", all_lineage_rows)
    _write_csv(folders["null"] / f"{RUN_ID}_null_antistrategy_ledger.csv", all_null_rows)
    _write_csv(folders["summary"] / f"{RUN_ID}_summary.csv", all_period_summaries)
    _write_json(folders["status"] / f"{RUN_ID}_status.json", overall)
    _write_json(folders["provenance"] / f"{RUN_ID}_provenance.json", _provenance_payload(overall))
    _write_json(folders["hashes"] / f"{RUN_ID}_sha256.json", _hash_tree(OUTPUT_ROOT))
    PROCESS_RESULT_DOC.write_text(_process_result_text(overall, all_period_summaries), encoding="utf-8")
    LOCAL_AUDIT_DOC.write_text(_local_audit_text(overall), encoding="utf-8")

    print(overall["status"])
    for row in all_period_summaries:
        print(
            f"{row['period_label']}: parity={row['aggregate_parity_status']} "
            f"net={row['reported_net_after_fees_usd']} replay_net={row['replayed_net_after_fees_usd']} "
            f"null_inverted_net={row['null_inverted_net_after_fees_usd']}"
        )
    print(f"artifact_root={OUTPUT_ROOT.relative_to(ROOT)}")


def _verify_period(period: PeriodArtifacts) -> dict[str, Any]:
    forecasts = _read_csv(period.forecast_csv)
    hourly_rows = _read_csv(period.hourly_csv)
    reported_ladder_rows = _read_csv(period.ladder_csv)
    reported_position_rows = _read_csv(period.position_csv)
    reported_backtest_rows = _read_csv(period.backtest_csv)
    reported_status = json.loads(period.status_json.read_text(encoding="utf-8"))

    replay_ladder_rows = _replay_ladder_rows(forecasts)
    replay_position_rows = _replay_position_rows(replay_ladder_rows)
    replay_backtest_rows = _replay_backtest_rows(replay_position_rows, hourly_rows)

    parity_rows = _aggregate_parity_rows(period, reported_status, reported_backtest_rows, replay_backtest_rows)
    row_replay_rows = _row_replay_rows(period, reported_backtest_rows, replay_backtest_rows)
    lookahead_rows = _lookahead_rows(period, forecasts, replay_ladder_rows, reported_backtest_rows)
    lineage_rows = _lineage_rows(period, forecasts, hourly_rows, reported_ladder_rows, reported_position_rows, reported_backtest_rows)
    null_rows = _null_rows(period, replay_position_rows, hourly_rows)

    aggregate_pass = all(row["check_status"] == "PASS" for row in parity_rows)
    replay_pass = all(row["check_status"] == "PASS" for row in row_replay_rows)
    lookahead_pass = all(row["check_status"] == "PASS" for row in lookahead_rows)
    lineage_pass = all(row["check_status"] == "PASS" for row in lineage_rows)

    reported_gross = sum(float(row["gross_pnl_usd"]) for row in reported_backtest_rows)
    reported_fees = sum(_fee(row) for row in reported_backtest_rows)
    reported_net = sum(_net(row) for row in reported_backtest_rows)
    replayed_gross = sum(float(row["gross_pnl_usd"]) for row in replay_backtest_rows)
    replayed_fees = sum(_fee(row) for row in replay_backtest_rows)
    replayed_net = sum(_net(row) for row in replay_backtest_rows)
    inverted = _build_null_backtest(replay_position_rows, hourly_rows, mode="INVERTED")
    delayed = _build_null_backtest(replay_position_rows, hourly_rows, mode="ONE_BAR_DELAYED")
    shuffled = _build_null_backtest(replay_position_rows, hourly_rows, mode="DAY_SHUFFLED")
    summary = {
        "period_label": period.label,
        "stage": period.stage,
        "reported_status": reported_status.get("status"),
        "effective_backtest_start": reported_status.get("effective_backtest_start"),
        "effective_backtest_end": reported_status.get("effective_backtest_end"),
        "reported_backtest_rows": len(reported_backtest_rows),
        "replayed_backtest_rows": len(replay_backtest_rows),
        "reported_gross_pnl_usd": reported_gross,
        "replayed_gross_pnl_usd": replayed_gross,
        "reported_fees_usd": reported_fees,
        "replayed_fees_usd": replayed_fees,
        "reported_net_after_fees_usd": reported_net,
        "replayed_net_after_fees_usd": replayed_net,
        "aggregate_parity_status": "PASS" if aggregate_pass else "FAIL",
        "row_replay_status": "PASS" if replay_pass else "FAIL",
        "lookahead_status": "PASS" if lookahead_pass else "FAIL",
        "lineage_status": "PASS" if lineage_pass else "FAIL",
        "null_inverted_net_after_fees_usd": sum(_net(row) for row in inverted),
        "null_one_bar_delayed_net_after_fees_usd": sum(_net(row) for row in delayed),
        "null_day_shuffled_net_after_fees_usd": sum(_net(row) for row in shuffled),
        "provider_api_access": "NO",
        "new_data_download": "NO",
        "diagnostics_run": "NULL_TESTS_ONLY_NOT_ALPHA_STATISTICS",
        "oos_access": "NO",
        "lockbox_access": "NO",
        "forward_access": "NO",
        "deployment": "NO",
        "trading": "NO",
        "promotion": "NO",
    }
    return {
        "summary": summary,
        "parity_rows": parity_rows,
        "replay_rows": row_replay_rows,
        "lookahead_rows": lookahead_rows,
        "lineage_rows": lineage_rows,
        "null_rows": null_rows,
    }


def _replay_ladder_rows(forecasts: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in forecasts:
        price = float(row["continuous_close"])
        runtime_day = row.get("source_daily_runtime_completed_trading_date") or row["source_vqm_completed_trading_date"]
        lag = _runtime_lag_days(row["completed_trading_date"], runtime_day)
        annual_risk = float(row["sigma_price_i_t"]) * 16.0 / price
        contract_risk = price * ZN_MULTIPLIER * FX_RATE * annual_risk
        target_currency_risk = CAPITAL_USD * TARGET_RISK
        base_unrounded = target_currency_risk * INSTRUMENT_WEIGHT * IDM / contract_risk
        capped = float(row["capped_forecast"])
        rows.append(
            {
                "raw_symbol": row["raw_symbol"],
                "completed_trading_date": row["completed_trading_date"],
                "derived_completed_bar_end_utc": row["derived_completed_bar_end_utc"],
                "source_daily_runtime_completed_trading_date": runtime_day,
                "source_daily_runtime_lag_days": lag,
                "current_held_price": price,
                "annual_risk_estimate_sigma_percent": annual_risk,
                "contract_risk_usd": contract_risk,
                "target_currency_risk_usd": target_currency_risk,
                "base_unrounded_contracts": base_unrounded,
                "capped_forecast": capped,
                "forecast_multiplier": capped / FORECAST_DIVISOR,
            }
        )
    return rows


def _replay_position_rows(ladder_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in ladder_rows:
        desired = float(row["base_unrounded_contracts"]) * float(row["forecast_multiplier"])
        rows.append(
            {
                "raw_symbol": row["raw_symbol"],
                "completed_trading_date": row["completed_trading_date"],
                "derived_completed_bar_end_utc": row["derived_completed_bar_end_utc"],
                "base_unrounded_contracts": row["base_unrounded_contracts"],
                "capped_forecast": row["capped_forecast"],
                "forecast_multiplier": row["forecast_multiplier"],
                "desired_unrounded_contracts": desired,
                "desired_rounded_contracts_nearest": round(desired),
            }
        )
    return rows


def _replay_backtest_rows(position_rows: list[dict[str, Any]], hourly_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    return _build_null_backtest(position_rows, hourly_rows, mode="BASE")


def _build_null_backtest(position_rows: list[dict[str, Any]], hourly_rows: list[dict[str, str]], mode: str) -> list[dict[str, Any]]:
    hourly_by_ts = {row["derived_completed_bar_end_utc"]: row for row in hourly_rows}
    ordered_ts = sorted(hourly_by_ts)
    base_position_by_ts = {row["derived_completed_bar_end_utc"]: int(row["desired_rounded_contracts_nearest"]) for row in position_rows}
    position_by_ts = _null_position_map(mode, ordered_ts, hourly_by_ts, base_position_by_ts)
    rows: list[dict[str, Any]] = []
    cumulative_gross = 0.0
    cumulative_cost = 0.0
    cumulative_net = 0.0
    prior_position: int | None = None
    for entry_ts, exit_ts in zip(ordered_ts[:-1], ordered_ts[1:], strict=True):
        if entry_ts not in position_by_ts:
            continue
        entry_bar = hourly_by_ts[entry_ts]
        exit_bar = hourly_by_ts[exit_ts]
        contracts = int(position_by_ts[entry_ts])
        price_change = float(exit_bar["continuous_close"]) - float(entry_bar["continuous_close"])
        gross = contracts * price_change * ZN_MULTIPLIER
        position_change = 0 if prior_position is None else contracts - prior_position
        roll_transition_sides = abs(contracts) * 2 if entry_bar["raw_symbol"] != exit_bar["raw_symbol"] and contracts != 0 else 0
        position_change_sides = abs(position_change)
        total_fee_sides = position_change_sides + roll_transition_sides
        fee = total_fee_sides * ETF_ZN_FEE_PER_SIDE_USD
        prior_position = contracts
        cumulative_gross += gross
        cumulative_cost += fee
        cumulative_net += gross - fee
        rows.append(
            {
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
                "entry_continuous_close": float(entry_bar["continuous_close"]),
                "exit_continuous_close": float(exit_bar["continuous_close"]),
                "price_change_points": price_change,
                "gross_pnl_usd": gross,
                "estimated_fee_usd": fee,
                "net_after_fees_usd": gross - fee,
                "cumulative_gross_pnl_usd": cumulative_gross,
                "cumulative_estimated_fees_usd": cumulative_cost,
                "cumulative_net_after_fees_usd": cumulative_net,
            }
        )
    return rows


def _null_position_map(
    mode: str,
    ordered_ts: list[str],
    hourly_by_ts: dict[str, dict[str, str]],
    base_position_by_ts: dict[str, int],
) -> dict[str, int]:
    if mode == "BASE":
        return dict(base_position_by_ts)
    if mode == "INVERTED":
        return {ts: -position for ts, position in base_position_by_ts.items()}
    if mode == "ONE_BAR_DELAYED":
        out: dict[str, int] = {}
        prior_position = 0
        for ts in ordered_ts:
            if ts in base_position_by_ts:
                out[ts] = prior_position
                prior_position = base_position_by_ts[ts]
        return out
    if mode == "DAY_SHUFFLED":
        by_day: dict[str, list[int]] = {}
        for ts, position in base_position_by_ts.items():
            by_day.setdefault(hourly_by_ts[ts]["completed_trading_date"], []).append(position)
        days = sorted(by_day)
        shuffled_days = list(days)
        random.Random(172004).shuffle(shuffled_days)
        day_map = dict(zip(days, shuffled_days, strict=True))
        offsets: dict[str, int] = {}
        for day, positions in by_day.items():
            offsets[day] = len(positions)
        counters: Counter[str] = Counter()
        out = {}
        for ts in sorted(base_position_by_ts):
            day = hourly_by_ts[ts]["completed_trading_date"]
            source_day = day_map[day]
            source_positions = by_day[source_day]
            out[ts] = source_positions[counters[day] % len(source_positions)]
            counters[day] += 1
        return out
    raise RuntimeError(f"unknown null mode {mode}")


def _aggregate_parity_rows(
    period: PeriodArtifacts,
    reported_status: dict[str, Any],
    reported_backtest_rows: list[dict[str, str]],
    replay_backtest_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    reported_gross = sum(float(row["gross_pnl_usd"]) for row in reported_backtest_rows)
    reported_fees = sum(_fee(row) for row in reported_backtest_rows)
    reported_net = sum(_net(row) for row in reported_backtest_rows)
    replayed_gross = sum(float(row["gross_pnl_usd"]) for row in replay_backtest_rows)
    replayed_fees = sum(_fee(row) for row in replay_backtest_rows)
    replayed_net = sum(_net(row) for row in replay_backtest_rows)
    return [
        _check(period, "backtest_row_count", len(reported_backtest_rows), len(replay_backtest_rows)),
        _check(period, "gross_pnl_sum", reported_gross, replayed_gross),
        _check(period, "fee_sum", reported_fees, replayed_fees),
        _check(period, "net_pnl_sum", reported_net, replayed_net),
        _check(period, "reported_status_gross", reported_status.get("gross_pnl_usd"), reported_gross),
        _check(period, "reported_status_net", _status_net(reported_status), reported_net),
    ]


def _row_replay_rows(
    period: PeriodArtifacts,
    reported_backtest_rows: list[dict[str, str]],
    replay_backtest_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    replay_by_entry = {row["entry_bar_end_utc"]: row for row in replay_backtest_rows}
    sorted_reported = sorted(reported_backtest_rows, key=lambda row: float(row["gross_pnl_usd"]))
    selected = sorted_reported[:10] + sorted_reported[-10:]
    rng = random.Random(172004)
    selected.extend(rng.sample(reported_backtest_rows, min(20, len(reported_backtest_rows))))
    seen = set()
    rows: list[dict[str, Any]] = []
    for row in selected:
        key = row["entry_bar_end_utc"]
        if key in seen:
            continue
        seen.add(key)
        replay = replay_by_entry.get(key)
        if replay is None:
            rows.append(_replay_check(period, row, None, "missing_replay_row", "FAIL"))
            continue
        checks = [
            _float_equal(float(row["gross_pnl_usd"]), float(replay["gross_pnl_usd"])),
            _float_equal(_fee(row), _fee(replay)),
            _float_equal(_net(row), _net(replay)),
            int(row["held_contracts_m1_ladder"]) == int(replay["held_contracts_m1_ladder"]),
            _float_equal(float(row["price_change_points"]), float(replay["price_change_points"])),
        ]
        rows.append(_replay_check(period, row, replay, "row_replay", "PASS" if all(checks) else "FAIL"))
    return rows


def _lookahead_rows(
    period: PeriodArtifacts,
    forecasts: list[dict[str, str]],
    ladder_rows: list[dict[str, Any]],
    backtest_rows: list[dict[str, str]],
) -> list[dict[str, Any]]:
    forecast_lags = [int(row.get("source_daily_runtime_lag_days", "0")) for row in forecasts]
    ladder_lags = [int(row["source_daily_runtime_lag_days"]) for row in ladder_rows]
    entry_before_exit = all(_parse_ts(row["entry_bar_end_utc"]) < _parse_ts(row["exit_bar_end_utc"]) for row in backtest_rows)
    return [
        _boolean_check(period, "forecast_daily_runtime_strict_prior", all(lag > 0 for lag in forecast_lags), len(forecast_lags)),
        _boolean_check(period, "forecast_daily_runtime_not_stale", all(lag <= MAX_SOURCE_RUNTIME_LAG_DAYS for lag in forecast_lags), len(forecast_lags)),
        _boolean_check(period, "ladder_daily_runtime_strict_prior", all(lag > 0 for lag in ladder_lags), len(ladder_lags)),
        _boolean_check(period, "ladder_daily_runtime_not_stale", all(lag <= MAX_SOURCE_RUNTIME_LAG_DAYS for lag in ladder_lags), len(ladder_lags)),
        _boolean_check(period, "pnl_exit_after_entry", entry_before_exit, len(backtest_rows)),
        _boolean_check(period, "position_from_entry_completed_bar_only", all(row["lookahead_status"].startswith("PASS") for row in backtest_rows), len(backtest_rows)),
    ]


def _lineage_rows(
    period: PeriodArtifacts,
    forecasts: list[dict[str, str]],
    hourly_rows: list[dict[str, str]],
    ladder_rows: list[dict[str, str]],
    position_rows: list[dict[str, str]],
    backtest_rows: list[dict[str, str]],
) -> list[dict[str, Any]]:
    forecast_ts = [row["derived_completed_bar_end_utc"] for row in forecasts]
    hourly_ts = [row["derived_completed_bar_end_utc"] for row in hourly_rows]
    ladder_ts = [row["derived_completed_bar_end_utc"] for row in ladder_rows]
    position_ts = [row["derived_completed_bar_end_utc"] for row in position_rows]
    entry_ts = [row["entry_bar_end_utc"] for row in backtest_rows]
    exit_ts = [row["exit_bar_end_utc"] for row in backtest_rows]
    hourly_set = set(hourly_ts)
    forecast_set = set(forecast_ts)
    ladder_set = set(ladder_ts)
    position_set = set(position_ts)
    return [
        _boolean_check(period, "forecast_timestamps_unique", len(forecast_ts) == len(forecast_set), len(forecast_ts)),
        _boolean_check(period, "hourly_timestamps_unique", len(hourly_ts) == len(hourly_set), len(hourly_ts)),
        _boolean_check(period, "ladder_timestamps_subset_forecast", set(ladder_ts).issubset(forecast_set), len(ladder_ts)),
        _boolean_check(period, "position_timestamps_subset_ladder", set(position_ts).issubset(ladder_set), len(position_ts)),
        _boolean_check(period, "backtest_entry_timestamps_subset_position", set(entry_ts).issubset(position_set), len(entry_ts)),
        _boolean_check(period, "backtest_entry_timestamps_subset_hourly", set(entry_ts).issubset(hourly_set), len(entry_ts)),
        _boolean_check(period, "backtest_exit_timestamps_subset_hourly", set(exit_ts).issubset(hourly_set), len(exit_ts)),
        _boolean_check(period, "non_empty_sha_inputs", all(_sha256(path) for path in (period.forecast_csv, period.hourly_csv, period.ladder_csv, period.position_csv, period.backtest_csv)), 5),
    ]


def _null_rows(period: PeriodArtifacts, position_rows: list[dict[str, Any]], hourly_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows = []
    for mode in ("BASE", "INVERTED", "ONE_BAR_DELAYED", "DAY_SHUFFLED"):
        backtest = _build_null_backtest(position_rows, hourly_rows, mode=mode)
        rows.append(
            {
                "period_label": period.label,
                "stage": period.stage,
                "null_mode": mode,
                "row_count": len(backtest),
                "gross_pnl_usd": sum(float(row["gross_pnl_usd"]) for row in backtest),
                "fees_usd": sum(_fee(row) for row in backtest),
                "net_after_fees_usd": sum(_net(row) for row in backtest),
                "purpose": "BUG_DETECTION_ONLY_NOT_TUNING_NOT_ALPHA_STATISTIC",
            }
        )
    return rows


def _overall_status(
    summaries: list[dict[str, Any]],
    parity_rows: list[dict[str, Any]],
    replay_rows: list[dict[str, Any]],
    lookahead_rows: list[dict[str, Any]],
    lineage_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    blocking = [
        row
        for row in (parity_rows + replay_rows + lookahead_rows + lineage_rows)
        if row.get("check_status") != "PASS"
    ]
    return {
        "gate": GATE,
        "status": "PASS_S27_ZN_BACKTEST_PARITY_VERIFIED_BEFORE_LOCKBOX" if not blocking else "FAIL_CLOSED_S27_ZN_BACKTEST_PARITY_GAP",
        "periods": [row["period_label"] for row in summaries],
        "blocking_findings": len(blocking),
        "period_count": len(summaries),
        "aggregate_parity_rows": len(parity_rows),
        "row_replay_rows": len(replay_rows),
        "lookahead_rows": len(lookahead_rows),
        "lineage_rows": len(lineage_rows),
        "null_tests_run": "YES_BUG_DETECTION_ONLY_NOT_TUNING",
        "provider_api_access": "NO",
        "new_data_download": "NO",
        "oos_access": "NO",
        "lockbox_access": "NO",
        "forward_access": "NO",
        "deployment": "NO",
        "trading": "NO",
        "promotion": "NO",
    }


def _check(period: PeriodArtifacts, name: str, reported: Any, replayed: Any) -> dict[str, Any]:
    passed = _float_equal(float(reported), float(replayed)) if _is_number(reported) and _is_number(replayed) else reported == replayed
    return {
        "period_label": period.label,
        "stage": period.stage,
        "check_name": name,
        "reported_value": reported,
        "replayed_value": replayed,
        "absolute_difference": abs(float(reported) - float(replayed)) if _is_number(reported) and _is_number(replayed) else "",
        "check_status": "PASS" if passed else "FAIL",
    }


def _boolean_check(period: PeriodArtifacts, name: str, passed: bool, observed_count: int) -> dict[str, Any]:
    return {
        "period_label": period.label,
        "stage": period.stage,
        "check_name": name,
        "observed_count": observed_count,
        "check_status": "PASS" if passed else "FAIL",
    }


def _replay_check(period: PeriodArtifacts, reported: dict[str, str], replay: dict[str, Any] | None, name: str, status: str) -> dict[str, Any]:
    return {
        "period_label": period.label,
        "stage": period.stage,
        "check_name": name,
        "entry_bar_end_utc": reported["entry_bar_end_utc"],
        "exit_bar_end_utc": reported["exit_bar_end_utc"],
        "reported_contracts": reported.get("held_contracts_m1_ladder"),
        "replayed_contracts": replay.get("held_contracts_m1_ladder") if replay else "",
        "reported_price_change_points": reported.get("price_change_points"),
        "replayed_price_change_points": replay.get("price_change_points") if replay else "",
        "reported_gross_pnl_usd": reported.get("gross_pnl_usd"),
        "replayed_gross_pnl_usd": replay.get("gross_pnl_usd") if replay else "",
        "reported_net_after_fees_usd": _net(reported),
        "replayed_net_after_fees_usd": _net(replay) if replay else "",
        "check_status": status,
    }


def _process_result_text(overall: dict[str, Any], summaries: list[dict[str, Any]]) -> str:
    lines = [
        "# Carver S27 ZN Backtest Parity Verification Result",
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
        "| Period | Stage | Net | Replay Net | Inverted Null Net | Delayed Null Net | Shuffled Null Net |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for row in summaries:
        lines.append(
            f"| {row['period_label']} | {row['stage']} | {row['reported_net_after_fees_usd']} | "
            f"{row['replayed_net_after_fees_usd']} | {row['null_inverted_net_after_fees_usd']} | "
            f"{row['null_one_bar_delayed_net_after_fees_usd']} | {row['null_day_shuffled_net_after_fees_usd']} |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This verifier uses existing local ZN artifacts only. It does not request provider data, download market rows, open OOS/Lockbox/Forward, tune parameters, deploy, trade, promote, or claim alpha. Null tests are bug-detection checks only.",
            "",
        ]
    )
    return "\n".join(lines)


def _local_audit_text(overall: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Local Hostile Audit - S27 ZN Backtest Parity Verification",
            "",
            "Mode: automatic local hostile audit over parity, replay, lookahead, lineage, and null-test artifacts.",
            "",
            "CRITICAL: None if status is PASS.",
            "",
            f"Blocking findings observed: `{overall['blocking_findings']}`.",
            "",
            "HIGH: None. The verifier does not import or call the original backtest scripts, does not access provider APIs, and does not open OOS/Lockbox/Forward.",
            "",
            "MEDIUM: Null tests are bug-detection checks only. They are not tuning criteria and must not be used to select parameters, symbols, costs, or windows.",
            "",
            "Verdict:",
            "",
            "```text",
            "BLOCKING_FINDINGS: NO" if overall["blocking_findings"] == 0 else "BLOCKING_FINDINGS: YES",
            f"AUDIT_DISPOSITION: {overall['status']}",
            "```",
            "",
        ]
    )


def _provenance_payload(overall: dict[str, Any]) -> dict[str, Any]:
    return {
        "gate": GATE,
        "created_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "status": overall,
        "input_artifacts": [
            {
                "period_label": period.label,
                "forecast_csv": str(period.forecast_csv.relative_to(ROOT)),
                "forecast_sha256": _sha256(period.forecast_csv),
                "hourly_csv": str(period.hourly_csv.relative_to(ROOT)),
                "hourly_sha256": _sha256(period.hourly_csv),
                "backtest_csv": str(period.backtest_csv.relative_to(ROOT)),
                "backtest_sha256": _sha256(period.backtest_csv),
            }
            for period in PERIODS
        ],
        "non_authorization": [
            "NO_PROVIDER_API_ACCESS",
            "NO_NEW_DATA_DOWNLOAD",
            "NO_OOS",
            "NO_LOCKBOX",
            "NO_FORWARD",
            "NO_DEPLOYMENT",
            "NO_TRADING",
            "NO_PROMOTION",
            "NO_PARAMETER_TUNING",
        ],
    }


def _require_period(period: PeriodArtifacts) -> None:
    for path in (period.forecast_csv, period.hourly_csv, period.ladder_csv, period.position_csv, period.backtest_csv, period.status_json):
        if not path.exists():
            raise SystemExit(f"Fail closed: missing required artifact {path}")


def _folders() -> dict[str, Path]:
    return {
        "parity": OUTPUT_ROOT / "parity",
        "replay": OUTPUT_ROOT / "row_replay",
        "lookahead": OUTPUT_ROOT / "lookahead",
        "lineage": OUTPUT_ROOT / "lineage",
        "null": OUTPUT_ROOT / "null_tests",
        "summary": OUTPUT_ROOT / "summary",
        "status": OUTPUT_ROOT / "status",
        "provenance": OUTPUT_ROOT / "provenance",
        "hashes": OUTPUT_ROOT / "hashes",
    }


def _read_csv(path: Path) -> list[dict[str, str]]:
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


def _hash_tree(root: Path) -> dict[str, str]:
    ledger_name = f"{RUN_ID}_sha256.json"
    return {
        str(path.relative_to(ROOT)): _sha256(path)
        for path in sorted(root.rglob("*"))
        if path.is_file() and path.name != ledger_name
    }


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def _parse_ts(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _runtime_lag_days(day: str, runtime_day: str) -> int:
    return (date.fromisoformat(day) - date.fromisoformat(runtime_day)).days


def _fee(row: dict[str, Any]) -> float:
    for field in ("estimated_etf_fee_usd", "estimated_fee_usd"):
        if field in row:
            return float(row[field])
    raise KeyError("fee field not found")


def _net(row: dict[str, Any]) -> float:
    for field in ("net_after_etf_fees_usd", "net_after_fees_usd"):
        if field in row:
            return float(row[field])
    raise KeyError("net field not found")


def _status_net(status: dict[str, Any]) -> Any:
    return status.get("net_after_etf_fees_usd", status.get("net_after_fees_usd"))


def _float_equal(left: float, right: float) -> bool:
    return math.isfinite(left) and math.isfinite(right) and abs(left - right) <= EPSILON


def _is_number(value: Any) -> bool:
    try:
        float(value)
        return True
    except (TypeError, ValueError):
        return False


if __name__ == "__main__":
    main()
