from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import sys
from collections import defaultdict
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import databento as db

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.carver.spine.s26_s27 import (
    S26_ZN_WORKED_EXAMPLE_AUTHOR_MARKET_CODE,
    S26_ZN_WORKED_EXAMPLE_DATABENTO_INSTRUMENT_ID,
    S26_ZN_WORKED_EXAMPLE_DATABENTO_RAW_SYMBOL,
    S26_ZN_WORKED_EXAMPLE_ROW_ID,
    S27_VOL_ATTENUATION_RUNTIME_STATUS,
)


RUN_ID = "20260531_ZN_S27_V_Q_M_TEN_YEAR_VOL_RUNTIME"
GATE = "S27_ZN_V_Q_M_TEN_YEAR_VOL_HISTORY_DATABENTO_EXECUTION_OR_FAIL_CLOSED_DECISION"
DATASET = "GLBX.MDP3"
SCHEMA = "ohlcv-1d"
ROOT_SYMBOL = "ZN"
OUTPUT_ROOT = (
    ROOT
    / "docs/researchops/s26_s27_hourly_bridge/ZN_S27_V_Q_M_VOL_ATTENUATION/"
    / "ten_year_vol_history_runtime_2026-05-31"
)
S26_FORECAST_CSV = (
    ROOT
    / "docs/researchops/s26_s27_hourly_bridge/ZN_S26_WORKED_EXAMPLE/2026-04-13_2026-05-22/"
    / "forecast_series_only_output/2026-05-31/forecast_rows/"
    / "20260531_G_R1E_ZN_S26_EXTENDED_SIGMA_AND_FORECAST_SERIES_forecast_series_only.csv"
)
KEY_CANDIDATES = (
    Path(os.environ["DATABENTO_API_KEY_FILE"]) if os.environ.get("DATABENTO_API_KEY_FILE") else None,
    Path("C:/Users/openclaw/Desktop/BentoKey.txt"),
    Path("C:/Users/openclaw/Desktop/BENTO.txt"),
    Path("C:/Users/openclaw/Desktop/bento.txt"),
)
MONTH_CODES = ((3, "H"), (6, "M"), (9, "U"), (12, "Z"))
REQUEST_START = date(2014, 1, 1)
REQUEST_END = date(2026, 5, 23)
RISK_HISTORY_START = date(2015, 1, 1)
ROLL_BUFFER_COMPLETED_DATES = 10
SIGMA_EWMA_SPAN = 32
SIGMA_WINDOW_ROWS = 34
TRADING_DAYS_PER_YEAR = 256
TEN_YEAR_SIGMA_ROWS = 2560
VQM_EWMA_SPAN = 10


def main() -> None:
    folders = _folders()
    for folder in folders.values():
        folder.mkdir(parents=True, exist_ok=True)

    key = _read_databento_key()
    client = db.Historical(key)
    contracts = _contract_specs()
    forecast_rows = _read_s26_forecast_rows()

    _write_json(
        folders["manifest"] / f"{RUN_ID}_request_manifest.json",
        {
            "gate": GATE,
            "provider": "DATABENTO_HISTORICAL",
            "dataset": DATASET,
            "schema": SCHEMA,
            "stype_in": "raw_symbol",
            "root_symbol": ROOT_SYMBOL,
            "request_start": REQUEST_START.isoformat(),
            "request_end_exclusive": REQUEST_END.isoformat(),
            "contract_count": len(contracts),
            "contracts": contracts,
            "s26_forecast_csv": str(S26_FORECAST_CSV.relative_to(ROOT)),
            "non_authorization": [
                "NO_DIAGNOSTICS",
                "NO_BACKTESTS",
                "NO_RETURNS_PNL_STATISTICS",
                "NO_POSITIONS",
                "NO_COSTS",
                "NO_CARRY",
                "NO_STRATEGY_TEST",
                "NO_OOS",
                "NO_LOCKBOX",
                "NO_FORWARD",
                "NO_DEPLOYMENT",
                "NO_TRADING",
                "NO_PROMOTION",
                "NO_GIT_OPERATIONS",
            ],
        },
    )

    condition = client.metadata.get_dataset_condition(
        dataset=DATASET,
        start_date=REQUEST_START.isoformat(),
        end_date=REQUEST_END.isoformat(),
    )
    condition_by_date = {
        str(row["date"]): str(row["condition"]).upper()
        for row in condition
        if row.get("date") and row.get("condition")
    }
    _write_json(folders["metadata"] / f"{RUN_ID}_dataset_condition.json", condition)

    all_contract_rows: dict[str, list[dict[str, Any]]] = {}
    symbology_rows: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []
    for contract in contracts:
        symbol = contract["raw_symbol"]
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
            _write_json(folders["metadata"] / f"{RUN_ID}_symbology_{symbol}_{contract['contract_year']}.json", resolution)
            resolved = resolution.get("result", {}).get(symbol, [])
            if not resolved:
                errors.append({"symbol": symbol, "contract_year": contract["contract_year"], "error": "SYMBOL_NOT_RESOLVED"})
                continue
            symbology_rows.extend(
                {
                    "raw_symbol": symbol,
                    "contract_year": contract["contract_year"],
                    "delivery_month": contract["delivery_month"],
                    "request_start": start,
                    "request_end": end,
                    "resolved_d0": item.get("d0"),
                    "resolved_d1": item.get("d1"),
                    "instrument_id": item.get("s"),
                }
                for item in resolved
            )
            raw_dbn = folders["raw"] / f"{RUN_ID}_{symbol}_{contract['contract_year']}.dbn"
            provider_csv = folders["raw"] / f"{RUN_ID}_{symbol}_{contract['contract_year']}_provider.csv"
            store = client.timeseries.get_range(
                dataset=DATASET,
                schema=SCHEMA,
                symbols=[symbol],
                stype_in="raw_symbol",
                start=f"{start}T00:00:00Z",
                end=f"{end}T00:00:00Z",
                path=raw_dbn,
            )
            df = store.to_df()
            df.to_csv(provider_csv)
            all_contract_rows[_contract_key(contract)] = _read_provider_daily_rows(provider_csv, contract, condition_by_date)
        except Exception as exc:  # noqa: BLE001 - preserve provider failure as data evidence.
            errors.append(
                {
                    "symbol": symbol,
                    "contract_year": contract["contract_year"],
                    "request_start": start,
                    "request_end": end,
                    "error": type(exc).__name__,
                    "message": str(exc),
                }
            )

    _write_csv(folders["ledger"] / f"{RUN_ID}_symbology_resolution_ledger.csv", symbology_rows)
    if errors:
        _write_csv(folders["status"] / f"{RUN_ID}_provider_errors.csv", errors)

    status: dict[str, Any]
    runtime_rows: list[dict[str, Any]] = []
    try:
        if errors:
            raise RuntimeError(f"{len(errors)} contract provider requests failed")
        continuous = _build_continuous_series(contracts, all_contract_rows)
        _write_csv(folders["ledger"] / f"{RUN_ID}_local_continuous_daily_risk_history.csv", continuous)
        sigma_rows = _build_sigma_rows(continuous)
        _write_csv(folders["ledger"] / f"{RUN_ID}_sigma_i_t_ledger.csv", sigma_rows)
        relative_rows = _build_relative_vol_rows(sigma_rows)
        _write_csv(folders["ledger"] / f"{RUN_ID}_relative_vol_v_q_m_daily_ledger.csv", relative_rows)
        runtime_rows = _build_runtime_rows(forecast_rows, relative_rows)
        _write_csv(folders["runtime"] / f"{RUN_ID}_runtime_rows.csv", runtime_rows)
        status = {
            "gate": GATE,
            "status": "PASS_S27_ZN_V_Q_M_TEN_YEAR_VOL_RUNTIME_LEDGER_DEV_RECON_ONLY",
            "contract_requests": len(contracts),
            "continuous_rows": len(continuous),
            "sigma_rows": len(sigma_rows),
            "relative_vol_rows": len(relative_rows),
            "s26_forecast_rows": len(forecast_rows),
            "runtime_rows": len(runtime_rows),
            "first_runtime_as_of": runtime_rows[0]["as_of"] if runtime_rows else None,
            "last_runtime_as_of": runtime_rows[-1]["as_of"] if runtime_rows else None,
            "diagnostics_run": "NO",
            "backtests_run": "NO",
            "positions_run": "NO",
            "s27_forecast_run": "NO",
            "strategy_test_run": "NO",
        }
    except Exception as exc:  # noqa: BLE001 - fail closed with provenance.
        status = {
            "gate": GATE,
            "status": "FAIL_CLOSED_S27_ZN_V_Q_M_TEN_YEAR_VOL_RUNTIME_NOT_EMITTED",
            "reason": type(exc).__name__,
            "message": str(exc),
            "contract_requests": len(contracts),
            "provider_error_count": len(errors),
            "s26_forecast_rows": len(forecast_rows),
            "runtime_rows": 0,
            "diagnostics_run": "NO",
            "backtests_run": "NO",
            "positions_run": "NO",
            "s27_forecast_run": "NO",
            "strategy_test_run": "NO",
        }

    status_path = folders["status"] / f"{RUN_ID}_status.json"
    provenance_path = folders["provenance"] / f"{RUN_ID}_provenance.md"
    _write_json(status_path, status)
    provenance_path.write_text(_provenance_text(status), encoding="utf-8")
    _write_hashes(folders["hashes"] / f"{RUN_ID}_sha256.json")

    print(status["status"])
    if runtime_rows:
        print(f"runtime_rows={len(runtime_rows)}")
    print(f"artifact_root={OUTPUT_ROOT.relative_to(ROOT)}")


def _folders() -> dict[str, Path]:
    return {
        "manifest": OUTPUT_ROOT / "request_manifest",
        "metadata": OUTPUT_ROOT / "raw_provider_metadata",
        "raw": OUTPUT_ROOT / "raw_provider_output",
        "ledger": OUTPUT_ROOT / "ledger",
        "runtime": OUTPUT_ROOT / "runtime_rows",
        "status": OUTPUT_ROOT / "status",
        "provenance": OUTPUT_ROOT / "provenance",
        "hashes": OUTPUT_ROOT / "hashes",
    }


def _contract_specs() -> list[dict[str, Any]]:
    contracts: list[dict[str, Any]] = []
    for year in range(2015, 2027):
        for month, code in MONTH_CODES:
            delivery = date(year, month, 1)
            if delivery < date(2015, 3, 1) or delivery > date(2026, 6, 1):
                continue
            request_start = max(REQUEST_START, delivery - timedelta(days=460))
            request_end = min(REQUEST_END, _month_end(year, month) + timedelta(days=35))
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


def _read_provider_daily_rows(
    provider_csv: Path,
    contract: dict[str, Any],
    condition_by_date: dict[str, str],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with provider_csv.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            ts = _parse_ts(row["ts_event"])
            completed_date = ts.date().isoformat()
            if completed_date < RISK_HISTORY_START.isoformat() or completed_date >= REQUEST_END.isoformat():
                continue
            condition = condition_by_date.get(completed_date, "UNKNOWN")
            if condition != "AVAILABLE":
                continue
            close = float(row["close"])
            if not math.isfinite(close) or close <= 0.0:
                continue
            rows.append(
                {
                    "raw_symbol": contract["raw_symbol"],
                    "contract_year": contract["contract_year"],
                    "delivery_month": contract["delivery_month"],
                    "delivery_code": contract["delivery_code"],
                    "completed_trading_date": completed_date,
                    "close": close,
                    "instrument_id": row.get("instrument_id", ""),
                    "provider_condition": condition,
                    "source_csv_sha256": _sha256(provider_csv),
                }
            )
    return rows


def _build_continuous_series(
    contracts: list[dict[str, Any]],
    all_contract_rows: dict[str, list[dict[str, Any]]],
) -> list[dict[str, Any]]:
    by_contract_date: dict[str, dict[str, dict[str, Any]]] = {
        _contract_key(contract): {row["completed_trading_date"]: row for row in all_contract_rows[_contract_key(contract)]}
        for contract in contracts
    }
    all_dates = sorted({date_ for rows in by_contract_date.values() for date_ in rows})
    if not all_dates:
        raise RuntimeError("no provider-condition-available daily rows")

    roll_rows: list[dict[str, Any]] = []
    for old, new in zip(contracts[:-1], contracts[1:], strict=True):
        first_notice = _first_notice_proxy(old, all_dates)
        prior_dates = [day for day in all_dates if day < first_notice.isoformat()]
        if len(prior_dates) <= ROLL_BUFFER_COMPLETED_DATES:
            raise RuntimeError(f"insufficient roll-buffer dates before first-notice proxy for {_contract_key(old)}")
        transition = prior_dates[-ROLL_BUFFER_COMPLETED_DATES]
        old_row = by_contract_date[_contract_key(old)].get(transition)
        new_row = by_contract_date[_contract_key(new)].get(transition)
        if old_row is None or new_row is None:
            raise RuntimeError(f"missing old/new overlap on roll transition {transition} for {_contract_key(old)}->{_contract_key(new)}")
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
        if current_index >= len(contracts):
            current_index = len(contracts) - 1
        contract = contracts[current_index]
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
        rows.append(
            {
                "completed_trading_date": day,
                "active_contract_key": _contract_key(contracts[segment_index]),
                "raw_symbol": active["raw_symbol"],
                "instrument_id": active["instrument_id"],
                "raw_close": active["close"],
                "additive_back_adjustment": offsets_by_segment[segment_index],
                "continuous_close": active["close"] + offsets_by_segment[segment_index],
                "lineage_status": "DEV_RECON_LOCAL_BACK_ADJUSTED_DATED_CONTRACT_CHAIN",
            }
        )
    if len(rows) < TEN_YEAR_SIGMA_ROWS + SIGMA_WINDOW_ROWS + 30:
        raise RuntimeError("continuous risk-history rows are insufficient for ten-year V/Q/M")
    _write_csv(_folders()["ledger"] / f"{RUN_ID}_roll_plan.csv", roll_rows)
    return rows


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
        sigma = math.sqrt(variance) * math.sqrt(TRADING_DAYS_PER_YEAR)
        rows.append(
            {
                "completed_trading_date": dates[index],
                "sigma_i_t": sigma,
                "sigma_method": "STRATEGY_3_STYLE_EWMA32_PERCENT_RETURN_SIGMA_ANNUALIZED_256",
                "source_window_start": dates[index - SIGMA_WINDOW_ROWS + 1],
                "source_window_end": dates[index],
                "source_window_rows": SIGMA_WINDOW_ROWS,
                "no_lookahead_status": "PASS_NO_LOOKAHEAD_DAILY_RUNTIME",
            }
        )
    return rows


def _build_relative_vol_rows(sigma_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    raw_multiplier_history: list[float] = []
    smoothed: float | None = None
    alpha = 2.0 / (VQM_EWMA_SPAN + 1.0)
    for index, sigma_row in enumerate(sigma_rows):
        if index < TEN_YEAR_SIGMA_ROWS:
            continue
        prior = sigma_rows[index - TEN_YEAR_SIGMA_ROWS : index]
        ten_year_avg = sum(float(row["sigma_i_t"]) for row in prior) / TEN_YEAR_SIGMA_ROWS
        sigma = float(sigma_row["sigma_i_t"])
        v = sigma / ten_year_avg
        historical_v = [
            float(row["sigma_i_t"])
            / (
                sum(float(prior_row["sigma_i_t"]) for prior_row in sigma_rows[j - TEN_YEAR_SIGMA_ROWS : j])
                / TEN_YEAR_SIGMA_ROWS
            )
            for j, row in enumerate(sigma_rows[: index + 1])
            if j >= TEN_YEAR_SIGMA_ROWS
            for _ in (row,)
        ]
        q = _quantile_rank_including_current(historical_v, v)
        raw_multiplier = 2.0 - 1.5 * q
        raw_multiplier_history.append(raw_multiplier)
        smoothed = raw_multiplier if smoothed is None else alpha * raw_multiplier + (1.0 - alpha) * smoothed
        rows.append(
            {
                "completed_trading_date": sigma_row["completed_trading_date"],
                "sigma_i_t": sigma,
                "ten_year_average_sigma": ten_year_avg,
                "relative_volatility_v": v,
                "historical_v_observation_count": len(historical_v),
                "quantile_q": q,
                "raw_multiplier_2_minus_1_5q": raw_multiplier,
                "vol_multiplier_m_ewma10": smoothed,
                "method_status": "LOCKED_S13_STYLE_V_Q_M_ATTENUATION_RUNTIME",
                "no_lookahead_status": "PASS_NO_LOOKAHEAD_DAILY_RUNTIME",
            }
        )
    return rows


def _build_runtime_rows(forecast_rows: list[dict[str, str]], relative_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_date = {row["completed_trading_date"]: row for row in relative_rows}
    available_dates = sorted(by_date)
    runtime_rows: list[dict[str, Any]] = []
    source_sha = _sha256(_folders()["ledger"] / f"{RUN_ID}_relative_vol_v_q_m_daily_ledger.csv")
    for forecast in forecast_rows:
        completed_date = forecast["completed_trading_date"]
        candidates = [day for day in available_dates if day < completed_date]
        if not candidates:
            raise RuntimeError(f"no V/Q/M runtime row strictly before completed trading date {completed_date}")
        runtime = by_date[candidates[-1]]
        runtime_rows.append(
            {
                "row_id": S26_ZN_WORKED_EXAMPLE_ROW_ID,
                "author_market_code": S26_ZN_WORKED_EXAMPLE_AUTHOR_MARKET_CODE,
                "instrument_id": S26_ZN_WORKED_EXAMPLE_DATABENTO_INSTRUMENT_ID,
                "raw_symbol": S26_ZN_WORKED_EXAMPLE_DATABENTO_RAW_SYMBOL,
                "as_of": forecast["derived_completed_bar_end_utc"],
                "completed_trading_date": completed_date,
                "source_vqm_completed_trading_date": runtime["completed_trading_date"],
                "vol_multiplier": runtime["vol_multiplier_m_ewma10"],
                "quantile_q": runtime["quantile_q"],
                "relative_volatility_v": runtime["relative_volatility_v"],
                "runtime_status": S27_VOL_ATTENUATION_RUNTIME_STATUS,
                "method_status": "LOCKED_S13_STYLE_V_Q_M_ATTENUATION_RUNTIME",
                "no_lookahead_status": "PASS_NO_LOOKAHEAD",
                "source_artifact_sha256": source_sha,
            }
        )
    if len(runtime_rows) != len(forecast_rows):
        raise RuntimeError("V/Q/M runtime row count does not match S26 forecast row count")
    return runtime_rows


def _read_s26_forecast_rows() -> list[dict[str, str]]:
    with S26_FORECAST_CSV.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 686:
        raise RuntimeError("S26 forecast row count is not 686")
    return rows


def _first_notice_proxy(contract: dict[str, Any], all_dates: list[str]) -> date:
    first_of_delivery = date(int(contract["contract_year"]), int(contract["delivery_month"]), 1)
    first_delivery_trading_date = min(day for day in all_dates if day >= first_of_delivery.isoformat())
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


def _contract_key(contract: dict[str, Any]) -> str:
    return f"{contract['raw_symbol']}_{contract['contract_year']}"


def _month_end(year: int, month: int) -> date:
    if month == 12:
        return date(year, 12, 31)
    return date(year, month + 1, 1) - timedelta(days=1)


def _read_databento_key() -> str:
    for path in KEY_CANDIDATES:
        if path is None or not path.exists():
            continue
        key = path.read_text(encoding="utf-8").strip()
        if len(key) == 32 and key.startswith("db-"):
            return key
    env_key = os.environ.get("DATABENTO_API_KEY", "").strip()
    if len(env_key) == 32 and env_key.startswith("db-"):
        return env_key
    raise SystemExit("Fail closed: no valid-shaped Databento key found in env or approved local key files")


def _parse_ts(value: str) -> datetime:
    normalized = value.strip().replace(" ", "T").replace("+00:00", "Z")
    ts = datetime.fromisoformat(normalized.replace("Z", "+00:00"))
    if ts.tzinfo is None:
        raise RuntimeError("provider timestamp is not timezone-aware")
    return ts.astimezone(timezone.utc)


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
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


def _provenance_text(status: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Carver S27 ZN V/Q/M Ten-Year Vol Runtime Provenance",
            "",
            "Status:",
            "",
            "```text",
            str(status["status"]),
            "```",
            "",
            f"Gate: `{GATE}`",
            "",
            "Boundary:",
            "",
            "This artifact is a Development/Reconciliation runtime-dependency artifact only. It is not a strategy test and does not authorize diagnostics, backtests, positions, costs, carry, deployment, trading, promotion, OOS, Lockbox, Forward, Git, or remote repository operations.",
            "",
            "Source method:",
            "",
            "- Databento GLBX.MDP3 dated ZN daily `ohlcv-1d` contract rows only.",
            "- Local additive back-adjusted dated-contract chain.",
            "- Strategy-3-style EWMA(32) annualized percentage sigma.",
            "- Ten-year rolling average using 2560 prior daily sigma observations.",
            "- Historical quantile of relative volatility with no lookahead.",
            "- EWMA(10) smoothing of `2 - 1.5 * Q`.",
            "- Runtime rows align one-for-one to existing S26 hourly forecast rows and use only daily V/Q/M rows strictly before the S26 completed trading date.",
            "",
        ]
    )


if __name__ == "__main__":
    main()
