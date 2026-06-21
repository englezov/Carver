# Carver S26 ZN 2022-2023 Comparison TEST Result

Date: 2026-06-01

Status:

```text
PASS_S26_ZN_2022_2023_COMPARISON_TEST_NOT_PROMOTION
```

## Scope

This artifact opens the one-time S26 versus existing S27 comparison TEST:

```text
TEST_WINDOW: 2022-01-01 through 2023-12-31
EXCEPTION_REASON: direct comparison to the already-run S27 ZN 2022-2023 result
FUTURE_DEFAULT: one-year TEST window
```

S26 is tested as standalone fast mean reversion on the existing local ZN hourly
lineage and existing S26 forecast rows emitted during S27 work. S27 is not
rerun or changed; it is used only as an existing reference artifact.

## Result

| Strategy | Gross PnL | Estimated ETF fees | Net after ETF fees | Position-change sides |
| --- | ---: | ---: | ---: | ---: |
| S26 standalone | -890.62 | 3726.68 | -4617.30 | 2468 |
| S27 reference | 22406.25 | 5889.00 | 16517.25 | 3900 |

```text
S26_MINUS_S27_NET_USD: -21134.56
```

## Boundaries

- no Databento provider API access;
- no new market data download;
- no OOS, Lockbox, or Forward access;
- no Sharpe, drawdown, alpha claim, deployment, trading, or promotion;
- no S27 V/Q/M or trend overlay used in the S26 standalone run;
- no parameter, cost, ladder, symbol, or window tuning.
