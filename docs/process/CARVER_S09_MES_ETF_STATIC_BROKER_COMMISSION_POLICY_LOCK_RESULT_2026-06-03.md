# S09 MES ETF Static Broker Commission Policy Lock Result

Date: 2026-06-03

Status:

```text
LOCKED_SELECTED_BROKER_STATIC_POLICY_ETF_CURRENT_MICRO_COMMISSION
```

Authorized execution scope:

```text
broker_current_fee_static_historical_policy
```

Scope:

- lane_class: SOURCE_NATIVE_FUTURES
- root: MES
- row_id: APPENDIX_C_174_006
- machinery_development_slice: 2019-05-05 through 2020-04-05
- selected_evidence_name: historical_mes_cost_values
- operator_policy_authorization: apply current Elite Trader Funding micro fee as static selected-venue broker commission

Locked selected-broker policy:

```text
broker_commission_value: LOCKED_SELECTED_BROKER_STATIC_POLICY_ETF_CURRENT_MICRO_COMMISSION_0_62_PER_SIDE
component_name: broker_commission
selected_broker_venue: Elite Trader Funding
amount_currency: 0.62
currency: USD
charge_timing: PER_SIDE
source_temporal_scope: current official help-center policy captured 2026-06-03
simulation_policy_scope: static selected-venue broker commission over the machinery-development historical slice
correction_policy: any replacement after result exposure invalidates affected scored/run evidence
```

Interpretation:

The operator explicitly selected the best available current broker venue fee for
this pre-backtest research state. This is a locked policy input for broker
commission only. It is not evidence that Elite Trader Funding charged this fee
in 2019 or 2020, and it must not be relabeled as historical broker evidence.

Cost evidence outcome:

```text
exchange_fee_value: SOURCE_NATIVE_CME_EXCHANGE_FEE_VALUE_EXTRACTED_FULL_MACHINERY_SLICE_NOT_FULL_COST_LOCK
clearing_regulatory_fee_value: PARTIAL_SOURCE_NATIVE_NFA_ASSESSMENT_FEE_VALUE_EXTRACTED_NOT_FULL_COST_LOCK
broker_commission_value: LOCKED_SELECTED_BROKER_STATIC_POLICY_ETF_CURRENT_MICRO_COMMISSION_0_62_PER_SIDE
spread_slippage_policy: AUTHORIZED_TBBO_BOUNDED_RAW_ACQUISITION_COMPLETED_NO_SPREAD_LOCK
historical_mes_cost_values: FAIL_CLOSED_S09_MES_HISTORICAL_COST_VALUES_NOT_LOCKED
```

Remaining blocker:

```text
spread_slippage_tbbo_source_native_extraction_and_degraded_day_policy_lock
```

Boundary preserved:

No active cost ledger rows were written. No spread/slippage extraction, cost
computation, risk-adjusted cost computation, speed eligibility computation,
forecast computation, diagnostics, backtests, TEST, VALIDATION, Lockbox,
Forward, deployment, trading, promotion, Git staging, commit, push, PR, or
remote operations were performed.

Explicit no-action checklist:

- no Databento API access
- no provider login
- no source extraction
- no market-row parsing
- no cost computation
- no risk-adjusted cost computation
- no speed eligibility computation
- no forecast computation
- no diagnostics
- no backtests
- no TEST
- no VALIDATION
- no Lockbox
- no Forward
- no deployment
- no trading
- no promotion
- no Git staging, commit, push, PR, or remote operations
