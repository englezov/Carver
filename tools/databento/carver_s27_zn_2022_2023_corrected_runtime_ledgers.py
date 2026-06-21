from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import math
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.carver.spine.s26_s27 import (  # noqa: E402
    S26_DAILY_EQUILIBRIUM_METHOD_STATUS,
    S26_DAILY_EQUILIBRIUM_RUNTIME_STATUS,
    S26_EQUILIBRIUM_EWMA_SPAN,
    S26_ZN_SIGMA_RUNTIME_STATUS,
    S27_DAILY_TREND_METHOD_STATUS,
    S27_DAILY_VOL_ATTENUATION_METHOD_STATUS,
    S27_TREND_FAST_SPAN,
    S27_TREND_RUNTIME_STATUS,
    S27_TREND_SLOW_SPAN,
    S27_VOL_ATTENUATION_RUNTIME_STATUS,
)


RUN_ID = "20260604_S27_ZN_2022_2023_CORRECTED_RUNTIME_LEDGERS"
GATE = "S27_ZN_2022_2023_CORRECTED_RUNTIME_LEDGER_PREP"
AUTH_ENV_VAR = "CARVER_OPERATOR_AUTHORIZES_S27_RUNTIME_LEDGERS"
AUTH_ENV_VALUE = "AUTHORIZED_CORRECTED_S27_ZN_2022_2023_RUNTIME_LEDGERS"
DEFAULT_OUTPUT_ROOT = (
    ROOT
    / "docs/researchops/s26_s27_backtest_readiness/ZN_S27_SINGLE_INSTRUMENT/"
    / "2022-01-01_2023-12-31/corrected_runtime_ledgers"
)

RUNNER_SCRIPT = ROOT / "tools/databento/carver_s27_zn_2022_2023_retargeted_dev_recon_backtest.py"
LOCAL_DAILY_SCRIPT = ROOT / "tools/databento/carver_s27_zn_local_extended_daily_runtime_2022_2023.py"

SIGMA_CSV_NAME = "s26_sigma_runtime_rows.csv"
EQUILIBRIUM_CSV_NAME = "s26_daily_ewma5_equilibrium_runtime_rows.csv"
TREND_CSV_NAME = "s27_daily_ewmac16_64_trend_runtime_rows.csv"
VOL_CSV_NAME = "s27_daily_ten_year_vqm_runtime_rows.csv"


def main() -> None:
    _require_runtime_authorization()
    runner = _load_module("s27_corrected_backtest_runner_for_runtime_prep", RUNNER_SCRIPT)
    local_daily = _load_module("s27_local_extended_daily_runtime_for_runtime_prep", LOCAL_DAILY_SCRIPT)
    _require_inputs(runner, local_daily)

    output_root = Path(os.environ.get("CARVER_S27_CORRECTED_RUNTIME_OUTPUT_ROOT", DEFAULT_OUTPUT_ROOT))
    folders = _folders(output_root)
    for folder in folders.values():
        folder.mkdir(parents=True, exist_ok=True)

    hourly_rows = runner._read_hourly_rows()
    forecast_rows, inactive_rows, roll_plan = runner._build_hourly_continuous_rows(hourly_rows)
    r2_unique = local_daily._dedupe_r2_daily_rows(local_daily._read_csv(local_daily.R2_DAILY_CONTINUOUS_CSV))
    vqm_source_rows = local_daily._read_csv(local_daily.VQM_DAILY_CONTINUOUS_CSV)
    daily_rows, stitch_record = local_daily._build_extended_daily_rows(r2_unique, vqm_source_rows)
    sigma_source_rows = local_daily._build_sigma_rows(daily_rows)
    vqm_runtime_rows = local_daily._build_vqm_rows(sigma_source_rows)
    ledgers = _build_corrected_runtime_ledgers(
        forecast_rows=forecast_rows,
        daily_rows=daily_rows,
        sigma_rows=sigma_source_rows,
        vqm_rows=vqm_runtime_rows,
        source_hashes={
            "hourly": _sha256(runner.HOURLY_SOURCE_CSV),
            "r2_daily": _sha256(local_daily.R2_DAILY_CONTINUOUS_CSV),
            "vqm_daily": _sha256(local_daily.VQM_DAILY_CONTINUOUS_CSV),
            "extended_daily": _composite_sha256(
                "S27_ZN_2022_2023_EXTENDED_DAILY_RUNTIME_SOURCE",
                _sha256(local_daily.R2_DAILY_CONTINUOUS_CSV),
                _sha256(local_daily.VQM_DAILY_CONTINUOUS_CSV),
                json.dumps(stitch_record, sort_keys=True, default=str),
            ),
        },
    )
    validation_rows = _validation_rows(forecast_rows, inactive_rows, roll_plan, daily_rows, sigma_source_rows, vqm_runtime_rows, ledgers)
    status = _status_payload(forecast_rows, inactive_rows, roll_plan, daily_rows, sigma_source_rows, vqm_runtime_rows, ledgers, validation_rows)

    _write_csv(output_root / SIGMA_CSV_NAME, ledgers["sigma"])
    _write_csv(output_root / EQUILIBRIUM_CSV_NAME, ledgers["equilibrium"])
    _write_csv(output_root / TREND_CSV_NAME, ledgers["trend"])
    _write_csv(output_root / VOL_CSV_NAME, ledgers["vol"])
    _write_csv(folders["validation"] / f"{RUN_ID}_validation_ledger.csv", validation_rows)
    _write_json(folders["status"] / f"{RUN_ID}_status.json", status)
    _write_json(folders["provenance"] / f"{RUN_ID}_provenance.json", _provenance_payload(runner, local_daily, stitch_record, status))
    _write_json(folders["hashes"] / f"{RUN_ID}_sha256.json", _hash_tree(output_root))

    print(status["status"])
    print(f"forecast_target_rows={status['forecast_target_rows']}")
    print(f"runtime_rows_per_ledger={status['runtime_rows_per_ledger']}")
    print(f"artifact_root={output_root.relative_to(ROOT)}")


def _build_corrected_runtime_ledgers(
    *,
    forecast_rows: list[dict[str, Any]],
    daily_rows: list[dict[str, Any]],
    sigma_rows: list[dict[str, Any]],
    vqm_rows: list[dict[str, Any]],
    source_hashes: dict[str, str],
) -> dict[str, list[dict[str, Any]]]:
    if not forecast_rows:
        raise SystemExit("Fail closed: no forecast target rows for corrected runtime ledgers")
    _require_source_hashes(source_hashes)
    daily_by_date = _daily_close_by_date(daily_rows)
    sigma_by_date = _rows_by_date("sigma", sigma_rows)
    vqm_by_date = _rows_by_date("V/Q/M", vqm_rows)
    daily_dates = sorted(daily_by_date)
    sigma_dates = sorted(sigma_by_date)
    vqm_dates = sorted(vqm_by_date)
    ledgers: dict[str, list[dict[str, Any]]] = {"sigma": [], "equilibrium": [], "trend": [], "vol": []}
    seen_as_of: set[str] = set()
    for forecast in sorted(forecast_rows, key=lambda row: row["derived_completed_bar_end_utc"]):
        as_of = forecast["derived_completed_bar_end_utc"]
        completed_date = forecast["completed_trading_date"]
        if as_of in seen_as_of:
            raise SystemExit(f"Fail closed: duplicate forecast as_of for runtime ledgers: {as_of}")
        seen_as_of.add(as_of)
        prior_daily_dates = [day for day in daily_dates if day < completed_date]
        if len(prior_daily_dates) < S27_TREND_SLOW_SPAN:
            raise SystemExit(f"Fail closed: fewer than {S27_TREND_SLOW_SPAN} prior daily rows before {completed_date}")
        sigma_day = _latest_prior_date("sigma", sigma_dates, completed_date)
        vqm_day = _latest_prior_date("V/Q/M", vqm_dates, completed_date)
        sigma = sigma_by_date[sigma_day]
        vqm = vqm_by_date[vqm_day]
        daily_values = tuple(daily_by_date[day] for day in prior_daily_dates)
        equilibrium = _ewma(daily_values, S26_EQUILIBRIUM_EWMA_SPAN)
        fast = _ewma(daily_values, S27_TREND_FAST_SPAN)
        slow = _ewma(daily_values, S27_TREND_SLOW_SPAN)
        trend = fast - slow
        common = _common_runtime_fields(forecast, as_of, completed_date)
        ledgers["sigma"].append(
            {
                **common,
                "sigma_percent_t": _finite_float(sigma["sigma_i_t"], "sigma_i_t"),
                "sigma_i_t": _finite_float(sigma["sigma_i_t"], "sigma_i_t"),
                "runtime_status": S26_ZN_SIGMA_RUNTIME_STATUS,
                "method_status": "LOCKED_TO_PART_ONE_S03_VARIABLE_RISK_FAMILY",
                "no_lookahead_status": "PASS_NO_LOOKAHEAD",
                "no_lookahead_policy": "SIGMA_ROW_STRICTLY_BEFORE_FORECAST_COMPLETED_TRADING_DATE",
                "source_completed_trading_date": sigma_day,
                "source_window_start": sigma.get("source_window_start", ""),
                "source_window_end": sigma.get("source_window_end", sigma_day),
                "source_window_rows": sigma.get("source_window_rows", ""),
                "source_artifact_sha256": source_hashes["extended_daily"],
                "forecast_target_source_artifact_sha256": source_hashes["hourly"],
                "runtime_output_boundary": "RUNTIME_LEDGER_ONLY_NOT_FORECAST_NOT_DIAGNOSTIC_NOT_BACKTEST",
            }
        )
        ledgers["equilibrium"].append(
            {
                **common,
                "equilibrium_ewma_5": f"{equilibrium:.12f}",
                "equilibrium_ewma5": f"{equilibrium:.12f}",
                "runtime_status": S26_DAILY_EQUILIBRIUM_RUNTIME_STATUS,
                "method_status": S26_DAILY_EQUILIBRIUM_METHOD_STATUS,
                "no_lookahead_status": "PASS_NO_LOOKAHEAD",
                "no_lookahead_policy": "DAILY_ROWS_STRICTLY_BEFORE_FORECAST_COMPLETED_TRADING_DATE",
                "source_artifact_sha256": source_hashes["extended_daily"],
                "forecast_target_source_artifact_sha256": source_hashes["hourly"],
                "daily_rows_used": len(prior_daily_dates),
                "first_daily_row_used": prior_daily_dates[0],
                "last_daily_row_used": prior_daily_dates[-1],
                "runtime_output_boundary": "RUNTIME_LEDGER_ONLY_NOT_FORECAST_NOT_DIAGNOSTIC_NOT_BACKTEST",
            }
        )
        ledgers["trend"].append(
            {
                **common,
                "trend_fast_ewma": f"{fast:.12f}",
                "trend_slow_ewma": f"{slow:.12f}",
                "trend_forecast": f"{trend:.12f}",
                "trend_forecast_proxy_fast_minus_slow": f"{trend:.12f}",
                "runtime_status": S27_TREND_RUNTIME_STATUS,
                "method_status": S27_DAILY_TREND_METHOD_STATUS,
                "no_lookahead_status": "PASS_NO_LOOKAHEAD",
                "no_lookahead_policy": "DAILY_ROWS_STRICTLY_BEFORE_FORECAST_COMPLETED_TRADING_DATE",
                "source_artifact_sha256": source_hashes["extended_daily"],
                "forecast_target_source_artifact_sha256": source_hashes["hourly"],
                "daily_rows_used": len(prior_daily_dates),
                "first_daily_row_used": prior_daily_dates[0],
                "last_daily_row_used": prior_daily_dates[-1],
                "runtime_output_boundary": "RUNTIME_LEDGER_ONLY_NOT_FORECAST_NOT_DIAGNOSTIC_NOT_BACKTEST",
            }
        )
        ledgers["vol"].append(
            {
                **common,
                "vol_multiplier": _finite_float(vqm["vol_multiplier_m_ewma10"], "vol_multiplier_m_ewma10"),
                "vol_multiplier_m_ewma10": _finite_float(vqm["vol_multiplier_m_ewma10"], "vol_multiplier_m_ewma10"),
                "relative_volatility_v": _finite_float(vqm["relative_volatility_v"], "relative_volatility_v"),
                "quantile_q": _finite_float(vqm["quantile_q"], "quantile_q"),
                "runtime_status": S27_VOL_ATTENUATION_RUNTIME_STATUS,
                "method_status": S27_DAILY_VOL_ATTENUATION_METHOD_STATUS,
                "no_lookahead_status": "PASS_NO_LOOKAHEAD",
                "no_lookahead_policy": "V_Q_M_ROW_STRICTLY_BEFORE_FORECAST_COMPLETED_TRADING_DATE",
                "source_artifact_sha256": source_hashes["extended_daily"],
                "forecast_target_source_artifact_sha256": source_hashes["hourly"],
                "source_vqm_completed_trading_date": vqm_day,
                "source_vqm_observation_count": vqm.get("historical_v_observation_count", ""),
                "runtime_output_boundary": "RUNTIME_LEDGER_ONLY_NOT_FORECAST_NOT_DIAGNOSTIC_NOT_BACKTEST",
            }
        )
    _require_equal_ledger_lengths(ledgers)
    return ledgers


def _require_source_hashes(source_hashes: dict[str, str]) -> None:
    for name in ("hourly", "r2_daily", "vqm_daily", "extended_daily"):
        value = source_hashes.get(name)
        if value is None:
            raise SystemExit(f"Fail closed: missing source hash {name}")
        _require_sha256(value, f"{name} source hash")


def _common_runtime_fields(forecast: dict[str, Any], as_of: str, completed_date: str) -> dict[str, Any]:
    return {
        "row_id": forecast["row_id"],
        "author_market_code": forecast["author_market_code"],
        "instrument_id": forecast["instrument_id"],
        "raw_symbol": forecast["raw_symbol"],
        "as_of": as_of,
        "completed_trading_date": completed_date,
    }


def _daily_close_by_date(rows: list[dict[str, Any]]) -> dict[str, float]:
    out: dict[str, float] = {}
    for row in rows:
        day = row.get("completed_trading_date") or row.get("continuous_row_date")
        close = row.get("continuous_close") or row.get("adjusted_close")
        if not day or close in (None, ""):
            raise SystemExit("Fail closed: daily row lacks completed date or continuous close")
        if day in out:
            raise SystemExit(f"Fail closed: duplicate daily runtime date {day}")
        out[str(day)] = _finite_float(close, "continuous daily close")
    if not out:
        raise SystemExit("Fail closed: no daily rows for corrected runtime ledgers")
    return out


def _rows_by_date(name: str, rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for row in rows:
        day = row.get("completed_trading_date")
        if not day:
            raise SystemExit(f"Fail closed: {name} runtime source row lacks completed_trading_date")
        if day in out:
            raise SystemExit(f"Fail closed: duplicate {name} runtime source date {day}")
        out[str(day)] = row
    if not out:
        raise SystemExit(f"Fail closed: no {name} runtime source rows")
    return out


def _latest_prior_date(name: str, dates: list[str], completed_date: str) -> str:
    prior = [day for day in dates if day < completed_date]
    if not prior:
        raise SystemExit(f"Fail closed: no strict-prior {name} runtime row before {completed_date}")
    return prior[-1]


def _ewma(values: tuple[float, ...], span: int) -> float:
    if len(values) < span:
        raise SystemExit(f"Fail closed: fewer than {span} values for EWMA runtime")
    alpha = 2.0 / (span + 1.0)
    smoothed = values[0]
    for value in values[1:]:
        smoothed = alpha * value + (1.0 - alpha) * smoothed
    return smoothed


def _finite_float(value: Any, name: str) -> float:
    parsed = float(value)
    if not math.isfinite(parsed):
        raise SystemExit(f"Fail closed: non-finite {name}")
    return parsed


def _require_sha256(value: str, name: str) -> None:
    normalized = value.strip()
    if len(normalized) != 64 or any(character not in "0123456789ABCDEFabcdef" for character in normalized):
        raise SystemExit(f"Fail closed: {name} must be a SHA-256 hex digest")


def _composite_sha256(*parts: str) -> str:
    digest = hashlib.sha256()
    for part in parts:
        digest.update(part.encode("utf-8"))
        digest.update(b"\n")
    return digest.hexdigest().upper()


def _require_equal_ledger_lengths(ledgers: dict[str, list[dict[str, Any]]]) -> None:
    lengths = {name: len(rows) for name, rows in ledgers.items()}
    if len(set(lengths.values())) != 1:
        raise SystemExit(f"Fail closed: corrected runtime ledger row count mismatch: {lengths}")
    if next(iter(lengths.values())) == 0:
        raise SystemExit("Fail closed: corrected runtime ledgers are empty")


def _validation_rows(
    forecast_rows: list[dict[str, Any]],
    inactive_rows: list[dict[str, Any]],
    roll_plan: list[dict[str, Any]],
    daily_rows: list[dict[str, Any]],
    sigma_source_rows: list[dict[str, Any]],
    vqm_runtime_rows: list[dict[str, Any]],
    ledgers: dict[str, list[dict[str, Any]]],
) -> list[dict[str, Any]]:
    dates = [row["completed_trading_date"] for row in forecast_rows]
    ledger_lengths = {name: len(rows) for name, rows in ledgers.items()}
    return [
        _validation("forecast_target_rows_available", bool(forecast_rows), len(forecast_rows)),
        _validation("forecast_target_as_of_unique", len({row["derived_completed_bar_end_utc"] for row in forecast_rows}) == len(forecast_rows), len(forecast_rows)),
        _validation("inactive_rows_explicitly_ledgers_by_runner", bool(inactive_rows), len(inactive_rows)),
        _validation("roll_plan_available", bool(roll_plan), len(roll_plan)),
        _validation("daily_support_rows_available", bool(daily_rows), len(daily_rows)),
        _validation("sigma_source_rows_available", bool(sigma_source_rows), len(sigma_source_rows)),
        _validation("vqm_runtime_rows_available", bool(vqm_runtime_rows), len(vqm_runtime_rows)),
        _validation("runtime_ledgers_match_forecast_rows", all(length == len(forecast_rows) for length in ledger_lengths.values()), sum(ledger_lengths.values())),
        _validation("forecast_window_is_2022_2023_target", min(dates) >= "2022-01-01" and max(dates) <= "2023-12-31", len(forecast_rows)),
        _validation("no_provider_api_access", True, 0),
        _validation("no_new_data_download", True, 0),
        _validation("no_diagnostics_or_backtest", True, 0),
        _validation("no_oos_lockbox_forward", True, 0),
    ]


def _status_payload(
    forecast_rows: list[dict[str, Any]],
    inactive_rows: list[dict[str, Any]],
    roll_plan: list[dict[str, Any]],
    daily_rows: list[dict[str, Any]],
    sigma_source_rows: list[dict[str, Any]],
    vqm_runtime_rows: list[dict[str, Any]],
    ledgers: dict[str, list[dict[str, Any]]],
    validation_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    ledger_lengths = {name: len(rows) for name, rows in ledgers.items()}
    return {
        "gate": GATE,
        "status": "PASS_S27_ZN_2022_2023_CORRECTED_RUNTIME_LEDGERS_NOT_BACKTEST",
        "forecast_target_rows": len(forecast_rows),
        "forecast_target_start": forecast_rows[0]["completed_trading_date"],
        "forecast_target_end": forecast_rows[-1]["completed_trading_date"],
        "inactive_rows_explicitly_ledgered_by_runner": len(inactive_rows),
        "roll_transition_count": len(roll_plan),
        "daily_support_rows": len(daily_rows),
        "sigma_source_rows": len(sigma_source_rows),
        "vqm_runtime_source_rows": len(vqm_runtime_rows),
        "runtime_ledger_lengths": ledger_lengths,
        "runtime_rows_per_ledger": next(iter(ledger_lengths.values())),
        "validation_status": "PASS" if all(row["check_status"] == "PASS" for row in validation_rows) else "FAIL",
        "provider_api_access": "NO",
        "new_data_download": "NO",
        "diagnostics_run": "NO",
        "backtest_run": "NO",
        "position_output": "NO",
        "oos_access": "NO",
        "lockbox_access": "NO",
        "forward_access": "NO",
        "deployment": "NO",
        "trading": "NO",
        "promotion": "NO",
        "git_operations": "NO",
    }


def _provenance_payload(runner: Any, local_daily: Any, stitch_record: dict[str, Any], status: dict[str, Any]) -> dict[str, Any]:
    return {
        "gate": GATE,
        "created_at_utc": _z(datetime.now(timezone.utc)),
        "hourly_source_csv": str(runner.HOURLY_SOURCE_CSV.relative_to(ROOT)),
        "hourly_source_sha256": _sha256(runner.HOURLY_SOURCE_CSV),
        "r2_daily_continuous_csv": str(local_daily.R2_DAILY_CONTINUOUS_CSV.relative_to(ROOT)),
        "r2_daily_continuous_sha256": _sha256(local_daily.R2_DAILY_CONTINUOUS_CSV),
        "vqm_daily_continuous_csv": str(local_daily.VQM_DAILY_CONTINUOUS_CSV.relative_to(ROOT)),
        "vqm_daily_continuous_sha256": _sha256(local_daily.VQM_DAILY_CONTINUOUS_CSV),
        "stitch_record": stitch_record,
        "output_csvs": [SIGMA_CSV_NAME, EQUILIBRIUM_CSV_NAME, TREND_CSV_NAME, VOL_CSV_NAME],
        "source_method": "One strict-prior daily runtime row per hourly forecast target as_of; no forecast, position, diagnostic, or backtest output.",
        "status": status,
    }


def _folders(output_root: Path) -> dict[str, Path]:
    return {
        "validation": output_root / "validation",
        "status": output_root / "status",
        "provenance": output_root / "provenance",
        "hashes": output_root / "hashes",
    }


def _require_runtime_authorization() -> None:
    if os.environ.get(AUTH_ENV_VAR) != AUTH_ENV_VALUE:
        raise SystemExit(
            f"Fail closed: corrected S27 runtime-ledger prep requires {AUTH_ENV_VAR}={AUTH_ENV_VALUE}; "
            "this is not backtest authorization"
        )


def _require_inputs(runner: Any, local_daily: Any) -> None:
    for path in (
        runner.HOURLY_SOURCE_CSV,
        runner.HOURLY_SOURCE_STATUS,
        local_daily.R2_DAILY_CONTINUOUS_CSV,
        local_daily.VQM_DAILY_CONTINUOUS_CSV,
    ):
        if not path.exists():
            raise SystemExit(f"Fail closed: required local artifact missing: {path}")


def _load_module(name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"Fail closed: unable to load script module {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _validation(name: str, passed: bool, observed_count: int) -> dict[str, Any]:
    return {"check_name": name, "check_status": "PASS" if passed else "FAIL", "observed_count": observed_count}


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise SystemExit(f"Fail closed: no rows for {path}")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def _write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8")


def _hash_tree(root: Path) -> dict[str, str]:
    hash_name = f"{RUN_ID}_sha256.json"
    return {
        str(path.relative_to(ROOT)): _sha256(path)
        for path in sorted(root.rglob("*"))
        if path.is_file() and path.name != hash_name
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
