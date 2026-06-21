# Carver 16-Symbol Daily Library Non-Strategy Schema/Date Join Smoke Test Provenance

Date: 2026-05-30

Status:

```text
PASS_NON_STRATEGY_SCHEMA_DATE_JOIN_SMOKE_TEST
```

## Scope

This smoke test read only existing local Carver artifacts and performed plumbing-only checks:

- manifest schema and counts;
- sanitized archive schema and row identity;
- provider-condition row join on `(provider_symbol, instrument_id, completed_trading_date, timestamp_utc)`;
- degraded-row exclusion from candidate view;
- duplicate key checks;
- per-symbol date ordering checks;
- hash lineage recording.

## Inputs

```text
docs\researchops\source_native_futures_daily_data_library\16_SYMBOL_DAILY_LIBRARY_PROMOTION_READINESS\manifest\CARVER_16_SYMBOL_DATABENTO_DAILY_LIBRARY_CANONICAL_MANIFEST_2026-05-30.csv
docs\researchops\source_native_futures_daily_data_library\16_SYMBOL_FULL_DAILY_HISTORY\raw_provider_archive\DATABENTO\20260530_DATED_CONTRACT_FULL_AVAILABLE_HISTORY_PER_SYMBOL_CURRENT_IDS\sanitized_bars\DATABENTO_16_SYMBOL_DATED_CONTRACT_FULL_HISTORY_PER_SYMBOL_CURRENT_IDS_SANITIZED.csv
docs\researchops\source_native_futures_daily_data_library\16_SYMBOL_FULL_DAILY_HISTORY\raw_provider_archive\DATABENTO\20260530_DATED_CONTRACT_FULL_AVAILABLE_HISTORY_PER_SYMBOL_CURRENT_IDS\provider_condition_metadata_2026-05-30\provider_condition_ledger\DATABENTO_16_SYMBOL_DATED_CONTRACT_PROVIDER_CONDITION_ROW_JOIN.csv
docs\researchops\source_native_futures_daily_data_library\16_SYMBOL_FULL_DAILY_HISTORY\raw_provider_archive\DATABENTO\20260530_DATED_CONTRACT_FULL_AVAILABLE_HISTORY_PER_SYMBOL_CURRENT_IDS\validation\DATABENTO_16_SYMBOL_DATED_CONTRACT_FULL_HISTORY_PER_SYMBOL_CURRENT_ID_VALIDATION.csv
```

## Outputs

```text
docs\researchops\source_native_futures_daily_data_library\16_SYMBOL_DAILY_LIBRARY_PROMOTION_READINESS\smoke_tests\2026-05-30_schema_date_join\NON_STRATEGY_SCHEMA_DATE_JOIN_SMOKE_TEST_STATUS.csv
docs\researchops\source_native_futures_daily_data_library\16_SYMBOL_DAILY_LIBRARY_PROMOTION_READINESS\smoke_tests\2026-05-30_schema_date_join\NON_STRATEGY_SCHEMA_DATE_JOIN_SMOKE_TEST_SYMBOL_SUMMARY.csv
docs\researchops\source_native_futures_daily_data_library\16_SYMBOL_DAILY_LIBRARY_PROMOTION_READINESS\smoke_tests\2026-05-30_schema_date_join\NON_STRATEGY_SCHEMA_DATE_JOIN_SMOKE_TEST_SHA256SUMS.txt
```

## Result Counts

```text
MANIFEST_ROWS_OBSERVED: 16
ARCHIVE_ROWS_OBSERVED: 4568
JOINED_ROWS_OBSERVED: 4568
NORMAL_PROVIDER_CONDITION_ROWS_OBSERVED: 4483
DEGRADED_ROWS_EXCLUDED_OBSERVED: 85
CANDIDATE_ROWS_AFTER_EXCLUSION: 4483
DUPLICATE_KEYS_AFTER_EXCLUSION: 0
NON_MANIFEST_SYMBOLS: 0
UNJOINED_ARCHIVE_ROWS: 0
```

## Non-Strategy Boundary

This smoke test did not request provider data, download market data, alter raw/sanitized archives, create a strategy-facing table, compute returns, run diagnostics, run backtests, compute forecasts, compute positions, compute costs, compute carry, compute trend, compute volatility/risk, access OOS/Lockbox/Forward, touch CFD adapters, use old QuantLab active pipelines, tune, deploy, trade, promote, stage Git changes, commit, push, update a PR, or perform remote operations.
