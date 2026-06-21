from __future__ import annotations

import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
RUN_ID = "20260601_S27_ZN_LOCKBOX_READINESS_DECISION"
GATE = "S27_ZN_LOCKBOX_READINESS_DECISION_GATE"
LANE = "SOURCE_NATIVE_FUTURES"

OUT_ROOT = ROOT / "docs/researchops/s26_s27_lockbox_readiness/ZN_S27" / RUN_ID
PROCESS_DOC = ROOT / "docs/process/CARVER_S27_ZN_LOCKBOX_READINESS_DECISION_GATE_2026-06-01.md"
LOCAL_AUDIT_DOC = ROOT / "docs/process/CARVER_S27_ZN_LOCKBOX_READINESS_LOCAL_HOSTILE_AUDIT_2026-06-01.md"

FREEZE_FILES = [
    "docs/process/CARVER_S26_S27_SOURCE_ATOM_SHEET_2026-05-30.md",
    "docs/process/CARVER_S27_ZN_SOURCE_LINE_AUDIT_EWMAC_VQM_CLOSURE_2026-06-01.md",
    "docs/process/CARVER_S27_ZN_M1_LADDER_DEV_RECON_BACKTEST_RESULT_2026-05-31.md",
    "docs/process/CARVER_S27_ZN_2024_VALIDATION_BACKTEST_RESULT_2026-06-01.md",
    "docs/process/CARVER_S27_ZN_PRE_LOCKBOX_ROBUSTNESS_STACK_RESULT_2026-06-01.md",
    "docs/process/CARVER_S27_ZN_PRE_LOCKBOX_MCPT_NULL_STACK_RESULT_2026-06-01.md",
    "docs/process/CARVER_S27_ZN_FUTURES_REALISTIC_COST_MODEL_SHAPE_GATE_2026-06-01.md",
    "docs/process/CARVER_S27_ZN_FUTURES_REALISTIC_COST_TEST_MANIFEST_RECORD_2026-06-01.md",
    "docs/researchops/s26_s27_ladder_attribution/ZN_S27/2022_2024/status/20260601_S27_ZN_LADDER_ATTRIBUTION_AND_BASELINE_RECONCILIATION_status.json",
    "docs/researchops/s26_s27_pre_lockbox_robustness/ZN_S27/2022_2024/summary/20260601_S27_ZN_PRE_LOCKBOX_ROBUSTNESS_STACK_summary.csv",
    "docs/researchops/s26_s27_pre_lockbox_robustness/ZN_S27/2022_2024/structure/20260601_S27_ZN_PRE_LOCKBOX_ROBUSTNESS_STACK_forward_horizon_structure.csv",
    "docs/researchops/s26_s27_pre_lockbox_mcpt/ZN_S27/2022_2024/summary/20260601_S27_ZN_PRE_LOCKBOX_MCPT_NULL_STACK_mcpt_summary.csv",
    "docs/researchops/s26_s27_cost_model/ZN_S27/CARVER_S27_ZN_FUTURES_REALISTIC_COST_TEST_MANIFEST_2026-06-01.csv",
    "tools/audit/carver_s27_zn_ladder_attribution.py",
    "tools/audit/carver_s27_zn_robustness.py",
    "tools/audit/carver_s27_zn_mcpt.py",
]

TOUCHED_EVIDENCE = [
    {
        "window_label": "2022_2023_INITIAL_DEV_RECON",
        "date_start": "2022-01-01",
        "date_end": "2023-12-31",
        "disposition": "TOUCHED_INITIAL_DEVELOPMENT_RECONCILIATION_NOT_LOCKBOX",
    },
    {
        "window_label": "2024_VALIDATION_STYLE",
        "date_start": "2024-01-01",
        "date_end": "2024-12-31",
        "disposition": "TOUCHED_INFORMATIONAL_VALIDATION_STYLE_NOT_LOCKBOX",
    },
]


def main() -> None:
    folders = {
        "freeze": OUT_ROOT / "freeze",
        "cost": OUT_ROOT / "cost_readiness",
        "window": OUT_ROOT / "window",
        "pass_fail": OUT_ROOT / "pass_fail",
        "status": OUT_ROOT / "status",
        "provenance": OUT_ROOT / "provenance",
        "hashes": OUT_ROOT / "hashes",
    }
    for folder in folders.values():
        folder.mkdir(parents=True, exist_ok=True)

    freeze_rows = _freeze_rows()
    cost_rows = _cost_readiness_rows()
    window_rows = _window_rows()
    pass_fail_rows = _pass_fail_rows()

    _write_csv(folders["freeze"] / f"{RUN_ID}_variant_hash_freeze.csv", freeze_rows)
    _write_csv(folders["cost"] / f"{RUN_ID}_cost_readiness_ledger.csv", cost_rows)
    _write_csv(folders["window"] / f"{RUN_ID}_lockbox_window_decision.csv", window_rows)
    _write_csv(folders["pass_fail"] / f"{RUN_ID}_predeclared_pass_fail_rules.csv", pass_fail_rows)

    status = _status_payload(freeze_rows, cost_rows, window_rows, pass_fail_rows)
    _write_json(folders["status"] / f"{RUN_ID}_status.json", status)
    _write_json(folders["provenance"] / f"{RUN_ID}_provenance.json", _provenance_payload(status))

    PROCESS_DOC.write_text(_process_doc(status), encoding="utf-8")
    LOCAL_AUDIT_DOC.write_text(_local_audit_doc(status), encoding="utf-8")
    _write_json(folders["hashes"] / f"{RUN_ID}_sha256.json", _hash_tree(OUT_ROOT))


def _freeze_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for rel in FREEZE_FILES:
        path = ROOT / rel
        rows.append(
            {
                "gate": GATE,
                "lane": LANE,
                "freeze_scope": "S27_ZN_SOURCE_NATIVE_VARIANT_READINESS_FREEZE",
                "artifact_path": rel,
                "artifact_exists": "YES" if path.exists() else "NO",
                "sha256": _sha256(path) if path.exists() else "",
                "freeze_status": "FROZEN_FOR_READINESS_NOT_LOCKBOX" if path.exists() else "MISSING_FAIL_CLOSED",
            }
        )
    return rows


def _cost_readiness_rows() -> list[dict[str, Any]]:
    return [
        _cost_row("cost_manifest_defined", "PASS_DEFINED_NOT_EXECUTED", "Existing manifest is present but not a cost execution."),
        _cost_row("exchange_fee", "FAIL_CLOSED_STATIC_FEE_EVIDENCE_NOT_LOCKED", "No audited exchange-fee evidence or execution ledger is present."),
        _cost_row("clearing_nfa_regulatory_fee", "FAIL_CLOSED_STATIC_FEE_EVIDENCE_NOT_LOCKED", "No audited clearing/NFA/regulatory fee evidence is present."),
        _cost_row("broker_commission", "FAIL_CLOSED_ACCOUNT_OR_PUBLIC_STATIC_SOURCE_NOT_LOCKED", "No broker-specific futures commission lock is present."),
        _cost_row("zn_tick_value_and_multiplier", "FAIL_CLOSED_CONTRACT_SPEC_REASSERTION_REQUIRED_FOR_LOCKBOX_COST", "Prior mechanics used ZN multiplier, but Lockbox cost readiness requires explicit static cost-spec reassertion."),
        _cost_row("spread_slippage_grid", "FAIL_CLOSED_SCENARIO_GRID_DEFINED_NOT_EXECUTED", "Scenario grid is defined but not applied to unit and M1 variants."),
        _cost_row("limit_order_fill_model", "FAIL_CLOSED_FILL_MODEL_DEFINED_NOT_EXECUTED", "Carver fast mean reversion limit-order semantics are not executable for Lockbox yet."),
        _cost_row("routing_and_margin_funding", "FAIL_CLOSED_DISPOSITION_NOT_LOCKED", "Routing and margin/funding treatment is not locked."),
        _cost_row("breakeven_cost_per_side", "FAIL_CLOSED_NOT_COMPUTED_WITH_FUTURES_REALISTIC_COSTS", "Breakeven cost per side has not been computed under locked futures costs."),
        _cost_row("unit_and_m1_ladder_cost_sensitivity", "FAIL_CLOSED_NOT_EXECUTED", "Unit/no-ladder and M1 ladder variants have not been sensitivity-tested under futures-realistic costs."),
        _cost_row("cfd_or_prop_adapter_substitution", "PASS_REJECTED_REQUIRES_SEPARATE_ADAPTER_GATE", "No CFD/prop costs may substitute for source-native futures costs."),
    ]


def _cost_row(component: str, status: str, note: str) -> dict[str, str]:
    return {
        "gate": GATE,
        "lane": LANE,
        "component": component,
        "cost_readiness_status": status,
        "lockbox_effect": "BLOCKS_LOCKBOX_OPENING" if status.startswith("FAIL_CLOSED") else "DOES_NOT_CLOSE_COST_READINESS_BY_ITSELF",
        "notes": note,
    }


def _window_rows() -> list[dict[str, Any]]:
    scan_matches = _selected_s27_zn_date_string_matches("2025-")
    rows: list[dict[str, Any]] = []
    for item in TOUCHED_EVIDENCE:
        rows.append(
            {
                "gate": GATE,
                "lane": LANE,
                "window_label": item["window_label"],
                "date_start": item["date_start"],
                "date_end": item["date_end"],
                "window_status": item["disposition"],
                "lockbox_eligible": "NO",
                "data_access_authorized": "NO",
                "notes": "Already touched by current S27 ZN development/reconciliation evidence stack.",
            }
        )
    rows.append(
        {
            "gate": GATE,
            "lane": LANE,
            "window_label": "2011_2026_DAILY_SIGNAL_RUNTIME_SUPPORT_HISTORY",
            "date_start": "2011-01-02",
            "date_end": _daily_runtime_touch_boundary(),
            "window_status": "TOUCHED_DAILY_SIGNAL_RUNTIME_SUPPORT_HISTORY_NOT_LOCKBOX_ELIGIBLE",
            "lockbox_eligible": "NO",
            "data_access_authorized": "NO",
            "notes": f"Selected S27 ZN artifact scan found {scan_matches} pre-existing '2025-' string matches; daily signal/runtime support history reaches this boundary.",
        }
    )
    rows.append(
        {
            "gate": GATE,
            "lane": LANE,
            "window_label": "2026_POST_TOUCH_FORWARD_LOCKBOX_ACCUMULATION_CANDIDATE",
            "date_start": "2026-05-23",
            "date_end": "2026-12-31",
            "window_status": "FUTURE_INCOMPLETE_CANDIDATE_UNTOUCHED_NOT_AVAILABLE_FOR_EXECUTION",
            "lockbox_eligible": "CONDITIONALLY_YES_AFTER_COMPLETION_COST_READINESS_AND_SEPARATE_AUTHORIZATION",
            "data_access_authorized": "NO",
            "notes": "Earliest strict candidate after the current daily signal/runtime touch boundary; incomplete as of this gate and not executable now.",
        }
    )
    return rows


def _pass_fail_rows() -> list[dict[str, str]]:
    return [
        _rule("variant_identity", "S27_ZN_SOURCE_NATIVE_M1_LADDER_ONLY", "No symbol, parameter, ladder, or source-line change after this readiness freeze."),
        _rule("lane", LANE, "Exactly one lane; no CFD_DIRECT or CFD_ADAPTER in Lockbox execution."),
        _rule("window", "POST_2026_05_22_UNTOUCHED_WINDOW_ONLY", "Exclude 2022-2023, 2024, and all dates touched by daily signal/runtime support history through 2026-05-22."),
        _rule("cost_precondition", "FUTURES_REALISTIC_COST_READINESS_MUST_PASS_BEFORE_LOCKBOX", "Current readiness decision blocks Lockbox until this is satisfied."),
        _rule("primary_metric", "SIGNAL_ATTRIBUTABLE_M1_MINUS_MATCHED_AVG_ABS_BETA_NET_OF_FUTURES_COSTS", "Raw net PnL is secondary only."),
        _rule("primary_threshold", "PRIMARY_SIGNAL_ATTRIBUTABLE_NET_PNL_GT_0", "Must hold after futures-realistic costs."),
        _rule("mcpt_threshold", "PRIMARY_NULL_P_LE_0_05_AND_MAX_T_ADJUSTED_P_LE_0_10", "Same family-wise correction discipline as pre-Lockbox MCPT."),
        _rule("secondary_sanity", "NO_DELAYED_OR_INVERTED_SIGNAL_EXPLAINS_RESULT", "Delayed and inverted/null contamination must remain non-explanatory."),
        _rule("data_quality", "NO_FILL_NO_DROP_NO_SUBSTITUTE_NORMAL_PROVIDER_CONDITION_ONLY", "Any degraded/unresolved row fails closed before statistics."),
        _rule("claim_boundary", "LOCKBOX_RESULT_NOT_PROMOTION_NOT_TRADING", "Pass, if ever achieved, authorizes no Forward/deployment/trading/promotion."),
    ]


def _rule(rule_id: str, locked_rule: str, notes: str) -> dict[str, str]:
    return {
        "gate": GATE,
        "lane": LANE,
        "rule_id": rule_id,
        "locked_rule": locked_rule,
        "rule_status": "PREDECLARED_FOR_LATER_LOCKBOX_GATE_NOT_EXECUTED",
        "notes": notes,
    }


def _status_payload(
    freeze_rows: list[dict[str, Any]],
    cost_rows: list[dict[str, Any]],
    window_rows: list[dict[str, Any]],
    pass_fail_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    missing_freeze = [row["artifact_path"] for row in freeze_rows if row["artifact_exists"] != "YES"]
    failing_costs = [row["component"] for row in cost_rows if str(row["cost_readiness_status"]).startswith("FAIL_CLOSED")]
    return {
        "gate": GATE,
        "run_id": RUN_ID,
        "created_at_utc": _z(datetime.now(timezone.utc)),
        "lane": LANE,
        "variant_freeze_status": "PASS_FREEZE_COMPLETE" if not missing_freeze else "FAIL_CLOSED_MISSING_FREEZE_ARTIFACTS",
        "missing_freeze_artifacts": missing_freeze,
        "cost_readiness_status": "FAIL_CLOSED_FUTURES_REALISTIC_COST_READINESS_NOT_EXECUTED",
        "failing_cost_components": failing_costs,
        "touched_windows_excluded": [
            "2022_2023_INITIAL_DEV_RECON",
            "2024_VALIDATION_STYLE",
            "2011_2026_DAILY_SIGNAL_RUNTIME_SUPPORT_HISTORY_THROUGH_2026-05-22",
        ],
        "candidate_lockbox_window": "NO_COMPLETED_UNTOUCHED_LOCKBOX_WINDOW_AVAILABLE_EARLIEST_STRICT_CANDIDATE_AFTER_2026-05-22",
        "predeclared_rule_count": len(pass_fail_rows),
        "lockbox_execution_gate_may_open": "NO",
        "lockbox_blocker": "FUTURES_REALISTIC_COST_READINESS_FAIL_CLOSED",
        "decision": "DO_NOT_OPEN_LOCKBOX_EXECUTION_GATE_YET",
        "data_access": "NO",
        "provider_api_access": "NO",
        "market_row_parsing": "NO",
        "diagnostics_or_backtest_run": "NO",
        "oos_lockbox_forward_access": "NO",
        "deployment_trading_promotion": "NO",
        "git_operations": "NO",
        "window_rows": window_rows,
    }


def _provenance_payload(status: dict[str, Any]) -> dict[str, Any]:
    return {
        "gate": GATE,
        "run_id": RUN_ID,
        "lane": LANE,
        "status": status["decision"],
        "source_artifacts": FREEZE_FILES,
        "process_docs": [
            str(PROCESS_DOC.relative_to(ROOT)),
            str(LOCAL_AUDIT_DOC.relative_to(ROOT)),
        ],
        "non_authorization": [
            "NO_DATA_ACCESS",
            "NO_PROVIDER_API_ACCESS",
            "NO_MARKET_ROW_PARSING",
            "NO_NEW_DIAGNOSTICS",
            "NO_NEW_BACKTEST",
            "NO_OOS",
            "NO_LOCKBOX_OPENED",
            "NO_FORWARD",
            "NO_CFD_ADAPTER",
            "NO_OLD_QUANTLAB_PIPELINE",
            "NO_TUNING",
            "NO_DEPLOYMENT",
            "NO_TRADING",
            "NO_PROMOTION",
            "NO_GIT_OPERATIONS",
        ],
    }


def _process_doc(status: dict[str, Any]) -> str:
    return f"""# Carver S27 ZN Lockbox Readiness Decision Gate

Status:

```text
{status["decision"]}
```

Gate: `{GATE}`

Lane:

```text
{LANE}
```

## Decision

Do **not** open the S27 ZN Lockbox execution gate yet.

Reason:

```text
{status["lockbox_blocker"]}
```

The exact source-native S27 ZN variant has been frozen for readiness review, and a candidate untouched Lockbox window is identified, but futures-realistic cost readiness is fail-closed because the current cost chapter is still a manifest/shape definition rather than an executed cost-readiness ledger.

## Frozen Variant

```text
S27_ZN_SOURCE_NATIVE_M1_LADDER_DEV_RECON_VARIANT
```

Frozen hash ledger:

```text
docs/researchops/s26_s27_lockbox_readiness/ZN_S27/{RUN_ID}/freeze/{RUN_ID}_variant_hash_freeze.csv
```

The freeze includes the source atom sheet, EWMAC/V/Q/M closure record, 2022-2023 dev/recon result, 2024 validation-style result, robustness summary, MCPT/null-stack summary, futures cost shape/manifest records, and the local audit tools used to produce the robustness and MCPT artifacts.

## Window Decision

Excluded as already touched:

```text
2022-01-01 through 2023-12-31
2024-01-01 through 2024-12-31
2011-01-02 through 2026-05-22 daily signal/runtime support history
```

Earliest strict candidate after the current touch boundary:

```text
2026-05-23 through 2026-12-31
```

That candidate is not a completed historical window as of this gate. This gate does not access that window, download it, parse it, or authorize any Lockbox run.

## Cost Readiness

Cost readiness:

```text
{status["cost_readiness_status"]}
```

Fail-closed cost components:

```text
{chr(10).join(status["failing_cost_components"])}
```

Machine-readable ledger:

```text
docs/researchops/s26_s27_lockbox_readiness/ZN_S27/{RUN_ID}/cost_readiness/{RUN_ID}_cost_readiness_ledger.csv
```

## Predeclared Later Lockbox Rules

Rules are frozen for a later separately authorized Lockbox gate but are not executed here:

- exact S27 ZN source-native M1 ladder variant only;
- post-2026-05-22 candidate window only, excluding touched 2022-2024 evidence and daily signal/runtime support history through 2026-05-22;
- futures-realistic costs must be locked before execution;
- primary metric is signal-attributable M1 minus matched-average-absolute-position beta, net of futures-realistic costs;
- primary signal-attributable net PnL must be positive;
- primary null `p <= 0.05` and max-T adjusted `p <= 0.10`;
- delayed/inverted/null contamination must not explain the result;
- no fill, drop, substitution, or degraded/unresolved provider rows;
- no promotion, Forward, deployment, or trading from a Lockbox pass.

## Non-Authorization

This decision gate authorizes no provider API access, no data download, no market-row parsing, no new diagnostics, no new backtest, no forecasts, no positions, no cost execution, no OOS, no Lockbox access, no Forward, no CFD adapter, no old QuantLab active pipeline, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.
"""


def _local_audit_doc(status: dict[str, Any]) -> str:
    blocking = "YES" if status["lockbox_execution_gate_may_open"] != "YES" else "NO"
    return f"""# Local Lean Hostile Audit - S27 ZN Lockbox Readiness Decision

Mode: automatic local lean hostile audit over process/readiness artifacts only. No provider API access, no data download, no market-row parsing, no diagnostics, no backtests, no Lockbox access, no Git operations.

## Findings

CRITICAL: Futures-realistic cost readiness remains fail-closed. The cost model is shape-defined but not executed, so Lockbox execution must not open.

HIGH: Touched evidence windows are correctly excluded: 2022-2023, 2024, and daily signal/runtime support history through 2026-05-22. The earliest strict candidate is future/incomplete and not executable now.

MEDIUM: Predeclared pass/fail rules are frozen for a later gate, but they are not executable until cost readiness passes.

LOW: None.

## Verdict

```text
BLOCKING_FINDINGS: {blocking}
AUDIT_DISPOSITION: {status["decision"]}
```
"""


def _selected_s27_zn_date_string_matches(needle: str) -> int:
    roots = [
        ROOT / "docs/process",
        ROOT / "docs/researchops/s26_s27_backtest_readiness/ZN_S27_SINGLE_INSTRUMENT",
        ROOT / "docs/researchops/s26_s27_validation/ZN_S27",
        ROOT / "docs/researchops/s26_s27_ladder_attribution/ZN_S27",
        ROOT / "docs/researchops/s26_s27_pre_lockbox_robustness/ZN_S27",
        ROOT / "docs/researchops/s26_s27_pre_lockbox_mcpt/ZN_S27",
    ]
    count = 0
    for root in roots:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if path.is_file() and path.suffix.lower() in {".md", ".csv", ".json", ".txt"}:
                if "lockbox_readiness" in str(path).lower():
                    continue
                try:
                    count += path.read_text(encoding="utf-8", errors="ignore").count(needle)
                except OSError:
                    continue
    return count


def _daily_runtime_touch_boundary() -> str:
    status_path = (
        ROOT
        / "docs/researchops/s26_s27_backtest_readiness/ZN_S27_SINGLE_INSTRUMENT/"
        / "2022-01-01_2023-12-31/local_extended_daily_runtime/status/"
        / "20260531_S27_ZN_2022_2023_LOCAL_EXTENDED_DAILY_RUNTIME_status.json"
    )
    if not status_path.exists():
        return "UNRESOLVED_DAILY_RUNTIME_STATUS_MISSING"
    payload = json.loads(status_path.read_text(encoding="utf-8"))
    return str(payload.get("extended_daily_end", "UNRESOLVED_DAILY_RUNTIME_END_MISSING"))


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def _write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8")


def _hash_tree(root: Path) -> dict[str, str]:
    return {
        str(path.relative_to(ROOT)): _sha256(path)
        for path in sorted(root.rglob("*"))
        if path.is_file() and path.name != f"{RUN_ID}_sha256.json"
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
