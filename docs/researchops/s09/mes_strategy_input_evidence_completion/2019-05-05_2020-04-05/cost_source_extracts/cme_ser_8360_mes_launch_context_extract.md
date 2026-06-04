# CME SER-8360 MES Launch Context Extract

Date captured: 2026-06-03

Authorized gate:

```text
source-native historical MES cost source acquisition/extraction
```

Source URL:

```text
https://www.cmegroup.com/notices/ser/2019/04/SER-8360.html
```

Use in this S09 MES gate:

```text
OFFICIAL_CME_MES_LAUNCH_CONTEXT_SOURCE_ONLY
```

Extracted source-context facts:

- CME SER-8360 has notice date 2019-04-03 and effective date 2019-05-05.
- SER-8360 covers the initial listing of Micro E-mini S&P 500 Index Futures and related Micro E-mini contracts.
- SER-8360 states the contracts would be listed for CME Globex trading and CME ClearPort clearing submission.

Extraction result:

```text
OFFICIAL_CME_MES_LAUNCH_CONTEXT_LOCKED_NOT_COST_VALUE_SOURCE
```

Boundary:

This extract supports the launch/effective-date context only. It does not extract or lock historical cost component values, risk-adjusted cost, speed eligibility, forecasts, diagnostics, backtests, TEST, VALIDATION, Lockbox, Forward, deployment, trading, promotion, Git staging, commit, push, PR, or remote operations.
