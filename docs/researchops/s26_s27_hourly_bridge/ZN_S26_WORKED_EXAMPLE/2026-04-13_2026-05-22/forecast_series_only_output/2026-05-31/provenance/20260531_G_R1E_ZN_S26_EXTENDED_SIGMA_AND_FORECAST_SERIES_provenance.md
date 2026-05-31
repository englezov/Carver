# Carver S26 ZN Extended Sigma Runtime And Forecast-Series Provenance

Status:

```text
PASS_G_R1E_S26_ZN_EXTENDED_SIGMA_RUNTIME_LEDGER_AND_FORECAST_SERIES_ONLY
```

Gate: `G_R1E_ZN_S26_EXTENDED_NO_LOOKAHEAD_SIGMA_RUNTIME_LEDGER_AND_FORECAST_SERIES_ONLY`

Inputs:

- hourly quarantine CSV: `docs\researchops\s26_s27_hourly_bridge\ZN_S26_WORKED_EXAMPLE\2026-04-13_2026-05-22\databento_ohlcv_1h_extended_forecast_only_quarantine\sanitized_bars\20260531_G_R1D_ZN_S26_OHLCV_1H_EXTENDED_sanitized_quarantine_ohlcv_1h.csv`
- daily provider CSV: `docs\researchops\source_native_futures_daily_data_library\16_SYMBOL_FULL_DAILY_HISTORY\raw_provider_archive\DATABENTO\20260530_DATED_CONTRACT_FULL_AVAILABLE_HISTORY_PER_SYMBOL_CURRENT_IDS\raw_provider_output\databento_GLBX-MDP3_ohlcv-1d_ZNM6_42000661_full_available_provider.csv`
- canonical manifest: `docs\researchops\source_native_futures_daily_data_library\16_SYMBOL_DAILY_LIBRARY_PROMOTION_READINESS\manifest\CARVER_16_SYMBOL_DATABENTO_DAILY_LIBRARY_CANONICAL_MANIFEST_2026-05-30.csv`

Method:

- one no-lookahead sigma runtime per emitted S26 forecast row;
- latest 34 normal-provider-condition daily ZNM6 rows strictly before the forecast row's completed trading date;
- percentage returns over that 34-row window;
- EWMA(32) variance initialized from the first squared return and recursively updated;
- annualized with multiplier 16;
- S26 forecast fields only.

Boundary:

No diagnostics, backtests, returns, PnL, Sharpe, drawdown, positions, orders, fills, costs, carry, trend, S27 overlay, OOS, Lockbox, Forward, deployment, trading, promotion, Git operation, provider API access, or new data download.
