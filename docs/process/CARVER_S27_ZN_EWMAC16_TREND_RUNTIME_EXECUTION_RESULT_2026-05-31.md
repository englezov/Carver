# Carver S27 ZN EWMAC16 Trend Runtime Execution Result

Date: 2026-05-31

Status:

```text
PASS_S27_EWMAC16_TREND_RUNTIME_LEDGER_REAL_ZN_DEV_RECON_ONLY
```

## Scope

This result emits the S27 EWMAC16 trend-overlay runtime ledger for the ZN worked-example path.

It consumes:

```text
S26 extended hourly forecast-series-only rows
ZN local continuous daily Development/Reconciliation-only lineage
```

It emits one prevalidated EWMAC16 runtime row per S26 forecast row. It does not compute S27, diagnostics, backtests, positions, costs, carry, or strategy performance.

## Source Inputs

S26 forecast rows:

```text
docs/researchops/s26_s27_hourly_bridge/ZN_S26_WORKED_EXAMPLE/2026-04-13_2026-05-22/forecast_series_only_output/2026-05-31/forecast_rows/20260531_G_R1E_ZN_S26_EXTENDED_SIGMA_AND_FORECAST_SERIES_forecast_series_only.csv
```

ZN local continuous daily lineage:

```text
docs/researchops/s26_s27_hourly_bridge/ZN_S27_EWMAC16_TREND_DEPENDENCY/local_continuous_daily_lineage_2026-05-31/ledger/20260531_ZN_S27_EWMAC16_LOCAL_CONTINUOUS_DAILY_LIFECYCLE_REPAIR_series_dev_recon_only.csv
```

## Method

Book atom:

```text
S27 uses EWMAC(16,64) as the trend overlay.
```

Runtime rule:

```text
trend_fast_ewma = recursive EWMA span 16 over adjusted ZN daily closes
trend_slow_ewma = recursive EWMA span 64 over adjusted ZN daily closes
trend_forecast = trend_fast_ewma - trend_slow_ewma
```

No-lookahead policy:

```text
For each S26 hourly forecast row, use only local continuous daily rows with continuous_row_date strictly before the S26 row completed_trading_date.
```

## Output

Artifact root:

```text
docs/researchops/s26_s27_hourly_bridge/ZN_S27_EWMAC16_TREND_DEPENDENCY/ewmac16_trend_runtime_ledger_2026-05-31/
```

Core file:

```text
runtime_rows/20260531_ZN_S27_EWMAC16_TREND_RUNTIME_LEDGER_runtime_rows.csv
```

Counts:

```text
s26_forecast_rows = 686
trend_runtime_rows = 686
continuous_daily_rows = 175
```

Runtime status per row:

```text
PREVALIDATED_S27_EWMAC16_TREND_RUNTIME_VALUE
```

Output boundary:

```text
RUNTIME_LEDGER_ONLY_NOT_S27_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Current S27 Dependency Status

```text
S26 forecast-series-only rows: PASS
S27 EWMAC16 trend runtime ledger: PASS
S27 V/Q/M volatility runtime ledger: NOT_OPEN
S27 forecast-only handoff: BLOCKED_PENDING_V_Q_M_RUNTIME
S27 strategy test: NOT_OPEN
```

## Non-Authorization

This result authorizes no provider API access, no new data download, no market-row expansion, no S27 forecast computation, no diagnostics, no backtests, no positions, no costs, no carry, no OOS, no Lockbox, no Forward, no CFD adapter, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, and no Git operation.
