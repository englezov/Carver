# Carver 16-Symbol NinjaTrader Chart/AddDataSeries Export Helper

Date: 2026-05-30

Status:

```text
LOCAL_PROCESS_CARVER_16_SYMBOL_NINJATRADER_CHART_ADDDATASERIES_EXPORT_HELPER_NOT_EXECUTED_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Create the locked chart/AddDataSeries-based NinjaTrader Desktop helper and process handoff for the 16-symbol daily intake pilot.

This follows the patched preflight fail-closed decision:

```text
docs/process/CARVER_16_SYMBOL_NINJATRADER_PATCHED_PREFLIGHT_FAIL_CLOSED_EXPORT_STRATEGY_REDECISION_2026-05-30.md
```

The prior `BarsRequest` helper remains preserved as evidence:

```text
tools/nt8/Carver16SymbolDailyExporterSessionEndUtc.cs
```

This gate creates helper code and process instructions only. It does not run NinjaTrader, export new data, access provider APIs, parse market rows, run diagnostics, run backtests, compute forecasts, compute positions, compute costs, compute carry, compute trend, access OOS/Lockbox/Forward, use CFD adapters, use old QuantLab active pipelines, tune, deploy, trade, promote, stage Git changes, commit, push, update a PR, or perform remote operations.

## Helper Artifact

Repo helper:

```text
tools/nt8/Carver16SymbolDailyChartSeriesExporterSessionEndUtc.cs
```

SHA256:

```text
CABC79C9CE7FCDA13C83CCEC9326CA44DDF4A9D60CB0203F32ED8B36CABB34C8
```

NinjaTrader indicator class:

```text
Carver16SymbolDailyChartSeriesExporterSessionEndUtc
```

The helper is disarmed by default:

```csharp
private const bool ExecutionArmed = false;
```

It requires a later separately authorized execution gate before any imported copy may be armed:

```csharp
private const bool ExecutionArmed = true;
```

It also requires the operator acknowledgement token in NinjaTrader:

```text
OPERATOR_AUTHORIZED_16_SYMBOL_DAILY_LAST_2026_05_18_TO_2026_05_22
```

## Export Path

Selected path:

```text
CHART_ADDDATASERIES_NOT_BARSREQUEST
```

The helper adds the exact 16 source-native dated contracts using NinjaTrader chart/AddDataSeries loading:

```csharp
AddDataSeries(row.NinjaTraderContract, BarsPeriodType.Day, 1, MarketDataType.Last);
```

The repo-disarmed helper returns before `AddDataSeries` in `State.Configure`, so simply importing or applying the disarmed repo helper does not add secondary data series. A later separately authorized execution gate must arm the imported copy before the chart/AddDataSeries loading path is active.

The helper uses NinjaTrader runtime `FullName` syntax for chart/AddDataSeries loading and primary-chart validation:

```text
SYMBOL MONYY
```

It keeps the ledger-native local contract syntax for output/provenance rows:

```text
SYMBOL MM-YY
```

This deliberately preserves the split observed in the MES tiny helper: NinjaTrader runtime uses `MES JUN26`; Carver ledger/provenance uses `MES 06-26`.

The helper also fail-closes if the loaded primary or secondary NinjaTrader series trading-hours template does not exactly match the row's locked static template. The template is checked at runtime before any helper raw-output write.

The helper does not use:

```text
BarsRequest
LookupPolicies.Provider
continuous contracts
manual row substitution
manual member dropping
reweighting
```

## Locked Manifest

The helper embeds exactly 16 rows:

| Row ID | Symbol | NinjaTrader runtime contract | Local contract | Template | Template session end |
|---|---:|---|---|---|---:|
| `APPENDIX_C_172_001` | `ZT` | `ZT JUN26` | `ZT 06-26` | `CBOT Interest Rate ETH` | `16:00 Central` |
| `APPENDIX_C_172_003` | `ZF` | `ZF JUN26` | `ZF 06-26` | `CBOT Interest Rate ETH` | `16:00 Central` |
| `APPENDIX_C_172_004` | `ZN` | `ZN JUN26` | `ZN 06-26` | `CBOT Interest Rate ETH` | `16:00 Central` |
| `APPENDIX_C_174_006` | `MES` | `MES JUN26` | `MES 06-26` | `CME US Index Futures ETH` | `16:00 Central` |
| `APPENDIX_C_174_002` | `MNQ` | `MNQ JUN26` | `MNQ 06-26` | `CME US Index Futures ETH` | `16:00 Central` |
| `APPENDIX_C_174_004` | `M2K` | `M2K JUN26` | `M2K 06-26` | `CME US Index Futures ETH` | `16:00 Central` |
| `APPENDIX_C_174_001` | `MYM` | `MYM JUN26` | `MYM 06-26` | `CME US Index Futures ETH` | `16:00 Central` |
| `APPENDIX_C_182_002` | `QM` | `QM JUL26` | `QM 07-26` | `Nymex Metals - Energy ETH` | `17:00 Eastern` |
| `APPENDIX_C_182_004` | `RB` | `RB JUL26` | `RB 07-26` | `Nymex Metals - Energy ETH` | `17:00 Eastern` |
| `APPENDIX_C_183_003` | `ZC` | `ZC JUL26` | `ZC 07-26` | `CBOT Agriculturals ETH` | `13:20 Central` |
| `APPENDIX_C_183_010` | `ZS` | `ZS JUL26` | `ZS 07-26` | `CBOT Agriculturals ETH` | `13:20 Central` |
| `APPENDIX_C_183_011` | `ZM` | `ZM JUL26` | `ZM 07-26` | `CBOT Agriculturals ETH` | `13:20 Central` |
| `APPENDIX_C_183_012` | `ZL` | `ZL JUL26` | `ZL 07-26` | `CBOT Agriculturals ETH` | `13:20 Central` |
| `APPENDIX_C_183_013` | `ZW` | `ZW JUL26` | `ZW 07-26` | `CBOT Agriculturals ETH` | `13:20 Central` |
| `APPENDIX_C_183_005` | `HE` | `HE JUN26` | `HE 06-26` | `CME Commodities ETH` | `13:05 Central` |
| `APPENDIX_C_183_006` | `LE` | `LE JUN26` | `LE 06-26` | `CME Commodities ETH` | `13:05 Central` |

Manifest source:

```text
docs/researchops/first_data_intake/CARVER_16_SYMBOL_NINJATRADER_STATIC_DATED_CONTRACT_SELECTION_2026-05-30.csv
SHA256: 4A6B975B5C4B58F422BB4695F4AD83C8166A12EED13EE86B5B1A05C4464C9F4F
```

## Locked Bar Surface

The helper is hard-locked to:

```text
bar_type: Last
timeframe: 1 Day
completed_trading_date_start: 2026-05-18
completed_trading_date_end: 2026-05-22
expected_manifest_rows: 16
expected_completed_dates_per_row: 5
```

The helper collects only the locked completed trading dates. It must not export any row outside the target window.

## Locked Output Root

The helper writes only under:

```text
C:\Users\openclaw\Desktop\Carver\docs\researchops\first_data_intake\quarantine\16_SYMBOL_DAILY_LAST_2026-05-18_2026-05-22\helper_raw_output\
```

Replacement is disabled:

```csharp
private const bool AllowReplaceExistingFiles = false;
```

## Raw Helper Output Policy

The helper output is explicitly:

```text
HELPER_RAW_OUTPUT_WITH_TEMPLATE_DERIVED_UTC_SESSION_END_TIMESTAMPS_NOT_PROVIDER_VERBATIM_TIME0
```

Each output row includes:

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

OHLCV values are helper output from NinjaTrader chart/AddDataSeries loaded daily Last bars. They remain quarantine-only until a later separately authorized parsing/intake gate validates row shape, timestamps, stale/missing behavior, duplicates, and session alignment.

## Internal Lock Checks

The helper rejects:

- wrong operator acknowledgement token;
- unarmed execution;
- primary chart not in the locked manifest;
- primary chart not `1 Day`;
- primary chart not `Last`;
- manifest row-count drift;
- duplicate row IDs;
- duplicate symbols;
- undeclared symbol/contract pairs;
- `NinjaTraderContract` drift from locked runtime `SYMBOL MONYY` syntax;
- `LocalContract` drift from locked `SYMBOL MM-YY` syntax;
- loaded NinjaTrader trading-hours template mismatch against the row's locked static template;
- output-root drift;
- missing expected completed daily rows;
- duplicate completed daily rows;
- existing target output file before write;
- existing temp output file before write;
- replacement unless a future separately authorized patch changes replacement policy.

The helper also cleans up any temp files and any just-moved batch outputs if a file-system error occurs during batch write/move, preserving batch all-or-nothing semantics as far as the local file system permits.

If any row is unavailable or incomplete, the helper records the row-level failure and prints:

```text
CARVER_16_SYMBOL_CHART_SERIES_EXPORT_AVAILABILITY_FAILURE
```

It then fails before any helper raw-output directory/file write.

## Handoff Instructions For Later Execution Gate

A later execution gate, if separately authorized, should:

1. Copy the helper from:

```text
C:\Users\openclaw\Desktop\Carver\tools\nt8\Carver16SymbolDailyChartSeriesExporterSessionEndUtc.cs
```

to the NinjaTrader custom indicators folder:

```text
C:\Users\openclaw\Documents\NinjaTrader 8\bin\Custom\Indicators\Carver16SymbolDailyChartSeriesExporterSessionEndUtc.cs
```

2. Under that later execution authorization only, arm the imported copy:

```csharp
private const bool ExecutionArmed = true;
```

3. Compile in NinjaTrader Desktop.

4. Open a `1 Day` / `Last` chart for one locked manifest dated contract, with enough loaded history to cover `2026-05-18` through `2026-05-22`.

5. Apply `Carver16SymbolDailyChartSeriesExporterSessionEndUtc` once, with:

```text
Operator acknowledgement = OPERATOR_AUTHORIZED_16_SYMBOL_DAILY_LAST_2026_05_18_TO_2026_05_22
```

6. Confirm that the helper writes only under the locked output root, or fails closed with row/date availability messages.

7. Do not manually edit, repair, rename, substitute, merge, back-adjust, forward-fill, or reweight helper outputs.

This handoff does not authorize taking those steps now.

## Expected Helper Output File Names

If later executed successfully, the helper should create exactly:

```text
ZT_06-26_Daily_Last_2026-05-18_2026-05-22_TEMPLATE_SESSION_END_UTC.csv
ZF_06-26_Daily_Last_2026-05-18_2026-05-22_TEMPLATE_SESSION_END_UTC.csv
ZN_06-26_Daily_Last_2026-05-18_2026-05-22_TEMPLATE_SESSION_END_UTC.csv
MES_06-26_Daily_Last_2026-05-18_2026-05-22_TEMPLATE_SESSION_END_UTC.csv
MNQ_06-26_Daily_Last_2026-05-18_2026-05-22_TEMPLATE_SESSION_END_UTC.csv
M2K_06-26_Daily_Last_2026-05-18_2026-05-22_TEMPLATE_SESSION_END_UTC.csv
MYM_06-26_Daily_Last_2026-05-18_2026-05-22_TEMPLATE_SESSION_END_UTC.csv
QM_07-26_Daily_Last_2026-05-18_2026-05-22_TEMPLATE_SESSION_END_UTC.csv
RB_07-26_Daily_Last_2026-05-18_2026-05-22_TEMPLATE_SESSION_END_UTC.csv
ZC_07-26_Daily_Last_2026-05-18_2026-05-22_TEMPLATE_SESSION_END_UTC.csv
ZS_07-26_Daily_Last_2026-05-18_2026-05-22_TEMPLATE_SESSION_END_UTC.csv
ZM_07-26_Daily_Last_2026-05-18_2026-05-22_TEMPLATE_SESSION_END_UTC.csv
ZL_07-26_Daily_Last_2026-05-18_2026-05-22_TEMPLATE_SESSION_END_UTC.csv
ZW_07-26_Daily_Last_2026-05-18_2026-05-22_TEMPLATE_SESSION_END_UTC.csv
HE_06-26_Daily_Last_2026-05-18_2026-05-22_TEMPLATE_SESSION_END_UTC.csv
LE_06-26_Daily_Last_2026-05-18_2026-05-22_TEMPLATE_SESSION_END_UTC.csv
```

## Validation Performed In This Gate

Read-only/source checks performed:

```text
helper file exists: YES
helper SHA256 recorded: YES
ExecutionArmed default false: YES
disarmed helper returns before AddDataSeries: YES
AllowReplaceExistingFiles false: YES
manifest row declarations: 16
AddDataSeries path present: YES
BarsRequest path absent: YES
SYMBOL MONYY NinjaTrader runtime contract syntax used for loading and primary validation: YES
SYMBOL MM-YY local ledger contract syntax preserved for output/provenance: YES
runtime trading-hours template check present: YES
file-write cleanup on batch failure present: YES
locked output root present: YES
1 Day Last lock present: YES
timestamp policy label present: YES
operator acknowledgement token present: YES
availability-failure print label present: YES
quarantine output folder created: NO
```

No NinjaTrader compile, import, execution, export, provider API access, market-row parsing, diagnostics, backtests, or remote operations were performed.

## Next Clean Gate

Selected next gate:

```text
CARVER_16_SYMBOL_NINJATRADER_CHART_ADDDATASERIES_EXPORT_HELPER_HOSTILE_AUDIT
```

That lean hostile audit may inspect the helper and process handoff read-only. It must not execute NinjaTrader, export data, parse market rows, run diagnostics, run backtests, or perform remote operations.

After a clean audit, the next implementation step would be a separately authorized local NinjaTrader chart/AddDataSeries helper execution gate.

## Non-Authorization

This helper gate authorizes no new data export, no provider API access, no market-row parsing, no NinjaTrader historical export, no diagnostics, no backtests, no forecasts, no positions, no costs, no carry, no trend, no OOS, no Lockbox, no Forward, no CFD adapter work, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no GitHub staging, no commit, no push, no PR update/opening, and no remote operations.
