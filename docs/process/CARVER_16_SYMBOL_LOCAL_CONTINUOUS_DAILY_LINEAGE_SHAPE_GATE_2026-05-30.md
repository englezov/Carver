# Carver 16-Symbol Local Continuous Daily Lineage Shape Gate

Date: 2026-05-30

Status:

```text
PROCESS_ONLY_CARVER_16_SYMBOL_LOCAL_CONTINUOUS_DAILY_LINEAGE_SHAPE_GATE_NOT_CONSTRUCTION_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Define the exact shape for a later local continuous daily lineage execution gate after the Carver source-native continuous/roll daily data policy decision.

This shape gate does not construct continuous series, parse market rows, request provider data, download data, create strategy input, run diagnostics, run backtests, compute forecasts, compute positions, compute costs, compute carry, compute trend, compute volatility or risk, access OOS/Lockbox/Forward, deploy, trade, promote, stage Git changes, commit, push, update a PR, or perform remote operations.

## Lane

```text
SOURCE_NATIVE_FUTURES
```

Old workspace remains:

```text
C:\Users\openclaw\Desktop\QuantLab_v3 = ARCHIVED_OPERATIONAL_BLOB_DO_NOT_PIPELINE
```

No CFD sessions, CFD symbols, broker clocks, old adapters, old data-prep scripts, or old active-pipeline state may be used.

## Governing Policy

Policy decision:

```text
docs/process/CARVER_SOURCE_NATIVE_CONTINUOUS_ROLL_DAILY_DATA_POLICY_DECISION_2026-05-30.md
```

Locked policy atoms:

```text
PROVIDER_BUILT_CONTINUOUS_SERIES_POLICY = REFERENCE_ONLY_UNTIL_SOURCE_AND_LINEAGE_AUDITED
STRATEGY_SERIES_METHOD = LOCAL_CONTINUOUS_FROM_DATED_DATABENTO_CONTRACTS
INITIAL_USE = DEVELOPMENT_RECONCILIATION_ONLY
PRICE_FIELD_POLICY = DATABENTO_OHLCV_1D_CLOSE_NOT_OFFICIAL_SETTLEMENT
ADJUSTMENT_POLICY = LOCAL_BACK_ADJUSTED_EXCESS_RETURN_SERIES_REQUIRED_FOR_TREND_STYLE_CONTINUOUS_INPUT
ROLL_TRIGGER_POLICY = DETERMINISTIC_LIFECYCLE_SAFE_RULE_REQUIRED_BEFORE_CONSTRUCTION
PROVIDER_CONDITION_POLICY = NORMAL_ROWS_ONLY_FOR_INITIAL_LOCAL_CONTINUOUS_LINEAGE_GATE
CARRY_POLICY = BLOCKED_PENDING_RAW_DATED_CONTRACT_CURVE_LEG_POLICY
STRATEGY_READINESS = NOT_READY_UNTIL_LOCAL_CONTINUOUS_LINEAGE_GATE_PASSES
```

Policy audit:

```text
docs/process/CARVER_SOURCE_NATIVE_CONTINUOUS_ROLL_DAILY_DATA_POLICY_DECISION_LEAN_HOSTILE_AUDIT_RESULT_2026-05-30.md
BLOCKING_FINDINGS: NO
AUDIT_DISPOSITION: PASS_CARVER_SOURCE_NATIVE_CONTINUOUS_ROLL_DAILY_DATA_POLICY_DECISION_SOURCE_FAITHFUL_REFERENCE_ONLY_LOCAL_LINEAGE_GATE_REQUIRED_SCOPE
```

## Row Scope

Initial row scope:

```text
16 locked pilot symbols
```

Locked symbol manifest:

```text
docs/researchops/source_native_futures_daily_data_library/16_SYMBOL_DAILY_LIBRARY_PROMOTION_READINESS/manifest/CARVER_16_SYMBOL_DATABENTO_DAILY_LIBRARY_CANONICAL_MANIFEST_2026-05-30.csv
SHA256: 0D1F86071A536227BB120163E8166BA13DE7F4C47345AE3CA1DF99F1B3DF0E88
```

Current locked dated contracts:

| Book symbol | Product family | Current source-native dated contract | Databento raw symbol | Instrument ID | Lifecycle class |
|---|---|---|---|---:|---|
| ZT | Treasury rates | ZT_JUN_2026 | ZTM6 | 42370722 | physical delivery |
| ZF | Treasury rates | ZF_JUN_2026 | ZFM6 | 42156042 | physical delivery |
| ZN | Treasury rates | ZN_JUN_2026 | ZNM6 | 42000661 | physical delivery |
| MES | Equity index | MES_JUN_2026 | MESM6 | 42005163 | cash settled |
| MNQ | Equity index | MNQ_JUN_2026 | MNQM6 | 42004936 | cash settled |
| M2K | Equity index | M2K_JUN_2026 | M2KM6 | 42002073 | cash settled |
| MYM | Equity index | MYM_JUN_2026 | MYMM6 | 42002662 | cash settled |
| QM | Energy | QM_JUL_2026 | QMN6 | 3159 | cash settled |
| RB | Energy | RB_JUL_2026 | RBN6 | 781272 | physical delivery |
| ZC | Agriculture grains/oilseeds | ZC_JUL_2026 | ZCN6 | 495552 | physical delivery |
| ZS | Agriculture grains/oilseeds | ZS_JUL_2026 | ZSN6 | 194904 | physical delivery |
| ZM | Agriculture grains/oilseeds | ZM_JUL_2026 | ZMN6 | 748931 | physical delivery |
| ZL | Agriculture grains/oilseeds | ZL_JUL_2026 | ZLN6 | 608206 | physical delivery |
| ZW | Agriculture grains/oilseeds | ZW_JUL_2026 | ZWN6 | 4121243 | physical delivery |
| HE | Livestock | HE_JUN_2026 | HEM6 | 42005488 | cash settled |
| LE | Livestock | LE_JUN_2026 | LEM6 | 42290645 | physical delivery |

The future execution gate may reduce the row set only by explicit fail-closed row status. It may not silently drop, substitute, bridge micro/full/mini contracts, reweight, or use provider-built continuous symbols as replacements.

## Required Input Artifacts For Future Execution

A future local continuous lineage execution gate must hash-check and use only:

```text
canonical 16-symbol manifest
Gate 1 dated-contract fragment table
Gate 1 status/provenance/SHA artifacts
Gate 2 continuous/roll evidence ledgers
policy decision artifact
this shape gate
```

Minimum required hash inputs already known:

| Input | SHA256 |
|---|---|
| Canonical 16-symbol manifest | `0D1F86071A536227BB120163E8166BA13DE7F4C47345AE3CA1DF99F1B3DF0E88` |
| Gate 1 fragment table | `C18C1956A75B161B86132D3CCC43ADAED4D3D7950002DB7BD0E01D50AA5C5AC9` |
| Gate 1 status CSV | `A81DA21AF8E6925478C6D7C2CFDC0119B56765AB4E82FB51C2294BBC8E0C6BB0` |
| Gate 1 provenance MD | `8D43EC12F2FF244481B7A9EB5302F36A5D4AD9D99B5A0BCBBCFFAC8BC65E6066` |
| Gate 2 source index | `F1F0F37D93C1B40957F2AA683C975ADCA1DCD041E12D27C98A28227EED94399A` |
| Gate 2 evidence requirements | `91764D3CBA3FA78BB1AF8DDB7D3207A33F1C154ECA1DF4611F623EBF4801CCF8` |
| Gate 2 provider capability status | `CFA374099B03AAEDDAD4C25AB257347C42DEFA14E928D857B64907FA73AA457F` |
| Gate 2 lifecycle evidence needs | `C36181673C9E79B0B322DDF885B32F1A5EC31DDFA7DCA99E7DFF224F6BD19BF6` |

The future execution must fail closed if any required hash differs from the locked value or if the source artifact is missing.

## Admission Rule For Future Construction

Future continuous-row source rows may be admitted only when all are true:

```text
book_symbol is one of the locked 16
source row comes from the Gate 1 fragment table or a separately authorized dated-contract expansion
source_contract_identity is EXPLICIT_DATED_CONTRACT
row_policy_status is NORMAL_PROVIDER_CONDITION_ROW_ONLY
provider_condition_readiness_status is ROW_READY_PROVIDER_CONDITION_NORMAL
strategy_use_status is NOT_STRATEGY_INPUT_NOT_BACKTEST_READY or stricter before construction
provider is DATABENTO
dataset is GLBX.MDP3
schema is ohlcv-1d
timestamp_policy is PASS_ALL_UTC_MIDNIGHT
symbol_roundtrip is PASS_RAW_SYMBOL_AND_INSTRUMENT_ID_MATCH
validation_status is PASS_PER_SYMBOL_CURRENT_ID_FULL_AVAILABLE_ROWS_PRESENT_NO_DUPLICATES
```

Rejected source rows:

```text
degraded provider-condition rows
missing provider-condition rows
blocked or unresolved provider-condition rows
duplicate symbol/date rows
non-manifest rows
provider-built continuous rows
continuous-contract downloaded rows
unhashed rows
filled, interpolated, substituted, or repaired rows
```

## Daily Price And Timestamp Labels

Future output must carry:

```text
daily_price_field = DATABENTO_OHLCV_1D_CLOSE
daily_price_semantics = TRADE_BAR_CLOSE_NOT_OFFICIAL_SETTLEMENT
settlement_policy = BLOCKED_PENDING_OFFICIAL_SETTLEMENT_SOURCE_GATE
provider_timestamp_policy = UTC_MIDNIGHT_PROVIDER_DAILY_BAR_TIMESTAMP_NOT_EXCHANGE_SESSION_END
completed_trading_date_policy = CARRIED_FROM_SOURCE_QUARANTINE_COMPLETED_TRADING_DATE
```

Official settlement must remain blocked unless separately sourced and authorized.

## Deterministic Roll Shape

The first future execution gate must use the deterministic lifecycle-safe roll shape defined here. A future execution gate may only implement this rule or fail closed; it must not invent a different roll rule without a separate policy patch and audit.

Locked first-pass roll-rule class:

```text
STATIC_LIFECYCLE_BUFFER_ROLL
```

Locked first-pass roll-rule parameters:

```text
physical_delivery_roll_buffer = 10 completed trading days before the earliest sourced first-notice, delivery-window, or last-trade blocker
cash_settled_roll_buffer = 5 completed trading days before the sourced expiration, termination, or final-settlement blocker
roll_transition_date = latest completed trading date on or before the buffer date where both old and new source contracts have normal provider-condition rows
roll_transition_date_search_order = sort eligible completed trading dates descending from buffer date toward earlier dates; choose the first eligible date in that descending order
roll_pair_requirement = old contract and new contract must both have normal provider-condition rows on the roll transition date
fallback_if_roll_pair_missing = FAIL_CLOSED_ROLL_PAIR_MISSING
fallback_if_lifecycle_blocker_missing = FAIL_CLOSED_LIFECYCLE_EVIDENCE_MISSING
fallback_if_adjacent_contract_missing = FAIL_CLOSED_SOURCE_CONTRACT_MISSING
```

Required product-family blockers:

| Lifecycle class | Required blocker handling before roll selection |
|---|---|
| physical delivery | roll before first notice / delivery-window / last-trade blockers using explicit static lifecycle evidence |
| cash settled | roll before expiration / final-settlement blockers using explicit static lifecycle evidence |

Forbidden first-pass roll triggers:

```text
volume switch
open-interest switch
provider-built continuous roll date
opaque provider smart-symbol roll
post-result roll-date adjustment
strategy-performance-informed roll date
manual row-by-row roll rescue
```

Reason:

Volume and open interest roll triggers require separately authorized volume/open-interest data and validation. Provider continuous roll dates are reference-only until lineage audited.

This shape deliberately prefers a simple static lifecycle buffer over a volume/open-interest roll because the current authorized data foundation has not opened volume or open-interest evidence.

## Back-Adjustment Shape

The first future local continuous construction should use a locally computed additive back-adjustment shape unless the execution gate chooses a stricter fail-closed policy.

Required labels:

```text
adjustment_method = LOCAL_ADDITIVE_BACK_ADJUSTMENT_SHAPE
adjustment_scope = DEVELOPMENT_RECONCILIATION_ONLY
adjusted_series_semantics = LOCAL_EXCESS_RETURN_PRICE_SERIES_FOR_TREND_STYLE_INPUT_ONLY
provider_built_adjustment = NO
ratio_adjustment = NO_UNLESS_SEPARATELY_AUTHORIZED
panama_or_other_adjustment = NO_UNLESS_EXPLICITLY_DEFINED
```

Required future arithmetic proof:

```text
roll_transition_date
old_contract
new_contract
old_contract_roll_date_close
new_contract_roll_date_close
roll_gap_or_offset
adjustment_offset_applied
adjusted_close_before_roll
adjusted_close_after_roll
```

No adjustment may be hidden. Negative adjusted prices, if they occur, must be labeled and not treated as an error unless a later strategy gate requires non-negative inputs.

## Required Future Output Root

Future execution, if separately authorized, should write under:

```text
docs/researchops/source_native_futures_daily_data_library/local_continuous_daily_lineage/16_SYMBOL/2026-05-30/
```

Required future files:

```text
CARVER_16_SYMBOL_LOCAL_CONTINUOUS_DAILY_POLICY_STATUS_2026-05-30.csv
CARVER_16_SYMBOL_LOCAL_CONTINUOUS_DAILY_ROLL_PLAN_2026-05-30.csv
CARVER_16_SYMBOL_LOCAL_CONTINUOUS_DAILY_SOURCE_LINEAGE_2026-05-30.csv
CARVER_16_SYMBOL_LOCAL_CONTINUOUS_DAILY_ADJUSTMENT_LEDGER_2026-05-30.csv
CARVER_16_SYMBOL_LOCAL_CONTINUOUS_DAILY_SERIES_DEV_RECON_ONLY_2026-05-30.csv
CARVER_16_SYMBOL_LOCAL_CONTINUOUS_DAILY_PROVENANCE_2026-05-30.md
CARVER_16_SYMBOL_LOCAL_CONTINUOUS_DAILY_SHA256SUMS_2026-05-30.txt
```

## Future Policy Status CSV Schema

Required columns:

```text
status_key
status_value
status_scope
```

Required labels:

```text
status_scope = LOCAL_CONTINUOUS_DAILY_LINEAGE_DEV_RECON_ONLY
daily_price_field = DATABENTO_OHLCV_1D_CLOSE
daily_price_semantics = TRADE_BAR_CLOSE_NOT_OFFICIAL_SETTLEMENT
provider_timestamp_policy = UTC_MIDNIGHT_PROVIDER_DAILY_BAR_TIMESTAMP_NOT_EXCHANGE_SESSION_END
completed_trading_date_policy = CARRIED_FROM_SOURCE_QUARANTINE_COMPLETED_TRADING_DATE
settlement_policy = BLOCKED_PENDING_OFFICIAL_SETTLEMENT_SOURCE_GATE
provider_api_access = NO
new_data_download = NO
provider_built_continuous_used_as_source = NO
market_row_parsing_scope = EXISTING_GATE1_FRAGMENT_OR_SEPARATELY_AUTHORIZED_DATED_EXPANSION_ONLY
strategy_input_created = NO_UNTIL_EXECUTION_AUDIT_AND_SEPARATE_STRATEGY_INPUT_GATE
diagnostics_run = NO
backtests_run = NO
forecasts_computed = NO
positions_computed = NO
costs_computed = NO
carry_computed = NO
trend_computed = NO
volatility_or_risk_computed = NO
oos_accessed = NO
lockbox_accessed = NO
forward_accessed = NO
git_or_remote_operations = NO
```

## Future Roll Plan CSV Schema

Required columns:

```text
book_symbol
product_family
lifecycle_class
roll_rule_class
roll_rule_parameters
old_source_contract
new_source_contract
roll_transition_date
last_old_contract_completed_trading_date
first_new_contract_completed_trading_date
first_notice_blocker_status
last_trade_blocker_status
expiration_or_final_settlement_blocker_status
provider_condition_policy_status
roll_plan_status
blocker
```

Allowed `roll_plan_status` values:

```text
ROLL_PLAN_READY_FOR_LOCAL_DEV_RECON_CONSTRUCTION
ROLL_PLAN_BLOCKED_LIFECYCLE_EVIDENCE_MISSING
ROLL_PLAN_BLOCKED_SOURCE_CONTRACT_MISSING
ROLL_PLAN_BLOCKED_ROLL_DATE_SOURCE_ROW_MISSING
ROLL_PLAN_BLOCKED_PROVIDER_CONDITION_DEGRADED
ROLL_PLAN_BLOCKED_DUPLICATE_OR_MISSING_DATE
ROLL_PLAN_BLOCKED_UNRESOLVED_FAIL_CLOSED
```

## Future Source Lineage CSV Schema

Required columns:

```text
foundation_scope
series_label
strategy_use_status
book_symbol
continuous_row_date
continuous_timestamp_utc
source_contract
source_provider_symbol
source_instrument_id
source_completed_trading_date
source_timestamp_utc
source_open
source_high
source_low
source_close
source_volume
daily_price_semantics
daily_price_field
provider_timestamp_policy
completed_trading_date_policy
adjustment_factor_or_offset
provider_condition_readiness_status
settlement_policy
source_archive_sha256
source_fragment_table_sha256
roll_policy_status
lineage_policy_status
execution_status
```

Required fixed labels:

```text
foundation_scope = SOURCE_NATIVE_FUTURES_DAILY_DATA_FOUNDATION
series_label = LOCAL_CONTINUOUS_DAILY_LINEAGE_DEV_RECON_ONLY
strategy_use_status = DEV_RECON_ONLY_NOT_TEST_NOT_VALIDATION_NOT_BACKTEST_READY
daily_price_semantics = TRADE_BAR_CLOSE_NOT_OFFICIAL_SETTLEMENT
daily_price_field = DATABENTO_OHLCV_1D_CLOSE
provider_timestamp_policy = UTC_MIDNIGHT_PROVIDER_DAILY_BAR_TIMESTAMP_NOT_EXCHANGE_SESSION_END
completed_trading_date_policy = CARRIED_FROM_SOURCE_QUARANTINE_COMPLETED_TRADING_DATE
settlement_policy = BLOCKED_PENDING_OFFICIAL_SETTLEMENT_SOURCE_GATE
execution_status = LOCAL_LINEAGE_ONLY_NOT_DIAGNOSTIC_NOT_BACKTEST_NOT_STRATEGY_PROMOTION
```

## Future Adjustment Ledger CSV Schema

Required columns:

```text
book_symbol
roll_transition_date
old_source_contract
new_source_contract
old_contract_roll_date_close
new_contract_roll_date_close
roll_gap_or_offset
adjustment_method
adjustment_offset_applied
adjustment_factor_or_offset
adjustment_applies_to_dates_before
adjusted_close_before_roll
adjusted_close_after_roll
negative_adjusted_price_flag
adjustment_policy_status
blocker
```

Allowed `adjustment_policy_status` values:

```text
ADJUSTMENT_READY_FOR_DEV_RECON_LINEAGE_ONLY
ADJUSTMENT_BLOCKED_ROLL_PAIR_MISSING
ADJUSTMENT_BLOCKED_ROLL_DATE_CLOSE_MISSING
ADJUSTMENT_BLOCKED_PROVIDER_CONDITION_DEGRADED
ADJUSTMENT_BLOCKED_UNRESOLVED_FAIL_CLOSED
```

## Future Local Continuous Series CSV Schema

Required columns:

```text
foundation_scope
series_label
strategy_use_status
book_symbol
continuous_row_date
continuous_timestamp_utc
adjusted_open
adjusted_high
adjusted_low
adjusted_close
source_contract
source_provider_symbol
source_instrument_id
source_completed_trading_date
daily_price_semantics
daily_price_field
provider_timestamp_policy
completed_trading_date_policy
adjustment_method
adjustment_factor_or_offset
provider_condition_readiness_status
lineage_policy_status
settlement_policy
execution_status
```

Required fixed labels:

```text
foundation_scope = SOURCE_NATIVE_FUTURES_DAILY_DATA_FOUNDATION
series_label = LOCAL_CONTINUOUS_DAILY_SERIES_DEV_RECON_ONLY
strategy_use_status = DEV_RECON_ONLY_NOT_TEST_NOT_VALIDATION_NOT_BACKTEST_READY
daily_price_semantics = TRADE_BAR_CLOSE_NOT_OFFICIAL_SETTLEMENT
daily_price_field = DATABENTO_OHLCV_1D_CLOSE
provider_timestamp_policy = UTC_MIDNIGHT_PROVIDER_DAILY_BAR_TIMESTAMP_NOT_EXCHANGE_SESSION_END
completed_trading_date_policy = CARRIED_FROM_SOURCE_QUARANTINE_COMPLETED_TRADING_DATE
settlement_policy = BLOCKED_PENDING_OFFICIAL_SETTLEMENT_SOURCE_GATE
execution_status = LOCAL_CONTINUOUS_CONSTRUCTION_DEV_RECON_ONLY_NOT_DIAGNOSTIC_NOT_BACKTEST_NOT_PROMOTION
```

This file, if later built, must still not be treated as strategy-facing TEST/VALIDATION/OOS/Lockbox/Forward data.

## Fail-Closed Rules

Future execution must fail closed on:

```text
missing input artifact
hash mismatch
non-manifest symbol
provider-built continuous row used as source
degraded provider-condition row admitted silently
missing completed trading date
duplicate continuous date per book_symbol
missing roll transition source row
missing old/new close needed for adjustment
unresolved lifecycle blocker
unresolved settlement/close label
unresolved source lineage
any fill, interpolation, substitution, bridge, or reweight
any strategy computation bundled with construction
```

Permitted fail-closed result:

```text
row or symbol marked blocked with explicit blocker
no silent drop
no silent substitute
no silent repair
no promotion
```

## Required Future Execution Audit

Any future execution gate must preserve an automatic lean hostile audit covering:

```text
input hashes
16-symbol coverage or explicit fail-closed subset
roll-rule determinism
lifecycle blocker handling
normal-provider-condition-only admission
no provider-built continuous source authority
no degraded-row silent inclusion
adjustment ledger transparency
source lineage for every continuous row
Development/Reconciliation-only labels
no diagnostics/backtests/forecasts/positions/costs/carry/trend/risk
no OOS/Lockbox/Forward
no CFD or old QuantLab active-pipeline use
no Git/remote operations
```

## Next Gate

Next gate, if separately authorized:

```text
CARVER_16_SYMBOL_LOCAL_CONTINUOUS_DAILY_LINEAGE_EXECUTION_GATE
```

This next gate must specify whether it uses only the existing Gate 1 fragment or separately authorizes additional dated-contract archive parsing needed to create actual roll transitions. If the Gate 1 fragment lacks sufficient adjacent contract overlap for roll construction, execution must fail closed or request a separate dated-contract expansion gate.

## Non-Authorization

This shape gate authorizes no provider API access, provider login, provider account portal use, new market-data request, data download, market-row parsing, continuous-contract download, continuous-series construction, strategy input creation, diagnostics, backtests, forecasts, positions, costs, carry, trend, volatility or risk calculations, OOS, Lockbox, Forward, CFD adapter execution, old QuantLab active-pipeline use, tuning, deployment, trading, promotion, Git staging, commit, push, PR update/opening, or remote operations.
