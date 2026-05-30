# Carver NinjaTrader-Supported Pilot Static Dated Contract Selection Shape Gate Draft

Date: 2026-05-30

Status:

```text
PROCESS_ONLY_CARVER_NINJATRADER_SUPPORTED_PILOT_STATIC_DATED_CONTRACT_SELECTION_SHAPE_GATE_DRAFT_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Define the process boundary for selecting explicit dated NinjaTrader futures contracts before any first historical-bar intake pilot.

This draft follows the first historical-bar intake decision:

```text
KEEP_16_ROW_PILOT_BLOCKED_FOR_IMMEDIATE_HISTORICAL_BAR_INTAKE
```

It does not select dated contracts, export NinjaTrader data, parse market rows, run diagnostics, run backtests, or open a trading lane.

## Current Source Universe

The current NinjaTrader-supported pilot candidate universe remains:

```text
ZT, ZF, ZN, MES, MNQ, M2K, MYM, QM, RB, ZC, ZS, ZM, ZL, ZW, HE, LE
```

Current readiness facts from the final static lock ledger:

```text
FINAL_STATIC_READY_FOR_TINY_HISTORICAL_BAR_INTAKE: 0
FINAL_STATIC_CONTRACT_IDENTITY_FAIL_CLOSED_NOT_READY_FOR_TINY_HISTORICAL_BAR_INTAKE: 16
EXPLICIT_DATED_CONTRACT_MONTH_SELECTED: 0
ACTIVE_LISTED_STATUS_LOCKED: 0
```

## First Intake Shape Decision

The first future historical-bar intake should not attempt all 16 symbols.

Selected tiny candidate row set for the first dated-contract selection execution gate:

```text
ZN, MES, QM, ZC
```

Reason:

- `ZN` covers the CBOT Treasury/rates template family;
- `MES` covers the CME equity index template family;
- `QM` covers the NYMEX energy template family;
- `ZC` covers the CBOT agricultural template family;
- this four-row shape tests multiple static template families without turning the first intake into a universe-wide readiness event.

If any of these four rows fails static dated-contract selection, it must fail closed. The future execution gate may proceed only with rows that pass static selection, with a minimum of one passing row required before any later intake gate may be considered.

The remaining 12 pilot rows stay closed for this first tiny intake shape.

## Exact As-Of Date

Contract-month selection as-of date:

```text
2026-05-30
```

The as-of date is a static process date only. It is not market data and does not authorize checking provider availability.

## Exact Target Historical-Bar Intake Window

Target completed trading-date window:

```text
2026-05-18 through 2026-05-22 inclusive
```

This window is selected as a tiny five completed-trading-date pilot window before the current process date. A future intake gate must still reject any row/date that the local NinjaTrader Trading Hours template and CME conflict-check policy classify as closed, partial, ambiguous, stale, missing, duplicate, non-UTC, non-end-of-bar, or session-misaligned.

## Static Evidence Required Before Dated Contract Selection

The dated-contract selection execution gate must use only static evidence. Required evidence:

- current Carver provider mapping ledger;
- current Carver contract identity/final static lock ledger;
- local NinjaTrader static instrument definitions;
- local NinjaTrader static rollover/month metadata where available;
- official CME/CBOT/NYMEX static contract specification pages or PDFs for contract months, active/listed status, last trade/expiration, and delivery-cycle constraints;
- local NinjaTrader Trading Hours template evidence already extracted for the selected rows.

Forbidden evidence:

- NinjaTrader historical export;
- provider API access;
- historical bar availability checks;
- market rows;
- diagnostics;
- backtests;
- performance evidence.

## Dated Contract Selection Rule

For each selected candidate row, the future execution gate must:

1. Preserve the Appendix C row ID, author market code, provider symbol, and local canonical instrument ID.
2. Confirm active/listed status from static evidence as of `2026-05-30`.
3. Enumerate only official listed contract months that cover the target window `2026-05-18` through `2026-05-22`.
4. Select the nearest official listed contract whose last-trade, expiration, first-notice, delivery, or cash-settlement constraints do not conflict with the full target window.
5. Confirm that the selected dated contract is representable in local NinjaTrader static contract-month syntax before any historical export is attempted.
6. Record the selected dated contract in both source-native and NinjaTrader-local form.
7. Fail closed if any conflict or ambiguity remains.

No continuous contract, merge policy, back-adjusted series, roll repair, substitution, or adjacent symbol may be used for the first intake.

## Row-Level Fail-Closed Rules

A row must remain closed if any of the following is true:

- active/listed status cannot be statically verified for the as-of date;
- the row has no official listed contract month covering the target window;
- the selected contract month cannot be represented in NinjaTrader local syntax;
- first-notice, last-trade, expiration, delivery, or settlement timing is ambiguous for the selected target window;
- local NinjaTrader and official CME/CBOT/NYMEX static evidence conflict;
- the local Trading Hours template is missing or hash-mismatched;
- a row would require continuous merge, back-adjustment, substitution, dropping after data visibility, or reweighting.

## Completed-Bar Parser Boundary For Later Intake

A later intake gate, if separately authorized, must be limited to:

- the rows that pass static dated-contract selection;
- the exact selected dated contract for each row;
- the exact target completed trading-date window;
- daily completed bars only;
- UTC end-of-bar timestamps only;
- local NinjaTrader `TradingDay` as canonical completed trading date;
- local Trading Hours template as operational filter;
- CME holiday/trading-hours evidence as conflict check;
- provider-recorded daily close only, with official settlement reconciliation closed.

The later intake gate must reject missing, duplicate, stale, future, non-UTC, non-end-of-bar, session-misaligned, substituted, or repaired rows.

## Next Clean Gate

Selected next gate:

```text
NINJATRADER_SUPPORTED_PILOT_STATIC_DATED_CONTRACT_SELECTION_EXECUTION_GATE
```

That gate should create a machine-readable dated-contract selection ledger for:

```text
ZN, MES, QM, ZC
```

It should record the selected contract or fail-closed status for each row using only static evidence.

## Non-Authorization

This draft authorizes no code edits, no tests, no real market data, no market-row parsing, no NinjaTrader historical export, no provider API access, no diagnostics, no backtests, no returns, no PnL, no Sharpe, no drawdown, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old QuantLab pipeline use, no tuning, no deployment, no trading, no promotion, no remote push, and no GitHub action.
