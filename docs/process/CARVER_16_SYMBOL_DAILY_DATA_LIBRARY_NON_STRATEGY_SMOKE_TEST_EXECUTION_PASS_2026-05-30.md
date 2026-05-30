# Carver 16-Symbol Daily Data Library Non-Strategy Smoke-Test Execution Pass

Date: 2026-05-30

Status:

```text
LOCAL_PROCESS_CARVER_16_SYMBOL_DAILY_DATA_LIBRARY_NON_STRATEGY_SCHEMA_DATE_JOIN_SMOKE_TEST_PASS_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Record the execution of the first non-strategy machinery smoke test for the 16-symbol source-native daily data library promotion-readiness chapter.

This smoke test used only existing local Databento quarantine artifacts and the canonical manifest. It did not request provider data, download market data, alter raw/sanitized archive files, create a strategy-facing table, compute returns, run diagnostics, run backtests, compute forecasts, compute positions, compute costs, compute carry, compute trend, compute volatility/risk, access OOS/Lockbox/Forward, touch CFD adapters, use old QuantLab active-pipeline state, tune, deploy, trade, promote, stage Git changes, commit, push, update a PR, or perform remote operations.

## Input Shape

Shape gate:

```text
docs/process/CARVER_16_SYMBOL_DAILY_DATA_LIBRARY_NON_STRATEGY_SMOKE_TEST_SHAPE_GATE_DRAFT_2026-05-30.md
```

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

Validation ledger:

```text
docs/researchops/source_native_futures_daily_data_library/16_SYMBOL_FULL_DAILY_HISTORY/raw_provider_archive/DATABENTO/20260530_DATED_CONTRACT_FULL_AVAILABLE_HISTORY_PER_SYMBOL_CURRENT_IDS/validation/DATABENTO_16_SYMBOL_DATED_CONTRACT_FULL_HISTORY_PER_SYMBOL_CURRENT_ID_VALIDATION.csv
```

## Execution Result

Result:

```text
PASS_NON_STRATEGY_SCHEMA_DATE_JOIN_SMOKE_TEST
```

Observed counts:

```text
MANIFEST_ROWS_OBSERVED: 16
ARCHIVE_ROWS_OBSERVED: 4568
CONDITION_ROWS_OBSERVED: 4568
JOINED_ROWS_OBSERVED: 4568
NORMAL_PROVIDER_CONDITION_ROWS_OBSERVED: 4483
DEGRADED_ROWS_EXCLUDED_OBSERVED: 85
OTHER_BLOCKED_OR_UNRESOLVED_ROWS_OBSERVED: 0
CANDIDATE_ROWS_AFTER_EXCLUSION: 4483
DUPLICATE_KEYS_AFTER_EXCLUSION: 0
NON_MANIFEST_SYMBOLS: 0
UNJOINED_ARCHIVE_ROWS: 0
MANIFEST_COUNT_ERRORS: 0
CANDIDATE_ORDER_FAILURES: 0
```

## Output Artifacts

Output root:

```text
docs/researchops/source_native_futures_daily_data_library/16_SYMBOL_DAILY_LIBRARY_PROMOTION_READINESS/smoke_tests/2026-05-30_schema_date_join
```

Artifacts:

```text
NON_STRATEGY_SCHEMA_DATE_JOIN_SMOKE_TEST_STATUS.csv
SHA256: 25ABE8D230EF45EAF96CE54792A91851E1B9B2DC7E1351BA659AA6347F881141

NON_STRATEGY_SCHEMA_DATE_JOIN_SMOKE_TEST_SYMBOL_SUMMARY.csv
SHA256: 0E74FF2E74CBA6D23A0ACCB0EE9E727F0D572C49CE96F54B54E1DB6D857C236A

NON_STRATEGY_SCHEMA_DATE_JOIN_SMOKE_TEST_PROVENANCE.md
SHA256: 36FC23B9EE1BE907D8E84A4A2ED722F23D4D11DC89C385CEB5B97F003413EB6F

NON_STRATEGY_SCHEMA_DATE_JOIN_SMOKE_TEST_SHA256SUMS.txt
```

## What Passed

The smoke test verified:

- all 16 manifest rows were present;
- all 4,568 sanitized archive rows joined to provider-condition rows on `(provider_symbol, instrument_id, completed_trading_date, timestamp_utc)`;
- all 85 degraded provider-condition rows were excluded from the candidate view;
- 4,483 normal provider-condition rows remained as the plumbing candidate row set;
- no non-manifest symbols appeared;
- no unjoined archive rows appeared;
- no duplicate `(provider_symbol, completed_trading_date)` keys remained after exclusion;
- per-symbol candidate dates were strictly increasing;
- manifest counts matched observed archive/condition counts.

## Boundary

This is not strategy data promotion. It is a non-strategy plumbing pass only.

The 4,483 candidate rows are still not authorized for diagnostics, backtests, forecasts, positions, costs, carry, trend, volatility/risk calculations, OOS, Lockbox, Forward, deployment, trading, or promotion. A separate gate is required to create any Development/Reconciliation strategy-facing table.

## Next Clean Gate

Recommended next gate:

```text
CARVER_16_SYMBOL_DAILY_LIBRARY_DEVELOPMENT_RECONCILIATION_TABLE_SHAPE_GATE
```

That future gate should decide whether to create a strategy-facing Development/Reconciliation input table from the 4,483 normal provider-condition rows, while preserving degraded-row exclusions and keeping diagnostics/backtests/forecasts/positions closed.

## Non-Authorization

This execution record authorizes no provider API access, no new market-data request, no new data download, no raw or sanitized archive modification, no strategy-facing table creation, no returns, no diagnostics, no backtests, no forecasts, no positions, no costs, no carry, no trend, no volatility/risk calculations, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.
