# Carver Databento Appendix C Alias Mapping Evidence Gate

Date: 2026-05-30

Status:

```text
PASS_ALIAS_MAPPING_EVIDENCE_PRE_REAL_DATA_WITH_ONE_FAIL_CLOSED_ROW
```

## Purpose

Resolve or fail-close the 17 Appendix C rows that Databento metadata/symbology identified as alias-required coverage candidates. This is a source-native static-evidence gate only. It does not authorize market-row intake.

## Inputs

- Appendix C 102-row machine-readable universe lock.
- Databento Appendix C coverage probe ledger.
- Databento provider coverage patch.
- Official static exchange/provider contract specification evidence.

## Result

```text
INPUT_ALIAS_ROWS: 17
ALIAS_EQUIVALENCE_RESOLVED_STATIC_PRE_REAL_DATA: 16
ALIAS_PRODUCT_FAMILY_IDENTIFIED_BUT_FAIL_CLOSED: 1
CORRECTED_CANDIDATE_ROWS: 1
MARKET_ROW_ACCESS: NO
OHLCV_DOWNLOAD_AUTHORIZED: NO
```

The machine-readable evidence ledger is:

```text
docs/researchops/provider_mappings/CARVER_APPENDIX_C_DATABENTO_ALIAS_MAPPING_EVIDENCE_LEDGER_2026-05-30.csv
```

## Corrected Candidate

`APPENDIX_C_175_005` (`DJ200S`, EU DJ Small cap 200) is corrected:

```text
PRIOR_UNSAFE_CANDIDATE: FXXS.c.0
LOCKED_STATIC_ALIAS_CANDIDATE: FSCP.c.0
```

Official Eurex evidence identifies `FSCP` as STOXX Europe Small 200 Index Futures. The prior `FXXS.c.0` candidate is superseded and may not be used for this row.

## Fail-Closed Row

`APPENDIX_C_175_004` (`SMI -> FSMI.c.0`) remains fail-closed:

```text
PRODUCT_FAMILY_IDENTIFIED: YES
FULL_ALIAS_LOCK: NO
BLOCKER: APPENDIX_C_CURRENCY_EUR_CONFLICTS_WITH_OFFICIAL_CHF_AND_SOURCE_EXCHANGE_SOFFEX_NEEDS_EUREX_SIX_NORMALIZATION
```

This is not a rejection of `FSMI` as the SMI futures product family. It is a refusal to silently normalize venue and currency semantics before a dedicated contract identity/currency normalization step.

## Next Gate

The clean next step is:

```text
DATABENTO_APPENDIX_C_CONTRACT_IDENTITY_STATIC_LOCK_AND_DATED_CONTRACT_SELECTION_GATE
```

That gate may consume the 16 static alias-resolved rows and must keep the SMI row fail-closed unless the currency/venue normalization conflict is explicitly resolved.

## Non-Authorization

No OHLCV download, no market-row parsing, no diagnostics, no backtests, no forecasts, no positions, no costs, no carry, no trend, no risk calculations, no OOS, no Lockbox, no Forward, no CFD adapters, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git operations, and no remote repository operations are authorized.
