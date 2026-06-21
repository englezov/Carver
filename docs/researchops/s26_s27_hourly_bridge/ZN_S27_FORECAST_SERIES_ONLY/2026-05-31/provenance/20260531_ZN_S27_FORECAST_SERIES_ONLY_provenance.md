# Carver S27 ZN Forecast-Series-Only Provenance

Status:

```text
PASS_S27_ZN_REAL_HOURLY_FORECAST_SERIES_ONLY_NOT_TEST
```

Gate: `S27_ZN_REAL_HOURLY_FORECAST_SERIES_ONLY_EXECUTION_NOT_TEST`

Inputs:

- S26 forecast-series-only rows: `docs\researchops\s26_s27_hourly_bridge\ZN_S26_WORKED_EXAMPLE\2026-04-13_2026-05-22\forecast_series_only_output\2026-05-31\forecast_rows\20260531_G_R1E_ZN_S26_EXTENDED_SIGMA_AND_FORECAST_SERIES_forecast_series_only.csv`
- S27 EWMAC16 trend runtime rows: `docs\researchops\s26_s27_hourly_bridge\ZN_S27_EWMAC16_TREND_DEPENDENCY\ewmac16_trend_runtime_ledger_2026-05-31\runtime_rows\20260531_ZN_S27_EWMAC16_TREND_RUNTIME_LEDGER_runtime_rows.csv`
- S27 V/Q/M volatility runtime rows: `docs\researchops\s26_s27_hourly_bridge\ZN_S27_V_Q_M_VOL_ATTENUATION\ten_year_vol_history_runtime_2026-05-31\runtime_rows\20260531_ZN_S27_V_Q_M_TEN_YEAR_VOL_RUNTIME_runtime_rows.csv`

Rows: `686`

Boundary:

Forecast-series-only artifact. No diagnostics, backtests, returns/PnL metrics, positions, orders, fills, costs, carry, strategy test, OOS, Lockbox, Forward, deployment, trading, promotion, Git, or remote repository operations.
