# Carver S27 ZN Pre-Lockbox MCPT Null Stack Result

Lane:

```text
SOURCE_NATIVE_FUTURES
```

Status:

```text
PASS_S27_ZN_PRE_LOCKBOX_MCPT_NULL_STACK_DEV_RECON_ONLY_NOT_LOCKBOX
```

## Scope

This run uses only existing local S27 ZN robustness input rows. It performs window-scoped MCPT-style primary null tests on signal-attributable net PnL. It is not Lockbox, not promotion, not a new data gate, and not a cost-model closeout.

## MCPT Summary

| Window | Observed signal-attributable net | Min primary p | Max-T adjusted p | Interpretation |
|---|---:|---:|---:|---|
| 2022_2023_INITIAL_DEV_RECON | 11422.9430739168 | 0.1297 | 0.6215 | PRIMARY_TEST_WINDOW_NOT_SIGNIFICANT_NOT_LOCKBOX |
| 2024_VALIDATION_STYLE | 28328.3913653262 | 0.0004 | 0.0122 | TOUCHED_2024_MCPT_THRESHOLD_HIT_INFORMATIONAL_NOT_LOCKBOX |

## Boundary

2022-2023 and 2024 remain separate evidence windows. 2024 remains informationally touched, not Lockbox. Futures-realistic costs remain unresolved and required before any Lockbox-facing interpretation.

## Non-Authorization

This result authorizes no provider API access, no new data download, no OOS, no Lockbox, no Forward, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.
