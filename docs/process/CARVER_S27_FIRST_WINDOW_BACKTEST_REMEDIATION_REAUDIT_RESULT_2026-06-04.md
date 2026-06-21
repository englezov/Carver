# Carver S27 First-Window Backtest Remediation Re-Audit Result

Date: 2026-06-04

Mode: subagent read-only re-audit after remediation. No provider/API access, no data download, no diagnostics, no backtest rerun, no Git operation, no OOS, no Lockbox, and no Forward access.

Auditor:

```text
subagent: 019e9253-fd53-71e3-9187-4a57cd18bc33
nickname: Archimedes
```

## Verdict

```text
HIGH: NONE
MEDIUM: NONE
LOW: NONE
AUDIT_DISPOSITION: PASS_S27_FIRST_WINDOW_BACKTEST_PACKAGE_AFTER_REMEDIATION
```

## Evidence

The re-audit verified:

```text
PackageDailyRuntimeRowsExists: False
QuarantineDailyRuntimeRowsExists: True
```

The orphan legacy daily-runtime artifact is preserved in:

```text
docs/researchops/s26_s27_backtest_readiness/ZN_S27_SINGLE_INSTRUMENT/2022-01-01_2023-12-31/retargeted_dev_recon_backtest_orphan_quarantine/daily_runtime_rows
```

The corrected package SHA manifest:

```text
entries: 13
excludes: daily_runtime_rows
excludes: retargeted_dev_recon_backtest_orphan_quarantine
includes: s27_blocked_dependency_rows.csv
```

The blocked dependency ledger is headered and zero-row:

```text
row_id,author_market_code,raw_symbol,completed_trading_date,derived_completed_bar_end_utc,block_reason,block_status
```

Row accounting remains internally consistent:

```text
s27_forecast_rows: 11775
backtest_rows: 11774
blocked_dependency_rows: 0
position/alignment/continuous rows: 11775
inactive rows: 9095
source rows: 20870
active plus inactive source accounting: PASS
```

The status remains:

```text
PASS_RETARGETED_S27_ZN_DEV_RECON_UNIT_PLUMBING_NO_COST_BACKTEST_NOT_ALPHA
```

The boundary-declaration caveat is recorded in:

```text
docs/process/CARVER_S27_FIRST_WINDOW_BACKTEST_HOSTILE_AUDIT_REMEDIATION_2026-06-04.md
```

## Non-Authorization

This re-audit result authorizes no provider/API call, no data download, no diagnostics, no backtest, no returns, no PnL, no positions beyond the already generated authorized first-window package, no OOS, no Lockbox, no Forward, no deployment, no trading, no promotion, no Git staging, no commit, no push, and no PR.
