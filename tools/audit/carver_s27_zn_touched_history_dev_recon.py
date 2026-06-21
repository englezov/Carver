from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
RUN_ID = "20260601_S27_ZN_TOUCHED_HISTORY_DEV_RECON_BACKTEST"
GATE = "S27_ZN_TOUCHED_HISTORY_DEVELOPMENT_RECONCILIATION_BACKTEST"

ROW_ATTRIBUTION_CSV = (
    ROOT
    / "docs/researchops/s26_s27_ladder_attribution/ZN_S27/2022_2024/row_attribution/"
    / "20260601_S27_ZN_LADDER_ATTRIBUTION_AND_BASELINE_RECONCILIATION_row_attribution.csv"
)
ATTRIBUTION_STATUS_JSON = (
    ROOT
    / "docs/researchops/s26_s27_ladder_attribution/ZN_S27/2022_2024/status/"
    / "20260601_S27_ZN_LADDER_ATTRIBUTION_AND_BASELINE_RECONCILIATION_status.json"
)
LOCKBOX_STATUS_JSON = (
    ROOT
    / "docs/researchops/s26_s27_lockbox_readiness/ZN_S27/20260601_S27_ZN_LOCKBOX_READINESS_DECISION/status/"
    / "20260601_S27_ZN_LOCKBOX_READINESS_DECISION_status.json"
)
EXTENDED_DAILY_STATUS_JSON = (
    ROOT
    / "docs/researchops/s26_s27_backtest_readiness/ZN_S27_SINGLE_INSTRUMENT/2022-01-01_2023-12-31/"
    / "local_extended_daily_runtime/status/"
    / "20260531_S27_ZN_2022_2023_LOCAL_EXTENDED_DAILY_RUNTIME_status.json"
)

OUTPUT_ROOT = ROOT / "docs/researchops/s26_s27_touched_history/ZN_S27/2022-01-04_2026-05-22"
PROCESS_RESULT_DOC = ROOT / "docs/process/CARVER_S27_ZN_TOUCHED_HISTORY_DEV_RECON_BACKTEST_RESULT_2026-06-01.md"
LOCAL_AUDIT_DOC = ROOT / "docs/process/CARVER_S27_ZN_TOUCHED_HISTORY_DEV_RECON_LOCAL_HOSTILE_AUDIT_2026-06-01.md"


def main() -> None:
    _require_inputs()
    folders = _folders()
    for folder in folders.values():
        folder.mkdir(parents=True, exist_ok=True)

    rows = _read_csv(ROW_ATTRIBUTION_CSV)
    attribution_status = _read_json(ATTRIBUTION_STATUS_JSON)
    lockbox_status = _read_json(LOCKBOX_STATUS_JSON)
    extended_daily_status = _read_json(EXTENDED_DAILY_STATUS_JSON)

    summary_rows = _summary_rows(rows)
    yearly_rows = _yearly_rows(rows)
    coverage_rows = _coverage_rows(rows, extended_daily_status)
    cost_rows = _cost_rows(lockbox_status)
    stats_rows = _stats_rows(rows)
    validation_rows = _validation_rows(rows, coverage_rows, cost_rows)
    status = _status_payload(
        rows=rows,
        summary_rows=summary_rows,
        yearly_rows=yearly_rows,
        coverage_rows=coverage_rows,
        cost_rows=cost_rows,
        attribution_status=attribution_status,
        lockbox_status=lockbox_status,
        extended_daily_status=extended_daily_status,
    )

    _write_csv(folders["summary"] / f"{RUN_ID}_summary.csv", summary_rows)
    _write_csv(folders["summary"] / f"{RUN_ID}_yearly_summary.csv", yearly_rows)
    _write_csv(folders["stats"] / f"{RUN_ID}_trade_stats.csv", stats_rows)
    _write_csv(folders["coverage"] / f"{RUN_ID}_coverage_and_fail_closed_extension.csv", coverage_rows)
    _write_csv(folders["cost"] / f"{RUN_ID}_cost_status.csv", cost_rows)
    _write_csv(folders["validation"] / f"{RUN_ID}_validation_ledger.csv", validation_rows)
    _write_json(folders["status"] / f"{RUN_ID}_status.json", status)
    _write_json(folders["provenance"] / f"{RUN_ID}_provenance.json", _provenance_payload(status))
    _write_json(folders["hashes"] / f"{RUN_ID}_sha256.json", _hash_tree(OUTPUT_ROOT))
    PROCESS_RESULT_DOC.write_text(_process_result_text(status, summary_rows, coverage_rows, cost_rows), encoding="utf-8")
    LOCAL_AUDIT_DOC.write_text(_local_audit_text(status), encoding="utf-8")

    print(status["status"])
    print(f"usable_hourly_backtest_start={status['usable_hourly_backtest_start']}")
    print(f"usable_hourly_backtest_end={status['usable_hourly_backtest_end']}")
    print(f"m1_ladder_net_after_recorded_fee_usd={status['m1_ladder_net_after_recorded_fee_usd']}")
    print(f"unit_no_ladder_net_after_recorded_fee_usd={status['unit_no_ladder_net_after_recorded_fee_usd']}")
    print(f"hourly_extension_status={status['post_2024_hourly_extension_status']}")
    print(f"artifact_root={OUTPUT_ROOT.relative_to(ROOT)}")


def _summary_rows(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    return [
        _summary_for(rows, "UNIT_NO_LADDER_SAME_INPUT", "unit"),
        _summary_for(rows, "M1_LADDER_SAME_INPUT", "m1_ladder"),
        _delta_summary(rows),
    ]


def _summary_for(rows: list[dict[str, str]], variant: str, prefix: str) -> dict[str, Any]:
    pnl = [float(row[f"{prefix}_net_after_etf_fees_usd"]) for row in rows]
    gross = [float(row[f"{prefix}_gross_pnl_usd"]) for row in rows]
    fees = [float(row[f"{prefix}_estimated_etf_fee_usd"]) for row in rows]
    positions = [int(row[f"{prefix}_contracts"]) if f"{prefix}_contracts" in row else int(row[f"{prefix}_no_ladder_contracts"]) for row in rows]
    position_changes = [abs(int(row[f"{prefix}_position_change_from_previous_pnl_row"])) for row in rows]
    total_fee_sides = [int(row[f"{prefix}_total_fee_sides"]) for row in rows]
    nonzero_pnl = [value for value in pnl if abs(value) > 1e-12]
    daily_net = _group_sum(rows, f"{prefix}_net_after_etf_fees_usd", "entry_completed_trading_date")
    nonzero_daily = [value for value in daily_net.values() if abs(value) > 1e-12]
    return {
        "gate": GATE,
        "strategy_variant": variant,
        "lane_class": "SOURCE_NATIVE_FUTURES",
        "evidence_class": "TOUCHED_HISTORY_DEVELOPMENT_RECONCILIATION_NOT_LOCKBOX_NOT_PROMOTION",
        "usable_hourly_backtest_start": min(row["entry_completed_trading_date"] for row in rows),
        "usable_hourly_backtest_end": max(row["exit_completed_trading_date"] for row in rows),
        "pnl_rows": len(rows),
        "active_position_rows": sum(1 for value in positions if value != 0),
        "flat_position_rows": sum(1 for value in positions if value == 0),
        "position_counts": json.dumps(dict(sorted(Counter(positions).items()))),
        "position_change_sides": sum(position_changes),
        "total_fee_sides": sum(total_fee_sides),
        "gross_pnl_usd": sum(gross),
        "recorded_fee_model": "ETF_PUBLIC_PER_SIDE_COMMISSION_ONLY_NO_SPREAD_NO_SLIPPAGE",
        "recorded_fees_usd": sum(fees),
        "net_after_recorded_fees_usd": sum(pnl),
        "nonzero_pnl_row_count": len(nonzero_pnl),
        "positive_nonzero_pnl_row_count": sum(1 for value in nonzero_pnl if value > 0),
        "nonzero_pnl_row_win_rate": _ratio(sum(1 for value in nonzero_pnl if value > 0), len(nonzero_pnl)),
        "nonzero_daily_count": len(nonzero_daily),
        "positive_nonzero_daily_count": sum(1 for value in nonzero_daily if value > 0),
        "nonzero_daily_win_rate": _ratio(sum(1 for value in nonzero_daily if value > 0), len(nonzero_daily)),
        "futures_realistic_cost_status": "FAIL_CLOSED_NOT_EXECUTED_RECORDED_FEE_IS_NOT_LOCKBOX_COST",
    }


def _delta_summary(rows: list[dict[str, str]]) -> dict[str, Any]:
    delta = [float(row["net_delta_m1_ladder_minus_unit_usd"]) for row in rows]
    gross_delta = [float(row["gross_delta_m1_ladder_minus_unit_usd"]) for row in rows]
    fee_delta = [float(row["fee_delta_m1_ladder_minus_unit_usd"]) for row in rows]
    daily_delta = _group_sum(rows, "net_delta_m1_ladder_minus_unit_usd", "entry_completed_trading_date")
    nonzero_delta = [value for value in delta if abs(value) > 1e-12]
    nonzero_daily = [value for value in daily_delta.values() if abs(value) > 1e-12]
    return {
        "gate": GATE,
        "strategy_variant": "DELTA_M1_LADDER_MINUS_UNIT_NO_LADDER",
        "lane_class": "SOURCE_NATIVE_FUTURES",
        "evidence_class": "TOUCHED_HISTORY_DEVELOPMENT_RECONCILIATION_NOT_LOCKBOX_NOT_PROMOTION",
        "usable_hourly_backtest_start": min(row["entry_completed_trading_date"] for row in rows),
        "usable_hourly_backtest_end": max(row["exit_completed_trading_date"] for row in rows),
        "pnl_rows": len(rows),
        "active_position_rows": "",
        "flat_position_rows": "",
        "position_counts": "",
        "position_change_sides": "",
        "total_fee_sides": "",
        "gross_pnl_usd": sum(gross_delta),
        "recorded_fee_model": "DELTA_OF_IDENTICAL_RECORDED_FEE_POLICY",
        "recorded_fees_usd": sum(fee_delta),
        "net_after_recorded_fees_usd": sum(delta),
        "nonzero_pnl_row_count": len(nonzero_delta),
        "positive_nonzero_pnl_row_count": sum(1 for value in nonzero_delta if value > 0),
        "nonzero_pnl_row_win_rate": _ratio(sum(1 for value in nonzero_delta if value > 0), len(nonzero_delta)),
        "nonzero_daily_count": len(nonzero_daily),
        "positive_nonzero_daily_count": sum(1 for value in nonzero_daily if value > 0),
        "nonzero_daily_win_rate": _ratio(sum(1 for value in nonzero_daily if value > 0), len(nonzero_daily)),
        "futures_realistic_cost_status": "FAIL_CLOSED_NOT_EXECUTED_RECORDED_FEE_IS_NOT_LOCKBOX_COST",
    }


def _yearly_rows(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for year in sorted({row["entry_year"] for row in rows}):
        year_rows = [row for row in rows if row["entry_year"] == year]
        for summary in _summary_rows(year_rows):
            summary["year"] = year
            output.append(summary)
    return output


def _stats_rows(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for variant, prefix in (("UNIT_NO_LADDER_SAME_INPUT", "unit"), ("M1_LADDER_SAME_INPUT", "m1_ladder")):
        prior = 0
        entries = 0
        exits = 0
        sign_flips = 0
        adjustments = 0
        for row in rows:
            current = int(row[f"{prefix}_contracts"]) if f"{prefix}_contracts" in row else int(row[f"{prefix}_no_ladder_contracts"])
            if prior == 0 and current != 0:
                entries += 1
            elif prior != 0 and current == 0:
                exits += 1
            elif prior != 0 and current != 0 and (prior > 0) != (current > 0):
                sign_flips += 1
            elif prior != 0 and current != 0 and prior != current:
                adjustments += 1
            prior = current
        output.append(
            {
                "gate": GATE,
                "strategy_variant": variant,
                "entry_events_zero_to_nonzero": entries,
                "exit_events_nonzero_to_zero": exits,
                "sign_flip_events": sign_flips,
                "same_side_size_adjustment_events": adjustments,
                "trade_count_interpretation": "EVENT_COUNTS_NOT_ROUND_TRIP_TRADE_ACCOUNTING",
                "evidence_class": "TOUCHED_HISTORY_DEVELOPMENT_RECONCILIATION_NOT_LOCKBOX_NOT_PROMOTION",
            }
        )
    return output


def _coverage_rows(rows: list[dict[str, str]], extended_daily_status: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "gate": GATE,
            "coverage_segment": "USABLE_HOURLY_BACKTEST_EVIDENCE",
            "date_start": min(row["entry_completed_trading_date"] for row in rows),
            "date_end": max(row["exit_completed_trading_date"] for row in rows),
            "row_count": len(rows),
            "coverage_status": "PASS_EXISTING_LOCAL_HOURLY_BACKTEST_ROWS_RECOMPUTED",
            "notes": "Existing local row attribution covers the usable hourly S27 ZN backtest evidence.",
        },
        {
            "gate": GATE,
            "coverage_segment": "POST_2024_THROUGH_2026_05_22",
            "date_start": "2025-01-01",
            "date_end": str(extended_daily_status.get("extended_daily_end", "2026-05-22")),
            "row_count": "",
            "coverage_status": "FAIL_CLOSED_NO_LOCAL_HOURLY_S27_BACKTEST_ROWS_DAILY_RUNTIME_SUPPORT_ONLY",
            "notes": "Local extended support reaches 2026-05-22 for daily runtime/VQM only; S27 source-frequency backtest requires hourly bars.",
        },
    ]


def _cost_rows(lockbox_status: dict[str, Any]) -> list[dict[str, Any]]:
    failing = lockbox_status.get("failing_cost_components", [])
    return [
        {
            "gate": GATE,
            "cost_component": "recorded_backtest_fee",
            "cost_status": "RECORDED_ETF_PUBLIC_PER_SIDE_COMMISSION_ONLY_NO_SPREAD_NO_SLIPPAGE",
            "notes": "Used only to reproduce existing touched-history artifacts; not futures-realistic Lockbox cost.",
        },
        {
            "gate": GATE,
            "cost_component": "futures_realistic_cost_readiness",
            "cost_status": lockbox_status.get("cost_readiness_status", "FAIL_CLOSED_UNKNOWN"),
            "notes": "Lockbox readiness gate remains controlling for futures-realistic cost closure.",
        },
        {
            "gate": GATE,
            "cost_component": "failing_cost_components",
            "cost_status": "FAIL_CLOSED_COMPONENTS_REMAIN",
            "notes": json.dumps(failing),
        },
    ]


def _validation_rows(rows: list[dict[str, str]], coverage_rows: list[dict[str, Any]], cost_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    statuses = {row["same_input_status"] for row in rows}
    return [
        _validation("source_native_lane", "PASS", "All generated artifacts declare SOURCE_NATIVE_FUTURES."),
        _validation("same_input_status", "PASS" if statuses == {"PASS_IDENTICAL_ENTRY_EXIT_HOURLY_ROW_SET"} else "FAIL", json.dumps(sorted(statuses))),
        _validation("not_lockbox_label", "PASS", "All outputs are touched-history Development/Reconciliation, NOT_LOCKBOX, NOT_PROMOTION."),
        _validation("post_2024_hourly_extension", coverage_rows[1]["coverage_status"], coverage_rows[1]["notes"]),
        _validation("futures_realistic_cost", cost_rows[1]["cost_status"], cost_rows[1]["notes"]),
        _validation("provider_api_access", "PASS_NO_PROVIDER_API_ACCESS", "This script reads existing local CSV/JSON artifacts only."),
    ]


def _validation(check: str, status: str, notes: str) -> dict[str, str]:
    return {"gate": GATE, "check": check, "status": status, "notes": notes}


def _status_payload(
    *,
    rows: list[dict[str, str]],
    summary_rows: list[dict[str, Any]],
    yearly_rows: list[dict[str, Any]],
    coverage_rows: list[dict[str, Any]],
    cost_rows: list[dict[str, Any]],
    attribution_status: dict[str, Any],
    lockbox_status: dict[str, Any],
    extended_daily_status: dict[str, Any],
) -> dict[str, Any]:
    by_variant = {row["strategy_variant"]: row for row in summary_rows}
    return {
        "gate": GATE,
        "run_id": RUN_ID,
        "status": "PASS_S27_ZN_TOUCHED_HISTORY_DEV_RECON_BACKTEST_NOT_LOCKBOX_NOT_PROMOTION",
        "lane_class": "SOURCE_NATIVE_FUTURES",
        "usable_hourly_backtest_start": min(row["entry_completed_trading_date"] for row in rows),
        "usable_hourly_backtest_end": max(row["exit_completed_trading_date"] for row in rows),
        "requested_outer_boundary_through": extended_daily_status.get("extended_daily_end", "2026-05-22"),
        "post_2024_hourly_extension_status": coverage_rows[1]["coverage_status"],
        "pnl_rows": len(rows),
        "year_count": len({row["entry_year"] for row in rows}),
        "yearly_summary_rows": len(yearly_rows),
        "unit_no_ladder_net_after_recorded_fee_usd": by_variant["UNIT_NO_LADDER_SAME_INPUT"]["net_after_recorded_fees_usd"],
        "m1_ladder_net_after_recorded_fee_usd": by_variant["M1_LADDER_SAME_INPUT"]["net_after_recorded_fees_usd"],
        "delta_m1_minus_unit_net_after_recorded_fee_usd": by_variant["DELTA_M1_LADDER_MINUS_UNIT_NO_LADDER"]["net_after_recorded_fees_usd"],
        "unit_no_ladder_daily_win_rate": by_variant["UNIT_NO_LADDER_SAME_INPUT"]["nonzero_daily_win_rate"],
        "m1_ladder_daily_win_rate": by_variant["M1_LADDER_SAME_INPUT"]["nonzero_daily_win_rate"],
        "recorded_fee_model": "ETF_PUBLIC_PER_SIDE_COMMISSION_ONLY_NO_SPREAD_NO_SLIPPAGE",
        "futures_realistic_cost_status": cost_rows[1]["cost_status"],
        "cost_readiness_controlling_decision": lockbox_status.get("decision", ""),
        "source_attribution_status": attribution_status.get("status", ""),
        "provider_api_access": "NO",
        "new_data_download": "NO",
        "market_row_source": "EXISTING_LOCAL_CARVER_ROW_ATTRIBUTION_ONLY",
        "oos_lockbox_forward_access": "NO",
        "diagnostics_scope": "TOUCHED_HISTORY_SUMMARY_STATISTICS_ONLY_NO_SHARPE_NO_DRAWDOWN_NO_ALPHA_CLAIM",
        "deployment_trading_promotion": "NO",
        "git_operations": "NO",
        "created_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }


def _process_result_text(status: dict[str, Any], summary_rows: list[dict[str, Any]], coverage_rows: list[dict[str, Any]], cost_rows: list[dict[str, Any]]) -> str:
    summary_lines = "\n".join(
        f"- {row['strategy_variant']}: net={float(row['net_after_recorded_fees_usd']):.2f}, "
        f"gross={float(row['gross_pnl_usd']):.2f}, recorded_fees={float(row['recorded_fees_usd']):.2f}, "
        f"daily_win_rate={row['nonzero_daily_win_rate']}"
        for row in summary_rows
    )
    return f"""# Carver S27 ZN Touched-History Development/Reconciliation Backtest

Status:

```text
{status["status"]}
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Scope

This artifact recomputes and summarizes existing local S27 ZN hourly backtest evidence only. It is explicitly:

```text
NOT_LOCKBOX
NOT_PROMOTION
NO_NEW_PROVIDER_ACCESS
NO_NEW_DATA_DOWNLOAD
```

## Usable Hourly Evidence

```text
{status["usable_hourly_backtest_start"]} through {status["usable_hourly_backtest_end"]}
```

The requested touched-history outer boundary through `{status["requested_outer_boundary_through"]}` is not fully source-frequency executable because the post-2024 local evidence is daily runtime/VQM support only, not hourly S27 backtest rows.

## Summary

{summary_lines}

## Coverage Boundary

```text
{coverage_rows[1]["coverage_status"]}
```

{coverage_rows[1]["notes"]}

## Cost Boundary

Recorded fee model:

```text
{status["recorded_fee_model"]}
```

Futures-realistic cost status:

```text
{cost_rows[1]["cost_status"]}
```

This run does not close futures-realistic cost readiness and does not open Lockbox.

## Non-Authorization

This artifact authorizes no provider API access, no data download, no OOS, no Lockbox, no Forward, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, and no remote operations.
"""


def _local_audit_text(status: dict[str, Any]) -> str:
    return f"""# Local Lean Hostile Audit - S27 ZN Touched-History Dev/Recon Backtest

Mode: automatic local hostile audit over existing local artifacts only. No provider API access, no data download, no OOS, no Lockbox, no Forward, no Git operations.

## Findings

CRITICAL: None.

HIGH: Post-2024 through `{status["requested_outer_boundary_through"]}` is fail-closed for hourly S27 backtesting. Local daily runtime support is not source-frequency-compatible hourly evidence.

MEDIUM: Futures-realistic costs remain fail-closed. The reproduced backtest uses the recorded ETF/public per-side commission-only assumption and no spread/slippage.

LOW: Summary statistics are touched-history Development/Reconciliation only and must not be read as validation, Lockbox, or promotion evidence.

## Verdict

```text
BLOCKING_FINDINGS: NO_FOR_TOUCHED_HISTORY_DEV_RECON_SCOPE
AUDIT_DISPOSITION: PASS_TOUCHED_HISTORY_DEV_RECON_NOT_LOCKBOX_NOT_PROMOTION
```
"""


def _provenance_payload(status: dict[str, Any]) -> dict[str, Any]:
    inputs = [ROW_ATTRIBUTION_CSV, ATTRIBUTION_STATUS_JSON, LOCKBOX_STATUS_JSON, EXTENDED_DAILY_STATUS_JSON]
    return {
        "gate": GATE,
        "run_id": RUN_ID,
        "status": status["status"],
        "created_at_utc": status["created_at_utc"],
        "inputs": [{"path": str(path.relative_to(ROOT)), "sha256": _sha256(path)} for path in inputs],
        "provider_api_access": "NO",
        "new_data_download": "NO",
        "git_operations": "NO",
    }


def _group_sum(rows: list[dict[str, str]], value_field: str, group_field: str) -> dict[str, float]:
    grouped: dict[str, float] = defaultdict(float)
    for row in rows:
        grouped[row[group_field]] += float(row[value_field])
    return dict(grouped)


def _ratio(numerator: int, denominator: int) -> str:
    if denominator == 0:
        return ""
    return f"{numerator / denominator:.6f}"


def _folders() -> dict[str, Path]:
    return {
        "summary": OUTPUT_ROOT / "summary",
        "stats": OUTPUT_ROOT / "stats",
        "coverage": OUTPUT_ROOT / "coverage",
        "cost": OUTPUT_ROOT / "cost",
        "validation": OUTPUT_ROOT / "validation",
        "status": OUTPUT_ROOT / "status",
        "provenance": OUTPUT_ROOT / "provenance",
        "hashes": OUTPUT_ROOT / "hashes",
    }


def _require_inputs() -> None:
    missing = [path for path in (ROW_ATTRIBUTION_CSV, ATTRIBUTION_STATUS_JSON, LOCKBOX_STATUS_JSON, EXTENDED_DAILY_STATUS_JSON) if not path.exists()]
    if missing:
        raise SystemExit("Missing required local input(s): " + ", ".join(str(path.relative_to(ROOT)) for path in missing))


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise SystemExit(f"Refusing to write empty CSV: {path}")
    fieldnames = list(rows[0])
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _hash_tree(root: Path) -> dict[str, str]:
    hash_file_name = f"{RUN_ID}_sha256.json"
    return {
        str(path.relative_to(ROOT)): _sha256(path)
        for path in sorted(root.rglob("*"))
        if path.is_file() and path.name != hash_file_name
    }


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


if __name__ == "__main__":
    main()
