# Carver 16-Symbol Dated-Contract Fragment Dev/Reconciliation Table Shape Gate

Date: 2026-05-30

Status:

```text
PROCESS_ONLY_CARVER_16_SYMBOL_DATED_CONTRACT_FRAGMENT_DEV_RECON_TABLE_SHAPE_GATE_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Define the future shape of a tightly fenced 16-symbol dated-contract fragment Development/Reconciliation table for plumbing only.

This gate does not create the table. It defines the contract a later execution gate must satisfy if the operator chooses to create a local table from already-quarantined Databento artifacts.

## Governing Decision

Decision record:

```text
docs/process/CARVER_16_SYMBOL_DAILY_LIBRARY_DEV_RECON_OR_CONTINUOUS_ROLL_DECISION_GATE_2026-05-30.md
```

Selected immediate gate:

```text
CARVER_16_SYMBOL_DATED_CONTRACT_FRAGMENT_DEV_RECON_TABLE_SHAPE_GATE
```

Allowed purpose:

```text
PLUMBING_ONLY_TABLE_FOR_SCHEMA_LOADING_DATE_JOIN_HASH_LINEAGE_AND_EXCLUSION_MECHANICS
```

Required label:

```text
DATED_CONTRACT_FRAGMENT_TABLE_FOR_PLUMBING_ONLY
```

## Lane

```text
SOURCE_NATIVE_FUTURES
```

No CFD assumptions, CFD adapters, old QuantLab active-pipeline state, or continuous-contract substitutions are admitted.

## Source Universe

The future table may use only the locked 16-symbol manifest:

```text
ZT, ZF, ZN, MES, MNQ, M2K, MYM, QM, RB, ZC, ZS, ZM, ZL, ZW, HE, LE
```

Canonical manifest:

```text
docs/researchops/source_native_futures_daily_data_library/16_SYMBOL_DAILY_LIBRARY_PROMOTION_READINESS/manifest/CARVER_16_SYMBOL_DATABENTO_DAILY_LIBRARY_CANONICAL_MANIFEST_2026-05-30.csv
SHA256: 0D1F86071A536227BB120163E8166BA13DE7F4C47345AE3CA1DF99F1B3DF0E88
```

## Allowed Input Artifacts

A future execution gate may read only existing local quarantine artifacts unless separately authorized:

```text
docs/researchops/source_native_futures_daily_data_library/16_SYMBOL_FULL_DAILY_HISTORY/raw_provider_archive/DATABENTO/20260530_DATED_CONTRACT_FULL_AVAILABLE_HISTORY_PER_SYMBOL_CURRENT_IDS/sanitized_bars/DATABENTO_16_SYMBOL_DATED_CONTRACT_FULL_HISTORY_PER_SYMBOL_CURRENT_IDS_SANITIZED.csv

docs/researchops/source_native_futures_daily_data_library/16_SYMBOL_FULL_DAILY_HISTORY/raw_provider_archive/DATABENTO/20260530_DATED_CONTRACT_FULL_AVAILABLE_HISTORY_PER_SYMBOL_CURRENT_IDS/provider_condition_metadata_2026-05-30/provider_condition_ledger/DATABENTO_16_SYMBOL_DATED_CONTRACT_PROVIDER_CONDITION_ROW_JOIN.csv

docs/researchops/source_native_futures_daily_data_library/16_SYMBOL_FULL_DAILY_HISTORY/raw_provider_archive/DATABENTO/20260530_DATED_CONTRACT_FULL_AVAILABLE_HISTORY_PER_SYMBOL_CURRENT_IDS/validation/DATABENTO_16_SYMBOL_DATED_CONTRACT_FULL_HISTORY_PER_SYMBOL_CURRENT_ID_VALIDATION.csv

docs/researchops/source_native_futures_daily_data_library/16_SYMBOL_DAILY_LIBRARY_PROMOTION_READINESS/smoke_tests/2026-05-30_schema_date_join/
```

No provider API call, new market-data request, new download, expanded date range, expanded symbol set, or continuous-contract request is opened by this shape gate.

## Admissible Row Rule

The future table may include only rows satisfying all of:

```text
provider == DATABENTO
dataset == GLBX.MDP3
schema == ohlcv-1d
source_contract_identity == EXPLICIT_DATED_CONTRACT
source_table_label == DATED_CONTRACT_FRAGMENT_TABLE_FOR_PLUMBING_ONLY
provider_condition_readiness_status == ROW_READY_PROVIDER_CONDITION_NORMAL
validation_status == PASS_PER_SYMBOL_CURRENT_ID_FULL_AVAILABLE_ROWS_PRESENT_NO_DUPLICATES
symbol_roundtrip == PASS_RAW_SYMBOL_AND_INSTRUMENT_ID_MATCH
timestamp_policy == PASS_ALL_UTC_MIDNIGHT
quarantine_status == QUARANTINE_ONLY_NOT_DIAGNOSTIC_NOT_BACKTEST
```

Rows must be excluded if any of the following apply:

```text
ROW_QUARANTINED_PROVIDER_CONDITION_DEGRADED
missing provider-condition metadata
blocked provider-condition metadata
unresolved provider-condition metadata
duplicate provider_symbol/completed_trading_date key
non-manifest symbol
non-ohlcv-1d schema
continuous-contract identity
symbol or instrument-id mismatch
timestamp policy failure
missing hash lineage
```

Expected current counts:

```text
MANIFEST_ROWS: 16
ARCHIVE_ROWS: 4568
NORMAL_PROVIDER_CONDITION_ROWS_ELIGIBLE_FOR_FRAGMENT_TABLE: 4483
DEGRADED_ROWS_EXCLUDED: 85
OTHER_BLOCKED_OR_UNRESOLVED_ROWS: 0
```

## Required Output Shape For Future Execution

Recommended future output root:

```text
docs/researchops/source_native_futures_daily_data_library/16_SYMBOL_DATED_CONTRACT_FRAGMENT_DEV_RECON_TABLE/2026-05-30/
```

Required future artifacts:

```text
CARVER_16_SYMBOL_DATED_CONTRACT_FRAGMENT_DEV_RECON_TABLE_2026-05-30.csv
CARVER_16_SYMBOL_DATED_CONTRACT_FRAGMENT_DEV_RECON_TABLE_STATUS_2026-05-30.csv
CARVER_16_SYMBOL_DATED_CONTRACT_FRAGMENT_DEV_RECON_TABLE_PROVENANCE_2026-05-30.md
CARVER_16_SYMBOL_DATED_CONTRACT_FRAGMENT_DEV_RECON_TABLE_SHA256SUMS_2026-05-30.txt
```

Minimum row schema:

```text
foundation_scope
table_label
provider
dataset
schema
book_symbol
provider_symbol
locked_raw_symbol
instrument_id
source_contract_month
timestamp_utc
completed_trading_date
open
high
low
close
volume
provider_condition_readiness_status
provider_condition_label
validation_status
quarantine_status
source_archive_sha256
condition_join_sha256
canonical_manifest_sha256
row_policy_status
strategy_use_status
```

Required row labels:

```text
foundation_scope: SOURCE_NATIVE_FUTURES_DAILY_DATA_FOUNDATION
table_label: DATED_CONTRACT_FRAGMENT_TABLE_FOR_PLUMBING_ONLY
row_policy_status: NORMAL_PROVIDER_CONDITION_ROW_ONLY
strategy_use_status: NOT_STRATEGY_INPUT_NOT_BACKTEST_READY
```

## Required Future Validation

A later execution gate must prove:

- exactly 16 manifest symbols are represented;
- exactly 4,483 normal provider-condition rows are admitted unless a stronger current artifact changes the count;
- all 85 degraded rows are excluded and preserved as an exclusion count;
- no non-manifest symbol is included;
- no continuous contract is included;
- no duplicate `(provider_symbol, completed_trading_date)` key exists;
- every row has condition metadata;
- every row has hash lineage back to the canonical manifest, sanitized archive, and provider-condition join;
- completed trading date is preserved as the daily key;
- UTC timestamp is preserved as provider daily timestamp, not exchange session-end authority;
- no returns, diagnostics, backtests, forecasts, positions, costs, carry, trend, volatility/risk, OOS, Lockbox, Forward, deployment, trading, or promotion are computed.

## Interpretation Boundary

This future table, if created, may support only:

```text
schema loading
date joins
manifest enforcement
hash lineage tests
degraded-row exclusion mechanics
downstream interface plumbing
```

It must not support:

```text
strategy interpretation
continuous-series interpretation
roll logic
back-adjusted prices
returns
forecast computation
position sizing
cost computation
carry computation
trend computation
volatility or risk calculation
diagnostics
backtests
performance claims
promotion
```

## Audit Requirements

Lean hostile audit is automatic for this shape gate and for any later execution record.

Opus or GPT Extended Pro audit is not required for this plumbing-only shape gate. It should be considered before broad multi-strategy use, before admitting degraded rows, before using continuous or rolled data as source authority, or before any portfolio-level interpretation.

## Next Required Gate Before Strategy Machinery

General Carver strategy machinery remains blocked until:

```text
CARVER_SOURCE_NATIVE_CONTINUOUS_ROLL_DAILY_DATA_SEMANTICS_SHAPE_GATE
```

is completed and a later separately authorized execution path creates a source-native daily strategy input with explicit continuous/roll semantics.

## Non-Authorization

This shape gate authorizes no provider API access, no new market-data request, no data download, no market-row parsing, no table execution, no raw or sanitized archive modification, no diagnostics, no backtests, no forecasts, no positions, no costs, no carry, no trend, no volatility/risk calculations, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.
