# S09 MES NFA Futures Assessment Fee Clearing/Regulatory Extract

Date: 2026-06-03

Status:

```text
PARTIAL_SOURCE_NATIVE_COST_SOURCE_EXTRACTION_CLEARING_REGULATORY_ONLY_NOT_HISTORICAL_COST_LOCK
```

Authorized route:

```text
clearing/regulatory fee source or policy
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

Official NFA source:

```text
https://www.nfa.futures.org/rulebooksql/rules.aspx?RuleID=9016&Section=9
```

Official NFA historical amendment support:

```text
https://www.nfa.futures.org/news/PDF/CFTC/2010-2019/20171117-Bylaw-1301-FCM-Assessment-Fee-Increase.pdf
```

Extracted clearing/regulatory source value:

```text
component_name: clearing_regulatory_fee
source_component_interpretation: NFA futures assessment fee
amount_currency: 0.02
currency: USD
charge_timing: PER_SIDE
effective_start: 2018-01-01
effective_end: not bounded within the authorized machinery-development slice by this extract
```

Source basis:

- NFA assessment-fee Q&A states that, as of 2018-01-01, the NFA assessment fee
  for futures contracts is 0.02 USD per side, invoiced to customers.
- The same NFA Q&A states there is no different assessment fee for futures
  contracts with very small notional value.
- The NFA 2017 filing describes the Bylaw 1301 amendment to increase the
  futures assessment fee to 0.02 USD per side effective 2018-01-01.
- The CME 2019 fee schedule archive notes that CME does not assess member firms
  an NFA fee and points NFA questions outside CME; therefore this component is
  sourced from NFA, not inferred from CME.

Cost evidence outcome:

```text
clearing_regulatory_fee_value: PARTIAL_SOURCE_NATIVE_NFA_ASSESSMENT_FEE_VALUE_EXTRACTED_NOT_FULL_COST_LOCK
historical_mes_cost_values: FAIL_CLOSED_S09_MES_HISTORICAL_COST_VALUES_NOT_LOCKED
```

Remaining cost blockers:

```text
broker_commission: not locked; CME FAQ states commissions are broker-specific.
spread_slippage: not locked; no source-native spread/slippage source or conservative policy has been authorized.
full exchange-fee coverage through 2020-04-05: not fully covered by the 2019 CME archive extraction.
```

Boundary preserved:

No cost computation, risk-adjusted cost computation, speed eligibility
computation, forecast computation, diagnostics, backtests, TEST, VALIDATION,
Lockbox, Forward, deployment, trading, promotion, Git staging, commit, push,
PR, or remote operations were performed.
