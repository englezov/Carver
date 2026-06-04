# CME Micro E-mini Fee Context Extract

Date captured: 2026-06-03

Authorized gate:

```text
source-native historical MES cost source acquisition/extraction
```

Source URL:

```text
https://www.cmegroup.com/articles/faqs/frequently-asked-questions-micro-e-mini-equity-index-futures.html
```

Use in this S09 MES gate:

```text
OFFICIAL_CME_MES_FEE_CONTEXT_SOURCE_LOCATION_ONLY
```

Extracted source-context facts:

- CME's Micro E-mini FAQ identifies the Micro E-mini S&P 500 futures product as CME DCM-listed.
- The same FAQ identifies the CME Globex product code for Micro E-mini S&P 500 futures as MES.
- The FAQ states that Micro E-mini S&P 500, Nasdaq-100, and Russell 2000 products are part of the Micro E-mini Equity Index futures suite according to the CME Fee Schedule.
- The FAQ states that broker commissions are broker-specific rather than CME clearing-fee values.

Extraction result:

```text
OFFICIAL_CME_MES_FEE_CONTEXT_LOCKED_VALUE_EXTRACTION_FAIL_CLOSED
```

Boundary:

This extract supports source routing only. It does not provide historical MES dollar fee values and does not authorize cost computation, risk-adjusted cost, speed eligibility, forecasts, diagnostics, backtests, TEST, VALIDATION, Lockbox, Forward, deployment, trading, promotion, Git staging, commit, push, PR, or remote operations.
