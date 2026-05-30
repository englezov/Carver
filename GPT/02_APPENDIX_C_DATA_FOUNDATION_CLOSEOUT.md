# Appendix C Data Foundation Closeout Context

Date: 2026-05-30

Status:

```text
PROCESS_ONLY_APPENDIX_C_DATA_FOUNDATION_CONTEXT_NOT_STRATEGY_AUTHORIZATION
```

## Purpose

Summarize the completed Appendix C/Jumbo practical data-foundation state for Opus before it designs the S26/S27 mean-reversion path.

This file is context only. It does not authorize strategy computation.

## Appendix C Source Universe

Book source universe:

```text
Appendix C Tables 172-183
102 instruments in Jumbo portfolio
```

Local machine-readable Appendix C universe work preserved all 102 rows and kept fail-closed rows visible rather than silently dropping, substituting, or reweighting them.

## Provider Path

Practical provider path selected:

```text
DATABENTO_SOURCE_NATIVE_FUTURES
```

Databento coverage work resolved a large source-native futures subset and replaced the earlier NinjaTrader-only bottleneck.

## Static Identity Result

After Databento contract-identity hardening:

```text
APPENDIX_C_ROWS: 102
STATIC_IDENTITY_READY_FOR_DATABENTO_INTAKE: 66
PRESERVED_NON_CANDIDATE_OR_FAIL_CLOSED_ROWS: 36
```

Three rows from a prior 69-row candidate set were hard fail-closed because the Databento candidate did not match the Appendix C product identity:

```text
TWN / FTSE Taiwan
UC / USD-Offshore CNH
SCI / Iron
```

## First 66-Row OHLCV Intake

Bounded Databento quarantine intake:

```text
provider: DATABENTO
schema: ohlcv-1d
stype_in: instrument_id
request_start_utc: 2026-05-18T00:00:00Z
request_end_utc_exclusive: 2026-05-23T00:00:00Z
completed_utc_dates: 2026-05-18 through 2026-05-22
```

Initial result:

```text
EXPECTED_TOTAL_ROWS: 330
OBSERVED_SANITIZED_ROWS: 380
VALIDATION_PASS_ROWS: 54
VALIDATION_FAIL_CLOSED_ROWS: 12
REQUEST_ERRORS: 0
```

The 12 initial failures were caused by duplicate publisher rows for XEUR/XCBF feeds and missing ALI rows.

## Publisher And Missing-Row Hardening

Canonical publisher policy:

```text
GLBX.MDP3  -> publisher_id 1   / GLBX
XEUR.EOBI  -> publisher_id 101 / XEUR
XCBF.PITCH -> publisher_id 105 / XCBF
```

Off-market rows are preserved but excluded:

```text
XEUR publisher_id 103 / XOFF
XCBF publisher_id 106 / XOFF
```

Strict missing-row policy:

```text
NO_FILL
NO_DROP
NO_SUBSTITUTE
NO_INTERPOLATION
NO_REWEIGHT
```

Hardening result:

```text
ORIGINAL_PASS_ROWS_PRESERVED: 54
ORIGINAL_FAIL_ROWS_TARGETED: 12
ORIGINAL_FAIL_ROWS_RESOLVED: 11
ORIGINAL_FAIL_ROWS_FAIL_CLOSED: 1
FINAL_DEV_RECON_DATA_READY_ROWS: 65
FINAL_FAIL_CLOSED_ROWS: 1
```

Remaining fail-closed row:

```text
APPENDIX_C_181_001 / ALI / Aluminium
reason: missing canonical GLBX rows on 2026-05-20 and 2026-05-21
```

## Meaning Of "Data Ready"

The 65-row result means:

```text
DEVELOPMENT_RECONCILIATION_DATA_READY_NOT_STRATEGY_READY
```

It does not mean:

```text
BACKTEST_READY
FORECAST_READY
POSITION_READY
COST_READY
CARRY_READY
TREND_READY
RISK_READY
OOS_READY
LOCKBOX_READY
FORWARD_READY
DEPLOYMENT_READY
TRADING_READY
PROMOTION_READY
```

## Why This Matters For S26/S27

The Appendix C work establishes that source-native futures data access is practical enough to support the next strategy-research chapter. It does not decide the S26/S27 universe, rules, parameters, or readiness path.

Opus should design S26/S27 from the book first, then decide what data and conformance gates are needed.

## Non-Authorization

This context authorizes no provider calls, no new data download, no market-row parsing, no diagnostics, no backtests, no forecasts, no positions, no costs, no carry, no trend, no risk calculations, no OOS, no Lockbox, no Forward, no CFD adapters, no old QuantLab pipeline use, no tuning, no deployment, no trading, no promotion, no Git operations, and no remote operations.
