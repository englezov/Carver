# Carver S09 MES NFA Clearing/Regulatory Fee Source Extraction Hostile Audit Result

Date: 2026-06-03

Verdict:

```text
PASS
```

Orchestration note:

The parent agent spawned subagent Galileo for this hostile audit. Inside the
subagent workspace, the subagent spawn tool itself was not exposed; that does
not affect this audit's role as a spawned hostile audit. No pipeline artifacts
were altered by the audit beyond this audit-result file.

Audit scope:

```text
operator authorized only: clearing/regulatory fee source or policy
```

Audited artifacts:

```text
docs/process/CARVER_S09_MES_NFA_CLEARING_REGULATORY_FEE_SOURCE_EXTRACTION_RESULT_2026-06-03.md
docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/cost_source_extracts/nfa_2018_futures_assessment_fee_clearing_regulatory_extract.md
docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/cost_source_extracts/20260603_S09_MES_HISTORICAL_COST_SOURCE_EXTRACTION_status.csv
docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/cost/20260603_S09_MES_HISTORICAL_COST_VALUE_ledger.csv
docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/cost/20260603_S09_MES_HISTORICAL_COST_VALUE_status.json
docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/evidence/20260603_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_required_evidence_ledger.csv
docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/status/20260603_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_status.json
```

Official source verification:

- PASS: The official NFA Bylaw 1301 assessment-fee Q&A supports a futures
  assessment fee of 0.02 USD per side effective 2018-01-01.
- PASS: The same official NFA Q&A states there is no different assessment fee
  for futures contracts with very small notional value.
- PASS: The official 2017 NFA filing supports the 2018-01-01 effective date for
  the increase to 0.02 USD per side.
- PASS: The extraction sources the regulatory fee from NFA, not from CME or an
  inferred CME clearing value.

Official sources checked:

```text
https://www.nfa.futures.org/rulebooksql/rules.aspx?RuleID=9016&Section=9
https://www.nfa.futures.org/news/PDF/CFTC/2010-2019/20171117-Bylaw-1301-FCM-Assessment-Fee-Increase.pdf
```

Scope containment:

- PASS: The result status is partial source-native NFA assessment-fee source
  extraction, not a full historical MES cost lock.
- PASS: `historical_mes_cost_values` remains
  `FAIL_CLOSED_S09_MES_HISTORICAL_COST_VALUES_NOT_LOCKED`.
- PASS: The active cost ledger remains header-only with zero locked historical
  cost rows.
- PASS: Broker commission remains unresolved/fail-closed.
- PASS: Spread/slippage remains unresolved/fail-closed.
- PASS: 2020 CME exchange-fee coverage remains unresolved for the
  2020-01-01 through 2020-04-05 portion of the machinery-development slice.
- PASS: Risk-adjusted cost remains blocked/unlocked.
- PASS: Speed eligibility remains blocked/unlocked.
- PASS: The global S09 evidence gate remains fail-closed with
  `remaining_evidence_count` equal to `6`.

Forbidden action scan:

- PASS: No diagnostics, backtests, TEST, VALIDATION, Lockbox, Forward,
  deployment, trading, promotion, Git staging, commit, push, PR, CFD adapter
  work, QuantLab reuse, current-fee default, unofficial mirror, or user-agent
  evasion was found in the clearing/regulatory extraction artifacts.

Residual blockers:

```text
broker_commission_source_or_policy
spread_slippage_source_or_policy
2020 CME fee schedule coverage for 2020-01-01 through 2020-04-05
historical_mes_cost_values lock
risk_adjusted_cost_values
speed_eligibility_values
eligible_speed_set
table36_fdm_row
hash_bound_provenance
```

Conclusion:

The S09 MES clearing/regulatory fee extraction is acceptable as a bounded,
official NFA source-native partial extraction for `0.02 USD per side` effective
2018-01-01. It must not be promoted as a complete historical MES cost lock or
used for risk-adjusted cost, speed eligibility, diagnostics, or backtests until
the remaining cost blockers and evidence gate requirements are separately
authorized, source-locked, and verified.
