# Carver S09 MES Official CME 2019 Fee Schedule Archive Exchange Fee Subagent Hostile Audit Result

Date: 2026-06-03

Status:

```text
PASS_WITH_NON_BLOCKING_ARTIFACT_COLUMN_REFERENCE_FINDING
```

Scope audited:

```text
official_cme_2019_fee_schedule_archive_permitted_route
```

Operator-provided source:

```text
C:\Users\openclaw\Desktop\cme-fee-schedules-2019.zip
```

Audited Carver workspace:

```text
C:\Users\openclaw\Desktop\Carver
```

## Verdict

The official CME archive handling passes the source-native boundary audit for this narrow route.

The operator-provided CME 2019 ZIP was copied into the S09 machinery-development evidence tree and hash-bound. The copied workspace ZIP has the same SHA256 observed for the Desktop ZIP:

```text
08347421A83E53258BB0D9CE3682F9C73A46D3A708031A649310BF1D74C600DF
```

The extracted CME exchange-fee value `0.20 USD per side` is present in the official 2019 CME XLS schedules on the actual `Non-Members` account group, `Globex - Outrights` transaction row, and `Micro E-mini Index` futures column. The ambiguous rows whose account labels contain `See Non-Members` were not used as the source row for the extracted value.

## Direct XLS Check

Independent read of the official archive XLS files found:

```text
cme-fee-schedule-2019-05-06.xls | Equity | Non-Members group | row 36 | Globex - Outrights | Micro E-mini Index Futures | 0.20
cme-fee-schedule-2019-07-01.xls | Equity | Non-Members group | row 36 | Globex - Outrights | Micro E-mini Index Futures | 0.20
cme-fee-schedule-2019-08-01.xls | Equity | Non-Members group | row 36 | Globex - Outrights | Micro E-mini Index Futures | 0.20
cme-fee-schedule-2019-09-09.xls | Equity | Non-Members group | row 36 | Globex - Outrights | Micro E-mini Index Futures | 0.20
cme-fee-schedule-2019-10-01.xls | Equity | Non-Members group | row 36 | Globex - Outrights | Micro E-mini Index Futures | 0.20
```

Direct header check found `Micro E-mini Index` on the Equity sheet header, with `Futures` underneath it. The direct row read shows the `0.20` value in the Micro E-mini Index futures column for the row 36 `Globex - Outrights` entry under the row 35 `Non-Members` group label.

## Non-Blocking Finding

The exchange-fee extract artifact states `row 36 | column 10` for the `0.20` values. Direct XLS reading shows physical column 10 contains `0.55`; the `0.20` Micro E-mini Index futures value is in physical column 11. This is an artifact column-reference defect, not a value-source defect, because the artifact's product/row/value selection is otherwise correct:

```text
Non-Members / Globex - Outrights / Micro E-mini Index = 0.20 USD per side
```

This should be corrected before promoting the extract into any stricter value-lock artifact, but it does not imply that a wrong fee value was selected.

## Boundaries Preserved

The following remain fail-closed or unlocked:

```text
clearing_regulatory_fee_value: FAIL_CLOSED
broker_commission_value: FAIL_CLOSED
spread_slippage_policy: FAIL_CLOSED
2020 CME fee schedule coverage: NOT LOCKED
historical_mes_cost_values: FAIL_CLOSED / NOT LOCKED
risk_adjusted_cost: NOT COMPUTED
speed_eligibility: NOT COMPUTED
```

The active historical MES cost value ledger remains header-only with zero locked rows.

The strategy input completion status remains:

```text
FAIL_CLOSED_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_NOT_READY
```

The locked evidence list remains limited to:

```text
official_lifecycle_evidence
roll_trading_day_semantics
annual_risk_runtime_values
daily_price_risk_values
```

`historical_mes_cost_values` is not locked.

## Contamination / Authorization Checks

No evidence was found of:

```text
backtests
diagnostics
TEST access
VALIDATION access
Lockbox access
Forward access
deployment
trading
promotion
Git staging
commit
push
PR
CFD assumptions
QuantLab_v3 reuse
unofficial mirrors
current-fee defaults
user-agent evasion
```

## Final Audit Classification

```text
PASS_WITH_NON_BLOCKING_ARTIFACT_COLUMN_REFERENCE_FINDING
```

The official CME archive copy/hash binding and exchange-fee source extraction are acceptable for this narrow source-extraction stage, subject to correcting the artifact's physical column reference before any later value-lock promotion. All remaining cost components and downstream computations correctly remain fail-closed.
