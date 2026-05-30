# Carver NinjaTrader-Supported Pilot MES Static Dated-Contract Lock

Date: 2026-05-30

Status:

```text
PROCESS_SOURCE_CARVER_NINJATRADER_SUPPORTED_PILOT_MES_STATIC_DATED_CONTRACT_LOCK_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Lock or fail-close the MES-only dated-contract candidate selected by the prior redecision gate:

```text
MES 06-26
```

This is a static process/source lock only. It does not authorize real market data, NinjaTrader historical export, provider API access, market-row parsing, diagnostics, backtests, trading, deployment, or promotion.

## Inputs

Redecision:

```text
docs/process/CARVER_NINJATRADER_SUPPORTED_PILOT_STATIC_DATED_CONTRACT_SELECTION_REDECISION_2026-05-30.md
```

Hash-bound source extract:

```text
docs/researchops/first_data_intake/CARVER_NINJATRADER_SUPPORTED_PILOT_MES_STATIC_DATED_CONTRACT_SOURCE_EXTRACT_2026-05-30.md
```

Source extract SHA256:

```text
72E9FA2F40AD66BEF7CB54307EE9AC0480FC509DA0952361E262BA93FAA39C2A
```

No market rows, historical-bar availability checks, NinjaTrader exports, provider APIs, diagnostics, or backtests were used.

## Output

Machine-readable MES static dated-contract selection ledger:

```text
docs/researchops/first_data_intake/CARVER_NINJATRADER_SUPPORTED_PILOT_MES_STATIC_DATED_CONTRACT_LOCK_2026-05-30.csv
```

SHA256:

```text
65E3F7C5E4E6D0B71DA78F6BDE742DFC2EA08263438A84F9D5ACD219FD6C1A7F
```

## Locked Static Contract

Selected static dated contract:

```text
MES_JUN_2026
MES 06-26
```

As-of date:

```text
2026-05-30
```

Target completed trading-date window:

```text
2026-05-18 through 2026-05-22 inclusive
```

## Static Lock Result

The MES row is statically ready for a later tiny historical-bar intake gate:

```text
STATIC_READY_FOR_LATER_TINY_HISTORICAL_BAR_INTAKE_NOT_DATA_AUTHORIZATION: 1
```

Locked atoms:

- official product and product code: Micro E-mini S&P 500 futures, `MES`;
- listed contract month rule: March quarterly cycle, including June;
- settlement/lifecycle rule: cash settled and terminates on the third Friday of the delivery month;
- target-window coverage: `2026-05-18` through `2026-05-22` precedes June 2026 third-Friday termination;
- local NinjaTrader static expiry row exists for June 2026;
- local NinjaTrader instrument is server-supported in the static database;
- local contract syntax: `MES 06-26`;
- local Trading Hours template: `CME US Index Futures ETH`.

## Boundary

This lock means only:

```text
MES 06-26 MAY BE USED AS THE SOLE STATICALLY READY CANDIDATE IN A LATER SEPARATELY AUTHORIZED TINY HISTORICAL-BAR INTAKE GATE
```

It does not authorize:

- opening NinjaTrader historical export;
- accessing provider APIs;
- parsing market rows;
- checking historical availability;
- repairing missing bars;
- diagnostics;
- backtests;
- OOS, Lockbox, Forward;
- CFD adapters;
- deployment;
- trading;
- promotion.

## Next Clean Gate

Selected next gate:

```text
NINJATRADER_SUPPORTED_PILOT_MES_TINY_HISTORICAL_BAR_INTAKE_SHAPE_GATE
```

That gate should define, before any export or parsing:

- exact row set: `MES 06-26` only;
- exact completed trading-date window: `2026-05-18` through `2026-05-22`;
- exact daily completed-bar fields to be accepted;
- UTC end-of-bar timestamp requirement;
- local NinjaTrader `TradingDay` mapping requirement;
- local Trading Hours template and CME conflict-check policy;
- strict stale/missing/duplicate/session-misaligned fail-closed rules;
- output quarantine path and no-diagnostics boundary.

It must not itself export NinjaTrader historical data or parse market rows unless separately authorized.

## Non-Authorization

This lock authorizes no code edits, no tests, no real market data, no market-row parsing, no NinjaTrader historical export, no provider API access, no diagnostics, no backtests, no returns, no PnL, no Sharpe, no drawdown, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old QuantLab pipeline use, no tuning, no deployment, no trading, no promotion, no remote push, and no GitHub action.
