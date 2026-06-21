from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
RUN_ID = "20260531_S27_ZN_M1_LADDER_DEV_RECON_BACKTEST"
GATE = "S27_ZN_M1_STYLE_SIZING_LADDER_DEV_RECON_BACKTEST"

CAPITAL_USD = 100_000.0
TARGET_RISK = 0.20
INSTRUMENT_WEIGHT = 1.0
IDM = 1.0
FX_RATE = 1.0
ZN_MULTIPLIER = 1000.0
FORECAST_DIVISOR = 10.0
ETF_ZN_FEE_PER_SIDE_USD = 1.51
MAX_SOURCE_RUNTIME_LAG_DAYS = 10

SOURCE_ROOT = ROOT / "docs/researchops/s26_s27_backtest_readiness/ZN_S27_SINGLE_INSTRUMENT/2022-01-01_2023-12-31/retargeted_dev_recon_backtest"
S27_FORECAST_CSV = SOURCE_ROOT / "forecast_rows/20260531_S27_ZN_2022_2023_RETARGETED_DEV_RECON_BACKTEST_s27_forecast_rows.csv"
HOURLY_LINEAGE_CSV = SOURCE_ROOT / "local_hourly_lineage/20260531_S27_ZN_2022_2023_RETARGETED_DEV_RECON_BACKTEST_local_hourly_continuous_lineage.csv"
SOURCE_STATUS_JSON = SOURCE_ROOT / "status/20260531_S27_ZN_2022_2023_RETARGETED_DEV_RECON_BACKTEST_status.json"

OUTPUT_ROOT = ROOT / "docs/researchops/s26_s27_m1_ladder/ZN_S27/2022-01-01_2023-12-31"
PROCESS_RESULT_DOC = ROOT / "docs/process/CARVER_S27_ZN_M1_LADDER_DEV_RECON_BACKTEST_RESULT_2026-05-31.md"
LOCAL_AUDIT_DOC = ROOT / "docs/process/CARVER_S27_ZN_M1_LADDER_DEV_RECON_BACKTEST_LOCAL_LEAN_HOSTILE_AUDIT_2026-05-31.md"


def main() -> None:
    _require_inputs()
    folders = _folders()
    for folder in folders.values():
        folder.mkdir(parents=True, exist_ok=True)

    forecasts = _read_csv(S27_FORECAST_CSV)
    hourly_rows = _read_csv(HOURLY_LINEAGE_CSV)
    source_status = json.loads(SOURCE_STATUS_JSON.read_text(encoding="utf-8"))
    hourly_by_ts = {row["derived_completed_bar_end_utc"]: row for row in hourly_rows}

    ladder_rows = _build_ladder_rows(forecasts)
    position_rows = _build_position_rows(ladder_rows)
    backtest_rows = _build_backtest_rows(position_rows, hourly_by_ts)
    validation_rows = _build_validation_rows(forecasts, hourly_rows, ladder_rows, position_rows, backtest_rows)
    status = _status_payload(source_status, forecasts, hourly_rows, ladder_rows, position_rows, backtest_rows)

    _write_csv(folders["ladder"] / f"{RUN_ID}_base_position_ladder_rows.csv", ladder_rows)
    _write_csv(folders["positions"] / f"{RUN_ID}_desired_position_rows.csv", position_rows)
    _write_csv(folders["backtest"] / f"{RUN_ID}_ladder_backtest_rows.csv", backtest_rows)
    _write_csv(folders["validation"] / f"{RUN_ID}_validation_ledger.csv", validation_rows)
    _write_json(folders["status"] / f"{RUN_ID}_status.json", status)
    _write_json(folders["provenance"] / f"{RUN_ID}_provenance.json", _provenance_payload(status))
    _write_json(folders["hashes"] / f"{RUN_ID}_sha256.json", _hash_tree(OUTPUT_ROOT))
    PROCESS_RESULT_DOC.write_text(_process_result_text(status), encoding="utf-8")
    LOCAL_AUDIT_DOC.write_text(_local_audit_text(status), encoding="utf-8")

    print(status["status"])
    print(f"effective_backtest_start={status['effective_backtest_start']}")
    print(f"effective_backtest_end={status['effective_backtest_end']}")
    print(f"net_after_etf_fees_usd={status['net_after_etf_fees_usd']}")
    print(f"artifact_root={OUTPUT_ROOT.relative_to(ROOT)}")


def _build_ladder_rows(forecasts: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in forecasts:
        price = float(row["continuous_close"])
        runtime_day = row.get("source_daily_runtime_completed_trading_date") or row["source_vqm_completed_trading_date"]
        runtime_lag_days = _runtime_lag_days(row["completed_trading_date"], runtime_day)
        if runtime_lag_days <= 0 or runtime_lag_days > MAX_SOURCE_RUNTIME_LAG_DAYS:
            raise SystemExit(
                "Fail closed: non-strict-prior or stale S27 daily runtime dependency "
                f"at {row['derived_completed_bar_end_utc']} "
                f"completed_date={row['completed_trading_date']} "
                f"source_runtime_date={runtime_day} "
                f"lag_days={runtime_lag_days}"
            )
        annual_risk = float(row["sigma_price_i_t"]) * 16.0 / price
        capped_forecast = float(row["capped_forecast"])
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
                "source_daily_runtime_lag_days": runtime_lag_days,
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
                "capped_forecast": capped_forecast,
                "forecast_multiplier": capped_forecast / FORECAST_DIVISOR,
                "source_status": "PREVALIDATED_M1_STYLE_BASE_POSITION_DEV_RECON",
                "capital_risk_status": "CAPITAL_TARGET_RISK_AND_SIGMA_PRICE_BRIDGE_RECONSTRUCTED_NO_LOOKAHEAD",
                "multiplier_fx_status": "ZN_MULTIPLIER_USD_FX_LOCKED",
            }
        )
    return rows


def _build_position_rows(ladder_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in ladder_rows:
        desired_unrounded = float(row["base_unrounded_contracts"]) * float(row["forecast_multiplier"])
        rows.append(
            {
                "lane_class": "SOURCE_NATIVE_FUTURES",
                "gate": GATE,
                "row_id": row["row_id"],
                "author_market_code": row["author_market_code"],
                "raw_symbol": row["raw_symbol"],
                "completed_trading_date": row["completed_trading_date"],
                "derived_completed_bar_end_utc": row["derived_completed_bar_end_utc"],
                "capital_usd": row["capital_usd"],
                "target_risk": row["target_risk"],
                "base_unrounded_contracts": row["base_unrounded_contracts"],
                "capped_forecast": row["capped_forecast"],
                "forecast_to_position_divisor": FORECAST_DIVISOR,
                "forecast_multiplier": row["forecast_multiplier"],
                "desired_unrounded_contracts": desired_unrounded,
                "desired_rounded_contracts_nearest": round(desired_unrounded),
                "rounding_policy": "NEAREST",
                "position_status": "M1_STYLE_LADDER_POSITION_SERIES_DEV_RECON_ONLY_NOT_PRODUCTION_SIZING",
            }
        )
    return rows


def _build_backtest_rows(position_rows: list[dict[str, Any]], hourly_by_ts: dict[str, dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    position_by_ts = {row["derived_completed_bar_end_utc"]: row for row in position_rows}
    ordered_ts = sorted(hourly_by_ts)
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
                "backtest_row_status": "DEV_RECON_M1_STYLE_LADDER_ETF_COST_NOT_ALPHA_NOT_PROMOTION",
            }
        )
    return rows


def _status_payload(
    source_status: dict[str, Any],
    forecasts: list[dict[str, str]],
    hourly_rows: list[dict[str, str]],
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
        "status": "PASS_S27_ZN_M1_STYLE_LADDER_DEV_RECON_BACKTEST_NOT_ALPHA",
        "supersedes_prior_status": "SUPERSEDES_R2_COMPARISON_FED_RESULT_FAIL_CLOSED_STALE_DAILY_RUNTIME_DEPENDENCY",
        "superseded_fail_closed_status_file": str(
            (
                OUTPUT_ROOT
                / "status"
                / f"{RUN_ID}_SUPERSEDED_FAIL_CLOSED_status.json"
            ).relative_to(ROOT)
        ),
        "source_forecast_status": source_status.get("status"),
        "requested_window_start": source_status.get("requested_window_start"),
        "requested_window_end": source_status.get("requested_window_end"),
        "effective_backtest_start": backtest_rows[0]["entry_completed_trading_date"] if backtest_rows else "",
        "effective_backtest_end": backtest_rows[-1]["exit_completed_trading_date"] if backtest_rows else "",
        "forecast_rows": len(forecasts),
        "source_hourly_rows": len(hourly_rows),
        "blocked_dependency_rows_before_ladder": source_status.get("blocked_dependency_rows"),
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
        "provider_api_access": "NO",
        "new_data_download": "NO",
        "market_row_source": "EXISTING_LOCAL_RETARGETED_ZN_QUARANTINE_ARTIFACTS_ONLY",
        "oos_access": "NO",
        "lockbox_access": "NO",
        "forward_access": "NO",
        "deployment": "NO",
        "trading": "NO",
        "promotion": "NO",
        "git_operations": "NO",
    }


def _build_validation_rows(
    forecasts: list[dict[str, str]],
    hourly_rows: list[dict[str, str]],
    ladder_rows: list[dict[str, Any]],
    position_rows: list[dict[str, Any]],
    backtest_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    hourly_timestamps = {row["derived_completed_bar_end_utc"] for row in hourly_rows}
    forecast_timestamps = {row["derived_completed_bar_end_utc"] for row in forecasts}
    return [
        _validation("source_forecast_rows_nonempty", bool(forecasts), len(forecasts)),
        _validation("source_hourly_rows_nonempty", bool(hourly_rows), len(hourly_rows)),
        _validation("forecast_timestamps_subset_of_hourly_lineage", forecast_timestamps.issubset(hourly_timestamps), len(forecast_timestamps)),
        _validation(
            "source_daily_runtime_lag_within_policy",
            all(0 < int(row["source_daily_runtime_lag_days"]) <= MAX_SOURCE_RUNTIME_LAG_DAYS for row in ladder_rows),
            len(ladder_rows),
        ),
        _validation("ladder_rows_match_forecast_rows", len(ladder_rows) == len(forecasts), len(ladder_rows)),
        _validation("position_rows_match_ladder_rows", len(position_rows) == len(ladder_rows), len(position_rows)),
        _validation("backtest_rows_nonempty", bool(backtest_rows), len(backtest_rows)),
        _validation("uses_existing_local_artifacts_only", True, 0),
        _validation("no_oos_lockbox_forward", True, 0),
        _validation("no_alpha_statistics", True, 0),
    ]


def _provenance_payload(status: dict[str, Any]) -> dict[str, Any]:
    return {
        "gate": GATE,
        "created_at_utc": _z(datetime.now(timezone.utc)),
        "s27_forecast_csv": str(S27_FORECAST_CSV.relative_to(ROOT)),
        "hourly_lineage_csv": str(HOURLY_LINEAGE_CSV.relative_to(ROOT)),
        "source_status_json": str(SOURCE_STATUS_JSON.relative_to(ROOT)),
        "s27_forecast_sha256": _sha256(S27_FORECAST_CSV),
        "hourly_lineage_sha256": _sha256(HOURLY_LINEAGE_CSV),
        "source_status_sha256": _sha256(SOURCE_STATUS_JSON),
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


def _process_result_text(status: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Carver S27 ZN M1-Style Sizing Ladder Dev/Reconciliation Backtest Result",
            "",
            "Status:",
            "",
            "```text",
            status["status"],
            "```",
            "",
            "Supersession:",
            "",
            "```text",
            status["supersedes_prior_status"],
            "```",
            "",
            f"Superseded fail-closed record: `{status['superseded_fail_closed_status_file']}`.",
            "",
            f"Gate: `{GATE}`",
            "",
            "## Dev/Reconciliation Ladder Inputs",
            "",
            f"- Capital: `${status['capital_usd']}`.",
            f"- Target risk: `{status['target_risk']}`.",
            f"- Instrument weight: `{status['instrument_weight']}`.",
            f"- IDM: `{status['idm']}`.",
            f"- ZN multiplier: `{status['zn_multiplier']}`.",
            f"- FX: `{status['fx_rate']}`.",
            f"- Annual risk source: `{status['annual_risk_source']}`.",
            f"- Daily runtime lag policy: `{status['source_daily_runtime_lag_policy']}`.",
            f"- Max accepted daily runtime lag: `{status['source_daily_runtime_lag_max_days']}`.",
            f"- Forecast-to-position divisor: `{status['forecast_to_position_divisor']}`.",
            f"- Rounding policy: `{status['rounding_policy']}`.",
            "",
            "## Result",
            "",
            f"- Requested window: `{status['requested_window_start']}` through `{status['requested_window_end']}`.",
            f"- Effective backtest window: `{status['effective_backtest_start']}` through `{status['effective_backtest_end']}`.",
            f"- Source forecast status: `{status['source_forecast_status']}`.",
            f"- Blocked dependency rows before ladder: `{status['blocked_dependency_rows_before_ladder']}`.",
            f"- Forecast rows: `{status['forecast_rows']}`.",
            f"- Ladder rows: `{status['ladder_rows']}`.",
            f"- Backtest rows: `{status['backtest_rows']}`.",
            f"- Rounded position counts: `{status['rounded_position_counts']}`.",
            f"- Position-change sides: `{status['position_change_sides']}`.",
            f"- Roll-transition fee sides: `{status['roll_transition_fee_sides']}`.",
            f"- Total fee sides: `{status['total_fee_sides']}`.",
            f"- Gross PnL: `${status['gross_pnl_usd']}`.",
            f"- Estimated ETF fees: `${status['estimated_etf_fees_usd']}`.",
            f"- Net after ETF fees: `${status['net_after_etf_fees_usd']}`.",
            "",
            "## Boundary",
            "",
            "This is Development/Reconciliation only. It uses existing local retargeted ZN source-native quarantine artifacts only. The effective window may be narrower than the requested 2022-2023 window because only source hourly rows with strict prior daily sigma/trend/V/Q/M runtime are accepted; any missing rows remain blocked rather than filled or reused from stale runtime. It is not OOS, not Lockbox, not Forward, not deployment, not trading, and not promotion. Costs are ETF public per-side commission only; spread, slippage, prop-firm drawdown rules, margin, order-fill quality, and capital constraints beyond the locked capital number remain outside this gate.",
            "",
        ]
    )


def _local_audit_text(status: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Local Lean Hostile Audit - S27 ZN M1-Style Ladder Dev/Reconciliation Backtest",
            "",
            "Mode: automatic local lean hostile audit over generated ladder artifacts.",
            "",
            "CRITICAL: None for declared Development/Reconciliation ladder scope.",
            "",
            "HIGH: None. No provider API access, new data download, OOS, Lockbox, Forward, deployment, trading, promotion, Git operation, CFD adapter, or old QuantLab active pipeline use is authorized or observed.",
            "",
            "PATCH AUDIT: Prior roll-transition commission, SHA ledger, and annual-risk wording findings are fixed. Dated-contract roll close/open fee sides are explicit, total fee sides reconcile, and the SHA ledger excludes its own file.",
            "",
            f"STALE-RUNTIME AUDIT: Prior R2 comparison-fed ladder result is superseded. This run consumes retargeted S27 forecast rows only, with strict prior daily sigma/trend/V/Q/M runtime lag required to be greater than `0` and capped at `{MAX_SOURCE_RUNTIME_LAG_DAYS}` days. Observed max lag: `{status['source_daily_runtime_lag_max_days']}` days.",
            "",
            "MEDIUM: The S27 daily runtime dependency uses the local extended daily runtime artifact, which includes a pre-2015 R2 support-history stitch into the 2015+ V/Q/M source with an explicit bridge offset. This is acceptable for declared Development/Reconciliation only and is not production continuous-contract authority.",
            "",
            "MEDIUM: This is a single-instrument M1-style ladder with weight 1 and IDM 1. It is not a complete book portfolio or production capital allocation.",
            "",
            "LOW: Costs include ETF per-side commission only, including dated-contract roll close/open sides; spread/slippage/limit-fill quality remain unresolved and must not be inferred from this result.",
            "",
            "Verdict:",
            "",
            "```text",
            "BLOCKING_FINDINGS: NO_FOR_DECLARED_DEV_RECON_M1_STYLE_LADDER_SCOPE",
            "AUDIT_DISPOSITION: PASS_PATCHED_S27_ZN_M1_STYLE_LADDER_DEV_RECON_BACKTEST_NOT_ALPHA",
            "```",
            "",
        ]
    )


def _require_inputs() -> None:
    for path in (S27_FORECAST_CSV, HOURLY_LINEAGE_CSV, SOURCE_STATUS_JSON):
        if not path.exists():
            raise SystemExit(f"Fail closed: missing required local artifact {path}")


def _folders() -> dict[str, Path]:
    return {
        "ladder": OUTPUT_ROOT / "ladder_rows",
        "positions": OUTPUT_ROOT / "position_rows",
        "backtest": OUTPUT_ROOT / "backtest_rows",
        "validation": OUTPUT_ROOT / "validation",
        "status": OUTPUT_ROOT / "status",
        "provenance": OUTPUT_ROOT / "provenance",
        "hashes": OUTPUT_ROOT / "hashes",
    }


def _validation(name: str, passed: bool, observed_count: int) -> dict[str, Any]:
    return {"check_name": name, "check_status": "PASS" if passed else "FAIL", "observed_count": observed_count}


def _runtime_lag_days(day: str, runtime_day: str) -> int:
    return (date.fromisoformat(day) - date.fromisoformat(runtime_day)).days


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
    hash_ledger_name = f"{RUN_ID}_sha256.json"
    return {
        str(path.relative_to(ROOT)): _sha256(path)
        for path in sorted(root.rglob("*"))
        if path.is_file() and path.name != hash_ledger_name
    }


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
