# Carver MES Static Dated-Contract Source Extract

Date: 2026-05-30

Status:

```text
PROCESS_SOURCE_CARVER_MES_STATIC_DATED_CONTRACT_SOURCE_EXTRACT_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Scope

Narrow source extract for the Carver NinjaTrader-supported pilot MES static dated-contract lock gate.

Candidate:

```text
MES 06-26
```

Target completed trading-date window:

```text
2026-05-18 through 2026-05-22 inclusive
```

No market rows, NinjaTrader historical exports, provider APIs, diagnostics, or backtests were used.

## Official CME Static Evidence

Source:

```text
https://www.cmegroup.com/trading/equity-index/files/cme-micro-e-mini-futures-fact-card.pdf
```

Extracted static atoms:

- product family: Micro E-mini S&P 500;
- product code: `MES`;
- contract size: `$5 x S&P 500 Index`;
- minimum tick: `0.25` index points, equal to `$1.25` per contract;
- contract months: five months in the March quarterly cycle, meaning March, June, September, December;
- delivery: cash settlement by reference to final settlement price;
- final settlement price basis: Special Opening Quotation of the index;
- last day of trading: third Friday of the delivery month;
- expiring futures terminate at `8:30 a.m. CT` on last day of trading;
- listed with and subject to CME rules.

Source:

```text
https://www.cmegroup.com/markets/equities/sp/micro-e-mini-sandp-500.contractSpecs.html
```

Extracted static atoms:

- product page identifies Micro E-mini S&P 500 futures as `MES`;
- contract unit is `$5 x S&P 500 Index`;
- minimum price fluctuation is `0.25` index points.

## Official NinjaTrader Static Evidence

Source:

```text
https://ninjatrader.com/support/helpguides/nt8/rolling_over_a_futures_contrac.htm
```

Extracted static atoms:

- NinjaTrader futures instruments use contract expiry selection;
- manual rollover can be done by typing the next contract expiry in the instrument selector;
- documented syntax example uses `SYMBOL MM-YY`, for example `ES 09-16` to `ES 12-16`.

## Local NinjaTrader Static Evidence

Source:

```text
C:\Users\openclaw\Documents\NinjaTrader 8\db\NinjaTrader.sqlite
```

Read-only query result for `MES` and expiry tick `639158688000000000`:

```text
Instrument Id: 699839150768036
Master Name: MES
Description: Micro E-mini S&P 500 Futures
IsServerSupported: 1
TradingHours: CME US Index Futures ETH
PointValue: 5.0
TickSize: 0.25
ExchangeCode: 23
ExpiryDate: 2026-06-01
```

Direct file hashing of `NinjaTrader.sqlite` was not available because the file was locked by a running NinjaTrader process. The query was performed read-only.

## Derived Lock Atoms

The following derived static atoms are locked for the narrow MES pilot:

- `MES 06-26` is the NinjaTrader local dated-contract syntax candidate for June 2026;
- June 2026 is a valid March-quarterly-cycle delivery month for MES;
- the target completed trading-date window ends before the third Friday of June 2026;
- MES is cash settled, so there is no physical delivery or first-notice-date blocker for this first tiny price-bar intake candidate;
- the local NinjaTrader static expiry row exists for June 2026 and is server supported.

## Non-Authorization

This extract authorizes no code edits, no tests, no real market data, no market-row parsing, no NinjaTrader historical export, no provider API access, no diagnostics, no backtests, no returns, no PnL, no Sharpe, no drawdown, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old QuantLab pipeline use, no tuning, no deployment, no trading, no promotion, no remote push, and no GitHub action.
