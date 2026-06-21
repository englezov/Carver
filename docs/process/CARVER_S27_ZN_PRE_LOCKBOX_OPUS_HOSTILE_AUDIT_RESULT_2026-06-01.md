# Carver S27 ZN Pre-Lockbox Opus Hostile Audit Result

Status:

```text
ROBUSTNESS_PROTOCOL_REQUIRED_BEFORE_LOCKBOX
```

## Scope

This record preserves the Opus hostile audit result for the Carver S27 ZN pre-Lockbox verification design. It is process-only. It performs no code execution, no data access, no provider call, no market-row parsing, no diagnostics, no backtest, no OOS, no Lockbox, no Forward, no tuning, no deployment, no trading, no promotion, and no Git operation.

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Preserved Opus Verdict

```text
BLOCKING_FINDINGS:
  - CRITICAL-1  Cost model not futures-realistic
  - CRITICAL-2  Shuffled-null contamination on 2022-23
  - CRITICAL-3  Headline claim is "S27 + M1 ladder", not pure Carver S27
  - HIGH-1      Delayed-null contamination on 2024
  - HIGH-2      EWMAC(16,64) trend-overlay frame ambiguous versus Carver S27
  - HIGH-3      V/Q/M attenuation atom not fully specified locally
  - HIGH-4      2024 is informationally touched and cannot be reclassified as untouched validation

AUDIT_DISPOSITION:
  ROBUSTNESS_PROTOCOL_REQUIRED_BEFORE_LOCKBOX

LOCKBOX_READY:
  NO
```

## Controlling Interpretation

The current S27 ZN machinery can remain mechanically useful Development/Reconciliation evidence, but it is not ready for Lockbox.

The governing claim must be stated as:

```text
Carver S27 signal + M1 ladder position-sizing layer on ZN
```

It must not be labeled as a pure Carver S27 result. The M1 ladder is a local overlay and is not a Carver book atom.

The 2024 window is reclassified as:

```text
TEST_2_VALIDATION_STYLE_INFORMATIONALLY_TOUCHED_NOT_LOCKBOX
```

Reason: inverted, delayed, shuffled, and related null evidence has already been observed on 2024. It remains useful as a second development/validation-style sample, but it is not pristine validation and not Lockbox.

## Blocking Findings Preserved

### CRITICAL-1 - Cost Model Not Futures-Realistic

The current cost model uses ETF/public per-side commission style assumptions. It does not yet lock realistic futures spread, slippage, limit-order fill quality, exchange fees, broker fees, routing, or margin/funding assumptions.

Disposition:

```text
FUTURES_REALISTIC_COST_MODEL_REQUIRED_BEFORE_LOCKBOX
```

### CRITICAL-2 - Shuffled-Null Contamination On 2022-23

Observed shuffled-null evidence on the 2022-2023 window recovers a large share of the headline net PnL. Opus interpreted this as evidence that raw net PnL may be contaminated by beta, long-bias, or ladder magnitude effects.

Required correction:

```text
RESTATE_PRIMARY_METRIC_AS_SIGNAL_ATTRIBUTABLE_NET_PNL
```

where signal-attributable net PnL means total net PnL less a constant-long ZN beta strip at matched notional/exposure.

### CRITICAL-3 - Claim Is S27 Signal Plus M1 Ladder

Same-input attribution shows the M1 ladder contributes materially to the result. The ladder is a local overlay and must be tested and reported separately from the unit/no-ladder source-faithful variant.

Disposition:

```text
CLAIM_SCOPE_MUST_EXPLICITLY_INCLUDE_M1_LADDER
UNIT_NO_LADDER_AND_M1_LADDER_VARIANTS_MUST_BE_SEPARATED
```

### HIGH-1 - Delayed-Null Contamination On 2024

The delayed one-bar null remains meaningfully positive on 2024. For a fast mean-reversion strategy, survival under a one-bar lag must be explained before Lockbox.

Disposition:

```text
DELAYED_NULL_CONTAMINATION_REQUIRES_ATTRIBUTION_BEFORE_LOCKBOX
```

### HIGH-2 - EWMAC(16,64) Trend-Overlay Frame Ambiguity

The trend overlay must be source-line audited against Carver S27. The audit must specify whether the EWMAC(16,64) overlay is daily or hourly, and must prove the local implementation matches the source interpretation.

Disposition:

```text
SOURCE_LINE_AUDIT_REQUIRED_FOR_EWMAC_FRAME_AND_VETO_LOGIC
```

### HIGH-3 - V/Q/M Attenuation Atom Not Fully Specified Locally

The V/Q/M volatility attenuation dependency must be locked with formula, alignment, runtime lag, and strict-prior behavior.

Disposition:

```text
SOURCE_LINE_AUDIT_REQUIRED_FOR_V_Q_M_FORMULA_ALIGNMENT_AND_RUNTIME
```

### HIGH-4 - 2024 Is Informationally Touched

2024 has already been used to observe null behavior. It cannot be treated as untouched validation or Lockbox.

Disposition:

```text
2024_RETAINS_VALIDATION_STYLE_INFORMATIONALLY_TOUCHED_STATUS
FUTURE_LOCKBOX_MUST_BE_SEPARATE_AND_UNTOUCHED
```

## Required Next Gate Sequence

Opus recommends the following order before any Lockbox gate:

1. Close EWMAC(16,64) frame ambiguity and V/Q/M source ambiguity through a source-line audit.
2. Land and SHA-pin a futures-realistic cost model.
3. Restate the claim using signal-attributable PnL net of a constant-long beta strip, then rerun shuffled and delayed nulls on 2022-2023 and 2024 against that restated metric.
4. Sign a Monte Carlo permutation/null-test predeclaration and a Lockbox predeclaration, with the claim scoped explicitly to S27 signal plus M1 ladder.
5. Only then name an untouched future ZN-only Lockbox candidate.

## Non-Authorization

This record authorizes none of the following:

```text
provider API access
new data download
market-row parsing
diagnostics
backtests
forecasts on new data
positions on new data
cost computation beyond process design
carry
trend sleeve combination
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
