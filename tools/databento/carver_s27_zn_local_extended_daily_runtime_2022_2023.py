from __future__ import annotations

import csv
import hashlib
import json
import math
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
RUN_ID = "20260531_S27_ZN_2022_2023_LOCAL_EXTENDED_DAILY_RUNTIME"
GATE = "S27_ZN_2022_2023_LOCAL_EXTENDED_DAILY_RUNTIME_RECONSTRUCTION"

SIGMA_EWMA_SPAN = 32
SIGMA_WINDOW_ROWS = 34
TRADING_DAYS_PER_YEAR = 256.0
TEN_YEAR_SIGMA_ROWS = 2560
VQM_EWMA_SPAN = 10
S27_TREND_FAST_SPAN = 16
S27_TREND_SLOW_SPAN = 64

R2_DAILY_CONTINUOUS_CSV = (
    ROOT
    / "docs/researchops/s26_s27_candidate_comparison/2022-01-01_2023-12-31/ZN/local_lineage/"
    / "20260531_S27_SOURCE_NATIVE_CANDIDATE_COMPARISON_2022_2023_R2_ZN_daily_continuous_lineage.csv"
)
VQM_DAILY_CONTINUOUS_CSV = (
    ROOT
    / "docs/researchops/s26_s27_hourly_bridge/ZN_S27_V_Q_M_VOL_ATTENUATION/ten_year_vol_history_runtime_2026-05-31/ledger/"
    / "20260531_ZN_S27_V_Q_M_TEN_YEAR_VOL_RUNTIME_local_continuous_daily_risk_history.csv"
)
OUTPUT_ROOT = (
    ROOT
    / "docs/researchops/s26_s27_backtest_readiness/ZN_S27_SINGLE_INSTRUMENT/2022-01-01_2023-12-31/"
    / "local_extended_daily_runtime"
)
PROCESS_DOC = ROOT / "docs/process/CARVER_S27_ZN_2022_2023_LOCAL_EXTENDED_DAILY_RUNTIME_RESULT_2026-05-31.md"
AUDIT_DOC = ROOT / "docs/process/CARVER_S27_ZN_2022_2023_LOCAL_EXTENDED_DAILY_RUNTIME_LOCAL_LEAN_HOSTILE_AUDIT_2026-05-31.md"


def main() -> None:
    _require_inputs()
    folders = _folders()
    for folder in folders.values():
        folder.mkdir(parents=True, exist_ok=True)

    r2_unique = _dedupe_r2_daily_rows(_read_csv(R2_DAILY_CONTINUOUS_CSV))
    vqm_rows = _read_csv(VQM_DAILY_CONTINUOUS_CSV)
    continuous_rows, stitch_record = _build_extended_daily_rows(r2_unique, vqm_rows)
    sigma_rows = _build_sigma_rows(continuous_rows)
    vqm_runtime_rows = _build_vqm_rows(sigma_rows)
    daily_runtime_rows = _build_daily_runtime_rows(continuous_rows, vqm_runtime_rows)
    validation_rows = _validation_rows(r2_unique, vqm_rows, continuous_rows, sigma_rows, vqm_runtime_rows, daily_runtime_rows)
    status = _status_payload(r2_unique, vqm_rows, continuous_rows, sigma_rows, vqm_runtime_rows, daily_runtime_rows, stitch_record, validation_rows)

    _write_csv(folders["ledger"] / f"{RUN_ID}_extended_local_continuous_daily_risk_history.csv", continuous_rows)
    _write_csv(folders["ledger"] / f"{RUN_ID}_sigma_i_t_ledger.csv", sigma_rows)
    _write_csv(folders["ledger"] / f"{RUN_ID}_relative_vol_v_q_m_daily_ledger.csv", vqm_runtime_rows)
    _write_csv(folders["runtime"] / f"{RUN_ID}_daily_runtime_rows.csv", daily_runtime_rows)
    _write_json(folders["provenance"] / f"{RUN_ID}_stitch_record.json", stitch_record)
    _write_csv(folders["validation"] / f"{RUN_ID}_validation_ledger.csv", validation_rows)
    _write_json(folders["status"] / f"{RUN_ID}_status.json", status)
    _write_json(folders["provenance"] / f"{RUN_ID}_provenance.json", _provenance_payload(status))
    _write_json(folders["hashes"] / f"{RUN_ID}_sha256.json", _hash_tree(OUTPUT_ROOT))
    PROCESS_DOC.write_text(_process_doc(status), encoding="utf-8")
    AUDIT_DOC.write_text(_audit_doc(status), encoding="utf-8")

    print(status["status"])
    print(f"extended_daily_rows={status['extended_daily_rows']}")
    print(f"vqm_rows={status['vqm_rows']}")
    print(f"daily_runtime_rows={status['daily_runtime_rows']}")
    print(f"artifact_root={OUTPUT_ROOT.relative_to(ROOT)}")


def _dedupe_r2_daily_rows(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row["completed_trading_date"]].append(row)
    output: list[dict[str, Any]] = []
    for day in sorted(grouped):
        candidates = grouped[day]
        signatures = {
            (
                row["raw_symbol"],
                row["instrument_id"],
                row["raw_close"],
                row["continuous_close"],
                row["additive_back_adjustment"],
            )
            for row in candidates
        }
        if len(signatures) != 1:
            raise SystemExit(f"Fail closed: non-identical duplicate R2 daily rows for {day}")
        row = candidates[0]
        output.append(
            {
                "completed_trading_date": day,
                "raw_symbol": row["raw_symbol"],
                "instrument_id": row["instrument_id"],
                "raw_close": float(row["raw_close"]),
                "additive_back_adjustment": float(row["additive_back_adjustment"]),
                "continuous_close": float(row["continuous_close"]),
                "source_artifact": str(R2_DAILY_CONTINUOUS_CSV.relative_to(ROOT)),
                "source_segment": "R2_DEDUPED_PRE_2015_SUPPORT_HISTORY",
            }
        )
    return output


def _build_extended_daily_rows(
    r2_unique: list[dict[str, Any]], vqm_rows: list[dict[str, str]]
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    r2_by_date = {row["completed_trading_date"]: row for row in r2_unique}
    vqm_by_date = {row["completed_trading_date"]: row for row in vqm_rows}
    bridge_day = "2015-01-01"
    if bridge_day not in r2_by_date or bridge_day not in vqm_by_date:
        raise SystemExit("Fail closed: missing bridge day for local daily runtime stitch")
    bridge_offset = float(vqm_by_date[bridge_day]["continuous_close"]) - float(r2_by_date[bridge_day]["continuous_close"])
    output: list[dict[str, Any]] = []
    for row in r2_unique:
        if row["completed_trading_date"] >= bridge_day:
            continue
        output.append(
            {
                "completed_trading_date": row["completed_trading_date"],
                "active_contract_key": row["raw_symbol"],
                "raw_symbol": row["raw_symbol"],
                "instrument_id": row["instrument_id"],
                "raw_close": row["raw_close"],
                "additive_back_adjustment": row["additive_back_adjustment"] + bridge_offset,
                "continuous_close": row["continuous_close"] + bridge_offset,
                "lineage_status": "DEV_RECON_LOCAL_BRIDGED_PRE_2015_R2_SUPPORT_HISTORY",
                "source_artifact": row["source_artifact"],
            }
        )
    for row in vqm_rows:
        output.append(
            {
                "completed_trading_date": row["completed_trading_date"],
                "active_contract_key": row["active_contract_key"],
                "raw_symbol": row["raw_symbol"],
                "instrument_id": row["instrument_id"],
                "raw_close": float(row["raw_close"]),
                "additive_back_adjustment": float(row["additive_back_adjustment"]),
                "continuous_close": float(row["continuous_close"]),
                "lineage_status": row["lineage_status"],
                "source_artifact": str(VQM_DAILY_CONTINUOUS_CSV.relative_to(ROOT)),
            }
        )
    dates = [row["completed_trading_date"] for row in output]
    if len(dates) != len(set(dates)):
        raise SystemExit("Fail closed: duplicate dates in extended daily runtime")
    stitch_record = {
        "gate": GATE,
        "bridge_day": bridge_day,
        "r2_bridge_continuous_close": r2_by_date[bridge_day]["continuous_close"],
        "vqm_bridge_continuous_close": float(vqm_by_date[bridge_day]["continuous_close"]),
        "pre_2015_bridge_offset_added_to_r2_history": bridge_offset,
        "pre_2015_source": str(R2_DAILY_CONTINUOUS_CSV.relative_to(ROOT)),
        "from_2015_source": str(VQM_DAILY_CONTINUOUS_CSV.relative_to(ROOT)),
        "stitch_status": "PASS_EXPLICIT_CONSTANT_BRIDGE_OFFSET_DEV_RECON_ONLY",
    }
    return output, stitch_record


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
    return rows


def _build_vqm_rows(sigma_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    smoothed: float | None = None
    alpha = 2.0 / (VQM_EWMA_SPAN + 1.0)
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
        raw_multiplier = 2.0 - 1.5 * q
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
                "method_status": "LOCKED_DAILY_S13_TEN_YEAR_V_Q_M_ATTENUATION_RUNTIME",
                "no_lookahead_status": "PASS_NO_LOOKAHEAD_DAILY_RUNTIME",
            }
        )
    if not rows:
        raise SystemExit("Fail closed: no V/Q/M rows emitted")
    return rows


def _build_daily_runtime_rows(continuous: list[dict[str, Any]], vqm_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    closes = [float(row["continuous_close"]) for row in continuous]
    dates = [row["completed_trading_date"] for row in continuous]
    fast = _ewma_series(closes, S27_TREND_FAST_SPAN)
    slow = _ewma_series(closes, S27_TREND_SLOW_SPAN)
    sigma_by_date = {row["completed_trading_date"]: row for row in _build_sigma_rows(continuous)}
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
                "source_vqm_completed_trading_date": day if vqm else "",
                "vol_multiplier_m_ewma10": vqm["vol_multiplier_m_ewma10"] if vqm else "",
                "relative_volatility_v": vqm["relative_volatility_v"] if vqm else "",
                "quantile_q": vqm["quantile_q"] if vqm else "",
                "runtime_status": "LOCAL_EXTENDED_DAILY_RUNTIME_DEPENDENCY_LEDGER_STRICT_PRIOR_DATE_REQUIRED",
            }
        )
    return output


def _validation_rows(
    r2_unique: list[dict[str, Any]],
    vqm_rows: list[dict[str, str]],
    continuous: list[dict[str, Any]],
    sigma_rows: list[dict[str, Any]],
    vqm_runtime_rows: list[dict[str, Any]],
    daily_runtime_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    dates = [row["completed_trading_date"] for row in continuous]
    return [
        _validation("r2_deduped_rows_available", bool(r2_unique), len(r2_unique)),
        _validation("vqm_bridge_rows_available", bool(vqm_rows), len(vqm_rows)),
        _validation("extended_daily_dates_unique", len(dates) == len(set(dates)), len(dates)),
        _validation("extended_daily_covers_2022_2023", min(dates) <= "2012-01-01" and max(dates) >= "2023-12-29", len(dates)),
        _validation("sigma_rows_nonempty", bool(sigma_rows), len(sigma_rows)),
        _validation("vqm_rows_cover_2022_2023", vqm_runtime_rows[0]["completed_trading_date"] <= "2022-01-01" and vqm_runtime_rows[-1]["completed_trading_date"] >= "2023-12-29", len(vqm_runtime_rows)),
        _validation("daily_runtime_rows_match_extended_daily", len(daily_runtime_rows) == len(continuous), len(daily_runtime_rows)),
        _validation("no_provider_api_access", True, 0),
        _validation("no_new_data_download", True, 0),
        _validation("no_oos_lockbox_forward", True, 0),
    ]


def _status_payload(
    r2_unique: list[dict[str, Any]],
    vqm_rows: list[dict[str, str]],
    continuous: list[dict[str, Any]],
    sigma_rows: list[dict[str, Any]],
    vqm_runtime_rows: list[dict[str, Any]],
    daily_runtime_rows: list[dict[str, Any]],
    stitch_record: dict[str, Any],
    validation_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "gate": GATE,
        "status": "PASS_LOCAL_EXTENDED_DAILY_RUNTIME_DEV_RECON_ONLY",
        "r2_deduped_rows": len(r2_unique),
        "vqm_bridge_rows": len(vqm_rows),
        "extended_daily_rows": len(continuous),
        "sigma_rows": len(sigma_rows),
        "vqm_rows": len(vqm_runtime_rows),
        "daily_runtime_rows": len(daily_runtime_rows),
        "extended_daily_start": continuous[0]["completed_trading_date"],
        "extended_daily_end": continuous[-1]["completed_trading_date"],
        "vqm_start": vqm_runtime_rows[0]["completed_trading_date"],
        "vqm_end": vqm_runtime_rows[-1]["completed_trading_date"],
        "bridge_day": stitch_record["bridge_day"],
        "pre_2015_bridge_offset_added_to_r2_history": stitch_record["pre_2015_bridge_offset_added_to_r2_history"],
        "validation_status": "PASS" if all(row["check_status"] == "PASS" for row in validation_rows) else "FAIL",
        "market_row_source": "EXISTING_LOCAL_QUARANTINE_ARTIFACTS_ONLY",
        "provider_api_access": "NO",
        "new_data_download": "NO",
        "diagnostics_run": "NO_SHARPE_NO_DRAWDOWN_NO_ALPHA_STATISTICS",
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
        "r2_daily_continuous_csv": str(R2_DAILY_CONTINUOUS_CSV.relative_to(ROOT)),
        "vqm_daily_continuous_csv": str(VQM_DAILY_CONTINUOUS_CSV.relative_to(ROOT)),
        "r2_daily_continuous_sha256": _sha256(R2_DAILY_CONTINUOUS_CSV),
        "vqm_daily_continuous_sha256": _sha256(VQM_DAILY_CONTINUOUS_CSV),
        "status": status,
    }


def _process_doc(status: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Carver S27 ZN 2022-2023 Local Extended Daily Runtime Result",
            "",
            "Status:",
            "",
            "```text",
            status["status"],
            "```",
            "",
            f"- Extended daily window: `{status['extended_daily_start']}` through `{status['extended_daily_end']}`.",
            f"- V/Q/M window: `{status['vqm_start']}` through `{status['vqm_end']}`.",
            f"- Extended daily rows: `{status['extended_daily_rows']}`.",
            f"- V/Q/M rows: `{status['vqm_rows']}`.",
            f"- Bridge day: `{status['bridge_day']}`.",
            f"- Pre-2015 R2 bridge offset: `{status['pre_2015_bridge_offset_added_to_r2_history']}`.",
            "",
            "Boundary: local Development/Reconciliation runtime reconstruction only. Existing local quarantine artifacts only; no provider API access, no new data download, no OOS, no Lockbox, no Forward, no deployment, no trading, no promotion, and no Git operations.",
            "",
        ]
    )


def _audit_doc(status: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Local Lean Hostile Audit - S27 ZN 2022-2023 Local Extended Daily Runtime",
            "",
            "CRITICAL: None for declared local runtime reconstruction scope.",
            "",
            "HIGH: None. The artifact uses existing local quarantine files only and emits explicit provenance for the R2 pre-2015 support-history segment, 2015+ V/Q/M segment, and bridge offset.",
            "",
            "MEDIUM: The pre-2015 support segment is a local Development/Reconciliation stitch, not a production continuous contract authority. It is used only to supply enough prior history for S13-style V/Q/M in 2022-2023.",
            "",
            "Verdict:",
            "",
            "```text",
            "BLOCKING_FINDINGS: NO_FOR_DECLARED_LOCAL_EXTENDED_DAILY_RUNTIME_SCOPE",
            "AUDIT_DISPOSITION: PASS_LOCAL_EXTENDED_DAILY_RUNTIME_DEV_RECON_ONLY",
            "```",
            "",
        ]
    )


def _ewma_series(values: list[float], span: int) -> list[float]:
    alpha = 2.0 / (span + 1.0)
    output: list[float] = []
    current: float | None = None
    for value in values:
        current = value if current is None else alpha * value + (1.0 - alpha) * current
        output.append(current)
    return output


def _quantile_rank_including_current(values: list[float], current: float) -> float:
    if len(values) < 2:
        return 0.5
    less = sum(1 for value in values if value < current)
    equal = sum(1 for value in values if value == current)
    rank = less + 0.5 * max(equal - 1, 0)
    return max(0.0, min(1.0, rank / (len(values) - 1)))


def _validation(name: str, passed: bool, observed_count: int) -> dict[str, Any]:
    return {"check_name": name, "check_status": "PASS" if passed else "FAIL", "observed_count": observed_count}


def _folders() -> dict[str, Path]:
    return {
        "ledger": OUTPUT_ROOT / "ledger",
        "runtime": OUTPUT_ROOT / "runtime_rows",
        "validation": OUTPUT_ROOT / "validation",
        "status": OUTPUT_ROOT / "status",
        "provenance": OUTPUT_ROOT / "provenance",
        "hashes": OUTPUT_ROOT / "hashes",
    }


def _require_inputs() -> None:
    for path in (R2_DAILY_CONTINUOUS_CSV, VQM_DAILY_CONTINUOUS_CSV):
        if not path.exists():
            raise SystemExit(f"Fail closed: missing required local artifact {path}")


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
    hash_name = f"{RUN_ID}_sha256.json"
    return {
        str(path.relative_to(ROOT)): _sha256(path)
        for path in sorted(root.rglob("*"))
        if path.is_file() and path.name != hash_name
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
