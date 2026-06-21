# Carver S09 MES NFA Clearing/Regulatory Fee Source Extraction Result

Date: 2026-06-03

Status:

```text
PARTIAL_SOURCE_NATIVE_NFA_ASSESSMENT_FEE_VALUE_EXTRACTED_NOT_FULL_COST_LOCK
```

Authorized execution scope:

```text
clearing/regulatory fee source or policy
```

Scope:

- lane_class: SOURCE_NATIVE_FUTURES
- root: MES
- row_id: APPENDIX_C_174_006
- machinery_development_slice: 2019-05-05 through 2020-04-05
- selected_evidence_name: historical_mes_cost_values

Official sources used:

```text
https://www.nfa.futures.org/rulebooksql/rules.aspx?RuleID=9016&Section=9
https://www.nfa.futures.org/news/PDF/CFTC/2010-2019/20171117-Bylaw-1301-FCM-Assessment-Fee-Increase.pdf
```

Extracted source-native component:

```text
clearing_regulatory_fee: 0.02 USD per side
source interpretation: NFA futures assessment fee
effective_start: 2018-01-01
```

Source notes:

- NFA states that, as of 2018-01-01, the futures assessment fee is 0.02 USD per
  side, invoiced to customers.
- NFA states there is no different assessment fee for futures contracts with
  very small notional value.
- NFA's 2017 filing supports the 2018-01-01 effective date for the increase to
  0.02 USD per side.
- CME's 2019 archive notes CME does not assess member firms an NFA fee; the
  regulatory component is therefore sourced from NFA rather than inferred from
  CME.

Cost evidence outcome:

```text
exchange_fee_value: PARTIAL_SOURCE_NATIVE_CME_EXCHANGE_FEE_VALUE_EXTRACTED_NOT_FULL_COST_LOCK
clearing_regulatory_fee_value: PARTIAL_SOURCE_NATIVE_NFA_ASSESSMENT_FEE_VALUE_EXTRACTED_NOT_FULL_COST_LOCK
historical_mes_cost_values: FAIL_CLOSED_S09_MES_HISTORICAL_COST_VALUES_NOT_LOCKED
```

Remaining blockers:

```text
broker_commission_source_or_policy_with_named_source_or_explicit_policy
spread_slippage_source_or_policy
2020 CME fee schedule coverage for the 2020-01-01 through 2020-04-05 exchange-fee portion of the machinery-development slice
```

Boundary preserved:

No active cost ledger rows were written. No cost computation, risk-adjusted cost
computation, speed eligibility computation, forecast computation, diagnostics,
backtests, TEST, VALIDATION, Lockbox, Forward, deployment, trading, promotion,
Git staging, commit, push, PR, or remote operations were performed.
