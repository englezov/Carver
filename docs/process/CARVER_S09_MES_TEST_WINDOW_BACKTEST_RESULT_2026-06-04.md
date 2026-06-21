# S09 MES TEST Window Backtest Result

Date: 2026-06-04

Status:

```text
PASS_S09_MES_TEST_WINDOW_BACKTEST_EXECUTED_EXACTLY_ONCE_NOT_PROMOTION
```

Scope:

- lane_class: SOURCE_NATIVE_FUTURES
- source_row: APPENDIX_C_174_006
- TEST window: 2020-04-06 through 2022-02-08
- completed_dates: 574
- warmup_bars_inside_test_window: 257
- forecast_rows: 318
- backtest_rows: 317
- trade_count_position_changes: 317
- data_access_for_this_execution: no new Databento API call; used existing authorized TEST download
- degraded_ohlcv_policy: SOURCE_NATIVE_DEGRADED_OHLCV_OPERATOR_POLICY_LOCKED

Scenario summaries:

```json
[
  {
    "scenario_name": "CONSERVATIVE_LIVE_FUTURES_PASS_THROUGH",
    "round_turn_cost_usd": 2.93,
    "test_window": "2020-04-06 through 2022-02-08",
    "completed_dates": 574,
    "warmup_bars": 257,
    "forecast_rows": 318,
    "backtest_rows": 317,
    "trade_count_position_changes": 317,
    "gross_pnl_usd": 470.33659217806064,
    "total_cost_usd": 116.45318209447889,
    "net_pnl_usd": 353.8834100835814,
    "mean_net_pnl_usd_per_row": 1.1163514513677646,
    "annualized_net_pnl_sharpe_like": 0.12395133705769155,
    "status": "TEST_BACKTEST_RESULT_NOT_VALIDATION_NOT_LOCKBOX_NOT_PROMOTION"
  },
  {
    "scenario_name": "ETF_SIM_FEE_ALL_IN_EXCHANGE_NFA_EXCLUDED",
    "round_turn_cost_usd": 2.49,
    "test_window": "2020-04-06 through 2022-02-08",
    "completed_dates": 574,
    "warmup_bars": 257,
    "forecast_rows": 318,
    "backtest_rows": 317,
    "trade_count_position_changes": 317,
    "gross_pnl_usd": 470.33659217806064,
    "total_cost_usd": 98.96533222363566,
    "net_pnl_usd": 371.37125995442494,
    "mean_net_pnl_usd_per_row": 1.1715181702032333,
    "annualized_net_pnl_sharpe_like": 0.13007553740930972,
    "status": "TEST_BACKTEST_RESULT_NOT_VALIDATION_NOT_LOCKBOX_NOT_PROMOTION"
  }
]
```

Artifacts:

- `docs/researchops/s09/mes_test_window_backtest/2020-04-06_2022-02-08/status/20260604_S09_MES_TEST_WINDOW_BACKTEST_status.json`
- `docs/researchops/s09/mes_test_window_backtest/2020-04-06_2022-02-08/status/20260604_S09_MES_TEST_WINDOW_BACKTEST_backtest_execution_receipt.json`
- `docs/researchops/s09/mes_test_window_backtest/2020-04-06_2022-02-08/backtest/20260604_S09_MES_TEST_WINDOW_BACKTEST_summary.csv`
- `docs/researchops/s09/mes_test_window_backtest/2020-04-06_2022-02-08/provenance/20260604_S09_MES_TEST_WINDOW_BACKTEST_provenance.md`

Boundary:

This consumes exactly one authorized TEST backtest. It is not VALIDATION,
Lockbox, Forward, deployment, trading, promotion, or Git publication.
