# Carver S26 ZN Hourly G_R1B Forecast-Only Execution Provenance

Date: 2026-05-31

Status:

```text
PASS_G_R1B_S26_ZN_HOURLY_FORECAST_OUTPUT_ONLY
```

## Scope

Used the already quarantined G_R1A ZN hourly `ohlcv-1h` bars and a newly prevalidated ZN/ZNM6 sigma-percent runtime record. No new Databento API call was made in this execution.

## Sigma Runtime

- Source: Databento local daily ZNM6 `ohlcv-1d` archive, existing Carver artifact only.
- Source window: `2026-04-13` through `2026-05-21` completed trading dates.
- Provider condition: all source-window rows `ROW_READY_PROVIDER_CONDITION_NORMAL`.
- Same-day policy: excluded 2026-05-22 daily row to avoid lookahead for `2026-05-22T21:00:00Z`.
- Method detail: short-run EWMA(32) annualized percentage-return current-risk component in the Part One S03 variable-risk family. This is not a full S03 position-sizing blend and emits no position-sizing output.

## Forecast Boundary

Output is one S26 forecast row only. It contains no returns, PnL, Sharpe, drawdown, hit rate, turnover, positions, contracts, orders, costs, carry, trend, S27 overlay, OOS, Lockbox, Forward, deployment, trading, or promotion labels.
