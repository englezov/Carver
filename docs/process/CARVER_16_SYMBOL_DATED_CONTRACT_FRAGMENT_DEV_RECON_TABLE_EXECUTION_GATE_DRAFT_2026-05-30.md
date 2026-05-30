# Carver 16-Symbol Dated-Contract Fragment Dev/Reconciliation Table Execution Gate Draft

Date: 2026-05-30

Status:

```text
PROCESS_ONLY_CARVER_16_SYMBOL_DATED_CONTRACT_FRAGMENT_DEV_RECON_TABLE_EXECUTION_GATE_DRAFT_NOT_EXECUTION_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Draft the exact future execution gate that would create a plumbing-only dated-contract fragment Development/Reconciliation table from existing local quarantine artifacts.

This draft does not execute the gate. It does not parse market rows, create the table, modify raw or sanitized archives, run diagnostics, run backtests, compute returns, compute forecasts, compute positions, compute costs, compute carry, compute trend, compute volatility/risk, access OOS/Lockbox/Forward, deploy, trade, promote, stage Git changes, commit, push, update a PR, or perform remote operations.

## Required Separate Authorization

The future execution gate must be separately authorized by the operator before any parsing or table creation.

Required future status string:

```text
LOCAL_PROCESS_CARVER_16_SYMBOL_DATED_CONTRACT_FRAGMENT_DEV_RECON_TABLE_EXECUTION_PLUMBING_ONLY_NOT_STRATEGY_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Governing Shape

Shape gate:

```text
docs/process/CARVER_16_SYMBOL_DATED_CONTRACT_FRAGMENT_DEV_RECON_TABLE_SHAPE_GATE_2026-05-30.md
```

Handoff decision:

```text
docs/process/CARVER_DAILY_DATA_FOUNDATION_NEXT_STEP_HANDOFF_DECISION_2026-05-30.md
```

## Future Allowed Inputs

If separately authorized, the execution may read only:

```text
docs/researchops/source_native_futures_daily_data_library/16_SYMBOL_DAILY_LIBRARY_PROMOTION_READINESS/manifest/CARVER_16_SYMBOL_DATABENTO_DAILY_LIBRARY_CANONICAL_MANIFEST_2026-05-30.csv

docs/researchops/source_native_futures_daily_data_library/16_SYMBOL_FULL_DAILY_HISTORY/raw_provider_archive/DATABENTO/20260530_DATED_CONTRACT_FULL_AVAILABLE_HISTORY_PER_SYMBOL_CURRENT_IDS/sanitized_bars/DATABENTO_16_SYMBOL_DATED_CONTRACT_FULL_HISTORY_PER_SYMBOL_CURRENT_IDS_SANITIZED.csv

docs/researchops/source_native_futures_daily_data_library/16_SYMBOL_FULL_DAILY_HISTORY/raw_provider_archive/DATABENTO/20260530_DATED_CONTRACT_FULL_AVAILABLE_HISTORY_PER_SYMBOL_CURRENT_IDS/provider_condition_metadata_2026-05-30/provider_condition_ledger/DATABENTO_16_SYMBOL_DATED_CONTRACT_PROVIDER_CONDITION_ROW_JOIN.csv

docs/researchops/source_native_futures_daily_data_library/16_SYMBOL_FULL_DAILY_HISTORY/raw_provider_archive/DATABENTO/20260530_DATED_CONTRACT_FULL_AVAILABLE_HISTORY_PER_SYMBOL_CURRENT_IDS/validation/DATABENTO_16_SYMBOL_DATED_CONTRACT_FULL_HISTORY_PER_SYMBOL_CURRENT_ID_VALIDATION.csv
```

No provider API access, new data download, expanded symbol set, expanded date range, raw archive mutation, or continuous-contract request may be included.

## Future Output Root

If separately authorized, output must be written under:

```text
docs/researchops/source_native_futures_daily_data_library/16_SYMBOL_DATED_CONTRACT_FRAGMENT_DEV_RECON_TABLE/2026-05-30/
```

Required outputs:

```text
CARVER_16_SYMBOL_DATED_CONTRACT_FRAGMENT_DEV_RECON_TABLE_2026-05-30.csv
CARVER_16_SYMBOL_DATED_CONTRACT_FRAGMENT_DEV_RECON_TABLE_STATUS_2026-05-30.csv
CARVER_16_SYMBOL_DATED_CONTRACT_FRAGMENT_DEV_RECON_TABLE_PROVENANCE_2026-05-30.md
CARVER_16_SYMBOL_DATED_CONTRACT_FRAGMENT_DEV_RECON_TABLE_SHA256SUMS_2026-05-30.txt
```

## Future Row Admission Rule

The future execution must admit only rows satisfying:

```text
provider == DATABENTO
dataset == GLBX.MDP3
schema == ohlcv-1d
source_contract_identity == EXPLICIT_DATED_CONTRACT
provider_condition_readiness_status == ROW_READY_PROVIDER_CONDITION_NORMAL
validation_status == PASS_PER_SYMBOL_CURRENT_ID_FULL_AVAILABLE_ROWS_PRESENT_NO_DUPLICATES
timestamp_policy == PASS_ALL_UTC_MIDNIGHT
symbol_roundtrip == PASS_RAW_SYMBOL_AND_INSTRUMENT_ID_MATCH
```

Expected admitted row count:

```text
4483
```

Expected excluded row count:

```text
85
```

Rows excluded:

```text
ROW_QUARANTINED_PROVIDER_CONDITION_DEGRADED
missing provider-condition metadata
blocked provider-condition metadata
unresolved provider-condition metadata
non-manifest symbol
continuous-contract identity
duplicate provider_symbol/completed_trading_date key
timestamp policy failure
symbol or instrument-id mismatch
missing hash lineage
```

## Future Output Labels

Every output row must include:

```text
foundation_scope: SOURCE_NATIVE_FUTURES_DAILY_DATA_FOUNDATION
table_label: DATED_CONTRACT_FRAGMENT_TABLE_FOR_PLUMBING_ONLY
row_policy_status: NORMAL_PROVIDER_CONDITION_ROW_ONLY
strategy_use_status: NOT_STRATEGY_INPUT_NOT_BACKTEST_READY
```

The status artifact must record:

```text
execution_scope: PLUMBING_ONLY
strategy_input_created: NO
diagnostics_run: NO
backtests_run: NO
forecasts_computed: NO
positions_computed: NO
costs_computed: NO
carry_computed: NO
trend_computed: NO
volatility_or_risk_computed: NO
provider_api_access: NO
new_data_download: NO
continuous_series_constructed: NO
```

## Future Validation Requirements

The future execution must prove:

- all 16 manifest symbols are present in the admitted or excluded evidence set;
- exactly 4,483 rows are admitted; if any current local artifact appears to imply a different count, the execution must fail closed unless that artifact is hash-bound, in-scope, pre-existing in the Carver workspace before execution, and separately authorized as the replacement count authority;
- exactly 85 degraded rows are excluded and counted;
- no non-manifest symbol is included;
- no continuous contract is included;
- no duplicate `(provider_symbol, completed_trading_date)` keys exist in admitted rows;
- every admitted row has condition metadata;
- every admitted row has source hash lineage;
- completed trading date is preserved as the daily key;
- UTC timestamp remains provider daily timestamp, not exchange session-end authority;
- no strategy math or performance evidence is produced.

## Automatic Audit Requirement

The future execution must preserve an automatic lean hostile audit result covering:

```text
row admission/exclusion counts
hash lineage
dated-contract-only labeling
no strategy input
no diagnostics/backtests/forecasts/positions/costs/carry/trend/risk
no provider access or new download
no Git/remote operations
```

## Non-Authorization

This draft authorizes no provider API access, no provider login, no new market-data request, no data download, no market-row parsing, no table execution, no raw or sanitized archive modification, no continuous-contract download, no continuous-series construction, no diagnostics, no backtests, no forecasts, no positions, no costs, no carry, no trend, no volatility/risk calculations, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.
