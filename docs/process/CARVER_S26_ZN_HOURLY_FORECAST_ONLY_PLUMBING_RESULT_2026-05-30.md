# Carver S26 ZN Hourly Forecast-Only Plumbing Result

Date: 2026-05-30

Status:

```text
PROCESS_AND_LOCAL_SYNTHETIC_TEST_CODE_CARVER_S26_ZN_HOURLY_FORECAST_ONLY_PLUMBING_NOT_DATA_NOT_BACKTEST
```

## Purpose

Record the local forecast-only plumbing added for the S26 ZN real-hourly bridge.

This result does not ingest Databento data, parse market rows, compute forecasts on real data, run diagnostics, run backtests, create positions, compute costs, compute carry, compute trend, run S27, deploy, trade, promote, or open Git operations.

## Implemented Surface

Code:

```text
src/carver/spine/s26_s27.py
```

New source-locked real-hourly bridge types:

```text
S26QuarantinedHourlyZNBar
S26QuarantinedHourlySourceLocks
S26QuarantinedHourlyForecastRequest
S26QuarantinedHourlyForecastResult
s26_forecast_only_from_quarantined_zn_hourly_bars
```

Locked first real-hourly instrument constants:

```text
S26_ZN_WORKED_EXAMPLE_ROW_ID = APPENDIX_C_172_004
S26_ZN_WORKED_EXAMPLE_AUTHOR_MARKET_CODE = ZN
S26_ZN_WORKED_EXAMPLE_DATABENTO_INSTRUMENT_ID = 42000661
S26_ZN_WORKED_EXAMPLE_DATABENTO_RAW_SYMBOL = ZNM6
```

Package export:

```text
src/carver/spine/__init__.py
```

Tests:

```text
tests/test_s26_s27_fast_mean_reversion_synthetic.py
```

## Boundary

The original synthetic S26/S27 path still requires `SyntheticHourlyPrice` labels and remains synthetic-only.

The new real-hourly bridge path is separate. It requires:

- `APPENDIX_C_172_004`;
- author market code `ZN`;
- Databento instrument id `42000661`;
- Databento raw symbol `ZNM6`;
- completed hourly `provider_ts_event_start_utc`;
- derived completed bar end equal to `ts_event + 1 hour`;
- strategy-use status `S26_FORECAST_INPUT_READY_QUARANTINE_ONLY`;
- all real-hourly source locks set to `LOCKED`;
- no diagnostics, no backtests, no position outputs.

## Formula

The forecast-only bridge reuses the same S26 formula proven in the synthetic chapter:

```text
equilibrium_t = EWMA_span_5(hourly_close_t)
raw_forecast_t = equilibrium_t - hourly_close_t
sigma_price_t = hourly_close_t * sigma_percent_t / 16
risk_adjusted_forecast_t = raw_forecast_t / sigma_price_t
scaled_forecast_t = risk_adjusted_forecast_t * 9.3
capped_forecast_t = max(min(scaled_forecast_t, 20), -20)
```

Allowed output status:

```text
S26_FORECAST_OUTPUT_ONLY_NOT_DIAGNOSTIC_NOT_BACKTEST_NOT_POSITION
```

## Verification

Focused S26/S27 tests:

```text
python -m unittest tests.test_s26_s27_fast_mean_reversion_synthetic
```

Result:

```text
Ran 10 tests
OK
```

Full local test suite:

```text
python -m unittest discover -s tests
```

Result:

```text
Ran 165 tests
OK
```

## Current Goal Status

The active bridge goal is not complete.

Completed locally:

```text
source-anchor ZN from the book
define hourly Databento request shape
lock hourly completed-bar semantics at process-shape level
prepare tiny authorized intake path
prepare source-locked S26 forecast-only plumbing for already-quarantined ZN hourly bars
lock S26 sigma_percent_t source method to the Part One S03 variable-risk family
```

Still required:

```text
operator-authorized Databento ohlcv-1h tiny intake for ZN instrument_id 42000661
market-row parsing of only that quarantined output
prevalidated runtime sigma_percent_t value with timestamp/no-lookahead provenance
forecast-only execution against the passed quarantined bars
```

## Non-Authorization

This result authorizes no Databento access, no data download, no market-row parsing, no real-data forecast computation, no diagnostics, no backtests, no positions, no costs, no carry, no trend computation, no S27 overlay, no volatility/risk calculations, no OOS, no Lockbox, no Forward, no CFD adapters, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.
