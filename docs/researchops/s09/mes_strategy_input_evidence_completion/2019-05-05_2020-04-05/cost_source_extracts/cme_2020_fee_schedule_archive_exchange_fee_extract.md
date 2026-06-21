# S09 MES Official CME 2020 Fee Schedule Archive Exchange Fee Extract

Date: 2026-06-03

Status:

```text
PARTIAL_SOURCE_NATIVE_CME_2020_EXCHANGE_FEE_COVERAGE_EXTRACTED_NOT_HISTORICAL_COST_LOCK
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

Operator-provided archive:

```text
C:\Users\openclaw\Desktop\cme-fee-schedules-2020.zip
```

Workspace archive copy:

```text
docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/cost_source_extracts/official_cme_2020_fee_schedule_archive/cme-fee-schedules-2020.zip
```

Archive SHA256:

```text
F7BB5F63C6E8B978075ABC79A55F79D28396CE09DA0B9B41DD6610FACC9DAFD4
```

Extraction method:

The operator-provided official CME 2020 archive was copied into the clean
Carver workspace and expanded locally. The relevant rows were read from the
archive XLS files' `Equity` sheets. The source-native row context was:

```text
Non-Members / Globex - Outrights / Micro E-mini Index / Futures
```

Extracted exchange-fee values:

```text
cme-fee-schedule-2020-01-01.xls | Equity | row 36 | physical column 11 (xlrd zero-based column 10) | Non-Members | Globex - Outrights | Micro E-mini Index | 0.20 USD per side
cme-fee-schedule-2020-02-01.xls | Equity | row 36 | physical column 11 (xlrd zero-based column 10) | Non-Members | Globex - Outrights | Micro E-mini Index | 0.20 USD per side
cme-fee-schedule-2020-03-01.xls | Equity | row 36 | physical column 11 (xlrd zero-based column 10) | Non-Members | Globex - Outrights | Micro E-mini Index | 0.20 USD per side
cme-fee-schedule-2020-04-01.xls | Equity | row 36 | physical column 11 (xlrd zero-based column 10) | Non-Members | Globex - Outrights | Micro E-mini Index | 0.20 USD per side
```

Coverage outcome:

```text
official_cme_2020_fee_schedule_coverage: PARTIAL_SOURCE_NATIVE_CME_2020_EXCHANGE_FEE_COVERAGE_EXTRACTED
exchange_fee_value: SOURCE_NATIVE_CME_EXCHANGE_FEE_VALUE_EXTRACTED_FULL_MACHINERY_SLICE_NOT_FULL_COST_LOCK
historical_mes_cost_values: FAIL_CLOSED_S09_MES_HISTORICAL_COST_VALUES_NOT_LOCKED
```

This extract completes source-native CME exchange-fee coverage for the
machinery-development slice when combined with the already extracted 2019 CME
fee schedule archive rows. It does not lock full historical MES cost values.

Remaining blockers:

```text
broker_current_fee_static_historical_policy
spread_slippage_source_or_policy
```

Boundary preserved:

No active cost ledger rows were written. No cost computation, risk-adjusted cost
computation, speed eligibility computation, forecast computation, diagnostics,
backtests, TEST, VALIDATION, Lockbox, Forward, deployment, trading, promotion,
Git staging, commit, push, PR, or remote operations were performed.
