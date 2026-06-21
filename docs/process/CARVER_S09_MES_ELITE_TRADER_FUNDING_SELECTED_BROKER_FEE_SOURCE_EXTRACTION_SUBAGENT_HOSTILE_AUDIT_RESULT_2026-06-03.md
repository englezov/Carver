# Carver S09 MES Elite Trader Funding Selected Broker Fee Source Extraction Hostile Audit Result

Date: 2026-06-03

Status:

```text
PASS
```

Orchestration note:

The parent agent spawned subagent Ohm for this hostile audit. Inside the
subagent workspace, the subagent spawn tool itself was not exposed; that does
not affect this audit's role as a spawned hostile audit. No pipeline artifacts
were altered by the audit beyond this audit-result file.

Audit scope:

```text
operator selected Elite Trader Funding as broker venue for fees
broker_commission_source_or_policy
S09 MES APPENDIX_C_174_006
machinery-development slice 2019-05-05 through 2020-04-05
```

Artifacts inspected:

```text
docs/process/CARVER_S09_MES_ELITE_TRADER_FUNDING_SELECTED_BROKER_FEE_SOURCE_EXTRACTION_RESULT_2026-06-03.md
docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/cost_source_extracts/elite_trader_funding_selected_broker_fee_extract.md
docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/cost_source_extracts/20260603_S09_MES_HISTORICAL_COST_SOURCE_EXTRACTION_status.csv
docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/cost_source_extracts/20260603_S09_MES_HISTORICAL_COST_SOURCE_EXTRACTION_sha256.txt
docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/cost/20260603_S09_MES_HISTORICAL_COST_VALUE_ledger.csv
docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/status/20260603_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_status.json
```

Official source verification:

```text
https://help.elitetraderfunding.com/help/commissions-and-exchanges
https://help.elitetraderfunding.com/help/live-elite-turning-strategy-into-income
```

The Elite Trader Funding commissions and exchanges help page supports the
broker-venue context used by the extraction: ETF supports futures products and
lists CME among supported exchanges.

The Elite Trader Funding LIVE ELITE program page supports the fee value used by
the extraction: under trading commissions and fees, micros are listed at
`$0.62`. The artifact interpretation as `0.62 USD per side` is consistent with
the source context and the extraction labels.

Source-boundary finding:

```text
PASS
```

The extracted `broker_commission_value` is correctly marked as:

```text
PARTIAL_SELECTED_BROKER_VENUE_CURRENT_MICRO_COMMISSION_SOURCE_EXTRACTED_NOT_FULL_COST_LOCK
```

The artifacts correctly describe this as a current selected-broker-venue source
captured on 2026-06-03, not as historical 2019/2020 broker-commission evidence.
They require a separate operator policy decision before applying the current ETF
micro fee as a static selected-venue broker commission over the historical
machinery-development slice.

Ledger and evidence-lock finding:

```text
PASS
```

The active historical cost ledger remains header-only:

```text
locked_historical_cost_rows: 0
```

No active cost ledger rows were written, and `historical_mes_cost_values`
remains:

```text
FAIL_CLOSED_S09_MES_HISTORICAL_COST_VALUES_NOT_LOCKED
```

Remaining blockers preserved:

```text
exchange_fee_value: PARTIAL_SOURCE_NATIVE_CME_EXCHANGE_FEE_VALUE_EXTRACTED_NOT_FULL_COST_LOCK
clearing_regulatory_fee_value: PARTIAL_SOURCE_NATIVE_NFA_ASSESSMENT_FEE_VALUE_EXTRACTED_NOT_FULL_COST_LOCK
spread_slippage_policy: FAIL_CLOSED_S09_MES_SPREAD_SLIPPAGE_POLICY_NOT_LOCKED
2020 CME exchange-fee coverage: unresolved for 2020-01-01 through 2020-04-05
historical_mes_cost_values: FAIL_CLOSED_S09_MES_HISTORICAL_COST_VALUES_NOT_LOCKED
```

Global gate finding:

```text
PASS
```

The global S09 MES strategy input evidence completion gate remains fail-closed:

```text
status: FAIL_CLOSED_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_NOT_READY
strategy_input_readiness_status: FAIL_CLOSED_S09_MES_STRATEGY_INPUT_NOT_READY
remaining_evidence_count: 6
```

Contamination and unauthorized-action scan:

```text
PASS
```

No current generic broker rate, silent zero broker commission, CFD broker
assumption, old QuantLab workspace use, active historical cost lock, cost
computation, risk-adjusted cost computation, speed eligibility computation,
forecast computation, diagnostic, backtest, TEST, VALIDATION, Lockbox, Forward,
deployment, trading, promotion, Git staging, commit, push, PR, or remote
publication was found in the audited artifacts or performed during this audit.

Hash manifest:

```text
HASH_MANIFEST_OK
```

Conclusion:

```text
PASS
```

The Elite Trader Funding selected broker fee source extraction is source-native
for the operator-selected broker venue and correctly bounded as current
selected-venue fee evidence only. It does not lock historical MES cost values
and does not move the S09 MES evidence gate out of fail-closed status.
