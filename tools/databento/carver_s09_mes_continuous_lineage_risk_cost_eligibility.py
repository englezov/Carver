from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter, defaultdict
from dataclasses import asdict
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

import sys

sys.path.insert(0, str(ROOT / "src"))

from carver.spine.s09_mes_lineage import (  # noqa: E402
    S09MESDatedContractBar,
    S09MESDatedContractDefinition,
    S09MESLineageRequest,
    build_s09_mes_lineage,
    evaluate_s09_mes_lineage_strategy_readiness,
)
from carver.spine.m0 import CarverBlocked  # noqa: E402


RUN_ID = "20260603_S09_MES_CONTINUOUS_LINEAGE_RISK_COST_ELIGIBILITY"
SOURCE_RUN_ID = "20260602_S09_MES_DEV_RECON_DAILY_EXPANSION"
DEPRECATED_TWO_YEAR_DEV_WINDOW_QUARANTINE = (
    "DEPRECATED_TWO_YEAR_DEV_WINDOW_QUARANTINE: this executable consumes the superseded "
    "2022-01-03 through 2023-12-29 development window. Use the oldest minimum machinery-development "
    "slice 2019-05-05 through 2020-04-05 via the authorized machinery-dev/evidence-completion path."
)
TARGET_START = date(2022, 1, 3)
TARGET_END = date(2023, 12, 29)
EXPANSION_ROOT = ROOT / "docs" / "researchops" / "s09" / "mes_dev_recon_data_expansion" / "2022-01-03_2023-12-29"
OUTPUT_ROOT = ROOT / "docs" / "researchops" / "s09" / "mes_continuous_lineage_risk_cost_eligibility" / "2022-01-03_2023-12-29"
SANITIZED_CSV = EXPANSION_ROOT / "sanitized_daily_bars" / f"{SOURCE_RUN_ID}_sanitized_quarantine_ohlcv_1d.csv"
STATUS_JSON = EXPANSION_ROOT / "status" / f"{SOURCE_RUN_ID}_status.json"
STATIC_MES_SOURCE_EXTRACT = ROOT / "docs" / "researchops" / "first_data_intake" / "CARVER_NINJATRADER_SUPPORTED_PILOT_MES_STATIC_DATED_CONTRACT_SOURCE_EXTRACT_2026-05-30.md"
SYMBOL_ORDER = (
    "MESH1",
    "MESM1",
    "MESU1",
    "MESZ1",
    "MESH2",
    "MESM2",
    "MESU2",
    "MESZ2",
    "MESH3",
    "MESM3",
    "MESU3",
    "MESZ3",
    "MESH4",
)


def main() -> None:
    raise CarverBlocked(DEPRECATED_TWO_YEAR_DEV_WINDOW_QUARANTINE)
    _require_inputs()
    _ensure_dirs()
    source_status = json.loads(STATUS_JSON.read_text(encoding="utf-8"))
    bars_by_symbol, admission_rows = _load_bars()
    definitions_by_symbol, lifecycle_rows = _load_definitions()
    result = build_s09_mes_lineage(
        S09MESLineageRequest(
            symbol_order=SYMBOL_ORDER,
            bars_by_symbol=bars_by_symbol,
            definitions_by_symbol=definitions_by_symbol,
            minimum_target_rows=257,
        )
    )
    readiness = evaluate_s09_mes_lineage_strategy_readiness(result)
    target_rows = [
        row
        for row in result.adjusted_rows
        if TARGET_START <= row.completed_trading_date <= TARGET_END
    ]
    status = {
        "run_id": RUN_ID,
        "gate": "S09_MES_CONTINUOUS_LINEAGE_RISK_COST_ELIGIBILITY_EXECUTION_GATE",
        "status": "FAIL_CLOSED_S09_MES_STRATEGY_INPUT_NOT_READY_LIFECYCLE_RISK_COST_SPEED_NOT_LOCKED",
        "lane_class": "SOURCE_NATIVE_FUTURES",
        "provider": "DATABENTO_HISTORICAL",
        "dataset": "GLBX.MDP3",
        "schema": "ohlcv-1d",
        "root": "MES",
        "source_expansion_status": source_status.get("status"),
        "source_sanitized_csv": _rel(SANITIZED_CSV),
        "databento_api_access": "NO",
        "new_provider_data_download": "NO",
        "market_row_parsing": "YES_EXISTING_S09_MES_QUARANTINE_ONLY",
        "continuous_lineage_constructed": "YES_PROVISIONAL_LOCAL_ADDITIVE_DEV_RECON_ONLY_NOT_STRATEGY_INPUT",
        "forecast_computation": "NO",
        "backtests_run": "NO",
        "position_computation": "NO",
        "cost_computation": "NO_COST_SOURCE_FAIL_CLOSED",
        "total_adjusted_rows": len(result.adjusted_rows),
        "target_window_adjusted_rows": len(target_rows),
        "roll_events": len(result.roll_events),
        "admitted_normal_rows": sum(row["admitted_rows"] for row in admission_rows),
        "rejected_degraded_or_unresolved_rows": sum(row["rejected_degraded_or_unresolved_rows"] for row in admission_rows),
        **readiness,
        "next_required_gate": "S09_MES_OFFICIAL_LIFECYCLE_ROLL_SEMANTICS_ANNUAL_RISK_AND_COST_SOURCE_LOCK_GATE",
    }

    _write_csv(OUTPUT_ROOT / "input_manifest" / f"{RUN_ID}_input_hash_manifest.csv", _input_manifest_rows())
    _write_csv(OUTPUT_ROOT / "admission" / f"{RUN_ID}_provider_condition_admission_ledger.csv", admission_rows)
    _write_csv(OUTPUT_ROOT / "lifecycle" / f"{RUN_ID}_lifecycle_evidence_ledger.csv", lifecycle_rows)
    _write_csv(OUTPUT_ROOT / "roll_plan" / f"{RUN_ID}_roll_plan.csv", [_serialize_roll_event(event) for event in result.roll_events])
    _write_csv(OUTPUT_ROOT / "adjustment" / f"{RUN_ID}_adjustment_ledger.csv", [_serialize_adjusted_row(row) for row in result.adjusted_rows])
    _write_csv(OUTPUT_ROOT / "continuous_series" / f"{RUN_ID}_continuous_daily_mes_dev_recon_only.csv", [_serialize_adjusted_row(row) for row in result.adjusted_rows])
    _write_csv(OUTPUT_ROOT / "risk_cost" / f"{RUN_ID}_annual_risk_and_cost_fail_closed_ledger.csv", [_risk_cost_blocker_row(status)])
    _write_csv(OUTPUT_ROOT / "status" / f"{RUN_ID}_strategy_input_readiness_status.csv", [status])
    (OUTPUT_ROOT / "status" / f"{RUN_ID}_strategy_input_readiness_status.json").write_text(
        json.dumps(status, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    _write_provenance(status)
    _write_hashes()


def _require_inputs() -> None:
    missing = [path for path in (SANITIZED_CSV, STATUS_JSON, STATIC_MES_SOURCE_EXTRACT) if not path.exists()]
    if missing:
        raise FileNotFoundError("Missing S09 MES lineage inputs: " + ", ".join(str(path) for path in missing))


def _ensure_dirs() -> None:
    for name in ("input_manifest", "admission", "lifecycle", "roll_plan", "adjustment", "continuous_series", "risk_cost", "status", "provenance", "hashes"):
        (OUTPUT_ROOT / name).mkdir(parents=True, exist_ok=True)


def _load_bars() -> tuple[dict[str, tuple[S09MESDatedContractBar, ...]], list[dict[str, object]]]:
    grouped: dict[str, list[S09MESDatedContractBar]] = defaultdict(list)
    counts: dict[str, Counter[str]] = defaultdict(Counter)
    with SANITIZED_CSV.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            symbol = row["raw_symbol"]
            classification = row["provider_condition_classification"]
            counts[symbol][classification] += 1
            if symbol not in SYMBOL_ORDER:
                raise ValueError(f"Unexpected S09 MES symbol {symbol}")
            if classification != "NORMAL_PROVIDER_CONDITION":
                continue
            grouped[symbol].append(
                S09MESDatedContractBar(
                    raw_symbol=symbol,
                    completed_trading_date=date.fromisoformat(row["completed_trading_date"]),
                    open=float(row["open"]),
                    high=float(row["high"]),
                    low=float(row["low"]),
                    close=float(row["close"]),
                    volume=float(row["volume"]),
                    provider_condition_classification=classification,
                    source_raw_sha256=row["source_raw_sha256"],
                )
            )
    bars_by_symbol = {symbol: tuple(grouped[symbol]) for symbol in SYMBOL_ORDER}
    rows: list[dict[str, object]] = []
    for symbol in SYMBOL_ORDER:
        rows.append(
            {
                "raw_symbol": symbol,
                "admitted_rows": len(bars_by_symbol[symbol]),
                "normal_provider_condition_rows": counts[symbol]["NORMAL_PROVIDER_CONDITION"],
                "rejected_degraded_or_unresolved_rows": sum(count for key, count in counts[symbol].items() if key != "NORMAL_PROVIDER_CONDITION"),
                "admission_status": "LOCKED_NORMAL_PROVIDER_CONDITION_ONLY",
            }
        )
    return bars_by_symbol, rows


def _load_definitions() -> tuple[dict[str, S09MESDatedContractDefinition], list[dict[str, object]]]:
    definitions: dict[str, S09MESDatedContractDefinition] = {}
    rows: list[dict[str, object]] = []
    for symbol in SYMBOL_ORDER:
        definition_csv = _definition_csv_for(symbol)
        selected = _first_definition_row(definition_csv, symbol)
        expiration = _parse_utc(selected["expiration"])
        multiplier = float(selected["unit_of_measure_qty"])
        tick_size = float(selected["min_price_increment"])
        venue = selected["exchange"]
        definition = S09MESDatedContractDefinition(
            raw_symbol=symbol,
            expiration=expiration,
            product_code=selected["asset"],
            currency=selected["currency"],
            multiplier=multiplier,
            tick_size=tick_size,
            venue=venue,
            lifecycle_source="DATABENTO_DEFINITION_CROSSCHECK_PLUS_LOCAL_CME_STATIC_MES_EXTRACT_2026-05-30",
        )
        definition.validate()
        definitions[symbol] = definition
        rows.append(
            {
                "raw_symbol": symbol,
                "definition_csv": _rel(definition_csv),
                "definition_csv_sha256": _sha256(definition_csv),
                "expiration_utc": expiration.isoformat(),
                "product_code": definition.product_code,
                "currency": definition.currency,
                "multiplier": definition.multiplier,
                "tick_size": definition.tick_size,
                "venue": definition.venue,
                "official_static_mes_source_extract": _rel(STATIC_MES_SOURCE_EXTRACT),
                "lifecycle_source_status": "PROVISIONAL_FOR_LOCAL_BUFFER_ROLL_CROSSCHECK_OFFICIAL_2021_2024_LIFECYCLE_PACKET_REQUIRED",
            }
        )
    return definitions, rows


def _input_manifest_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = [
        {
            "input_role": "source_sanitized_csv",
            "path": _rel(SANITIZED_CSV),
            "sha256": _sha256(SANITIZED_CSV),
            "scope_note": "Existing S09 MES quarantine OHLCV-1d rows only",
        },
        {
            "input_role": "source_status_json",
            "path": _rel(STATUS_JSON),
            "sha256": _sha256(STATUS_JSON),
            "scope_note": "Existing S09 MES expansion status",
        },
        {
            "input_role": "static_mes_extract_narrow_scope",
            "path": _rel(STATIC_MES_SOURCE_EXTRACT),
            "sha256": _sha256(STATIC_MES_SOURCE_EXTRACT),
            "scope_note": "Generic MES facts plus MES 06-26 narrow pilot; not sufficient for official 2021-2024 lifecycle lock",
        },
    ]
    for symbol in SYMBOL_ORDER:
        path = _definition_csv_for(symbol)
        rows.append(
            {
                "input_role": f"databento_definition_crosscheck_{symbol}",
                "path": _rel(path),
                "sha256": _sha256(path),
                "scope_note": f"Provider definition cross-check for {symbol}; not a replacement for official lifecycle evidence",
            }
        )
    return rows


def _definition_csv_for(symbol: str) -> Path:
    metadata_root = EXPANSION_ROOT / "raw_provider_metadata"
    if symbol == "MESZ3":
        path = metadata_root / f"{SOURCE_RUN_ID}_{symbol}_definition_retry.csv"
    else:
        path = metadata_root / f"{SOURCE_RUN_ID}_{symbol}_definition.csv"
    if not path.exists():
        raise FileNotFoundError(path)
    return path


def _first_definition_row(path: Path, symbol: str) -> dict[str, str]:
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if row["raw_symbol"] == symbol and row["expiration"]:
                return row
    raise ValueError(f"No definition row with expiration for {symbol}")


def _parse_utc(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _serialize_roll_event(event) -> dict[str, object]:
    row = asdict(event)
    for key in ("expiration_date", "roll_buffer_date", "roll_transition_date"):
        row[key] = row[key].isoformat()
    row["roll_rule"] = "STATIC_LIFECYCLE_BUFFER_ROLL_5_COMPLETED_PROVIDER_DATES"
    row["adjustment_method"] = "LOCAL_ADDITIVE_BACK_ADJUSTMENT_OLD_HISTORY_TO_NEW_CONTRACT_LEVEL"
    return row


def _serialize_adjusted_row(row) -> dict[str, object]:
    output = asdict(row)
    output["completed_trading_date"] = row.completed_trading_date.isoformat()
    output["lineage_status"] = "LOCAL_CONTINUOUS_DEV_RECON_ONLY_NOT_BACKTEST_NOT_PRODUCTION"
    return output


def _risk_cost_blocker_row(status: dict[str, object]) -> dict[str, object]:
    return {
        "root": "MES",
        "official_lifecycle_evidence_status": status["official_lifecycle_evidence_status"],
        "roll_trading_day_semantics_status": status["roll_trading_day_semantics_status"],
        "annual_risk_runtime_status": status["annual_risk_runtime_status"],
        "daily_price_risk_runtime_status": status["daily_price_risk_runtime_status"],
        "cost_source_status": status["cost_source_status"],
        "risk_adjusted_cost_status": status["risk_adjusted_cost_status"],
        "speed_cost_eligibility_status": status["speed_cost_eligibility_status"],
        "eligible_speed_set_status": status["eligible_speed_set_status"],
        "blocker_summary": "S09 MES provisional local continuous lineage exists, but official 2021-2024 lifecycle evidence, provider trading-date roll semantics, S03 annual-risk runtime, and source-native cost/speed eligibility are not locked.",
    }


def _write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"No rows to write for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def _write_provenance(status: dict[str, object]) -> None:
    lines = [
        "# Carver S09 MES Continuous Lineage Risk Cost Eligibility Execution Result",
        "",
        "Date: 2026-06-03",
        "",
        "Status:",
        "",
        "```text",
        str(status["status"]),
        "```",
        "",
        "This execution used only the existing S09 MES Databento daily expansion artifacts. It made no Databento API call and downloaded no new data.",
        "",
        "Outputs are Development/Reconciliation-only local continuous lineage artifacts. They are not forecasts, diagnostics, backtests, positions, or promotion evidence.",
        "",
        "Provider-condition admission is locked for normal rows only. The lineage, roll plan, and additive back-adjustment surfaces are provisional local Development/Reconciliation artifacts because official 2021-2024 lifecycle evidence and provider trading-date roll semantics are not yet locked.",
        "",
        "Roll transitions use provider trading-date rows, including Sunday session labels when Databento publishes those completed daily rows. This is not yet a Carver/S09 completed-trading-day semantic lock.",
        "",
        "Strategy input remains fail-closed because official lifecycle evidence, roll-date semantics, the S03 annual-risk runtime, and source-native MES cost/speed eligibility are not locked.",
        "",
        "Non-Authorization: no provider API access, no new data download, no S09 forecast computation, no diagnostics, no backtests, no returns, no PnL, no positions, no cost computation, no carry, no CFD adapter work, no old QuantLab pipeline use, no tuning, no TEST, no VALIDATION, no OOS, no Lockbox, no Forward, no deployment, no trading, no promotion, no Git staging, no commit, no push, and no remote operations.",
        "",
    ]
    (OUTPUT_ROOT / "provenance" / f"{RUN_ID}_provenance.md").write_text("\n".join(lines), encoding="utf-8")


def _write_hashes() -> None:
    hash_path = OUTPUT_ROOT / "hashes" / f"{RUN_ID}_sha256.json"
    hashes: dict[str, str] = {}
    for path in sorted(OUTPUT_ROOT.rglob("*")):
        if path.is_file() and path != hash_path:
            hashes[_rel(path)] = _sha256(path)
    hash_path.write_text(json.dumps(hashes, indent=2, sort_keys=True), encoding="utf-8")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def _rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


if __name__ == "__main__":
    main()
