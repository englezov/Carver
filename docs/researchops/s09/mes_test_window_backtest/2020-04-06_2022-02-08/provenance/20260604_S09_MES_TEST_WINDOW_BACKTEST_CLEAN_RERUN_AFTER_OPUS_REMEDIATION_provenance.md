# S09 MES TEST Window Backtest Provenance

Date: 2026-06-04

Status:

```text
CLEAN_S09_MES_TEST_BACKTEST_WRITTEN_AFTER_REMEDIATION_GUARDS_NOT_PROMOTION
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
- state_history_window: 2019-05-05 through 2020-04-05
- raw_symbols: MESM9, MESU9, MESZ9, MESH0, MESM0, MESU0, MESZ0, MESH1, MESM1, MESU1, MESZ1, MESH2
- scored_completed_dates: 574
- completed_dates_field_scope: SCORING_WINDOW_ONLY_DO_NOT_ADD_STATE_HISTORY
- state_history_completed_dates: 289
- total_state_plus_scoring_completed_dates: 863
- warmup_bars_required_before_scoring: 257
- fractional_trade_event_count: 567
- whole_contract_equivalent_change_count: 1
- trade_count_sample_definition: FRACTIONAL_CONTRACT_EQUIVALENT_POSITION_CHANGE_EVENTS_ABOVE_NUMERICAL_EPSILON
- backtest_execution_count: 1

Execution semantics:

The state-history window may initialize indicators, but it is not scored
evidence. Forecasts are emitted only for completed dates inside the TEST scoring
window and are applied to the next completed TEST scoring bar.
Position is a fractional contract-equivalent research multiplier equal to
final forecast divided by 10.0. No buffer, contract rounding,
capital sizing, intraday fill model, validation, lockbox, forward, deployment,
trading, promotion, Git staging, commit, push, PR, or remote operation is in
scope.

Written artifacts:

- source sanitized inputs:
- `docs/researchops/s09/mes_machinery_dev_minimum_slice/2019-05-05_2020-04-05/sanitized_daily_bars/20260603_S09_MES_MACHINERY_DEV_MINIMUM_SLICE_DOWNLOAD_sanitized_quarantine_ohlcv_1d.csv`
- `docs/researchops/s09/mes_test_window_backtest/2020-04-06_2022-02-08/sanitized_daily_bars/20260604_S09_MES_TEST_WINDOW_BACKTEST_sanitized_quarantine_ohlcv_1d.csv`
- `docs/researchops/s09/mes_test_window_backtest/2020-04-06_2022-02-08/lineage/20260604_S09_MES_TEST_WINDOW_BACKTEST_CLEAN_RERUN_AFTER_OPUS_REMEDIATION_continuous_adjusted_mes_test.csv`
- `docs/researchops/s09/mes_test_window_backtest/2020-04-06_2022-02-08/forecast/20260604_S09_MES_TEST_WINDOW_BACKTEST_CLEAN_RERUN_AFTER_OPUS_REMEDIATION_s09_forecast_rows.csv`
- `docs/researchops/s09/mes_test_window_backtest/2020-04-06_2022-02-08/backtest/20260604_S09_MES_TEST_WINDOW_BACKTEST_CLEAN_RERUN_AFTER_OPUS_REMEDIATION_backtest_rows.csv`
- `docs/researchops/s09/mes_test_window_backtest/2020-04-06_2022-02-08/backtest/20260604_S09_MES_TEST_WINDOW_BACKTEST_CLEAN_RERUN_AFTER_OPUS_REMEDIATION_summary.csv`
