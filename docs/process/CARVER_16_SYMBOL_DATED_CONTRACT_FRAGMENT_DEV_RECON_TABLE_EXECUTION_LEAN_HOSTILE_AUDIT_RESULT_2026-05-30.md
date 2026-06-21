# Carver 16-Symbol Dated-Contract Fragment Dev/Reconciliation Table Execution Lean Hostile Audit Result - 2026-05-30

## Mode

Read-only hostile audit of the Gate 1 output artifacts after local plumbing-only execution.

No provider API access, no new data download, no market-row expansion, no diagnostics, no backtests, no forecasts, no positions, no costs, no carry, no trend, no volatility or risk calculations, no OOS, no Lockbox, no Forward, no CFD adapters, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update, and no remote operations were authorized or performed by the audit.

## Audited Output Artifacts

- `docs/researchops/source_native_futures_daily_data_library/16_SYMBOL_DATED_CONTRACT_FRAGMENT_DEV_RECON_TABLE/2026-05-30/CARVER_16_SYMBOL_DATED_CONTRACT_FRAGMENT_DEV_RECON_TABLE_2026-05-30.csv`
- `docs/researchops/source_native_futures_daily_data_library/16_SYMBOL_DATED_CONTRACT_FRAGMENT_DEV_RECON_TABLE/2026-05-30/CARVER_16_SYMBOL_DATED_CONTRACT_FRAGMENT_DEV_RECON_TABLE_STATUS_2026-05-30.csv`
- `docs/researchops/source_native_futures_daily_data_library/16_SYMBOL_DATED_CONTRACT_FRAGMENT_DEV_RECON_TABLE/2026-05-30/CARVER_16_SYMBOL_DATED_CONTRACT_FRAGMENT_DEV_RECON_TABLE_PROVENANCE_2026-05-30.md`
- `docs/researchops/source_native_futures_daily_data_library/16_SYMBOL_DATED_CONTRACT_FRAGMENT_DEV_RECON_TABLE/2026-05-30/CARVER_16_SYMBOL_DATED_CONTRACT_FRAGMENT_DEV_RECON_TABLE_SHA256SUMS_2026-05-30.txt`

## Output SHA256

```text
C18C1956A75B161B86132D3CCC43ADAED4D3D7950002DB7BD0E01D50AA5C5AC9  CARVER_16_SYMBOL_DATED_CONTRACT_FRAGMENT_DEV_RECON_TABLE_2026-05-30.csv
A81DA21AF8E6925478C6D7C2CFDC0119B56765AB4E82FB51C2294BBC8E0C6BB0  CARVER_16_SYMBOL_DATED_CONTRACT_FRAGMENT_DEV_RECON_TABLE_STATUS_2026-05-30.csv
8D43EC12F2FF244481B7A9EB5302F36A5D4AD9D99B5A0BCBBCFFAC8BC65E6066  CARVER_16_SYMBOL_DATED_CONTRACT_FRAGMENT_DEV_RECON_TABLE_PROVENANCE_2026-05-30.md
```

## Initial Audit Finding And Correction

An initial hostile audit found one blocking schema-label mismatch: the status CSV used semantic status-scope buckets instead of the schema-required literal `PLUMBING_ONLY`.

The status file was patched only to set every `status_scope` value to `PLUMBING_ONLY`, and the SHA256SUMS file was refreshed. No data rows, provider rows, market rows, strategy fields, or authorization boundaries were expanded.

## Re-Audit Findings

### Critical

None.

### High

None.

### Medium

None.

### Low

None.

## Verified Checks

- Input hashes in table rows and provenance match the preflight locked hashes.
- Output table preserves the exact schema contract and required fixed labels.
- Status CSV preserves exact columns: `status_key,status_value,status_scope`.
- Every status row has `status_scope=PLUMBING_ONLY`.
- Admitted normal provider-condition rows: `4483`.
- Excluded degraded provider-condition rows: `85`.
- Manifest symbols represented: `16`.
- Non-manifest rows: `0`.
- Continuous-contract rows: `0`.
- Duplicate `(provider_symbol, completed_trading_date)` rows: `0`.
- All non-authorization flags are preserved as `NO`.
- No strategy input, diagnostics, backtests, forecasts, positions, costs, carry, trend, volatility or risk calculations, OOS, Lockbox, Forward, CFD, old QuantLab active use, Git/remote operation, provider access, or new download authorization is present.

## Disposition

```text
BLOCKING_FINDINGS: NO
AUDIT_DISPOSITION: PASS_CARVER_16_SYMBOL_DATED_CONTRACT_FRAGMENT_DEV_RECON_TABLE_EXECUTION_PLUMBING_ONLY_SCOPE
```

## Boundary

This pass covers Gate 1 only: the dated-contract fragment Development/Reconciliation table for plumbing-only table-shape work.

It does not authorize Gate 2, continuous or rolled daily strategy series construction, strategy-facing input creation, diagnostics, backtests, forecasts, positions, costs, carry, trend, volatility or risk calculations, OOS, Lockbox, Forward, deployment, trading, promotion, Git operations, provider access, or additional data downloads.
