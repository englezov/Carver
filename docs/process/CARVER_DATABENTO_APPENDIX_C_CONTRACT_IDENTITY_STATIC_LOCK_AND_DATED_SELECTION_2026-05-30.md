# Carver Databento Appendix C Contract Identity Static Lock And Dated Selection

Date: 2026-05-30

Status:

```text
PROCESS_SOURCE_DATABENTO_APPENDIX_C_CONTRACT_IDENTITY_STATIC_LOCK_AND_DATED_SELECTION_PRE_OHLCV_NOT_STRATEGY
```

## Purpose

Execute the next static gate after the Databento Appendix C provider coverage and alias mapping patch.

This gate consumes the 69 post-alias Databento static provider candidates, preserves the remaining Appendix C rows fail-closed, resolves Databento continuous symbols to current dated instrument IDs using metadata/symbology only, and records static contract identity status before any OHLCV intake.

## Inputs

- `docs/researchops/provider_mappings/CARVER_APPENDIX_C_DATABENTO_PROVIDER_COVERAGE_AFTER_ALIAS_PATCH_2026-05-30.csv`
- `docs/researchops/portfolios/CARVER_APPENDIX_C_JUMBO_UNIVERSE_LOCK_2026-05-29.csv`
- Databento `symbology.resolve` metadata only.
- Databento `definition` schema metadata only.

## Provider Metadata Window

```text
PROVIDER_METADATA_SAFE_WINDOW_START: 2026-05-27
PROVIDER_METADATA_SAFE_WINDOW_END: 2026-05-29
AS_OF_LABEL: 2026-05-30
```

The safe window is used because metadata requests beyond the live-license boundary can fail for some datasets after `2026-05-29T22:00:00Z`. This gate uses the same pre-real-data metadata posture as the prior coverage probe and does not request OHLCV rows.

Databento emitted a reduced-quality warning for `2026-05-27` during definition metadata retrieval. The warning is preserved as provider-metadata context. It does not convert any row to strategy use, and no OHLCV bars were requested.

## Result

```text
APPENDIX_C_ROWS: 102
POST_ALIAS_STATIC_PROVIDER_CANDIDATES_ATTEMPTED: 69
DATED_CONTRACT_SELECTED_FROM_DATABENTO_CONTINUOUS_METADATA: 69
STATIC_CONTRACT_IDENTITY_AND_DATED_CONTRACT_SELECTED_NOT_MARKET_READY: 35
STATIC_DATED_CONTRACT_SELECTED_BUT_CONTRACT_IDENTITY_REQUIRES_REVIEW_OR_FAIL_CLOSED: 34
PRESERVED_FAIL_CLOSED_NOT_IN_69_DATABENTO_STATIC_PROVIDER_CANDIDATES: 33
DEFINITION_METADATA_REQUEST_ERRORS: 0
MARKET_ROW_ACCESS: NO
OHLCV_DOWNLOAD_AUTHORIZED: NO
STRATEGY_USE: NO
```

The 35 static-lock rows are not data-ready. They may advance only to session/roll/provider-condition/data-intake shape gates.

The 34 selected-but-review rows have a dated Databento contract selection, but at least one static identity field remains unresolved or conflicted, including exchange normalization, currency normalization, multiplier/point-value semantics, active/listed field completeness, or roll-boundary ambiguity.

The 33 non-candidate rows remain fail-closed from the post-alias provider coverage patch.

## Machine-Readable Outputs

Primary ledger:

```text
docs/researchops/contract_identity/databento_appendix_c_contract_identity_static_lock_2026-05-30/ledger/CARVER_DATABENTO_APPENDIX_C_CONTRACT_IDENTITY_STATIC_LOCK_AND_DATED_SELECTION_LEDGER_2026-05-30.csv
```

Status:

```text
docs/researchops/contract_identity/databento_appendix_c_contract_identity_static_lock_2026-05-30/provenance/CARVER_DATABENTO_APPENDIX_C_CONTRACT_IDENTITY_STATIC_LOCK_AND_DATED_SELECTION_STATUS_2026-05-30.csv
```

Raw provider metadata:

```text
docs/researchops/contract_identity/databento_appendix_c_contract_identity_static_lock_2026-05-30/raw_provider_metadata/
docs/researchops/contract_identity/databento_appendix_c_contract_identity_static_lock_2026-05-30/definition_metadata/
```

These provider files are metadata/reference artifacts only, not OHLCV bars and not strategy inputs.

## Locked Interpretations

```text
DATABENTO_CONTINUOUS_SYMBOL_RESOLUTION = STATIC_DATED_CONTRACT_SELECTION_EVIDENCE
DATABENTO_DEFINITION_SCHEMA = STATIC_PROVIDER_CONTRACT_IDENTITY_EVIDENCE
DATED_CONTRACT_SELECTED != MARKET_DATA_READY
CONTRACT_IDENTITY_STATIC_LOCK != SESSION_ROLL_READY
CONTRACT_IDENTITY_STATIC_LOCK != STRATEGY_READY
```

## Next Gates

Rows marked:

```text
STATIC_CONTRACT_IDENTITY_AND_DATED_CONTRACT_SELECTED_NOT_MARKET_READY
```

may advance only to:

```text
SESSION_ROLL_PROVIDER_CONDITION_AND_DATA_INTAKE_SHAPE_GATE_BEFORE_OHLCV
```

Rows marked:

```text
STATIC_DATED_CONTRACT_SELECTED_BUT_CONTRACT_IDENTITY_REQUIRES_REVIEW_OR_FAIL_CLOSED
```

must go through:

```text
CONTRACT_IDENTITY_REVIEW_OR_PRODUCT_SPEC_RECONCILIATION_BEFORE_OHLCV
```

Rows marked:

```text
PRESERVED_FAIL_CLOSED_NOT_IN_69_DATABENTO_STATIC_PROVIDER_CANDIDATES
```

remain closed unless a separate provider coverage, alias normalization, or static source evidence gate changes their status.

## Non-Authorization

This gate authorizes no OHLCV download, no market-row parsing, no diagnostics, no backtests, no forecasts, no positions, no costs, no carry, no trend, no risk calculations, no OOS, no Lockbox, no Forward, no CFD adapters, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git operations, and no remote repository operations.
