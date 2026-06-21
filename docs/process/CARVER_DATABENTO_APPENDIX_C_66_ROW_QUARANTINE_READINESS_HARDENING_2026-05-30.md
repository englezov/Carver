# Carver Databento Appendix C 66-Row Quarantine Readiness Hardening

Date: 2026-05-30

Status:

```text
PASS_POLICY_HARDENING_65_DEV_RECON_READY_1_FAIL_CLOSED_NOT_STRATEGY_READY
```

## Purpose

Harden the partial Databento Appendix C 66-row OHLCV quarantine intake into a clean Development/Reconciliation data-readiness set.

This pass resolves or fail-closes the 12 rows that failed the first row/date validation, while preserving the 54 rows that already passed.

## Inputs

Original execution record:

```text
docs/process/CARVER_DATABENTO_APPENDIX_C_66_ROW_DATED_CONTRACT_DAILY_OHLCV_QUARANTINE_INTAKE_EXECUTION_PARTIAL_FAIL_CLOSED_2026-05-30.md
```

Original intake root:

```text
docs/researchops/source_native_futures_daily_data_library/APPENDIX_C_DATABENTO_66_ROW_DATED_CONTRACT_DAILY_ARCHIVE/2026-05-18_2026-05-22
```

Original validation:

```text
VALIDATION_PASS_ROWS: 54
VALIDATION_FAIL_CLOSED_ROWS: 12
```

No new provider request was made by this hardening pass. It used only existing local raw provider output, provider-condition metadata, publisher metadata from the existing Databento coverage probe, and local validation artifacts.

## Publisher Evidence

Existing Databento publisher metadata records:

```text
publisher_id 1   dataset GLBX.MDP3   venue GLBX  description CME Globex MDP 3.0
publisher_id 101 dataset XEUR.EOBI   venue XEUR  description Eurex EOBI
publisher_id 103 dataset XEUR.EOBI   venue XOFF  description Eurex EOBI - Off-Market Trades
publisher_id 105 dataset XCBF.PITCH  venue XCBF  description Cboe Futures Exchange (CFE)
publisher_id 106 dataset XCBF.PITCH  venue XOFF  description Cboe Futures Exchange (CFE) - Off-Market Trades
```

## Deduplication Policy

Canonical publisher policy:

```text
GLBX.MDP3  -> publisher_id 1
XEUR.EOBI  -> publisher_id 101
XCBF.PITCH -> publisher_id 105
```

Rules:

```text
SELECT_PRIMARY_VENUE_PUBLISHER_EXCLUDE_OFF_MARKET_XOFF
```

For each row/date:

1. Select exactly one canonical primary-venue publisher row.
2. Preserve all non-canonical rows with publisher labels.
3. Exclude `XOFF` off-market rows from the policy-applied readiness set.
4. Fail closed if the canonical row is missing, duplicated, malformed, or has non-available provider condition metadata.
5. Do not aggregate, average, merge, replace, substitute, drop, or reweight source rows.

## Missing-Row Policy

Strict missing-row policy:

```text
FAIL_CLOSED_STRICT_MISSING_ROW_POLICY_NO_FILL_NO_DROP_NO_INTERPOLATION
```

No forward fill, backfill, interpolation, stale carry-forward, alternate contract substitution, adjacent symbol substitution, row drop, or portfolio reweighting is permitted.

## Result

```text
ORIGINAL_PASS_ROWS_PRESERVED: 54
ORIGINAL_FAIL_ROWS_TARGETED: 12
ORIGINAL_FAIL_ROWS_RESOLVED: 11
ORIGINAL_FAIL_ROWS_FAIL_CLOSED: 1
FINAL_DEV_RECON_DATA_READY_ROWS: 65
FINAL_FAIL_CLOSED_ROWS: 1
```

Resolved rows:

```text
OAT, GBS, GBM, GBL, GBX, BTS, BTP, DJ200S, DJ600, ESTX50, VIX
```

These rows are resolved only by selecting the canonical primary-venue publisher and excluding the off-market `XOFF` publisher rows.

Remaining fail-closed row:

```text
APPENDIX_C_181_001 ALI Aluminium
```

Reason:

```text
missing canonical GLBX.MDP3 rows on 2026-05-20 and 2026-05-21
```

## Output Root

```text
docs/researchops/source_native_futures_daily_data_library/APPENDIX_C_DATABENTO_66_ROW_DATED_CONTRACT_DAILY_ARCHIVE/2026-05-18_2026-05-22/readiness_hardening_2026-05-30
```

Key artifacts:

```text
policy/DATABENTO_APPENDIX_C_PUBLISHER_DEDUP_POLICY_LEDGER_2026-05-30.csv
policy/DATABENTO_APPENDIX_C_65_ROW_DEV_RECON_DATA_READY_CANONICAL_MANIFEST_2026-05-30.csv
sanitized_bars/DATABENTO_APPENDIX_C_66_ROW_POLICY_OBSERVED_WITH_PUBLISHER_LABELS_2026-05-18_2026-05-22.csv
sanitized_bars/DATABENTO_APPENDIX_C_65_ROW_POLICY_APPLIED_DEV_RECON_READY_PLUS_FAIL_CLOSED_OBSERVED_2026-05-18_2026-05-22.csv
validation/DATABENTO_APPENDIX_C_66_ROW_POLICY_APPLIED_ROW_VALIDATION_2026-05-30.csv
validation/DATABENTO_APPENDIX_C_66_ROW_HARDENING_RESOLUTION_LEDGER_2026-05-30.csv
validation/DATABENTO_APPENDIX_C_12_FAIL_CLOSED_RAW_PUBLISHER_DETAIL_2026-05-30.csv
provenance/DATABENTO_APPENDIX_C_66_ROW_QUARANTINE_READINESS_HARDENING_STATUS_2026-05-30.csv
provenance/DATABENTO_APPENDIX_C_66_ROW_QUARANTINE_READINESS_HARDENING_PROVENANCE_2026-05-30.md
provenance/DATABENTO_APPENDIX_C_66_ROW_QUARANTINE_READINESS_HARDENING_SHA256SUMS_2026-05-30.txt
```

## Boundary

The 65 ready rows are:

```text
YES_DEV_RECON_DATA_READY_NOT_STRATEGY_READY
```

They are not diagnostics-ready, not backtest-ready, not forecast-ready, not position-ready, not cost/carry/trend-ready, not risk-ready, not OOS/Lockbox/Forward-ready, not deployment-ready, not trading-ready, and not promotion-ready.

## Non-Authorization

This hardening pass authorizes no provider API access, no new data download, no expanded symbols, no expanded windows, no diagnostics, no backtests, no forecasts, no positions, no costs, no carry, no trend, no volatility/risk calculations, no OOS, no Lockbox, no Forward, no CFD adapters, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.
