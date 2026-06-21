# Carver Databento 16-Symbol Daily OHLCV Quarantine Pipe Smoke Test Pass

Date: 2026-05-30

Status:

```text
LOCAL_PROCESS_CARVER_DATABENTO_16_SYMBOL_DAILY_OHLCV_PIPE_SMOKE_TEST_PASS_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Record the bounded local pipe smoke test for the already-downloaded Databento 16-symbol daily OHLCV quarantine artifacts.

This smoke test used only existing local quarantine files from:

```text
docs/researchops/first_data_intake/quarantine/DATABENTO_16_SYMBOL_DAILY_OHLCV_2026-05-18_2026-05-22/attempt_2026-05-30_auth_ok
```

No new Databento API call, provider request, or data download was performed.

## Smoke-Test Scope

The test reran the local quarantine normalization/validation path from the saved raw provider CSV and compared regenerated outputs to the existing accepted artifacts.

Checked:

- raw provider schema/header;
- exact 16 locked raw symbols;
- exactly 80 rows;
- exactly five completed trading dates per symbol;
- no missing dates;
- no duplicate dates;
- no unexpected dates;
- deterministic sanitized OHLCV reproduction;
- deterministic row-validation reproduction.

## Result

```text
PIPE_SMOKE_STATUS: PASS_REPRODUCIBLE_QUARANTINE_NORMALIZATION_AND_VALIDATION
RAW_SCHEMA_OK: YES
ACCEPTED_ROWS: 80
SANITIZED_BYTE_IDENTICAL: YES
VALIDATION_BYTE_IDENTICAL: YES
```

The regenerated sanitized OHLCV CSV and regenerated row-validation CSV are byte-identical to the accepted artifacts.

## Format Observations

Observed raw provider header:

```text
ts_event, rtype, publisher_id, instrument_id, open, high, low, close, volume, symbol
```

Observed sanitized header:

```text
provider, dataset, schema, stype_in, provider_symbol, instrument_id, timestamp_utc, completed_trading_date, open, high, low, close, volume, quarantine_status
```

Observed Databento daily timestamp policy for this request:

```text
ohlcv-1d ts_event is 00:00:00Z for each completed trading date.
```

Observed price format:

```text
Decimal OHLC values are emitted by provider output and preserved in canonical sanitized output.
```

Observed volume format:

```text
Volume is integer-like in provider and sanitized output.
```

## Created Smoke-Test Artifacts

Root:

```text
docs/researchops/first_data_intake/quarantine/DATABENTO_16_SYMBOL_DAILY_OHLCV_2026-05-18_2026-05-22/attempt_2026-05-30_auth_ok/pipe_smoke_2026-05-30
```

Artifacts:

```text
regenerated/DATABENTO_16_SYMBOL_DAILY_OHLCV_2026-05-18_2026-05-22_SANITIZED_REGENERATED.csv
regenerated/DATABENTO_16_SYMBOL_DAILY_OHLCV_2026-05-18_2026-05-22_ROW_VALIDATION_REGENERATED.csv
comparison/DATABENTO_16_SYMBOL_DAILY_OHLCV_PIPE_SMOKE_COMPARISON.csv
provenance/DATABENTO_16_SYMBOL_DAILY_OHLCV_PIPE_SMOKE_STATUS.csv
provenance/DATABENTO_16_SYMBOL_DAILY_OHLCV_PIPE_SMOKE_FORMAT_NOTES.json
provenance/DATABENTO_16_SYMBOL_DAILY_OHLCV_PIPE_SMOKE_SHA256SUMS.txt
```

## Interpretation

This pass proves only that the local quarantine formatting pipe is reproducible for the saved Databento 16-symbol, five-day `ohlcv-1d` request.

It does not prove full-history availability, continuous-contract readiness, strategy readiness, diagnostic validity, backtest validity, cost readiness, carry readiness, trend readiness, production readiness, deployment readiness, trading readiness, or promotion.

## Closed Boundaries

Still closed:

```text
new provider API access
new data download
symbols/date windows outside the existing quarantine request
diagnostics
backtests
forecasts
positions
costs
carry
trend
volatility or risk calculations
OOS
Lockbox
Forward
CFD adapters
old QuantLab active-pipeline use
tuning
deployment
trading
promotion
GitHub staging
commit
push
PR update/opening
remote repository operations
```
