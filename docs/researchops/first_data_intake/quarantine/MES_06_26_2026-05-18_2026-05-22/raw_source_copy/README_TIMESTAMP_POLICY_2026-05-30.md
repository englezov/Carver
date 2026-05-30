# MES 06-26 Raw Source Copy Timestamp Policy

Date: 2026-05-30

Status:

```text
PROCESS_SOURCE_TIMESTAMP_POLICY_NOTE_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

This folder preserves raw helper outputs for the MES 06-26 tiny quarantine intake.

The original file:

```text
MES_06-26_Daily_Last_2026-05-18_2026-05-22.csv
```

contains the NinjaTrader-observed daily bar timestamp field and was fail-closed because its `23:00:00Z` timestamps did not match the locked template session-end policy.

The corrected v2 file:

```text
MES_06-26_Daily_Last_2026-05-18_2026-05-22_TEMPLATE_SESSION_END_UTC.csv
```

is raw output from the locked `CarverMesTinyDailyExporterSessionEndUtc` helper. Its OHLCV values are not transformed, but its `timestamp_utc` field is template-derived from the locked `CME US Index Futures ETH` session-end policy. It is not a provider-verbatim copy of NinjaTrader `Time[0]`.

Both files remain quarantine-only. This note authorizes no new data export, no market-row parsing, no diagnostics, no backtests, no forecasts, no positions, no trading, no deployment, and no promotion.
