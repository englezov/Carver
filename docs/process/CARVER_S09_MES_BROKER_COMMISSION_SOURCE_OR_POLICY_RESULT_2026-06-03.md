# Carver S09 MES Broker Commission Source Or Policy Result

Date: 2026-06-03

Status:

```text
SUPERSEDED_BY_ELITE_TRADER_FUNDING_SELECTED_BROKER_FEE_SOURCE_EXTRACTION
```

Authorized execution scope:

```text
broker_commission_source_or_policy
```

Scope:

- lane_class: SOURCE_NATIVE_FUTURES
- root: MES
- row_id: APPENDIX_C_174_006
- machinery_development_slice: 2019-05-05 through 2020-04-05
- selected_evidence_name: historical_mes_cost_values

Result:

The broker commission gate was authorized, but no broker, account commission
schedule, contractual commission source, or explicit no-broker-cost policy was
specified. Because CME identifies broker commissions as broker-specific, this
lane remains fail-closed for broker commission.

Supersession note:

After this fail-closed result was recorded, the operator selected Elite Trader
Funding as the broker venue for fees. See:

```text
docs/process/CARVER_S09_MES_ELITE_TRADER_FUNDING_SELECTED_BROKER_FEE_SOURCE_EXTRACTION_RESULT_2026-06-03.md
```

Rejected actions:

```text
do not invent a broker commission
do not use a current generic broker rate
do not silently set broker commission to zero
do not treat CME exchange fees as broker commission
do not use CFD broker assumptions
```

Cost evidence outcome:

```text
exchange_fee_value: PARTIAL_SOURCE_NATIVE_CME_EXCHANGE_FEE_VALUE_EXTRACTED_NOT_FULL_COST_LOCK
clearing_regulatory_fee_value: PARTIAL_SOURCE_NATIVE_NFA_ASSESSMENT_FEE_VALUE_EXTRACTED_NOT_FULL_COST_LOCK
broker_commission_value: FAIL_CLOSED_S09_MES_BROKER_COMMISSION_SOURCE_OR_POLICY_NOT_SPECIFIED
historical_mes_cost_values: FAIL_CLOSED_S09_MES_HISTORICAL_COST_VALUES_NOT_LOCKED
```

Next required action:

```text
Operator must name a broker/source, provide an official or contractual commission schedule, or explicitly authorize a fail-closed/no-broker-cost policy for this research lane.
```

Other remaining blockers:

```text
spread_slippage_source_or_policy
2020 CME fee schedule coverage for the 2020-01-01 through 2020-04-05 exchange-fee portion of the machinery-development slice
```

Boundary preserved:

No active cost ledger rows were written. No cost computation, risk-adjusted cost
computation, speed eligibility computation, forecast computation, diagnostics,
backtests, TEST, VALIDATION, Lockbox, Forward, deployment, trading, promotion,
Git staging, commit, push, PR, or remote operations were performed.
