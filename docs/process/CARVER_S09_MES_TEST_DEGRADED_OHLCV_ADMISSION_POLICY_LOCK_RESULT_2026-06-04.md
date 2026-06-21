# S09 MES TEST Degraded OHLCV Admission Policy Lock Result

Date: 2026-06-04

Status:

```text
LOCKED_SOURCE_NATIVE_TEST_DEGRADED_OHLCV_ADMISSION_POLICY_NOT_BACKTEST
```

Scope:

- lane_class: SOURCE_NATIVE_FUTURES
- source_row: APPENDIX_C_174_006
- provider: DATABENTO_HISTORICAL
- dataset: GLBX.MDP3
- schema: ohlcv-1d
- TEST window: 2020-04-06 through 2022-02-08

Policy:

The operator authorized a source-native degraded-day OHLCV admission policy for
the TEST window. The policy admits only Databento-native OHLCV rows already
present in the authorized TEST download when Databento marks the completed date
as `DEGRADED`.

Authorized degraded completed dates:

- 2020-06-30
- 2020-07-01
- 2021-12-05
- 2022-01-02

Boundaries:

- no fill, interpolation, repair, or row synthesis;
- no ES, CFD, alternate provider, or old QuantLab substitution;
- no window widening and no date outside TEST;
- degraded labels must be preserved in strategy-facing artifacts;
- any degraded date outside this four-date set remains fail-closed;
- this policy authorizes no backtest, forecast, VALIDATION, Lockbox, Forward,
  deployment, trading, promotion, Git staging, commit, push, PR, or remote
  operation.

Written artifacts:

- `docs/researchops/s09/mes_test_window_backtest/2020-04-06_2022-02-08/degraded_ohlcv_policy/20260604_S09_MES_TEST_DEGRADED_OHLCV_ADMISSION_POLICY_status.json`
- `docs/researchops/s09/mes_test_window_backtest/2020-04-06_2022-02-08/degraded_ohlcv_policy/20260604_S09_MES_TEST_DEGRADED_OHLCV_ADMISSION_POLICY_ledger.csv`
- `docs/researchops/s09/mes_test_window_backtest/2020-04-06_2022-02-08/degraded_ohlcv_policy/20260604_S09_MES_TEST_DEGRADED_OHLCV_ADMISSION_POLICY_row_overlay.csv`
