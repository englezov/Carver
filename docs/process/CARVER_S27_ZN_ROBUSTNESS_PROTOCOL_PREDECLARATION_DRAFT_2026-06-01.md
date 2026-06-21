# Carver S27 ZN Robustness Protocol Predeclaration Draft

Status:

```text
PROCESS_ONLY_ROBUSTNESS_PROTOCOL_PREDECLARATION_DRAFT_NOT_EXECUTED
```

## Purpose

Predeclare the robustness and null-test stack required by the Opus pre-Lockbox audit before any new statistical run. This draft exists to prevent robustness testing from becoming a tuning engine.

This is not a run result. It performs no data access, no market-row parsing, no diagnostics, no backtest, no new forecast execution, no position execution, no cost execution, no OOS, no Lockbox, no Forward, no promotion, and no Git operation.

## Lane And Claim

Lane:

```text
SOURCE_NATIVE_FUTURES
```

Claim under test:

```text
Carver S27 signal + M1 ladder position-sizing layer on ZN front-month hourly completed bars
```

Comparator that must remain separately reported:

```text
UNIT_NO_LADDER_SOURCE_FAITHFUL_COMPARATOR
```

Forbidden headline:

```text
PURE_CARVER_S27_WORKS_ON_ZN
```

## Evidence Windows

```text
2022-2023 = TEST_1_DEVELOPMENT_RECONCILIATION
2024      = TEST_2_VALIDATION_STYLE_INFORMATIONALLY_TOUCHED_NOT_LOCKBOX
future    = LOCKBOX_NOT_NAMED_NOT_OPENED
```

2024 may be used only as an already-touched second sample for pre-Lockbox robustness. It must not be treated as clean validation or Lockbox.

## Primary Metric

Primary metric:

```text
signal_attributable_net_pnl = total_net_pnl - constant_long_beta_strip_pnl
```

The constant-long beta strip must use a matched notional/exposure schedule sufficient to isolate ZN duration/beta drift from signal-direction edge. The exact construction must be SHA-pinned before execution.

Raw net PnL remains reportable only as a secondary descriptive number.

## Required Attribution Tests

The next execution gate must emit machine-readable ledgers for:

1. unit/no-ladder versus M1 ladder same-input attribution;
2. constant-long ZN beta strip;
3. signal-attributable PnL net of beta strip;
4. random-position null with the same absolute position distribution;
5. long/short contribution;
6. trend-veto on/off contribution;
7. V/Q/M attenuation contribution;
8. roll/contract-period attribution;
9. year and sub-period attribution.

## Required Mean-Reversion Structure Tests

The next execution gate must emit machine-readable ledgers for:

1. forecast bucket monotonicity;
2. extreme forecast reversal in the top absolute-forecast bucket;
3. edge half-life by forward holding horizon;
4. active versus flat contribution sanity;
5. long/short asymmetry;
6. PnL concentration by year, half-year, and contract segment.

## Required Null Tests

Primary null tests:

1. circular shift of signal versus forward returns;
2. stationary block bootstrap preserving local autocorrelation and volatility clustering;
3. shuffled signal null against signal-attributable PnL;
4. one-bar delayed signal null against signal-attributable PnL;
5. random-position null with same absolute position distribution.

Secondary null tests:

1. sign-flip null;
2. day-block permutation;
3. inverted signal mechanical sanity.

Rejected as primary:

```text
plain hourly return permutation
volatility-regime-conditioned permutation as strategy null
contract-segment permutation without boundary resynchronization
```

## Trial Counts And Randomness

Primary null trial count:

```text
B_PRIMARY = 9999
```

Secondary null trial count:

```text
B_SECONDARY = 1999
```

Random seed policy:

```text
DETERMINISTIC_SEED_FROM_PROTOCOL_ID_AND_ARTIFACT_HASHES
```

Seeds must be recorded in the run status artifact. Re-running with a different seed after observing a result is forbidden.

## Multiple-Test Correction

Required family-wise correction:

```text
MAX_T_OR_WESTFALL_YOUNG_STEPDOWN
```

Unadjusted p-values may be reported, but they are not sufficient for pass/fail.

## Draft Pass/Fail Shape

No final pass/fail threshold is executable until a later signed execution gate freezes:

- exact data artifact hashes;
- exact code SHA;
- exact cost model SHA;
- exact constant-long beta-strip method;
- exact statistic definitions;
- final p-value thresholds;
- exact family-wise correction implementation.

Minimum Opus-derived shape:

```text
primary signal-attributable net PnL > 0
primary null p <= 0.05
family-wise adjusted p <= 0.10
no secondary inversion
no unresolved shuffled-null contamination
no unresolved delayed-null contamination
```

## Futures-Realistic Cost Tests

Before Lockbox, the cost model must define and test:

- commission;
- exchange and clearing fees;
- realistic ZN bid/ask spread assumption;
- slippage grid;
- limit-order non-fill or fill-probability model;
- breakeven cost level;
- sensitivity of both unit/no-ladder and M1-ladder variants.

The current ETF/public per-side fee model is not sufficient for Lockbox.

## One-Run Rule

The robustness execution gate must be one-shot for each declared artifact/code combination. Any change after observing results creates a new protocol version and invalidates comparability.

## Exit Criteria Before Lockbox Can Be Discussed

All of the following must be true:

- EWMAC/VQM source-line ambiguities are closed or fail-closed;
- futures-realistic cost model is SHA-pinned;
- signal-attributable metric is implemented and reported;
- shuffled-null and delayed-null contamination are re-evaluated on signal-attributable PnL;
- 2024 remains informationally touched;
- MCPT/null protocol is signed before execution;
- claim remains scoped to S27 signal plus M1 ladder;
- unit/no-ladder comparator remains separate.

## Non-Authorization

This draft authorizes no:

```text
provider API access
new data download
market-row parsing
new diagnostics
new backtests
new forecasts
new positions
new cost computation
OOS
Lockbox
Forward
CFD adapters
old QuantLab active-pipeline use
tuning
deployment
trading
promotion
Git staging
commit
push
PR update
remote operations
```
