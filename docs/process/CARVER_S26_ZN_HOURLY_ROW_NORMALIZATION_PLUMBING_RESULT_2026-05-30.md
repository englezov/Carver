# Carver S26 ZN Hourly Row Normalization Plumbing Result

Date: 2026-05-30

Status:

```text
PROCESS_ONLY_ROW_NORMALIZATION_PLUMBING_COMPLETE_NOT_DATA_AUTHORIZATION
```

## Purpose

Record the local, in-memory quarantine row-shape plumbing for the future S26 ZN hourly Databento intake.

This does not read Databento files, call Databento, parse real market rows, or compute a real-data forecast. It only locks the row object and completed-bar transformation that the later authorized gate must use.

## Locked Input Shape

The raw row object is:

```text
S26DatabentoHourlyOHLCVRawRow
```

It is locked to:

```text
provider: DATABENTO_HISTORICAL
dataset: GLBX.MDP3
schema: ohlcv-1h
stype_in: instrument_id
row_id: APPENDIX_C_172_004
author_market_code: ZN
instrument_id: 42000661
raw_symbol: ZNM6
request envelope: 2026-05-17T00:00:00Z through 2026-05-23T00:00:00Z
```

The validator fails closed on wrong dataset, schema, selector, row id, market code, instrument id, raw symbol, timestamp outside the request envelope, non-hour-aligned timestamps, non-positive OHLC prices, negative volume, incoherent high/low/open/close bounds, empty raw SHA, or missing provider-condition status.

## Completed-Bar Policy

The local normalizer is:

```text
normalize_s26_zn_databento_hourly_ohlcv_raw_row
```

It preserves Databento `ts_event` as the provider interval start and derives:

```text
derived_completed_bar_end_utc = provider_ts_event_start_utc + 1 hour
```

The completed trading date must be one of:

```text
2026-05-18
2026-05-19
2026-05-20
2026-05-21
2026-05-22
```

## Strategy-Use Boundary

Default normalized row status:

```text
QUARANTINE_ONLY_NOT_FORECAST_READY
```

Rows with that status cannot feed S26 forecast output.

Forecast handoff remains separately gated and requires explicit row status:

```text
S26_FORECAST_INPUT_READY_QUARANTINE_ONLY
```

Even after that status is present, forecast output still requires locked hourly intake, session mapping, provider-condition, sigma-percent, no-diagnostics, no-backtests, and no-positions source locks.

## Test Result

```text
python -m unittest tests.test_s26_s27_fast_mean_reversion_synthetic
Ran 16 tests
OK
```

## Non-Authorization

This record authorizes no provider API access, no data download, no market-row parsing, no real-data forecast computation, no diagnostics, no backtests, no positions, no costs, no carry, no trend computation, no S27 overlay, no volatility/risk calculations, no OOS, no Lockbox, no Forward, no CFD adapters, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.
