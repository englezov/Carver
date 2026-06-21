# S09 MES Cost Ledger Renderers Local Hostile Audit

Date: 2026-06-03

Status:

```text
PROCESS_AND_SYNTHETIC_CODE_S09_MES_COST_LEDGER_RENDERERS_NOT_DATA_NOT_EXECUTION_NOT_BACKTEST
```

## Scope

This audit covers the synthetic CSV contract renderers:

```text
render_s09_mes_cost_value_ledger_csv
render_s09_mes_risk_adjusted_cost_ledger_csv
```

The renderers support the future, separately authorized S09 MES source-native roll-date normalization and runtime risk/cost execution gate.

Cost-value ledger header:

```text
completed_trading_date,component_name,amount_currency,currency,charge_timing,effective_start,effective_end,source_label,source_sha256,status
```

Risk-adjusted cost ledger header:

```text
completed_trading_date,total_cost_per_trade_currency,daily_price_risk_currency,risk_adjusted_cost_per_trade_sr,status
```

Allowed cost-value row status:

```text
LOCKED_SOURCE_NATIVE_COST_COMPONENT_VALUE
```

Allowed risk-adjusted row status:

```text
LOCKED_SOURCE_NATIVE_RISK_ADJUSTED_COST_VALUE
```

## Formula And Source Guards

The cost-value renderer rejects rows unless:

- component name is one of the locked MES cost components;
- currency is USD;
- charge timing is `PER_SIDE` or `ROUND_TURN`;
- effective dates are exact completed dates and cover the completed trading date;
- source label and SHA256 are present and valid;
- row status is locked.

The risk-adjusted renderer rejects rows unless:

```text
risk_adjusted_cost_per_trade_sr = total_cost_per_trade_currency / daily_price_risk_currency
```

## Oldest Data Rule

The renderers are intended for the locked Development/Reconciliation window:

```text
2022-01-03 through 2023-12-29
```

Rows must preserve oldest authorized completed source-native data first. Later data must not shape parameters, thresholds, filters, costs, speed selection, FDM selection, or rescue choices.

## Hostile Checks

The synthetic hostile tests reject:

- empty ledgers
- datetime values where exact completed `date` values are required
- non-required cost component names
- negative or non-finite cost values
- non-USD currency
- unresolved charge timing
- effective ranges that do not cover the completed trading date
- missing source labels
- missing or invalid source SHA256
- risk-adjusted rows that do not match the locked total-cost-over-risk formula
- provisional or unlocked row statuses

## Red/Green Evidence

Red check:

```text
ImportError: cannot import name 'S09MESCostValueLedgerRow'
FAILED
```

Green checks:

```text
tests.test_s09_mes_readiness_synthetic.S09MESReadinessSyntheticTests.test_mes_cost_ledger_renderers_output_locked_source_native_cost_values
Ran 1 test
OK

tests.test_s09_mes_readiness_synthetic.S09MESReadinessSyntheticTests.test_mes_cost_ledger_renderers_fail_closed_on_unlocked_or_inconsistent_values
Ran 1 test
OK

tests.test_s09_mes_readiness_synthetic.S09MESReadinessSyntheticTests.test_mes_cost_and_risk_adjusted_cost_ledgers_use_locked_components_only
Ran 1 test
OK
```

Audit red check:

```text
FileNotFoundError: CARVER_S09_MES_COST_LEDGER_RENDERERS_LOCAL_HOSTILE_AUDIT_2026-06-03.md
FAILED
```

## Non-Authorization

These renderers and audit authorize no Databento API access, no provider download, no market-row parsing, no roll execution, no runtime risk execution, no cost extraction, no forecast computation, no diagnostics, no backtests, no OOS, no Lockbox, no Forward, no deployment, no trading, no promotion, and no Git staging, commit, push, PR, or remote operations.
