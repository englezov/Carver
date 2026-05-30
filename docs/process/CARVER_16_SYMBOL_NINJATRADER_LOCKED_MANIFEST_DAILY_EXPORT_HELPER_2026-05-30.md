# Carver 16-Symbol NinjaTrader Locked Manifest Daily Export Helper

Date: 2026-05-30

Status:

```text
LOCAL_PROCESS_CARVER_16_SYMBOL_NINJATRADER_LOCKED_MANIFEST_DAILY_EXPORT_HELPER_NOT_EXECUTED_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Create the locked local NinjaTrader Desktop helper and process handoff for the later 16-symbol daily intake pilot.

This gate follows:

```text
docs/process/CARVER_16_SYMBOL_NINJATRADER_BATCH_DAILY_INTAKE_SHAPE_GATE_DRAFT_2026-05-30.md
```

It creates helper code and instructions only. It does not run the helper, copy it into NinjaTrader's live custom indicator folder, export historical bars, parse market rows, access provider APIs, run diagnostics, run backtests, compute forecasts, compute positions, compute costs, compute carry, compute trend, deploy, trade, promote, stage Git changes, commit, push, update a PR, or perform remote operations.

## Helper Artifact

Repo helper:

```text
tools/nt8/Carver16SymbolDailyExporterSessionEndUtc.cs
```

SHA256:

```text
22C76501A9F4296D243972902770527074C851F207AB590089009E8B63623666
```

NinjaTrader indicator class:

```text
Carver16SymbolDailyExporterSessionEndUtc
```

The helper is disarmed by default:

```csharp
private const bool ExecutionArmed = false;
```

It requires a file edit under a later separately authorized execution gate:

```csharp
private const bool ExecutionArmed = true;
```

It also requires the operator acknowledgement token in NinjaTrader:

```text
OPERATOR_AUTHORIZED_16_SYMBOL_DAILY_LAST_2026_05_18_TO_2026_05_22
```

## Locked Manifest

The helper embeds exactly 16 rows:

| Row ID | Symbol | NinjaTrader symbol | Local contract | Template | Template session end |
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

The helper requests no other symbol, contract, timeframe, bar type, or date window.

## Locked Output Root

The helper writes only under:

```text
C:\Users\openclaw\Desktop\Carver\docs\researchops\first_data_intake\quarantine\16_SYMBOL_DAILY_LAST_2026-05-18_2026-05-22\helper_raw_output\
```

It refuses output root drift.

Replacement is disabled by default:

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

The helper writes template-derived UTC session-end timestamps. It does not preserve NinjaTrader provider-verbatim `Time[0]` as the canonical timestamp.

OHLCV values are helper output from NinjaTrader historical bars. They remain quarantine-only until a later separately authorized parsing/intake gate validates row shape, timestamps, stale/missing behavior, duplicates, and session alignment.

## Internal Lock Checks

The helper rejects:

- manifest row-count drift;
- duplicate row IDs;
- duplicate symbols;
- undeclared symbol/contract pairs;
- `NinjaTraderSymbol` drift from the locked `SYMBOL MONYY` syntax;
- `LocalContract` drift from the locked `SYMBOL MM-YY` syntax;
- output-root drift;
- any contract month not in the embedded manifest;
- missing expected completed daily rows;
- duplicate completed daily rows;
- rows outside `2026-05-18` through `2026-05-22`;
- any existing target output file before the write phase starts;
- any existing temp output file before the write phase starts;
- existing target files unless a future separately authorized patch changes replacement policy.

The helper collects all 16 manifest row responses in memory and writes outputs only after all 16 requests have returned five completed rows each.

If any row is unavailable, has missing expected completed daily bars, has duplicate completed dates, has rows outside the locked date window, or has a BarsRequest error, the helper records the row-level failure and continues collecting the rest of the manifest. After all 16 responses are accounted for, it prints every row/date availability failure with:

```text
CARVER_16_SYMBOL_DAILY_EXPORT_AVAILABILITY_FAILURE
```

and then fails once before any helper raw-output directory/file write.

Before writing any helper raw-output file, the helper now preflights all 16 target output paths and all 16 temp paths. If any target or temp conflict exists, it fails before writing the first file. This preserves the all-or-nothing write boundary required by the batch shape gate.

## Audit-Fix Record

Prior helper SHA256:

```text
EAC0009D94ACB1FF45F6A36472410B0E3DBBE8668AEBF452F4F3EE99D53E18AD
```

Lean hostile audit finding:

```text
FAIL_HELPER_WRITE_PHASE_PRECHECK_REQUIRED
```

Fix applied:

```text
PREFLIGHT_ALL_16_TARGET_OUTPUT_PATHS_AND_TEMP_PATHS_BEFORE_ANY_FILE_WRITE
```

New helper SHA256:

```text
25DE90BFF6A87435E3699CE1849B30E3F76CACC6F317902C0FBD1E957B91AA03
```

No NinjaTrader execution, data export, provider API access, market-row parsing, diagnostics, backtests, or remote operations occurred while applying this fix.

## Availability-Preflight Patch Record

Prior helper SHA256:

```text
25DE90BFF6A87435E3699CE1849B30E3F76CACC6F317902C0FBD1E957B91AA03
```

Fail-closed execution evidence:

```text
docs/process/CARVER_16_SYMBOL_NINJATRADER_BATCH_EXPORT_FAIL_CLOSED_REDECISION_2026-05-30.md
BATCH_EXPORT_FAIL_CLOSED_PROVIDER_BARS_UNAVAILABLE
```

Patch applied:

```text
AGGREGATE_ALL_16_ROW_DATE_AVAILABILITY_FAILURES_BEFORE_ANY_HELPER_RAW_OUTPUT_WRITE
```

New helper SHA256:

```text
22C76501A9F4296D243972902770527074C851F207AB590089009E8B63623666
```

The patch keeps:

```text
ExecutionArmed default false
AllowReplaceExistingFiles false
16 manifest rows unchanged
1 Day Last unchanged
2026-05-18 through 2026-05-22 unchanged
locked output root unchanged
template-session-end UTC helper-output policy unchanged
```

No NinjaTrader execution, data export, provider API access, market-row parsing, diagnostics, backtests, or remote operations occurred while applying this availability-preflight patch.

## Handoff Instructions For Later Execution Gate

A later execution gate, if separately authorized, should:

1. Copy the helper from:

```text
C:\Users\openclaw\Desktop\Carver\tools\nt8\Carver16SymbolDailyExporterSessionEndUtc.cs
```

to the NinjaTrader custom indicators folder:

```text
C:\Users\openclaw\Documents\NinjaTrader 8\bin\Custom\Indicators\Carver16SymbolDailyExporterSessionEndUtc.cs
```

The copy should be made fresh from the repo helper SHA in this document. Any previously imported and armed NinjaTrader copy from the fail-closed attempt is not the locked helper authority for a later run.

2. Under that later execution authorization only, edit the copied file or repo helper as directed by the gate:

```csharp
private const bool ExecutionArmed = true;
```

3. Compile in NinjaTrader Desktop.

4. Apply `Carver16SymbolDailyExporterSessionEndUtc` once, with:

```text
Operator acknowledgement = OPERATOR_AUTHORIZED_16_SYMBOL_DAILY_LAST_2026_05_18_TO_2026_05_22
```

5. Confirm that the helper writes only under the locked output root.

6. Do not manually edit, repair, rename, substitute, merge, back-adjust, forward-fill, or reweight helper outputs.

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
manifest row declarations: 16
locked output root present: YES
1 Day Last lock present: YES
timestamp policy label present: YES
operator acknowledgement token present: YES
all target output paths preflighted before any write: YES
all temp output paths preflighted before any write: YES
all row/date availability failures aggregated before any write: YES
```

No NinjaTrader compile, import, execution, export, provider API access, market-row parsing, diagnostics, backtests, or remote operations were performed.

## Next Clean Gate

Selected next gate:

```text
CARVER_16_SYMBOL_NINJATRADER_LOCKED_MANIFEST_DAILY_EXPORT_HELPER_HOSTILE_AUDIT
```

That audit should be a lean hostile audit of the helper code and this process handoff. It may inspect the helper and process files read-only. It must not execute NinjaTrader, export data, parse market rows, run diagnostics, run backtests, or perform remote operations.

After a clean audit, the next implementation step would be a separately authorized helper execution and quarantine-only intake parsing gate.

## Non-Authorization

This helper gate authorizes no new data export, no provider API access, no market-row parsing, no NinjaTrader historical export, no diagnostics, no backtests, no forecasts, no positions, no costs, no carry, no trend, no OOS, no Lockbox, no Forward, no CFD adapter work, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no GitHub staging, no commit, no push, no PR update/opening, and no remote operations.
