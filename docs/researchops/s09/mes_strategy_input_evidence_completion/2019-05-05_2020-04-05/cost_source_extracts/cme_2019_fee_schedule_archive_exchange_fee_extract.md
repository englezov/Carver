# S09 MES Official CME 2019 Fee Schedule Archive Exchange Fee Extract

Date: 2026-06-03

Status:

```text
PARTIAL_SOURCE_NATIVE_COST_SOURCE_EXTRACTION_EXCHANGE_FEE_ONLY_NOT_HISTORICAL_COST_LOCK
```

Authorized route:

```text
official_cme_2019_fee_schedule_archive_permitted_route
```

Operator-provided official archive:

```text
C:\Users\openclaw\Desktop\cme-fee-schedules-2019.zip
```

Workspace evidence copy:

```text
docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/cost_source_extracts/official_cme_2019_fee_schedule_archive/cme-fee-schedules-2019.zip
```

Archive SHA256:

```text
08347421A83E53258BB0D9CE3682F9C73A46D3A708031A649310BF1D74C600DF
```

Official CME historical-fees page:

```text
https://www.cmegroup.com/company/clearing-fees/historical-fees.html
```

Official CME 2019 historical schedules archive URL:

```text
https://www.cmegroup.com/company/clearing-fees/historical-fees/files/cme-fee-schedules-2019.zip
```

Extraction method:

- Read official CME archive member `.xls` files from the operator-provided archive copy.
- Opened the `Equity` sheet.
- Selected the actual `Non-Members` account group, not rows that merely reference `See Non-Members`.
- Selected `Venue/Transaction Type = Globex - Outrights`.
- Selected the `Micro E-mini Index` futures column.

Extracted CME exchange-fee source values:

```text
cme-fee-schedule-2019-05-06.xls | Equity | row 36 | spreadsheet physical column 11 (xlrd zero-based column 10) | Non-Members | Globex - Outrights | Micro E-mini Index | 0.20 USD per side
cme-fee-schedule-2019-07-01.xls | Equity | row 36 | spreadsheet physical column 11 (xlrd zero-based column 10) | Non-Members | Globex - Outrights | Micro E-mini Index | 0.20 USD per side
cme-fee-schedule-2019-08-01.xls | Equity | row 36 | spreadsheet physical column 11 (xlrd zero-based column 10) | Non-Members | Globex - Outrights | Micro E-mini Index | 0.20 USD per side
cme-fee-schedule-2019-09-09.xls | Equity | row 36 | spreadsheet physical column 11 (xlrd zero-based column 10) | Non-Members | Globex - Outrights | Micro E-mini Index | 0.20 USD per side
cme-fee-schedule-2019-10-01.xls | Equity | row 36 | spreadsheet physical column 11 (xlrd zero-based column 10) | Non-Members | Globex - Outrights | Micro E-mini Index | 0.20 USD per side
```

Scope limitation:

This extract supports only the CME exchange-fee source value present in the
official 2019 CME fee schedule archive. It does not lock the complete
historical MES cost values evidence family.

Remaining cost blockers:

```text
clearing_regulatory_fee: not locked from this CME archive; CME notes it does not assess member firms an NFA fee and points NFA questions outside CME.
broker_commission: not locked; CME FAQ states commissions are broker-specific.
spread_slippage: not locked; no source-native spread/slippage source or conservative policy has been authorized.
full machinery slice through 2020-04-05: not fully covered by a 2020 CME fee schedule archive in this extraction.
```

Boundary preserved:

No cost computation, risk-adjusted cost computation, speed eligibility
computation, forecast computation, diagnostics, backtests, TEST, VALIDATION,
Lockbox, Forward, deployment, trading, promotion, Git staging, commit, push,
PR, or remote operations were performed.
