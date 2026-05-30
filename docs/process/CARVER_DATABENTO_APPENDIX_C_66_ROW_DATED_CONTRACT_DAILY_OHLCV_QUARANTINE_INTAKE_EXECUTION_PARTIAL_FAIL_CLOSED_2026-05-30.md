# Carver Databento Appendix C 66-Row Dated Contract Daily OHLCV Quarantine Intake Execution

Date: 2026-05-30

Status:

```text
PARTIAL_DATED_CONTRACT_DAILY_OHLCV_QUARANTINE_INTAKE_FAIL_CLOSED_FOR_INCOMPLETE_OR_CONDITION_ROWS
```

## Scope

Executed one bounded Databento Historical `ohlcv-1d` quarantine intake for the 66 Appendix C rows that passed Databento static contract-identity hardening.

Request:

```text
provider: DATABENTO
schema: ohlcv-1d
stype_in: instrument_id
request_start_utc: 2026-05-18T00:00:00Z
request_end_utc_exclusive: 2026-05-23T00:00:00Z
completed_utc_dates: 2026-05-18 through 2026-05-22
```

No continuous contracts were requested as market data. Databento continuous symbols remained selection/provenance evidence only.

## Input Manifest

Input hardening ledger:

```text
docs/researchops/contract_identity/databento_appendix_c_contract_identity_hardening_2026-05-30/ledger/CARVER_DATABENTO_APPENDIX_C_CONTRACT_IDENTITY_HARDENED_LEDGER_2026-05-30.csv
```

Eligible predicate:

```text
eligible_for_session_roll_provider_condition_data_intake_shape_gate == YES
```

Manifest count:

```text
66
```

Dataset split:

```text
GLBX.MDP3: 52
XEUR.EOBI: 13
XCBF.PITCH: 1
```

## Output Root

```text
docs/researchops/source_native_futures_daily_data_library/APPENDIX_C_DATABENTO_66_ROW_DATED_CONTRACT_DAILY_ARCHIVE/2026-05-18_2026-05-22
```

Key artifacts:

```text
request_manifest/CARVER_DATABENTO_APPENDIX_C_66_ROW_DATED_CONTRACT_DAILY_OHLCV_REQUEST_MANIFEST_2026-05-30.csv
request_manifest/CARVER_DATABENTO_APPENDIX_C_66_ROW_DATED_CONTRACT_DAILY_OHLCV_REQUEST_2026-05-30.json
raw_provider_output/databento_GLBX-MDP3_ohlcv-1d_appendix_c_66_row_subset_2026-05-18_2026-05-23.dbn
raw_provider_output/databento_XEUR-EOBI_ohlcv-1d_appendix_c_66_row_subset_2026-05-18_2026-05-23.dbn
raw_provider_output/databento_XCBF-PITCH_ohlcv-1d_appendix_c_66_row_subset_2026-05-18_2026-05-23.dbn
raw_provider_output/databento_ALL_DATASETS_ohlcv-1d_appendix_c_66_row_subset_2026-05-18_2026-05-23_provider_combined.csv
provider_condition_metadata/DATABENTO_APPENDIX_C_66_ROW_PROVIDER_CONDITION_LEDGER_2026-05-18_2026-05-23.csv
sanitized_bars/DATABENTO_APPENDIX_C_66_ROW_DATED_CONTRACT_DAILY_OHLCV_2026-05-18_2026-05-22_SANITIZED_QUARANTINE_ONLY.csv
validation/DATABENTO_APPENDIX_C_66_ROW_DATED_CONTRACT_DAILY_OHLCV_2026-05-18_2026-05-22_ROW_VALIDATION.csv
provenance/DATABENTO_APPENDIX_C_66_ROW_DATED_CONTRACT_DAILY_OHLCV_INTAKE_STATUS_2026-05-30.csv
provenance/DATABENTO_APPENDIX_C_66_ROW_DATED_CONTRACT_DAILY_OHLCV_PROVENANCE_2026-05-30.md
provenance/DATABENTO_APPENDIX_C_66_ROW_DATED_CONTRACT_DAILY_OHLCV_SHA256SUMS_2026-05-30.txt
```

## Result

```text
EXPECTED_TOTAL_ROWS: 330
OBSERVED_SANITIZED_ROWS: 380
REQUEST_ERRORS: 0
VALIDATION_PASS_ROWS: 54
VALIDATION_FAIL_CLOSED_ROWS: 12
```

Pass status means exactly one Databento UTC daily `ohlcv-1d` row existed for each of the five expected dates and provider condition metadata joined as available.

Fail-closed status means the row remains quarantined and cannot be used as a strategy input without a later policy/evidence gate.

## Fail-Closed Rows

```text
APPENDIX_C_173_001 OAT    duplicate XEUR.EOBI rows for all five dates
APPENDIX_C_173_002 GBS    duplicate XEUR.EOBI rows for all five dates
APPENDIX_C_173_003 GBM    duplicate XEUR.EOBI rows for all five dates
APPENDIX_C_173_004 GBL    duplicate XEUR.EOBI rows for all five dates
APPENDIX_C_173_005 GBX    duplicate XEUR.EOBI rows for all five dates
APPENDIX_C_173_006 BTS    duplicate XEUR.EOBI rows for all five dates
APPENDIX_C_173_007 BTP    duplicate XEUR.EOBI rows for all five dates
APPENDIX_C_175_005 DJ200S duplicate XEUR.EOBI rows on 2026-05-18 and 2026-05-21
APPENDIX_C_175_007 DJ600  duplicate XEUR.EOBI rows for all five dates
APPENDIX_C_175_008 ESTX50 duplicate XEUR.EOBI rows for all five dates
APPENDIX_C_178_001 VIX    duplicate XCBF.PITCH rows for all five dates
APPENDIX_C_181_001 ALI    missing GLBX.MDP3 rows on 2026-05-20 and 2026-05-21
```

The duplicate rows are not silently collapsed. XEUR.EOBI and XCBF.PITCH require an explicit source-native publisher/deduplication policy before those rows can be admitted.

ALI requires a stale/missing-row policy or alternate static/data evidence before admission.

## Admitted Quarantine Rows

The 54 passing rows are admitted only at quarantine scope:

```text
PASS_ROW_DATE_SHAPE_PROVIDER_CONDITION_QUARANTINE_ONLY
```

They are not strategy inputs, not backtest-ready, not forecast-ready, not roll-ready, and not promotion-ready.

## Timestamp And Price Semantics

Databento `ohlcv-1d` rows are UTC daily aggregate bars. They are not yet locked as exchange-session completed trading days or official settlement data.

The sanitized archive labels this boundary through:

```text
strategy_use_status = NOT_STRATEGY_INPUT_NOT_BACKTEST_READY
```

## Non-Authorization

This execution authorizes no diagnostics, backtests, forecasts, positions, costs, carry, trend, volatility/risk calculations, OOS, Lockbox, Forward, CFD adapters, old QuantLab active-pipeline use, tuning, deployment, trading, promotion, Git staging, commit, push, PR update/opening, or remote repository operations.
