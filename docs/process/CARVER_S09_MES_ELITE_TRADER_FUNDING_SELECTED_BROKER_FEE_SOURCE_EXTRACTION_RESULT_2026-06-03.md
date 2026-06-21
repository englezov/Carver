# Carver S09 MES Elite Trader Funding Selected Broker Fee Source Extraction Result

Date: 2026-06-03

Status:

```text
PARTIAL_SELECTED_BROKER_VENUE_CURRENT_MICRO_COMMISSION_SOURCE_EXTRACTED_NOT_HISTORICAL_COST_LOCK
```

Authorized execution scope:

```text
broker_commission_source_or_policy
```

Operator-selected broker venue:

```text
Elite Trader Funding
```

Scope:

- lane_class: SOURCE_NATIVE_FUTURES
- root: MES
- row_id: APPENDIX_C_174_006
- machinery_development_slice: 2019-05-05 through 2020-04-05
- selected_evidence_name: historical_mes_cost_values

Official sources used:

```text
https://help.elitetraderfunding.com/help/commissions-and-exchanges
https://help.elitetraderfunding.com/help/live-elite-turning-strategy-into-income
```

Extracted selected-broker-venue component:

```text
broker_commission: 0.62 USD per side
source interpretation: Elite Trader Funding current micro trading commission/fee
source temporal scope: current official help-center policy captured 2026-06-03
```

Temporal limitation:

This source is not historical 2019/2020 broker-commission evidence. It is a
current selected-broker-venue source. Applying it to the 2019-05-05 through
2020-04-05 machinery-development slice as a static broker-commission policy
requires separate explicit operator authorization.

Cost evidence outcome:

```text
exchange_fee_value: PARTIAL_SOURCE_NATIVE_CME_EXCHANGE_FEE_VALUE_EXTRACTED_NOT_FULL_COST_LOCK
clearing_regulatory_fee_value: PARTIAL_SOURCE_NATIVE_NFA_ASSESSMENT_FEE_VALUE_EXTRACTED_NOT_FULL_COST_LOCK
broker_commission_value: PARTIAL_SELECTED_BROKER_VENUE_CURRENT_MICRO_COMMISSION_SOURCE_EXTRACTED_NOT_FULL_COST_LOCK
historical_mes_cost_values: FAIL_CLOSED_S09_MES_HISTORICAL_COST_VALUES_NOT_LOCKED
```

Remaining blockers:

```text
operator policy decision: whether current Elite Trader Funding micro commission may be applied as static selected-venue broker commission over the historical machinery-development slice
spread_slippage_source_or_policy
2020 CME fee schedule coverage for the 2020-01-01 through 2020-04-05 exchange-fee portion of the machinery-development slice
```

Boundary preserved:

No active cost ledger rows were written. No cost computation, risk-adjusted cost
computation, speed eligibility computation, forecast computation, diagnostics,
backtests, TEST, VALIDATION, Lockbox, Forward, deployment, trading, promotion,
Git staging, commit, push, PR, or remote operations were performed.
