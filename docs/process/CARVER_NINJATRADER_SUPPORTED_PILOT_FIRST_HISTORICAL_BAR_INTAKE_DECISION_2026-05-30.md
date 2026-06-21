# Carver NinjaTrader-Supported Pilot First Historical-Bar Intake Decision

Date: 2026-05-30

Status:

```text
PROCESS_ONLY_CARVER_NINJATRADER_SUPPORTED_PILOT_FIRST_HISTORICAL_BAR_INTAKE_DECISION_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Decide whether the selected 16-row NinjaTrader-supported pilot universe can proceed to a tiny first historical-bar intake pilot, should be reduced, or must remain blocked.

Selected 16-row pilot:

```text
ZT, ZF, ZN, MES, MNQ, M2K, MYM, QM, RB, ZC, ZS, ZM, ZL, ZW, HE, LE
```

This is a process-only decision artifact. It does not authorize real market data, NinjaTrader historical export, provider API access, market-row parsing, diagnostics, backtests, trading, deployment, or promotion.

## Inputs

Current readiness artifacts:

```text
docs/process/CARVER_NINJATRADER_SUPPORTED_PILOT_STATIC_POLICY_READINESS_REFRESH_2026-05-30.md
docs/researchops/first_data_intake/CARVER_NINJATRADER_SUPPORTED_PILOT_STATIC_POLICY_READINESS_REFRESH_2026-05-30.csv
docs/process/CARVER_NINJATRADER_SUPPORTED_PILOT_EXPLICIT_CONTRACT_MONTH_CONTRACT_IDENTITY_FINAL_STATIC_LOCK_2026-05-30.md
docs/researchops/first_data_intake/CARVER_NINJATRADER_SUPPORTED_PILOT_EXPLICIT_CONTRACT_MONTH_CONTRACT_IDENTITY_FINAL_STATIC_LOCK_2026-05-30.csv
```

No market rows, historical bars, NinjaTrader exports, provider APIs, diagnostics, or backtests were used.

## Current Evidence

The 16-row pilot has useful static scaffolding:

```text
VENUE_NORMALIZATION_LOCKED: 16
CURRENCY_NORMALIZATION_LOCKED: 16
MULTIPLIER_OR_QUOTE_UNIT_SEMANTICS_LOCKED: 16
POINT_TICK_RECONCILIATION_LOCKED: 16
CONTRACT_FAMILY_VARIANT_LOCKED: 16
LOCAL_CANONICAL_ID_PRESENT: 16
```

But it is not ready for historical-bar intake:

```text
STATIC_POLICY_READY_FOR_TINY_HISTORICAL_BAR_INTAKE: 0
FINAL_STATIC_READY_FOR_TINY_HISTORICAL_BAR_INTAKE: 0
FINAL_STATIC_CONTRACT_IDENTITY_FAIL_CLOSED_NOT_READY_FOR_TINY_HISTORICAL_BAR_INTAKE: 16
```

Blocking facts:

- explicit dated contract month selected: `0`;
- active/listed status locked: `0`;
- delivery cycle fully locked: `1`;
- no row has an authorized as-of date or target historical-bar intake window;
- no row has a row-level dated contract selection rule applied;
- no row has authorization for NinjaTrader historical export or market-row parsing.

## Decision

Decision:

```text
KEEP_16_ROW_PILOT_BLOCKED_FOR_IMMEDIATE_HISTORICAL_BAR_INTAKE
```

The 16-row pilot is not reduced in this artifact, and no tiny historical-bar intake pilot is opened here.

Reason:

- reducing the row set would not solve the common blocker: no explicit dated contract month has been selected;
- defining exact dated contracts without an as-of date, target date window, and static contract selection evidence would smuggle an intake assumption;
- opening historical-bar intake while all 16 rows are explicitly marked not ready would contradict the current static ledgers.

## Pilot Shape Preserved

The selected pilot universe remains the correct working candidate set:

```text
ZT, ZF, ZN, MES, MNQ, M2K, MYM, QM, RB, ZC, ZS, ZM, ZL, ZW, HE, LE
```

Preserving the 16-row shape is useful because it contains rates, equity index, energy, grains/oilseeds, and livestock futures that are locally represented in NinjaTrader static evidence. Preservation does not imply data readiness.

## Not Authorized

This decision does not authorize:

- choosing historical rows;
- selecting a date range from observed availability;
- exporting from NinjaTrader;
- parsing market rows;
- resolving missing rows after seeing data;
- reducing the universe after seeing data;
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
NINJATRADER_SUPPORTED_PILOT_STATIC_DATED_CONTRACT_SELECTION_SHAPE_GATE
```

That gate should define, before any market-row access:

- exact as-of date for contract-month selection;
- exact target historical-bar intake window;
- static evidence source for active/listed status and contract availability;
- dated contract selection rule;
- row-level fail-closed behavior if the dated contract cannot be selected;
- whether the first future intake should use all 16 symbols or a smaller row set;
- completed-bar parser boundary for a later intake gate.

No historical-bar export or parsing should occur until a later gate records at least one row:

```text
STATIC_READY_FOR_TINY_HISTORICAL_BAR_INTAKE
```

## Non-Authorization

This decision authorizes no code edits, no tests, no real market data, no market-row parsing, no NinjaTrader historical export, no provider API access, no diagnostics, no backtests, no returns, no PnL, no Sharpe, no drawdown, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old QuantLab pipeline use, no tuning, no deployment, no trading, no promotion, no remote push, and no GitHub action.
