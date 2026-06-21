# Carver 16-Symbol Dated-Contract Fragment Dev/Reconciliation Table Input Preflight

Date: 2026-05-30

Status:

```text
PROCESS_ONLY_CARVER_16_SYMBOL_DATED_CONTRACT_FRAGMENT_DEV_RECON_TABLE_INPUT_PREFLIGHT_NOT_MARKET_ROW_PARSING_NOT_EXECUTION_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Record read-only filesystem availability and SHA256 hashes for the four local artifacts named by the future dated-contract fragment Development/Reconciliation table execution gate draft.

This preflight does not execute the table gate. It does not parse market rows, count rows, validate row contents, create the dated-contract fragment table, modify raw or sanitized archives, inspect provider accounts, download data, construct continuous series, create strategy input, run diagnostics, run backtests, compute forecasts, compute positions, compute costs, compute carry, compute trend, compute volatility/risk, access OOS/Lockbox/Forward, deploy, trade, promote, stage Git changes, commit, push, update a PR, or perform remote operations.

## Governing Draft

Future execution gate draft:

```text
docs/process/CARVER_16_SYMBOL_DATED_CONTRACT_FRAGMENT_DEV_RECON_TABLE_EXECUTION_GATE_DRAFT_2026-05-30.md
```

The future execution gate remains separately required before any parsing or table creation.

## Read-Only Preflight Result

| Role in future gate | Path | Exists | Bytes | SHA256 |
|---|---|---:|---:|---|
| Canonical manifest | `docs/researchops/source_native_futures_daily_data_library/16_SYMBOL_DAILY_LIBRARY_PROMOTION_READINESS/manifest/CARVER_16_SYMBOL_DATABENTO_DAILY_LIBRARY_CANONICAL_MANIFEST_2026-05-30.csv` | YES | 15823 | `0D1F86071A536227BB120163E8166BA13DE7F4C47345AE3CA1DF99F1B3DF0E88` |
| Sanitized dated-contract archive | `docs/researchops/source_native_futures_daily_data_library/16_SYMBOL_FULL_DAILY_HISTORY/raw_provider_archive/DATABENTO/20260530_DATED_CONTRACT_FULL_AVAILABLE_HISTORY_PER_SYMBOL_CURRENT_IDS/sanitized_bars/DATABENTO_16_SYMBOL_DATED_CONTRACT_FULL_HISTORY_PER_SYMBOL_CURRENT_IDS_SANITIZED.csv` | YES | 783981 | `64279985F0E3A7BD77E97813C5A8D2312B615AA1E3F2451CA24D9910F3556A3F` |
| Provider-condition row join | `docs/researchops/source_native_futures_daily_data_library/16_SYMBOL_FULL_DAILY_HISTORY/raw_provider_archive/DATABENTO/20260530_DATED_CONTRACT_FULL_AVAILABLE_HISTORY_PER_SYMBOL_CURRENT_IDS/provider_condition_metadata_2026-05-30/provider_condition_ledger/DATABENTO_16_SYMBOL_DATED_CONTRACT_PROVIDER_CONDITION_ROW_JOIN.csv` | YES | 1266712 | `649B853CE23E9488541FD3179349FAED2A577282616D93E58447417F88BF58D4` |
| Validation ledger | `docs/researchops/source_native_futures_daily_data_library/16_SYMBOL_FULL_DAILY_HISTORY/raw_provider_archive/DATABENTO/20260530_DATED_CONTRACT_FULL_AVAILABLE_HISTORY_PER_SYMBOL_CURRENT_IDS/validation/DATABENTO_16_SYMBOL_DATED_CONTRACT_FULL_HISTORY_PER_SYMBOL_CURRENT_ID_VALIDATION.csv` | YES | 3392 | `F1AC0D687038027859B8F36BBDAD414C5A97D30990179A5DACD1B89657735AA4` |

Preflight disposition:

```text
ALL_FOUR_FUTURE_INPUT_FILES_PRESENT_AND_HASH_BOUND
```

## What This Proves

This preflight proves only:

- the four paths named by the future execution draft currently exist in the Carver workspace;
- each file can be hash-bound by SHA256;
- the future table execution gate has concrete local inputs available if separately authorized.

## What This Does Not Prove

This preflight does not prove:

- row counts;
- row contents;
- row eligibility;
- admission of 4,483 normal provider-condition rows;
- exclusion of 85 degraded provider-condition rows;
- duplicate-key status;
- symbol membership;
- timestamp policy;
- strategy readiness;
- continuous/roll semantics;
- settlement/close semantics;
- any performance, diagnostic, or backtest fact.

Those claims require the separately authorized future execution gate and its automatic lean hostile audit.

## Current Goal Completion State

Current broad-goal completion state remains:

```text
NOT_COMPLETE
```

Reason:

```text
The input files are present and hash-bound, but the dated-contract fragment table has not been executed and the continuous/roll semantics evidence execution has not been performed.
```

## Non-Authorization

This preflight authorizes no provider API access, no provider login, no new market-data request, no data download, no market-row parsing, no table execution, no raw or sanitized archive modification, no continuous-contract download, no continuous-series construction, no diagnostics, no backtests, no forecasts, no positions, no costs, no carry, no trend, no volatility/risk calculations, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.
