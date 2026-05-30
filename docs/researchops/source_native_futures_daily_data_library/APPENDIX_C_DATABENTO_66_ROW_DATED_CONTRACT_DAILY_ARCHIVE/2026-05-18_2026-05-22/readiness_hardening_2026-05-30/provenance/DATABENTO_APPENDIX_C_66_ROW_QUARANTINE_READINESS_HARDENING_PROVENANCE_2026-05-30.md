# Databento Appendix C 66-Row Quarantine Readiness Hardening Provenance

Date: 2026-05-30
Run UTC: 2026-05-30T20:39:28Z

Status:

```text
PASS_POLICY_HARDENING_65_DEV_RECON_READY_1_FAIL_CLOSED_NOT_STRATEGY_READY
```

## Inputs

Original intake root:

```text
C:/Users/openclaw/Desktop/Carver/docs/researchops/source_native_futures_daily_data_library/APPENDIX_C_DATABENTO_66_ROW_DATED_CONTRACT_DAILY_ARCHIVE/2026-05-18_2026-05-22
```

Raw provider output, original sanitized OHLCV, original validation ledger, provider condition metadata, and request manifest were inspected locally. No new provider request was made by this hardening pass.

## Publisher Policy

```text
GLBX.MDP3  -> canonical publisher_id 1   / venue GLBX
XEUR.EOBI  -> canonical publisher_id 101 / venue XEUR; exclude publisher_id 103 / venue XOFF off-market
XCBF.PITCH -> canonical publisher_id 105 / venue XCBF; exclude publisher_id 106 / venue XOFF off-market
```

## Missing-Row Policy

Strict fail-closed. No forward fill, backfill, interpolation, row drop, substitution, or reweighting is permitted. A row/date with no canonical provider row remains blocked.

## Counts

```text
ORIGINAL_PASS_ROWS_PRESERVED: 54
ORIGINAL_FAIL_ROWS_TARGETED: 12
ORIGINAL_FAIL_ROWS_RESOLVED: 11
ORIGINAL_FAIL_ROWS_FAIL_CLOSED: 1
FINAL_DEV_RECON_DATA_READY_ROWS: 65
FINAL_FAIL_CLOSED_ROWS: 1
```

## Boundary

The final ready rows are Development/Reconciliation data-ready only. They are not strategy inputs, not backtest-ready, not forecast-ready, not roll-ready, not cost/carry/trend-ready, and not promotion-ready.
