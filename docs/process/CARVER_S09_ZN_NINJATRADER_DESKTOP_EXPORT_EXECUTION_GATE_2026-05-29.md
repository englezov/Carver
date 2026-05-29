# Carver S09 ZN NinjaTrader Desktop Export Execution Gate

Date: 2026-05-29

Status:

```text
CARVER_S09_ZN_NINJATRADER_DESKTOP_EXPORT_EXECUTION_GATE_OPEN_NOT_YET_EXPORTED_NOT_DIAGNOSTIC
```

## Purpose

Open the one-shot NinjaTrader Desktop export gate for the locked S09 ZN direct-daily intake slice, after the Tradovate web/API-token path was blocked by missing API access.

## Exact Export Boundary

```text
source: NinjaTrader Desktop local data/provider access
artifact: tools/nt8/CarverDailyBarExporter.cs
contract: ZN
contract month: 06-26
NinjaTrader chart name: ZN JUN26
Carver export display symbol: ZN 06-26
bar type: Last
timeframe: 1 Day
required completed rows: 257
last completed trade date UTC: 2026-05-28
locked output file: ZN_06-26_Daily_Last_257.csv
locked output directory: C:\Users\openclaw\Desktop\Carver\data\quarantine\ninjatrader\desktop_daily_exports
```

Rationale for `last completed trade date UTC: 2026-05-28`:

- The current date is 2026-05-29.
- The current 2026-05-29 daily bar is not treated as completed by this gate.
- Completed bars only.

## Allowed Actions

- Place/import `tools/nt8/CarverDailyBarExporter.cs` into NinjaTrader Desktop's custom indicator workflow.
- Attach the indicator to an exact `ZN 06-26` 1 Day chart.
- Set:

```text
ExpectedNinjaTraderInstrumentFullName = ZN JUN26
ExpectedCarverDisplaySymbol = ZN 06-26
ExpectedInstrumentCode = ZN
ExpectedContractMonth = 06-26
LastCompletedTradeDateUtc = 2026-05-28
RequiredBars = 257
OutputDirectory = C:\Users\openclaw\Desktop\Carver\data\quarantine\ninjatrader\desktop_daily_exports
```

- Produce exactly one quarantined CSV/text output:

```text
C:\Users\openclaw\Desktop\Carver\data\quarantine\ninjatrader\desktop_daily_exports\ZN_06-26_Daily_Last_257.csv
```

- After the file exists, run only the Carver-side schema/identity/completed-bar parser validation for this file.

## Current Local Preflight

Preflight before execution found:

```text
origin remote: https://github.com/englezov/Carver.git
branch state after push: master...origin/master
NinjaTrader process: running
NinjaTrader custom indicator folder: present
locked export file: absent
```

No desktop export had run at the time this gate was opened.

## Source Placement

The exporter source was copied, without execution, to the NinjaTrader custom indicator folder:

```text
source: C:\Users\openclaw\Desktop\Carver\tools\nt8\CarverDailyBarExporter.cs
target: C:\Users\openclaw\Documents\NinjaTrader 8\bin\Custom\Indicators\CarverDailyBarExporter.cs
sha256: A29B94A0E1D4A9CC1EFAB4F997D88F6B70CA1C83D3B9D3D01EFBB890731F6FE5F85B
```

No NinjaTrader compile, import confirmation, chart attachment, or data export was performed by this file copy.

## Runtime Patch

After the first chart attempt, NinjaTrader displayed the chart instrument as `ZN JUN26`. The exporter was patched to distinguish:

```text
NinjaTrader chart name: ZN JUN26
Carver export display symbol: ZN 06-26
```

The default `LastCompletedTradeDateUtc` was then set to the locked gate date:

```text
2026-05-28
```

This reduces manual property-entry risk but does not broaden the export boundary.

If NinjaTrader's indicator UI leaves `LastCompletedTradeDateUtc` blank, the exporter now falls back internally to the same locked gate date, `2026-05-28`. If the UI leaves `RequiredBars` unset or zero, the exporter falls back internally to the same locked row count, `257`. Any non-blank/non-zero value outside those locks still blocks.

The exporter was then patched to avoid relying on NinjaTrader's final chart-bar callback. It now keeps a rolling 257-row buffer and writes once it reaches the locked completed trade date, or attempts the same final write if it sees a newer in-progress bar. If fewer than 257 completed daily rows are loaded, it prints a waiting/blocking line with the loaded row count and stops without creating a file.

## Stop Conditions

Stop without trying to fix inside NinjaTrader if:

- NinjaTrader cannot load `ZN 06-26`;
- a `1 Day` chart cannot be opened;
- fewer than 257 completed daily bars are available;
- the script compile/import fails;
- the output file is not exactly the locked filename;
- any path outside the Carver quarantine is required;
- any order/account/report/trading prompt appears;
- any API token, browser storage, cookie, localStorage, or session extraction is requested.

## Non-Authorization

This gate authorizes no trading, no order routing, no account endpoint, no report endpoint, no Tradovate web API token, no browser storage inspection, no credential extraction, no diagnostics, no backtest, no returns, no PnL, no Sharpe, no drawdown, no OOS, no Lockbox, no Forward, no CFD adapter, no old QuantLab import, no tuning, no deployment, no promotion, and no remote push by inference.
