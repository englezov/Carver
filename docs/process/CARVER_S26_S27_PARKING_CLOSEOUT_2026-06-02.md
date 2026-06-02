# Carver S26/S27 Parking Closeout

Date: 2026-06-02

Status:

```text
S26_S27_PARKED_NOT_DELETED_NOT_PROMOTION
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Purpose

Close the current S26/S27 mean-reversion chapter for now, preserve the useful evidence, and prevent further rescue-by-tuning before opening the next source-native Carver chapter.

This is a process closeout. It does not authorize new data access, diagnostics, backtests, OOS, Lockbox, Forward, CFD adapter work, deployment, trading, promotion, Git operations, or remote operations.

## Controlling Decision

```text
S26_S27_STATUS: PARKED_NOT_DELETED
NEXT_RESEARCH_CHAPTER: S09_MULTIPLE_TREND_FOLLOWING_SOURCE_NATIVE_DAILY
GITHUB_CHECKPOINT_REQUIRED_BEFORE_S09: YES
```

The chapter is parked because the source-native evidence is mixed and not promotion-ready:

- S26 standalone did not clear as the stronger path.
- S27 ZN showed positive Development/Reconciliation evidence in earlier/touched windows.
- S27 ZN 2025-2026 produced a mechanically sound negative available-row diagnostic.
- S27 M1 ladder remains a local overlay rather than a Carver book atom.
- Futures-realistic cost and fill readiness remains fail-closed.
- Lockbox readiness remains closed.
- The old CFD/P27DO positive index result has been rejected for lookahead bias and is not Carver source-native evidence.

## Preserved Evidence

### Source Design And Initial Opus Verdict

```text
docs/process/CARVER_S26_S27_MEAN_REVERSION_OPUS_AUDIT_RESULT_2026-05-30.md
docs/process/CARVER_S26_S27_SOURCE_ATOM_SHEET_2026-05-30.md
```

Initial Opus disposition:

```text
SOURCE_PATH_DEFINED_BUT_BLOCKED_AT_FIRST_REAL_DATA_GATE_BY_FREQUENCY
```

### Positive / Mixed Development Evidence

```text
docs/process/CARVER_S27_ZN_TOUCHED_HISTORY_DEV_RECON_BACKTEST_RESULT_2026-06-01.md
docs/process/CARVER_S27_ZN_PRE_LOCKBOX_ROBUSTNESS_STACK_RESULT_2026-06-01.md
docs/process/CARVER_S27_ZN_2024_VALIDATION_BACKTEST_RESULT_2026-06-01.md
```

Interpretation:

```text
USEFUL_DEV_RECON_EVIDENCE_NOT_LOCKBOX_NOT_PROMOTION
```

### Negative 2025-2026 Evidence

```text
docs/process/CARVER_S27_ZN_2025_2026_TOUCHED_SUPPORT_DEV_RECON_BACKTEST_RESULT_2026-06-01.md
docs/process/CARVER_S27_ZN_2025_2026_NEGATIVE_RESULT_OPUS_HOSTILE_AUDIT_2026-06-02.md
```

Opus negative-result verdict:

```text
MECHANICAL_RESULT_STATUS: SOUND
NEGATIVE_RESULT_INTERPRETATION: AVAILABLE_ROW_DIAGNOSTIC_ONLY
S27_PARKING_DECISION_SUPPORT: MODERATE
CONFIDENCE: MEDIUM
```

Key Opus explanation:

```text
The negative result is not a mechanical bug. It is a real available-row diagnostic with a robust fragility warning attached, but remains fail-closed as a complete-window backtest because of provider-degraded dates and other non-promotion boundaries.
```

### Prior Robustness / Pre-Lockbox Opus Findings

```text
docs/process/CARVER_S27_ZN_PRE_LOCKBOX_OPUS_HOSTILE_AUDIT_RESULT_2026-06-01.md
docs/process/CARVER_S27_ZN_ROBUSTNESS_OPUS_AUDIT_RESULT_2026-06-01.md
```

Controlling blockers:

```text
FUTURES_REALISTIC_COST_READINESS_FAIL_CLOSED
LADDER_NON_SOURCE_NATIVE_OVERLAY_CONFIRMED
NULL_SUFFICIENCY_NOT_CLOSED
2024_INFORMATIONALLY_TOUCHED_NOT_LOCKBOX
2025_2026_AVAILABLE_ROW_DIAGNOSTIC_ONLY
```

## S26/S27 Final Interpretation

```text
S26_SOURCE_NATIVE_STATUS:
  TESTED_DEV_RECON_COMPARISON_ONLY
  NOT_PROMOTION_READY
  PARKED_WITH_FAILURE_INFORMATION_PRESERVED

S27_SOURCE_NATIVE_STATUS:
  MECHANICALLY_COHERENT_FOR_DEV_RECON
  NOT_LOCKBOX_READY
  NOT_PROMOTION_READY
  PARKED_NOT_DELETED

M1_LADDER_STATUS:
  LOCAL_OVERLAY
  NOT_CARVER_BOOK_ATOM
  AMPLIFIES_BOTH_POSITIVE_AND_NEGATIVE_WINDOWS

CFD_INDEX_RESULT_STATUS:
  REJECTED_LOOKAHEAD_BIAS
  NOT_SOURCE_NATIVE_EVIDENCE
```

## What Would Be Required To Reopen S27 Later

S27 should not be reopened casually. A later reopening would need a separate explicit gate that closes, at minimum:

- provider-clean complete-window evidence;
- futures-realistic spread, slippage, exchange, clearing, broker, and fill assumptions;
- source-faithful treatment of Carver's limit-order execution statement;
- whether the M1 ladder is excluded from the source-faithful reference run or explicitly moved to an adapter/overlay lane;
- mechanical and parity verifier rerun on any reopened evidence window;
- signal-attributable PnL net of beta/exposure baselines;
- null-test predeclaration before seeing new results.

## Next Step

After this closeout:

```text
1. GitHub checkpoint publication gate for completed S26/S27 chapter.
2. Open S09 implementation planning/source-atom gate.
3. Implement S09 from the book, not by inheriting S27/V/Q/M-contaminated trend code.
```

The GitHub checkpoint remains a critical remote operation and requires operator authorization.

## Non-Authorization

This closeout authorizes no provider API access, no data download, no market-row parsing, no diagnostics, no backtests, no forecasts on new data, no positions on new data, no costs, no carry, no trend computation on new data, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.
