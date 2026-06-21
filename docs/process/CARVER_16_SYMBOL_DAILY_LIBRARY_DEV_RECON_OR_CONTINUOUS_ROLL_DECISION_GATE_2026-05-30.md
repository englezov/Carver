# Carver 16-Symbol Daily Library Development/Reconciliation Or Continuous/Roll Decision Gate

Date: 2026-05-30

Status:

```text
PROCESS_ONLY_CARVER_16_SYMBOL_DAILY_LIBRARY_DEV_RECON_OR_CONTINUOUS_ROLL_DECISION_GATE_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Decide the next clean gate after the local hostile readiness review of the 16-symbol daily data library.

This decision determines whether to create a Development/Reconciliation table now, or first shape continuous/roll semantics.

## Inputs

Local hostile review:

```text
docs/process/CARVER_16_SYMBOL_DAILY_LIBRARY_LOCAL_HOSTILE_READINESS_REVIEW_2026-05-30.md
```

Current smoke-test pass:

```text
docs/process/CARVER_16_SYMBOL_DAILY_DATA_LIBRARY_NON_STRATEGY_SMOKE_TEST_EXECUTION_PASS_2026-05-30.md
```

Canonical manifest:

```text
docs/researchops/source_native_futures_daily_data_library/16_SYMBOL_DAILY_LIBRARY_PROMOTION_READINESS/manifest/CARVER_16_SYMBOL_DATABENTO_DAILY_LIBRARY_CANONICAL_MANIFEST_2026-05-30.csv
```

## Options Considered

### Option A: Create a dated-contract-only Development/Reconciliation table immediately

Disposition:

```text
SELECTED_WITH_RESTRICTIONS
```

Allowed purpose:

```text
PLUMBING_ONLY_TABLE_FOR_SCHEMA_LOADING_DATE_JOIN_HASH_LINEAGE_AND_EXCLUSION_MECHANICS
```

Restrictions:

- must be labeled `DATED_CONTRACT_FRAGMENT_TABLE_FOR_PLUMBING_ONLY`;
- must include only the 4,483 normal provider-condition rows;
- must exclude all 85 degraded rows;
- must preserve provider symbol, instrument ID, dated contract, timestamp, completed trading date, source hashes, and provider-condition policy;
- must not compute returns, forecasts, positions, costs, carry, trend, volatility/risk, diagnostics, or backtests;
- must not be used as general Carver strategy input.

Reason:

The non-strategy smoke test proved the plumbing surface. A restricted table is useful for testing loaders and future table contracts without pretending continuous-series semantics are solved.

### Option B: Block all table creation until continuous/roll semantics exist

Disposition:

```text
NOT_SELECTED
```

Reason:

This would be safe but unnecessarily slow. The current artifacts are strong enough to support a plumbing-only table, provided it is labeled and fenced.

### Option C: Create two-track plan

Disposition:

```text
SELECTED
```

Tracks:

```text
TRACK_1: DATED_CONTRACT_FRAGMENT_DEV_RECON_TABLE_FOR_PLUMBING_ONLY
TRACK_2: CONTINUOUS_ROLL_SEMANTICS_SHAPE_GATE_BEFORE_GENERAL_STRATEGY_INPUT
```

Reason:

This preserves momentum while preventing semantic overreach.

## Decision

Selected next gate:

```text
CARVER_16_SYMBOL_DATED_CONTRACT_FRAGMENT_DEV_RECON_TABLE_SHAPE_GATE
```

Required scope:

- create shape only, not execution, unless separately authorized;
- define a table from existing archive rows only;
- include only normal provider-condition rows;
- exclude degraded rows;
- preserve hash lineage;
- label as plumbing-only;
- forbid strategy interpretation.

Parallel required follow-up chapter:

```text
CARVER_SOURCE_NATIVE_CONTINUOUS_ROLL_SEMANTICS_SHAPE_GATE
```

This must be completed before any broad Carver strategy machinery treats the 16-symbol library as a historical strategy input.

## Explicit Blocks

The following remain blocked:

```text
general strategy-facing input
continuous contracts
rolled/stiched futures series
returns
diagnostics
backtests
forecasts
positions
costs
carry
trend
volatility/risk calculations
OOS
Lockbox
Forward
CFD adapters
old QuantLab active-pipeline use
tuning
deployment
trading
promotion
Git staging
commit
push
PR update/opening
remote operations
```

## Recommended Next Broad Goal

Recommended broad goal:

```text
Build the Carver source-native daily data foundation for first strategy machinery.
```

First concrete step under that broad goal:

```text
CARVER_16_SYMBOL_DATED_CONTRACT_FRAGMENT_DEV_RECON_TABLE_SHAPE_GATE
```

Second required step before real strategy machinery:

```text
CARVER_SOURCE_NATIVE_CONTINUOUS_ROLL_SEMANTICS_SHAPE_GATE
```

## Non-Authorization

This decision authorizes no provider API access, no new market-data request, no new data download, no raw or sanitized archive modification, no strategy-facing table creation, no returns, no diagnostics, no backtests, no forecasts, no positions, no costs, no carry, no trend, no volatility/risk calculations, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.
