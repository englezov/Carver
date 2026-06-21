# Carver 16-Symbol Dated-Contract Fragment Dev/Reconciliation Table Provenance - 2026-05-30

## Status

Execution status: `LOCAL_PROCESS_CARVER_16_SYMBOL_DATED_CONTRACT_FRAGMENT_DEV_RECON_TABLE_EXECUTION_PLUMBING_ONLY_NOT_STRATEGY_NOT_DIAGNOSTIC_NOT_BACKTEST`.

This artifact records Gate 1 only. It creates a dated-contract fragment table for plumbing and development/reconciliation table-shape work. It is not a source-native continuous or rolled strategy series, not a strategy input, not diagnostic-ready, and not backtest-ready.

## Scope

- Foundation scope: `SOURCE_NATIVE_FUTURES_DAILY_DATA_FOUNDATION`
- Table label: `DATED_CONTRACT_FRAGMENT_TABLE_FOR_PLUMBING_ONLY`
- Provider: `DATABENTO`
- Dataset: `GLBX.MDP3`
- Schema: `ohlcv-1d`
- Contract identity: explicit dated contracts only
- Manifest symbol count: 16

The provider timestamp is carried from the existing Databento quarantine artifact. It is not promoted as an exchange session-end authority. Continuous/roll daily data semantics remain closed pending Gate 2.

## Input Artifacts And Hashes

| Input | Path | SHA256 |
|---|---|---|
| Canonical manifest | `docs\researchops\source_native_futures_daily_data_library\16_SYMBOL_DAILY_LIBRARY_PROMOTION_READINESS\manifest\CARVER_16_SYMBOL_DATABENTO_DAILY_LIBRARY_CANONICAL_MANIFEST_2026-05-30.csv` | `0D1F86071A536227BB120163E8166BA13DE7F4C47345AE3CA1DF99F1B3DF0E88` |
| Sanitized dated-contract archive | `docs\researchops\source_native_futures_daily_data_library\16_SYMBOL_FULL_DAILY_HISTORY\raw_provider_archive\DATABENTO\20260530_DATED_CONTRACT_FULL_AVAILABLE_HISTORY_PER_SYMBOL_CURRENT_IDS\sanitized_bars\DATABENTO_16_SYMBOL_DATED_CONTRACT_FULL_HISTORY_PER_SYMBOL_CURRENT_IDS_SANITIZED.csv` | `64279985F0E3A7BD77E97813C5A8D2312B615AA1E3F2451CA24D9910F3556A3F` |
| Provider-condition row join | `docs\researchops\source_native_futures_daily_data_library\16_SYMBOL_FULL_DAILY_HISTORY\raw_provider_archive\DATABENTO\20260530_DATED_CONTRACT_FULL_AVAILABLE_HISTORY_PER_SYMBOL_CURRENT_IDS\provider_condition_metadata_2026-05-30\provider_condition_ledger\DATABENTO_16_SYMBOL_DATED_CONTRACT_PROVIDER_CONDITION_ROW_JOIN.csv` | `649B853CE23E9488541FD3179349FAED2A577282616D93E58447417F88BF58D4` |
| Validation ledger | `docs\researchops\source_native_futures_daily_data_library\16_SYMBOL_FULL_DAILY_HISTORY\raw_provider_archive\DATABENTO\20260530_DATED_CONTRACT_FULL_AVAILABLE_HISTORY_PER_SYMBOL_CURRENT_IDS\validation\DATABENTO_16_SYMBOL_DATED_CONTRACT_FULL_HISTORY_PER_SYMBOL_CURRENT_ID_VALIDATION.csv` | `F1AC0D687038027859B8F36BBDAD414C5A97D30990179A5DACD1B89657735AA4` |

All input hashes were verified before output creation. Hash mismatch is fail-closed.

## Row Admission Rule

Rows are admitted only when all of the following are true:

- The row joins to the locked 16-symbol manifest by raw Databento symbol and instrument ID.
- Provider is `DATABENTO`, dataset is `GLBX.MDP3`, and schema is `ohlcv-1d`.
- Source contract identity is explicit dated contract only.
- Provider-condition readiness is `ROW_READY_PROVIDER_CONDITION_NORMAL`.
- Validation status is `PASS_PER_SYMBOL_CURRENT_ID_FULL_AVAILABLE_ROWS_PRESENT_NO_DUPLICATES`.
- Timestamp policy is `PASS_ALL_UTC_MIDNIGHT`.
- Symbol roundtrip is `PASS_RAW_SYMBOL_AND_INSTRUMENT_ID_MATCH`.

## Row Exclusion Rule

Rows with provider-condition readiness `ROW_QUARANTINED_PROVIDER_CONDITION_DEGRADED` are excluded from the fragment output. They are not repaired, imputed, relabeled, substituted, or silently skipped. Missing, blocked, unresolved, duplicate, non-manifest, continuous-contract, or hash-mismatched rows fail closed.

## Output Files

| Output | Path |
|---|---|
| Fragment table | `docs\researchops\source_native_futures_daily_data_library\16_SYMBOL_DATED_CONTRACT_FRAGMENT_DEV_RECON_TABLE\2026-05-30\CARVER_16_SYMBOL_DATED_CONTRACT_FRAGMENT_DEV_RECON_TABLE_2026-05-30.csv` |
| Status ledger | `docs\researchops\source_native_futures_daily_data_library\16_SYMBOL_DATED_CONTRACT_FRAGMENT_DEV_RECON_TABLE\2026-05-30\CARVER_16_SYMBOL_DATED_CONTRACT_FRAGMENT_DEV_RECON_TABLE_STATUS_2026-05-30.csv` |
| Provenance record | `docs\researchops\source_native_futures_daily_data_library\16_SYMBOL_DATED_CONTRACT_FRAGMENT_DEV_RECON_TABLE\2026-05-30\CARVER_16_SYMBOL_DATED_CONTRACT_FRAGMENT_DEV_RECON_TABLE_PROVENANCE_2026-05-30.md` |
| SHA256SUMS | `docs\researchops\source_native_futures_daily_data_library\16_SYMBOL_DATED_CONTRACT_FRAGMENT_DEV_RECON_TABLE\2026-05-30\CARVER_16_SYMBOL_DATED_CONTRACT_FRAGMENT_DEV_RECON_TABLE_SHA256SUMS_2026-05-30.txt` |

## Validation Summary

- Admitted rows: `4483`
- Excluded degraded rows: `85`
- Non-manifest rows: `0`
- Continuous-contract rows: `0`
- Duplicate `(provider_symbol, completed_trading_date)` rows in admitted output: `0`
- Provider-condition source status counts across manifest rows: `ROW_QUARANTINED_PROVIDER_CONDITION_DEGRADED=85, ROW_READY_PROVIDER_CONDITION_NORMAL=4483`

## Audit Requirement

A lean hostile audit result must be preserved for this Gate 1 execution. The audit is limited to source-faithfulness, local plumbing boundaries, row-count/hash consistency, and governance non-authorization checks.

## Non-Authorization

This Gate 1 execution did not authorize or perform provider API access, new data download, expanded symbols, expanded date windows, continuous series construction, strategy input creation, diagnostics, backtests, forecasts, positions, costs, carry, trend, volatility or risk calculations, OOS, Lockbox, Forward, CFD adapters, old QuantLab active-pipeline use, tuning, deployment, trading, promotion, Git staging, commit, push, PR update, or remote operations.

Strategy-facing data remains blocked pending source-native continuous/roll daily data semantics, policy decision, and a separately authorized strategy-facing input gate.
