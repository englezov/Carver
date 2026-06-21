# Requested Output And Hostile Checklist

Date: 2026-06-02

Status:

```text
PROCESS_ONLY_REQUESTED_OUTPUT_SPEC_NOT_AUTHORIZATION
```

## Required Audit Posture

Be hostile. Do not assume the negative S27 ZN 2025-2026 result is correct just because it is inconvenient. The task is to attack it for possible mistakes.

At the same time, do not rescue S27 by hand-waving away negative evidence. If the result is mechanically sound but fail-closed as a complete-window backtest, say that plainly.

## Core Questions

1. Could the negative 2025-2026 result be caused by a bug in:
   - roll lineage;
   - additive adjustment;
   - inactive-contract exclusion;
   - daily runtime alignment;
   - V/Q/M lagging;
   - EWMAC(16,64) trend veto alignment;
   - S26 raw forecast calculation;
   - scalar/cap application;
   - position generation;
   - M1 ladder construction;
   - PnL sign convention;
   - multiplier/tick scaling;
   - fee-side accounting;
   - provider-condition exclusion policy;
   - partial-year end handling?

2. Does every 2025-2026 hourly forecast use only prior completed daily state?

3. Does every backtest PnL row use the intended next-hour or post-signal price interval, never same-bar/future information?

4. Are the four blocked dependency rows expected, or do they indicate a missing-start/end alignment bug?

5. Does the 8093 forecast row count, 8092 same-input backtest row count, and 8097 local continuous hourly row count reconcile cleanly?

6. Are the six degraded provider dates handled correctly? Could excluding them distort the result materially? Should they make the result unusable, or merely available-row diagnostic evidence?

7. Why does the M1 ladder have a positive daily win rate but strongly negative net/gross PnL in 2026? Does this indicate tail loss, sign inversion, fee amplification, ladder asymmetry, or a calculation problem?

8. Are the 2025 and 2026 partial-year losses internally consistent with the earlier 2022-2024 positive records, or is there an implementation discontinuity after 2024?

9. Are the comparator surfaces apples-to-apples? If not, identify exactly which labels/surfaces differ.

10. Does this result strengthen the case to park S27, or is it unresolved pending a cleaner rerun?

## Required Findings Format

Return findings ordered by severity:

```text
CRITICAL
HIGH
MEDIUM
LOW
INFORMATIONAL
```

For each finding provide:

- exact file/path inside the packet or zip;
- evidence;
- why it matters;
- whether it could flip the 2025-2026 interpretation;
- required fix or evidence needed.

## Required Verdict

End with:

```text
MECHANICAL_RESULT_STATUS:
  SOUND | UNSOUND | UNRESOLVED

NEGATIVE_RESULT_INTERPRETATION:
  ROBUST_FRAGILITY_WARNING |
  AVAILABLE_ROW_DIAGNOSTIC_ONLY |
  DATA_POLICY_ARTIFACT |
  MECHANICAL_BUG_SUSPECTED |
  UNRESOLVED

S27_PARKING_DECISION_SUPPORT:
  STRONG | MODERATE | WEAK | NONE

CONFIDENCE:
  HIGH | MEDIUM | LOW
```

## Non-Authorization

This checklist authorizes no provider API access, no new data download, no market-row parsing beyond reading supplied evidence, no diagnostics, no backtests, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git operation, and no remote operation.
