# Carver Databento Appendix C Alias Mapping Evidence Provenance

Date: 2026-05-30

Status:

```text
PROCESS_SOURCE_ALIAS_MAPPING_EVIDENCE_PRE_REAL_DATA_NOT_OHLCV_AUTHORIZATION
```

## Scope

This record preserves the static evidence used to resolve or fail-close the 17 Appendix C rows previously classified as `DATABENTO_ALIAS_REQUIRED_METADATA_MATCH`.

Inputs:

- `docs/researchops/portfolios/CARVER_APPENDIX_C_JUMBO_UNIVERSE_LOCK_2026-05-29.csv`
- `docs/researchops/provider_mappings/CARVER_APPENDIX_C_DATABENTO_PROVIDER_COVERAGE_PATCH_2026-05-30.csv`
- `docs/researchops/source_native_futures_daily_data_library/databento_appendix_c_coverage_probe/2026-05-30/coverage_ledger/CARVER_DATABENTO_APPENDIX_C_COVERAGE_LEDGER_2026-05-30.csv`

Outputs:

- `docs/researchops/provider_mappings/CARVER_APPENDIX_C_DATABENTO_ALIAS_MAPPING_EVIDENCE_LEDGER_2026-05-30.csv`
- `docs/researchops/source_native_futures_daily_data_library/databento_appendix_c_coverage_probe/2026-05-30/provenance/CARVER_DATABENTO_APPENDIX_C_ALIAS_MAPPING_EVIDENCE_STATUS_2026-05-30.csv`

## Static Evidence Sources

Official static sources used:

- Eurex fixed-income futures contract specification page and current Eurex contract specification PDF for `FOAT`, `FGBS`, `FGBM`, `FGBX`, `FBTS`, and `FBTP`.
- Eurex SMI page and current Eurex contract specification PDF for `FSMI`.
- Eurex STOXX Europe 600 product pages and current Eurex contract specification PDF for `FXXP`, `FSCP`, and `FESX`.
- Eurex VSTOXX futures page for `FVS`.
- Cboe VIX futures contract specification page for `VX`.
- CME FX futures contract specification/product pages for `6S`, `6E`, `6J`, and `6N`.
- CME Ether futures contract specification/product pages for `ETH`.

Databento metadata/symbology evidence:

- Existing Databento coverage probe classified all 17 rows as metadata alias candidates.
- A metadata/symbology check confirmed `FSCP.c.0` is available in `XEUR.EOBI`; this supersedes the prior unsafe `DJ200S -> FXXS.c.0` candidate.

## Results

```text
ALIAS_EQUIVALENCE_RESOLVED_STATIC_PRE_REAL_DATA: 16
ALIAS_PRODUCT_FAMILY_IDENTIFIED_BUT_FAIL_CLOSED_CURRENCY_AND_VENUE_NORMALIZATION_REQUIRED: 1
CORRECTED_DATABENTO_CANDIDATE_ROWS: 1
MARKET_ROW_ACCESS: NO
OHLCV_DOWNLOAD_AUTHORIZED: NO
STRATEGY_USE: NO
```

The one fail-closed row is `APPENDIX_C_175_004` (`SMI -> FSMI.c.0`). The product family is identified, but the Appendix C lock records `SOFFEX` and `EUR`, while official static evidence for SMI futures points to a Eurex/SIX Swiss index derivative with CHF point-value semantics. It must go through a currency/venue normalization review before any market-row intake.

`APPENDIX_C_175_005` (`DJ200S`) is corrected from the prior Databento candidate `FXXS.c.0` to `FSCP.c.0`. `FXXS.c.0` is not allowed for this row.

## Non-Authorization

This gate authorizes no OHLCV download, no market-row parsing, no diagnostics, no backtests, no forecasts, no positions, no costs, no carry, no trend, no risk calculations, no OOS, no Lockbox, no Forward, no CFD adapter work, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, and no Git or remote repository operations.
