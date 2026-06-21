# S09 MES VALIDATION Window Backtest Provenance

Date: 2026-06-04

Status:

```text
PASS_S09_MES_VALIDATION_WINDOW_BACKTEST_EXECUTED_EXACTLY_ONCE_NOT_PROMOTION
```

Authorized scope:

- gate: S09_MES_VALIDATION_WINDOW_BACKTEST_AUTHORIZED_EXECUTION_GATE
- lane_class: SOURCE_NATIVE_FUTURES
- source_row: APPENDIX_C_174_006
- author_market_code: MES
- provider: DATABENTO_HISTORICAL
- dataset: GLBX.MDP3
- schema: ohlcv-1d
- VALIDATION window: 2022-02-09 through 2023-12-13
- state_history_window: 2020-04-06 through 2022-02-08
- raw_symbols: MESM0, MESU0, MESZ0, MESH1, MESM1, MESU1, MESZ1, MESH2, MESM2, MESU2, MESZ2, MESH3, MESM3, MESU3, MESZ3, MESH4
- scored_completed_dates: 574
- completed_dates_field_scope: VALIDATION_SCORING_WINDOW_ONLY_DO_NOT_ADD_TEST_STATE_HISTORY
- state_history_completed_dates: 574
- total_state_plus_scoring_completed_dates: 1148
- warmup_bars_required_before_scoring: 257
- fractional_trade_event_count: 573
- whole_contract_equivalent_change_count: 0
- trade_count_sample_definition: FRACTIONAL_CONTRACT_EQUIVALENT_POSITION_CHANGE_EVENTS_ABOVE_NUMERICAL_EPSILON
- backtest_execution_count: 1

Execution semantics:

The TEST window initializes state only and is not scored evidence. Forecasts are
emitted only for completed dates inside the VALIDATION scoring window and are
applied to the next completed VALIDATION scoring bar. Position is a fractional
contract-equivalent research multiplier equal to final forecast divided by
10.0. No buffer, contract rounding, capital sizing,
intraday fill model, Lockbox, Forward, deployment, trading, promotion, Git
staging, commit, push, PR, or remote operation is in scope.

Written artifacts:

- source sanitized inputs:
- `docs/researchops/s09/mes_test_window_backtest/2020-04-06_2022-02-08/sanitized_daily_bars/20260604_S09_MES_TEST_WINDOW_BACKTEST_sanitized_quarantine_ohlcv_1d.csv`
- `docs/researchops/s09/mes_validation_window_download/2022-02-09_2023-12-13/sanitized_daily_bars/20260604_S09_MES_VALIDATION_WINDOW_DOWNLOAD_sanitized_quarantine_ohlcv_1d.csv`
- `docs/researchops/s09/mes_validation_window_backtest/2022-02-09_2023-12-13/lineage/20260604_S09_MES_VALIDATION_WINDOW_BACKTEST_continuous_adjusted_mes_test.csv`
- `docs/researchops/s09/mes_validation_window_backtest/2022-02-09_2023-12-13/forecast/20260604_S09_MES_VALIDATION_WINDOW_BACKTEST_s09_forecast_rows.csv`
- `docs/researchops/s09/mes_validation_window_backtest/2022-02-09_2023-12-13/backtest/20260604_S09_MES_VALIDATION_WINDOW_BACKTEST_backtest_rows.csv`
- `docs/researchops/s09/mes_validation_window_backtest/2022-02-09_2023-12-13/backtest/20260604_S09_MES_VALIDATION_WINDOW_BACKTEST_summary.csv`
