# S09 MES Elite Trader Funding Selected Broker Fee Extract

Date: 2026-06-03

Status:

```text
STATIC_SELECTED_BROKER_POLICY_LOCKED_FOR_HISTORICAL_SIMULATION_USE
```

Authorized route:

```text
broker_commission_source_or_policy
```

Operator-selected broker venue:

```text
Elite Trader Funding
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

Scope:

- root: MES
- row_id: APPENDIX_C_174_006
- machinery_development_slice: 2019-05-05 through 2020-04-05
- selected_evidence_name: historical_mes_cost_values

Official Elite Trader Funding source:

```text
https://help.elitetraderfunding.com/help/live-elite-turning-strategy-into-income
```

Official broker-venue context source:

```text
https://help.elitetraderfunding.com/help/commissions-and-exchanges
```

Extracted selected-broker-venue fee source:

```text
component_name: broker_commission
source_component_interpretation: Elite Trader Funding trading commissions and fees for micros
amount_currency: 0.62
currency: USD
charge_timing: PER_SIDE
source_temporal_scope: current official help-center policy captured 2026-06-03
```

Source basis:

- Elite Trader Funding's commissions and exchanges guide states that ETF
  supports futures products and supports CME.
- Elite Trader Funding's LIVE ELITE program information lists trading
  commissions and fees with `Micros: $0.62`.

Temporal limitation:

This is a selected-broker-venue current fee source, not historical 2019/2020
broker-commission evidence. On 2026-06-03, the operator authorized this current
Elite Trader Funding micro fee as a static selected-venue broker commission
policy for historical simulation use over the machinery-development slice. It
must not be relabeled as historical broker evidence.

Operator static policy lock:

```text
broker_commission_value: LOCKED_SELECTED_BROKER_STATIC_POLICY_ETF_CURRENT_MICRO_COMMISSION_0_62_PER_SIDE
component_name: broker_commission
amount_currency: 0.62
currency: USD
charge_timing: PER_SIDE
simulation_policy_scope: static selected-venue broker commission over the machinery-development historical slice
correction_policy: any replacement after result exposure invalidates affected scored/run evidence
```

Cost evidence outcome:

```text
broker_commission_value: LOCKED_SELECTED_BROKER_STATIC_POLICY_ETF_CURRENT_MICRO_COMMISSION_0_62_PER_SIDE
historical_mes_cost_values: FAIL_CLOSED_S09_MES_HISTORICAL_COST_VALUES_NOT_LOCKED
```

Remaining blockers:

```text
spread_slippage_tbbo_source_native_extraction_and_degraded_day_policy_lock
```

Boundary preserved:

No active cost ledger rows were written. No cost computation, risk-adjusted cost
computation, speed eligibility computation, forecast computation, diagnostics,
backtests, TEST, VALIDATION, Lockbox, Forward, deployment, trading, promotion,
Git staging, commit, push, PR, or remote operations were performed.
