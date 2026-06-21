# Carver S26 ZN Hourly Forecast-Only Handoff Gate Draft

Date: 2026-05-30

Status:

```text
PROCESS_ONLY_CARVER_S26_ZN_HOURLY_FORECAST_ONLY_HANDOFF_GATE_DRAFT_NOT_AUTHORIZATION
```

## Purpose

Define the future handoff from a passed ZN hourly quarantine intake to S26 forecast-output-only computation.

This is not a forecast execution. It defines the strict prerequisites and output boundary for the fifth step of the active goal:

```text
FEED_QUARANTINED_ZN_HOURLY_BARS_INTO_S26_FORECAST_OUTPUT_ONLY
```

## Required Inputs

This gate may only proceed after these artifacts exist and pass:

```text
G_R1A_ZN_S26_WORKED_EXAMPLE_DATABENTO_OHLCV_1H_TINY_QUARANTINE_INTAKE: PASS
ZN hourly sanitized quarantine CSV: present
ZN hourly validation ledger: pass
ZN hourly provenance/status/hash artifacts: present
ZN session/trading-date mapping: pass
ZN provider-condition policy: pass or explicitly reviewed-not-applicable
S26 sigma_percent_t estimation atom: locked from source
```

Current status as of this draft:

```text
G_R1A_ZN_HOURLY_INTAKE: NOT_RUN_REQUIRES_OPERATOR_DATA_AUTHORIZATION
S26_SIGMA_PERCENT_SOURCE_METHOD: LOCKED_TO_PART_ONE_S03_VARIABLE_RISK_FAMILY
S26_SIGMA_PERCENT_RUNTIME_VALUE: NOT_AVAILABLE_REQUIRES_PREVALIDATED_RISK_ARTIFACT
FORECAST_OUTPUT_EXECUTION: BLOCKED
```

## S26 Forecast-Only Formula Boundary

Allowed formula fields:

```text
equilibrium_t = EWMA_span_5(hourly_close_t)
raw_forecast_t = equilibrium_t - hourly_close_t
sigma_price_t = hourly_close_t * sigma_percent_t / 16
risk_adjusted_forecast_t = raw_forecast_t / sigma_price_t
scaled_forecast_t = risk_adjusted_forecast_t * 9.3
capped_forecast_t = max(min(scaled_forecast_t, 20), -20)
```

The forecast output may use only the same S26 formula implementation already proven on synthetic hourly data, but with a separate real-data source-lock object that proves the quarantined input and sigma method are locked.

The `sigma_percent_t` method is source-locked in:

```text
docs/process/CARVER_S26_ZN_HOURLY_SIGMA_PERCENT_SOURCE_GATE_2026-05-30.md
```

That source gate locks the method only. A future forecast-output execution still needs a prevalidated runtime value whose own provenance proves timestamp alignment and no lookahead.

## Maximum Output Schema

```text
lane_class
strategy_id
strategy_context
row_id
author_market_code
instrument_id
raw_symbol
provider_ts_event_start_utc
derived_completed_bar_end_utc
completed_trading_date
price_close
equilibrium_ewma_5
raw_forecast
sigma_percent
sigma_price
risk_adjusted_forecast
forecast_scalar
scaled_forecast
capped_forecast
source_locks_status
forecast_output_status
source_hourly_quarantine_sha256
source_sigma_method_sha256
```

Allowed forecast-output status:

```text
S26_FORECAST_OUTPUT_ONLY_NOT_DIAGNOSTIC_NOT_BACKTEST_NOT_POSITION
```

## Explicitly Forbidden Outputs

The handoff must emit none of:

```text
returns
PnL
Sharpe
drawdown
hit rate
turnover
position size
contracts
orders
fills
costs
carry
trend forecast
S27 overlay
portfolio weights
risk target application
IDM
FDM
buffering
OOS/Lockbox/Forward labels
deployment or trading labels
```

## Fail-Closed Rules

The gate fails closed if:

- the hourly input is daily data or resampled daily data;
- the input contains a symbol other than ZN/`42000661`/`ZNM6`;
- any hourly row is missing required validation or provenance hashes;
- any timestamp is not a completed hourly bar;
- any target completed trading date lacks a locked session mapping;
- `sigma_percent_t` is supplied from an undocumented local convention;
- `sigma_percent_t` is estimated from only the five-day hourly intake window;
- `sigma_percent_t` is tuned after seeing output;
- S27 trend overlay, volatility attenuation, or portfolio integration is attempted;
- any diagnostic/backtest/performance/position artifact is produced.

## Next Gate After Pass

If this gate eventually passes, the next clean source-faithful chapter is not S27 or portfolio integration by default. The next chapter should be selected explicitly from:

```text
S26_SINGLE_INSTRUMENT_HOURLY_FORECAST_REVIEW_PACKET
S26_SMALL_HOURLY_INTAKE_SUBSET_SHAPE_GATE
S27_DEPENDENCY_LOCK_GATE_FOR_EWMAC16_AND_V_Q_M
```

## Non-Authorization

This draft authorizes no Databento access, no data download, no market-row parsing, no real-data forecast computation, no diagnostics, no backtests, no positions, no costs, no carry, no trend computation, no S27 overlay, no volatility/risk calculations, no OOS, no Lockbox, no Forward, no CFD adapters, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.
