# Carver S27 ZN Forecast-Series-Only Execution Result

Date: 2026-05-31

Status:

```text
PASS_S27_ZN_REAL_HOURLY_FORECAST_SERIES_ONLY_NOT_TEST
```

## Gate

```text
S27_ZN_REAL_HOURLY_FORECAST_SERIES_ONLY_EXECUTION_NOT_TEST
```

## Scope

This execution created the S27 forecast-series-only artifact for the ZN worked-example path by consuming only prevalidated local artifacts:

```text
S26 forecast-series-only rows
S27 EWMAC16 trend runtime rows
S27 V/Q/M volatility attenuation runtime rows
```

No provider API access, new data download, new market-row expansion, diagnostics, backtests, returns/PnL statistics, positions, orders, fills, costs, carry, OOS, Lockbox, Forward, deployment, trading, promotion, or Git operations were performed by this execution.

## Result

```text
input_s26_forecast_rows: 686
trend_runtime_rows: 686
vqm_runtime_rows: 686
forecast_rows: 686
first_forecast_as_of: 2026-04-13T03:00:00Z
last_forecast_as_of: 2026-05-22T21:00:00Z
series_output_status: PASS_S27_REAL_HOURLY_FORECAST_SERIES_ONLY_HANDOFF_PLUMBING
```

Status artifact:

```text
docs/researchops/s26_s27_hourly_bridge/ZN_S27_FORECAST_SERIES_ONLY/2026-05-31/status/20260531_ZN_S27_FORECAST_SERIES_ONLY_status.json
```

Forecast rows:

```text
docs/researchops/s26_s27_hourly_bridge/ZN_S27_FORECAST_SERIES_ONLY/2026-05-31/forecast_rows/20260531_ZN_S27_FORECAST_SERIES_ONLY_forecast_series_only.csv
```

## Boundary

Allowed output:

```text
S27_FORECAST_OUTPUT_ONLY_NOT_DIAGNOSTIC_NOT_BACKTEST_NOT_POSITION
```

Explicitly absent:

```text
diagnostics
backtests
returns/PnL statistics
positions
orders
fills
costs
carry
strategy test
portfolio integration
OOS
Lockbox
Forward
deployment
trading
promotion
```

## Non-Authorization

This result authorizes no additional provider API access, no additional data download, no wider market-row expansion, no diagnostics, no backtests, no returns/PnL/Sharpe/drawdown, no positions, no orders, no fills, no costs, no carry, no strategy test, no OOS, no Lockbox, no Forward, no CFD adapters, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.
