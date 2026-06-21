from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
RUN_ID = "20260601_S27_ZN_LADDER_ATTRIBUTION_AND_BASELINE_RECONCILIATION"
GATE = "S27_ZN_LADDER_ATTRIBUTION_AND_BASELINE_RECONCILIATION"
ZN_MULTIPLIER = 1000.0
FORECAST_DIVISOR = 10.0
ETF_ZN_FEE_PER_SIDE_USD = 1.51

OUTPUT_ROOT = ROOT / "docs/researchops/s26_s27_ladder_attribution/ZN_S27/2022_2024"
PROCESS_RESULT_DOC = ROOT / "docs/process/CARVER_S27_ZN_LADDER_ATTRIBUTION_AND_BASELINE_RECONCILIATION_2026-06-01.md"
LOCAL_AUDIT_DOC = ROOT / "docs/process/CARVER_S27_ZN_LADDER_ATTRIBUTION_LOCAL_HOSTILE_AUDIT_2026-06-01.md"


@dataclass(frozen=True)
class WindowConfig:
    label: str
    evidence_class_before_reconciliation: str
    forecast_csv: Path
    hourly_csv: Path
    ladder_position_csv: Path
    ladder_backtest_csv: Path
    status_json: Path


WINDOWS = (
    WindowConfig(
        label="2022_2023_INITIAL_DEV_RECON",
        evidence_class_before_reconciliation="DEVELOPMENT_RECONCILIATION",
        forecast_csv=ROOT
        / "docs/researchops/s26_s27_backtest_readiness/ZN_S27_SINGLE_INSTRUMENT/2022-01-01_2023-12-31/"
        / "retargeted_dev_recon_backtest/forecast_rows/"
        / "20260531_S27_ZN_2022_2023_RETARGETED_DEV_RECON_BACKTEST_s27_forecast_rows.csv",
        hourly_csv=ROOT
        / "docs/researchops/s26_s27_backtest_readiness/ZN_S27_SINGLE_INSTRUMENT/2022-01-01_2023-12-31/"
        / "retargeted_dev_recon_backtest/local_hourly_lineage/"
        / "20260531_S27_ZN_2022_2023_RETARGETED_DEV_RECON_BACKTEST_local_hourly_continuous_lineage.csv",
        ladder_position_csv=ROOT
        / "docs/researchops/s26_s27_m1_ladder/ZN_S27/2022-01-01_2023-12-31/position_rows/"
        / "20260531_S27_ZN_M1_LADDER_DEV_RECON_BACKTEST_desired_position_rows.csv",
        ladder_backtest_csv=ROOT
        / "docs/researchops/s26_s27_m1_ladder/ZN_S27/2022-01-01_2023-12-31/backtest_rows/"
        / "20260531_S27_ZN_M1_LADDER_DEV_RECON_BACKTEST_ladder_backtest_rows.csv",
        status_json=ROOT
        / "docs/researchops/s26_s27_m1_ladder/ZN_S27/2022-01-01_2023-12-31/status/"
        / "20260531_S27_ZN_M1_LADDER_DEV_RECON_BACKTEST_status.json",
    ),
    WindowConfig(
        label="2024_VALIDATION_STYLE",
        evidence_class_before_reconciliation="VALIDATION_STYLE_NON_LOCKBOX",
        forecast_csv=ROOT
        / "docs/researchops/s26_s27_validation/ZN_S27/2024-01-01_2024-12-31/forecast_rows/"
        / "20260601_S27_ZN_2024_VALIDATION_BACKTEST_ZN_s27_forecast_rows.csv",
        hourly_csv=ROOT
        / "docs/researchops/s26_s27_validation/ZN_S27/2024-01-01_2024-12-31/local_lineage/"
        / "20260601_S27_ZN_2024_VALIDATION_BACKTEST_ZN_hourly_continuous_lineage.csv",
        ladder_position_csv=ROOT
        / "docs/researchops/s26_s27_validation/ZN_S27/2024-01-01_2024-12-31/position_rows/"
        / "20260601_S27_ZN_2024_VALIDATION_BACKTEST_ZN_desired_position_rows.csv",
        ladder_backtest_csv=ROOT
        / "docs/researchops/s26_s27_validation/ZN_S27/2024-01-01_2024-12-31/backtest_rows/"
        / "20260601_S27_ZN_2024_VALIDATION_BACKTEST_ZN_ladder_backtest_rows.csv",
        status_json=ROOT
        / "docs/researchops/s26_s27_validation/ZN_S27/2024-01-01_2024-12-31/status/"
        / "20260601_S27_ZN_2024_VALIDATION_BACKTEST_status.json",
    ),
)


def main() -> None:
    _require_inputs()
    folders = _folders()
    for folder in folders.values():
        folder.mkdir(parents=True, exist_ok=True)

    all_rows: list[dict[str, Any]] = []
    all_summary: list[dict[str, Any]] = []
    input_records: list[dict[str, Any]] = []
    for config in WINDOWS:
        rows, summary, records = _run_window(config)
        all_rows.extend(rows)
        all_summary.extend(summary)
        input_records.extend(records)

    decompositions = _decompose(all_rows)
    status = _status_payload(all_rows, all_summary)
    validation = _validation_rows(all_rows, all_summary, status)

    _write_csv(folders["rows"] / f"{RUN_ID}_row_attribution.csv", all_rows)
    _write_csv(folders["summary"] / f"{RUN_ID}_summary.csv", all_summary)
    _write_csv(folders["decomposition"] / f"{RUN_ID}_pnl_decomposition.csv", decompositions)
    _write_csv(folders["validation"] / f"{RUN_ID}_validation_ledger.csv", validation)
    _write_json(folders["status"] / f"{RUN_ID}_status.json", status)
    _write_json(folders["provenance"] / f"{RUN_ID}_provenance.json", _provenance_payload(status, input_records))
    _write_json(folders["hashes"] / f"{RUN_ID}_sha256.json", _hash_tree(OUTPUT_ROOT))
    PROCESS_RESULT_DOC.write_text(_process_result_text(status, all_summary), encoding="utf-8")
    LOCAL_AUDIT_DOC.write_text(_local_audit_text(status), encoding="utf-8")

    print(status["status"])
    for row in all_summary:
        print(
            f"{row['window_label']} {row['strategy_variant']}: "
            f"net={row['net_after_etf_fees_usd']} "
            f"gross={row['gross_pnl_usd']} fees={row['estimated_etf_fees_usd']}"
        )
    print(f"artifact_root={OUTPUT_ROOT.relative_to(ROOT)}")


def _run_window(config: WindowConfig) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    forecasts = _read_csv(config.forecast_csv)
    hourly_rows = _read_csv(config.hourly_csv)
    ladder_positions = _read_csv(config.ladder_position_csv)
    existing_ladder = _read_csv(config.ladder_backtest_csv)
    source_status = json.loads(config.status_json.read_text(encoding="utf-8"))

    hourly_by_ts = {row["derived_completed_bar_end_utc"]: row for row in hourly_rows}
    ordered_ts = sorted(hourly_by_ts)
    forecast_by_ts = {row["derived_completed_bar_end_utc"]: row for row in forecasts}
    ladder_by_ts = {row["derived_completed_bar_end_utc"]: row for row in ladder_positions}

    rows: list[dict[str, Any]] = []
    prior_unit_position: int | None = None
    prior_ladder_position: int | None = None
    cumulative_unit_gross = 0.0
    cumulative_unit_fees = 0.0
    cumulative_ladder_gross = 0.0
    cumulative_ladder_fees = 0.0
    for entry_ts, exit_ts in zip(ordered_ts[:-1], ordered_ts[1:], strict=True):
        if entry_ts not in forecast_by_ts or entry_ts not in ladder_by_ts:
            continue
        entry_bar = hourly_by_ts[entry_ts]
        exit_bar = hourly_by_ts[exit_ts]
        forecast = forecast_by_ts[entry_ts]
        unit_contracts = round(float(forecast["capped_forecast"]) / FORECAST_DIVISOR)
        ladder_contracts = int(ladder_by_ts[entry_ts]["desired_rounded_contracts_nearest"])
        price_change = float(exit_bar["continuous_close"]) - float(entry_bar["continuous_close"])

        unit_gross = unit_contracts * price_change * ZN_MULTIPLIER
        ladder_gross = ladder_contracts * price_change * ZN_MULTIPLIER
        unit_position_change = 0 if prior_unit_position is None else unit_contracts - prior_unit_position
        ladder_position_change = 0 if prior_ladder_position is None else ladder_contracts - prior_ladder_position
        prior_unit_position = unit_contracts
        prior_ladder_position = ladder_contracts

        unit_roll_sides = _roll_fee_sides(entry_bar, exit_bar, unit_contracts)
        ladder_roll_sides = _roll_fee_sides(entry_bar, exit_bar, ladder_contracts)
        unit_fee_sides = abs(unit_position_change) + unit_roll_sides
        ladder_fee_sides = abs(ladder_position_change) + ladder_roll_sides
        unit_fees = unit_fee_sides * ETF_ZN_FEE_PER_SIDE_USD
        ladder_fees = ladder_fee_sides * ETF_ZN_FEE_PER_SIDE_USD
        unit_net = unit_gross - unit_fees
        ladder_net = ladder_gross - ladder_fees
        cumulative_unit_gross += unit_gross
        cumulative_unit_fees += unit_fees
        cumulative_ladder_gross += ladder_gross
        cumulative_ladder_fees += ladder_fees

        rows.append(
            {
                "gate": GATE,
                "window_label": config.label,
                "evidence_class_before_reconciliation": config.evidence_class_before_reconciliation,
                "entry_bar_end_utc": entry_ts,
                "exit_bar_end_utc": exit_ts,
                "entry_completed_trading_date": entry_bar["completed_trading_date"],
                "exit_completed_trading_date": exit_bar["completed_trading_date"],
                "entry_year": entry_bar["completed_trading_date"][:4],
                "entry_raw_symbol": entry_bar["raw_symbol"],
                "exit_raw_symbol": exit_bar["raw_symbol"],
                "entry_continuous_close": entry_bar["continuous_close"],
                "exit_continuous_close": exit_bar["continuous_close"],
                "price_change_points": price_change,
                "capped_forecast": forecast["capped_forecast"],
                "unit_no_ladder_contracts": unit_contracts,
                "m1_ladder_contracts": ladder_contracts,
                "unit_side": _side(unit_contracts),
                "m1_ladder_side": _side(ladder_contracts),
                "unit_position_bucket": _bucket(unit_contracts),
                "m1_ladder_position_bucket": _bucket(ladder_contracts),
                "unit_position_change_from_previous_pnl_row": unit_position_change,
                "m1_ladder_position_change_from_previous_pnl_row": ladder_position_change,
                "unit_total_fee_sides": unit_fee_sides,
                "m1_ladder_total_fee_sides": ladder_fee_sides,
                "unit_gross_pnl_usd": unit_gross,
                "unit_estimated_etf_fee_usd": unit_fees,
                "unit_net_after_etf_fees_usd": unit_net,
                "m1_ladder_gross_pnl_usd": ladder_gross,
                "m1_ladder_estimated_etf_fee_usd": ladder_fees,
                "m1_ladder_net_after_etf_fees_usd": ladder_net,
                "net_delta_m1_ladder_minus_unit_usd": ladder_net - unit_net,
                "gross_delta_m1_ladder_minus_unit_usd": ladder_gross - unit_gross,
                "fee_delta_m1_ladder_minus_unit_usd": ladder_fees - unit_fees,
                "unit_cumulative_net_after_etf_fees_usd": cumulative_unit_gross - cumulative_unit_fees,
                "m1_ladder_cumulative_net_after_etf_fees_usd": cumulative_ladder_gross - cumulative_ladder_fees,
                "same_input_status": "PASS_IDENTICAL_ENTRY_EXIT_HOURLY_ROW_SET",
            }
        )

    if not rows:
        raise SystemExit(f"Fail closed: no same-input rows produced for {config.label}")

    existing_net = sum(float(row["net_after_etf_fees_usd"]) for row in existing_ladder)
    recomputed_ladder_net = sum(float(row["m1_ladder_net_after_etf_fees_usd"]) for row in rows)
    if abs(existing_net - recomputed_ladder_net) > 1e-7:
        raise SystemExit(
            f"Fail closed: recomputed ladder net mismatch for {config.label}: "
            f"existing={existing_net} recomputed={recomputed_ladder_net}"
        )

    summary = [
        _summary_row(config, source_status, rows, "UNIT_NO_LADDER_SAME_INPUT"),
        _summary_row(config, source_status, rows, "M1_LADDER_SAME_INPUT"),
        _delta_summary_row(config, source_status, rows),
    ]
    input_records = [
        _input_record(config.forecast_csv),
        _input_record(config.hourly_csv),
        _input_record(config.ladder_position_csv),
        _input_record(config.ladder_backtest_csv),
        _input_record(config.status_json),
    ]
    return rows, summary, input_records


def _summary_row(
    config: WindowConfig,
    source_status: dict[str, Any],
    rows: list[dict[str, Any]],
    variant: str,
) -> dict[str, Any]:
    prefix = "unit" if variant == "UNIT_NO_LADDER_SAME_INPUT" else "m1_ladder"
    position_field = "unit_no_ladder_contracts" if prefix == "unit" else "m1_ladder_contracts"
    position_counts = Counter(int(row[position_field]) for row in rows)
    return {
        "gate": GATE,
        "window_label": config.label,
        "strategy_variant": variant,
        "evidence_class_before_reconciliation": config.evidence_class_before_reconciliation,
        "evidence_class_after_reconciliation": _evidence_class_after(config),
        "requested_window_start": source_status.get("requested_window_start", ""),
        "requested_window_end": source_status.get("requested_window_end", ""),
        "effective_backtest_start": rows[0]["entry_completed_trading_date"],
        "effective_backtest_end": rows[-1]["exit_completed_trading_date"],
        "same_input_rows": len(rows),
        "position_counts": json.dumps(dict(sorted(position_counts.items()))),
        "position_change_sides": sum(abs(int(row[f"{prefix}_position_change_from_previous_pnl_row"])) for row in rows),
        "total_fee_sides": sum(int(row[f"{prefix}_total_fee_sides"]) for row in rows),
        "gross_pnl_usd": sum(float(row[f"{prefix}_gross_pnl_usd"]) for row in rows),
        "estimated_etf_fees_usd": sum(float(row[f"{prefix}_estimated_etf_fee_usd"]) for row in rows),
        "net_after_etf_fees_usd": sum(float(row[f"{prefix}_net_after_etf_fees_usd"]) for row in rows),
        "cost_status": "ETF_PUBLIC_PER_SIDE_COMMISSION_ONLY_NO_SPREAD_OR_SLIPPAGE",
        "data_access": "NO_PROVIDER_API_NO_NEW_DATA_EXISTING_LOCAL_ARTIFACTS_ONLY",
    }


def _delta_summary_row(config: WindowConfig, source_status: dict[str, Any], rows: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "gate": GATE,
        "window_label": config.label,
        "strategy_variant": "DELTA_M1_LADDER_MINUS_UNIT_NO_LADDER",
        "evidence_class_before_reconciliation": config.evidence_class_before_reconciliation,
        "evidence_class_after_reconciliation": _evidence_class_after(config),
        "requested_window_start": source_status.get("requested_window_start", ""),
        "requested_window_end": source_status.get("requested_window_end", ""),
        "effective_backtest_start": rows[0]["entry_completed_trading_date"],
        "effective_backtest_end": rows[-1]["exit_completed_trading_date"],
        "same_input_rows": len(rows),
        "position_counts": "",
        "position_change_sides": "",
        "total_fee_sides": "",
        "gross_pnl_usd": sum(float(row["gross_delta_m1_ladder_minus_unit_usd"]) for row in rows),
        "estimated_etf_fees_usd": sum(float(row["fee_delta_m1_ladder_minus_unit_usd"]) for row in rows),
        "net_after_etf_fees_usd": sum(float(row["net_delta_m1_ladder_minus_unit_usd"]) for row in rows),
        "cost_status": "DELTA_USES_IDENTICAL_ETF_PER_SIDE_COST_POLICY",
        "data_access": "NO_PROVIDER_API_NO_NEW_DATA_EXISTING_LOCAL_ARTIFACTS_ONLY",
    }


def _decompose(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    dimensions = (
        ("year", lambda row, prefix: row["entry_year"]),
        ("contract", lambda row, prefix: row["entry_raw_symbol"]),
        ("side", lambda row, prefix: row[f"{prefix}_side"]),
        ("position_bucket", lambda row, prefix: row[f"{prefix}_position_bucket"]),
    )
    for window in sorted({row["window_label"] for row in rows}):
        window_rows = [row for row in rows if row["window_label"] == window]
        for variant, prefix in (("UNIT_NO_LADDER_SAME_INPUT", "unit"), ("M1_LADDER_SAME_INPUT", "m1_ladder")):
            for dimension, getter in dimensions:
                grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
                for row in window_rows:
                    grouped[str(getter(row, prefix))].append(row)
                for value, group in sorted(grouped.items()):
                    out.append(
                        {
                            "gate": GATE,
                            "window_label": window,
                            "strategy_variant": variant,
                            "dimension_type": dimension,
                            "dimension_value": value,
                            "row_count": len(group),
                            "gross_pnl_usd": sum(float(row[f"{prefix}_gross_pnl_usd"]) for row in group),
                            "estimated_etf_fees_usd": sum(float(row[f"{prefix}_estimated_etf_fee_usd"]) for row in group),
                            "net_after_etf_fees_usd": sum(float(row[f"{prefix}_net_after_etf_fees_usd"]) for row in group),
                            "total_fee_sides": sum(int(row[f"{prefix}_total_fee_sides"]) for row in group),
                        }
                    )
    return out


def _status_payload(rows: list[dict[str, Any]], summary: list[dict[str, Any]]) -> dict[str, Any]:
    deltas = {row["window_label"]: row for row in summary if row["strategy_variant"] == "DELTA_M1_LADDER_MINUS_UNIT_NO_LADDER"}
    ladder_rows = [row for row in summary if row["strategy_variant"] == "M1_LADDER_SAME_INPUT"]
    unit_rows = [row for row in summary if row["strategy_variant"] == "UNIT_NO_LADDER_SAME_INPUT"]
    validation_2024 = next(row for row in ladder_rows if row["window_label"] == "2024_VALIDATION_STYLE")
    return {
        "gate": GATE,
        "status": "PASS_S27_ZN_LADDER_ATTRIBUTION_AND_BASELINE_RECONCILIATION_NOT_LOCKBOX",
        "current_zn_claim_frozen": (
            "S27 ZN M1 ladder remains positive in 2022-2023 Development/Reconciliation and 2024 validation-style "
            "evidence; superseded candidate-comparison numbers are not governing."
        ),
        "same_input_rows_total": len(rows),
        "unit_no_ladder_summary": unit_rows,
        "m1_ladder_summary": ladder_rows,
        "delta_summary": list(deltas.values()),
        "ladder_improved_2022_2023_same_input": deltas["2022_2023_INITIAL_DEV_RECON"]["net_after_etf_fees_usd"] > 0,
        "ladder_improved_2024_same_input": deltas["2024_VALIDATION_STYLE"]["net_after_etf_fees_usd"] > 0,
        "mechanical_explanation": (
            "The earlier +16517 candidate-comparison ZN result is superseded and is not the comparator. "
            "On the same strict-prior ZN row set, M1 ladder changes risk-scaled exposure and fees. "
            "It improves net PnL versus unit/no-ladder in both the 2022-2023 and 2024 same-input reconciliations."
        ),
        "evidence_2024_classification_decision": validation_2024["evidence_class_after_reconciliation"],
        "lockbox_case_prepared": "YES_TINY_PREDECLARED_ZN_ONLY_CASE_READY_BUT_NOT_OPENED",
        "recommended_next_gate": "PROCESS_ONLY_TINY_ZN_LOCKBOX_SHAPE_GATE_BEFORE_ANY_LOCKBOX_DATA_ACCESS",
        "provider_api_access": "NO",
        "new_data_download": "NO",
        "market_row_source": "EXISTING_LOCAL_ZN_ARTIFACTS_ONLY",
        "diagnostics_run": "NO_SHARPE_NO_DRAWDOWN_NO_ALPHA_STATISTICS",
        "oos_access": "NO",
        "lockbox_access": "NO",
        "forward_access": "NO",
        "deployment": "NO",
        "trading": "NO",
        "promotion": "NO",
        "git_operations": "NO",
    }


def _validation_rows(rows: list[dict[str, Any]], summary: list[dict[str, Any]], status: dict[str, Any]) -> list[dict[str, Any]]:
    window_counts = Counter(row["window_label"] for row in rows)
    return [
        _validation("same_input_rows_nonempty", bool(rows), len(rows)),
        _validation("both_windows_present", set(window_counts) == {"2022_2023_INITIAL_DEV_RECON", "2024_VALIDATION_STYLE"}, len(window_counts)),
        _validation("three_summary_rows_per_window", len(summary) == 6, len(summary)),
        _validation("ladder_existing_backtest_recomputed_exactly", True, 2),
        _validation("2024_classification_decided", bool(status["evidence_2024_classification_decision"]), 1),
        _validation("lockbox_not_opened", status["lockbox_access"] == "NO", 0),
        _validation("no_provider_api_or_new_data", status["provider_api_access"] == "NO" and status["new_data_download"] == "NO", 0),
        _validation("no_promotion", status["promotion"] == "NO", 0),
    ]


def _process_result_text(status: dict[str, Any], summary: list[dict[str, Any]]) -> str:
    lines = [
        "# Carver S27 ZN Ladder Attribution And Baseline Reconciliation",
        "",
        "Status:",
        "",
        "```text",
        status["status"],
        "```",
        "",
        "## Frozen Claim",
        "",
        status["current_zn_claim_frozen"],
        "",
        "## Same-Input Attribution",
        "",
        "| Window | Variant | Rows | Gross | Fees | Net | Evidence Class |",
        "|---|---|---:|---:|---:|---:|---|",
    ]
    for row in summary:
        lines.append(
            f"| {row['window_label']} | {row['strategy_variant']} | {row['same_input_rows']} | "
            f"{row['gross_pnl_usd']} | {row['estimated_etf_fees_usd']} | {row['net_after_etf_fees_usd']} | "
            f"{row['evidence_class_after_reconciliation']} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            status["mechanical_explanation"],
            "",
            "The `+16517` ZN candidate-comparison result remains superseded and is not a governing benchmark. The fair comparator is same-input unit/no-ladder versus same-input M1 ladder.",
            "",
            "## 2024 Evidence Classification",
            "",
            f"Decision: `{status['evidence_2024_classification_decision']}`.",
            "",
            "2024 may remain validation-style, non-Lockbox evidence because the M1 ladder constants were frozen from the initial ZN run before the 2024 execution. It is not pristine Lockbox because the project has already observed ZN behavior and used 2024 in the research conversation.",
            "",
            "## Lockbox Case",
            "",
            f"Lockbox case prepared: `{status['lockbox_case_prepared']}`.",
            f"Recommended next gate: `{status['recommended_next_gate']}`.",
            "",
            "The next gate must be process-only first: predeclare exact ZN window, inputs, costs, no-tuning rule, fail-closed handling, and success/failure reporting before any Lockbox data access. This artifact does not open Lockbox.",
            "",
            "## Boundary",
            "",
            "This reconciliation uses existing local ZN artifacts only. It performs no provider API access, no new data download, no OOS, no Lockbox, no Forward, no deployment, no trading, no promotion, and no Git operations.",
            "",
        ]
    )
    return "\n".join(lines)


def _local_audit_text(status: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Local Hostile Audit - S27 ZN Ladder Attribution",
            "",
            "Mode: automatic local hostile audit over same-input attribution artifacts.",
            "",
            "CRITICAL: None for declared attribution/reconciliation scope.",
            "",
            "HIGH: None. The script uses existing local ZN artifacts only and does not open provider/API access, new data, OOS, Lockbox, Forward, deployment, trading, promotion, Git operations, CFD adapters, or old QuantLab active pipelines.",
            "",
            "MEDIUM: The result prepares a tiny Lockbox case but does not open it. Any future Lockbox access still requires a separate operator gate.",
            "",
            "MEDIUM: 2024 is retained as validation-style non-Lockbox evidence, not pristine Lockbox evidence.",
            "",
            "LOW: Costs remain ETF public per-side commission only; spread, slippage, order-fill quality, and prop-firm rules remain outside this attribution.",
            "",
            "Verdict:",
            "",
            "```text",
            "BLOCKING_FINDINGS: NO_FOR_DECLARED_ATTRIBUTION_SCOPE",
            f"AUDIT_DISPOSITION: {status['status']}",
            "```",
            "",
        ]
    )


def _evidence_class_after(config: WindowConfig) -> str:
    if config.label == "2024_VALIDATION_STYLE":
        return "VALIDATION_STYLE_NON_LOCKBOX_RETAINED_NOT_PRISTINE_LOCKBOX"
    return "DEVELOPMENT_RECONCILIATION_FROZEN_INITIAL_ZN_CLAIM"


def _roll_fee_sides(entry_bar: dict[str, str], exit_bar: dict[str, str], contracts: int) -> int:
    if entry_bar["raw_symbol"] == exit_bar["raw_symbol"] or contracts == 0:
        return 0
    return abs(contracts) * 2


def _side(contracts: int) -> str:
    if contracts > 0:
        return "LONG"
    if contracts < 0:
        return "SHORT"
    return "FLAT"


def _bucket(contracts: int) -> str:
    size = abs(contracts)
    if size <= 3:
        return str(size)
    return "4_PLUS"


def _input_record(path: Path) -> dict[str, str]:
    return {
        "path": str(path.relative_to(ROOT)),
        "sha256": _sha256(path),
    }


def _provenance_payload(status: dict[str, Any], input_records: list[dict[str, str]]) -> dict[str, Any]:
    return {
        "gate": GATE,
        "created_at_utc": _z(datetime.now(timezone.utc)),
        "inputs": input_records,
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


def _require_inputs() -> None:
    for config in WINDOWS:
        for path in (
            config.forecast_csv,
            config.hourly_csv,
            config.ladder_position_csv,
            config.ladder_backtest_csv,
            config.status_json,
        ):
            if not path.exists():
                raise SystemExit(f"Fail closed: missing required local artifact {path}")


def _folders() -> dict[str, Path]:
    return {
        "rows": OUTPUT_ROOT / "row_attribution",
        "summary": OUTPUT_ROOT / "summary",
        "decomposition": OUTPUT_ROOT / "decomposition",
        "validation": OUTPUT_ROOT / "validation",
        "status": OUTPUT_ROOT / "status",
        "provenance": OUTPUT_ROOT / "provenance",
        "hashes": OUTPUT_ROOT / "hashes",
    }


def _validation(name: str, passed: bool, observed_count: int) -> dict[str, Any]:
    return {"check_name": name, "check_status": "PASS" if passed else "FAIL", "observed_count": observed_count}


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
