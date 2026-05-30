# Carver 16-Symbol Dated-Contract Fragment Dev/Reconciliation Table Output Schema Contract

Date: 2026-05-30

Status:

```text
PROCESS_ONLY_CARVER_16_SYMBOL_DATED_CONTRACT_FRAGMENT_DEV_RECON_TABLE_OUTPUT_SCHEMA_CONTRACT_NOT_EXECUTION_NOT_MARKET_ROW_PARSING_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Define the exact future output schema and fail-closed contract for a separately authorized 16-symbol dated-contract fragment Development/Reconciliation table execution.

This artifact does not execute the table gate. It does not parse market rows, count rows, validate row contents, create the dated-contract fragment table, modify raw or sanitized archives, inspect provider accounts, download data, construct continuous series, create strategy input, run diagnostics, run backtests, compute forecasts, compute positions, compute costs, compute carry, compute trend, compute volatility/risk, access OOS/Lockbox/Forward, deploy, trade, promote, stage Git changes, commit, push, update a PR, or perform remote operations.

## Governing Artifacts

Gate draft:

```text
docs/process/CARVER_16_SYMBOL_DATED_CONTRACT_FRAGMENT_DEV_RECON_TABLE_EXECUTION_GATE_DRAFT_2026-05-30.md
```

Input preflight:

```text
docs/process/CARVER_16_SYMBOL_DATED_CONTRACT_FRAGMENT_DEV_RECON_TABLE_INPUT_PREFLIGHT_2026-05-30.md
```

Two-gate handoff:

```text
docs/process/CARVER_DAILY_DATA_FOUNDATION_TWO_GATE_AUTHORIZATION_READY_PACKET_2026-05-30.md
```

Completion matrix:

```text
docs/process/CARVER_DAILY_DATA_FOUNDATION_COMPLETION_CRITERIA_AND_EVIDENCE_MATRIX_2026-05-30.md
```

## Future Output Root

If the future gate is separately authorized, outputs must be written under:

```text
docs/researchops/source_native_futures_daily_data_library/16_SYMBOL_DATED_CONTRACT_FRAGMENT_DEV_RECON_TABLE/2026-05-30/
```

Required future files:

```text
CARVER_16_SYMBOL_DATED_CONTRACT_FRAGMENT_DEV_RECON_TABLE_2026-05-30.csv
CARVER_16_SYMBOL_DATED_CONTRACT_FRAGMENT_DEV_RECON_TABLE_STATUS_2026-05-30.csv
CARVER_16_SYMBOL_DATED_CONTRACT_FRAGMENT_DEV_RECON_TABLE_PROVENANCE_2026-05-30.md
CARVER_16_SYMBOL_DATED_CONTRACT_FRAGMENT_DEV_RECON_TABLE_SHA256SUMS_2026-05-30.txt
```

## Table CSV Contract

Future file:

```text
CARVER_16_SYMBOL_DATED_CONTRACT_FRAGMENT_DEV_RECON_TABLE_2026-05-30.csv
```

Future expected row scope, not current proof:

```text
ADMITTED_ROWS_ONLY
EXPECTED_ADMITTED_ROWS: 4483
```

Future required columns, in order:

| Column | Required value/domain |
|---|---|
| `foundation_scope` | `SOURCE_NATIVE_FUTURES_DAILY_DATA_FOUNDATION` |
| `table_label` | `DATED_CONTRACT_FRAGMENT_TABLE_FOR_PLUMBING_ONLY` |
| `row_policy_status` | `NORMAL_PROVIDER_CONDITION_ROW_ONLY` |
| `strategy_use_status` | `NOT_STRATEGY_INPUT_NOT_BACKTEST_READY` |
| `provider` | `DATABENTO` |
| `dataset` | `GLBX.MDP3` |
| `schema` | `ohlcv-1d` |
| `source_contract_identity` | `EXPLICIT_DATED_CONTRACT` |
| `book_symbol` | one of the 16 locked manifest symbols |
| `provider_symbol` | dated-contract provider symbol, never continuous |
| `instrument_id` | provider instrument id from the existing local artifacts |
| `completed_trading_date` | preserved daily key from existing local artifacts |
| `provider_timestamp_utc` | provider daily timestamp from existing local artifacts |
| `open` | provider OHLCV value carried from existing local artifacts |
| `high` | provider OHLCV value carried from existing local artifacts |
| `low` | provider OHLCV value carried from existing local artifacts |
| `close` | provider OHLCV value carried from existing local artifacts |
| `volume` | provider OHLCV value carried from existing local artifacts |
| `provider_condition_readiness_status` | `ROW_READY_PROVIDER_CONDITION_NORMAL` |
| `provider_condition_code` | provider-condition code carried from existing local provider-condition artifact |
| `validation_status` | `PASS_PER_SYMBOL_CURRENT_ID_FULL_AVAILABLE_ROWS_PRESENT_NO_DUPLICATES` |
| `timestamp_policy` | `PASS_ALL_UTC_MIDNIGHT` |
| `symbol_roundtrip` | `PASS_RAW_SYMBOL_AND_INSTRUMENT_ID_MATCH` |
| `input_manifest_sha256` | `0D1F86071A536227BB120163E8166BA13DE7F4C47345AE3CA1DF99F1B3DF0E88` |
| `input_sanitized_archive_sha256` | `64279985F0E3A7BD77E97813C5A8D2312B615AA1E3F2451CA24D9910F3556A3F` |
| `input_provider_condition_join_sha256` | `649B853CE23E9488541FD3179349FAED2A577282616D93E58447417F88BF58D4` |
| `input_validation_ledger_sha256` | `F1AC0D687038027859B8F36BBDAD414C5A97D30990179A5DACD1B89657735AA4` |
| `execution_status` | `PLUMBING_ONLY_NOT_STRATEGY_NOT_DIAGNOSTIC_NOT_BACKTEST` |

The table must not include:

```text
returns
PnL
Sharpe
drawdown
forecast
position
cost
carry
trend
volatility
risk
continuous contract field promoted as source authority
strategy-ready flag
```

## Status CSV Contract

Future file:

```text
CARVER_16_SYMBOL_DATED_CONTRACT_FRAGMENT_DEV_RECON_TABLE_STATUS_2026-05-30.csv
```

Required columns:

| Column | Required value/domain |
|---|---|
| `status_key` | stable status key |
| `status_value` | exact status value |
| `status_scope` | `PLUMBING_ONLY` |

Future required status rows, not current row-count proof:

| `status_key` | Required `status_value` |
|---|---|
| `execution_status` | `LOCAL_PROCESS_CARVER_16_SYMBOL_DATED_CONTRACT_FRAGMENT_DEV_RECON_TABLE_EXECUTION_PLUMBING_ONLY_NOT_STRATEGY_NOT_DIAGNOSTIC_NOT_BACKTEST` |
| `admitted_row_count` | `4483` |
| `excluded_degraded_row_count` | `85` |
| `manifest_symbol_count` | `16` |
| `non_manifest_symbol_count` | `0` |
| `continuous_contract_row_count` | `0` |
| `duplicate_provider_symbol_completed_trading_date_count` | `0` |
| `provider_api_access` | `NO` |
| `new_data_download` | `NO` |
| `continuous_series_constructed` | `NO` |
| `strategy_input_created` | `NO` |
| `diagnostics_run` | `NO` |
| `backtests_run` | `NO` |
| `forecasts_computed` | `NO` |
| `positions_computed` | `NO` |
| `costs_computed` | `NO` |
| `carry_computed` | `NO` |
| `trend_computed` | `NO` |
| `volatility_or_risk_computed` | `NO` |
| `oos_accessed` | `NO` |
| `lockbox_accessed` | `NO` |
| `forward_accessed` | `NO` |
| `git_or_remote_operations` | `NO` |

## Provenance MD Contract

Future file:

```text
CARVER_16_SYMBOL_DATED_CONTRACT_FRAGMENT_DEV_RECON_TABLE_PROVENANCE_2026-05-30.md
```

Required sections:

```text
Status
Scope
Input Artifacts And Hashes
Row Admission Rule
Row Exclusion Rule
Output Files
Validation Summary
Audit Requirement
Non-Authorization
```

Required statements:

- the table is a dated-contract fragment table for plumbing only;
- the table is not a continuous or rolled strategy series;
- UTC provider timestamp is not exchange session-end authority;
- degraded provider-condition rows are excluded, not repaired;
- missing, blocked, unresolved, duplicate, non-manifest, continuous, or hash-mismatched rows fail closed;
- strategy-facing data remains blocked pending continuous/roll policy.

## SHA256SUMS Contract

Future file:

```text
CARVER_16_SYMBOL_DATED_CONTRACT_FRAGMENT_DEV_RECON_TABLE_SHA256SUMS_2026-05-30.txt
```

Required contents:

```text
SHA256  CARVER_16_SYMBOL_DATED_CONTRACT_FRAGMENT_DEV_RECON_TABLE_2026-05-30.csv
SHA256  CARVER_16_SYMBOL_DATED_CONTRACT_FRAGMENT_DEV_RECON_TABLE_STATUS_2026-05-30.csv
SHA256  CARVER_16_SYMBOL_DATED_CONTRACT_FRAGMENT_DEV_RECON_TABLE_PROVENANCE_2026-05-30.md
```

The actual SHA256 values must be computed only after the future files are created by the separately authorized execution gate.

## Future Fail-Closed Validation Checklist

The future execution must fail closed if any of the following occurs:

- any required input file is missing;
- any required input hash differs from the input preflight;
- admitted row count is not 4,483 unless a separately authorized replacement count authority exists before execution;
- excluded degraded row count is not 85 unless a separately authorized replacement count authority exists before execution;
- any admitted row lacks provider-condition metadata;
- any admitted row has provider-condition status other than `ROW_READY_PROVIDER_CONDITION_NORMAL`;
- any admitted row has validation status other than `PASS_PER_SYMBOL_CURRENT_ID_FULL_AVAILABLE_ROWS_PRESENT_NO_DUPLICATES`;
- any admitted row has timestamp policy other than `PASS_ALL_UTC_MIDNIGHT`;
- any admitted row has symbol roundtrip status other than `PASS_RAW_SYMBOL_AND_INSTRUMENT_ID_MATCH`;
- any non-manifest symbol appears;
- any continuous-contract row appears;
- any duplicate `(provider_symbol, completed_trading_date)` key appears;
- any output row lacks the required plumbing-only and not-strategy labels;
- any strategy math or performance evidence is produced;
- any forbidden operation is attempted.

## Current Goal Completion State

Current broad-goal completion state remains:

```text
NOT_COMPLETE
```

Reason:

```text
This schema contract defines future output expectations only. It does not execute the dated-contract fragment table and does not execute continuous/roll evidence.
```

## Non-Authorization

This schema contract authorizes no provider API access, no provider login, no new market-data request, no data download, no market-row parsing, no table execution, no row counting, no row validation, no raw or sanitized archive modification, no continuous-contract download, no continuous-series construction, no diagnostics, no backtests, no forecasts, no positions, no costs, no carry, no trend, no volatility/risk calculations, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.
