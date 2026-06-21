# S09 MES VALIDATION Window Backtest Result

Date: 2026-06-04

Status:

```text
PASS_S09_MES_VALIDATION_WINDOW_BACKTEST_EXECUTED_EXACTLY_ONCE_NOT_PROMOTION
```

Scope:

- lane_class: SOURCE_NATIVE_FUTURES
- source_row: APPENDIX_C_174_006
- state_history_window: 2020-04-06 through 2022-02-08
- VALIDATION window: 2022-02-09 through 2023-12-13
- scored_completed_dates: 574
- completed_dates_field_scope: VALIDATION_SCORING_WINDOW_ONLY_DO_NOT_ADD_TEST_STATE_HISTORY
- state_history_completed_dates: 574
- total_state_plus_scoring_completed_dates: 1148
- warmup_bars_required_before_scoring: 257
- forecast_rows: 574
- backtest_rows: 573
- fractional_trade_event_count: 573
- whole_contract_equivalent_change_count: 0
- fractional_turnover_contract_equivalent: 83.47594437435706
- trade_count_sample_definition: FRACTIONAL_CONTRACT_EQUIVALENT_POSITION_CHANGE_EVENTS_ABOVE_NUMERICAL_EPSILON

Scenario summaries:

```json
[
  {
    "scenario_name": "CONSERVATIVE_LIVE_FUTURES_PASS_THROUGH",
    "round_turn_cost_usd": 2.93,
    "validation_window": "2022-02-09 through 2023-12-13",
    "completed_dates": 574,
    "warmup_bars": 257,
    "forecast_rows": 574,
    "backtest_rows": 573,
    "trade_count_position_changes": 573,
    "fractional_trade_event_count": 573,
    "whole_contract_equivalent_change_count": 0,
    "fractional_turnover_contract_equivalent": 83.47594437435706,
    "max_position_change_contract_equivalent": 0.6290804197625715,
    "trade_count_sample_definition": "FRACTIONAL_CONTRACT_EQUIVALENT_POSITION_CHANGE_EVENTS_ABOVE_NUMERICAL_EPSILON",
    "whole_contract_count_definition": "EXECUTABILITY_DIAGNOSTIC_NOT_STATISTICAL_SAMPLE_GATE",
    "gross_pnl_usd": -4241.857073205769,
    "total_cost_usd": 244.5845170168662,
    "net_pnl_usd": -4486.441590222635,
    "mean_net_pnl_usd_per_row": -7.82974099515294,
    "annualized_net_pnl_sharpe_like": -0.6900648874897165,
    "status": "VALIDATION_BACKTEST_RESULT_NOT_LOCKBOX_NOT_FORWARD_NOT_PROMOTION"
  },
  {
    "scenario_name": "ETF_SIM_FEE_ALL_IN_EXCHANGE_NFA_EXCLUDED",
    "round_turn_cost_usd": 2.49,
    "validation_window": "2022-02-09 through 2023-12-13",
    "completed_dates": 574,
    "warmup_bars": 257,
    "forecast_rows": 574,
    "backtest_rows": 573,
    "trade_count_position_changes": 573,
    "fractional_trade_event_count": 573,
    "whole_contract_equivalent_change_count": 0,
    "fractional_turnover_contract_equivalent": 83.47594437435706,
    "max_position_change_contract_equivalent": 0.6290804197625715,
    "trade_count_sample_definition": "FRACTIONAL_CONTRACT_EQUIVALENT_POSITION_CHANGE_EVENTS_ABOVE_NUMERICAL_EPSILON",
    "whole_contract_count_definition": "EXECUTABILITY_DIAGNOSTIC_NOT_STATISTICAL_SAMPLE_GATE",
    "gross_pnl_usd": -4241.857073205769,
    "total_cost_usd": 207.8551014921491,
    "net_pnl_usd": -4449.712174697918,
    "mean_net_pnl_usd_per_row": -7.7656407935391245,
    "annualized_net_pnl_sharpe_like": -0.6844034571595802,
    "status": "VALIDATION_BACKTEST_RESULT_NOT_LOCKBOX_NOT_FORWARD_NOT_PROMOTION"
  }
]
```

Artifacts:

- `docs/researchops/s09/mes_validation_window_backtest/2022-02-09_2023-12-13/status/20260604_S09_MES_VALIDATION_WINDOW_BACKTEST_status.json`
- `docs/researchops/s09/mes_validation_window_backtest/2022-02-09_2023-12-13/status/20260604_S09_MES_VALIDATION_WINDOW_BACKTEST_backtest_execution_receipt.json`
- `docs/researchops/s09/mes_validation_window_backtest/2022-02-09_2023-12-13/backtest/20260604_S09_MES_VALIDATION_WINDOW_BACKTEST_summary.csv`
- `docs/researchops/s09/mes_validation_window_backtest/2022-02-09_2023-12-13/provenance/20260604_S09_MES_VALIDATION_WINDOW_BACKTEST_provenance.md`

Boundary:

This consumes exactly one authorized VALIDATION backtest. It is not Lockbox,
Forward, deployment, trading, promotion, or Git publication.
