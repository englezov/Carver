# Carver Databento Appendix C Contract Identity Static Lock And Dated Selection Provenance

Date: 2026-05-30

Status:

```text
DATABENTO_METADATA_ONLY_CONTRACT_IDENTITY_AND_DATED_SELECTION_PRE_OHLCV
```

## Scope

This provenance record covers the metadata-only Databento contract identity and dated-contract selection execution for the Appendix C post-alias provider candidates.

The gate used:

- Databento `symbology.resolve` with `stype_in=continuous` and `stype_out=instrument_id`.
- Databento `definition` schema for the selected instrument IDs.

It did not use:

- OHLCV schemas.
- Trade, MBP, MBO, statistics, or market-row schemas.
- Strategy computations.
- Diagnostics or backtests.

## Source Inputs

```text
docs/researchops/provider_mappings/CARVER_APPENDIX_C_DATABENTO_PROVIDER_COVERAGE_AFTER_ALIAS_PATCH_2026-05-30.csv
docs/researchops/portfolios/CARVER_APPENDIX_C_JUMBO_UNIVERSE_LOCK_2026-05-29.csv
```

## Metadata Requests

```text
DATASETS: GLBX.MDP3, XEUR.EOBI, XCBF.PITCH, IFLL.IMPACT, IFUS.IMPACT
SYMBOL SURFACE: Databento continuous symbols only
SYMBOL RESOLUTION: continuous -> instrument_id
REFERENCE SCHEMA: definition
SAFE WINDOW: 2026-05-27 to 2026-05-29
```

Raw metadata is preserved under:

```text
docs/researchops/contract_identity/databento_appendix_c_contract_identity_static_lock_2026-05-30/raw_provider_metadata/
docs/researchops/contract_identity/databento_appendix_c_contract_identity_static_lock_2026-05-30/definition_metadata/
```

## Result Summary

```text
APPENDIX_C_ROWS_PRESERVED: 102
POST_ALIAS_STATIC_PROVIDER_CANDIDATES_ATTEMPTED: 69
DATED_CONTRACT_SELECTIONS_CREATED: 69
STATIC_IDENTITY_LOCK_SCOPE_PASS_NOT_MARKET_READY: 35
STATIC_IDENTITY_REVIEW_OR_FAIL_CLOSED: 34
PRESERVED_FAIL_CLOSED_NON_CANDIDATES: 33
DEFINITION_METADATA_REQUEST_ERRORS: 0
```

## Important Boundary

The 35 rows marked static-lock at this scope are not production contract identity locks and not market-data readiness. They are provider-definition and dated-contract-selection locks only.

The 34 review rows are intentionally not promoted. They require product-spec or normalization review before OHLCV.

## Non-Authorization

No OHLCV download, market-row parsing, diagnostics, backtests, forecasts, positions, costs, carry, trend, risk calculations, OOS, Lockbox, Forward, CFD adapters, old QuantLab active-pipeline use, tuning, deployment, trading, promotion, Git operations, or remote repository operations are authorized.
