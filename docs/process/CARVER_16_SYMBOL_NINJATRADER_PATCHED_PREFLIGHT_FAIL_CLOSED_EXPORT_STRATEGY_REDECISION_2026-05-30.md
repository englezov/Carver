# Carver 16-Symbol NinjaTrader Patched Preflight Fail-Closed Export Strategy Redecision

Date: 2026-05-30

Status:

```text
PROCESS_ONLY_CARVER_16_SYMBOL_NINJATRADER_PATCHED_PREFLIGHT_FAIL_CLOSED_EXPORT_STRATEGY_REDECISION_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Record the patched 16-symbol NinjaTrader helper execution result and decide the next clean export strategy.

This follows:

```text
docs/process/CARVER_16_SYMBOL_NINJATRADER_BATCH_EXPORT_FAIL_CLOSED_REDECISION_2026-05-30.md
docs/process/CARVER_16_SYMBOL_NINJATRADER_LOCKED_MANIFEST_DAILY_EXPORT_HELPER_2026-05-30.md
```

This artifact is process-only. It does not export data, access provider APIs, parse market rows, run diagnostics, run backtests, compute forecasts, compute positions, compute costs, compute carry, compute trend, access OOS/Lockbox/Forward, use CFD adapters, use old QuantLab active pipelines, tune, deploy, trade, promote, stage Git changes, commit, push, update a PR, or perform remote operations.

## Evidence

Patched repo helper:

```text
tools/nt8/Carver16SymbolDailyExporterSessionEndUtc.cs
SHA256: 22C76501A9F4296D243972902770527074C851F207AB590089009E8B63623666
```

Observed NinjaTrader log:

```text
C:\Users\openclaw\Documents\NinjaTrader 8\log\log.20260530.00001.en.txt
```

Observed patched-helper result time:

```text
2026-05-30 05:44:49
```

Observed result:

```text
Carver 16-symbol export blocked: availability preflight failed before any helper raw-output write.
failures=96
```

Quarantine output check:

```text
C:\Users\openclaw\Desktop\Carver\docs\researchops\first_data_intake\quarantine\16_SYMBOL_DAILY_LAST_2026-05-18_2026-05-22
MISSING_16_SYMBOL_QUARANTINE_ROOT
```

Outcome:

```text
PATCHED_HELPER_EXECUTED: YES
HELPER_RAW_OUTPUT_FILES_WRITTEN: NO
QUARANTINE_FOLDER_CREATED: NO
MARKET_ROW_PARSING: NO
DIAGNOSTICS_RUN: NO
BACKTESTS_RUN: NO
FORECASTS_COMPUTED: NO
POSITIONS_COMPUTED: NO
```

## Failure Summary

The patched helper reported zero collected completed daily rows for every manifest row over the target window.

The 96 failures decompose as:

```text
16 contracts * 5 missing completed trading dates = 80 missing-date failures
16 contracts * expected-five-rows collected-zero failures = 16 row-count failures
80 + 16 = 96
```

Affected contracts:

```text
ZT JUN26
ZF JUN26
ZN JUN26
MES JUN26
MNQ JUN26
M2K JUN26
MYM JUN26
QM JUL26
RB JUL26
ZC JUL26
ZS JUL26
ZM JUL26
ZL JUL26
ZW JUL26
HE JUN26
LE JUN26
```

Affected completed trading dates:

```text
2026-05-18
2026-05-19
2026-05-20
2026-05-21
2026-05-22
```

Interpretation:

```text
BARSREQUEST_PROVIDER_PATH_RETURNED_ZERO_ROWS_FOR_FULL_MANIFEST
```

This is not evidence that the Appendix C/NinjaTrader mapping is wrong, not evidence that the 16-symbol universe is invalid, not evidence that any specific symbol should be dropped, and not evidence for substitution or reweighting.

## Options Considered

### Option A: NinjaTrader Historical Data Manager pre-download

Disposition:

```text
NOT_SELECTED_AS_NEXT_GATE
```

Reason:

Pre-downloading may eventually help if the issue is cache population. However, it introduces a manual stateful precondition outside the helper and still leaves the batch export path dependent on the same `BarsRequest` behavior that just returned zero rows. It should remain an available fallback, but it is not the cleanest next engineering gate.

### Option B: Chart/AddDataSeries helper path

Disposition:

```text
SELECTED_NEXT_GATE
```

Reason:

The prior MES tiny quarantine success used a chart-loaded bar path rather than the `BarsRequest` provider path. The most source-native next step is to build a locked multi-series helper that uses NinjaTrader's chart/AddDataSeries loading surface for the same exact 16 dated contracts, `1 Day` / `Last`, and completed trading dates. This tests the practical path that already worked for MES while preserving the 16-symbol manifest and all fail-closed boundaries.

Required properties:

- repo helper disarmed by default;
- exact same 16 manifest rows and dated contracts;
- exact same `2026-05-18` through `2026-05-22` completed trading-date window;
- exact same `1 Day` / `Last` bar surface;
- no continuous contracts;
- no substitutions;
- no row dropping;
- no reweighting;
- no date-window widening;
- no market-row parsing outside the helper execution gate;
- no diagnostics, backtests, forecasts, positions, costs, carry, trend, OOS/Lockbox/Forward, deployment, trading, or promotion;
- all-or-nothing output semantics;
- helper raw-output label must remain template-session-end UTC helper output, not provider-verbatim `Time[0]`.

### Option C: Smaller cache-proven subset

Disposition:

```text
NOT_SELECTED_AS_NEXT_GATE
```

Reason:

The patched helper returned zero rows for every manifest row. That points to the `BarsRequest` retrieval path, not to a row-specific availability ranking. Shrinking now would prematurely abandon the 16-symbol pilot before testing the chart-loaded route.

## Decision

Selected next gate:

```text
CARVER_16_SYMBOL_NINJATRADER_CHART_ADDDATASERIES_EXPORT_HELPER_SHAPE_AND_PATCH
```

This gate should create or patch only helper code and process documentation. It should not execute NinjaTrader, export new data, parse market rows, run diagnostics, run backtests, compute forecasts, compute positions, compute costs, compute carry, compute trend, or perform remote operations.

After the shape/patch gate and lean hostile audit, a separately authorized local execution gate may apply the chart/AddDataSeries helper in NinjaTrader Desktop. Only that later gate may attempt the exact 16-symbol helper raw-output export.

## Closed Boundaries

Still closed:

```text
new data export
provider API access beyond separately authorized local NinjaTrader execution
market-row parsing
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

## Non-Authorization

This decision authorizes no new data export, no provider API access, no market-row parsing, no diagnostics, no backtests, no forecasts, no positions, no costs, no carry, no trend, no OOS, no Lockbox, no Forward, no CFD adapter work, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no GitHub staging, no commit, no push, no PR update/opening, and no remote operations.
