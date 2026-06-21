# Carver 16-Symbol NinjaTrader Full Daily History Helper Patch Handoff

Date: 2026-05-30

Status:

```text
LOCAL_PROCESS_CARVER_16_SYMBOL_NINJATRADER_FULL_DAILY_HISTORY_HELPER_PATCH_HANDOFF_NOT_EXECUTED_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Record the patch to the locked 16-symbol NinjaTrader chart/AddDataSeries helper so a later separately authorized run can attempt a full daily history quarantine archive for the exact locked 16-symbol pilot universe.

This follows:

```text
docs/process/CARVER_16_SYMBOL_FULL_DAILY_HISTORY_QUARANTINE_ARCHIVE_SHAPE_GATE_DRAFT_2026-05-30.md
```

This handoff records helper code and process instructions only. It does not run NinjaTrader, retrieve historical data, export data, access provider APIs, parse market rows, run diagnostics, run backtests, compute forecasts, compute positions, compute costs, compute carry, compute trend, access OOS/Lockbox/Forward, use CFD adapters, use old QuantLab active pipelines, tune, deploy, trade, promote, stage Git changes, commit, push, update a PR, or perform remote operations.

## Patched Helper

Repo helper:

```text
tools/nt8/Carver16SymbolDailyChartSeriesExporterSessionEndUtc.cs
```

Helper class:

```text
Carver16SymbolDailyChartSeriesExporterSessionEndUtc
```

Patched helper SHA256:

```text
114C61C90C168C4172BAA3513CB1A200E48D9C82AA098CA2905A1093638B2FFF
```

Patch disposition:

```text
FIVE_DAY_WINDOW_RETIRED_FOR_THIS_HELPER
FULL_HISTORY_DAILY_LAST_HELPER_OUTPUT_ENABLED_FOR_LATER_SEPARATELY_AUTHORIZED_RUN
```

The helper remains disarmed by default:

```csharp
private const bool ExecutionArmed = false;
```

The helper still rejects execution unless the imported/armed copy carries this operator acknowledgement token:

```text
OPERATOR_AUTHORIZED_16_SYMBOL_FULL_DAILY_HISTORY_DAILY_LAST_QUARANTINE
```

## Locked Manifest

The helper still embeds exactly 16 source-native manifest rows:

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

No symbol, dated contract, adjacent product, continuous contract, micro/mini/full-size substitute, CFD symbol, row drop, or reweighting was added.

## Locked Bar Surface

The helper remains locked to:

```text
bar_type: Last
timeframe: 1 Day
source: NinjaTrader chart/AddDataSeries loaded daily bars
```

The helper still rejects:

- primary chart outside the locked manifest;
- non-`1 Day` primary chart;
- non-`Last` primary chart;
- manifest row-count drift;
- duplicate row IDs;
- duplicate symbols;
- undeclared symbol/contract pairs;
- loaded trading-hours template mismatch;
- output root drift;
- existing target output file when replacement is disabled.

## Full-History Behavior

Previous behavior:

```text
collect only 2026-05-18 through 2026-05-22
require exactly five rows per symbol before any helper raw-output write
```

New behavior:

```text
collect all loaded historical completed daily bars for each locked dated contract
write raw helper output for symbols with at least one loaded row
write an availability report for all 16 symbols
record zero-row symbols as BLOCKED_PROVIDER_UNAVAILABLE_OR_NOT_LOADED
preserve duplicate-date failures in the availability report
```

Important boundary:

This helper can only write the history NinjaTrader loads into the chart/AddDataSeries series. It is not proof that NinjaTrader is a complete central data provider. Missing or zero-row symbols remain recorded as availability gaps.

## Locked Output Root

The helper may write only under:

```text
C:\Users\openclaw\Desktop\Carver\docs\researchops\source_native_futures_daily_data_library\16_SYMBOL_FULL_DAILY_HISTORY\raw_provider_archive\NINJATRADER\20260530_FULL_HISTORY_HELPER_ATTEMPT\
```

Raw helper output folder:

```text
raw_market_files\
```

Provider metadata folder:

```text
provider_metadata\
```

Replacement remains disabled:

```csharp
private const bool AllowReplaceExistingFiles = false;
```

## Output Files

For each symbol with at least one loaded daily row, the helper writes:

```text
raw_market_files\<SYMBOL>_<MM-YY>_Daily_Last_FULL_HISTORY_TEMPLATE_SESSION_END_UTC_HELPER_RAW.csv
```

The helper always attempts to write:

```text
provider_metadata\NINJATRADER_16_SYMBOL_FULL_DAILY_HISTORY_HELPER_AVAILABILITY_REPORT.csv
```

Availability statuses:

```text
ACCEPTED_QUARANTINE_HELPER_RAW_AVAILABLE
ACCEPTED_WITH_RECORDED_AVAILABILITY_FAILURES
BLOCKED_PROVIDER_UNAVAILABLE_OR_NOT_LOADED
```

## Raw Helper Output Schema

Each helper raw row uses:

```text
row_id
provider_symbol
local_contract
timestamp_utc
completed_trading_date
open
high
low
close
volume
trading_hours_template
helper_timestamp_policy
```

Timestamp policy:

```text
HELPER_RAW_OUTPUT_WITH_TEMPLATE_DERIVED_UTC_SESSION_END_TIMESTAMPS_NOT_PROVIDER_VERBATIM_TIME0
```

No diagnostics, returns, forecasts, positions, costs, carry, trend, volatility/risk, strategy fields, PnL, Sharpe, drawdown, OOS/Lockbox/Forward, deployment, trading, or promotion fields are emitted.

## Handoff For Later Execution

A later execution gate, if separately authorized, should:

1. Copy:

```text
C:\Users\openclaw\Desktop\Carver\tools\nt8\Carver16SymbolDailyChartSeriesExporterSessionEndUtc.cs
```

to:

```text
C:\Users\openclaw\Documents\NinjaTrader 8\bin\Custom\Indicators\Carver16SymbolDailyChartSeriesExporterSessionEndUtc.cs
```

2. Arm only the imported copy:

```csharp
private const bool ExecutionArmed = true;
```

3. Compile in NinjaTrader Desktop.

4. Open a `1 Day` / `Last` chart for one locked manifest dated contract, with as much historical daily data loaded as NinjaTrader/provider can supply.

5. Apply the helper with:

```text
Operator acknowledgement = OPERATOR_AUTHORIZED_16_SYMBOL_FULL_DAILY_HISTORY_DAILY_LAST_QUARANTINE
```

6. Do not manually edit, repair, fill, merge, back-adjust, substitute, or reweight any helper output.

This handoff does not authorize those execution steps now.

## Validation Performed In This Gate

Static checks performed:

```text
helper file exists: YES
ExecutionArmed default false: YES
fixed five-day date strings removed from helper code: YES
locked output root changed to full-history data-library archive root: YES
1 Day Last lock retained: YES
exact 16-symbol manifest retained: YES
replacement-disabled policy retained: YES
availability report added: YES
zero-row symbol reporting added: YES
market-row parsing performed: NO
NinjaTrader execution performed: NO
diagnostics/backtests/forecasts/positions/costs/carry/trend performed: NO
```

## Next Clean Gate

Selected next gate:

```text
CARVER_16_SYMBOL_NINJATRADER_FULL_DAILY_HISTORY_HELPER_IMPORT_EXECUTION_GATE
```

That gate may authorize local NinjaTrader import/arming/execution and quarantine-only parsing if helper raw files are produced. It must still forbid diagnostics, backtests, forecasts, positions, costs, carry, trend, OOS/Lockbox/Forward, CFD adapters, old QuantLab active-pipeline use, tuning, deployment, trading, promotion, Git staging, commit, push, PR update/opening, and remote operations.

## Non-Authorization

This patch handoff authorizes no NinjaTrader execution, no new data export, no provider API access, no market-row parsing, no diagnostics, no backtests, no forecasts, no positions, no costs, no carry, no trend, no OOS, no Lockbox, no Forward, no CFD adapter work, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no GitHub staging, no commit, no push, no PR update/opening, and no remote operations.
