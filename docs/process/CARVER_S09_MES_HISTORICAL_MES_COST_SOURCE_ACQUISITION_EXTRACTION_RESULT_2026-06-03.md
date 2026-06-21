# Carver S09 MES Historical MES Cost Source Acquisition Extraction Result

Date: 2026-06-03

Status:

```text
PARTIAL_SOURCE_LOCATION_LOCK_HISTORICAL_MES_COST_VALUES_FAIL_CLOSED
```

Authorized execution scope:

```text
source-native historical MES cost source acquisition/extraction
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

Scope:

- source_row: APPENDIX_C_174_006
- root: MES
- machinery_development_slice: 2019-05-05 through 2020-04-05
- runtime_input_lock_scope: oldest minimum machinery-development slice only
- design_ordering: oldest authorized completed source-native data first

Source acquisition performed:

- located official CME historical-fees source page;
- located official CME 2019 historical schedule URL;
- attempted official CME 2019 fee schedule archive retrieval;
- captured the CME automated-access blocker;
- captured official CME Micro E-mini fee-routing context;
- captured official CME SER-8360 MES launch context.

Result:

```text
historical_fee_schedule_source_location: LOCKED_SOURCE_LOCATION_ONLY
mes_fee_schedule_context: LOCKED_SOURCE_LOCATION_ONLY
exchange_fee_value: FAIL_CLOSED_S09_MES_EXCHANGE_FEE_VALUE_NOT_EXTRACTED
clearing_regulatory_fee_value: FAIL_CLOSED_S09_MES_CLEARING_REGULATORY_FEE_VALUE_NOT_EXTRACTED
broker_commission_value: FAIL_CLOSED_S09_MES_BROKER_COMMISSION_SOURCE_NOT_NAMED
spread_slippage_policy: FAIL_CLOSED_S09_MES_SPREAD_SLIPPAGE_POLICY_NOT_LOCKED
historical_mes_cost_values: FAIL_CLOSED_S09_MES_HISTORICAL_COST_VALUES_NOT_LOCKED
```

Artifacts:

- `docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/cost_source_extracts/cme_historical_fees_2019_source_location_extract.md`
- `docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/cost_source_extracts/cme_micro_emini_fee_context_extract.md`
- `docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/cost_source_extracts/cme_ser_8360_mes_launch_context_extract.md`
- `docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/cost_source_extracts/cme_2019_fee_schedule_download_blocker_extract.md`
- `docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/cost_source_extracts/20260603_S09_MES_HISTORICAL_COST_SOURCE_EXTRACTION_status.csv`

Boundary preserved:

No unofficial mirror, current-fee default, broker assumption, spread/slippage assumption, old QuantLab active-pipeline state, retired-window artifact, risk-adjusted cost computation, speed eligibility computation, forecast computation, diagnostics, backtests, TEST, VALIDATION, Lockbox, Forward, deployment, trading, promotion, Git staging, commit, push, PR, or remote operations were performed.
