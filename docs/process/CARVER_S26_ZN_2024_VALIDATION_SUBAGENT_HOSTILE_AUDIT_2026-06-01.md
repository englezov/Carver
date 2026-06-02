# Carver S26 ZN 2024 Validation Subagent Hostile Audit

Date: 2026-06-01

Mode: read-only subagent hostile audit. No edits, provider calls, data downloads,
backtests, diagnostics, OOS, Lockbox, Forward, deployment, trading, promotion,
Git operations, or remote operations were performed by the subagent audit.

## Findings

CRITICAL: None.

HIGH: None.

MEDIUM: None.

The subagent audit confirmed that the S26 ZN 2024 validation artifacts preserve
the required boundaries:

- existing local ZN 2024 validation artifacts only;
- no new provider/API access;
- no new market data download;
- no OOS, Lockbox, Forward, deployment, trading, or promotion;
- no S27 V/Q/M volatility attenuation, EWMAC trend overlay, or safety stack used
  in S26 standalone rows;
- 2024 is labelled `VALIDATION`, not Lockbox;
- no parameter, cost, ladder, symbol, or window tuning is opened.

## Count Checks

```text
S26_FORECAST_ROWS: 5919
POSITION_ROWS: 5919
BACKTEST_ROWS: 5918
FORMULA_RECON_ROWS: 12
VALIDATION_ROWS: 10
BLOCKING_VALIDATION_FINDINGS: 0
```

Rounded position counts sum to `5919`:

```text
-2: 1
-1: 80
 0: 5741
 1: 91
 2: 6
```

S26 validation result totals:

```text
GROSS_PNL_USD: 3296.875
ESTIMATED_ETF_FEES_USD: 359.38
NET_AFTER_ETF_FEES_USD: 2937.495
POSITION_CHANGE_SIDES: 238
```

The audit confirmed that S26 2022-2023 TEST is negative while S26 2024
validation is positive:

```text
S26_2022_2023_TEST_NET_AFTER_ETF_FEES_USD: -4617.30
S26_2024_VALIDATION_NET_AFTER_ETF_FEES_USD: 2937.50
S26_TEST_AND_VALIDATION_BOTH_NEGATIVE: NO
```

All `5919` S26 position rows mark S27 safety stack status as:

```text
NOT_USED_S26_STANDALONE_RAW_FAST_MEAN_REVERSION
```

## Disposition

```text
BLOCKING_FINDINGS: NO
AUDIT_DISPOSITION: PASS_S26_ZN_2024_VALIDATION_SCOPE
```
