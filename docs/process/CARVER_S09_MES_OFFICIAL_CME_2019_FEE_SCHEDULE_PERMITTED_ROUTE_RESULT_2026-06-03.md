# Carver S09 MES Official CME 2019 Fee Schedule Permitted Route Result

Date: 2026-06-03

Status:

```text
PARTIAL_SOURCE_NATIVE_CME_2019_FEE_SCHEDULE_ARCHIVE_EXTRACTED_EXCHANGE_FEE_ONLY
```

Authorized execution scope:

```text
official_cme_2019_fee_schedule_archive_permitted_route
```

Scope:

- lane_class: SOURCE_NATIVE_FUTURES
- root: MES
- row_id: APPENDIX_C_174_006
- machinery_development_slice: 2019-05-05 through 2020-04-05
- selected_evidence_name: historical_mes_cost_values

Official source page:

```text
https://www.cmegroup.com/company/clearing-fees/historical-fees.html
```

Official linked CME 2019 historical schedule archive:

```text
https://www.cmegroup.com/company/clearing-fees/historical-fees/files/cme-fee-schedules-2019.zip
```

Result:

The official historical-fees page lists CME 2019 Historical Schedules. A plain
request to the official linked ZIP from the clean Carver workspace returned
CME's automated-access block response instead of the archive. No user-agent
spoofing, mirror source, current-fee substitution, old workspace source, or
retired-window source was used.

Operator then provided the official CME archive on the Desktop:

```text
C:\Users\openclaw\Desktop\cme-fee-schedules-2019.zip
```

The archive was copied into the S09 evidence tree and expanded for source-native
extraction. Workspace archive SHA256:

```text
08347421A83E53258BB0D9CE3682F9C73A46D3A708031A649310BF1D74C600DF
```

Source-native exchange-fee extraction:

```text
Non-Members / Globex - Outrights / Micro E-mini Index = 0.20 USD per side
```

The same `0.20` source value was present in the official CME Equity sheet for
the 2019-05-06, 2019-07-01, 2019-08-01, 2019-09-09, and 2019-10-01 schedules.

Cost evidence outcome:

```text
historical_fee_schedule_source_location: LOCKED_SOURCE_LOCATION_ONLY
exchange_fee_value: PARTIAL_SOURCE_NATIVE_CME_EXCHANGE_FEE_VALUE_EXTRACTED_NOT_FULL_COST_LOCK
clearing_regulatory_fee_value: PARTIAL_SOURCE_NATIVE_NFA_ASSESSMENT_FEE_VALUE_EXTRACTED_NOT_FULL_COST_LOCK
historical_mes_cost_values: FAIL_CLOSED_S09_MES_HISTORICAL_COST_VALUES_NOT_LOCKED
```

Boundary preserved:

No broker commission source or policy was selected. No spread/slippage source
or policy was selected. No cost computation, risk-adjusted cost computation,
speed eligibility computation, forecast computation, diagnostics, backtests,
TEST, VALIDATION, Lockbox, Forward, deployment, trading, promotion, Git staging,
commit, push, PR, or remote operations were performed.

Next required action:

Operator must provide or authorize the remaining missing cost inputs before
historical_mes_cost_values can lock: broker commission source or policy,
spread/slippage source or policy, and any needed 2020 CME historical fee
schedule coverage for the 2020-01-01 through 2020-04-05 portion of the
machinery-development slice.
