# Carver NinjaTrader-Supported Pilot MES Tiny Daily Export Helper

Date: 2026-05-30

Status:

```text
PROCESS_AND_LOCAL_HELPER_CARVER_NINJATRADER_SUPPORTED_PILOT_MES_TINY_DAILY_EXPORT_HELPER_NOT_EXECUTED_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Create a locked local NinjaTrader Desktop helper for the MES-only tiny historical-bar intake pilot.

This gate creates helper code and run instructions only. It does not execute NinjaTrader, export historical data, parse market rows, run diagnostics, run backtests, compute forecasts, size positions, deploy, trade, promote, call provider APIs, or touch old QuantLab pipelines.

## Helper

```text
tools/nt8/CarverMesTinyDailyExporter.cs
```

SHA256:

```text
788504D71541C6119FE4E90D71867BB16AB8A92717998A3A326642938AA0CDDF
```

The helper is disabled by default:

```text
ExecutionArmed = false
```

It requires explicit arming inside the file before any local NinjaTrader run:

```text
private const bool ExecutionArmed = true;
```

It also requires this acknowledgement token in the NinjaTrader indicator properties:

```text
OPERATOR_AUTHORIZED_MES_06_26_2026_05_18_TO_2026_05_22
```

## Locked Export Surface

Only this surface is admitted:

```text
NinjaTrader instrument: MES JUN26
Carver local contract: MES 06-26
bar type: Last
timeframe: 1 Day
completed trading-date window: 2026-05-18 through 2026-05-22 inclusive
expected rows: 5
```

The helper rejects every other chart instrument, contract, timeframe, output path, missing row set, duplicate row, or existing target file.

## Locked Output

Output directory:

```text
C:\Users\openclaw\Desktop\Carver\docs\researchops\first_data_intake\quarantine\MES_06_26_2026-05-18_2026-05-22\raw_source_copy
```

Output file:

```text
MES_06-26_Daily_Last_2026-05-18_2026-05-22_TEMPLATE_SESSION_END_UTC.csv
```

Schema:

```text
provider_symbol,local_contract,timestamp_utc,open,high,low,close,volume
```

This output is the raw source copy for the tiny intake gate. It is not a strategy dataset, diagnostic dataset, backtest dataset, or promotion artifact.

Timestamp policy:

```text
timestamp_utc = extracted CME US Index Futures ETH TradingDay session end
timezone = Central Standard Time
local session end = 16:00
UTC conversion performed by helper
```

The earlier raw file:

```text
MES_06-26_Daily_Last_2026-05-18_2026-05-22.csv
```

is preserved as a fail-closed source artifact and must not be overwritten or silently modified.

## Local Run Instructions

1. In NinjaTrader Desktop, open a chart for:

```text
MES 06-26 / MES JUN26
1 Day
Last
```

2. Make sure the chart has loaded the completed daily bars covering:

```text
2026-05-18 through 2026-05-22
```

3. Import or paste the helper from:

```text
C:\Users\openclaw\Desktop\Carver\tools\nt8\CarverMesTinyDailyExporter.cs
```

4. Only when ready to perform the authorized local export, edit the file so:

```text
private const bool ExecutionArmed = true;
```

5. Apply the indicator to the MES JUN26 1 Day Last chart and set:

```text
OperatorAcknowledgement = OPERATOR_AUTHORIZED_MES_06_26_2026_05_18_TO_2026_05_22
```

6. Confirm the file appears at:

```text
C:\Users\openclaw\Desktop\Carver\docs\researchops\first_data_intake\quarantine\MES_06_26_2026-05-18_2026-05-22\raw_source_copy\MES_06-26_Daily_Last_2026-05-18_2026-05-22.csv
```

After the timestamp policy patch, the expected corrected output is:

```text
C:\Users\openclaw\Desktop\Carver\docs\researchops\first_data_intake\quarantine\MES_06_26_2026-05-18_2026-05-22\raw_source_copy\MES_06-26_Daily_Last_2026-05-18_2026-05-22_TEMPLATE_SESSION_END_UTC.csv
```

7. After export, return the helper to:

```text
private const bool ExecutionArmed = false;
```

The subsequent Carver intake rerun must parse only that one file and apply only the locked row-shape, timestamp, TradingDay, template/CME conflict, stale/missing/duplicate, and session-alignment checks.

## Boundary

The helper contains no order-routing logic, no strategy logic, no diagnostics, no backtest logic, no return calculation, no PnL calculation, no Sharpe calculation, no drawdown calculation, no forecast computation, no position sizing, no cost logic, no carry logic, no trend logic, no OOS/Lockbox/Forward access, no CFD adapter behavior, no old QuantLab imports, no remote operations, and no promotion path.

## Next Clean Gate

After the raw export file exists in the locked `raw_source_copy/` folder, the next clean gate is:

```text
MES_TINY_HISTORICAL_BAR_INTAKE_RERUN_AGAINST_EXPLICIT_RAW_FILE
```

That rerun should ingest only:

```text
docs/researchops/first_data_intake/quarantine/MES_06_26_2026-05-18_2026-05-22/raw_source_copy/MES_06-26_Daily_Last_2026-05-18_2026-05-22.csv
```

After the timestamp policy patch, the rerun should ingest only:

```text
docs/researchops/first_data_intake/quarantine/MES_06_26_2026-05-18_2026-05-22/raw_source_copy/MES_06-26_Daily_Last_2026-05-18_2026-05-22_TEMPLATE_SESSION_END_UTC.csv
```

## Non-Authorization

This helper gate authorizes no NinjaTrader execution by Codex, no market-row parsing, no diagnostics, no backtests, no returns, no PnL, no Sharpe, no drawdown, no forecast computation, no position sizing, no costs, no carry, no trend, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old QuantLab pipeline use, no tuning, no deployment, no trading, no promotion, no provider API access, no remote push, and no GitHub action.
