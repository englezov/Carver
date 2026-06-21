# Carver S26 ZN 2022-2023 Comparison TEST Subagent Hostile Audit

Date: 2026-06-01

Mode: read-only subagent hostile audit. No edits, provider calls, data downloads,
backtests, OOS, Lockbox, Forward, deployment, trading, promotion, Git operations,
or remote operations were performed by the subagent audit.

## Findings

CRITICAL: None.

HIGH: None.

MEDIUM: None.

The subagent audit confirmed that the S26 TEST artifacts preserve the required
boundaries:

- the run is explicitly labelled as a one-time `2022-01-01` through
  `2023-12-31` TEST exception for direct S26 versus existing S27 comparison;
- future strategy default remains a one-year TEST window;
- no Databento access, new download, OOS/Lockbox/Forward, promotion, trading, or
  deployment is authorized;
- S26 does not consume the S27 V/Q/M volatility attenuation, EWMAC trend overlay,
  or safety stack;
- counts and statuses are internally consistent.

## Count Checks

```text
S26_FORECAST_ROWS: 11793
POSITION_ROWS: 11793
BACKTEST_ROWS: 11792
VALIDATION_ROWS: 10
BLOCKING_VALIDATION_FINDINGS: 0
```

Rounded position counts sum to `11793`:

```text
-2: 104
-1: 984
 0: 9468
 1: 1163
 2: 74
```

S26 result totals:

```text
GROSS_PNL_USD: -890.625
ESTIMATED_ETF_FEES_USD: 3726.68
NET_AFTER_ETF_FEES_USD: -4617.305
POSITION_CHANGE_SIDES: 2468
```

All `11793` S26 position rows mark S27 safety stack status as:

```text
NOT_USED_S26_STANDALONE_RAW_FAST_MEAN_REVERSION
```

## Disposition

```text
BLOCKING_FINDINGS: NO
AUDIT_DISPOSITION: PASS_S26_ZN_2022_2023_COMPARISON_TEST_SCOPE
```
