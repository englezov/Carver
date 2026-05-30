# Carver MES Tiny Daily Export Helper Timestamp Policy Patch

Date: 2026-05-30

Status:

```text
PROCESS_AND_LOCAL_HELPER_CARVER_MES_TINY_DAILY_EXPORT_TIMESTAMP_POLICY_PATCH_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Patch the locked MES tiny daily NinjaTrader helper so it writes the template-derived UTC session-end timestamp instead of the observed NinjaTrader daily `Time[0]` timestamp.

The prior raw file is preserved and is not overwritten or silently modified.

## Prior Fail-Closed Evidence

Prior raw file:

```text
docs/researchops/first_data_intake/quarantine/MES_06_26_2026-05-18_2026-05-22/raw_source_copy/MES_06-26_Daily_Last_2026-05-18_2026-05-22.csv
```

Prior raw SHA256:

```text
9313F3A3128DF0A989F7DEE09C007C81246D968AE5FE690ECE47143199F91FF1
```

Prior disposition:

```text
FAIL_CLOSED_UTC_END_OF_BAR_TEMPLATE_SESSION_ALIGNMENT_FAILED_NO_SANITIZED_BARS_CREATED
```

Reason:

```text
NinjaTrader Time[0] daily row timestamps were 23:00:00Z, which mapped to 18:00 Central in May 2026 and failed the extracted CME US Index Futures ETH 16:00 Central session-end policy.
```

## Patch

Repo helper:

```text
tools/nt8/CarverMesTinyDailyExporter.cs
```

Repo helper SHA256 after patch:

```text
788504D71541C6119FE4E90D71867BB16AB8A92717998A3A326642938AA0CDDF
```

Patch summary:

- repo helper remains disarmed by default;
- helper remains locked to `MES JUN26` / `MES 06-26`;
- helper remains locked to `1 Day` and `Last`;
- helper still writes only to the locked `raw_source_copy/` quarantine folder;
- helper now writes a separate corrected raw filename:

```text
MES_06-26_Daily_Last_2026-05-18_2026-05-22_TEMPLATE_SESSION_END_UTC.csv
```

- helper computes each row timestamp as the extracted template TradingDay session end:

```text
Central Standard Time
16:00 local template session end
converted to UTC
```

For the May 2026 target dates this should produce:

```text
2026-05-18T21:00:00Z
2026-05-19T21:00:00Z
2026-05-20T21:00:00Z
2026-05-21T21:00:00Z
2026-05-22T21:00:00Z
```

## Required Rerun

An armed local NinjaTrader copy was placed at:

```text
C:\Users\openclaw\Documents\NinjaTrader 8\bin\Custom\Indicators\CarverMesTinyDailyExporter.cs
```

Armed copy SHA256:

```text
949E075ED0C73B228FBA5DF9B5C2CA87789E5FD926B1D4A7E8FC3475F6987EB9
```

Corrected raw file current state after armed-copy placement:

```text
CORRECTED_RAW_FILE_NOT_PRESENT_AFTER_ARMED_PATCH_COPY_PLACEMENT
```

NinjaTrader Desktop still needs the local GUI compile/apply run before Carver can rerun the tiny intake.

The corrected raw file must be produced by the patched helper and then parsed by the same tiny intake gate. No sanitized bars may be created unless the corrected raw file passes:

- exact row identity;
- exact row count;
- UTC timestamp format;
- extracted template session-end alignment;
- target TradingDay mapping;
- stale/missing/duplicate checks;
- basic OHLCV row shape.

## Boundary

This patch does not authorize diagnostics, backtests, returns, PnL, Sharpe, drawdown, forecasts, position sizing, costs, carry, trend, OOS, Lockbox, Forward, CFD adapter work, old QuantLab active-pipeline use, tuning, deployment, trading, promotion, provider API access, remote operations, other symbols, or a wider date window.
