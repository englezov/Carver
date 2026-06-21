# Carver S26 ZN Extended Hourly Forecast-Only Coverage Shape Gate Draft

Date: 2026-05-31

Status:

```text
PROCESS_ONLY_S26_ZN_EXTENDED_HOURLY_FORECAST_ONLY_COVERAGE_SHAPE_GATE_DRAFT_NOT_DATA_AUTHORIZATION
```

## Purpose

Define the next S26 ZN forecast-only coverage expansion before any S27 strategy test gate.

This draft does not request data and does not authorize provider access. It defines the exact shape a later data gate must use if the operator opens it.

## Locked Scope

Instrument identity:

```text
row_id: APPENDIX_C_172_004
author_market_code: ZN
Databento instrument_id: 42000661
raw_symbol: ZNM6
dataset: GLBX.MDP3
schema: ohlcv-1h
stype_in: instrument_id
```

Extended request envelope:

```text
request_start_utc: 2026-04-12T00:00:00Z
request_end_utc: 2026-05-23T00:00:00Z
target_completed_trading_dates: 2026-04-13 through 2026-05-22, weekdays only
target_completed_trading_date_count: 30
```

The original G_R1A target dates, `2026-05-18` through `2026-05-22`, must remain a strict subset of this extended window.

## Required Future Runtime Inputs

Any later forecast-series artifact execution must provide:

```text
quarantined ZNM6 ohlcv-1h rows only
one PREVALIDATED_S26_ZN_SIGMA_PERCENT_RUNTIME_VALUE per emitted forecast row
strict timestamp match between each sigma runtime and each completed hourly forecast row
source_window_status = PASS_SOURCE_WINDOW_PREVALIDATED
no_lookahead_status = PASS_NO_LOOKAHEAD
```

## Output Boundary

Allowed later output:

```text
S26 forecast fields only
```

Forbidden later output:

```text
diagnostics
backtests
returns
PnL
Sharpe
drawdown
positions
orders
fills
costs
carry
trend computation
S27 overlay
OOS
Lockbox
Forward
deployment
trading
promotion
```

## Fail-Closed Rules

Fail closed if a future artifact:

- uses any symbol other than Databento instrument `42000661` / `ZNM6`;
- uses continuous contracts or parent symbols instead of the locked dated contract;
- changes dataset, schema, selector, request envelope, target completed dates, or output root;
- omits the original G_R1A target dates;
- emits forecasts without one prevalidated no-lookahead sigma runtime per forecast row;
- estimates sigma from only the target hourly rows;
- silently drops, fills, interpolates, or reweights rows;
- emits diagnostics, backtests, positions, costs, trend, S27, or performance fields.

## Non-Authorization

This draft authorizes no provider API access, no new data download, no market-row parsing, no real forecast-series execution, no diagnostics, no backtests, no returns, no PnL, no positions, no orders, no fills, no costs, no carry, no trend computation, no S27 real-data computation, no testing, no OOS, no Lockbox, no Forward, no CFD adapters, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.

