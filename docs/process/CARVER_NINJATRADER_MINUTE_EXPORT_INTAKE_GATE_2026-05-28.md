# Carver NinjaTrader Minute Export Intake Gate

Date: 2026-05-28

Status:

```text
PROCESS_ONLY_CARVER_NINJATRADER_MINUTE_EXPORT_INTAKE_GATE_SYNTHETIC_ONLY
```

## Purpose

Define and test the clean text-export intake boundary for NinjaTrader-sourced 1-minute futures bars before any real export, API download, diagnostic, backtest, OOS, Lockbox, Forward, CFD adapter work, deployment, trading, or promotion.

NinjaTrader remains the intended source for source-native futures data. This gate explicitly rejects ad hoc parsing of NinjaTrader `.ncd` binary cache files. The authorized intake surface is a future operator-provided text export with a locked schema.

## Authorized Implementation Surface

Authorized code may include only:

- A strict expected 1-minute export schema.
- Synthetic row parsing from in-memory strings only.
- Source-native contract identity validation.
- Completed-minute timestamp validation.
- OHLCV numeric validation.
- Duplicate, unsorted, missing-field, wrong-contract, wrong-timeframe, wrong-bar-type, and bad-number fail-closed checks.
- An operator export request template for one tiny MES sample.

## Expected Export Schema

The parser expects comma-separated text with exactly this header:

```text
instrument,contract_month,bar_type,timeframe,timestamp,open,high,low,close,volume
```

Rules:

- `instrument` must match the expected source-native contract code, e.g. `MES`.
- `contract_month` must use `MM-YY`, e.g. `06-26`.
- `bar_type` must be `Last`.
- `timeframe` must be `1 Minute`.
- `timestamp` must be timezone-aware ISO-8601 and second/microsecond aligned to zero.
- The locked synthetic intake window is `13:30 <= timestamp time < 20:00` with timezone offset `+00:00`.
- Rows must be contiguous one-minute bars; missing minute gaps fail closed.
- OHLC prices must be finite positive numbers.
- `volume` must be finite and non-negative.
- `high >= max(open, close, low)` and `low <= min(open, close, high)`.
- Rows must be strictly increasing by timestamp.
- Duplicate timestamps fail closed.
- Contract months are fail-closed to the allowed source-native month set for the expected contract. The default gate set is quarterly: `03`, `06`, `09`, `12`.

## Operator Export Request Template

When the operator authorizes the first real schema conformance sample, export exactly one tiny file:

```text
Source: NinjaTrader
Instrument: MES 06-26
Bars: 1 Minute
Price type: Last
Date window: one completed regular trading day only
Output: CSV/text with header
Columns: instrument,contract_month,bar_type,timeframe,timestamp,open,high,low,close,volume
Timezone: include explicit timezone offset in each timestamp
Purpose: schema conformance only, not diagnostic/backtest
```

No larger export should be produced until the one-file conformance sample is operator-reviewed.

## Standing Non-Authorization

This file authorizes no raw `.ncd` decoding, no real exported file parsing, no NinjaTrader automation or API download, no market-row diagnostics, no historical backtests, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old QuantLab import, no tuning, no deployment, no trading, and no promotion.
