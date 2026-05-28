# Lane Classification And Adapter Quarantine Rules

Date: 2026-05-28

Status:

```text
PROCESS_ONLY_LANE_CLASSIFICATION_ADAPTER_QUARANTINE_RULES_NOT_PIPELINE_AUTHORIZATION
```

## Required Lane Classification

Before any data work, each lane must declare exactly one:

```text
SOURCE_NATIVE_FUTURES
CFD_DIRECT
CFD_ADAPTER
```

## Source-Native Futures

`SOURCE_NATIVE_FUTURES` means:

- source signal logic is interpreted on the book/source-native futures instrument where possible;
- futures data, sessions, rolls, timestamps, bar semantics, and contract rules must be locked before strategy computation;
- CFD broker sessions, CFD spreads, CFD symbols, and CFD timestamps are not discovery authority.

## CFD Direct

`CFD_DIRECT` means:

- the source hypothesis is directly about a CFD/broker venue;
- broker symbol specs, sessions, spreads, swaps, and fills are primary source fields;
- this class must not be confused with a futures source translated to CFD.

## CFD Adapter

`CFD_ADAPTER` means:

- source-native behavior already exists or is explicitly being compared;
- the adapter asks whether source-native behavior survives target broker translation;
- adapter work requires its own gate memo;
- adapter results may not tune or rescue source-native rules.

## Old Plumbing Quarantine

The following are rejected as default authority:

- old CFD broker-clock assumptions;
- old ICMarkets/The5ers adapter scripts;
- old mixed futures/CFD translation scripts;
- old data-prep scripts not rebuilt under this workspace's rules;
- old TEST/VALIDATION/Lockbox state;
- old contaminated results;
- old pipeline convenience shortcuts.

## Backtest Length Guard

No backtest or diagnostic over 2 years may be run without explicit operator approval.

## Non-Authorization

This rule file authorizes no data access, no export, no parsing, no implementation, no tests/backtests, no strategy computation, no OOS, no Lockbox, no Forward, no deployment, no trading, and no promotion.
