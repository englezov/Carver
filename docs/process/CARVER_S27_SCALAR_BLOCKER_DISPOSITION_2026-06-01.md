# Carver S27 Scalar Blocker Disposition

Date: 2026-06-01

Status:

```text
SCALAR_BLOCKER_RESOLVED_NOT_FAILING_S27_RESULT
```

## Scope

This record resolves the hostile-audit concern that S27 forecast rows used `forecast_scalar = 20.0` while S26 uses `9.3`.

No provider API access, no data download, no market-row parsing, no diagnostics, no backtest rerun, no positions, no costs, no tuning, no promotion, and no Git operation was performed for this disposition.

## Source Check

Source authority:

```text
Carver.pdf
```

Confirmed source atoms:

```text
S26 scalar: 9.3
Source: p. 480

S27 scalar: around 20 after the trend overlay and volatility multiplier
Source: p. 502

S27 cap: common forecast cap +/-20
```

The S27 `20.0` scalar is therefore not a cap mislabeled as a scalar and not an accidental reuse error. It is the source-faithful Chapter 27 scalar after the safer fast mean-reversion overlay turns the strategy off for a material share of observations.

## Machine Check

Current code constants:

```text
S26_FORECAST_SCALAR = 9.3
S27_FORECAST_SCALAR = 20.0
```

Current S27 paths scale with `S27_FORECAST_SCALAR`:

```text
s27_safer_fast_mean_reversion_forecast
s27_forecast_only_from_s26_forecast_row
```

The local lock labels were hardened so the S27 source lock no longer describes this as an inherited S26 scalar. The source lock now describes it as:

```text
S27 scalar around 20 and forecast cap
```

## Disposition

```text
OPUS_SCALAR_FINDING_STATUS: RESOLVED_BY_DIRECT_SOURCE_CHECK
S27_FORECAST_SCALAR_STATUS: SOURCE_FAITHFUL_20_0
S26_FORECAST_SCALAR_STATUS: SOURCE_FAITHFUL_9_3_UNCHANGED
BACKTEST_RESULT_SCALAR_STATUS: NOT_FAILED_BY_SCALAR_ATOM
```

This disposition does not bless the backtest as strategy-valid. It only resolves the scalar-specific blocker. Other open verification work remains governed by the existing parity, input-lineage, execution, cost, and window-control gates.

## Non-Authorization

This record authorizes no provider API access, no new data download, no market-row parsing, no diagnostics, no backtests, no forecasts on new data, no positions, no costs, no carry, no trend sleeve integration, no OOS, no Lockbox, no Forward, no CFD adapters, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.
