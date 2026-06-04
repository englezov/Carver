# S09 MES Speed And Status Renderers Local Hostile Audit

Date: 2026-06-03

Status:

```text
PROCESS_AND_SYNTHETIC_CODE_S09_MES_SPEED_STATUS_RENDERERS_NOT_DATA_NOT_EXECUTION_NOT_BACKTEST
```

## Scope

This audit covers the synthetic CSV and JSON contract renderers:

```text
render_s09_mes_speed_eligibility_ledger_csv
render_s09_mes_roll_risk_cost_execution_status_json
```

The renderers support the future, separately authorized S09 MES source-native roll-date normalization and runtime risk/cost execution gate.

Speed ledger header:

```text
span,turnover,risk_adjusted_cost_per_trade_sr,threshold_sr,eligible,status
```

Allowed speed row status:

```text
LOCKED_SOURCE_NATIVE_SPEED_ELIGIBILITY_VALUE
```

Allowed execution status values:

```text
READY_FOR_S09_MES_DEV_RECON_FORECAST_INPUT_GATE_NOT_BACKTEST
FAIL_CLOSED_S09_MES_STRATEGY_INPUT_NOT_READY
```

## Speed Guards

The speed renderer rejects rows unless:

- span is one of the locked EWMAC spans: 2, 4, 8, 16, 32, 64;
- turnover matches the locked MES EWMAC turnover table;
- threshold is locked to `0.15` SR;
- eligibility matches `turnover * risk_adjusted_cost_per_trade_sr <= threshold_sr`;
- row status is locked.

## Status Guards

The status JSON renderer rejects payloads unless:

- `databento_api_access` is `NO`;
- `new_provider_data_download` is `NO`;
- `market_row_parsing` is `NO`;
- ready status pairs with `S09_MES_STRATEGY_INPUT_READY_DEV_RECON_ONLY`;
- fail-closed status pairs with `FAIL_CLOSED_S09_MES_STRATEGY_INPUT_NOT_READY`.

## Oldest Data Rule

The renderers are intended for the locked Development/Reconciliation window:

```text
2022-01-03 through 2023-12-29
```

Rows must preserve oldest authorized completed source-native data first. Later data must not shape parameters, thresholds, filters, costs, speed selection, FDM selection, or rescue choices.

## Hostile Checks

The synthetic hostile tests reject:

- empty speed ledgers
- non-locked EWMAC spans
- turnover values that do not match the locked table
- non-positive risk-adjusted cost
- threshold drift away from `0.15` SR
- eligibility flags that do not match the locked cost screen
- provisional or unlocked speed statuses
- unauthorized status JSON values
- status JSON showing API access, provider download, or market-row parsing
- ready/fail-closed status pair mismatches

## Red/Green Evidence

Red check:

```text
ImportError: cannot import name 'S09MESRollRiskCostExecutionStatus'
FAILED
```

Green checks:

```text
tests.test_s09_mes_readiness_synthetic.S09MESReadinessSyntheticTests.test_mes_speed_eligibility_and_status_renderers_output_locked_contracts
Ran 1 test
OK

tests.test_s09_mes_readiness_synthetic.S09MESReadinessSyntheticTests.test_mes_speed_eligibility_and_status_renderers_fail_closed_on_contract_drift
Ran 1 test
OK

tests.test_s09_mes_readiness_synthetic.S09MESReadinessSyntheticTests.test_mes_speed_eligibility_status_can_feed_readiness_only_after_locks
Ran 1 test
OK
```

Audit red check:

```text
FileNotFoundError: CARVER_S09_MES_SPEED_STATUS_RENDERERS_LOCAL_HOSTILE_AUDIT_2026-06-03.md
FAILED
```

## Non-Authorization

These renderers and audit authorize no Databento API access, no provider download, no market-row parsing, no roll execution, no runtime risk execution, no cost extraction, no forecast computation, no diagnostics, no backtests, no OOS, no Lockbox, no Forward, no deployment, no trading, no promotion, and no Git staging, commit, push, PR, or remote operations.
