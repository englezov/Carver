# S09 MES Runtime Risk Ledger Renderers Local Hostile Audit

Date: 2026-06-03

Status:

```text
PROCESS_AND_SYNTHETIC_CODE_S09_MES_RUNTIME_RISK_LEDGER_RENDERERS_NOT_DATA_NOT_EXECUTION_NOT_BACKTEST
```

## Scope

This audit covers the synthetic CSV contract renderers:

```text
render_s09_mes_annual_risk_runtime_ledger_csv
render_s09_mes_daily_price_risk_runtime_ledger_csv
```

The renderers support the future, separately authorized S09 MES source-native roll-date normalization and runtime risk/cost execution gate.

Annual-risk ledger header:

```text
completed_trading_date,long_run_annual_risk,current_ewma32_annual_risk,annual_percentage_risk,source_sha256,status
```

Daily price-risk ledger header:

```text
completed_trading_date,current_price,annual_percentage_risk,daily_price_risk_currency,source_sha256,status
```

Allowed annual-risk row status:

```text
LOCKED_SOURCE_NATIVE_ANNUAL_RISK_RUNTIME_VALUE
```

Allowed daily price-risk row status:

```text
LOCKED_SOURCE_NATIVE_DAILY_PRICE_RISK_RUNTIME_VALUE
```

## Formula Guards

The annual-risk renderer rejects rows unless:

```text
annual_percentage_risk = 0.30 * long_run_annual_risk + 0.70 * current_ewma32_annual_risk
```

The daily price-risk renderer rejects rows unless:

```text
daily_price_risk_currency = current_price * annual_percentage_risk / 16
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
- non-positive or non-finite annual-risk inputs
- annual-risk rows that do not match the locked 30/70 blend
- daily price-risk rows that do not match the locked price-risk formula
- missing source SHA256
- invalid source SHA256
- provisional or unlocked row statuses

## Red/Green Evidence

Red check:

```text
ImportError: cannot import name 'S09MESAnnualRiskRuntimeLedgerRow'
FAILED
```

Green checks:

```text
tests.test_s09_mes_readiness_synthetic.S09MESReadinessSyntheticTests.test_mes_runtime_risk_ledger_renderers_output_locked_source_native_values
Ran 1 test
OK

tests.test_s09_mes_readiness_synthetic.S09MESReadinessSyntheticTests.test_mes_runtime_risk_ledger_renderers_fail_closed_on_unlocked_or_inconsistent_values
Ran 1 test
OK

tests.test_s09_mes_readiness_synthetic.S09MESReadinessSyntheticTests.test_mes_runtime_risk_values_require_same_completed_bar_timestamp
Ran 1 test
OK
```

Audit red check:

```text
FileNotFoundError: CARVER_S09_MES_RUNTIME_RISK_LEDGER_RENDERERS_LOCAL_HOSTILE_AUDIT_2026-06-03.md
FAILED
```

## Non-Authorization

These renderers and audit authorize no Databento API access, no provider download, no market-row parsing, no roll execution, no runtime risk execution, no cost extraction, no forecast computation, no diagnostics, no backtests, no OOS, no Lockbox, no Forward, no deployment, no trading, no promotion, and no Git staging, commit, push, PR, or remote operations.
