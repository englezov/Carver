# S09 MES TEST Window Backtest Result

Date: 2026-06-04

Status:

```text
CLEAN_S09_MES_TEST_BACKTEST_WRITTEN_AFTER_REMEDIATION_GUARDS_NOT_PROMOTION
```

Scope:

- lane_class: SOURCE_NATIVE_FUTURES
- source_row: APPENDIX_C_174_006
- state_history_window: 2019-05-05 through 2020-04-05
- TEST window: 2020-04-06 through 2022-02-08
- scored_completed_dates: 574
- completed_dates_field_scope: SCORING_WINDOW_ONLY_DO_NOT_ADD_STATE_HISTORY
- state_history_completed_dates: 289
- total_state_plus_scoring_completed_dates: 863
- warmup_bars_required_before_scoring: 257
- forecast_rows: 574
- backtest_rows: 573
- fractional_trade_event_count: 567
- whole_contract_equivalent_change_count: 1
- fractional_turnover_contract_equivalent: 72.97109068697873
- trade_count_sample_definition: FRACTIONAL_CONTRACT_EQUIVALENT_POSITION_CHANGE_EVENTS_ABOVE_NUMERICAL_EPSILON

Scenario summaries:

```json
[
  {
    "scenario_name": "CONSERVATIVE_LIVE_FUTURES_PASS_THROUGH",
    "round_turn_cost_usd": 2.93,
    "test_window": "2020-04-06 through 2022-02-08",
    "completed_dates": 574,
    "warmup_bars": 257,
    "forecast_rows": 574,
    "backtest_rows": 573,
    "trade_count_position_changes": 567,
    "fractional_trade_event_count": 567,
    "whole_contract_equivalent_change_count": 1,
    "fractional_turnover_contract_equivalent": 72.97109068697873,
    "max_position_change_contract_equivalent": 1.0707822946505483,
    "trade_count_sample_definition": "FRACTIONAL_CONTRACT_EQUIVALENT_POSITION_CHANGE_EVENTS_ABOVE_NUMERICAL_EPSILON",
    "whole_contract_count_definition": "EXECUTABILITY_DIAGNOSTIC_NOT_STATISTICAL_SAMPLE_GATE",
    "gross_pnl_usd": 531.9436406856365,
    "total_cost_usd": 213.80529571284768,
    "net_pnl_usd": 318.13834497278896,
    "mean_net_pnl_usd_per_row": 0.5552152617326159,
    "annualized_net_pnl_sharpe_like": 0.05360756904561793,
    "status": "TEST_BACKTEST_RESULT_NOT_VALIDATION_NOT_LOCKBOX_NOT_PROMOTION"
  },
  {
    "scenario_name": "ETF_SIM_FEE_ALL_IN_EXCHANGE_NFA_EXCLUDED",
    "round_turn_cost_usd": 2.49,
    "test_window": "2020-04-06 through 2022-02-08",
    "completed_dates": 574,
    "warmup_bars": 257,
    "forecast_rows": 574,
    "backtest_rows": 573,
    "trade_count_position_changes": 567,
    "fractional_trade_event_count": 567,
    "whole_contract_equivalent_change_count": 1,
    "fractional_turnover_contract_equivalent": 72.97109068697873,
    "max_position_change_contract_equivalent": 1.0707822946505483,
    "trade_count_sample_definition": "FRACTIONAL_CONTRACT_EQUIVALENT_POSITION_CHANGE_EVENTS_ABOVE_NUMERICAL_EPSILON",
    "whole_contract_count_definition": "EXECUTABILITY_DIAGNOSTIC_NOT_STATISTICAL_SAMPLE_GATE",
    "gross_pnl_usd": 531.9436406856365,
    "total_cost_usd": 181.69801581057706,
    "net_pnl_usd": 350.2456248750593,
    "mean_net_pnl_usd_per_row": 0.6112489090315172,
    "annualized_net_pnl_sharpe_like": 0.05901703450887615,
    "status": "TEST_BACKTEST_RESULT_NOT_VALIDATION_NOT_LOCKBOX_NOT_PROMOTION"
  }
]
```

Artifacts:

- `docs/researchops/s09/mes_test_window_backtest/2020-04-06_2022-02-08/status/20260604_S09_MES_TEST_WINDOW_BACKTEST_CLEAN_RERUN_AFTER_OPUS_REMEDIATION_status.json`
- `docs/researchops/s09/mes_test_window_backtest/2020-04-06_2022-02-08/status/20260604_S09_MES_TEST_WINDOW_BACKTEST_CLEAN_RERUN_AFTER_OPUS_REMEDIATION_backtest_execution_receipt.json`
- `docs/researchops/s09/mes_test_window_backtest/2020-04-06_2022-02-08/backtest/20260604_S09_MES_TEST_WINDOW_BACKTEST_CLEAN_RERUN_AFTER_OPUS_REMEDIATION_summary.csv`
- `docs/researchops/s09/mes_test_window_backtest/2020-04-06_2022-02-08/provenance/20260604_S09_MES_TEST_WINDOW_BACKTEST_CLEAN_RERUN_AFTER_OPUS_REMEDIATION_provenance.md`

Boundary:

This consumes exactly one authorized TEST backtest. It is not VALIDATION,
Lockbox, Forward, deployment, trading, promotion, or Git publication.
