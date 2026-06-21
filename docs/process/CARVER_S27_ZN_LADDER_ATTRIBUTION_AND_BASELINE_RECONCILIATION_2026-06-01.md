# Carver S27 ZN Ladder Attribution And Baseline Reconciliation

Status:

```text
PASS_S27_ZN_LADDER_ATTRIBUTION_AND_BASELINE_RECONCILIATION_NOT_LOCKBOX
```

## Frozen Claim

S27 ZN M1 ladder remains positive in 2022-2023 Development/Reconciliation and 2024 validation-style evidence; superseded candidate-comparison numbers are not governing.

## Same-Input Attribution

| Window | Variant | Rows | Gross | Fees | Net | Evidence Class |
|---|---|---:|---:|---:|---:|---|
| 2022_2023_INITIAL_DEV_RECON | UNIT_NO_LADDER_SAME_INPUT | 11770 | 2968.75 | 1217.06 | 1751.6900000000007 | DEVELOPMENT_RECONCILIATION_FROZEN_INITIAL_ZN_CLAIM |
| 2022_2023_INITIAL_DEV_RECON | M1_LADDER_SAME_INPUT | 11770 | 10343.75 | 5001.12 | 5342.630000000004 | DEVELOPMENT_RECONCILIATION_FROZEN_INITIAL_ZN_CLAIM |
| 2022_2023_INITIAL_DEV_RECON | DELTA_M1_LADDER_MINUS_UNIT_NO_LADDER | 11770 | 7375.0 | 3784.06 | 3590.940000000002 | DEVELOPMENT_RECONCILIATION_FROZEN_INITIAL_ZN_CLAIM |
| 2024_VALIDATION_STYLE | UNIT_NO_LADDER_SAME_INPUT | 5918 | 8453.125 | 1156.66 | 7296.465 | VALIDATION_STYLE_NON_LOCKBOX_RETAINED_NOT_PRISTINE_LOCKBOX |
| 2024_VALIDATION_STYLE | M1_LADDER_SAME_INPUT | 5918 | 29968.75 | 5349.93 | 24618.820000000003 | VALIDATION_STYLE_NON_LOCKBOX_RETAINED_NOT_PRISTINE_LOCKBOX |
| 2024_VALIDATION_STYLE | DELTA_M1_LADDER_MINUS_UNIT_NO_LADDER | 5918 | 21515.625 | 4193.27 | 17322.355 | VALIDATION_STYLE_NON_LOCKBOX_RETAINED_NOT_PRISTINE_LOCKBOX |

## Interpretation

The earlier +16517 candidate-comparison ZN result is superseded and is not the comparator. On the same strict-prior ZN row set, M1 ladder changes risk-scaled exposure and fees. It improves net PnL versus unit/no-ladder in both the 2022-2023 and 2024 same-input reconciliations.

The `+16517` ZN candidate-comparison result remains superseded and is not a governing benchmark. The fair comparator is same-input unit/no-ladder versus same-input M1 ladder.

## 2024 Evidence Classification

Decision: `VALIDATION_STYLE_NON_LOCKBOX_RETAINED_NOT_PRISTINE_LOCKBOX`.

2024 may remain validation-style, non-Lockbox evidence because the M1 ladder constants were frozen from the initial ZN run before the 2024 execution. It is not pristine Lockbox because the project has already observed ZN behavior and used 2024 in the research conversation.

## Lockbox Case

Lockbox case prepared: `YES_TINY_PREDECLARED_ZN_ONLY_CASE_READY_BUT_NOT_OPENED`.
Recommended next gate: `PROCESS_ONLY_TINY_ZN_LOCKBOX_SHAPE_GATE_BEFORE_ANY_LOCKBOX_DATA_ACCESS`.

The next gate must be process-only first: predeclare exact ZN window, inputs, costs, no-tuning rule, fail-closed handling, and success/failure reporting before any Lockbox data access. This artifact does not open Lockbox.

## Boundary

This reconciliation uses existing local ZN artifacts only. It performs no provider API access, no new data download, no OOS, no Lockbox, no Forward, no deployment, no trading, no promotion, and no Git operations.
