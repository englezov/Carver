# S09 MES TEST Window Backtest Fail-Closed Result

Date: 2026-06-04

Status:

```text
FAIL_CLOSED_S09_MES_TEST_WINDOW_BACKTEST_BLOCKED_BEFORE_BACKTEST
```

Authorized scope:

- lane_class: SOURCE_NATIVE_FUTURES
- source_row: APPENDIX_C_174_006
- provider: DATABENTO_HISTORICAL
- dataset: GLBX.MDP3
- schema: ohlcv-1d
- TEST window: 2020-04-06 through 2022-02-08
- raw_symbols: MESM0, MESU0, MESZ0, MESH1, MESM1, MESU1, MESZ1, MESH2

Outcome:

The authorized TEST Databento download completed inside the locked TEST
boundary. The backtest failed closed before any forecast rows, PnL rows, summary
rows, or backtest execution receipt were written.

Blocker:

- downloaded completed dates before provider-condition filter: 574
- admitted completed dates after normal-provider-only admission: 570
- locked TEST completed-date budget: 574
- quarantined Databento degraded completed dates: 2020-06-30, 2020-07-01, 2021-12-05, 2022-01-02
- backtest_execution_count: 0

Boundary:

No VALIDATION, Lockbox, Forward, CFD, old QuantLab active-pipeline state,
deployment, trading, promotion, Git staging, commit, push, PR, or remote
operation was used by this fail-closed result.

Next authorization needed:

The operator must choose a source-native policy for TEST OHLCV degraded
provider-condition days before the first TEST backtest can run. Conservative
options are to keep the fail-closed block, explicitly admit the four degraded
TEST OHLCV completed dates with a documented degraded-day policy, or re-lock the
TEST window/date budget.
