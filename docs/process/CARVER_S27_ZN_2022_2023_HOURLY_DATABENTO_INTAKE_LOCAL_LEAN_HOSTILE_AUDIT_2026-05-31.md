# Carver S27 ZN 2022-2023 Hourly Databento Intake Local Lean Hostile Audit

Date: 2026-05-31

Mode: Local hostile audit over the bounded Databento intake result. No new provider API access, no new data download, no diagnostics, no backtests, no forecasts, no positions, no costs, no deployment, no trading, no promotion, no Git operations.

## Audited Artifacts

```text
tools/databento/carver_s27_zn_2022_2023_hourly_intake.py
docs/process/CARVER_S27_ZN_2022_2023_DEV_RECON_BACKTEST_EXECUTION_GATE_DRAFT_2026-05-31.md
docs/process/CARVER_S27_ZN_2022_2023_HOURLY_DATABENTO_INTAKE_RESULT_2026-05-31.md
docs/researchops/s26_s27_backtest_readiness/ZN_S27_SINGLE_INSTRUMENT/2022-01-01_2023-12-31/hourly_archive_quarantine/status/20260531_S27_ZN_2022_2023_OHLCV_1H_ARCHIVE_quarantine_intake_status.json
docs/researchops/s26_s27_backtest_readiness/ZN_S27_SINGLE_INSTRUMENT/2022-01-01_2023-12-31/hourly_archive_quarantine/validation/20260531_S27_ZN_2022_2023_OHLCV_1H_ARCHIVE_row_validation.json
```

## Findings

Critical: None.

High: None.

Medium: One provider-condition blocker is correctly preserved and blocks backtest readiness:

```text
PROVIDER_CONDITION_DEGRADED: 1
status: FAIL_CLOSED_PROVIDER_CONDITION_BLOCKERS_PRESENT_NOT_BACKTEST_READY
```

This is not a governance failure. It prevents silent use of the affected row.

Low: The row-count distribution is uneven by dated contract, as expected for overlapping individual Treasury note contracts and differing liquidity/active windows. This is acceptable for quarantine intake but not sufficient for a strategy-facing continuous lineage until the next roll/lineage gate validates selected rows.

## Disposition

```text
BLOCKING_FINDINGS: YES_FOR_BACKTEST_EXECUTION
AUDIT_DISPOSITION: PASS_QUARANTINE_INTAKE_PRESERVED_FAIL_CLOSED_NOT_BACKTEST_READY
```

The archive exists and is useful. It does not yet authorize or support backtest execution because one provider-condition degraded row must be handled by a separate fail-closed decision.

## Non-Authorization

This audit result authorizes no provider API access, no data download, no market-row parsing, no diagnostics, no backtests, no forecasts, no positions, no costs, no carry, no OOS, no Lockbox, no Forward, no CFD adapters, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.
