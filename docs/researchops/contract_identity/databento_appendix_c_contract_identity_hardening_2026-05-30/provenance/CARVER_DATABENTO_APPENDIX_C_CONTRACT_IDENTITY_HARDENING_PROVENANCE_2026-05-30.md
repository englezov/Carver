# Carver Databento Appendix C Contract Identity Hardening Provenance

Date: 2026-05-30

Status:

```text
DATABENTO_STATIC_CONTRACT_IDENTITY_HARDENING_PRE_OHLCV
```

## Scope

This record covers the hardening pass for the 34 Databento selected-but-review-required Appendix C rows.

It used current Carver static artifacts, Databento metadata/symbology, Databento `definition` reference metadata, and previously recorded official static alias evidence.

No OHLCV request, market-row parsing, diagnostic, backtest, forecast, position, cost, carry, trend, risk calculation, OOS, Lockbox, Forward, CFD adapter, old QuantLab pipeline, tuning, deployment, trading, promotion, Git operation, or remote repository operation was performed.

## Outputs

```text
docs/researchops/contract_identity/databento_appendix_c_contract_identity_hardening_2026-05-30/ledger/CARVER_DATABENTO_APPENDIX_C_CONTRACT_IDENTITY_HARDENED_LEDGER_2026-05-30.csv
docs/researchops/contract_identity/databento_appendix_c_contract_identity_hardening_2026-05-30/provenance/CARVER_DATABENTO_APPENDIX_C_CONTRACT_IDENTITY_HARDENING_STATUS_2026-05-30.csv
```

## Result

```text
APPENDIX_C_ROWS: 102
STATIC_READY_AFTER_HARDENING: 66
HARDENING_FAIL_CLOSED: 3
PRESERVED_NON_CANDIDATE_FAIL_CLOSED: 33
```

## Boundary

The 66 static-ready rows are not market-data-ready and not strategy-ready. They are eligible only for the next process-only session/roll/provider-condition/data-intake shape gate.
