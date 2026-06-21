# Carver Source-Native Continuous/Roll Daily Data Semantics Shape Gate

Date: 2026-05-30

Status:

```text
PROCESS_ONLY_CARVER_SOURCE_NATIVE_CONTINUOUS_ROLL_DAILY_DATA_SEMANTICS_SHAPE_GATE_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Define the source-native continuous/roll daily futures semantics required before any broad Carver strategy machinery may treat the daily data library as historical strategy input.

This gate is process-only. It does not select a final roll rule, create a continuous series, request provider data, parse market rows, compute returns, or run strategy logic.

## Governing Decision

Decision record:

```text
docs/process/CARVER_16_SYMBOL_DAILY_LIBRARY_DEV_RECON_OR_CONTINUOUS_ROLL_DECISION_GATE_2026-05-30.md
```

Required follow-up before broad strategy machinery:

```text
CARVER_SOURCE_NATIVE_CONTINUOUS_ROLL_SEMANTICS_SHAPE_GATE
```

Reason:

```text
DATED_CONTRACT_FRAGMENT_ROWS_ARE_NOT_GENERAL_CARVER_STRATEGY_INPUT
```

## Lane

```text
SOURCE_NATIVE_FUTURES
```

This gate rejects CFD sessions, CFD symbols, CFD broker clocks, CFD spread assumptions, old QuantLab active-pipeline state, and adapter shortcuts.

## Current State

Available foundation artifacts:

```text
16 dated-contract manifest rows
4568 Databento dated-contract archive rows
4483 normal provider-condition candidate rows
85 degraded provider-condition rows quarantined
0 blocked/unresolved provider-condition rows
non-strategy schema/date join smoke test passed
```

Current blocked interpretation:

```text
GENERAL_STRATEGY_INPUT: BLOCKED
CONTINUOUS_OR_ROLLED_DAILY_SERIES: NOT_DEFINED
ROLL_RULE: NOT_DEFINED
BACK_ADJUSTMENT_POLICY: NOT_DEFINED
SETTLEMENT_CLOSE_POLICY: NOT_DEFINED
CARRY_LEG_POLICY: NOT_DEFINED
STRATEGY_COMPUTATION: CLOSED
```

## Semantics To Resolve

Before any strategy-facing Development/Reconciliation table can be interpreted as Carver daily futures input, a later evidence/execution path must resolve or fail-close:

```text
source-native series identity
front-contract definition
next-contract definition
roll trigger rule
roll date source
first-notice / last-trade / expiration blocker policy
cash-settled versus physically delivered handling
settlement versus close field policy
volume/open-interest use policy if roll requires it
back-adjustment policy
non-adjusted splice policy if no back-adjustment is used
raw dated-contract lineage for every continuous row
completed trading-date authority
UTC timestamp preservation and interpretation
provider-condition gap handling
holiday/session alignment
duplicate/missing row behavior
symbol and instrument-id lineage
hash lineage from continuous row to source rows
```

## Acceptable Future Source Evidence

A future semantics execution gate may use only explicitly authorized static/source evidence and already quarantined rows unless separately authorized.

Potential evidence classes to shape before execution:

```text
Carver source passages for price series and futures roll expectations
Databento instrument definitions and metadata
Databento continuous-contract documentation if used as reference
exchange contract specifications and lifecycle rules
static settlement/close field documentation
existing dated-contract quarantine archive
existing provider-condition metadata ledger
```

Any provider API access, new market-data request, or new data download requires a separate execution gate.

## Continuous Series Policy Questions

A later decision must explicitly answer:

- Is Carver strategy research using provider-built continuous symbols, locally built continuous symbols, or both?
- If provider-built continuous symbols are inspected, are they source authority or reference-only?
- Does the strategy input use back-adjusted prices, ratio-adjusted prices, Panama adjustment, unadjusted splices, or a different policy?
- What is the exact roll trigger: days before expiry, days before first notice, volume switch, open-interest switch, calendar rule, or source-specific rule?
- What is the fail-closed behavior when volume/open-interest or lifecycle metadata is unavailable?
- How are degraded provider-condition dates handled in continuous rows?
- How is the raw dated-contract lineage preserved for each continuous row?
- Does the policy differ by asset family, contract family, cash settlement, or physical delivery?

## Required Future Output Shape

A future continuous/roll semantics execution gate, if authorized, must produce at minimum:

```text
continuous_roll_policy_record.md
continuous_roll_contract_lineage_ledger.csv
continuous_roll_gap_and_condition_policy.csv
continuous_roll_status.csv
continuous_roll_sha256sums.txt
```

Minimum policy fields:

```text
book_symbol
provider
dataset
series_identity
front_contract_policy
next_contract_policy
roll_trigger_policy
roll_date_source
first_notice_policy
last_trade_policy
expiration_policy
settlement_close_policy
adjustment_policy
provider_condition_policy
completed_trading_date_policy
timestamp_policy
lineage_requirement
fail_closed_rule
strategy_use_status
```

Minimum lineage fields for any later continuous row:

```text
book_symbol
continuous_row_date
continuous_timestamp_utc
selected_source_contract
source_provider_symbol
source_instrument_id
source_completed_trading_date
source_open
source_high
source_low
source_close
source_volume
adjustment_factor_or_offset
provider_condition_readiness_status
source_archive_sha256
lineage_policy_status
```

## Required Validation Before Strategy-Facing Use

Any later source-native daily strategy input must prove:

- no dated-contract fragment row is silently treated as continuous history;
- every continuous row has raw dated-contract lineage;
- roll dates are deterministic and reproducible;
- lifecycle blockers are applied before roll selection;
- degraded provider-condition rows are excluded, blocked, or explicitly policy-labeled;
- completed trading dates are monotonic per symbol;
- no duplicate strategy date exists per symbol;
- missing dates are policy-labeled and never silently filled;
- timestamp semantics are explicit;
- settlement/close semantics are explicit;
- no strategy computation is bundled into data construction.

## Closed Until Separate Authorization

The following remain closed:

```text
provider API access
new market-data requests
continuous-contract downloads
dated-contract expansion
market-row parsing
continuous-series construction
strategy-facing table execution
returns
diagnostics
backtests
forecasts
positions
costs
carry
trend
volatility or risk calculations
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

## Audit Requirements

Lean hostile audit is automatic for this shape gate and any future execution artifact.

Opus or GPT Extended Pro audit is recommended before a continuous/rolled series is admitted as broad multi-strategy or portfolio Development/Reconciliation input, because this gate is the semantic bridge between raw market data and book-strategy interpretation.

## Next Clean Gate

Recommended next concrete gate:

```text
CARVER_16_SYMBOL_DATED_CONTRACT_FRAGMENT_DEV_RECON_TABLE_EXECUTION_GATE
```

Allowed purpose if opened:

```text
CREATE_PLUMBING_ONLY_TABLE_FROM_EXISTING_4483_NORMAL_PROVIDER_CONDITION_ROWS
```

Required parallel future gate before strategy machinery:

```text
CARVER_SOURCE_NATIVE_CONTINUOUS_ROLL_DAILY_DATA_SEMANTICS_EVIDENCE_PACKET
```

## Non-Authorization

This shape gate authorizes no provider API access, no new market-data request, no data download, no market-row parsing, no continuous-series construction, no table execution, no diagnostics, no backtests, no forecasts, no positions, no costs, no carry, no trend, no volatility/risk calculations, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.
