# Carver NinjaTrader-Supported Pilot Static Dated-Contract Selection Redecision

Date: 2026-05-30

Status:

```text
PROCESS_ONLY_CARVER_NINJATRADER_SUPPORTED_PILOT_STATIC_DATED_CONTRACT_SELECTION_REDECISION_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Decide the next clean step after static dated-contract evidence intake for:

```text
ZN, MES, QM, ZC
```

This is a process-only decision artifact. It does not select contracts, export NinjaTrader data, parse market rows, run diagnostics, run backtests, or open any trading lane.

## Inputs

Evidence intake:

```text
docs/process/CARVER_NINJATRADER_SUPPORTED_PILOT_STATIC_DATED_CONTRACT_EVIDENCE_INTAKE_2026-05-30.md
docs/researchops/first_data_intake/CARVER_NINJATRADER_SUPPORTED_PILOT_STATIC_DATED_CONTRACT_EVIDENCE_INTAKE_2026-05-30.csv
```

Prior execution:

```text
docs/process/CARVER_NINJATRADER_SUPPORTED_PILOT_STATIC_DATED_CONTRACT_SELECTION_EXECUTION_2026-05-30.md
docs/researchops/first_data_intake/CARVER_NINJATRADER_SUPPORTED_PILOT_STATIC_DATED_CONTRACT_SELECTION_EXECUTION_2026-05-30.csv
```

No market rows, historical bars, NinjaTrader exports, provider APIs, diagnostics, or backtests were used.

## Current Evidence Summary

The evidence intake improved local static dated-contract evidence:

```text
LOCAL_NINJATRADER_STATIC_EXPIRY_ROW_FOUND: 4
```

Candidate local contracts recorded:

```text
ZN: ZN 06-26
MES: MES 06-26
QM: QM 06-26
ZC: ZC 07-26
```

But no row is ready for dated-contract selection re-execution:

```text
STATIC_READY_FOR_DATED_CONTRACT_SELECTION_REEXECUTION: 0
STATIC_DATED_CONTRACT_EVIDENCE_PARTIAL_FAIL_CLOSED_NOT_READY_FOR_SELECTION_REEXECUTION: 4
```

## Row Ranking

Strongest candidate:

```text
MES
```

Reason:

- local NinjaTrader static expiry row exists for `MES 06-26`;
- candidate uses the simple quarterly equity index cycle;
- evidence intake records static cash-settled termination/expiration evidence as partial;
- target window `2026-05-18` through `2026-05-22` is before the June 2026 third-Friday expiration.

Rows kept blocked for the next attempt:

```text
ZN, QM, ZC
```

Reasons:

- `ZN` still needs stronger Treasury first-notice/delivery window evidence before it can be used as the first pilot;
- `QM` has possible energy expiration conflict around the target window and should not be the first bar-intake candidate;
- `ZC` needs stronger grain first-notice/delivery evidence and may be more operationally complex than a cash-settled equity index contract.

## Decision

Decision:

```text
NARROW_NEXT_STATIC_SELECTION_ATTEMPT_TO_MES_ONLY_REQUIRE_HASH_BOUND_OFFICIAL_SPEC_EXTRACT
```

The next dated-contract selection attempt should not include all four rows. It should focus only on:

```text
MES 06-26
```

This is not a selection of `MES 06-26` for data intake. It is a process decision to make `MES` the only candidate for the next static evidence-hardening and selection attempt.

## Required Evidence Before Re-Selection

Before any MES dated-contract selection re-execution may mark a row ready, it must have a hash-bound static evidence artifact that locks:

- official active/listed status as of `2026-05-30`;
- official listed contract months proving June 2026 is listed;
- termination/expiration/cash-settlement rule for `MES 06-26`;
- target-window coverage for `2026-05-18` through `2026-05-22`;
- local NinjaTrader static expiry row for `MES 06-26`;
- NinjaTrader local syntax for `MES 06-26`;
- local Trading Hours template hash/evidence for `CME US Index Futures ETH`.

## Still Closed

The following remain closed:

- historical-bar intake;
- NinjaTrader historical export;
- provider API access;
- market-row parsing;
- diagnostics;
- backtests;
- OOS, Lockbox, Forward;
- CFD adapters;
- old QuantLab active-pipeline use;
- tuning;
- deployment;
- trading;
- promotion;
- remote operations.

## Next Clean Gate

Selected next gate:

```text
NINJATRADER_SUPPORTED_PILOT_MES_STATIC_DATED_CONTRACT_LOCK_GATE
```

That gate should create a hash-bound static evidence artifact and selection ledger for `MES 06-26` only. It should either mark `MES 06-26` statically ready for a later tiny historical-bar intake gate or fail closed with exact unresolved evidence atoms.

It must not export historical bars, parse market rows, access provider APIs, run diagnostics, or run backtests.

## Non-Authorization

This redecision authorizes no code edits, no tests, no real market data, no market-row parsing, no NinjaTrader historical export, no provider API access, no diagnostics, no backtests, no returns, no PnL, no Sharpe, no drawdown, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old QuantLab pipeline use, no tuning, no deployment, no trading, no promotion, no remote push, and no GitHub action.
