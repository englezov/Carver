# Carver Databento Appendix C Provider Coverage After Alias Patch Decision

Date: 2026-05-30

Status:

```text
PROCESS_SOURCE_DATABENTO_APPENDIX_C_PROVIDER_COVERAGE_AFTER_ALIAS_PATCH_PRE_REAL_DATA_NOT_OHLCV_NOT_STRATEGY
```

## Purpose

Close the follow-through from the Databento Appendix C coverage probe and alias mapping evidence gate. This decision creates one post-alias provider coverage view for the 102-row Appendix C universe.

This is not a market-data gate. It authorizes no OHLCV download, no market-row parsing, no diagnostics, no backtests, no forecasts, no positions, no costs, no carry, no trend, no risk calculations, no OOS, no Lockbox, no Forward, no CFD adapter work, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git operations, and no remote repository operations.

## Inputs

- `docs/researchops/provider_mappings/CARVER_APPENDIX_C_DATABENTO_PROVIDER_COVERAGE_PATCH_2026-05-30.csv`
- `docs/researchops/provider_mappings/CARVER_APPENDIX_C_DATABENTO_ALIAS_MAPPING_EVIDENCE_LEDGER_2026-05-30.csv`
- `docs/process/CARVER_DATABENTO_APPENDIX_C_ALIAS_MAPPING_EVIDENCE_GATE_2026-05-30.md`

## Post-Alias Coverage Score

```text
APPENDIX_C_ROWS: 102
DATABENTO_EXACT_METADATA_CANDIDATE_NOT_DATA_READY: 53
DATABENTO_ALIAS_STATIC_MAPPING_RESOLVED_NOT_DATA_READY: 16
DATABENTO_ALIAS_FAIL_CLOSED_CURRENCY_VENUE_NORMALIZATION_REQUIRED: 1
DATABENTO_NO_COVERAGE_CANDIDATE_FAIL_CLOSED: 32
```

Interpretation:

```text
DATABENTO_STATIC_PROVIDER_CANDIDATES_AFTER_ALIAS_PATCH: 69
STILL_FAIL_CLOSED_OR_UNRESOLVED: 33
```

Compared with the prior NinjaTrader static position:

```text
NINJATRADER_MAPPED_OR_REVIEW_REQUIRED_ROWS: 41
DATABENTO_STATIC_PROVIDER_CANDIDATES_AFTER_ALIAS_PATCH: 69
NET_STATIC_COVERAGE_GAIN: 28
```

## Alias-Specific Decision

Sixteen alias rows are now allowed to advance to a Databento contract identity/static dated-contract selection gate, but remain not data-ready.

One alias row remains fail-closed:

```text
APPENDIX_C_175_004: SMI -> FSMI.c.0
BLOCKER: APPENDIX_C_CURRENCY_EUR_CONFLICTS_WITH_OFFICIAL_CHF_AND_SOURCE_EXCHANGE_SOFFEX_NEEDS_EUREX_SIX_NORMALIZATION
```

One alias candidate is corrected:

```text
APPENDIX_C_175_005: DJ200S
PRIOR_UNSAFE_CANDIDATE: FXXS.c.0
CORRECTED_STATIC_ALIAS_CANDIDATE: FSCP.c.0
```

`FXXS.c.0` is not allowed for the `DJ200S` row.

## Machine-Readable Rollup

```text
docs/researchops/provider_mappings/CARVER_APPENDIX_C_DATABENTO_PROVIDER_COVERAGE_AFTER_ALIAS_PATCH_2026-05-30.csv
```

This ledger is the current clean provider-coverage view to use before the next static contract identity gate.

## Next Clean Gate

```text
DATABENTO_APPENDIX_C_CONTRACT_IDENTITY_STATIC_LOCK_AND_DATED_CONTRACT_SELECTION_GATE
```

That gate should consume the 69 Databento static provider candidates and preserve the 33 fail-closed/unresolved rows. The `SMI/FSMI` row must either pass a dedicated currency/venue normalization gate or remain closed.

## Non-Authorization

This decision is process/source only. It authorizes no OHLCV download, no market-row parsing, no diagnostics, no backtests, no forecasts, no positions, no costs, no carry, no trend, no risk calculations, no OOS, no Lockbox, no Forward, no CFD adapters, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git operations, and no remote repository operations.
