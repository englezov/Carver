# Carver S26 ZN Sigma Runtime And G_R1B Forecast-Only Execution Result

Date: 2026-05-31

Status:

```text
PASS_G_R1B_S26_ZN_HOURLY_FORECAST_OUTPUT_ONLY
```

## Scope

Operator opened the Databento-facing and sigma gates for the S26 ZN worked-example bridge.

This execution used existing local Carver Databento artifacts only. No new Databento API call, provider download, NinjaTrader export, Git operation, diagnostic, backtest, position, cost, carry, trend, S27 overlay, OOS, Lockbox, Forward, deployment, trading, or promotion was performed.

## Sigma Runtime

Runtime artifact:

```text
docs/researchops/s26_s27_hourly_bridge/ZN_S26_WORKED_EXAMPLE/2026-05-18_2026-05-22/sigma_percent_runtime/2026-05-31/runtime/20260531_G_R1B_ZNM6_sigma_percent_runtime_value.json
```

Source window:

```text
raw_symbol: ZNM6
instrument_id: 42000661
completed_daily_source_window: 2026-04-13 through 2026-05-21
source_rows: 34
returns: 33
provider_condition_policy: all rows ROW_READY_PROVIDER_CONDITION_NORMAL
same_day_daily_row_policy: 2026-05-22 daily row excluded to avoid lookahead for 2026-05-22T21:00:00Z
```

Method:

```text
SHORT_RUN_EWMA32_ANNUALIZED_PERCENT_RETURN_CURRENT_RISK_COMPONENT_FOR_S26_SIGMA_PRICE
```

Runtime value:

```text
sigma_percent_t: 0.04472077776691995
as_of: 2026-05-22T21:00:00Z
runtime_status: PREVALIDATED_S26_ZN_SIGMA_PERCENT_RUNTIME_VALUE
method_status: LOCKED_TO_PART_ONE_S03_VARIABLE_RISK_FAMILY
no_lookahead_status: PASS_NO_LOOKAHEAD
source_window_status: PASS_SOURCE_WINDOW_PREVALIDATED
```

Important limitation:

```text
NOT_FULL_S03_POSITION_SIZING_BLEND
```

The runtime value is the short-run EWMA(32) annualized percentage-return current-risk component used to form S26 `sigma_price_t = price_t * sigma_percent_t / 16`. It is not a full S03 position-sizing risk estimate and does not authorize position sizing.

## Forecast-Only Output

Forecast artifact:

```text
docs/researchops/s26_s27_hourly_bridge/ZN_S26_WORKED_EXAMPLE/2026-05-18_2026-05-22/forecast_only_output/2026-05-31/forecast_rows/20260531_G_R1B_ZNM6_S26_forecast_output_only.csv
```

Output:

```text
forecast_rows_emitted: 1
accepted_hourly_rows_consumed: 115
forecast_output_status: S26_FORECAST_OUTPUT_ONLY_NOT_DIAGNOSTIC_NOT_BACKTEST_NOT_POSITION
capped_forecast: -0.995560007091342
```

The row contains only S26 forecast fields:

```text
EWMA(5) equilibrium
raw forecast
sigma_percent
sigma_price
risk-adjusted forecast
scalar 9.3
scaled forecast
capped forecast
source/provenance hashes
```

## Hashes

Hash ledger:

```text
docs/researchops/s26_s27_hourly_bridge/ZN_S26_WORKED_EXAMPLE/2026-05-18_2026-05-22/forecast_only_output/2026-05-31/hashes/20260531_G_R1B_ZNM6_S26_forecast_output_only_sha256.txt
```

## Non-Authorization

This result authorizes no additional provider API access, no additional data download, no market-row expansion, no diagnostics, no backtests, no returns, no PnL, no Sharpe, no drawdown, no positions, no orders, no costs, no carry, no trend computation, no S27 overlay, no volatility/risk use beyond the explicitly recorded S26 sigma runtime value, no OOS, no Lockbox, no Forward, no CFD adapters, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.
