# S09 MES TEST Window Backtest Provenance

Date: 2026-06-04

Status:

```text
PASS_S09_MES_TEST_WINDOW_BACKTEST_EXECUTED_EXACTLY_ONCE_NOT_PROMOTION
```

Authorized scope:

- gate: S09_MES_TEST_WINDOW_BACKTEST_AUTHORIZED_EXECUTION_GATE
- lane_class: SOURCE_NATIVE_FUTURES
- source_row: APPENDIX_C_174_006
- author_market_code: MES
- provider: DATABENTO_HISTORICAL
- dataset: GLBX.MDP3
- schema: ohlcv-1d
- TEST window: 2020-04-06 through 2022-02-08
- raw_symbols: MESM0, MESU0, MESZ0, MESH1, MESM1, MESU1, MESZ1, MESH2
- completed_dates: 574
- warmup_bars_inside_test_window: 257
- backtest_execution_count: 1
- data_access_for_this_execution: no new Databento API call; used existing authorized TEST download
- degraded_ohlcv_policy: SOURCE_NATIVE_DEGRADED_OHLCV_OPERATOR_POLICY_LOCKED

Execution semantics:

The first 257 TEST completed bars are indicator warmup. Forecasts are
computed from completed daily bars only and applied to the next completed bar.
Position is a fractional contract-equivalent research multiplier equal to
final forecast divided by 10.0. No buffer, contract rounding,
capital sizing, intraday fill model, validation, lockbox, forward, deployment,
trading, promotion, Git staging, commit, push, PR, or remote operation is in
scope.

Written artifacts:

- `docs/researchops/s09/mes_test_window_backtest/2020-04-06_2022-02-08/sanitized_daily_bars/20260604_S09_MES_TEST_WINDOW_BACKTEST_sanitized_quarantine_ohlcv_1d.csv`
- `docs/researchops/s09/mes_test_window_backtest/2020-04-06_2022-02-08/lineage/20260604_S09_MES_TEST_WINDOW_BACKTEST_continuous_adjusted_mes_test.csv`
- `docs/researchops/s09/mes_test_window_backtest/2020-04-06_2022-02-08/forecast/20260604_S09_MES_TEST_WINDOW_BACKTEST_s09_forecast_rows.csv`
- `docs/researchops/s09/mes_test_window_backtest/2020-04-06_2022-02-08/backtest/20260604_S09_MES_TEST_WINDOW_BACKTEST_backtest_rows.csv`
- `docs/researchops/s09/mes_test_window_backtest/2020-04-06_2022-02-08/backtest/20260604_S09_MES_TEST_WINDOW_BACKTEST_summary.csv`
