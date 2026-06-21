# Carver Source-Native Continuous/Roll Daily Data Policy Decision

Date: 2026-05-30

Status:

```text
PROCESS_POLICY_CARVER_SOURCE_NATIVE_CONTINUOUS_ROLL_DAILY_DATA_DECISION_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Record the source-native continuous/roll daily data policy decision after Gate 1 dated-contract fragment plumbing and Gate 2 static continuous/roll evidence execution.

This decision chooses the next architecture for Carver daily futures data. It does not construct continuous series, create strategy input, request provider data, parse market rows, run diagnostics, run backtests, compute forecasts, compute positions, compute costs, compute carry, compute trend, compute volatility or risk, access OOS/Lockbox/Forward, deploy, trade, promote, stage Git changes, commit, push, update a PR, or perform remote operations.

## Lane

```text
SOURCE_NATIVE_FUTURES
```

Old QuantLab remains:

```text
C:\Users\openclaw\Desktop\QuantLab_v3 = ARCHIVED_OPERATIONAL_BLOB_DO_NOT_PIPELINE
```

No CFD assumptions, CFD adapters, broker-clock assumptions, or old pipeline state may enter this policy.

## Evidence Basis

Gate 1:

```text
docs/researchops/source_native_futures_daily_data_library/16_SYMBOL_DATED_CONTRACT_FRAGMENT_DEV_RECON_TABLE/2026-05-30/CARVER_16_SYMBOL_DATED_CONTRACT_FRAGMENT_DEV_RECON_TABLE_2026-05-30.csv
docs/process/CARVER_16_SYMBOL_DATED_CONTRACT_FRAGMENT_DEV_RECON_TABLE_EXECUTION_LEAN_HOSTILE_AUDIT_RESULT_2026-05-30.md
```

Gate 1 proved:

```text
4483 normal provider-condition dated-contract rows admitted for plumbing only
85 degraded provider-condition rows excluded
16 manifest symbols preserved
0 non-manifest rows
0 continuous-contract rows
0 duplicate provider-symbol/completed-date rows
NOT_STRATEGY_INPUT_NOT_BACKTEST_READY labels preserved
```

Gate 2:

```text
docs/researchops/source_native_futures_daily_data_library/continuous_roll_semantics_evidence/2026-05-30/CARVER_SOURCE_NATIVE_CONTINUOUS_ROLL_EVIDENCE_SOURCE_INDEX_2026-05-30.md
docs/researchops/source_native_futures_daily_data_library/continuous_roll_semantics_evidence/2026-05-30/CARVER_16_SYMBOL_CONTINUOUS_ROLL_EVIDENCE_REQUIREMENTS_2026-05-30.csv
docs/researchops/source_native_futures_daily_data_library/continuous_roll_semantics_evidence/2026-05-30/CARVER_16_SYMBOL_CONTINUOUS_ROLL_PROVIDER_CAPABILITY_STATUS_2026-05-30.csv
docs/researchops/source_native_futures_daily_data_library/continuous_roll_semantics_evidence/2026-05-30/CARVER_16_SYMBOL_CONTINUOUS_ROLL_LIFECYCLE_EVIDENCE_NEEDS_2026-05-30.csv
docs/process/CARVER_SOURCE_NATIVE_CONTINUOUS_ROLL_DAILY_DATA_SEMANTICS_EVIDENCE_EXECUTION_LEAN_HOSTILE_AUDIT_RESULT_2026-05-30.md
```

Gate 2 proved:

```text
Databento continuous symbology and roll-rule documentation exists
Databento continuous prices are documented as original/unadjusted, not local Carver back-adjusted source authority
Databento OHLCV-1d is trade-bar evidence, not locked official settlement authority
provider condition metadata is a usable policy input
definition/lifecycle evidence is partial and product-family-specific
continuous row lineage remains unresolved
all 16 symbols remain BLOCKED_PENDING_CONTINUOUS_ROLL_POLICY
```

## Policy Decision

### Provider-Built Continuous Series

Decision:

```text
PROVIDER_BUILT_CONTINUOUS_SERIES_POLICY = REFERENCE_ONLY_UNTIL_SOURCE_AND_LINEAGE_AUDITED
```

Meaning:

Databento provider-built continuous symbols may be inspected later as reference documentation or a comparison surface only if separately authorized. They are not source authority for Carver strategy input in the current foundation.

Reason:

The static evidence indicates provider continuous rows are original/unadjusted and smart-symbol mapped, not a Carver-locked back-adjusted excess-return series with local row lineage, provider-condition labels, and hash-bound source rows.

### Strategy Series Construction Method

Decision:

```text
STRATEGY_SERIES_METHOD = LOCAL_CONTINUOUS_FROM_DATED_DATABENTO_CONTRACTS
```

Meaning:

The preferred Carver source-native path is to construct any later Development/Reconciliation continuous daily series locally from explicit dated Databento contracts, preserving raw row lineage.

Required lineage for any later continuous row:

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
roll_policy_status
lineage_policy_status
```

No continuous row may be admitted without explicit dated-contract source lineage.

### Development/Reconciliation Boundary

Decision:

```text
INITIAL_USE = DEVELOPMENT_RECONCILIATION_ONLY
```

Meaning:

Any later locally constructed continuous series, if authorized and passed, may be used only as Development/Reconciliation input. It is not TEST, VALIDATION, OOS, Lockbox, Forward, promotion, deployment, or trading evidence.

### Daily Price Field

Decision:

```text
PRICE_FIELD_POLICY = DATABENTO_OHLCV_1D_CLOSE_NOT_OFFICIAL_SETTLEMENT
```

Meaning:

For the first local continuous lineage gate, Databento `ohlcv-1d` close may be used as the daily close field for Development/Reconciliation plumbing and trend-style research only, with explicit labeling:

```text
DAILY_CLOSE_FIELD = TRADE_BAR_CLOSE_NOT_OFFICIAL_SETTLEMENT
SETTLEMENT_POLICY = BLOCKED_PENDING_OFFICIAL_SETTLEMENT_SOURCE_GATE
```

This does not solve official settlement, settlement statistics, or product-family official close/settlement publication policy.

### Adjustment Policy

Decision:

```text
ADJUSTMENT_POLICY = LOCAL_BACK_ADJUSTED_EXCESS_RETURN_SERIES_REQUIRED_FOR_TREND_STYLE_CONTINUOUS_INPUT
```

Meaning:

Carver trend-style continuous daily input should be locally back-adjusted from dated-contract rows if a later gate authorizes construction. Provider-built unadjusted continuous prices do not satisfy this policy as strategy input.

The exact adjustment arithmetic, roll trigger, adjustment direction, roll-date handling, and negative adjusted price labels must be specified in a later local continuous lineage gate before any construction occurs.

### Roll Trigger Policy

Decision:

```text
ROLL_TRIGGER_POLICY = DETERMINISTIC_LIFECYCLE_SAFE_RULE_REQUIRED_BEFORE_CONSTRUCTION
```

Current preferred shape for the next gate:

```text
avoid volume/open-interest roll until volume/open-interest evidence is separately authorized and validated
use product-family lifecycle blockers before selecting roll dates
roll physical-delivery products before first-notice / delivery-window / last-trade blockers
roll cash-settled equity-index products before expiration/final-settlement blockers
record every selected roll date and source contract transition in a lineage ledger
```

No final roll rule is selected by this policy decision. The next gate must define the exact deterministic rule.

### Provider Condition Policy

Decision:

```text
PROVIDER_CONDITION_POLICY = NORMAL_ROWS_ONLY_FOR_INITIAL_LOCAL_CONTINUOUS_LINEAGE_GATE
```

Meaning:

Rows with degraded provider-condition metadata remain excluded or explicitly quarantined. They must not be repaired, interpolated, filled, substituted, silently dropped, or silently admitted into continuous strategy rows.

### Carry Policy

Decision:

```text
CARRY_POLICY = BLOCKED_PENDING_RAW_DATED_CONTRACT_CURVE_LEG_POLICY
```

Meaning:

This policy supports only the architecture needed to attempt trend-style continuous daily input later. It does not open carry, combined trend/carry, curve-leg construction, expiry-distance annualization, raw held/comparison contract selection, seasonal/wrong-sign handling, carry costs, or carry portfolio work.

### Strategy Readiness

Decision:

```text
STRATEGY_READINESS = NOT_READY_UNTIL_LOCAL_CONTINUOUS_LINEAGE_GATE_PASSES
```

Meaning:

The daily data foundation is not yet strategy-facing. A later gate must create and audit local continuous rows, lineage, roll status, source hashes, and fail-closed counts before any strategy-facing input can be considered.

## Rejected Alternatives

### Provider-Built Continuous As Immediate Source Authority

Rejected:

```text
PROVIDER_BUILT_CONTINUOUS_SERIES_AS_SOURCE_AUTHORITY_NOW = NO
```

Reason:

Provider continuous rows are not currently hash-bound to the local dated-contract archive, not locally back-adjusted, and not proven against Carver-specific roll/back-adjustment semantics.

### Dated-Contract Fragment Rows As General Strategy Input

Rejected:

```text
DATED_CONTRACT_FRAGMENT_ROWS_AS_GENERAL_STRATEGY_INPUT = NO
```

Reason:

Gate 1 output is plumbing-only and explicitly labeled `NOT_STRATEGY_INPUT_NOT_BACKTEST_READY`.

### Official Settlement Solved By OHLCV-1d

Rejected:

```text
OHLCV_1D_CLOSE_EQUALS_OFFICIAL_SETTLEMENT = NO
```

Reason:

Gate 2 evidence separates trade-bar OHLCV from official settlement/statistics or product-family official settlement sources.

### Carry Opened By Continuous Trend Policy

Rejected:

```text
CARRY_READY_FROM_CONTINUOUS_POLICY = NO
```

Reason:

Carry requires raw dated-contract held/comparison prices, curve-leg availability, and expiry-distance evidence. None is opened by this policy.

## Required Next Gate

Next gate:

```text
CARVER_16_SYMBOL_LOCAL_CONTINUOUS_DAILY_LINEAGE_SHAPE_GATE
```

Purpose:

Define the exact local continuous construction shape before any continuous rows are built.

Minimum next-gate requirements:

```text
16-symbol row scope or narrower fail-closed subset
source dated-contract archive inputs and hashes
normal-provider-condition-only admission rule
exact deterministic roll trigger rule by product family
first-notice / last-trade / expiration / delivery / cash-settlement blockers
trade-bar close versus settlement label
local back-adjustment method
adjustment factor or offset ledger schema
raw dated-contract source-lineage ledger schema
duplicate/missing/stale/degraded row fail-closed policy
no continuous provider substitution
no carry curve-leg work
Development/Reconciliation-only strategy-use status
automatic lean hostile audit
```

That shape gate must still not build the series. A later execution gate would be required for local continuous construction.

## Current Goal State

The current daily data foundation goal remains:

```text
NOT_COMPLETE
```

Reason:

Gate 1 and Gate 2 have executed and passed hostile audits, and this policy decision now selects the local continuous construction architecture. However, no local continuous lineage shape gate, no local continuous construction execution, and no strategy-facing input gate have been executed.

## Non-Authorization

This policy decision authorizes no provider API access, provider login, provider account portal use, new market-data request, data download, market-row parsing, continuous-contract download, continuous-series construction, strategy input creation, diagnostics, backtests, forecasts, positions, costs, carry, trend, volatility or risk calculations, OOS, Lockbox, Forward, CFD adapter execution, old QuantLab active-pipeline use, tuning, deployment, trading, promotion, Git staging, commit, push, PR update/opening, or remote operations.
