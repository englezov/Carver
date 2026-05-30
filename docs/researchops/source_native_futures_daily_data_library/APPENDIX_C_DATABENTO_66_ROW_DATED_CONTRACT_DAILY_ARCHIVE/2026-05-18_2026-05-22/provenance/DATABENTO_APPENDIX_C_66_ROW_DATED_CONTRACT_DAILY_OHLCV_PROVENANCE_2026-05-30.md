# Databento Appendix C 66-Row Dated Contract Daily OHLCV Quarantine Intake Provenance

Date: 2026-05-30
Run UTC: 2026-05-30T20:33:43Z

Status:

```text
PARTIAL_DATED_CONTRACT_DAILY_OHLCV_QUARANTINE_INTAKE_FAIL_CLOSED_FOR_INCOMPLETE_OR_CONDITION_ROWS
```

## Scope

Provider: Databento Historical
Datasets: GLBX.MDP3, XCBF.PITCH, XEUR.EOBI
Schema: `ohlcv-1d`
SType In: `instrument_id`
Request window: `2026-05-18T00:00:00Z` through `2026-05-23T00:00:00Z` exclusive
Completed UTC daily dates expected: 2026-05-18, 2026-05-19, 2026-05-20, 2026-05-21, 2026-05-22
Manifest rows: 66

## Source Manifest

Input hardening ledger:

```text
C:/Users/openclaw/Desktop/Carver/docs/researchops/contract_identity/databento_appendix_c_contract_identity_hardening_2026-05-30/ledger/CARVER_DATABENTO_APPENDIX_C_CONTRACT_IDENTITY_HARDENED_LEDGER_2026-05-30.csv
```

Eligible predicate:

```text
eligible_for_session_roll_provider_condition_data_intake_shape_gate == YES
```

## Output Root

```text
C:/Users/openclaw/Desktop/Carver/docs/researchops/source_native_futures_daily_data_library/APPENDIX_C_DATABENTO_66_ROW_DATED_CONTRACT_DAILY_ARCHIVE/2026-05-18_2026-05-22
```

## Result Counts

```text
EXPECTED_TOTAL_ROWS: 330
OBSERVED_SANITIZED_ROWS: 380
VALIDATION_PASS_ROWS: 54
VALIDATION_FAIL_CLOSED_ROWS: 12
REQUEST_ERRORS: 0
```

## Boundary

This is quarantine-only real-data intake. It is not a diagnostic, backtest, forecast, position-sizing run, cost run, carry run, trend run, volatility/risk calculation, OOS, Lockbox, Forward, deployment, trading, or promotion.

`ohlcv-1d` rows are Databento UTC daily aggregate bars and remain labeled as not exchange-session/settlement locked strategy inputs.
