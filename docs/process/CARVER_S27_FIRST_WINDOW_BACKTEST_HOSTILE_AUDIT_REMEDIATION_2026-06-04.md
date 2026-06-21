# Carver S27 First-Window Backtest Hostile Audit Remediation

Date: 2026-06-04

Status:

```text
PASS_S27_FIRST_WINDOW_BACKTEST_PACKAGE_REMEDIATED_AFTER_LOCAL_HOSTILE_AUDIT
```

## Scope

This record covers remediation after the subagent local hostile audit of the authorized corrected S27 first-window backtest.

The backtest result remains bounded as:

```text
DEV_RECON_UNIT_PLUMBING_NO_COST_NOT_ALPHA_NOT_PROMOTION
```

## Backtest Result Preserved

The authorized runner was rerun after remediation.

Observed status:

```text
PASS_RETARGETED_S27_ZN_DEV_RECON_UNIT_PLUMBING_NO_COST_BACKTEST_NOT_ALPHA
```

Observed window and row counts:

```text
effective_backtest_start: 2022-01-04
effective_backtest_end: 2023-12-29
s27_forecast_rows: 11775
backtest_rows: 11774
blocked_dependency_rows: 0
gross_no_cost_pnl_usd: 531.25
position_change_count: 177
```

Boundary claims in status:

```text
provider_api_access: NO
new_data_download: NO
diagnostics_run: NO_SHARPE_NO_DRAWDOWN_NO_ALPHA_STATISTICS
oos_access: NO
lockbox_access: NO
forward_access: NO
git_operations: NO
cost_status: FAIL_CLOSED_NO_COMMISSION_OR_SPREAD_COST_LOCK_NO_COSTS_APPLIED
real_m1_position_sizing_status: BLOCKED_CAPITAL_NOT_LOCKED_UNIT_BASE_USED_FOR_DEV_RECON_PLUMBING
```

## Finding Remediation

### HIGH: Orphan Legacy Daily Runtime Artifact

Finding:

```text
The corrected backtest package contained an orphan daily_runtime_rows artifact spanning outside the declared 2022-2023 package.
```

Remediation:

```text
docs/process/CARVER_S27_BACKTEST_ORPHAN_DAILY_RUNTIME_QUARANTINE_2026-06-04.md
```

The orphan folder was moved out of the corrected package and preserved in:

```text
docs/researchops/s26_s27_backtest_readiness/ZN_S27_SINGLE_INSTRUMENT/2022-01-01_2023-12-31/retargeted_dev_recon_backtest_orphan_quarantine/daily_runtime_rows
```

Verification:

```text
Package daily_runtime_rows exists: False
Corrected package top folders:
backtest_rows
corrected_runtime_alignment_rows
cost_fail_closed_record
forecast_rows
hashes
local_hourly_lineage
position_rows
provenance
status
validation
```

The corrected package hash manifest now has:

```text
IncludesDailyRuntime: 0
IncludesQuarantine: 0
IncludesBlockedLedger: 1
```

### MEDIUM: Boundary Declaration Rows

Finding:

```text
Some validation rows are boundary declarations emitted by the local runner rather than independent external proof.
```

Disposition:

This is accepted and explicitly governed. Rows such as `no_provider_api_access`, `no_oos_lockbox_forward`, `costs_fail_closed`, and `real_m1_position_sizing_blocked` are local runner boundary declarations. They must be read as process/status declarations from this execution, not as external attestation.

No contradictory provider, download, OOS, Lockbox, Forward, Git, deployment, trading, promotion, real-cost, or real-sizing artifact was found in the corrected package.

### LOW: Headerless Zero-Row Blocked Dependency Ledger

Finding:

```text
The blocked dependency ledger was a 0-byte empty file.
```

Remediation:

The runner now writes the blocked dependency ledger with a header even when zero rows are blocked.

Verification:

```text
row_id,author_market_code,raw_symbol,completed_trading_date,derived_completed_bar_end_utc,block_reason,block_status
ImportCsvRows: 0
```

## Verification

```text
python -m py_compile tools/databento/carver_s27_zn_2022_2023_retargeted_dev_recon_backtest.py tests/test_s27_corrected_backtest_runner_preflight.py
python -m unittest tests.test_s27_corrected_backtest_runner_preflight
```

Result:

```text
Ran 3 tests
OK
```

The authorized corrected backtest was rerun after remediation and produced the same headline status and row counts.

## Non-Authorization

This remediation record authorizes no provider/API call, no data download, no diagnostics, no additional backtest beyond the already operator-authorized first-window corrected S27 rerun, no OOS, no Lockbox, no Forward, no deployment, no trading, no promotion, no Git staging, no commit, no push, and no PR.
