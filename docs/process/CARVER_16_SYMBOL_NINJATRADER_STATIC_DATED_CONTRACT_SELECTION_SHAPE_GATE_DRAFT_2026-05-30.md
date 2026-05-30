# Carver 16-Symbol NinjaTrader Static Dated-Contract Selection Shape Gate Draft

Date: 2026-05-30

Status:

```text
PROCESS_ONLY_CARVER_16_SYMBOL_NINJATRADER_STATIC_DATED_CONTRACT_SELECTION_SHAPE_GATE_DRAFT_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Define the process boundary for selecting explicit dated contracts across the full 16-symbol NinjaTrader-supported daily intake pilot before any batch historical-bar intake can be opened.

This gate follows:

```text
docs/process/CARVER_16_SYMBOL_NINJATRADER_DAILY_INTAKE_PILOT_NEXT_STEP_DECISION_2026-05-30.md
```

It does not select contracts, export NinjaTrader data, parse market rows, run diagnostics, run backtests, compute forecasts, compute positions, or open any trading lane.

## Exact Pilot Row Set

The selection surface is exactly:

```text
ZT, ZF, ZN, MES, MNQ, M2K, MYM, QM, RB, ZC, ZS, ZM, ZL, ZW, HE, LE
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

No other Appendix C row, alias-required row, unavailable row, adjacent symbol, CFD symbol, continuous contract, substitute contract, or reweighted universe may enter this shape.

## Exact As-Of Date

Static contract selection as-of date:

```text
2026-05-30
```

The as-of date is a static evidence cutoff. It is not market data and does not authorize provider availability checks, NinjaTrader historical export, or historical-bar parsing.

## Exact Target Completed Trading-Date Window

Target completed trading-date window:

```text
2026-05-18 through 2026-05-22 inclusive
```

Reason:

- the Opus-audited MES tiny quarantine intake already proved the row-shape/session-alignment mechanics for this fixed window;
- reusing the same window avoids selecting a new window after data visibility;
- five completed trading dates are sufficient for a first 16-symbol row-shape and provenance pilot.

Any future selection or intake artifact must fail closed if it needs a different window.

## Current Blocking State

The existing 16-row static ledgers show:

```text
STATIC_READINESS_FAIL_CLOSED_NOT_READY_FOR_TINY_HISTORICAL_BAR_INTAKE: 16
CONTRACT_IDENTITY_FAIL_CLOSED_NOT_LOCKED: 16
SESSION_ROLL_COMPLETED_BAR_FAIL_CLOSED_NOT_LOCKED: 16
RISK_FX_COST_CARRY_LEG_FAIL_CLOSED_NOT_LOCKED: 16
FAIL_CLOSED_EXPLICIT_DATED_CONTRACT_MONTH_NOT_SELECTED_NO_AS_OF_DATE_OR_TARGET_WINDOW: 16
final_static_readiness_for_tiny_historical_bar_intake NO: 16
```

This shape gate is intended to remove only the explicit dated-contract selection blocker if static evidence supports doing so. It does not by itself make any row ready for batch intake.

## Static Evidence Sources

The future selection execution gate may use only static evidence:

- current Carver Appendix C machine-readable universe lock;
- current Carver NinjaTrader source-native provider mapping ledger;
- current Carver contract identity hardening and static contract specification ledgers;
- current Carver 16-symbol static readiness and static policy ledgers;
- local NinjaTrader static instrument definitions;
- local NinjaTrader static expiry, rollover, month, and instrument metadata where available;
- official exchange or provider static contract specification pages, fact cards, PDFs, or rulebook sections;
- local NinjaTrader Trading Hours template evidence already extracted for the selected rows.

Forbidden evidence:

- NinjaTrader historical export;
- provider API access;
- historical bar availability checks;
- market rows;
- diagnostics;
- backtests;
- returns, PnL, Sharpe, drawdown, or performance evidence;
- observed data continuity or liquidity after the target window is queried.

## Product-Family Selection Rules

The future execution gate must preserve every row and apply family-specific static rules before selecting a dated contract.

### Rates: `ZT`, `ZF`, `ZN`

Required static lock atoms:

- official product identity and product code;
- official listed contract months covering the target window;
- last trade and delivery/last delivery constraints;
- first-notice or delivery-process constraints if applicable;
- local NinjaTrader dated-contract syntax;
- local Trading Hours template and timezone;
- confirmation that the full target window is not inside an unsafe delivery, notice, expiration, or last-trade conflict interval.

Selection rule:

```text
SELECT_NEAREST_LISTED_CONTRACT_THAT_COVERS_FULL_TARGET_WINDOW_AND_HAS_NO_NOTICE_DELIVERY_LAST_TRADE_CONFLICT
```

### Equity Index: `MES`, `MNQ`, `M2K`, `MYM`

Required static lock atoms:

- official product identity and product code;
- official quarterly or otherwise listed contract months covering the target window;
- last trade, expiration, and cash-settlement rule;
- local NinjaTrader dated-contract syntax;
- local Trading Hours template and timezone;
- confirmation that the selected contract remains valid for the full target window.

Selection rule:

```text
SELECT_NEAREST_LISTED_CASH_SETTLED_EQUITY_INDEX_CONTRACT_THAT_COVERS_FULL_TARGET_WINDOW
```

### Energy: `QM`, `RB`

Required static lock atoms:

- official product identity and product code;
- official listed monthly contracts covering the target window;
- last trade, expiration, delivery, and settlement constraints;
- local NinjaTrader dated-contract syntax;
- local Trading Hours template and timezone;
- confirmation that expiration or delivery timing does not fall inside or before the full target window in a way that would make the selected contract unsafe.

Selection rule:

```text
SELECT_NEAREST_LISTED_ENERGY_CONTRACT_WITH_LAST_TRADE_EXPIRATION_DELIVERY_SAFE_AFTER_TARGET_WINDOW
```

If the nearby contract has an expiration or delivery conflict around `2026-05-18` through `2026-05-22`, the row must select the next safe listed contract using static rules or fail closed.

### Grains/Oilseeds: `ZC`, `ZS`, `ZM`, `ZL`, `ZW`

Required static lock atoms:

- official product identity and product code;
- official listed contract months covering the target window;
- first notice, last trade, delivery, and expiration constraints;
- local NinjaTrader dated-contract syntax;
- local Trading Hours template and timezone;
- confirmation that the full target window is before any first-notice or delivery-risk conflict for the selected contract.

Selection rule:

```text
SELECT_NEAREST_LISTED_GRAIN_OR_OILSEED_CONTRACT_WITH_NO_FIRST_NOTICE_DELIVERY_LAST_TRADE_CONFLICT
```

### Livestock: `HE`, `LE`

Required static lock atoms:

- official product identity and product code;
- official listed contract months covering the target window;
- last trade, expiration, delivery or cash-settlement constraints as applicable;
- local NinjaTrader dated-contract syntax;
- local Trading Hours template and timezone;
- confirmation that the full target window is not inside an expiration, delivery, or settlement conflict.

Selection rule:

```text
SELECT_NEAREST_LISTED_LIVESTOCK_CONTRACT_THAT_COVERS_FULL_TARGET_WINDOW_AND_HAS_NO_LIFECYCLE_CONFLICT
```

## Universal Row-Level Selection Requirements

For every one of the 16 rows, the future execution gate must:

1. Preserve the Appendix C row ID, author market code, descriptive name, provider symbol, and local canonical instrument ID.
2. Preserve the 16-row pilot ordering or explicitly record any machine-readable sort key used for the output ledger.
3. Confirm active/listed status from static evidence as of `2026-05-30`.
4. Enumerate official listed contract months that can cover `2026-05-18` through `2026-05-22`.
5. Select one source-native dated contract using the family rule above.
6. Record the local NinjaTrader dated-contract syntax for the selected contract.
7. Confirm that the selected contract's lifecycle constraints are compatible with the full target window.
8. Confirm that the row has a local Trading Hours template and template timezone.
9. Record any unresolved source/provider conflict explicitly.
10. Fail closed if any static atom is missing, ambiguous, conflicting, or non-source-native.

No row may be selected from observed historical-bar availability.

## Machine-Readable Output Expectations

The future execution gate must create a machine-readable dated-contract selection ledger with exactly 16 rows.

Required columns:

```text
row_id
author_market_code
descriptive_name
source_group
lane_class
provider_symbol
local_canonical_instrument_id
product_family_group
as_of_date
target_completed_trading_date_start
target_completed_trading_date_end
official_exchange_venue
official_product_code
official_product_name
official_listed_contract_months_status
official_lifecycle_constraint_status
active_listed_status_as_of_2026_05_30
candidate_source_native_dated_contract
selected_source_native_dated_contract
selected_ninjatrader_local_contract
ninjatrader_local_contract_syntax_status
trading_hours_template
trading_hours_template_status
target_window_coverage_status
dated_contract_selection_status
final_static_dated_contract_selection_result
remaining_blockers
market_row_access_status
provider_api_accessed
ninjatrader_historical_export_used
diagnostics_or_backtests_run
substitution_status
```

Required global checks:

```text
SELECTED_ROWS_EXPECTED: 16
SELECTED_ROWS_PRESERVED: 16
MARKET_ROW_ACCESS_STATUS: NO_MARKET_ROW_ACCESS
PROVIDER_API_ACCESSED: NO
NINJATRADER_HISTORICAL_EXPORT_USED: NO
DIAGNOSTICS_OR_BACKTESTS_RUN: NO
SUBSTITUTION_STATUS: FAIL_CLOSED_NO_DROP_NO_SUBSTITUTE_NO_REWEIGHT
```

## Pass And Fail-Closed Semantics

The future execution gate may mark the dated-contract selection stage passed only if:

```text
STATIC_DATED_CONTRACT_SELECTED_FOR_16_SYMBOL_DAILY_INTAKE: 16
```

If fewer than 16 rows can be selected, the gate must use:

```text
STATIC_DATED_CONTRACT_SELECTION_PARTIAL_FAIL_CLOSED_REDECISION_REQUIRED
```

and open no batch intake shape gate without a separate process-only redecision.

Rows must fail closed on:

- missing active/listed status;
- missing official listed contract months;
- product code or contract variant mismatch;
- local NinjaTrader syntax ambiguity;
- official/local source conflict;
- first-notice, last-trade, expiration, delivery, or cash-settlement ambiguity;
- target-window lifecycle conflict;
- missing or hash-mismatched Trading Hours template evidence;
- need for continuous contract, merge, back-adjustment, substitution, row dropping, or post-data reweighting;
- any need to inspect historical bars to choose the contract.

## Relationship To Later Batch Intake

A later 16-symbol batch intake shape gate may be opened only after this selection stage records:

```text
STATIC_DATED_CONTRACT_SELECTED_FOR_16_SYMBOL_DAILY_INTAKE: 16
```

The later shape gate must then define:

- exact manifest rows and selected dated contracts;
- `1 Day` timeframe;
- `Last` bars;
- the same completed trading-date window;
- quarantine directory layout;
- raw helper-output timestamp policy;
- sanitized OHLCV schema;
- row validation and provenance ledgers;
- all-16 pass/fail policy.

## Next Clean Gate

Selected next gate:

```text
CARVER_16_SYMBOL_NINJATRADER_STATIC_DATED_CONTRACT_EVIDENCE_INTAKE_AND_SELECTION_EXECUTION_GATE
```

That gate should create the 16-row dated-contract selection ledger described above using only static evidence.

## Non-Authorization

This draft authorizes no code edits, no tests, no new data export, no provider API access, no market-row parsing, no NinjaTrader historical export, no diagnostics, no backtests, no forecasts, no positions, no costs, no carry, no trend, no OOS, no Lockbox, no Forward, no CFD adapter work, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no GitHub staging, no commit, no push, no PR update/opening, and no remote operations.
