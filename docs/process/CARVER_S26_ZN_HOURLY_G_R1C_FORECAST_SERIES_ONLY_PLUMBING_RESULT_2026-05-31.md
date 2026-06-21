# Carver S26 ZN Hourly G_R1C Forecast-Series-Only Plumbing Result

Date: 2026-05-31

Status:

```text
PROCESS_AND_CODE_G_R1C_FORECAST_SERIES_ONLY_PLUMBING_COMPLETE_NOT_REAL_SERIES_EXECUTION
```

## Purpose

Add source-faithful machinery for a later S26 ZN hourly forecast-series-only gate.

G_R1B proved one real S26 forecast-only row. G_R1C must prove repeatability without changing scope into diagnostics, backtests, positions, costs, carry, trend, or S27.

## Implemented Code Surface

Code:

```text
src/carver/spine/s26_s27.py
```

New public objects:

```text
S26_ZN_FORECAST_SERIES_STATUS
S26QuarantinedHourlyForecastSeriesRequest
S26QuarantinedHourlyForecastSeriesResult
s26_forecast_series_only_from_quarantined_zn_hourly_ohlcv_bars
```

The series function requires:

```text
SOURCE_NATIVE_FUTURES lane
locked G_R1B source locks
quarantined ZN / APPENDIX_C_172_004 / 42000661 / ZNM6 hourly OHLCV bars
one PREVALIDATED_S26_ZN_SIGMA_PERCENT_RUNTIME_VALUE per emitted forecast row
strict timestamp match between each sigma runtime and each completed hourly forecast row
```

It emits:

```text
PASS_G_R1C_S26_ZN_HOURLY_FORECAST_SERIES_ONLY
```

and only contains S26 forecast fields. It contains no diagnostics, backtests, returns, PnL, positions, costs, carry, trend, S27 overlay, OOS, Lockbox, Forward, deployment, trading, or promotion fields.

## Verification

Focused verification:

```text
python -m unittest tests.test_s26_s27_fast_mean_reversion_synthetic -v
```

Result:

```text
22 tests passed
```

New tests prove:

- a six-row hourly fixture produces two forecast-only rows;
- each output row remains `S26_FORECAST_OUTPUT_ONLY_NOT_DIAGNOSTIC_NOT_BACKTEST_NOT_POSITION`;
- the series result emits no diagnostics, backtests, or positions;
- missing or misaligned sigma runtimes fail closed.

## Boundary

This is plumbing only. It does not execute the real G_R1C series against the existing 115-row G_R1A quarantine artifact.

The later real-artifact gate remains:

```text
G_R1C_ZN_S26_HOURLY_FORECAST_SERIES_ONLY
```

That later gate must provide or derive prevalidated no-lookahead sigma runtime records for each forecast row before emitting the real forecast series.

## Non-Authorization

This result authorizes no new provider API access, no new data download, no market-row expansion, no real forecast-series execution, no diagnostics, no backtests, no returns, no PnL, no Sharpe, no drawdown, no positions, no orders, no costs, no carry, no trend computation, no S27 overlay, no OOS, no Lockbox, no Forward, no CFD adapters, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.
