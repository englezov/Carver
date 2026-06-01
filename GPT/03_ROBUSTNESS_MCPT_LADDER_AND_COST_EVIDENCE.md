# Robustness, MCPT, Ladder, And Cost Evidence

## Robustness Stack

Status:

```text
PASS_S27_ZN_PRE_LOCKBOX_ROBUSTNESS_STACK_DEV_RECON_ONLY_NOT_MCPT_NOT_LOCKBOX
```

Scope:

```text
SOURCE_NATIVE_FUTURES
S27_SIGNAL_PLUS_M1_LADDER_NOT_PURE_CARVER_S27
WINDOW_SCOPED_2022_2023_AND_2024_SEPARATELY
NO_PROVIDER_API_ACCESS
NO_NEW_DATA_DOWNLOAD
NO_LOCKBOX_OPENED
NO_COMBINED_WINDOW_STATISTIC_USED_FOR_PASS_FAIL
```

Robustness summary:

| Window | Measure | Net PnL | Active rows | Gross PnL | Fees |
|---|---|---:|---:|---:|---:|
| 2022-2023 | UNIT_NO_LADDER | 1751.69 | 710 | 2968.75 | 1217.06 |
| 2022-2023 | M1_LADDER | 5342.63 | 2537 | 10343.75 | 5001.12 |
| 2022-2023 | Constant long 1 contract | -18992.91 | 11770 | -18968.75 | 24.16 |
| 2022-2023 | Matched avg abs beta strip | -6080.31 | 11770 | -6072.58 | 7.73 |
| 2022-2023 | Signal attributable M1 minus matched beta | 11422.94 | 2537 | 16416.33 | 4993.39 |
| 2024 | UNIT_NO_LADDER | 7296.47 | 666 | 8453.13 | 1156.66 |
| 2024 | M1_LADDER | 24618.82 | 2041 | 29968.75 | 5349.93 |
| 2024 | Constant long 1 contract | -5324.58 | 5918 | -5312.50 | 12.08 |
| 2024 | Matched avg abs beta strip | -3709.57 | 5918 | -3701.16 | 8.42 |
| 2024 | Signal attributable M1 minus matched beta | 28328.39 | 2041 | 33669.91 | 5341.51 |

Null summary examples:

| Window | Null | Net | Signal-attributable net |
|---|---|---:|---:|
| 2022-2023 | DELAYED_1_BAR | -10606.95 | -4526.64 |
| 2022-2023 | SHUFFLED_SIGNAL_SEED_20260601 | -2396.55 | 3683.77 |
| 2022-2023 | RANDOM_SIGN_SAME_ABS_POSITION_SEED_20260601 | -2875.64 | 3204.67 |
| 2022-2023 | INVERTED_SIGNAL | -15344.87 | -9264.56 |
| 2024 | DELAYED_1_BAR | 9151.58 | 12861.15 |
| 2024 | SHUFFLED_SIGNAL_SEED_20260601 | -5055.63 | -1346.06 |
| 2024 | RANDOM_SIGN_SAME_ABS_POSITION_SEED_20260601 | 6809.29 | 10518.86 |
| 2024 | INVERTED_SIGNAL | -35318.68 | -31609.11 |

Potential hostile issue: the 2024 delayed 1-bar and random-sign same-abs-position nulls remain positive. Opus should decide whether this suggests structural rate/beta/regime exposure, residual serial correlation, or an incomplete null design.

## MCPT Null Stack

Status:

```text
PASS_S27_ZN_PRE_LOCKBOX_MCPT_NULL_STACK_DEV_RECON_ONLY_NOT_LOCKBOX
```

Primary null families:

```text
CIRCULAR_SHIFT_SIGNAL
STATIONARY_BLOCK_BOOTSTRAP_RETURNS
SHUFFLED_SIGNAL
RANDOM_SIGN_SAME_ABS_POSITION
```

Secondary nulls:

```text
DELAYED_1_BAR
INVERTED_SIGNAL
```

Configuration:

```text
b_primary: 9999
stationary_mean_block_length: 24
seed: 3880699556
combined_window_statistic_used_for_pass_fail: NO
```

MCPT summary:

| Window | Observed signal-attributable net | Min primary unadjusted p | Max-T adjusted p | Interpretation |
|---|---:|---:|---:|---|
| 2022-2023 | 11422.94 | 0.1297 | 0.6215 | PRIMARY_TEST_WINDOW_NOT_SIGNIFICANT_NOT_LOCKBOX |
| 2024 | 28328.39 | 0.0004 | 0.0122 | TOUCHED_2024_MCPT_THRESHOLD_HIT_INFORMATIONAL_NOT_LOCKBOX |

Hostile interpretation request:

```text
Does a non-significant 2022-2023 window followed by a strong touched 2024 window and a negative 2025-2026 available-row window indicate regime-specificity, data/implementation sensitivity, or a strategy whose edge is too unstable for lockbox?
```

## Ladder Attribution

Status:

```text
PASS_S27_ZN_LADDER_ATTRIBUTION_AND_BASELINE_RECONCILIATION_NOT_LOCKBOX
```

The ladder is not pure Carver S27. It is an M1 sizing/ladder overlay tested on the same input rows as the unit/no-ladder variant.

Same-input results:

| Window | Unit net | M1 ladder net | M1 delta vs unit | Unit fee sides | M1 fee sides |
|---|---:|---:|---:|---:|---:|
| 2022-2023 | 1751.69 | 5342.63 | 3590.94 | 806 | 3312 |
| 2024 | 7296.47 | 24618.82 | 17322.36 | 766 | 3543 |
| 2025 | -6243.19 | -7222.12 | -978.93 | 844 | 4162 |
| 2026 through 2026-05-22 | -4199.26 | -18475.04 | -14275.78 | 401 | 2529 |

Hostile interpretation request:

```text
Is the M1 ladder a genuine source-consistent improvement, or is it a convex exposure amplifier that helped in 2024 and punished 2026?
```

## Cost Caveat

No futures-realistic cost model is locked. Every reported net is commission-only under the recorded ETF/public per-side policy and excludes futures spread/slippage/limit-order fill uncertainty.

Opus should decide whether any positive result remains meaningfully interpretable before futures-realistic costs are locked.
