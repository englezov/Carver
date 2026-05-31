# Carver S26/S27 Synthetic Conformance Implementation Result

Date: 2026-05-30

Status:

```text
PROCESS_AND_SYNTHETIC_CODE_CARVER_S26_S27_FAST_MEAN_REVERSION_CONFORMANCE_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Record the first synthetic-only implementation result for:

```text
G_SYN_S26_S27_SOURCE_ATOM_LOCK_AND_SYNTHETIC_CONFORMANCE
```

This result implements deterministic synthetic formula conformance only. It does not authorize real data, provider access, market-row parsing, diagnostics, backtests, real-data forecasts, positions, costs, carry, trend-sleeve computation on real data, OOS, Lockbox, Forward, deployment, trading, promotion, Git operations, or remote operations.

## Implemented Surface

Code:

```text
src/carver/spine/s26_s27.py
```

Tests:

```text
tests/test_s26_s27_fast_mean_reversion_synthetic.py
```

Package export surface:

```text
src/carver/spine/__init__.py
```

## S26 Synthetic Mechanics

Implemented:

```text
equilibrium_t = EWMA_span_5(price_t)
raw_forecast_t = equilibrium_t - price_t
sigma_price_t = price_t * sigma_percent_t / 16
risk_adjusted_forecast_t = raw_forecast_t / sigma_price_t
scaled_forecast_t = risk_adjusted_forecast_t * 9.3
capped_forecast_t = max(min(scaled_forecast_t, 20), -20)
```

Structural locks:

```text
NO_FDM
NO_BUFFERING
NO_PERFORMANCE_METRICS
NO_POSITION_OUTPUTS
SYNTHETIC_HOURLY_INPUTS_ONLY
```

## S27 Synthetic Mechanics

Implemented:

```text
trend_forecast_t = EWMAC(16,64) sign surface from synthetic hourly prices
vol_multiplier_t = EWMA_span_10(2 - 1.5 * Q_t)
adjusted_raw_forecast_t = S26_raw_forecast_t * vol_multiplier_t
```

Trend interaction convention locked for synthetic conformance:

```text
ZERO_OPPOSING_MEAN_REVERSION_FORECAST
```

If the S26 mean-reversion raw forecast and EWMAC(16,64) trend forecast have opposite signs, the S27 adjusted raw forecast is zero for this synthetic conformance surface. This is a forecast-block convention only; it is not a position, order, cost, or execution rule.

Structural locks:

```text
INHERITS_S26_SCALAR_9_3
INHERITS_S26_CAP_PLUS_MINUS_20
NO_DAILY_FORECAST_COMBINATION_FDM
NO_BUFFERING
NO_PERFORMANCE_METRICS
NO_POSITION_OUTPUTS
SYNTHETIC_HOURLY_INPUTS_ONLY
```

## Source-Faithful Instrument Boundary

No instrument rows are read or used by this implementation.

The process guardrail remains:

```text
S26_FIRST_REAL_DATA_ANCHOR: BOOK_US_10_YEAR_FUTURE_FIG_81
EXPECTED_IDENTITY_PATH_AFTER_SEPARATE_LOCK: US_10_YEAR / ZN
FORBIDDEN_SHORTCUTS: ZT, T_BILLS, 2_YEAR_TREASURY_NOTES, 16_SYMBOL_DAILY_PILOT_CONVENIENCE_ROWS
S27_SP500_MES_NATIVE_WORKED_EXAMPLE_LOCK: NOT_LOCKED_FROM_CHAPTER_27
```

## Verification

Focused S26/S27 tests:

```text
python -m unittest tests.test_s26_s27_fast_mean_reversion_synthetic
```

Result:

```text
Ran 7 tests
OK
```

Full local synthetic suite:

```text
python -m unittest discover -s tests
```

Result:

```text
Ran 162 tests
OK
```

## Non-Authorization

This file authorizes no provider API access, no data download, no market-row parsing, no diagnostics, no backtests, no forecasts on real data, no positions, no costs, no carry, no trend computation on real data, no volatility/risk calculations on real data, no OOS, no Lockbox, no Forward, no CFD adapters, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.
