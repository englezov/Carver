# Carver NinjaTrader Desktop Daily Export Bridge Gate

Date: 2026-05-29

Status:

```text
CARVER_S09_ZN_NINJATRADER_DESKTOP_DAILY_EXPORT_BRIDGE_IMPLEMENTED_NOT_DATA_NOT_DIAGNOSTIC
```

## Purpose

Replace the blocked Tradovate web/API-token path with a desktop-side NinjaTrader export bridge for the S09 ZN direct-daily intake probe.

This gate creates a minimal local artifact/spec for exporting completed daily ZN bars from NinjaTrader Desktop into the Carver Git-ignored quarantine.

## Authorized Surface

Instrument identity:

```text
contract: ZN
contract month: 06-26
desktop display symbol: ZN 06-26
bar type: Last
timeframe: 1 Day
required completed rows: 257
```

NinjaScript artifact:

```text
tools/nt8/CarverDailyBarExporter.cs
```

Carver parser/validator:

```text
src/carver/spine/ninjatrader_desktop_export.py
```

The parser is hard-locked to the same single export surface as the NinjaScript artifact:

```text
ZN 06-26 / ZN 06-26 / Last / 1 Day / exactly 257 rows
```

It does not admit generic NinjaTrader daily exports, MES/ES substitutes, adjacent contracts, or alternate row counts.

Synthetic tests:

```text
tests/test_ninjatrader_desktop_daily_export_synthetic.py
```

Output quarantine:

```text
C:\Users\openclaw\Desktop\Carver\data\quarantine\ninjatrader\desktop_daily_exports
```

Locked output file name:

```text
ZN_06-26_Daily_Last_257.csv
```

The output path is Git-ignored through the existing `data/` ignore rule.

## Export Schema

The NinjaScript bridge writes exactly this CSV header:

```text
instrument,contract_month,display_symbol,bar_type,timeframe,trade_date,open,high,low,close,volume
```

Rows are admitted only if:

- `instrument == ZN`;
- `contract_month == 06-26`;
- `display_symbol == ZN 06-26`;
- `bar_type == Last`;
- `timeframe == 1 Day`;
- `trade_date` uses `YYYY-MM-DD`;
- OHLC values are finite positive numbers;
- volume is finite and non-negative;
- rows are strictly increasing by trade date;
- row count is exactly 257.

The parser converts each `trade_date` into a date-aligned UTC `CompletedBar` at `00:00:00+00:00`. No intraday timestamp or session assumption is inferred from the desktop export.

## Implementation Boundary

The NinjaScript artifact is an indicator-style export bridge. It is not a strategy and contains no order-routing logic.

The script refuses to write unless:

- it is attached to `ZN 06-26`;
- the chart uses `1 Day` bars;
- `RequiredBars == 257`;
- `LastCompletedTradeDateUtc` is explicitly set as `YYYY-MM-DD`;
- output stays under `C:\Users\openclaw\Desktop\Carver\data\quarantine\ninjatrader\desktop_daily_exports`.

It keeps only rows with `trade_date <= LastCompletedTradeDateUtc` and writes the last 257 eligible completed daily rows.

If an in-progress current daily bar is present after the locked completed date, the script attempts the final write before returning from that newer bar. The file write uses a temporary file followed by move into the locked output filename, reducing partial-output risk.

## Official Documentation Anchors

NinjaTrader official docs record that:

- the Historical Data window supports import, export, edit, and download of historical data;
- historical data can be downloaded from the connected data provider;
- historical data exports write text files;
- exported historical data uses end-of-bar timestamps in UTC;
- NinjaScript can write OHLC/date-stamped data to files with `StreamWriter`;
- `BarsRequest` exists for requesting bar data inside NinjaScript/add-on contexts;
- ATI is not a full market-data API and is therefore not the route for this bridge.

Sources:

- <https://ninjatrader.com/support/helpGuides/nt8/historical_data_manager.htm>
- <https://ninjatrader.com/ru/support/helpGuides/nt8/download.htm>
- <https://ninjatrader.com/support/helpGuides/nt8/exporting.htm>
- <https://developer.ninjatrader.com/docs/desktop/using_streamwriter_to_write_to_a_text_file>
- <https://developer.ninjatrader.com/docs/desktop/barsrequest>
- <https://ninjatrader.com/support/helpguides/nt7/automated_trading_interface_at.htm>

## Execution State

No NinjaTrader Desktop export was executed by this gate.

No real ZN data file was created by this gate.

This gate only adds the bridge artifact, Carver-side parser, and synthetic conformance tests.

## Next Operator Gate

A separate execution gate is required before importing/running the NinjaScript bridge in NinjaTrader Desktop or parsing a real exported file.

That future gate must specify:

- `LastCompletedTradeDateUtc`;
- whether the operator has connected NinjaTrader Desktop to the data provider;
- the exact chart/instrument context;
- the expected quarantine file path;
- whether the one-shot export may be consumed by Carver parser validation.

## Non-Authorization

This gate authorizes no NinjaTrader Desktop run, no data export execution, no strategy execution, no trading, no order routing, no account endpoint, no report endpoint, no Tradovate web API token, no browser storage inspection, no credential extraction, no diagnostics, no backtest, no returns, no PnL, no Sharpe, no OOS, no Lockbox, no Forward, no CFD adapter, no old QuantLab import, no tuning, no deployment, no promotion, and no remote push by inference.
