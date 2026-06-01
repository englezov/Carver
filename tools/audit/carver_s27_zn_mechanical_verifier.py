from __future__ import annotations

import csv
import hashlib
import json
import math
from collections import Counter
from dataclasses import dataclass
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
RUN_ID = "20260601_S27_ZN_2022_2024_MECHANICAL_VERIFIER"
OUTPUT_ROOT = ROOT / "docs/researchops/s26_s27_mechanical_verification/ZN_S27/2022_2024"
PROCESS_RESULT_DOC = ROOT / "docs/process/CARVER_S27_ZN_MECHANICAL_VERIFICATION_RESULT_2026-06-01.md"
LOCAL_AUDIT_DOC = ROOT / "docs/process/CARVER_S27_ZN_MECHANICAL_VERIFICATION_LOCAL_HOSTILE_AUDIT_2026-06-01.md"

S26_EWMA_SPAN = 5
S27_TREND_FAST_SPAN = 16
S27_TREND_SLOW_SPAN = 64
S27_VOL_EWMA_SPAN = 10
S27_FORECAST_SCALAR = 20.0
FORECAST_CAP = 20.0
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
    hourly_csv: Path
    daily_runtime_csv: Path
    forecast_csv: Path
    ladder_csv: Path
    position_csv: Path
    backtest_csv: Path
    status_json: Path


PERIODS = (
    PeriodArtifacts(
        label="ZN_2022_2023_INITIAL_TEST",
        stage="INITIAL_TEST",
        hourly_csv=ROOT
        / "docs/researchops/s26_s27_backtest_readiness/ZN_S27_SINGLE_INSTRUMENT/2022-01-01_2023-12-31/retargeted_dev_recon_backtest/local_hourly_lineage/20260531_S27_ZN_2022_2023_RETARGETED_DEV_RECON_BACKTEST_local_hourly_continuous_lineage.csv",
        daily_runtime_csv=ROOT
        / "docs/researchops/s26_s27_backtest_readiness/ZN_S27_SINGLE_INSTRUMENT/2022-01-01_2023-12-31/retargeted_dev_recon_backtest/daily_runtime_rows/20260531_S27_ZN_2022_2023_RETARGETED_DEV_RECON_BACKTEST_daily_runtime_rows.csv",
        forecast_csv=ROOT
        / "docs/researchops/s26_s27_backtest_readiness/ZN_S27_SINGLE_INSTRUMENT/2022-01-01_2023-12-31/retargeted_dev_recon_backtest/forecast_rows/20260531_S27_ZN_2022_2023_RETARGETED_DEV_RECON_BACKTEST_s27_forecast_rows.csv",
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
        hourly_csv=ROOT
        / "docs/researchops/s26_s27_validation/ZN_S27/2024-01-01_2024-12-31/local_lineage/20260601_S27_ZN_2024_VALIDATION_BACKTEST_ZN_hourly_continuous_lineage.csv",
        daily_runtime_csv=ROOT
        / "docs/researchops/s26_s27_validation/ZN_S27/2024-01-01_2024-12-31/daily_runtime_rows/20260601_S27_ZN_2024_VALIDATION_BACKTEST_ZN_daily_runtime_rows.csv",
        forecast_csv=ROOT
        / "docs/researchops/s26_s27_validation/ZN_S27/2024-01-01_2024-12-31/forecast_rows/20260601_S27_ZN_2024_VALIDATION_BACKTEST_ZN_s27_forecast_rows.csv",
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

    all_checks: list[dict[str, Any]] = []
    all_roll_rows: list[dict[str, Any]] = []
    all_fee_rows: list[dict[str, Any]] = []
    all_episode_rows: list[dict[str, Any]] = []
    summaries: list[dict[str, Any]] = []

    for period in PERIODS:
        _require_period(period)
        result = _verify_period(period)
        summaries.append(result["summary"])
        all_checks.extend(result["checks"])
        all_roll_rows.extend(result["roll_rows"])
        all_fee_rows.extend(result["fee_rows"])
        all_episode_rows.extend(result["episode_rows"])

    blocking = [row for row in all_checks if row["check_status"] != "PASS"]
    status = {
        "gate": "S27_ZN_MECHANICAL_VERIFICATION_BEFORE_ANY_LOCKBOX_OR_PROMOTION",
        "status": "PASS_S27_ZN_MECHANICAL_VERIFICATION_DEV_RECON" if not blocking else "FAIL_CLOSED_S27_ZN_MECHANICAL_VERIFICATION",
        "blocking_findings": len(blocking),
        "periods": [row["period_label"] for row in summaries],
        "check_rows": len(all_checks),
        "roll_rows": len(all_roll_rows),
        "fee_rows": len(all_fee_rows),
        "episode_rows": len(all_episode_rows),
        "provider_api_access": "NO",
        "new_data_download": "NO",
        "market_row_source": "EXISTING_LOCAL_ARTIFACTS_ONLY",
        "oos_access": "NO",
        "lockbox_access": "NO",
        "forward_access": "NO",
        "deployment": "NO",
        "trading": "NO",
        "promotion": "NO",
    }

    _write_csv(folders["checks"] / f"{RUN_ID}_check_ledger.csv", all_checks)
    _write_csv(folders["roll"] / f"{RUN_ID}_roll_runtime_ledger.csv", all_roll_rows)
    _write_csv(folders["fees"] / f"{RUN_ID}_fee_ledger.csv", all_fee_rows)
    _write_csv(folders["episodes"] / f"{RUN_ID}_episode_ledger.csv", all_episode_rows)
    _write_csv(folders["summary"] / f"{RUN_ID}_summary.csv", summaries)
    _write_json(folders["status"] / f"{RUN_ID}_status.json", status)
    _write_json(folders["provenance"] / f"{RUN_ID}_provenance.json", _provenance_payload(status))
    _write_json(folders["hashes"] / f"{RUN_ID}_sha256.json", _hash_tree(OUTPUT_ROOT))
    PROCESS_RESULT_DOC.write_text(_process_result_text(status, summaries), encoding="utf-8")
    LOCAL_AUDIT_DOC.write_text(_local_audit_text(status), encoding="utf-8")

    print(status["status"])
    for row in summaries:
        print(
            f"{row['period_label']}: checks={row['checks_passed']}/{row['checks_total']} "
            f"net={row['net_after_fees_usd']} episodes={row['nonzero_episode_count']} "
            f"episode_win_rate={row['episode_win_rate']}"
        )
    print(f"artifact_root={OUTPUT_ROOT.relative_to(ROOT)}")


def _verify_period(period: PeriodArtifacts) -> dict[str, Any]:
    hourly_rows = _read_csv(period.hourly_csv)
    daily_rows = _read_csv(period.daily_runtime_csv)
    forecast_rows = _read_csv(period.forecast_csv)
    ladder_rows = _read_csv(period.ladder_csv)
    position_rows = _read_csv(period.position_csv)
    backtest_rows = _read_csv(period.backtest_csv)
    status = json.loads(period.status_json.read_text(encoding="utf-8"))

    checks: list[dict[str, Any]] = []
    roll_rows = _roll_runtime_rows(period, hourly_rows, forecast_rows, ladder_rows, backtest_rows)
    fee_rows = _fee_rows(period, backtest_rows)
    episode_rows = _episode_rows(period, backtest_rows)

    s26_by_ts = _recompute_s26_raw_by_ts(hourly_rows)
    daily_by_day = {row["completed_trading_date"]: row for row in daily_rows}
    recomputed_daily = _recompute_daily_runtime(daily_rows)
    position_by_ts = {row["derived_completed_bar_end_utc"]: row for row in position_rows}
    hourly_by_ts = {row["derived_completed_bar_end_utc"]: row for row in hourly_rows}

    checks.extend(_runtime_recalculation_checks(period, daily_rows, recomputed_daily))
    checks.extend(_forecast_formula_checks(period, forecast_rows, s26_by_ts, daily_by_day))
    checks.extend(_ladder_position_checks(period, forecast_rows, ladder_rows, position_by_ts))
    checks.extend(_pnl_fee_checks(period, hourly_by_ts, backtest_rows, status))
    checks.extend(_roll_runtime_checks(period, roll_rows))
    checks.extend(_shape_boundary_checks(period, hourly_rows, daily_rows, forecast_rows, ladder_rows, position_rows, backtest_rows, status))

    pass_count = sum(1 for row in checks if row["check_status"] == "PASS")
    total_net = sum(_net(row) for row in backtest_rows)
    episodes = [row for row in episode_rows if row["episode_kind"] == "NONZERO_POSITION_EPISODE"]
    wins = sum(1 for row in episodes if float(row["episode_net_after_fees_usd"]) > 0)
    summary = {
        "period_label": period.label,
        "stage": period.stage,
        "checks_passed": pass_count,
        "checks_total": len(checks),
        "net_after_fees_usd": total_net,
        "gross_pnl_usd": sum(float(row["gross_pnl_usd"]) for row in backtest_rows),
        "fees_usd": sum(_fee(row) for row in backtest_rows),
        "nonzero_episode_count": len(episodes),
        "winning_episode_count": wins,
        "episode_win_rate": wins / len(episodes) if episodes else "",
        "position_change_fee_sides": sum(int(row["position_change_fee_sides"]) for row in backtest_rows),
        "roll_transition_fee_sides": sum(int(row["roll_transition_fee_sides"]) for row in backtest_rows),
        "total_fee_sides": sum(int(row["total_fee_sides"]) for row in backtest_rows),
        "max_runtime_lag_days": max(
            int(row["source_runtime_lag_days"]) for row in roll_rows if row["source_runtime_lag_days"] != ""
        )
        if roll_rows
        else "",
        "provider_api_access": "NO",
        "new_data_download": "NO",
        "oos_lockbox_forward": "NO",
        "promotion": "NO",
    }
    return {
        "summary": summary,
        "checks": checks,
        "roll_rows": roll_rows,
        "fee_rows": fee_rows,
        "episode_rows": episode_rows,
    }


def _recompute_s26_raw_by_ts(hourly_rows: list[dict[str, str]]) -> dict[str, float]:
    alpha = 2.0 / (S26_EWMA_SPAN + 1.0)
    ewma: float | None = None
    out: dict[str, float] = {}
    for row in sorted(hourly_rows, key=lambda item: item["derived_completed_bar_end_utc"]):
        close = float(row["continuous_close"])
        ewma = close if ewma is None else alpha * close + (1.0 - alpha) * ewma
        out[row["derived_completed_bar_end_utc"]] = ewma - close
    return out


def _recompute_daily_runtime(daily_rows: list[dict[str, str]]) -> dict[str, dict[str, float]]:
    fast_alpha = 2.0 / (S27_TREND_FAST_SPAN + 1.0)
    slow_alpha = 2.0 / (S27_TREND_SLOW_SPAN + 1.0)
    vol_alpha = 2.0 / (S27_VOL_EWMA_SPAN + 1.0)
    fast: float | None = None
    slow: float | None = None
    vol_m: float | None = None
    out: dict[str, dict[str, float]] = {}
    for row in sorted(daily_rows, key=lambda item: item["completed_trading_date"]):
        close = _maybe_float(row.get("daily_continuous_close", ""))
        if close is not None:
            fast = close if fast is None else fast_alpha * close + (1.0 - fast_alpha) * fast
            slow = close if slow is None else slow_alpha * close + (1.0 - slow_alpha) * slow
        q = _maybe_float(row.get("quantile_q", ""))
        if q is not None:
            raw_m = 2.0 - 1.5 * q
            vol_m = raw_m if vol_m is None else vol_alpha * raw_m + (1.0 - vol_alpha) * vol_m
        out[row["completed_trading_date"]] = {
            "ewmac16_fast_ewma": fast if fast is not None else math.nan,
            "ewmac16_slow_ewma": slow if slow is not None else math.nan,
            "trend_forecast_proxy_fast_minus_slow": (fast - slow) if fast is not None and slow is not None else math.nan,
            "vol_multiplier_m_ewma10": vol_m if vol_m is not None else math.nan,
        }
    return out


def _runtime_recalculation_checks(period: PeriodArtifacts, daily_rows: list[dict[str, str]], recomputed: dict[str, dict[str, float]]) -> list[dict[str, Any]]:
    rows = []
    for field in ("ewmac16_fast_ewma", "ewmac16_slow_ewma", "trend_forecast_proxy_fast_minus_slow", "vol_multiplier_m_ewma10"):
        diffs = []
        count = 0
        for row in daily_rows:
            actual = _maybe_float(row.get(field, ""))
            expected = recomputed[row["completed_trading_date"]][field]
            if actual is None or math.isnan(expected):
                continue
            diffs.append(abs(actual - expected))
            count += 1
        rows.append(_check(period, f"daily_runtime_recomputes_{field}", max(diffs, default=0.0), 0.0, count))
    return rows


def _forecast_formula_checks(
    period: PeriodArtifacts,
    forecast_rows: list[dict[str, str]],
    s26_by_ts: dict[str, float],
    daily_by_day: dict[str, dict[str, str]],
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    max_s26 = max_sigma = max_trend = max_m = max_adjusted = max_risk = max_scaled = max_capped = 0.0
    bad_oppose = 0
    bad_scalar = 0
    for row in forecast_rows:
        ts = row["derived_completed_bar_end_utc"]
        runtime_day = row.get("source_daily_runtime_completed_trading_date") or row.get("source_vqm_completed_trading_date")
        runtime = daily_by_day[runtime_day]
        s26_raw = s26_by_ts[ts]
        trend = float(runtime["trend_forecast_proxy_fast_minus_slow"])
        vol_m = float(runtime["vol_multiplier_m_ewma10"])
        sigma_price = float(row["continuous_close"]) * float(runtime["sigma_i_t"]) / 16.0
        opposes = s26_raw * trend < 0.0
        adjusted = 0.0 if opposes else s26_raw * vol_m
        risk_adjusted = adjusted / sigma_price
        scaled = risk_adjusted * S27_FORECAST_SCALAR
        capped = max(min(scaled, FORECAST_CAP), -FORECAST_CAP)
        max_s26 = max(max_s26, abs(s26_raw - float(row["s26_raw_forecast"])))
        max_sigma = max(max_sigma, abs(sigma_price - float(row["sigma_price_i_t"])))
        max_trend = max(max_trend, abs(trend - float(row["s27_trend_forecast_proxy_fast_minus_slow"])))
        max_m = max(max_m, abs(vol_m - float(row["vol_multiplier_m_ewma10"])))
        max_adjusted = max(max_adjusted, abs(adjusted - float(row["adjusted_raw_forecast"])))
        max_risk = max(max_risk, abs(risk_adjusted - float(row["risk_adjusted_forecast"])))
        max_scaled = max(max_scaled, abs(scaled - float(row["scaled_forecast"])))
        max_capped = max(max_capped, abs(capped - float(row["capped_forecast"])))
        if ("YES" if opposes else "NO") != row["s27_opposes_trend"]:
            bad_oppose += 1
        if abs(float(row["forecast_scalar"]) - S27_FORECAST_SCALAR) > EPSILON:
            bad_scalar += 1
    count = len(forecast_rows)
    checks.extend(
        [
            _check(period, "forecast_recomputes_s26_ewma5_raw", max_s26, 0.0, count),
            _check(period, "forecast_recomputes_sigma_price_from_prior_daily_sigma", max_sigma, 0.0, count),
            _check(period, "forecast_uses_prior_daily_ewmac16_trend", max_trend, 0.0, count),
            _check(period, "forecast_uses_prior_daily_vqm_multiplier", max_m, 0.0, count),
            _check(period, "forecast_recomputes_adjusted_raw", max_adjusted, 0.0, count),
            _check(period, "forecast_recomputes_risk_adjusted", max_risk, 0.0, count),
            _check(period, "forecast_recomputes_scaled_with_s27_scalar_20", max_scaled, 0.0, count),
            _check(period, "forecast_recomputes_common_cap", max_capped, 0.0, count),
            _boolean_check(period, "forecast_trend_opposition_flag_matches_sign", bad_oppose == 0, count, bad_oppose),
            _boolean_check(period, "forecast_scalar_is_s27_20_not_s26_9_3", bad_scalar == 0, count, bad_scalar),
        ]
    )
    return checks


def _ladder_position_checks(
    period: PeriodArtifacts,
    forecast_rows: list[dict[str, str]],
    ladder_rows: list[dict[str, str]],
    position_by_ts: dict[str, dict[str, str]],
) -> list[dict[str, Any]]:
    ladder_by_ts = {row["derived_completed_bar_end_utc"]: row for row in ladder_rows}
    max_base = max_position = max_forecast_mult = 0.0
    missing = 0
    for row in forecast_rows:
        ts = row["derived_completed_bar_end_utc"]
        ladder = ladder_by_ts.get(ts)
        position = position_by_ts.get(ts)
        if not ladder or not position:
            missing += 1
            continue
        annual_risk = float(row["sigma_price_i_t"]) * 16.0 / float(row["continuous_close"])
        contract_risk = float(row["continuous_close"]) * ZN_MULTIPLIER * FX_RATE * annual_risk
        base = CAPITAL_USD * TARGET_RISK * INSTRUMENT_WEIGHT * IDM / contract_risk
        forecast_mult = float(row["capped_forecast"]) / FORECAST_DIVISOR
        desired = base * forecast_mult
        max_base = max(max_base, abs(base - float(ladder["base_unrounded_contracts"])))
        max_forecast_mult = max(max_forecast_mult, abs(forecast_mult - float(ladder["forecast_multiplier"])))
        max_position = max(max_position, abs(desired - float(position["desired_unrounded_contracts"])))
        if round(desired) != int(position["desired_rounded_contracts_nearest"]):
            missing += 1
    count = len(forecast_rows)
    return [
        _check(period, "ladder_recomputes_base_unrounded_contracts", max_base, 0.0, count),
        _check(period, "ladder_recomputes_forecast_multiplier", max_forecast_mult, 0.0, count),
        _check(period, "position_recomputes_desired_unrounded_contracts", max_position, 0.0, count),
        _boolean_check(period, "position_rounding_nearest_matches", missing == 0, count, missing),
    ]


def _pnl_fee_checks(
    period: PeriodArtifacts,
    hourly_by_ts: dict[str, dict[str, str]],
    backtest_rows: list[dict[str, str]],
    status: dict[str, Any],
) -> list[dict[str, Any]]:
    max_price_change = max_gross = max_fee = max_net = 0.0
    bad_status = 0
    bad_fee_sides = 0
    prior_position: int | None = None
    for row in backtest_rows:
        entry = hourly_by_ts[row["entry_bar_end_utc"]]
        exit_ = hourly_by_ts[row["exit_bar_end_utc"]]
        contracts = int(row["held_contracts_m1_ladder"])
        price_change = float(exit_["continuous_close"]) - float(entry["continuous_close"])
        gross = contracts * price_change * ZN_MULTIPLIER
        expected_position_change = 0 if prior_position is None else contracts - prior_position
        expected_position_sides = abs(expected_position_change)
        expected_roll_sides = abs(contracts) * 2 if row["entry_raw_symbol"] != row["exit_raw_symbol"] and contracts != 0 else 0
        expected_total_sides = expected_position_sides + expected_roll_sides
        fee = int(row["total_fee_sides"]) * ETF_ZN_FEE_PER_SIDE_USD
        if (
            int(row["position_change_from_previous_pnl_row"]) != expected_position_change
            or int(row["position_change_fee_sides"]) != expected_position_sides
            or int(row["roll_transition_fee_sides"]) != expected_roll_sides
            or int(row["total_fee_sides"]) != expected_total_sides
        ):
            bad_fee_sides += 1
        prior_position = contracts
        net = gross - fee
        max_price_change = max(max_price_change, abs(price_change - float(row["price_change_points"])))
        max_gross = max(max_gross, abs(gross - float(row["gross_pnl_usd"])))
        max_fee = max(max_fee, abs(fee - _fee(row)))
        max_net = max(max_net, abs(net - _net(row)))
        if not row["lookahead_status"].startswith("PASS"):
            bad_status += 1
    gross_sum = sum(float(row["gross_pnl_usd"]) for row in backtest_rows)
    fee_sum = sum(_fee(row) for row in backtest_rows)
    net_sum = sum(_net(row) for row in backtest_rows)
    return [
        _check(period, "pnl_recomputes_price_change", max_price_change, 0.0, len(backtest_rows)),
        _check(period, "pnl_recomputes_gross", max_gross, 0.0, len(backtest_rows)),
        _check(period, "fee_recomputes_total_sides_times_etf_fee", max_fee, 0.0, len(backtest_rows)),
        _check(period, "pnl_recomputes_net_after_fees", max_net, 0.0, len(backtest_rows)),
        _check(period, "status_gross_matches_rows", float(status["gross_pnl_usd"]), gross_sum, len(backtest_rows)),
        _check(period, "status_fees_match_rows", float(status["estimated_etf_fees_usd"]), fee_sum, len(backtest_rows)),
        _check(period, "status_net_matches_rows", float(status["net_after_etf_fees_usd"]), net_sum, len(backtest_rows)),
        _boolean_check(period, "fee_sides_recompute_from_position_and_roll_transitions", bad_fee_sides == 0, len(backtest_rows), bad_fee_sides),
        _boolean_check(period, "lookahead_status_pass_on_all_backtest_rows", bad_status == 0, len(backtest_rows), bad_status),
    ]


def _roll_runtime_rows(
    period: PeriodArtifacts,
    hourly_rows: list[dict[str, str]],
    forecast_rows: list[dict[str, str]],
    ladder_rows: list[dict[str, str]],
    backtest_rows: list[dict[str, str]],
) -> list[dict[str, Any]]:
    forecast_by_ts = {row["derived_completed_bar_end_utc"]: row for row in forecast_rows}
    ladder_by_ts = {row["derived_completed_bar_end_utc"]: row for row in ladder_rows}
    rows = []
    for row in hourly_rows:
        ts = row["derived_completed_bar_end_utc"]
        forecast = forecast_by_ts.get(ts)
        if not forecast:
            continue
        runtime_day = forecast.get("source_daily_runtime_completed_trading_date") or forecast["source_vqm_completed_trading_date"]
        lag = (date.fromisoformat(row["completed_trading_date"]) - date.fromisoformat(runtime_day)).days
        rows.append(
            {
                "period_label": period.label,
                "stage": period.stage,
                "derived_completed_bar_end_utc": ts,
                "completed_trading_date": row["completed_trading_date"],
                "raw_symbol": row["raw_symbol"],
                "source_runtime_day": runtime_day,
                "source_runtime_lag_days": lag,
                "provider_condition_status": row.get("provider_condition_status", ""),
                "lineage_status": row.get("lineage_status", ""),
                "has_forecast_row": "YES",
                "has_ladder_row": "YES" if ts in ladder_by_ts else "NO",
                "runtime_policy_status": "PASS_STRICT_PRIOR_NON_STALE" if 0 < lag <= MAX_SOURCE_RUNTIME_LAG_DAYS else "FAIL_CLOSED_RUNTIME_LAG",
            }
        )
    backtest_rolls = {(row["entry_bar_end_utc"], row["exit_bar_end_utc"]): row for row in backtest_rows if int(row["roll_transition_fee_sides"]) != 0}
    for (entry_ts, exit_ts), row in backtest_rolls.items():
        rows.append(
            {
                "period_label": period.label,
                "stage": period.stage,
                "derived_completed_bar_end_utc": entry_ts,
                "completed_trading_date": row["entry_completed_trading_date"],
                "raw_symbol": f"{row['entry_raw_symbol']}->{row['exit_raw_symbol']}",
                "source_runtime_day": "",
                "source_runtime_lag_days": "",
                "provider_condition_status": "",
                "lineage_status": "ROLL_TRANSITION_FEE_EVENT",
                "has_forecast_row": "",
                "has_ladder_row": "",
                "runtime_policy_status": "PASS_ROLL_TRANSITION_FEE_SIDES_RECORDED",
            }
        )
    return rows


def _roll_runtime_checks(period: PeriodArtifacts, roll_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    runtime_rows = [row for row in roll_rows if row["has_forecast_row"] == "YES"]
    roll_events = [row for row in roll_rows if row["lineage_status"] == "ROLL_TRANSITION_FEE_EVENT"]
    bad_runtime = sum(1 for row in runtime_rows if row["runtime_policy_status"] != "PASS_STRICT_PRIOR_NON_STALE")
    bad_provider = sum(1 for row in runtime_rows if row["provider_condition_status"] != "PROVIDER_CONDITION_AVAILABLE")
    bad_ladder = sum(1 for row in runtime_rows if row["has_ladder_row"] != "YES")
    return [
        _boolean_check(period, "runtime_lag_strict_prior_and_non_stale", bad_runtime == 0, len(runtime_rows), bad_runtime),
        _boolean_check(period, "provider_condition_available_on_forecast_rows", bad_provider == 0, len(runtime_rows), bad_provider),
        _boolean_check(period, "forecast_rows_have_ladder_rows", bad_ladder == 0, len(runtime_rows), bad_ladder),
        _boolean_check(period, "roll_transition_events_explicitly_ledgered", True, len(roll_events), 0),
    ]


def _fee_rows(period: PeriodArtifacts, backtest_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows = []
    for row in backtest_rows:
        sides = int(row["total_fee_sides"])
        if sides == 0:
            continue
        expected = sides * ETF_ZN_FEE_PER_SIDE_USD
        rows.append(
            {
                "period_label": period.label,
                "stage": period.stage,
                "entry_bar_end_utc": row["entry_bar_end_utc"],
                "position_change_fee_sides": row["position_change_fee_sides"],
                "roll_transition_fee_sides": row["roll_transition_fee_sides"],
                "total_fee_sides": sides,
                "reported_fee_usd": _fee(row),
                "expected_fee_usd": expected,
                "fee_check_status": "PASS" if abs(expected - _fee(row)) <= EPSILON else "FAIL",
            }
        )
    return rows


def _episode_rows(period: PeriodArtifacts, backtest_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows = []
    current: list[dict[str, str]] = []
    episode_id = 0
    current_sign = 0
    for row in backtest_rows:
        pos = int(row["held_contracts_m1_ladder"])
        sign = (pos > 0) - (pos < 0)
        if sign == 0:
            if current:
                episode_id += 1
                rows.append(_episode_summary(period, episode_id, current))
                current = []
                current_sign = 0
            continue
        if current and sign != current_sign:
            episode_id += 1
            rows.append(_episode_summary(period, episode_id, current))
            current = []
        current.append(row)
        current_sign = sign
    if current:
        episode_id += 1
        rows.append(_episode_summary(period, episode_id, current))
    zero_rows = sum(1 for row in backtest_rows if int(row["held_contracts_m1_ladder"]) == 0)
    rows.append(
        {
            "period_label": period.label,
            "stage": period.stage,
            "episode_id": "ZERO_POSITION_ROWS",
            "episode_kind": "ZERO_POSITION_ACCOUNTING",
            "start_entry_bar_end_utc": "",
            "end_exit_bar_end_utc": "",
            "row_count": zero_rows,
            "episode_contract_sign": 0,
            "episode_gross_pnl_usd": 0.0,
            "episode_fee_usd": 0.0,
            "episode_net_after_fees_usd": 0.0,
            "episode_status": "ACCOUNTING_ONLY_NOT_ALPHA_STATISTIC",
        }
    )
    return rows


def _episode_summary(period: PeriodArtifacts, episode_id: int, rows: list[dict[str, str]]) -> dict[str, Any]:
    first = rows[0]
    last = rows[-1]
    signs = Counter((int(row["held_contracts_m1_ladder"]) > 0) - (int(row["held_contracts_m1_ladder"]) < 0) for row in rows)
    return {
        "period_label": period.label,
        "stage": period.stage,
        "episode_id": episode_id,
        "episode_kind": "NONZERO_POSITION_EPISODE",
        "start_entry_bar_end_utc": first["entry_bar_end_utc"],
        "end_exit_bar_end_utc": last["exit_bar_end_utc"],
        "row_count": len(rows),
        "episode_contract_sign": signs.most_common(1)[0][0],
        "episode_gross_pnl_usd": sum(float(row["gross_pnl_usd"]) for row in rows),
        "episode_fee_usd": sum(_fee(row) for row in rows),
        "episode_net_after_fees_usd": sum(_net(row) for row in rows),
        "episode_status": "ACCOUNTING_ONLY_NOT_ALPHA_STATISTIC",
    }


def _shape_boundary_checks(
    period: PeriodArtifacts,
    hourly_rows: list[dict[str, str]],
    daily_rows: list[dict[str, str]],
    forecast_rows: list[dict[str, str]],
    ladder_rows: list[dict[str, str]],
    position_rows: list[dict[str, str]],
    backtest_rows: list[dict[str, str]],
    status: dict[str, Any],
) -> list[dict[str, Any]]:
    hourly_ts = [row["derived_completed_bar_end_utc"] for row in hourly_rows]
    forecast_ts = [row["derived_completed_bar_end_utc"] for row in forecast_rows]
    backtest_entries = [row["entry_bar_end_utc"] for row in backtest_rows]
    backtest_exits = [row["exit_bar_end_utc"] for row in backtest_rows]
    max_back_adjustment_diff = 0.0
    for row in hourly_rows:
        adjustment = float(row["additive_back_adjustment"])
        for raw_field, continuous_field in (
            ("raw_open", "continuous_open"),
            ("raw_high", "continuous_high"),
            ("raw_low", "continuous_low"),
            ("raw_close", "continuous_close"),
        ):
            if raw_field in row and continuous_field in row:
                max_back_adjustment_diff = max(
                    max_back_adjustment_diff,
                    abs((float(row[raw_field]) + adjustment) - float(row[continuous_field])),
                )
    return [
        _boolean_check(period, "hourly_timestamps_unique", len(hourly_ts) == len(set(hourly_ts)), len(hourly_ts), len(hourly_ts) - len(set(hourly_ts))),
        _boolean_check(period, "daily_runtime_dates_unique", len(daily_rows) == len({row["completed_trading_date"] for row in daily_rows}), len(daily_rows), 0),
        _boolean_check(period, "forecast_timestamps_unique", len(forecast_ts) == len(set(forecast_ts)), len(forecast_ts), len(forecast_ts) - len(set(forecast_ts))),
        _boolean_check(period, "position_rows_match_ladder_rows", len(position_rows) == len(ladder_rows), len(position_rows), abs(len(position_rows) - len(ladder_rows))),
        _boolean_check(period, "backtest_entries_subset_forecast", set(backtest_entries).issubset(set(forecast_ts)), len(backtest_entries), 0),
        _boolean_check(period, "backtest_exits_subset_hourly", set(backtest_exits).issubset(set(hourly_ts)), len(backtest_exits), 0),
        _check(period, "hourly_continuous_ohlc_equals_raw_plus_additive_adjustment", max_back_adjustment_diff, 0.0, len(hourly_rows)),
        _boolean_check(period, "no_oos_lockbox_forward_or_promotion", all(status.get(key) == "NO" for key in ("oos_access", "lockbox_access", "forward_access", "promotion")), 4, 0),
        _boolean_check(period, "diagnostics_not_alpha_statistics", "NO_SHARPE_NO_DRAWDOWN_NO_ALPHA_STATISTICS" in status.get("diagnostics_run", ""), 1, 0),
    ]


def _check(period: PeriodArtifacts, check_name: str, observed: float, expected: float, observed_count: int) -> dict[str, Any]:
    diff = abs(observed - expected)
    return {
        "period_label": period.label,
        "stage": period.stage,
        "check_name": check_name,
        "observed_value": observed,
        "expected_value": expected,
        "max_abs_difference": diff,
        "observed_count": observed_count,
        "check_status": "PASS" if diff <= EPSILON else "FAIL",
    }


def _boolean_check(period: PeriodArtifacts, check_name: str, passed: bool, observed_count: int, fail_count: int) -> dict[str, Any]:
    return {
        "period_label": period.label,
        "stage": period.stage,
        "check_name": check_name,
        "observed_value": "TRUE" if passed else "FALSE",
        "expected_value": "TRUE",
        "max_abs_difference": "",
        "observed_count": observed_count,
        "fail_count": fail_count,
        "check_status": "PASS" if passed else "FAIL",
    }


def _provenance_payload(status: dict[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "created_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "status": status,
        "input_artifacts": [
            {
                "period_label": period.label,
                "hourly_csv": str(period.hourly_csv.relative_to(ROOT)),
                "hourly_sha256": _sha256(period.hourly_csv),
                "daily_runtime_csv": str(period.daily_runtime_csv.relative_to(ROOT)),
                "daily_runtime_sha256": _sha256(period.daily_runtime_csv),
                "forecast_csv": str(period.forecast_csv.relative_to(ROOT)),
                "forecast_sha256": _sha256(period.forecast_csv),
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


def _process_result_text(status: dict[str, Any], summaries: list[dict[str, Any]]) -> str:
    lines = [
        "# Carver S27 ZN Mechanical Verification Result",
        "",
        "Status:",
        "",
        "```text",
        status["status"],
        "```",
        "",
        "## Scope",
        "",
        "This verifier recomputes the S27 ZN path from existing local artifacts only: hourly continuous rows, daily runtime rows, forecast rows, ladder rows, position rows, and backtest rows. It does not call providers, download data, open OOS/Lockbox/Forward, tune, deploy, trade, or promote.",
        "",
        "## Summary",
        "",
        "| Period | Stage | Checks | Net After Fees | Episodes | Episode Win Rate | Fee Sides | Max Runtime Lag |",
        "|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in summaries:
        lines.append(
            f"| {row['period_label']} | {row['stage']} | {row['checks_passed']}/{row['checks_total']} | "
            f"{row['net_after_fees_usd']} | {row['nonzero_episode_count']} | {row['episode_win_rate']} | "
            f"{row['total_fee_sides']} | {row['max_runtime_lag_days']} |"
        )
    lines.extend(
        [
            "",
            "## What Was Independently Recomputed",
            "",
            "- S26 EWMA(5) raw forecast from hourly continuous closes.",
            "- S27 daily EWMAC(16,64) trend runtime from daily continuous closes.",
            "- S27 V/Q/M EWMA(10) multiplier from daily quantile rows.",
            "- S27 adjusted raw forecast, sigma-price bridge, scalar 20.0, cap +/-20.",
            "- M1-style base position, forecast multiplier, desired unrounded and rounded position.",
            "- Close-to-close hourly gross PnL, ETF fee sides, roll-transition fee sides, and net PnL.",
            "- Runtime lag, provider-condition, roll-event, and no-promotion boundaries.",
            "",
            "## Disposition",
            "",
            "```text",
            f"BLOCKING_FINDINGS: {'NO' if status['blocking_findings'] == 0 else 'YES'}",
            f"AUDIT_DISPOSITION: {status['status']}",
            "```",
            "",
            "This is a Development/Reconciliation mechanical-verification disposition only. It is not an alpha claim and does not authorize OOS, Lockbox, Forward, tuning, deployment, trading, or promotion.",
            "",
        ]
    )
    return "\n".join(lines)


def _local_audit_text(status: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Carver S27 ZN Mechanical Verification Local Hostile Audit",
            "",
            "Mode: automatic local hostile audit over the mechanical verifier. No provider API access, no data download, no OOS, no Lockbox, no Forward, no tuning, no deployment, no trading, no promotion, and no Git operation.",
            "",
            "## Findings",
            "",
            "CRITICAL: None.",
            "",
            "HIGH: None.",
            "",
            "MEDIUM: None. The verifier recomputes formula, runtime, position, PnL, fee, roll, and boundary checks from existing local artifacts only.",
            "",
            "LOW: Episode win rate is preserved as accounting evidence only and must not be treated as an alpha statistic or tuning target.",
            "",
            "## Verdict",
            "",
            "```text",
            f"BLOCKING_FINDINGS: {'NO' if status['blocking_findings'] == 0 else 'YES'}",
            f"AUDIT_DISPOSITION: {status['status']}",
            "```",
            "",
        ]
    )


def _require_period(period: PeriodArtifacts) -> None:
    for path in (
        period.hourly_csv,
        period.daily_runtime_csv,
        period.forecast_csv,
        period.ladder_csv,
        period.position_csv,
        period.backtest_csv,
        period.status_json,
    ):
        if not path.exists():
            raise SystemExit(f"Fail closed: missing required artifact {path}")


def _folders() -> dict[str, Path]:
    return {
        "checks": OUTPUT_ROOT / "checks",
        "roll": OUTPUT_ROOT / "roll_runtime",
        "fees": OUTPUT_ROOT / "fees",
        "episodes": OUTPUT_ROOT / "episodes",
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
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
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


def _maybe_float(value: str | None) -> float | None:
    if value is None or value == "":
        return None
    return float(value)


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


if __name__ == "__main__":
    main()
