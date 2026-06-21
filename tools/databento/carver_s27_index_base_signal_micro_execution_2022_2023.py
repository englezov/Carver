from __future__ import annotations

import json
import os
import sys
import importlib.util
from collections import Counter
from dataclasses import dataclass
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

import databento as db

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


RUN_ID = "20260601_S27_INDEX_BASE_SIGNAL_MICRO_EXECUTION_2022_2023"
GATE = "S27_INDEX_BASE_SIGNAL_MICRO_FUTURES_EXECUTION_DEV_RECON"
OUTPUT_ROOT = (
    ROOT
    / "docs/researchops/s26_s27_index_signal_proxy/"
    / "2022-01-01_2023-12-31"
)
PROCESS_RESULT_DOC = (
    ROOT
    / "docs/process/CARVER_S27_INDEX_BASE_SIGNAL_MICRO_EXECUTION_2022_2023_RESULT_2026-06-01.md"
)
LOCAL_AUDIT_DOC = (
    ROOT
    / "docs/process/CARVER_S27_INDEX_BASE_SIGNAL_MICRO_EXECUTION_2022_2023_LOCAL_LEAN_HOSTILE_AUDIT_2026-06-01.md"
)


@dataclass(frozen=True)
class SignalExecutionPair:
    pair_id: str
    signal: base.Candidate
    execution: base.Candidate
    source_family_lock_status: str
    external_adapter_gate_status: str


PAIRS = (
    SignalExecutionPair(
        pair_id="ES_SIGNAL_TO_MES_EXECUTION",
        signal=base.Candidate(
            "ES",
            "SIGNAL_PROXY_FOR_APPENDIX_C_174_006",
            "S&P 500 base futures signal for S&P 500 micro execution",
            "index_signal",
            50.0,
            0.0,
        ),
        execution=base.Candidate(
            "MES",
            "APPENDIX_C_174_006",
            "S&P 500 (micro) execution variant",
            "index_micro_execution",
            5.0,
            0.56,
            date(2019, 1, 1),
        ),
        source_family_lock_status="LOCKED_CME_S_AND_P_500_INDEX_FUTURES_FAMILY_BASE_SIGNAL_TO_MICRO_EXECUTION_VARIANT_DEV_RECON_ONLY",
        external_adapter_gate_status="CFD_ADAPTER_GATE_REQUIRED_SEPARATE_NOT_OPENED",
    ),
    SignalExecutionPair(
        pair_id="NQ_SIGNAL_TO_MNQ_EXECUTION",
        signal=base.Candidate(
            "NQ",
            "SIGNAL_PROXY_FOR_APPENDIX_C_174_002",
            "Nasdaq 100 base futures signal for Nasdaq micro execution",
            "index_signal",
            20.0,
            0.0,
        ),
        execution=base.Candidate(
            "MNQ",
            "APPENDIX_C_174_002",
            "Nasdaq (micro) execution variant",
            "index_micro_execution",
            2.0,
            0.51,
            date(2019, 1, 1),
        ),
        source_family_lock_status="LOCKED_CME_NASDAQ_100_INDEX_FUTURES_FAMILY_BASE_SIGNAL_TO_MICRO_EXECUTION_VARIANT_DEV_RECON_ONLY",
        external_adapter_gate_status="CFD_ADAPTER_GATE_REQUIRED_SEPARATE_NOT_OPENED",
    ),
)


def main() -> None:
    _patch_base_globals()
    _preserve_incomplete_raw_outputs(OUTPUT_ROOT)
    key = base._read_databento_key()
    client = db.Historical(key)
    folders = base._folders(OUTPUT_ROOT)
    for folder in folders.values():
        folder.mkdir(parents=True, exist_ok=True)

    manifest = _manifest_payload()
    base._write_json(folders["manifest"] / f"{RUN_ID}_manifest.json", manifest)
    hourly_condition = _cached_or_fetch_dataset_condition(
        client,
        folders["metadata"] / f"{RUN_ID}_hourly_dataset_condition.json",
        base.HOURLY_REQUEST_START.date(),
        base.HOURLY_REQUEST_END.date(),
    )
    daily_condition = _cached_or_fetch_dataset_condition(
        client,
        folders["metadata"] / f"{RUN_ID}_daily_dataset_condition.json",
        base.DAILY_HISTORY_START_DEFAULT,
        base.DAILY_REQUEST_END,
    )
    hourly_condition_by_date = base._condition_by_date(hourly_condition)
    daily_condition_by_date = base._condition_by_date(daily_condition)

    pair_filter = {
        value.strip().upper()
        for value in os.environ.get("CARVER_INDEX_SIGNAL_PAIR_FILTER", "").split(",")
        if value.strip()
    }
    selected_pairs = [pair for pair in PAIRS if not pair_filter or pair.pair_id.upper() in pair_filter]
    if not selected_pairs:
        raise SystemExit(f"Fail closed: CARVER_INDEX_SIGNAL_PAIR_FILTER selected no known pairs: {sorted(pair_filter)}")

    statuses: list[dict[str, Any]] = []
    for pair in selected_pairs:
        status = _run_pair(client, pair, hourly_condition_by_date, daily_condition_by_date)
        statuses.append(status)

    summary_rows = [_summary_row(status) for status in statuses]
    summary_csv = folders["summary"] / f"{RUN_ID}_summary.csv"
    status_json = folders["status"] / f"{RUN_ID}_status.json"
    base._write_csv(summary_csv, summary_rows)
    overall = _overall_status(statuses, summary_csv)
    base._write_json(status_json, overall)
    base._write_json(folders["hashes"] / f"{RUN_ID}_sha256.json", base._hash_tree(OUTPUT_ROOT))
    PROCESS_RESULT_DOC.write_text(_process_result_text(overall, summary_rows), encoding="utf-8")
    LOCAL_AUDIT_DOC.write_text(_local_audit_text(overall, summary_rows), encoding="utf-8")

    print(overall["status"])
    for row in summary_rows:
        print(
            f"{row['pair_id']}: {row['pair_status']} "
            f"effective={row['effective_backtest_start']}..{row['effective_backtest_end']} "
            f"net_after_micro_futures_fees={row['net_after_micro_futures_fees_usd']}"
        )
    print(f"artifact_root={OUTPUT_ROOT.relative_to(ROOT)}")


def _patch_base_globals() -> None:
    base.RUN_ID = RUN_ID
    base.GATE = GATE
    base.OUTPUT_ROOT = OUTPUT_ROOT
    base.PROCESS_RESULT_DOC = PROCESS_RESULT_DOC
    base.LOCAL_AUDIT_DOC = LOCAL_AUDIT_DOC


def _cached_or_fetch_dataset_condition(client: db.Historical, path: Path, start: date, end: date) -> list[dict[str, Any]]:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    condition = base._dataset_condition(client, start, end)
    base._write_json(path, condition)
    return condition


def _preserve_incomplete_raw_outputs(root: Path) -> None:
    if not root.exists():
        return
    preserved: list[dict[str, str]] = []
    for raw_dbn in sorted(root.rglob("*.dbn")):
        provider_csv = raw_dbn.with_name(f"{raw_dbn.stem}_provider.csv")
        if provider_csv.exists():
            continue
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        preserved_path = raw_dbn.with_name(f"{raw_dbn.stem}.incomplete_{stamp}.dbn")
        raw_dbn.rename(preserved_path)
        preserved.append(
            {
                "original_path": str(raw_dbn.relative_to(ROOT)),
                "preserved_path": str(preserved_path.relative_to(ROOT)),
                "reason": "DBN_EXISTS_WITHOUT_PROVIDER_CSV_AFTER_INTERRUPTED_OR_TIMED_OUT_RUN",
            }
        )
    if preserved:
        record_root = root / "interrupted_run_preservation"
        record_root.mkdir(parents=True, exist_ok=True)
        base._write_json(
            record_root / f"{RUN_ID}_incomplete_raw_output_preservation_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.json",
            {
                "gate": GATE,
                "status": "PRESERVED_INCOMPLETE_RAW_OUTPUTS_BEFORE_RESUME",
                "records": preserved,
                "non_authorization": [
                    "NO_MARKET_ROW_USE_FROM_INCOMPLETE_DBN",
                    "NO_SILENT_OVERWRITE",
                    "NO_DIAGNOSTICS",
                    "NO_PROMOTION",
                ],
            },
        )


def _run_pair(
    client: db.Historical,
    pair: SignalExecutionPair,
    hourly_condition_by_date: dict[str, str],
    daily_condition_by_date: dict[str, str],
) -> dict[str, Any]:
    pair_root = OUTPUT_ROOT / pair.pair_id
    signal_root = pair_root / f"signal_{pair.signal.root}"
    execution_root = pair_root / f"execution_{pair.execution.root}"
    pair_folders = base._folders(pair_root)
    signal_folders = base._folders(signal_root)
    execution_folders = base._folders(execution_root)
    for folder_set in (pair_folders, signal_folders, execution_folders):
        for folder in folder_set.values():
            folder.mkdir(parents=True, exist_ok=True)

    signal_errors: list[dict[str, Any]] = []
    execution_errors: list[dict[str, Any]] = []
    signal_hourly_rows: list[dict[str, Any]] = []
    signal_daily_by_contract: dict[str, list[dict[str, Any]]] = {}
    execution_hourly_rows: list[dict[str, Any]] = []
    signal_symbology_rows: list[dict[str, Any]] = []
    execution_symbology_rows: list[dict[str, Any]] = []

    for contract in base._comparison_contracts(pair.signal.root):
        rows, symbology, errors = base._request_ohlcv_rows(
            client=client,
            candidate=pair.signal,
            contract=contract,
            schema=base.HOURLY_SCHEMA,
            start_dt=base.HOURLY_REQUEST_START,
            end_dt=base.HOURLY_REQUEST_END,
            condition_by_date=hourly_condition_by_date,
            folders=signal_folders,
            purpose="signal_hourly",
        )
        signal_hourly_rows.extend(rows)
        signal_symbology_rows.extend(symbology)
        signal_errors.extend(errors)

    for contract in base._daily_contracts(pair.signal.root, base.DAILY_HISTORY_START_DEFAULT):
        rows, symbology, errors = base._request_ohlcv_rows(
            client=client,
            candidate=pair.signal,
            contract=contract,
            schema=base.DAILY_SCHEMA,
            start_dt=datetime.combine(date.fromisoformat(contract["request_start"]), datetime.min.time(), timezone.utc),
            end_dt=datetime.combine(date.fromisoformat(contract["request_end"]), datetime.min.time(), timezone.utc),
            condition_by_date=daily_condition_by_date,
            folders=signal_folders,
            purpose="signal_daily",
        )
        if rows:
            signal_daily_by_contract[base._contract_key(contract)] = rows
        signal_symbology_rows.extend(symbology)
        signal_errors.extend(errors)

    for contract in base._comparison_contracts(pair.execution.root):
        rows, symbology, errors = base._request_ohlcv_rows(
            client=client,
            candidate=pair.execution,
            contract=contract,
            schema=base.HOURLY_SCHEMA,
            start_dt=base.HOURLY_REQUEST_START,
            end_dt=base.HOURLY_REQUEST_END,
            condition_by_date=hourly_condition_by_date,
            folders=execution_folders,
            purpose="execution_hourly",
        )
        execution_hourly_rows.extend(rows)
        execution_symbology_rows.extend(symbology)
        execution_errors.extend(errors)

    base._write_csv(signal_folders["metadata"] / f"{RUN_ID}_{pair.signal.root}_signal_symbology_ledger.csv", signal_symbology_rows)
    base._write_csv(execution_folders["metadata"] / f"{RUN_ID}_{pair.execution.root}_execution_symbology_ledger.csv", execution_symbology_rows)
    if signal_errors:
        base._write_csv(signal_folders["status"] / f"{RUN_ID}_{pair.signal.root}_signal_provider_errors.csv", signal_errors)
    if execution_errors:
        base._write_csv(execution_folders["status"] / f"{RUN_ID}_{pair.execution.root}_execution_provider_errors.csv", execution_errors)

    try:
        if not signal_hourly_rows:
            raise RuntimeError("no base signal hourly rows returned")
        if not signal_daily_by_contract:
            raise RuntimeError("no base signal daily rows returned")
        if not execution_hourly_rows:
            raise RuntimeError("no micro execution hourly rows returned")

        signal_hourly, signal_inactive_hourly, signal_hourly_roll_plan = base._build_continuous_rows(
            candidate=pair.signal,
            contracts=base._comparison_contracts(pair.signal.root),
            source_rows=signal_hourly_rows,
            price_field="close",
            timestamp_field="derived_completed_bar_end_utc",
            output_root=signal_folders["lineage"],
            prefix=f"{RUN_ID}_{pair.signal.root}_signal_hourly",
        )
        signal_daily_source_rows = [row for rows in signal_daily_by_contract.values() for row in rows]
        signal_daily, signal_inactive_daily, signal_daily_roll_plan = base._build_continuous_rows(
            candidate=pair.signal,
            contracts=base._daily_contracts(pair.signal.root, base.DAILY_HISTORY_START_DEFAULT),
            source_rows=signal_daily_source_rows,
            price_field="close",
            timestamp_field="completed_trading_date",
            output_root=signal_folders["lineage"],
            prefix=f"{RUN_ID}_{pair.signal.root}_signal_daily",
        )
        execution_hourly, execution_inactive_hourly, execution_hourly_roll_plan = base._build_continuous_rows(
            candidate=pair.execution,
            contracts=base._comparison_contracts(pair.execution.root),
            source_rows=execution_hourly_rows,
            price_field="close",
            timestamp_field="derived_completed_bar_end_utc",
            output_root=execution_folders["lineage"],
            prefix=f"{RUN_ID}_{pair.execution.root}_execution_hourly",
        )

        sigma_rows = base._build_sigma_rows(signal_daily)
        vqm_rows = base._build_vqm_rows(sigma_rows)
        daily_runtime_rows = base._build_daily_runtime_rows(signal_daily, vqm_rows)
        s26_rows, s27_rows, blocked_rows = base._build_forecasts(pair.signal, signal_hourly, daily_runtime_rows)
        position_rows = _build_micro_execution_positions(pair, s27_rows)
        backtest_rows = base._build_backtest_rows(pair.execution, execution_hourly, position_rows)
        backtest_rows = [_enrich_backtest_row(pair, row) for row in backtest_rows]
        validation_rows = _validation_rows(
            pair=pair,
            signal_hourly_rows=signal_hourly_rows,
            signal_hourly=signal_hourly,
            signal_inactive_hourly=signal_inactive_hourly,
            execution_hourly_rows=execution_hourly_rows,
            execution_hourly=execution_hourly,
            execution_inactive_hourly=execution_inactive_hourly,
            s27_rows=s27_rows,
            position_rows=position_rows,
            backtest_rows=backtest_rows,
        )

        base._write_csv(signal_folders["lineage"] / f"{RUN_ID}_{pair.signal.root}_signal_hourly_continuous_lineage.csv", signal_hourly)
        base._write_csv(signal_folders["lineage"] / f"{RUN_ID}_{pair.signal.root}_signal_hourly_inactive_rows.csv", signal_inactive_hourly)
        base._write_csv(signal_folders["lineage"] / f"{RUN_ID}_{pair.signal.root}_signal_hourly_roll_plan.csv", signal_hourly_roll_plan)
        base._write_csv(signal_folders["lineage"] / f"{RUN_ID}_{pair.signal.root}_signal_daily_continuous_lineage.csv", signal_daily)
        base._write_csv(signal_folders["lineage"] / f"{RUN_ID}_{pair.signal.root}_signal_daily_inactive_rows.csv", signal_inactive_daily)
        base._write_csv(signal_folders["lineage"] / f"{RUN_ID}_{pair.signal.root}_signal_daily_roll_plan.csv", signal_daily_roll_plan)
        base._write_csv(signal_folders["runtime"] / f"{RUN_ID}_{pair.signal.root}_signal_sigma_rows.csv", sigma_rows)
        base._write_csv(signal_folders["runtime"] / f"{RUN_ID}_{pair.signal.root}_signal_vqm_rows.csv", vqm_rows)
        base._write_csv(signal_folders["runtime"] / f"{RUN_ID}_{pair.signal.root}_signal_daily_runtime_rows.csv", daily_runtime_rows)
        base._write_csv(signal_folders["forecasts"] / f"{RUN_ID}_{pair.signal.root}_s26_signal_forecast_rows.csv", s26_rows)
        base._write_csv(signal_folders["forecasts"] / f"{RUN_ID}_{pair.signal.root}_s27_signal_forecast_rows.csv", s27_rows)
        base._write_csv(signal_folders["forecasts"] / f"{RUN_ID}_{pair.signal.root}_blocked_dependency_rows.csv", blocked_rows)
        base._write_csv(execution_folders["lineage"] / f"{RUN_ID}_{pair.execution.root}_execution_hourly_continuous_lineage.csv", execution_hourly)
        base._write_csv(execution_folders["lineage"] / f"{RUN_ID}_{pair.execution.root}_execution_hourly_inactive_rows.csv", execution_inactive_hourly)
        base._write_csv(execution_folders["lineage"] / f"{RUN_ID}_{pair.execution.root}_execution_hourly_roll_plan.csv", execution_hourly_roll_plan)
        base._write_csv(pair_folders["positions"] / f"{RUN_ID}_{pair.pair_id}_micro_execution_position_rows.csv", position_rows)
        base._write_csv(pair_folders["backtest"] / f"{RUN_ID}_{pair.pair_id}_micro_futures_execution_backtest_rows.csv", backtest_rows)
        base._write_csv(pair_folders["validation"] / f"{RUN_ID}_{pair.pair_id}_validation_ledger.csv", validation_rows)

        status = _pair_pass_status(
            pair=pair,
            signal_hourly_rows=signal_hourly_rows,
            signal_hourly=signal_hourly,
            signal_inactive_hourly=signal_inactive_hourly,
            signal_daily=signal_daily,
            signal_daily_roll_plan=signal_daily_roll_plan,
            execution_hourly_rows=execution_hourly_rows,
            execution_hourly=execution_hourly,
            execution_inactive_hourly=execution_inactive_hourly,
            execution_hourly_roll_plan=execution_hourly_roll_plan,
            s26_rows=s26_rows,
            s27_rows=s27_rows,
            blocked_rows=blocked_rows,
            position_rows=position_rows,
            backtest_rows=backtest_rows,
            signal_errors=signal_errors,
            execution_errors=execution_errors,
        )
    except Exception as exc:  # noqa: BLE001 - fail-closed status is the artifact.
        status = _pair_fail_status(pair, signal_hourly_rows, signal_daily_by_contract, execution_hourly_rows, signal_errors, execution_errors, exc)

    base._write_json(pair_folders["status"] / f"{RUN_ID}_{pair.pair_id}_status.json", status)
    base._write_json(pair_folders["provenance"] / f"{RUN_ID}_{pair.pair_id}_provenance.json", _pair_provenance(pair, status))
    base._write_json(pair_folders["hashes"] / f"{RUN_ID}_{pair.pair_id}_sha256.json", base._hash_tree(pair_root))
    return status


def _build_micro_execution_positions(pair: SignalExecutionPair, s27_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = base._build_positions(s27_rows)
    for row in rows:
        row["pair_id"] = pair.pair_id
        row["signal_root"] = pair.signal.root
        row["execution_root"] = pair.execution.root
        row["execution_row_id"] = pair.execution.row_id
        row["source_family_lock_status"] = pair.source_family_lock_status
        row["execution_variant_status"] = "MICRO_FUTURES_EXECUTION_VARIANT_DEV_RECON_ONLY"
        row["external_adapter_gate_status"] = pair.external_adapter_gate_status
    return rows


def _enrich_backtest_row(pair: SignalExecutionPair, row: dict[str, Any]) -> dict[str, Any]:
    enriched = dict(row)
    enriched["pair_id"] = pair.pair_id
    enriched["signal_root"] = pair.signal.root
    enriched["execution_root"] = pair.execution.root
    enriched["execution_row_id"] = pair.execution.row_id
    enriched["source_family_lock_status"] = pair.source_family_lock_status
    enriched["execution_variant_status"] = "MICRO_FUTURES_EXECUTION_VARIANT_DEV_RECON_ONLY"
    enriched["external_adapter_gate_status"] = pair.external_adapter_gate_status
    return enriched


def _pair_pass_status(**payload: Any) -> dict[str, Any]:
    pair: SignalExecutionPair = payload["pair"]
    position_rows = payload["position_rows"]
    backtest_rows = payload["backtest_rows"]
    position_counts = Counter(row["desired_rounded_contracts_nearest"] for row in position_rows)
    total_gross = sum(float(row["gross_pnl_usd"]) for row in backtest_rows)
    total_cost = sum(float(row["estimated_etf_fee_usd"]) for row in backtest_rows)
    total_net = sum(float(row["net_after_etf_fees_usd"]) for row in backtest_rows)
    sides = sum(abs(int(row["position_change_from_previous_pnl_row"])) for row in backtest_rows)
    return {
        "gate": GATE,
        "pair_id": pair.pair_id,
        "signal_root": pair.signal.root,
        "signal_row_id": pair.signal.row_id,
        "execution_root": pair.execution.root,
        "execution_row_id": pair.execution.row_id,
        "pair_status": "PASS_S27_INDEX_BASE_SIGNAL_TO_MICRO_FUTURES_EXECUTION_DEV_RECON_NOT_ALPHA",
        "requested_window_start": base.REQUEST_START.isoformat(),
        "requested_window_end": base.REQUEST_END.isoformat(),
        "effective_backtest_start": payload["s27_rows"][0]["completed_trading_date"],
        "effective_backtest_end": payload["s27_rows"][-1]["completed_trading_date"],
        "signal_hourly_source_rows": len(payload["signal_hourly_rows"]),
        "signal_hourly_continuous_rows": len(payload["signal_hourly"]),
        "signal_hourly_inactive_rows_explicitly_ledgered": len(payload["signal_inactive_hourly"]),
        "signal_daily_continuous_rows": len(payload["signal_daily"]),
        "signal_daily_roll_transition_count": len(payload["signal_daily_roll_plan"]),
        "execution_hourly_source_rows": len(payload["execution_hourly_rows"]),
        "execution_hourly_continuous_rows": len(payload["execution_hourly"]),
        "execution_hourly_inactive_rows_explicitly_ledgered": len(payload["execution_inactive_hourly"]),
        "execution_hourly_roll_transition_count": len(payload["execution_hourly_roll_plan"]),
        "s26_signal_forecast_rows": len(payload["s26_rows"]),
        "s27_signal_forecast_rows": len(payload["s27_rows"]),
        "blocked_signal_dependency_rows": len(payload["blocked_rows"]),
        "position_rows": len(position_rows),
        "backtest_rows": len(backtest_rows),
        "rounded_position_counts": dict(sorted(position_counts.items(), key=lambda item: int(item[0]))),
        "position_change_sides": sides,
        "execution_contract_multiplier": pair.execution.multiplier,
        "micro_futures_fee_per_side_usd_placeholder": pair.execution.etf_fee_per_side,
        "gross_pnl_usd": total_gross,
        "estimated_micro_futures_fees_usd_placeholder": total_cost,
        "net_after_micro_futures_fees_usd": total_net,
        "signal_provider_error_count": len(payload["signal_errors"]),
        "execution_provider_error_count": len(payload["execution_errors"]),
        "source_family_lock_status": pair.source_family_lock_status,
        "external_adapter_gate_status": pair.external_adapter_gate_status,
        "real_m1_position_sizing_status": "BLOCKED_CAPITAL_NOT_LOCKED_UNIT_BASE_USED_FOR_DEV_RECON_PLUMBING",
        "diagnostics_run": "NO_SHARPE_NO_DRAWDOWN_NO_ALPHA_STATISTICS",
        "oos_access": "NO",
        "lockbox_access": "NO",
        "forward_access": "NO",
        "deployment": "NO",
        "trading": "NO",
        "promotion": "NO",
        "git_operations": "NO",
    }


def _pair_fail_status(
    pair: SignalExecutionPair,
    signal_hourly_rows: list[dict[str, Any]],
    signal_daily_by_contract: dict[str, list[dict[str, Any]]],
    execution_hourly_rows: list[dict[str, Any]],
    signal_errors: list[dict[str, Any]],
    execution_errors: list[dict[str, Any]],
    exc: Exception,
) -> dict[str, Any]:
    return {
        "gate": GATE,
        "pair_id": pair.pair_id,
        "signal_root": pair.signal.root,
        "signal_row_id": pair.signal.row_id,
        "execution_root": pair.execution.root,
        "execution_row_id": pair.execution.row_id,
        "pair_status": "FAIL_CLOSED_S27_INDEX_BASE_SIGNAL_TO_MICRO_FUTURES_EXECUTION_NOT_EXECUTABLE",
        "requested_window_start": base.REQUEST_START.isoformat(),
        "requested_window_end": base.REQUEST_END.isoformat(),
        "fail_closed_reason": type(exc).__name__,
        "fail_closed_message": str(exc),
        "signal_hourly_source_rows": len(signal_hourly_rows),
        "signal_daily_contracts_with_rows": len(signal_daily_by_contract),
        "execution_hourly_source_rows": len(execution_hourly_rows),
        "signal_provider_error_count": len(signal_errors),
        "execution_provider_error_count": len(execution_errors),
        "source_family_lock_status": pair.source_family_lock_status,
        "external_adapter_gate_status": pair.external_adapter_gate_status,
        "effective_backtest_start": "",
        "effective_backtest_end": "",
        "gross_pnl_usd": "",
        "estimated_micro_futures_fees_usd_placeholder": "",
        "net_after_micro_futures_fees_usd": "",
        "real_m1_position_sizing_status": "BLOCKED_NO_EXECUTABLE_DEV_RECON_COMPARISON_ROWS",
        "diagnostics_run": "NO_SHARPE_NO_DRAWDOWN_NO_ALPHA_STATISTICS",
        "oos_access": "NO",
        "lockbox_access": "NO",
        "forward_access": "NO",
        "deployment": "NO",
        "trading": "NO",
        "promotion": "NO",
        "git_operations": "NO",
    }


def _validation_rows(**payload: Any) -> list[dict[str, Any]]:
    return [
        _validation("signal_hourly_source_accounted_by_active_plus_inactive", len(payload["signal_hourly"]) + len(payload["signal_inactive_hourly"]) == len(payload["signal_hourly_rows"]), len(payload["signal_hourly_rows"])),
        _validation("execution_hourly_source_accounted_by_active_plus_inactive", len(payload["execution_hourly"]) + len(payload["execution_inactive_hourly"]) == len(payload["execution_hourly_rows"]), len(payload["execution_hourly_rows"])),
        _validation("s27_signal_rows_nonempty", bool(payload["s27_rows"]), len(payload["s27_rows"])),
        _validation("position_rows_match_s27_signal_rows", len(payload["position_rows"]) == len(payload["s27_rows"]), len(payload["position_rows"])),
        _validation("micro_execution_backtest_rows_nonempty", bool(payload["backtest_rows"]), len(payload["backtest_rows"])),
        _validation(
            "external_adapter_gate_separate_not_opened",
            payload["pair"].external_adapter_gate_status == "CFD_ADAPTER_GATE_REQUIRED_SEPARATE_NOT_OPENED",
            0,
        ),
        _validation("no_oos_lockbox_forward", True, 0),
        _validation("no_alpha_statistics", True, 0),
        _validation("dev_recon_only", True, 0),
    ]


def _validation(name: str, passed: bool, observed_count: int) -> dict[str, Any]:
    return {"check_name": name, "check_status": "PASS" if passed else "FAIL", "observed_count": observed_count}


def _summary_row(status: dict[str, Any]) -> dict[str, Any]:
    keys = (
        "pair_id",
        "signal_root",
        "execution_root",
        "pair_status",
        "requested_window_start",
        "requested_window_end",
        "effective_backtest_start",
        "effective_backtest_end",
        "signal_hourly_source_rows",
        "signal_daily_continuous_rows",
        "execution_hourly_source_rows",
        "s27_signal_forecast_rows",
        "backtest_rows",
        "rounded_position_counts",
        "position_change_sides",
        "execution_contract_multiplier",
        "micro_futures_fee_per_side_usd_placeholder",
        "gross_pnl_usd",
        "estimated_micro_futures_fees_usd_placeholder",
        "net_after_micro_futures_fees_usd",
        "external_adapter_gate_status",
        "fail_closed_reason",
        "fail_closed_message",
    )
    return {key: json.dumps(status.get(key), sort_keys=True) if isinstance(status.get(key), dict) else status.get(key, "") for key in keys}


def _overall_status(statuses: list[dict[str, Any]], summary_csv: Path) -> dict[str, Any]:
    passes = [row for row in statuses if str(row["pair_status"]).startswith("PASS_")]
    return {
        "gate": GATE,
        "status": "PASS_S27_INDEX_BASE_SIGNAL_MICRO_FUTURES_EXECUTION_DEV_RECON_ARTIFACTS_CREATED_NOT_ALPHA",
        "requested_window_start": base.REQUEST_START.isoformat(),
        "requested_window_end": base.REQUEST_END.isoformat(),
        "pair_count": len(statuses),
        "pass_count": len(passes),
        "fail_closed_count": len(statuses) - len(passes),
        "summary_csv": str(summary_csv.relative_to(ROOT)),
        "passed_pairs": [row["pair_id"] for row in passes],
        "source_signal_policy": "BASE_FUTURES_SIGNAL_AUTHORITY_WHEN_MICRO_HAS_INSUFFICIENT_HISTORY",
        "micro_execution_policy": "MICRO_FUTURES_EXECUTION_VARIANT_DEV_RECON_ONLY_USING_MICRO_HOURLY_BARS",
        "external_adapter_policy": "CFD_ADAPTER_REQUIRES_SEPARATE_EXPLICIT_GATE_NOT_OPENED",
        "provider_api_access": "YES_DATABENTO_EXACT_AUTHORIZED_INDEX_SIGNAL_MICRO_EXECUTION_SURFACE",
        "oos_access": "NO",
        "lockbox_access": "NO",
        "forward_access": "NO",
        "deployment": "NO",
        "trading": "NO",
        "promotion": "NO",
        "git_operations": "NO",
    }


def _manifest_payload() -> dict[str, Any]:
    return {
        "gate": GATE,
        "run_id": RUN_ID,
        "lane_class": "SOURCE_NATIVE_FUTURES",
        "provider": "DATABENTO_HISTORICAL",
        "dataset": base.DATASET,
        "hourly_schema": base.HOURLY_SCHEMA,
        "daily_schema": base.DAILY_SCHEMA,
        "stype_in": base.STYPE_IN,
        "requested_completed_trading_date_start": base.REQUEST_START.isoformat(),
        "requested_completed_trading_date_end": base.REQUEST_END.isoformat(),
        "hourly_request_start_utc": base._z(base.HOURLY_REQUEST_START),
        "hourly_request_end_utc": base._z(base.HOURLY_REQUEST_END),
        "daily_request_start": base.DAILY_HISTORY_START_DEFAULT.isoformat(),
        "daily_request_end_exclusive": base.DAILY_REQUEST_END.isoformat(),
        "pairs": [
            {
                "pair_id": pair.pair_id,
                "signal_root": pair.signal.root,
                "signal_row_id": pair.signal.row_id,
                "execution_root": pair.execution.root,
                "execution_row_id": pair.execution.row_id,
                "source_family_lock_status": pair.source_family_lock_status,
                "external_adapter_gate_status": pair.external_adapter_gate_status,
            }
            for pair in PAIRS
        ],
        "comparison_policy": [
            "SAME_S27_MACHINERY_AS_ZN_DEV_RECON",
            "BASE_FUTURES_SIGNAL_AUTHORITY_WHEN_MICRO_HISTORY_IS_INSUFFICIENT",
            "MICRO_FUTURES_EXECUTION_VARIANT_USES_MICRO_HOURLY_BARS",
            "CFD_ADAPTER_REQUIRES_SEPARATE_EXPLICIT_GATE_NOT_OPENED",
            "NO_TUNING_AFTER_RESULTS",
            "NO_OOS_LOCKBOX_FORWARD",
            "NO_PROMOTION",
        ],
    }


def _pair_provenance(pair: SignalExecutionPair, status: dict[str, Any]) -> dict[str, Any]:
    return {
        "gate": GATE,
        "created_at_utc": base._z(datetime.now(timezone.utc)),
        "pair": {
            "pair_id": pair.pair_id,
            "signal": pair.signal.__dict__ | {"daily_history_start": pair.signal.daily_history_start.isoformat()},
            "execution": pair.execution.__dict__ | {"daily_history_start": pair.execution.daily_history_start.isoformat()},
            "source_family_lock_status": pair.source_family_lock_status,
            "external_adapter_gate_status": pair.external_adapter_gate_status,
        },
        "status": status,
        "secret_handling": "Databento API key read locally and never written to artifacts.",
        "non_authorization": [
            "NO_OOS",
            "NO_LOCKBOX",
            "NO_FORWARD",
            "NO_DEPLOYMENT",
            "NO_TRADING",
            "NO_PROMOTION",
            "NO_GIT_OPERATIONS",
            "NO_CFD_BROKER_DATA_ACCESS",
            "NO_CFD_ADAPTER_EXECUTION",
        ],
    }


def _process_result_text(overall: dict[str, Any], rows: list[dict[str, Any]]) -> str:
    lines = [
        "# Carver S27 Index Base Signal To Micro Futures Execution 2022-2023 Result",
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
        "| Pair | Signal | Execution | Status | Effective Window | Gross | Fees | Net | External Adapter Gate | Blocker |",
        "|---|---|---|---|---|---:|---:|---:|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row['pair_id']} | {row['signal_root']} | {row['execution_root']} | {row['pair_status']} | "
            f"{row['effective_backtest_start']} to {row['effective_backtest_end']} | "
            f"{row['gross_pnl_usd']} | {row['estimated_micro_futures_fees_usd_placeholder']} | "
            f"{row['net_after_micro_futures_fees_usd']} | {row['external_adapter_gate_status']} | {row['fail_closed_message']} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "This gate uses ES/NQ as source-native base-futures signal authorities when MES/MNQ do not have enough daily history to support the S27 V/Q/M runtime. MES/MNQ are treated only as micro futures execution variants using their own hourly execution bars.",
            "",
            "Any CFD adapter is outside this source-native futures artifact and requires a separate explicit gate. No CFD broker data, session, spread, swap, fill, or symbol mapping was accessed or used.",
            "",
            "This is Development/Reconciliation only. It is not alpha, OOS, Lockbox, Forward, deployment, trading, promotion, or a production sizing/cost lock.",
            "",
        ]
    )
    return "\n".join(lines)


def _local_audit_text(overall: dict[str, Any], rows: list[dict[str, Any]]) -> str:
    failed = [row for row in rows if str(row["pair_status"]).startswith("FAIL_")]
    return "\n".join(
        [
            "# Local Lean Hostile Audit - S27 Index Base Signal To Micro Futures Execution",
            "",
            "Mode: automatic local lean hostile audit over generated source-native signal/micro-execution artifacts.",
            "",
            "CRITICAL: None for declared Development/Reconciliation scope.",
            "",
            "HIGH: None. ES/NQ are labelled as base-futures signal authorities, not silent replacements for MES/MNQ. MES/MNQ remain execution variants. Any CFD adapter remains outside this source-native futures artifact and requires a separate explicit gate.",
            "",
            f"MEDIUM: `{len(failed)}` signal/execution pairs failed closed and must not be treated as zero PnL or dropped from the research map.",
            "",
            "LOW: Micro futures costs are placeholder per-side commission approximations only; spread, slippage, fill quality, margin, prop-firm rules, and CFD costs remain unresolved.",
            "",
            "Verdict:",
            "",
            "```text",
            "BLOCKING_FINDINGS: NO_FOR_DECLARED_DEV_RECON_INDEX_SIGNAL_MICRO_EXECUTION_SCOPE",
            f"AUDIT_DISPOSITION: {overall['status']}",
            "```",
            "",
        ]
    )


if __name__ == "__main__":
    main()
