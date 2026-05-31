# Carver S26 ZN Extended Sigma Runtime And Forecast-Series Execution Result

Date: 2026-05-31

Status:

```text
PASS_G_R1E_S26_ZN_EXTENDED_SIGMA_RUNTIME_LEDGER_AND_FORECAST_SERIES_ONLY
```

## Gate

```text
G_R1E_ZN_S26_EXTENDED_NO_LOOKAHEAD_SIGMA_RUNTIME_LEDGER_AND_FORECAST_SERIES_ONLY
```

## Scope

This execution used only existing local Carver artifacts:

```text
hourly input:
docs/researchops/s26_s27_hourly_bridge/ZN_S26_WORKED_EXAMPLE/2026-04-13_2026-05-22/databento_ohlcv_1h_extended_forecast_only_quarantine/sanitized_bars/20260531_G_R1D_ZN_S26_OHLCV_1H_EXTENDED_sanitized_quarantine_ohlcv_1h.csv

daily risk source:
docs/researchops/source_native_futures_daily_data_library/16_SYMBOL_FULL_DAILY_HISTORY/raw_provider_archive/DATABENTO/20260530_DATED_CONTRACT_FULL_AVAILABLE_HISTORY_PER_SYMBOL_CURRENT_IDS/raw_provider_output/databento_GLBX-MDP3_ohlcv-1d_ZNM6_42000661_full_available_provider.csv

daily readiness manifest:
docs/researchops/source_native_futures_daily_data_library/16_SYMBOL_DAILY_LIBRARY_PROMOTION_READINESS/manifest/CARVER_16_SYMBOL_DATABENTO_DAILY_LIBRARY_CANONICAL_MANIFEST_2026-05-30.csv
```

No provider API access, new data download, wider market-row parsing, diagnostics, backtest, position, cost, carry, trend, S27 overlay, OOS, Lockbox, Forward, deployment, trading, promotion, or Git operation was performed.

## Sigma Runtime Method

Method:

```text
SHORT_RUN_EWMA32_ANNUALIZED_PERCENT_RETURN_CURRENT_RISK_COMPONENT_FOR_S26_SIGMA_PRICE
```

This is the same method as the prior single-row G_R1B bridge and is not a full S03 position-sizing blend.

For each emitted S26 forecast row:

```text
source window: latest 34 normal-provider-condition ZNM6 daily rows strictly before the hourly row's completed trading date
returns: 33 daily percentage returns
EWMA span: 32
EWMA alpha: 2 / 33
variance initialization: first squared return
annualization multiplier: 16
no-lookahead: PASS
source_window_status: PASS_SOURCE_WINDOW_PREVALIDATED
```

Provider-condition policy:

```text
EXCLUDE_DEGRADED_ROWS_FROM_STRATEGY_FACING_CANDIDATE_SET_KEEP_QUARANTINED_WITH_LABELS
```

Excluded ZNM6 completed daily rows from the canonical manifest:

```text
2025-11-28
2026-03-15
2026-03-16
2026-04-10
2026-05-24
```

## Result

```text
input_hourly_rows: 690
sigma_runtime_rows: 686
forecast_rows: 686
first_forecast_as_of: 2026-04-13T03:00:00Z
last_forecast_as_of: 2026-05-22T21:00:00Z
daily_source_rows_available_normal: 168
daily_source_window_rows_per_runtime: 34
daily_source_returns_per_runtime: 33
series_output_status: PASS_G_R1C_S26_ZN_HOURLY_FORECAST_SERIES_ONLY
```

The final row matches the prior G_R1B single-row result:

```text
as_of: 2026-05-22T21:00:00Z
sigma_percent_t: 0.04472077776691995
capped_forecast: -0.995560007091342
```

## Artifact Root

```text
docs/researchops/s26_s27_hourly_bridge/ZN_S26_WORKED_EXAMPLE/2026-04-13_2026-05-22/forecast_series_only_output/2026-05-31/
```

Key artifacts:

```text
sigma_runtime_ledger/20260531_G_R1E_ZN_S26_EXTENDED_SIGMA_AND_FORECAST_SERIES_source_window_ledger.csv
sigma_runtime_ledger/20260531_G_R1E_ZN_S26_EXTENDED_SIGMA_AND_FORECAST_SERIES_runtime_ledger.csv
forecast_rows/20260531_G_R1E_ZN_S26_EXTENDED_SIGMA_AND_FORECAST_SERIES_forecast_series_only.csv
provenance/20260531_G_R1E_ZN_S26_EXTENDED_SIGMA_AND_FORECAST_SERIES_status.json
provenance/20260531_G_R1E_ZN_S26_EXTENDED_SIGMA_AND_FORECAST_SERIES_provenance.md
hashes/20260531_G_R1E_ZN_S26_EXTENDED_SIGMA_AND_FORECAST_SERIES_sha256.txt
```

## Helper

```text
tools/databento/carver_s26_zn_extended_sigma_and_forecast_series.py
```

The helper reads local CSV artifacts only, validates ZN/ZNM6 identity and daily-source hash alignment, creates the no-lookahead sigma runtime ledger, and calls the already tested S26 forecast-series-only machinery.

## Boundary

This result is:

```text
FORECAST_SERIES_ONLY_NOT_DIAGNOSTIC_NOT_BACKTEST_NOT_POSITION
```

## Non-Authorization

This result authorizes no additional provider API access, no additional data download, no wider market-row expansion, no diagnostics, no backtests, no returns/PnL/Sharpe/drawdown, no positions, no orders, no fills, no costs, no carry, no trend computation, no S27 real-data computation, no testing, no OOS, no Lockbox, no Forward, no CFD adapters, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.
