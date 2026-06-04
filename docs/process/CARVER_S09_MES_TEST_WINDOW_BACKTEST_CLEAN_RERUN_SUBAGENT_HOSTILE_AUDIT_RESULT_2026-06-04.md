# S09 MES TEST Window Backtest Clean Rerun Subagent Hostile Audit Result

Date: 2026-06-04

Status:

```text
SUBAGENT_HOSTILE_AUDIT_PASS_S09_MES_TEST_CLEAN_RERUN_NOT_PROMOTION
```

## Scope

This hostile audit reviewed the completed S09 MES TEST clean rerun artifacts
for the authorized TEST window `2020-04-06` through `2022-02-08`.

No provider API access, new market-data request, data download, VALIDATION,
Lockbox, Forward, Git staging, commit, push, PR, deployment, trading, or
promotion was performed by the audit.

## Verdict

PASS.

## Findings

- exactly one clean-rerun receipt exists for
  `20260604_S09_MES_TEST_WINDOW_BACKTEST_CLEAN_RERUN_AFTER_OPUS_REMEDIATION`;
- receipt has `backtest_execution_count: 1` and the exact clean-rerun `run_id`;
- status and manifest assert no new Databento/API call and existing authorized
  TEST download only;
- no clean-rerun-named raw provider output or metadata files exist;
- no VALIDATION, Lockbox, Forward, deployment, trading, promotion, or Git
  overclaim was found;
- lineage has `289` state-history dates from `2019-05-05` through
  `2020-04-05`, `574` TEST scoring dates from `2020-04-06` through
  `2022-02-08`, and zero out-of-mask dates;
- forecast rows are TEST scoring-window only, count `574`;
- backtest rows are TEST scoring-window only, count `573`;
- fractional sample gate reports `fractional_trade_event_count = 567`;
- whole-contract count reports `whole_contract_equivalent_change_count = 1`
  and is labeled diagnostic-only;
- guard checks all pass.

## Verification

Hostile subagent ran:

```text
python -m unittest tests.test_s09_mes_test_window_backtest_guard
```

Observed result:

```text
Ran 24 tests
OK
```

Main-agent focused verification after the run:

```text
python -m py_compile tools\databento\carver_s09_mes_test_window_backtest.py src\carver\spine\s09_mes_lineage.py
python -m unittest tests.test_s09_mes_test_window_backtest_guard tests.test_s09_mes_lineage_synthetic
```

Observed result:

```text
Ran 110 tests
OK
```

## Boundary

This hostile audit pass does not promote the strategy and does not authorize
VALIDATION, Lockbox, Forward, deployment, trading, Git operations, or any
further backtest.
