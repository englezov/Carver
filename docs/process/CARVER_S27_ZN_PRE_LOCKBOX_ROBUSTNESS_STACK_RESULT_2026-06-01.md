# Carver S27 ZN Pre-Lockbox Robustness Stack Result

Lane:

```text
SOURCE_NATIVE_FUTURES
```

Status:

```text
PASS_S27_ZN_PRE_LOCKBOX_ROBUSTNESS_STACK_DEV_RECON_ONLY_NOT_MCPT_NOT_LOCKBOX
```

## Scope

This execution uses only existing local ZN Development/Reconciliation artifacts. It emits robustness summaries and deterministic null summaries. It is not MCPT, not Lockbox, not promotion, and not a new backtest/data gate. The 2022-2023 and 2024 windows are reported separately; no combined-window statistic is used for pass/fail.

The matched-average-absolute-position beta strip is an attribution-only fractional exposure baseline, not a tradable position model.

## Summary

| Window | Measure | Net PnL | Gross PnL | Fees |
|---|---|---:|---:|---:|
| 2022_2023_INITIAL_DEV_RECON | UNIT_NO_LADDER | 1751.69 | 2968.75 | 1217.06 |
| 2022_2023_INITIAL_DEV_RECON | M1_LADDER | 5342.6299999997 | 10343.75 | 5001.1200000003 |
| 2022_2023_INITIAL_DEV_RECON | CONSTANT_LONG_ONE_CONTRACT_BETA_STRIP | -18992.91 | -18968.75 | 24.16 |
| 2022_2023_INITIAL_DEV_RECON | CONSTANT_LONG_MATCHED_AVG_ABS_POSITION_BETA_STRIP | -6080.3130733949 | -6072.5785891125 | 7.7344842824 |
| 2022_2023_INITIAL_DEV_RECON | SIGNAL_ATTRIBUTABLE_M1_MINUS_MATCHED_AVG_ABS_BETA | 11422.9430733946 | 16416.3285891125 | 4993.3855157179 |
| 2024_VALIDATION_STYLE | UNIT_NO_LADDER | 7296.465 | 8453.125 | 1156.66 |
| 2024_VALIDATION_STYLE | M1_LADDER | 24618.8199999998 | 29968.75 | 5349.9300000002 |
| 2024_VALIDATION_STYLE | CONSTANT_LONG_ONE_CONTRACT_BETA_STRIP | -5324.58 | -5312.5 | 12.08 |
| 2024_VALIDATION_STYLE | CONSTANT_LONG_MATCHED_AVG_ABS_POSITION_BETA_STRIP | -3709.571365358 | -3701.1553734688 | 8.4159918892 |
| 2024_VALIDATION_STYLE | SIGNAL_ATTRIBUTABLE_M1_MINUS_MATCHED_AVG_ABS_BETA | 28328.3913653578 | 33669.9053734688 | 5341.514008111 |

## Null Summaries

| Window | Null | Net | Signal-attributable net |
|---|---|---:|---:|
| 2022_2023_INITIAL_DEV_RECON | DELAYED_1_BAR | -10606.9500000003 | -4526.6369266054 |
| 2022_2023_INITIAL_DEV_RECON | SHUFFLED_SIGNAL_SEED_20260601 | -2396.5450000008 | 3683.7680733941 |
| 2022_2023_INITIAL_DEV_RECON | RANDOM_SIGN_SAME_ABS_POSITION_SEED_20260601 | -2875.6400000004 | 3204.6730733945 |
| 2022_2023_INITIAL_DEV_RECON | INVERTED_SIGNAL | -15344.8700000003 | -9264.5569266054 |
| 2024_VALIDATION_STYLE | DELAYED_1_BAR | 9151.5799999998 | 12861.1513653578 |
| 2024_VALIDATION_STYLE | SHUFFLED_SIGNAL_SEED_20260601 | -5055.6300000005 | -1346.0586346425 |
| 2024_VALIDATION_STYLE | RANDOM_SIGN_SAME_ABS_POSITION_SEED_20260601 | 6809.2899999997 | 10518.8613653577 |
| 2024_VALIDATION_STYLE | INVERTED_SIGNAL | -35318.6800000002 | -31609.1086346422 |

## Boundary

This result does not close Opus CRITICAL-1, CRITICAL-2, CRITICAL-3, HIGH-1, or HIGH-4. It provides the local robustness plumbing needed to evaluate those findings under a later signed MCPT/cost execution gate.

## Non-Authorization

This result authorizes no provider API access, no new data download, no OOS, no Lockbox, no Forward, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.
