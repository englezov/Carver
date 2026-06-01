# Carver S27 ZN Source-Line And Robustness Precondition Gate

Status:

```text
PROCESS_ONLY_GATE_DRAFT_NOT_DATA_AUTHORIZATION
```

## Purpose

Define the next clean gate after the Opus pre-Lockbox hostile audit result:

```text
ROBUSTNESS_PROTOCOL_REQUIRED_BEFORE_LOCKBOX
```

This gate closes source ambiguity and statistical-claim ambiguity before any Lockbox naming, data access, or broader promotion. It keeps the current work in Development/Reconciliation.

## Lane

```text
SOURCE_NATIVE_FUTURES
```

## Inputs

Allowed inputs for this gate:

- current Carver process artifacts;
- current S27 ZN machine-readable artifacts already present in the workspace;
- local reference book `Carver.pdf` for source-line audit;
- existing local ZN 2022-2023 and 2024 artifacts only, if a later execution gate explicitly authorizes local parsing;
- no new provider data.

## Required Outputs

This gate expects four outputs before any Lockbox work can be discussed:

1. Source-line audit for S27 EWMAC(16,64) frame and trend-veto logic.
2. Source-line audit for V/Q/M attenuation formula, alignment, and runtime strict-prior behavior.
3. Robustness predeclaration for signal-attributable PnL and null tests.
4. Futures-realistic cost-model shape gate.

## Step 1 - Source-Line Audit For EWMAC Frame

The audit must resolve:

- whether Carver S27 applies EWMAC(16,64) on a daily or hourly frame;
- whether the local implementation matches that frame;
- whether the overlay is a veto/permission rule rather than a direction blender;
- whether the veto is applied before position construction, not after PnL is observed.

Required disposition:

```text
EWMAC16_FRAME_AND_VETO_LOGIC_LOCKED
```

or:

```text
EWMAC16_FRAME_AND_VETO_LOGIC_FAIL_CLOSED
```

## Step 2 - Source-Line Audit For V/Q/M

The audit must resolve:

- Carver source citation for V/Q/M volatility attenuation;
- the exact formula for V, Q, and M;
- EWMA smoothing rule;
- runtime alignment to hourly S27 forecast rows;
- strict-prior lag behavior;
- no use of same-bar or future volatility state.

Required disposition:

```text
V_Q_M_FORMULA_ALIGNMENT_AND_RUNTIME_LOCKED
```

or:

```text
V_Q_M_FORMULA_ALIGNMENT_AND_RUNTIME_FAIL_CLOSED
```

## Step 3 - Claim Restatement And Robustness Predeclaration

The claim under test must be frozen as:

```text
Carver S27 signal + M1 ladder position-sizing layer on ZN front-month hourly completed bars
```

The unit/no-ladder variant must remain separately reported as the closest local source-faithful comparator.

The primary metric must be:

```text
signal_attributable_net_pnl = total_net_pnl - constant_long_beta_strip_pnl
```

Required null and robustness checks:

- constant-long ZN beta strip at matched notional/exposure;
- random-position null with same absolute position distribution;
- shuffled signal null;
- one-bar delayed signal null;
- circular-shift signal/return null;
- stationary block bootstrap;
- sign-flip null;
- forecast bucket monotonicity;
- long/short asymmetry;
- trend-veto attribution;
- V/Q/M attenuation attribution;
- year/sub-period attribution.

Predeclaration must include:

- test list;
- primary and secondary statistics;
- trial counts;
- random seed policy;
- family-wise correction method;
- pass/fail thresholds;
- exact artifact hashes;
- one-run rule.

## Step 4 - Futures-Realistic Cost-Model Shape

The cost model must be designed before any Lockbox:

- commission;
- exchange and clearing fees;
- realistic ZN spread assumption;
- slippage sensitivity;
- limit-order non-fill model or fill-probability model;
- breakeven-cost analysis;
- explicit distinction between source-faithful execution claim and prop-firm/account-cost adaptation.

Required disposition:

```text
FUTURES_REALISTIC_COST_MODEL_SHAPE_LOCKED_NOT_EXECUTED
```

This gate does not execute costs against new data. It only defines the shape required before execution.

## 2024 Evidence Classification

2024 must remain:

```text
TEST_2_VALIDATION_STYLE_INFORMATIONALLY_TOUCHED_NOT_LOCKBOX
```

It may be used for pre-Lockbox robustness analysis only as an already-touched second sample. It must not be renamed untouched validation and must not become Lockbox.

## Exit Criteria

This gate is complete only when all of the following are true:

- EWMAC frame and veto logic are locked or fail-closed;
- V/Q/M formula and runtime alignment are locked or fail-closed;
- claim scope explicitly says S27 signal plus M1 ladder;
- unit/no-ladder and M1 ladder variants remain separated;
- robustness predeclaration exists before any new robustness run;
- futures-realistic cost-model shape exists before any Lockbox;
- 2024 remains informationally touched;
- no Lockbox window is named or opened.

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
