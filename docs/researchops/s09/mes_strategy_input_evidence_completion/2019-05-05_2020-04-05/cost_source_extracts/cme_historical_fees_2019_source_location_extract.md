# CME Historical Fees 2019 Source Location Extract

Date captured: 2026-06-03

Authorized gate:

```text
source-native historical MES cost source acquisition/extraction
```

Source URL:

```text
https://www.cmegroup.com/company/clearing-fees/historical-fees.html
```

2019 CME schedule URL attempted:

```text
https://www.cmegroup.com/content/dam/cmegroup/company/clearing-fees/files/cme-fee-schedule-2019.zip
```

Use in this S09 MES gate:

```text
OFFICIAL_CME_HISTORICAL_FEE_SOURCE_LOCATION_ONLY
```

Extracted source-location facts:

- CME's official historical-fees page states that downloadable historical schedules are available for trading and clearing exchange fees.
- The page lists CME 2019 Historical Schedules as an available historical schedule family.
- The page gives CME's exchange-fee contact route through the Exchange Fee Hotline / EFS Admin.

Extraction result:

```text
SOURCE_LOCATION_LOCKED_VALUE_EXTRACTION_FAIL_CLOSED_OFFICIAL_ARCHIVE_DOWNLOAD_BLOCKED
```

Boundary:

This extract does not lock historical MES exchange_fee, clearing_regulatory_fee, broker_commission, spread_slippage, risk-adjusted cost, speed eligibility, eligible speed set, Table 36 FDM, forecasts, diagnostics, backtests, TEST, VALIDATION, Lockbox, Forward, deployment, trading, promotion, Git staging, commit, push, PR, or remote operations.
