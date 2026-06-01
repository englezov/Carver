# Carver S27 ZN Robustness Opus Audit Result

Date: 2026-06-01

Status:

```text
OPUS_AUDIT_RESULT_PRESERVED_PROCESS_ONLY_NOT_LOCKBOX_NOT_PROMOTION
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

Scope:

```text
S27_ZN_ROBUSTNESS_AND_RESULT_INTERPRETATION
```

## Audit Verdict

```text
BLOCKING_FINDINGS: YES
AUDIT_DISPOSITION: DEV_RECON_ONLY_BLOCKED_BEFORE_LOCKBOX_BY_COST_READINESS_NULL_SUFFICIENCY_AND_LADDER_SOURCE_FAITHFULNESS_NOT_PROMOTION
RECOMMENDED_NEXT_GATE: GATE_B_FUTURES_REALISTIC_COST_AND_FILL_READINESS_BEFORE_MORE_BACKTESTS
```

## Controlling Interpretation

The Opus audit finds that S27 ZN has cleared the earlier daily/hourly frequency mismatch for Development/Reconciliation purposes, but it has not cleared robustness, cost, ladder source-faithfulness, or Lockbox readiness.

The observed result pattern is:

```text
2022-2023:
  Positive but MCPT primary window not significant.

2024:
  Strongly positive, MCPT-significant, but touched / validation-style / not pristine Lockbox.

2025-2026:
  Negative available-row result; complete-window interpretation fail-closed because provider degraded dates exist.
```

No combined 2022-2026 statistic is admissible as pass/fail evidence.

## Core Findings

### Mechanical Soundness

```text
COHERENT_FOR_DEV_RECON_NOT_CLEARED_FOR_LOCKBOX
```

Hourly frequency now aligns with Carver Part Four / Strategy 27 requirements, but the audit does not consider source/mechanics risks fully closed. Remaining risks include:

```text
LOOKAHEAD_OR_SAME_BAR_EXECUTION_NOT_EXCLUDED
SESSION_OR_COMPLETED_BAR_ALIGNMENT_ERROR_NOT_EXCLUDED
S26_MEAN_REVERSION_FORMULA_NOT_INDEPENDENTLY_VERIFIED
S27_TREND_OVERLAY_OR_VQM_DEPENDENCY_NOT_INDEPENDENTLY_VERIFIED
```

### Robustness Evidence

```text
INSUFFICIENT
```

The 2024 delayed-one-bar null remains positive, and the 2024 random-sign same-absolute-position null remains positive. The audit interprets this as evidence that the 2024 result may be driven by exposure timing, intensity, structural rate regime, or residual serial behavior rather than a clean directional mean-reversion signal.

### Statistical Evidence

```text
WEAK_AND_WINDOW_SELECTED
```

The primary 2022-2023 Development/Reconciliation window is not MCPT-significant. The only significant MCPT window is 2024, which is touched / validation-style and not Lockbox.

### Ladder Source-Faithfulness

```text
LADDER_NON_SOURCE_NATIVE_OVERLAY_CONFIRMED
```

The audit treats the current M1 ladder as an empirical regime/exposure amplifier, not as a source-faithful Carver ladder. The ladder increases fee sides roughly fourfold and amplifies both favorable and unfavorable periods:

```text
2022-2023 delta M1 minus unit: +3590.94
2024 delta M1 minus unit:      +17322.36
2025 delta M1 minus unit:      -978.93
2026 H1 delta M1 minus unit:   -14275.78
```

The ladder must either be dropped from the inferential reference run or explicitly reconciled to Carver's source-described limit-order execution concept before it can carry evidentiary weight.

### Cost Readiness

```text
FAIL_CLOSED
```

All net results remain based on:

```text
ETF_PUBLIC_PER_SIDE_COMMISSION_ONLY_NO_SPREAD_NO_SLIPPAGE
```

Futures-realistic spread, slippage, limit-order fill uncertainty, and Carver speed-limit readiness are not locked.

### Data Quality

```text
MIXED_FAIL_CLOSED_ON_2025_2026
```

The 2025-2026 negative available-row result is not Lockbox-admissible because six degraded provider dates exist:

```text
2025-09-17
2025-09-24
2025-11-28
2026-03-15
2026-03-16
2026-04-10
```

The audit explicitly warns that fail-closed status is not exoneration. The negative available-row signature should be treated as evidence reserved and as a fragility warning, not as cleared or ignored.

## Required Next Gate

The controlling recommended next gate is:

```text
GATE_B_FUTURES_REALISTIC_COST_AND_FILL_READINESS_BEFORE_MORE_BACKTESTS
```

This gate is logically prior to more breadth tests, more windows, or Lockbox-shape work because current reported net PnL is uninterpretable under Carver source authority until futures-realistic costs and fill assumptions are locked.

## Gates That Remain Closed

```text
NO_NEW_PROVIDER_API_ACCESS
NO_NEW_DATA_DOWNLOAD
NO_NEW_MARKET_ROW_PARSING
NO_NEW_BACKTEST_EXECUTION
NO_TUNING
NO_OOS
NO_LOCKBOX
NO_FORWARD
NO_DEPLOYMENT
NO_TRADING
NO_PROMOTION
NO_GIT_OPERATIONS
NO_REMOTE_OPERATIONS
NO_CFD_ADAPTER
NO_OLD_QUANTLAB_ACTIVE_PIPELINE_USE
```

## Handoff

Next clean work should define and execute a process/source cost-and-fill readiness gate for S27 ZN before any additional backtest interpretation. The gate should decide, before reruns:

- source-faithful treatment of Carver's limit-order execution statement;
- whether M1 ladder is excluded from source-faithful reference results;
- commission, exchange, NFA, clearing, spread, slippage, and non-fill policy;
- whether costs can be bounded without tuning;
- whether Carver's fast-strategy cost speed-limit can be evaluated;
- how to label prior results after realistic costs are applied.

This record authorizes no data access, no backtest, no Git operation, no deployment, no trading, and no promotion.
