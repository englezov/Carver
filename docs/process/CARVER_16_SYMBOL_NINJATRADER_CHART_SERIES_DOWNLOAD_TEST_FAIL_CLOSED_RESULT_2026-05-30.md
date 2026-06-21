# Carver 16-Symbol NinjaTrader Chart-Series Download Test Fail-Closed Result

Date: 2026-05-30

Status:

```text
LOCAL_PROCESS_CARVER_16_SYMBOL_NINJATRADER_CHART_SERIES_DOWNLOAD_TEST_FAIL_CLOSED_NO_HELPER_RAW_OUTPUT_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Record the bounded 16-symbol NinjaTrader chart/AddDataSeries daily download test result.

This follows:

```text
docs/process/CARVER_16_SYMBOL_NINJATRADER_CHART_ADDDATASERIES_EXPORT_HELPER_2026-05-30.md
```

The execution surface was limited to the locked 16-symbol manifest, `1 Day` / `Last` bars, and completed trading dates `2026-05-18` through `2026-05-22`.

This artifact records process state only. It does not authorize new data export, provider API access, diagnostics, backtests, forecasts, positions, costs, carry, trend, OOS, Lockbox, Forward, CFD adapters, old QuantLab active-pipeline use, tuning, deployment, trading, promotion, GitHub staging, commit, push, PR update/opening, or remote operations.

## Observed Execution

Correct chart-series helper:

```text
Carver16SymbolDailyChartSeriesExporterSessionEndUtc
```

Observed NinjaTrader log:

```text
C:\Users\openclaw\Documents\NinjaTrader 8\log\log.20260530.00001.txt
```

Observed log time:

```text
2026-05-30 06:27:05
```

Observed result:

```text
Carver 16-symbol chart-series export blocked: availability preflight failed before any helper raw-output write.
failures=84
```

Quarantine output check:

```text
C:\Users\openclaw\Desktop\Carver\docs\researchops\first_data_intake\quarantine\16_SYMBOL_DAILY_LAST_2026-05-18_2026-05-22
MISSING_16_SYMBOL_QUARANTINE_ROOT
```

Outcome:

```text
CHART_SERIES_HELPER_EXECUTED: YES
HELPER_RAW_OUTPUT_FILES_WRITTEN: NO
QUARANTINE_FOLDER_CREATED: NO
SANITIZED_CSV_CREATED: NO
MARKET_ROW_PARSING_AFTER_HELPER_OUTPUT: NO
DIAGNOSTICS_RUN: NO
BACKTESTS_RUN: NO
FORECASTS_COMPUTED: NO
POSITIONS_COMPUTED: NO
```

## Availability Preflight Result

Rows reported missing all five completed daily bars plus the expected-row-count check:

```text
HE JUN26
LE JUN26
M2K JUN26
MNQ JUN26
MYM JUN26
QM JUL26
RB JUL26
ZC JUL26
ZF JUN26
ZL JUL26
ZM JUL26
ZS JUL26
ZT JUN26
ZW JUL26
```

Rows not present in the missing-date failure list:

```text
MES JUN26
ZN JUN26
```

Interpretation:

```text
CHART_SERIES_PATH_AVAILABLE_BY_OBSERVATION_FOR_MES_AND_ZN_ONLY
CHART_SERIES_PATH_FAIL_CLOSED_FOR_14_OF_16_MANIFEST_ROWS
NO_PARTIAL_BATCH_ACCEPTED
NO_SYMBOL_DROPPED
NO_SYMBOL_SUBSTITUTED
NO_WEIGHT_CHANGED
NO_DATE_WINDOW_CHANGED
```

This is not evidence that the Appendix C/NinjaTrader source mapping is invalid. It is evidence that the current local NinjaTrader chart/AddDataSeries availability path did not provide the full locked 16-symbol batch for the target window.

## Decision Point

The 16-symbol all-or-nothing helper boundary held. The next clean gate should choose one of:

```text
NINJATRADER_HISTORICAL_DATA_MANAGER_PRELOAD_FOR_EXACT_16_ROW_MANIFEST
SMALLER_CACHE_PROVEN_MES_ZN_QUARANTINE_BATCH
ALTERNATE_SOURCE_NATIVE_STATIC_OR_PROVIDER_DATA_ACCESS_PATH
```

No next export or parsing step is authorized by this artifact.

## Closed Boundaries

Still closed:

```text
new data export
provider API access beyond a separately authorized local NinjaTrader action
market-row parsing without helper raw output
diagnostics
backtests
forecasts
positions
costs
carry
trend
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
remote operations
```
