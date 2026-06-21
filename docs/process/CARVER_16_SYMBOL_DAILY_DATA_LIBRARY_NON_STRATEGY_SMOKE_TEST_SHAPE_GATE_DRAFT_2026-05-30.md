# Carver 16-Symbol Daily Data Library Non-Strategy Smoke-Test Shape Gate Draft

Date: 2026-05-30

Status:

```text
PROCESS_ONLY_CARVER_16_SYMBOL_DAILY_DATA_LIBRARY_NON_STRATEGY_SMOKE_TEST_SHAPE_GATE_DRAFT_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Define the first machinery smoke test for the 16-symbol source-native daily data library promotion-readiness chapter.

This is a plumbing-only shape gate. The future smoke test may verify schema, ordering, date joins, provider-condition exclusion logic, and hash lineage. It must not compute returns, diagnostics, backtests, forecasts, positions, costs, carry, trend, volatility, risk, performance statistics, OOS, Lockbox, Forward, deployment, trading, or promotion.

## Inputs

Canonical manifest:

```text
docs/researchops/source_native_futures_daily_data_library/16_SYMBOL_DAILY_LIBRARY_PROMOTION_READINESS/manifest/CARVER_16_SYMBOL_DATABENTO_DAILY_LIBRARY_CANONICAL_MANIFEST_2026-05-30.csv
SHA256: 0D1F86071A536227BB120163E8166BA13DE7F4C47345AE3CA1DF99F1B3DF0E88
```

Sanitized quarantine archive:

```text
docs/researchops/source_native_futures_daily_data_library/16_SYMBOL_FULL_DAILY_HISTORY/raw_provider_archive/DATABENTO/20260530_DATED_CONTRACT_FULL_AVAILABLE_HISTORY_PER_SYMBOL_CURRENT_IDS/sanitized_bars/DATABENTO_16_SYMBOL_DATED_CONTRACT_FULL_HISTORY_PER_SYMBOL_CURRENT_IDS_SANITIZED.csv
```

Provider-condition row join:

```text
docs/researchops/source_native_futures_daily_data_library/16_SYMBOL_FULL_DAILY_HISTORY/raw_provider_archive/DATABENTO/20260530_DATED_CONTRACT_FULL_AVAILABLE_HISTORY_PER_SYMBOL_CURRENT_IDS/provider_condition_metadata_2026-05-30/provider_condition_ledger/DATABENTO_16_SYMBOL_DATED_CONTRACT_PROVIDER_CONDITION_ROW_JOIN.csv
```

## Allowed Future Smoke-Test Actions

A later explicitly authorized smoke-test execution may:

- read only the existing manifest, sanitized quarantine archive, validation ledger, and provider-condition row join;
- join archive rows to condition rows on `(provider_symbol, instrument_id, completed_trading_date, timestamp_utc)`;
- apply the provider-condition policy from the manifest;
- verify all 16 manifest symbols are represented;
- verify degraded rows are excluded from the candidate view;
- verify row counts match the manifest;
- verify rows sort by `provider_symbol`, then `completed_trading_date`;
- verify no duplicate `(provider_symbol, completed_trading_date)` keys exist after exclusion;
- verify required columns exist and are non-empty;
- write a plumbing-only smoke-test status/provenance artifact.

## Forbidden Future Smoke-Test Actions

The smoke test must not:

- request data from Databento or any provider;
- download data;
- alter raw or sanitized quarantine archive files;
- compute returns;
- compute price changes as a signal or statistic;
- compute volatility or risk;
- compute costs;
- compute carry;
- compute trend;
- compute forecasts;
- compute positions;
- run diagnostics;
- run backtests;
- access OOS, Lockbox, or Forward;
- touch CFD adapters;
- use old QuantLab active-pipeline state;
- tune;
- deploy;
- trade;
- promote.

## Expected Smoke-Test Result Shape

The future execution result should report:

```text
MANIFEST_ROWS_EXPECTED: 16
MANIFEST_ROWS_OBSERVED: 16
ARCHIVE_ROWS_OBSERVED: 4568
NORMAL_PROVIDER_CONDITION_ROWS_EXPECTED: 4483
DEGRADED_ROWS_EXCLUDED_EXPECTED: 85
JOINED_ROWS_OBSERVED: 4568
CANDIDATE_ROWS_AFTER_EXCLUSION: 4483
DUPLICATE_KEYS_AFTER_EXCLUSION: 0
NON_MANIFEST_SYMBOLS: 0
DIAGNOSTICS_RUN: NO
BACKTESTS_RUN: NO
FORECASTS_COMPUTED: NO
POSITIONS_COMPUTED: NO
```

Any mismatch must fail closed and produce no strategy-facing table.

## Output Boundary

The smoke-test output, if later authorized, may be:

```text
docs/researchops/source_native_futures_daily_data_library/16_SYMBOL_DAILY_LIBRARY_PROMOTION_READINESS/smoke_tests/
```

Permitted output files:

```text
NON_STRATEGY_SCHEMA_DATE_JOIN_SMOKE_TEST_STATUS.csv
NON_STRATEGY_SCHEMA_DATE_JOIN_SMOKE_TEST_PROVENANCE.md
NON_STRATEGY_SCHEMA_DATE_JOIN_SMOKE_TEST_SHA256SUMS.txt
```

No strategy-facing data table is created by this shape gate.

## Audit Requirements

Lean hostile audit should verify:

- the smoke-test shape is plumbing-only;
- degraded rows remain excluded;
- no performance/statistical calculation is smuggled in;
- no provider access is opened;
- no GitHub operation is implied.

## Non-Authorization

This draft authorizes no provider API access, no new market-data request, no market-row parsing, no diagnostics, no backtests, no forecasts, no positions, no costs, no carry, no trend, no volatility/risk calculations, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.
