# Carver S09 MES Official CME 2020 Fee Schedule Coverage Route Result

Date: 2026-06-03

Status:

```text
PARTIAL_SOURCE_NATIVE_CME_2020_EXCHANGE_FEE_COVERAGE_EXTRACTED_NOT_HISTORICAL_COST_LOCK
```

Authorized execution scope:

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

Official source page:

```text
https://www.cmegroup.com/company/clearing-fees/historical-fees.html
```

Official linked CME 2020 historical schedule archive:

```text
https://www.cmegroup.com/company/clearing-fees/historical-fees/files/cme-fee-schedules-2020.zip
```

Result:

The official historical-fees page lists CME 2020 Historical Schedules. A plain
request to the official linked ZIP from the clean Carver workspace returned
CME's automated-access block response instead of the archive. No user-agent
spoofing, mirror source, current-fee substitution, old workspace source, or
retired-window source was used.

The operator then provided the official CME 2020 archive at:

```text
C:\Users\openclaw\Desktop\cme-fee-schedules-2020.zip
```

The archive was copied into the clean Carver workspace, hash-bound, expanded,
and read locally for the authorized 2020-01-01 through 2020-04-05 exchange-fee
portion only.

Archive SHA256:

```text
F7BB5F63C6E8B978075ABC79A55F79D28396CE09DA0B9B41DD6610FACC9DAFD4
```

Extracted source-native CME exchange-fee rows:

```text
cme-fee-schedule-2020-01-01.xls | Equity | row 36 | physical column 11 (xlrd zero-based column 10) | Non-Members | Globex - Outrights | Micro E-mini Index | 0.20 USD per side
cme-fee-schedule-2020-02-01.xls | Equity | row 36 | physical column 11 (xlrd zero-based column 10) | Non-Members | Globex - Outrights | Micro E-mini Index | 0.20 USD per side
cme-fee-schedule-2020-03-01.xls | Equity | row 36 | physical column 11 (xlrd zero-based column 10) | Non-Members | Globex - Outrights | Micro E-mini Index | 0.20 USD per side
cme-fee-schedule-2020-04-01.xls | Equity | row 36 | physical column 11 (xlrd zero-based column 10) | Non-Members | Globex - Outrights | Micro E-mini Index | 0.20 USD per side
```

Cost evidence outcome:

```text
exchange_fee_value: SOURCE_NATIVE_CME_EXCHANGE_FEE_VALUE_EXTRACTED_FULL_MACHINERY_SLICE_NOT_FULL_COST_LOCK
official_cme_2020_fee_schedule_coverage: PARTIAL_SOURCE_NATIVE_CME_2020_EXCHANGE_FEE_COVERAGE_EXTRACTED
historical_mes_cost_values: FAIL_CLOSED_S09_MES_HISTORICAL_COST_VALUES_NOT_LOCKED
```

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
