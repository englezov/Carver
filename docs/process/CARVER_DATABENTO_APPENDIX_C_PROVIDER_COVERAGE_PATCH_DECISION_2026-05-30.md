# Carver Databento Appendix C Provider Coverage Patch Decision

Date: 2026-05-30

Status:

```text
PROCESS_SOURCE_CARVER_DATABENTO_APPENDIX_C_PROVIDER_COVERAGE_PATCH_PRE_REAL_DATA_NOT_OHLCV_NOT_STRATEGY
```

## Purpose

Patch the Appendix C provider-coverage interpretation after the Databento metadata/symbology coverage probe. This record converts the coverage probe into pre-real-data row status and next gates. It does not authorize OHLCV download, market-row parsing, diagnostics, backtests, forecasts, positions, costs, carry, trend, risk calculations, OOS, Lockbox, Forward, CFD adapter work, old QuantLab active-pipeline use, tuning, deployment, trading, promotion, Git, or remote operations.

## Source Inputs

| Artifact | SHA256 |
|---|---|
| Appendix C universe lock | `9453A9635148AE4D998306E0AC921C534D35D4D97DDE3934C8AEA02104E48C5F` |
| NinjaTrader provider mapping | `80C7F52FE599318FE6E095C7F6105B6B9646FC2F35DC1CCF821BCC2AFE3586CE` |
| Databento coverage ledger | `A12C83CE0735B3744E62A8EF8F3DCBA30A5130F2A0A3B18B5862F92E99FF19C3` |

## Patch Result

| Category | Count | Meaning |
|---|---:|---|
| Databento exact metadata candidates | 53 | Candidate coverage exists, but each row still requires Databento contract identity, dated-contract selection, lifecycle, provider-condition, and data-readiness gates before any OHLCV intake. |
| Databento alias metadata candidates | 17 | Candidate coverage exists only through an alias. Alias is fail-closed until a source/provider mapping gate proves equivalence. |
| Databento blocked/unresolved | 32 | No usable metadata candidate was found in this probe. |
| NinjaTrader blocked rows recovered by exact Databento candidate | 16 | Rows previously blocked/variant in NinjaTrader that now have exact Databento metadata candidates. |
| NinjaTrader blocked rows partially recovered by Databento alias candidate | 17 | Rows previously blocked/variant in NinjaTrader that now have alias candidates but remain fail-closed. |

## Locked Interpretation

```text
DATABENTO_METADATA_COVERAGE != DATA_READY
DATABENTO_CONTINUOUS_SYMBOLOGY != CONTINUOUS_SOURCE_AUTHORITY
DATABENTO_ALIAS_MATCH != SOURCE_MAPPING_LOCK
DATABENTO_EXACT_METADATA_MATCH != DATED_CONTRACT_LOCK
```

Exact candidates may advance only to a static Databento contract identity / dated-contract readiness gate. Alias candidates may advance only to a source-native alias mapping evidence gate. Blocked rows remain blocked unless a separate provider/source evidence gate changes their status.

## Machine-Readable Patch

```text
docs/researchops/provider_mappings/CARVER_APPENDIX_C_DATABENTO_PROVIDER_COVERAGE_PATCH_2026-05-30.csv
SHA256: 9EB9F93D2C553F102CDE26EF64259F2901042A1CEBDD79B4A246F3765515686E
```

## Next Efficient Gates

1. Run a Databento exact-candidate contract identity/static definition gate for exact metadata candidates that matter to the next portfolio scope.
2. Run a separate alias mapping gate only for high-value alias candidates. No alias row should enter data intake before equivalence is source-locked.
3. Keep blocked/unresolved rows out of real-data intake.
4. Only after provider mapping, contract identity, lifecycle, session/timestamp, provider-condition, and roll rules are locked should OHLCV intake open.

## Non-Authorization

This patch authorizes no OHLCV download, no market-row parsing, no diagnostics, no backtests, no forecasts, no positions, no costs, no carry, no trend, no risk calculations, no OOS, no Lockbox, no Forward, no CFD adapters, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git operations, and no remote repository operations.
