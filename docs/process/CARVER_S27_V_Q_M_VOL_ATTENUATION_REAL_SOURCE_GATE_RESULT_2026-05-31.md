# Carver S27 V/Q/M Vol Attenuation Real Source Gate Result

Date: 2026-05-31

Status:

```text
FAIL_CLOSED_S27_V_Q_M_REAL_RUNTIME_SOURCE_TEN_YEAR_RELATIVE_VOL_DISTRIBUTION_NOT_AVAILABLE
```

## Gate

```text
S27_V_Q_M_VOL_ATTENUATION_REAL_HOURLY_SOURCE_GATE
```

## Purpose

Decide whether the current Carver workspace can source-faithfully emit the real S27 V/Q/M volatility attenuation runtime ledger aligned one-for-one to the existing S26 ZN extended hourly forecast-series-only rows.

This gate performs no new provider API access, no new data download, no new market-row parsing, no diagnostics, no backtests, no positions, no costs, no carry, no strategy test, and no promotion.

## Source Requirement

Source authority:

```text
Carver.pdf
```

The Chapter 27 S27 mechanism depends on the S13 volatility-regime method:

```text
current estimated percentage standard deviation sigma_i_t from Strategy 3
relative volatility V_i_t = current sigma_i_t / ten-year rolling average sigma for instrument i
Q_i_t = historical quantile point of V_i_t for the same instrument
raw multiplier input = 2 - 1.5 * Q_i_t
M_i_t = EWMA span 10 of the raw multiplier input
adjusted raw forecast = S26 raw forecast * M_i_t before S27 scalar/cap path
```

Source locations:

```text
S13 volatility-regime method: p. 301
S27 restatement and ten-year rolling-average relation: pp. 501-502
S27 scalar correction after overlay and V/Q/M: p. 502
```

## Evidence Inspected

Existing S26 extended forecast-series-only output:

```text
docs/researchops/s26_s27_hourly_bridge/ZN_S26_WORKED_EXAMPLE/2026-04-13_2026-05-22/forecast_series_only_output/2026-05-31/
```

Existing S26 sigma runtime method:

```text
SHORT_RUN_EWMA32_ANNUALIZED_PERCENT_RETURN_CURRENT_RISK_COMPONENT_FOR_S26_SIGMA_PRICE
source window: latest 34 normal-provider-condition ZNM6 daily rows strictly before each hourly forecast row's completed trading date
```

Existing S27 V/Q/M plumbing:

```text
src/carver/spine/s26_s27.py
docs/process/CARVER_S27_V_Q_M_VOL_ATTENUATION_RUNTIME_LEDGER_PLUMBING_RESULT_2026-05-31.md
```

## Decision

```text
S27_V_Q_M_REAL_RUNTIME_LEDGER: NOT_EMITTED
S27_V_Q_M_SOURCE_STATUS: FAIL_CLOSED_TEN_YEAR_RELATIVE_VOL_DISTRIBUTION_NOT_AVAILABLE
```

Reason:

The existing S26 sigma runtime rows provide current short-run sigma inputs for the S26 forecast denominator only. They do not provide:

```text
ten-year rolling average sigma_i_t
historical distribution of relative volatility V_i_t
historical quantile Q_i_t
EWMA(10) multiplier M_i_t from source-complete Q_i_t rows
```

The current local ZN daily lineage repair provides a Development/Reconciliation daily continuous series for the EWMAC16 trend dependency, but it is only a short local roll repair surface. It is not a ten-year source-native continuous risk history and must not be used to fabricate Q.

## Forbidden Substitutions

This gate explicitly rejects:

```text
NO_NEUTRAL_VOL_MULTIPLIER_1_0_AS_REAL_S27_RUNTIME
NO_CURRENT_S26_SIGMA_RUNTIME_AS_Q
NO_34_ROW_SIGMA_WINDOW_AS_TEN_YEAR_HISTORY
NO_SHORT_DATED_ZNM6_HISTORY_AS_TEN_YEAR_RELATIVE_VOL_DISTRIBUTION
NO_PROVIDER_BUILT_CONTINUOUS_SYMBOL_AS_SOURCE_AUTHORITY_WITHOUT_SEPARATE_GATE
NO_S27_FORECAST_SERIES_EXECUTION_WITHOUT_V_Q_M_RUNTIME
```

## Next Required Gate

```text
S27_ZN_V_Q_M_TEN_YEAR_VOL_HISTORY_AND_RUNTIME_SHAPE_GATE
```

Minimum requirement:

```text
Build or fail-close a source-native ZN daily risk-history foundation sufficient to compute Strategy-3-style sigma_i_t, ten-year rolling average sigma, historical V_i_t quantile Q_i_t, and EWMA(10) M_i_t with strict no-lookahead alignment to the S26 hourly forecast rows.
```

The future gate must define:

```text
data source
exact instrument/root and contract lineage
roll/back-adjustment policy
history start/end
provider-condition policy
sigma_i_t method
ten-year rolling-average method
historical quantile method
hourly alignment policy
output boundary: runtime ledger only, not S27 forecast/test
```

## Non-Authorization

This result authorizes no provider API access, no new data download, no new market-row parsing, no diagnostics, no backtests, no returns, no PnL, no forecasts beyond existing S26 forecast-only artifacts, no S27 forecast execution, no positions, no orders, no fills, no costs, no carry, no strategy test, no OOS, no Lockbox, no Forward, no CFD adapters, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.
