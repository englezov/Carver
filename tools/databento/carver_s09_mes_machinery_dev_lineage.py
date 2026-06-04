from __future__ import annotations

import csv
import hashlib
import json
import sys
from collections import Counter, defaultdict
from dataclasses import asdict
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from carver.spine.s09_mes_lineage import (  # noqa: E402
    S09MESDatedContractBar,
    S09MESDatedContractDefinition,
    S09MESLineageRequest,
    build_s09_mes_lineage,
    evaluate_s09_mes_lineage_strategy_readiness,
)

RUN_ID = "20260603_S09_MES_MACHINERY_DEV_LINEAGE"
SOURCE_RUN_ID = "20260603_S09_MES_MACHINERY_DEV_MINIMUM_SLICE_DOWNLOAD"
WINDOW_LABEL = "2019-05-05_2020-04-05"
WINDOW_TEXT = "2019-05-05 through 2020-04-05"
SOURCE_ROOT = ROOT / "docs" / "researchops" / "s09" / "mes_machinery_dev_minimum_slice" / WINDOW_LABEL
OUTPUT_ROOT = ROOT / "docs" / "researchops" / "s09" / "mes_machinery_dev_lineage" / WINDOW_LABEL
SANITIZED_CSV = SOURCE_ROOT / "sanitized_daily_bars" / f"{SOURCE_RUN_ID}_sanitized_quarantine_ohlcv_1d.csv"
SOURCE_STATUS_JSON = SOURCE_ROOT / "status" / f"{SOURCE_RUN_ID}_status.json"
SYMBOL_ORDER = ("MESM9", "MESU9", "MESZ9", "MESH0", "MESM0")
EWMAC64_MINIMUM_COMPLETED_BARS = 257


def main() -> None:
    _require_inputs()
    _ensure_dirs()

    source_status = json.loads(SOURCE_STATUS_JSON.read_text(encoding="utf-8"))
    bars_by_symbol, admission_rows = _load_bars()
    definitions_by_symbol, lifecycle_rows = _load_definitions()
    result = build_s09_mes_lineage(
        S09MESLineageRequest(
            symbol_order=SYMBOL_ORDER,
            bars_by_symbol=bars_by_symbol,
            definitions_by_symbol=definitions_by_symbol,
            minimum_target_rows=EWMAC64_MINIMUM_COMPLETED_BARS,
        )
    )
    readiness = evaluate_s09_mes_lineage_strategy_readiness(result)
    adjusted_rows = [_serialize_adjusted_row(row) for row in result.adjusted_rows]
    ewmac64_first_usable = (
        result.adjusted_rows[EWMAC64_MINIMUM_COMPLETED_BARS].completed_trading_date.isoformat()
        if len(result.adjusted_rows) > EWMAC64_MINIMUM_COMPLETED_BARS
        else ""
    )
    status: dict[str, Any] = {
        "run_id": RUN_ID,
        "gate": "S09_MES_MACHINERY_DEV_LINEAGE_GATE",
        "status": "FAIL_CLOSED_S09_MES_MACHINERY_DEV_LINEAGE_NOT_STRATEGY_INPUT",
        "lane_class": "SOURCE_NATIVE_FUTURES",
        "provider": "DATABENTO_HISTORICAL",
        "dataset": "GLBX.MDP3",
        "schema": "ohlcv-1d",
        "root": "MES",
        "row_id": "APPENDIX_C_174_006",
        "source_window": WINDOW_TEXT,
        "window_role": "MINIMUM_OLDEST_MACHINERY_DEVELOPMENT_SLICE_NOT_SCORED_EVIDENCE",
        "source_download_status": source_status.get("status"),
        "source_sanitized_csv": _rel(SANITIZED_CSV),
        "databento_api_access": "NO",
        "new_provider_data_download": "NO",
        "market_row_parsing": "YES_EXISTING_AUTHORIZED_MACHINERY_SLICE_ONLY",
        "continuous_lineage_constructed": "YES_PROVISIONAL_LOCAL_MACHINERY_ONLY_NOT_STRATEGY_INPUT",
        "forecast_computation": "NO",
        "diagnostics_run": "NO",
        "backtests_run": "NO",
        "position_computation": "NO",
        "cost_computation": "NO",
        "test_validation_lockbox_forward_access": "NO",
        "total_adjusted_rows": len(result.adjusted_rows),
        "roll_events": len(result.roll_events),
        "admitted_normal_rows": sum(int(row["admitted_rows"]) for row in admission_rows),
        "rejected_degraded_or_unresolved_rows": sum(int(row["rejected_degraded_or_unresolved_rows"]) for row in admission_rows),
        "ewmac64_minimum_completed_bars": EWMAC64_MINIMUM_COMPLETED_BARS,
        "first_ewmac64_usable_completed_date": ewmac64_first_usable,
        "ewmac64_usable_rows_after_minimum_warmup": max(0, len(result.adjusted_rows) - EWMAC64_MINIMUM_COMPLETED_BARS),
        **readiness,
        "provider_condition_admission_status": "LOCKED_NORMAL_PROVIDER_ROWS_ONLY",
        "strategy_input_readiness_status": "FAIL_CLOSED_S09_MES_STRATEGY_INPUT_NOT_READY",
        "next_required_gate": "S09_MES_RUNTIME_RISK_COST_INPUT_LOCK_GATE_OR_OFFICIAL_ROLL_SEMANTICS_GATE",
    }

    _write_csv(OUTPUT_ROOT / "input_manifest" / f"{RUN_ID}_input_hash_manifest.csv", _input_manifest_rows())
    _write_csv(OUTPUT_ROOT / "admission" / f"{RUN_ID}_provider_condition_admission_ledger.csv", admission_rows)
    _write_csv(OUTPUT_ROOT / "lifecycle" / f"{RUN_ID}_definition_crosscheck_ledger.csv", lifecycle_rows)
    _write_csv(OUTPUT_ROOT / "roll_plan" / f"{RUN_ID}_roll_plan.csv", [_serialize_roll_event(event) for event in result.roll_events])
    _write_csv(OUTPUT_ROOT / "continuous_series" / f"{RUN_ID}_continuous_daily_mes_machinery_only.csv", adjusted_rows)
    _write_csv(OUTPUT_ROOT / "warmup" / f"{RUN_ID}_ewmac64_warmup_accounting.csv", [_warmup_row(status)])
    _write_csv(OUTPUT_ROOT / "status" / f"{RUN_ID}_status.csv", [status])
    _write_json(OUTPUT_ROOT / "status" / f"{RUN_ID}_status.json", status)
    _write_provenance(status)
    _write_hashes()
    print("S09_MES_MACHINERY_DEV_LINEAGE_RESULT_WRITTEN")
    print(f"artifact_root={OUTPUT_ROOT.relative_to(ROOT).as_posix()}")
    print(f"total_adjusted_rows={status['total_adjusted_rows']}")
    print(f"first_ewmac64_usable_completed_date={status['first_ewmac64_usable_completed_date']}")


def _require_inputs() -> None:
    missing = [path for path in (SANITIZED_CSV, SOURCE_STATUS_JSON) if not path.exists()]
    for symbol in SYMBOL_ORDER:
        definition_csv = SOURCE_ROOT / "raw_provider_metadata" / f"{SOURCE_RUN_ID}_{symbol}_definition.csv"
        if not definition_csv.exists():
            missing.append(definition_csv)
    if missing:
        raise FileNotFoundError("Missing S09 MES machinery lineage inputs: " + ", ".join(str(path) for path in missing))


def _ensure_dirs() -> None:
    for name in ("input_manifest", "admission", "lifecycle", "roll_plan", "continuous_series", "warmup", "status", "provenance", "hashes"):
        (OUTPUT_ROOT / name).mkdir(parents=True, exist_ok=True)


def _load_bars() -> tuple[dict[str, tuple[S09MESDatedContractBar, ...]], list[dict[str, object]]]:
    grouped: dict[str, list[S09MESDatedContractBar]] = defaultdict(list)
    counts: dict[str, Counter[str]] = defaultdict(Counter)
    with SANITIZED_CSV.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            symbol = row["raw_symbol"]
            if symbol not in SYMBOL_ORDER:
                raise ValueError(f"Unexpected S09 MES machinery symbol {symbol}")
            classification = row["provider_condition_classification"]
            counts[symbol][classification] += 1
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

    bars_by_symbol = {symbol: tuple(sorted(grouped[symbol], key=lambda bar: bar.completed_trading_date)) for symbol in SYMBOL_ORDER}
    admission_rows: list[dict[str, object]] = []
    for symbol in SYMBOL_ORDER:
        admission_rows.append(
            {
                "raw_symbol": symbol,
                "admitted_rows": len(bars_by_symbol[symbol]),
                "normal_provider_condition_rows": counts[symbol]["NORMAL_PROVIDER_CONDITION"],
                "rejected_degraded_or_unresolved_rows": sum(count for key, count in counts[symbol].items() if key != "NORMAL_PROVIDER_CONDITION"),
                "admission_status": "LOCKED_NORMAL_PROVIDER_CONDITION_ONLY",
            }
        )
    return bars_by_symbol, admission_rows


def _load_definitions() -> tuple[dict[str, S09MESDatedContractDefinition], list[dict[str, object]]]:
    definitions: dict[str, S09MESDatedContractDefinition] = {}
    rows: list[dict[str, object]] = []
    for symbol in SYMBOL_ORDER:
        path = SOURCE_ROOT / "raw_provider_metadata" / f"{SOURCE_RUN_ID}_{symbol}_definition.csv"
        selected = _first_definition_row(path, symbol)
        definition = S09MESDatedContractDefinition(
            raw_symbol=symbol,
            expiration=_parse_utc(selected["expiration"]),
            product_code=selected["asset"],
            currency=selected["currency"],
            multiplier=float(selected["unit_of_measure_qty"]),
            tick_size=float(selected["min_price_increment"]),
            venue=selected["exchange"],
            lifecycle_source="DATABENTO_DEFINITION_CROSSCHECK_MACHINERY_ONLY",
        )
        definition.validate()
        definitions[symbol] = definition
        rows.append(
            {
                "raw_symbol": symbol,
                "definition_csv": _rel(path),
                "definition_csv_sha256": _sha256(path),
                "expiration_utc": definition.expiration.isoformat(),
                "product_code": definition.product_code,
                "currency": definition.currency,
                "multiplier": definition.multiplier,
                "tick_size": definition.tick_size,
                "venue": definition.venue,
                "lifecycle_source_status": "PROVIDER_DEFINITION_CROSSCHECK_ONLY_NOT_OFFICIAL_ROLL_SEMANTICS_LOCK",
            }
        )
    return definitions, rows


def _input_manifest_rows() -> list[dict[str, object]]:
    rows = [
        {
            "input_role": "source_sanitized_csv",
            "path": _rel(SANITIZED_CSV),
            "sha256": _sha256(SANITIZED_CSV),
            "scope_note": "Authorized oldest S09 MES machinery-development slice only",
        },
        {
            "input_role": "source_status_json",
            "path": _rel(SOURCE_STATUS_JSON),
            "sha256": _sha256(SOURCE_STATUS_JSON),
            "scope_note": "Source download status; confirms no forecast/backtest in download gate",
        },
    ]
    for symbol in SYMBOL_ORDER:
        path = SOURCE_ROOT / "raw_provider_metadata" / f"{SOURCE_RUN_ID}_{symbol}_definition.csv"
        rows.append(
            {
                "input_role": f"definition_crosscheck_{symbol}",
                "path": _rel(path),
                "sha256": _sha256(path),
                "scope_note": "Provider definition cross-check for machinery only",
            }
        )
    return rows


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


def _serialize_roll_event(event: Any) -> dict[str, object]:
    row = asdict(event)
    for key in ("expiration_date", "roll_buffer_date", "roll_transition_date"):
        row[key] = row[key].isoformat()
    row["roll_rule"] = "STATIC_LIFECYCLE_BUFFER_ROLL_5_PROVIDER_DATES_MACHINERY_ONLY"
    row["adjustment_method"] = "LOCAL_ADDITIVE_BACK_ADJUSTMENT_NOT_STRATEGY_INPUT"
    return row


def _serialize_adjusted_row(row: Any) -> dict[str, object]:
    output = asdict(row)
    output["completed_trading_date"] = row.completed_trading_date.isoformat()
    output["lineage_status"] = "PROVISIONAL_LOCAL_MACHINERY_LINEAGE_NOT_STRATEGY_INPUT"
    return output


def _warmup_row(status: dict[str, Any]) -> dict[str, object]:
    return {
        "source_window": status["source_window"],
        "total_adjusted_rows": status["total_adjusted_rows"],
        "ewmac64_minimum_completed_bars": status["ewmac64_minimum_completed_bars"],
        "first_ewmac64_usable_completed_date": status["first_ewmac64_usable_completed_date"],
        "ewmac64_usable_rows_after_minimum_warmup": status["ewmac64_usable_rows_after_minimum_warmup"],
        "warmup_status": "PLANNING_ACCOUNTING_ONLY_NOT_FORECAST_NOT_BACKTEST",
    }


def _write_provenance(status: dict[str, Any]) -> None:
    text = f"""# S09 MES Machinery Development Lineage Provenance

Date: 2026-06-03

Status:

```text
{status["status"]}
```

This packet used only the authorized oldest machinery-development slice:
{WINDOW_TEXT}. It is not scored evidence.

The runner admitted normal provider-condition rows only, rejected degraded or
unresolved rows, and emitted a provisional local additive lineage for machinery
inspection. The EWMAC64 first usable date is warmup planning accounting only.

Boundary: no provider API access, no new data download, no S09 forecast computation, no diagnostics, no backtests, no returns, no PnL, no positions, no carry, no cost computation, no TEST, no VALIDATION, no OOS, no Lockbox, no Forward, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR, and no remote operations.
"""
    _write_text(OUTPUT_ROOT / "provenance" / f"{RUN_ID}_provenance.md", text)


def _write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"No rows to write for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def _write_json(path: Path, payload: Any) -> None:
    _write_text(path, json.dumps(payload, indent=2, sort_keys=True, default=str) + "\n")


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def _write_hashes() -> None:
    hash_path = OUTPUT_ROOT / "hashes" / f"{RUN_ID}_sha256.json"
    hashes: dict[str, str] = {}
    for path in sorted(OUTPUT_ROOT.rglob("*")):
        if path.is_file() and path != hash_path:
            hashes[_rel(path)] = _sha256(path)
    _write_json(hash_path, hashes)


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
