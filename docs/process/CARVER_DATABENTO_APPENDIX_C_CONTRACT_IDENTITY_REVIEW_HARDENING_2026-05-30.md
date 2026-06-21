# Carver Databento Appendix C Contract Identity Review Hardening

Date: 2026-05-30

Status:

```text
PROCESS_SOURCE_DATABENTO_APPENDIX_C_CONTRACT_IDENTITY_REVIEW_HARDENING_PRE_OHLCV_NOT_STRATEGY
```

## Purpose

Resolve or fail-close the 34 Databento Appendix C rows that had a dated-contract selection but remained contract-identity review-required after the static lock gate.

The hardening rule is conservative: keep as many source-native contracts as static evidence supports, but do not carry forward rows where the provider candidate points to a different venue, currency, family, or variant.

## Inputs

- `docs/researchops/contract_identity/databento_appendix_c_contract_identity_static_lock_2026-05-30/ledger/CARVER_DATABENTO_APPENDIX_C_CONTRACT_IDENTITY_STATIC_LOCK_AND_DATED_SELECTION_LEDGER_2026-05-30.csv`
- Databento metadata/symbology only.
- Databento `definition` reference metadata only.
- Existing Appendix C universe lock.
- Existing official static alias evidence where already recorded.

## Result

```text
APPENDIX_C_ROWS: 102
PRE_HARDENING_STATIC_READY_ROWS: 35
PRE_HARDENING_REVIEW_ROWS: 34
REVIEW_ROWS_HARDENED_TO_STATIC_READY: 31
REVIEW_ROWS_FAIL_CLOSED_AFTER_HARDENING: 3
FINAL_STATIC_IDENTITY_READY_ROWS: 66
PRESERVED_NON_CANDIDATE_FAIL_CLOSED_ROWS: 33
FINAL_TOTAL_FAIL_CLOSED_OR_NOT_READY_ROWS: 36
MARKET_ROW_ACCESS: NO
OHLCV_DOWNLOAD_AUTHORIZED: NO
STRATEGY_USE: NO
```

## Corrections Preserved

The following prior provider candidates were corrected with static Databento metadata/definition evidence:

| Row | Prior Issue | Hardened Candidate |
|---|---|---|
| `APPENDIX_C_173_004` / `GBL` | Bad `GBL.c.0` IFLL/ICE-style candidate | `FGBL.c.0` Eurex Bund |
| `APPENDIX_C_175_003` / `DAX` | Bad `DAX.c.0` GLBX energy-style candidate | `FDXS.c.0` Micro-DAX, matching Appendix multiplier 1 |
| `APPENDIX_C_179_001` / `AUD` | Bad `AUD.c.0` IFUS candidate | `6A.c.0` CME Australian Dollar |
| `APPENDIX_C_179_002` / `CAD` | Bad `CAD.c.0` IFUS candidate | `6C.c.0` CME Canadian Dollar |
| `APPENDIX_C_179_005` / `GBP` | Bad `GBP.c.0` IFLL candidate | `6B.c.0` CME British Pound |
| `APPENDIX_C_180_006` / `MXP` | Provider `MXP.c.0` did not match Appendix multiplier semantics | `6M.c.0` CME Mexican Peso |
| `APPENDIX_C_181_007` / `SI` | Full-size `SI.c.0` mismatched Appendix multiplier 1000 | `SIL.c.0` Micro Silver |

## Fail-Closed Rows

The following rows remain closed after hardening:

| Row | Reason |
|---|---|
| `APPENDIX_C_177_012` / `TWN` | Provider definition points to IFLO/GBX, not SGX/USD FTSE Taiwan. |
| `APPENDIX_C_180_004` / `UC` | Provider definition points to IFLO/EUR, not SGX/CNH USD/CNH. |
| `APPENDIX_C_181_004` / `SCI` | Provider definition points to IFLO/NOK, not SGX/USD iron ore. |

No row is silently dropped, substituted, or reweighted.

## Machine-Readable Output

```text
docs/researchops/contract_identity/databento_appendix_c_contract_identity_hardening_2026-05-30/ledger/CARVER_DATABENTO_APPENDIX_C_CONTRACT_IDENTITY_HARDENED_LEDGER_2026-05-30.csv
```

## Next Gate

The 66 rows marked:

```text
HARDENED_STATIC_CONTRACT_IDENTITY_AND_DATED_CONTRACT_SELECTED_NOT_MARKET_READY
```

may be consumed by:

```text
DATABENTO_APPENDIX_C_SESSION_ROLL_PROVIDER_CONDITION_DATA_INTAKE_SHAPE_GATE
```

That shape gate still must not download OHLCV by itself.

## Non-Authorization

This hardening gate authorizes no OHLCV download, no market-row parsing, no diagnostics, no backtests, no forecasts, no positions, no costs, no carry, no trend, no risk calculations, no OOS, no Lockbox, no Forward, no CFD adapters, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git operations, and no remote repository operations.
