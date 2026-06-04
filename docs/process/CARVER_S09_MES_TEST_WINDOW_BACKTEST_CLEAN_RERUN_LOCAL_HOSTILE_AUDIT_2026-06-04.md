# S09 MES TEST Window Backtest Local Hostile Audit

Date: 2026-06-04

Status:

```text
LOCAL_HOSTILE_AUDIT_S09_MES_TEST_BACKTEST_RECORDED_PENDING_SUBAGENT_AUDIT
```

Observed:

- status: CLEAN_S09_MES_TEST_BACKTEST_WRITTEN_AFTER_REMEDIATION_GUARDS_NOT_PROMOTION
- TEST window: 2020-04-06 through 2022-02-08
- scored_completed_dates: 574
- completed_dates_field_scope: SCORING_WINDOW_ONLY_DO_NOT_ADD_STATE_HISTORY
- state_history_completed_dates: 289
- backtest_execution_count: 1
- fractional_trade_event_count: 567
- whole_contract_equivalent_change_count: 1
- validation_lockbox_forward_access: NO
- deployment_trading_promotion: NO

Artifacts:

- `docs/researchops/s09/mes_test_window_backtest/2020-04-06_2022-02-08/guard_checks/20260604_S09_MES_TEST_WINDOW_BACKTEST_CLEAN_RERUN_AFTER_OPUS_REMEDIATION_guard_checks.csv`
- `docs/researchops/s09/mes_test_window_backtest/2020-04-06_2022-02-08/provenance/20260604_S09_MES_TEST_WINDOW_BACKTEST_CLEAN_RERUN_AFTER_OPUS_REMEDIATION_provenance.md`

Hostile audit focus for subagent:

- exactly one TEST backtest receipt exists
- no date beyond 2022-02-08 was admitted
- no VALIDATION, Lockbox, Forward, CFD, old QuantLab, Git, deployment, trading, or promotion path appears
- TEST trade-count and completed-date guards are explicit
