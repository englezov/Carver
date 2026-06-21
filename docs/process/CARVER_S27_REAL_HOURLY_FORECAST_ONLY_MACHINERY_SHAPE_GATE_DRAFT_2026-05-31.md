# Carver S27 Real-Hourly Forecast-Only Machinery Shape Gate Draft

Date: 2026-05-31

Status:

```text
PROCESS_ONLY_S27_REAL_HOURLY_FORECAST_ONLY_MACHINERY_SHAPE_GATE_DRAFT_NOT_TEST_AUTHORIZATION
```

## Purpose

Define the shape for building S27 real-hourly forecast-only machinery after S26 forecast-series machinery exists.

The later strategy test target is S27 first. This draft does not authorize that test.

## Source-Faithful S27 Dependency Chain

S27 depends on:

```text
S26 fast mean-reversion forecast
EWMAC(16,64) trend overlay
S13-style V/Q/M volatility attenuation
does-not-oppose-trend interaction
S27 scalar around 20 and inherited S26 cap +/-20
no forecast-combination FDM between fast mean reversion and trend
```

2026-05-31 source correction:

```text
S27_FORECAST_SCALAR = approximately 20 per p. 502 after applying the trend overlay and V/Q/M volatility multiplier.
S27 must not reuse the S26 scalar 9.3.
S27 still inherits the +/-20 forecast cap and the S26 execution methodology boundary.
```

## Required Real-Hourly Forecast-Only Inputs

A future S27 real-hourly forecast-only gate must consume only:

```text
source-native hourly completed bars
S26 forecast-only series rows
EWMAC(16,64) source-locked trend overlay inputs
V/Q/M volatility attenuation source-locked inputs
prevalidated sigma runtime values
provider-condition-normal rows or explicit fail-closed exclusions
```

Current plumbing implementation:

```text
S27 handoff consumes prevalidated S26 forecast rows plus prevalidated trend and V/Q/M runtime rows.
It does not calculate unresolved trend or V/Q/M dependencies internally.
S27 series handoff consumes the S26 forecast-only series plus exactly one trend runtime and one V/Q/M runtime per S26 forecast row.
S27 EWMAC16 trend runtime ledger plumbing validates prevalidated trend rows against the S26 forecast-only series; it does not compute real-data EWMAC16.
S27 V/Q/M volatility runtime ledger plumbing validates prevalidated attenuation rows against the S26 forecast-only series; it does not compute real-data S13-style V/Q/M, relative volatility, quantiles, or attenuation multipliers.
```

## Required Output Boundary

Allowed output:

```text
S27_FORECAST_OUTPUT_ONLY_NOT_DIAGNOSTIC_NOT_BACKTEST_NOT_POSITION
```

Allowed fields:

```text
S26 raw forecast
trend_fast_ewma
trend_slow_ewma
trend_forecast
vol_multiplier
opposes_trend
adjusted_raw_forecast
sigma_price
risk_adjusted_forecast
S27 scalar approximately 20
scaled_forecast
capped_forecast
source/provenance hashes
```

Forbidden fields:

```text
returns
PnL
Sharpe
drawdown
hit rate
turnover
positions
orders
fills
costs
portfolio weights
FDM
buffering
OOS
Lockbox
Forward
deployment
trading
promotion
```

## First Later Test Target

After this machinery exists and is hostile-audited, the first future strategy test gate should be:

```text
S27_FIRST_SOURCE_NATIVE_HOURLY_FORECAST_TO_TEST_GATE
```

That future gate must be separately authorized and must state the evidence window, instrument set, execution assumptions, cost status, and what remains closed.

## Non-Authorization

This draft authorizes no provider API access, no new data download, no market-row expansion, no real S27 computation, no diagnostics, no backtests, no returns, no PnL, no positions, no orders, no fills, no costs, no carry, no testing, no OOS, no Lockbox, no Forward, no CFD adapters, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.
