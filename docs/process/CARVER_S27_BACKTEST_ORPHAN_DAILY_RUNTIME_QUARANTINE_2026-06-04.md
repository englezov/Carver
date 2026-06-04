# Carver S27 Backtest Orphan Daily Runtime Quarantine

Date: 2026-06-04

Status:

```text
PASS_ORPHAN_LEGACY_DAILY_RUNTIME_REMOVED_FROM_CORRECTED_BACKTEST_PACKAGE_AND_QUARANTINED
```

## Reason

The local hostile audit of the completed corrected S27 first-window backtest found an orphan legacy `daily_runtime_rows` artifact inside the corrected backtest output root.

That artifact was not produced by the converted corrected runner, was not included in the current SHA ledger, and spanned outside the declared 2022-2023 first-window package.

## Quarantine Action

The orphan folder was moved from:

```text
docs/researchops/s26_s27_backtest_readiness/ZN_S27_SINGLE_INSTRUMENT/2022-01-01_2023-12-31/retargeted_dev_recon_backtest/daily_runtime_rows
```

to:

```text
docs/researchops/s26_s27_backtest_readiness/ZN_S27_SINGLE_INSTRUMENT/2022-01-01_2023-12-31/retargeted_dev_recon_backtest_orphan_quarantine/daily_runtime_rows
```

The file was preserved, not deleted.

## Boundary

The quarantined legacy daily-runtime artifact is not part of the corrected S27 first-window backtest package and must not be used as evidence for the corrected run.

The corrected package is:

```text
docs/researchops/s26_s27_backtest_readiness/ZN_S27_SINGLE_INSTRUMENT/2022-01-01_2023-12-31/retargeted_dev_recon_backtest
```

## Non-Authorization

This quarantine record authorizes no provider/API call, no data download, no diagnostics, no backtest, no OOS, no Lockbox, no Forward, no deployment, no trading, no promotion, no Git staging, no commit, no push, and no PR.
