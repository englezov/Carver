# Carver First MES NinjaTrader Export Conformance Gate

Date: 2026-05-28

Status:

```text
PROCESS_ONLY_CARVER_FIRST_MES_NINJATRADER_EXPORT_CONFORMANCE_GATE_SCHEMA_ONLY
```

## Purpose

Prepare the first controlled real-file conformance touchpoint for one operator-provided NinjaTrader MES export without opening diagnostics, backtests, OOS, Lockbox, Forward, CFD adapters, old QuantLab imports, tuning, deployment, trading, or promotion.

This gate does not authorize downloading data, automating NinjaTrader, decoding `.ncd` cache files, or scanning arbitrary folders. It authorizes only a file-level wrapper that can read one explicitly named text/CSV file under the quarantined ignored path once the operator places it there.

This is a schema-slice conformance gate. It verifies that an explicitly named export slice matches the locked text schema and minute-bar invariants. It does not prove full-day completeness, session completeness, data coverage, continuity across sessions, or historical availability.

## Quarantine Path

Real operator exports must be placed under:

```text
data/quarantine/ninjatrader/minute_exports/
```

This path is intentionally ignored by Git through the existing `data/` rule. Data files must remain untracked.

Recommended first filename:

```text
MES_06-26_1Minute_Last_YYYYMMDD.csv
```

## Required First Sample

```text
Source: NinjaTrader
Instrument: MES 06-26
Bars: 1 Minute
Price type: Last
Date window: a tiny slice from one completed regular trading day only
Format: CSV/text with header
Path: data/quarantine/ninjatrader/minute_exports/MES_06-26_1Minute_Last_YYYYMMDD.csv
Purpose: schema conformance only, not diagnostic/backtest
```

The file must use the previously locked header:

```text
instrument,contract_month,bar_type,timeframe,timestamp,open,high,low,close,volume
```

The current locked synthetic conformance settings are:

- Contract: `MES`
- Contract month: `06-26`
- Bar type: `Last`
- Timeframe: `1 Minute`
- Timestamp offset: `+00:00`
- Session window: `13:30 <= timestamp time < 20:00`
- Rows: strictly increasing and contiguous one-minute bars

Full regular-session completeness is deliberately deferred to a later data-quality gate.

## Standing Non-Authorization

This file authorizes no raw `.ncd` decoding, no NinjaTrader automation or API download, no scanning of arbitrary export folders, no market diagnostics, no historical backtests, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old QuantLab import, no tuning, no deployment, no trading, no promotion, and no remote push.
