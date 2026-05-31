# Carver S27 ZN V/Q/M Ten-Year Vol Runtime Execution Result

Date: 2026-05-31

Status:

```text
PASS_S27_ZN_V_Q_M_TEN_YEAR_VOL_RUNTIME_LEDGER_DEV_RECON_ONLY
```

## Gate

```text
S27_ZN_V_Q_M_TEN_YEAR_VOL_HISTORY_DATABENTO_EXECUTION_OR_FAIL_CLOSED_DECISION
```

## Scope

This execution used Databento Historical only for ZN dated-contract daily `ohlcv-1d` rows needed to build the S27 V/Q/M volatility-attenuation runtime dependency for the existing S26 ZN forecast-series-only rows.

It did not run diagnostics, backtests, returns/PnL statistics, S27 strategy tests, positions, orders, fills, costs, carry, OOS, Lockbox, Forward, deployment, trading, promotion, or Git operations.

## Method

Runtime method:

```text
Strategy-3-style EWMA(32) annualized percentage sigma
ten-year rolling average: 2560 prior daily sigma observations
relative volatility V = sigma_i_t / ten_year_average_sigma
historical quantile Q of V with no lookahead
raw multiplier = 2 - 1.5 * Q
M = EWMA(10) of raw multiplier
hourly alignment: latest daily M strictly before each S26 hourly forecast row's completed trading date
```

Data policy:

```text
provider-condition AVAILABLE rows only
degraded/unresolved rows excluded from the local risk-history construction
local additive back-adjusted dated-contract chain
no provider-built continuous source authority
```

## Result

```text
contract_requests: 46
continuous_rows: 3527
sigma_rows: 3494
relative_vol_rows: 934
s26_forecast_rows: 686
runtime_rows: 686
first_runtime_as_of: 2026-04-13T03:00:00Z
last_runtime_as_of: 2026-05-22T21:00:00Z
```

Status artifact:

```text
docs/researchops/s26_s27_hourly_bridge/ZN_S27_V_Q_M_VOL_ATTENUATION/ten_year_vol_history_runtime_2026-05-31/status/20260531_ZN_S27_V_Q_M_TEN_YEAR_VOL_RUNTIME_status.json
```

Runtime artifact:

```text
docs/researchops/s26_s27_hourly_bridge/ZN_S27_V_Q_M_VOL_ATTENUATION/ten_year_vol_history_runtime_2026-05-31/runtime_rows/20260531_ZN_S27_V_Q_M_TEN_YEAR_VOL_RUNTIME_runtime_rows.csv
```

## Boundary

This result is a runtime dependency ledger only:

```text
PREVALIDATED_S27_V_Q_M_VOL_ATTENUATION_RUNTIME_VALUE
```

It is not a forecast test, strategy test, diagnostic, backtest, cost model, position model, portfolio integration, deployment, trading, or promotion artifact.

## Non-Authorization

This result authorizes no additional provider API access, no additional data download, no wider market-row expansion, no diagnostics, no backtests, no returns/PnL/Sharpe/drawdown, no positions, no orders, no fills, no costs, no carry, no strategy test, no OOS, no Lockbox, no Forward, no CFD adapters, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.
