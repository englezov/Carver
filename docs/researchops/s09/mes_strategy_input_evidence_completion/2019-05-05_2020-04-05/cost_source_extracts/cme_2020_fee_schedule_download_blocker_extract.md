# S09 MES Official CME 2020 Fee Schedule Download Blocker Extract

Date: 2026-06-03

Status:

```text
SUPERSEDED_BY_OPERATOR_PROVIDED_OFFICIAL_CME_2020_ARCHIVE_EXTRACTED
```

Authorized route:

```text
official_cme_2020_fee_schedule_coverage_permitted_route
```

Scope:

- lane_class: SOURCE_NATIVE_FUTURES
- root: MES
- row_id: APPENDIX_C_174_006
- machinery_development_slice: 2019-05-05 through 2020-04-05
- selected_evidence_name: historical_mes_cost_values
- target coverage: 2020-01-01 through 2020-04-05 exchange-fee portion only

Official CME historical-fees page:

```text
https://www.cmegroup.com/company/clearing-fees/historical-fees.html
```

Official CME 2020 historical schedules archive route:

```text
https://www.cmegroup.com/company/clearing-fees/historical-fees/files/cme-fee-schedules-2020.zip
```

Original route result:

A plain request to the official CME 2020 linked ZIP from the clean Carver
workspace returned CME's automated-access block response instead of the archive.
No user-agent spoofing, mirror source, current-fee substitution, old workspace
source, or retired-window source was used.

Superseding result:

After this fail-closed blocker was recorded, the operator provided the official
CME 2020 archive at:

```text
C:\Users\openclaw\Desktop\cme-fee-schedules-2020.zip
```

That archive was copied into the clean Carver workspace, hash-bound, expanded,
and used only for bounded 2020-01-01 through 2020-04-05 exchange-fee source
extraction. The superseding extraction artifact is:

```text
docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/cost_source_extracts/cme_2020_fee_schedule_archive_exchange_fee_extract.md
```

Original cost evidence outcome:

```text
official_cme_2020_fee_schedule_coverage: FAIL_CLOSED_OFFICIAL_CME_2020_FEE_SCHEDULE_ARCHIVE_NOT_RETRIEVED_AUTOMATED_ACCESS_BLOCKED
exchange_fee_value: PARTIAL_SOURCE_NATIVE_CME_EXCHANGE_FEE_VALUE_EXTRACTED_NOT_FULL_COST_LOCK
historical_mes_cost_values: FAIL_CLOSED_S09_MES_HISTORICAL_COST_VALUES_NOT_LOCKED
```

Superseding cost evidence outcome:

```text
official_cme_2020_fee_schedule_coverage: PARTIAL_SOURCE_NATIVE_CME_2020_EXCHANGE_FEE_COVERAGE_EXTRACTED
exchange_fee_value: SOURCE_NATIVE_CME_EXCHANGE_FEE_VALUE_EXTRACTED_FULL_MACHINERY_SLICE_NOT_FULL_COST_LOCK
historical_mes_cost_values: FAIL_CLOSED_S09_MES_HISTORICAL_COST_VALUES_NOT_LOCKED
```

Next required action:

```text
No further 2020 CME exchange-fee coverage action is required for the machinery-development slice. Full historical_mes_cost_values remains fail-closed until broker temporal policy and spread/slippage source or policy are resolved.
```

Boundary preserved:

No active cost ledger rows were written. No cost computation, risk-adjusted cost
computation, speed eligibility computation, forecast computation, diagnostics,
backtests, TEST, VALIDATION, Lockbox, Forward, deployment, trading, promotion,
Git staging, commit, push, PR, or remote operations were performed.
