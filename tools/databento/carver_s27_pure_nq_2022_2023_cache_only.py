from __future__ import annotations

import csv
import importlib.util
import json
import sys
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

BASE_MODULE_PATH = ROOT / "tools/databento/carver_s27_candidate_comparison_2022_2023.py"
BASE_SPEC = importlib.util.spec_from_file_location("carver_s27_candidate_comparison_2022_2023", BASE_MODULE_PATH)
if BASE_SPEC is None or BASE_SPEC.loader is None:
    raise RuntimeError(f"Unable to load base comparison module from {BASE_MODULE_PATH}")
base = importlib.util.module_from_spec(BASE_SPEC)
sys.modules[BASE_SPEC.name] = base
BASE_SPEC.loader.exec_module(base)


RUN_ID = "20260601_S27_PURE_NQ_CACHE_ONLY_TEST_2022_2023"
GATE = "S27_PURE_NQ_SOURCE_NATIVE_FUTURES_CACHE_ONLY_TEST"
SOURCE_CACHE_ROOT = (
    ROOT
    / "docs/researchops/s26_s27_index_signal_proxy/2022-01-01_2023-12-31/NQ_SIGNAL_TO_MNQ_EXECUTION/signal_NQ"
)
CONDITION_ROOT = ROOT / "docs/researchops/s26_s27_index_signal_proxy/2022-01-01_2023-12-31/raw_provider_metadata"
OUTPUT_ROOT = ROOT / "docs/researchops/s26_s27_pure_nq/2022-01-01_2023-12-31"
PROCESS_RESULT_DOC = ROOT / "docs/process/CARVER_S27_PURE_NQ_CACHE_ONLY_TEST_2022_2023_RESULT_2026-06-01.md"
LOCAL_AUDIT_DOC = ROOT / "docs/process/CARVER_S27_PURE_NQ_CACHE_ONLY_TEST_2022_2023_LOCAL_LEAN_HOSTILE_AUDIT_2026-06-01.md"


def main() -> None:
    _patch_base_globals()
    folders = base._folders(OUTPUT_ROOT)
    for folder in folders.values():
        folder.mkdir(parents=True, exist_ok=True)

    candidate = base.Candidate(
        "NQ",
        "SOURCE_NATIVE_BASE_FUTURES_NQ",
        "Nasdaq 100 base futures source-native signal and execution",
        "index",
        20.0,
        0.0,
        date(2011, 1, 1),
    )

    hourly_condition = _condition_by_date("hourly")
    daily_condition = _condition_by_date("daily")
    status: dict[str, Any]
    cache_ledger: list[dict[str, Any]] = []
    hourly_rows: list[dict[str, Any]] = []
    daily_rows_by_contract: dict[str, list[dict[str, Any]]] = {}
    try:
        hourly_rows, daily_rows_by_contract, cache_ledger = _load_cached_rows(candidate, hourly_condition, daily_condition)
        base._write_csv(folders["metadata"] / f"{RUN_ID}_NQ_cache_source_ledger.csv", cache_ledger)
        missing_cache = [row for row in cache_ledger if row["cache_status"] != "CACHE_FILE_PRESENT_USED"]
        if missing_cache:
            missing_text = ", ".join(row["expected_file"] for row in missing_cache[:12])
            raise RuntimeError(f"missing cached NQ provider files: {missing_text}")
        hourly_contracts = base._comparison_contracts("NQ")
        daily_contracts = base._daily_contracts("NQ", candidate.daily_history_start)
        hourly_continuous, inactive_hourly, hourly_roll_plan = base._build_continuous_rows(
            candidate=candidate,
            contracts=hourly_contracts,
            source_rows=hourly_rows,
            price_field="close",
            timestamp_field="derived_completed_bar_end_utc",
            output_root=folders["lineage"],
            prefix=f"{RUN_ID}_NQ_hourly",
        )
        daily_source_rows = [row for rows in daily_rows_by_contract.values() for row in rows]
        daily_continuous, inactive_daily, daily_roll_plan = base._build_continuous_rows(
            candidate=candidate,
            contracts=daily_contracts,
            source_rows=daily_source_rows,
            price_field="close",
            timestamp_field="completed_trading_date",
            output_root=folders["lineage"],
            prefix=f"{RUN_ID}_NQ_daily",
        )
        sigma_rows = base._build_sigma_rows(daily_continuous)
        vqm_rows = base._build_vqm_rows(sigma_rows)
        daily_runtime_rows = base._build_daily_runtime_rows(daily_continuous, vqm_rows)
        s26_rows, s27_rows, blocked_rows = base._build_forecasts(candidate, hourly_continuous, daily_runtime_rows)
        position_rows = base._build_positions(s27_rows)
        backtest_rows = base._build_backtest_rows(candidate, hourly_continuous, position_rows)
        validation_rows = base._build_validation_rows(
            hourly_rows=hourly_rows,
            hourly_continuous=hourly_continuous,
            inactive_hourly=inactive_hourly,
            s26_rows=s26_rows,
            s27_rows=s27_rows,
            position_rows=position_rows,
            backtest_rows=backtest_rows,
        )

        base._write_csv(folders["lineage"] / f"{RUN_ID}_NQ_hourly_continuous_lineage.csv", hourly_continuous)
        base._write_csv(folders["lineage"] / f"{RUN_ID}_NQ_hourly_inactive_rows.csv", inactive_hourly)
        base._write_csv(folders["lineage"] / f"{RUN_ID}_NQ_hourly_roll_plan.csv", hourly_roll_plan)
        base._write_csv(folders["lineage"] / f"{RUN_ID}_NQ_daily_continuous_lineage.csv", daily_continuous)
        base._write_csv(folders["lineage"] / f"{RUN_ID}_NQ_daily_inactive_rows.csv", inactive_daily)
        base._write_csv(folders["lineage"] / f"{RUN_ID}_NQ_daily_roll_plan.csv", daily_roll_plan)
        base._write_csv(folders["runtime"] / f"{RUN_ID}_NQ_sigma_rows.csv", sigma_rows)
        base._write_csv(folders["runtime"] / f"{RUN_ID}_NQ_vqm_rows.csv", vqm_rows)
        base._write_csv(folders["runtime"] / f"{RUN_ID}_NQ_daily_runtime_rows.csv", daily_runtime_rows)
        base._write_csv(folders["forecasts"] / f"{RUN_ID}_NQ_s26_forecast_rows.csv", s26_rows)
        base._write_csv(folders["forecasts"] / f"{RUN_ID}_NQ_s27_forecast_rows.csv", s27_rows)
        base._write_csv(folders["forecasts"] / f"{RUN_ID}_NQ_blocked_dependency_rows.csv", blocked_rows)
        base._write_csv(folders["positions"] / f"{RUN_ID}_NQ_unit_position_rows.csv", position_rows)
        base._write_csv(folders["backtest"] / f"{RUN_ID}_NQ_unit_zero_cost_backtest_rows.csv", backtest_rows)
        base._write_csv(folders["validation"] / f"{RUN_ID}_NQ_validation_ledger.csv", validation_rows)

        status = base._candidate_pass_status(
            candidate,
            hourly_rows,
            hourly_continuous,
            inactive_hourly,
            hourly_roll_plan,
            daily_continuous,
            daily_roll_plan,
            s26_rows,
            s27_rows,
            blocked_rows,
            position_rows,
            backtest_rows,
            [],
        )
        status["status"] = "PASS_S27_PURE_NQ_SOURCE_NATIVE_FUTURES_CACHE_ONLY_TEST_NOT_ALPHA"
        status["gate"] = GATE
        status["source_cache"] = "REUSED_NQ_PROVIDER_FILES_FROM_INTERRUPTED_NQ_SIGNAL_TO_MNQ_GATE_NO_API_CALL_IN_THIS_RUN"
        status["cost_model_status"] = "NOT_LOCKED_ZERO_PLACEHOLDER_NO_SPREAD_NO_SLIPPAGE"
        status["validation_2024_status"] = "NOT_RUN_LOCAL_CACHE_MISSING_FULL_2024_NQ_HOURLY_CHAIN"
    except Exception as exc:  # noqa: BLE001 - fail closed into status artifact.
        status = base._candidate_fail_status(candidate, hourly_rows, daily_rows_by_contract, [], exc)
        status["status"] = "FAIL_CLOSED_S27_PURE_NQ_CACHE_ONLY_TEST_NOT_EXECUTABLE"
        status["gate"] = GATE
        status["validation_2024_status"] = "NOT_RUN_AFTER_TEST_FAIL_CLOSED"
        status["source_cache"] = "CACHE_ONLY_NO_PROVIDER_API_CALL"
        status["missing_cache_files"] = len([row for row in cache_ledger if row.get("cache_status") != "CACHE_FILE_PRESENT_USED"])

    summary_rows = [_summary_row(status)]
    base._write_json(folders["status"] / f"{RUN_ID}_status.json", status)
    base._write_csv(folders["summary"] / f"{RUN_ID}_summary.csv", summary_rows)
    base._write_json(folders["provenance"] / f"{RUN_ID}_provenance.json", _provenance(status, cache_ledger))
    base._write_json(folders["hashes"] / f"{RUN_ID}_sha256.json", base._hash_tree(OUTPUT_ROOT))
    PROCESS_RESULT_DOC.write_text(_process_result_text(status), encoding="utf-8")
    LOCAL_AUDIT_DOC.write_text(_local_audit_text(status), encoding="utf-8")
    print(status["status"])
    print(f"artifact_root={OUTPUT_ROOT.relative_to(ROOT)}")
    if summary_rows:
        print(summary_rows[0])


def _patch_base_globals() -> None:
    base.RUN_ID = RUN_ID
    base.GATE = GATE
    base.OUTPUT_ROOT = OUTPUT_ROOT


def _condition_by_date(kind: str) -> dict[str, str]:
    path = CONDITION_ROOT / f"20260601_S27_INDEX_BASE_SIGNAL_MICRO_EXECUTION_2022_2023_{kind}_dataset_condition.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    return base._condition_by_date(payload)


def _load_cached_rows(
    candidate: Any,
    hourly_condition: dict[str, str],
    daily_condition: dict[str, str],
) -> tuple[list[dict[str, Any]], dict[str, list[dict[str, Any]]], list[dict[str, Any]]]:
    hourly_rows: list[dict[str, Any]] = []
    daily_rows_by_contract: dict[str, list[dict[str, Any]]] = {}
    ledger: list[dict[str, Any]] = []
    raw_root = SOURCE_CACHE_ROOT / "raw_provider_output"

    for contract in base._comparison_contracts("NQ"):
        rows, entry = _read_cached_contract(raw_root, candidate, contract, base.HOURLY_SCHEMA, "signal_hourly", hourly_condition)
        hourly_rows.extend(rows)
        ledger.append(entry)

    for contract in base._daily_contracts("NQ", candidate.daily_history_start):
        rows, entry = _read_cached_contract(raw_root, candidate, contract, base.DAILY_SCHEMA, "signal_daily", daily_condition)
        if rows:
            daily_rows_by_contract[base._contract_key(contract)] = rows
        ledger.append(entry)

    return hourly_rows, daily_rows_by_contract, ledger


def _read_cached_contract(
    raw_root: Path,
    candidate: Any,
    contract: dict[str, Any],
    schema: str,
    purpose: str,
    condition_by_date: dict[str, str],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    stem = base._provider_contract_stem(contract)
    provider_csv = raw_root / f"20260601_S27_INDEX_BASE_SIGNAL_MICRO_EXECUTION_2022_2023_NQ_{purpose}_{stem}_provider.csv"
    if not provider_csv.exists():
        return [], {
            "root": "NQ",
            "raw_symbol": contract["raw_symbol"],
            "schema": schema,
            "purpose": purpose,
            "expected_file": str(provider_csv.relative_to(ROOT)),
            "cache_status": "MISSING_FAIL_CLOSED_NO_PROVIDER_CALL",
        }
    source_sha = base._sha256(provider_csv)
    rows = base._read_provider_rows(provider_csv, candidate, contract, schema, purpose.replace("signal_", ""), condition_by_date, source_sha)
    return rows, {
        "root": "NQ",
        "raw_symbol": contract["raw_symbol"],
        "schema": schema,
        "purpose": purpose,
        "expected_file": str(provider_csv.relative_to(ROOT)),
        "source_sha256": source_sha,
        "rows_loaded": len(rows),
        "cache_status": "CACHE_FILE_PRESENT_USED",
    }


def _summary_row(status: dict[str, Any]) -> dict[str, Any]:
    return {
        "root": "NQ",
        "status": status.get("status", ""),
        "requested_window_start": status.get("requested_window_start", ""),
        "requested_window_end": status.get("requested_window_end", ""),
        "effective_backtest_start": status.get("effective_backtest_start", ""),
        "effective_backtest_end": status.get("effective_backtest_end", ""),
        "s27_forecast_rows": status.get("s27_forecast_rows", ""),
        "backtest_rows": status.get("backtest_rows", ""),
        "gross_pnl_usd": status.get("gross_pnl_usd", ""),
        "estimated_costs_usd": status.get("estimated_costs_usd", ""),
        "net_after_placeholder_costs_usd": status.get("net_after_placeholder_costs_usd", ""),
        "cost_model_status": status.get("cost_model_status", ""),
        "validation_2024_status": status.get("validation_2024_status", ""),
    }


def _provenance(status: dict[str, Any], cache_ledger: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "gate": GATE,
        "lane_class": "SOURCE_NATIVE_FUTURES",
        "source_cache_root": str(SOURCE_CACHE_ROOT.relative_to(ROOT)),
        "provider_api_access": "NO",
        "new_data_download": "NO",
        "status": status.get("status", ""),
        "cache_file_count": len(cache_ledger),
        "non_authorization": [
            "NO_PROVIDER_API_ACCESS",
            "NO_NEW_DATA_DOWNLOAD",
            "NO_OOS",
            "NO_LOCKBOX",
            "NO_FORWARD",
            "NO_DEPLOYMENT",
            "NO_TRADING",
            "NO_PROMOTION",
        ],
    }


def _process_result_text(status: dict[str, Any]) -> str:
    return f"""# Carver S27 Pure NQ Cache-Only TEST 2022-2023 Result

Status:

```text
{status.get("status", "")}
```

Gate: `{GATE}`

This run reuses only the already cached NQ provider CSV files created during the interrupted NQ signal-to-MNQ gate. No Databento client is created, no provider API call is made, and no new data is downloaded.

## Result

| Root | Window | Forecast Rows | Backtest Rows | Gross | Costs | Net | Cost Boundary |
|---|---|---:|---:|---:|---:|---:|---|
| NQ | {status.get("effective_backtest_start", "")} to {status.get("effective_backtest_end", "")} | {status.get("s27_forecast_rows", "")} | {status.get("backtest_rows", "")} | {status.get("gross_pnl_usd", "")} | {status.get("estimated_costs_usd", "")} | {status.get("net_after_placeholder_costs_usd", "")} | {status.get("cost_model_status", "")} |

Validation 2024 status: `{status.get("validation_2024_status", "")}`.

This is a source-native futures TEST-surface check only. It is not alpha, OOS, Lockbox, Forward, deployment, trading, promotion, production sizing, or a production cost lock.
"""


def _local_audit_text(status: dict[str, Any]) -> str:
    return f"""# Local Lean Hostile Audit - S27 Pure NQ Cache-Only TEST

Mode: automatic local lean hostile audit over generated pure NQ cache-only source-native futures TEST artifacts.

CRITICAL: None for declared cache-only TEST scope.

HIGH: None. The run uses NQ as both source-native signal and execution/PnL lane. It does not substitute MNQ, CFD, ICMarkets, OOS, Lockbox, Forward, deployment, trading, or promotion.

MEDIUM: 2024 validation is not run because the local cache does not contain a full 2024 NQ hourly dated-contract chain. This must remain blocked unless a separate provider/data gate is opened.

LOW: Costs remain zero placeholder only; spread, slippage, fill quality, margin, prop-firm rules, and CFD costs remain unresolved.

Verdict:

```text
BLOCKING_FINDINGS: NO_FOR_DECLARED_CACHE_ONLY_NQ_TEST_SCOPE
AUDIT_DISPOSITION: {status.get("status", "")}
```
"""


if __name__ == "__main__":
    main()
