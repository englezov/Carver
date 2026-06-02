# Carver S26 ZN 2024 Validation Result

Date: 2026-06-01

Status:

```text
PASS_S26_ZN_2024_VALIDATION_NOT_PROMOTION
```

## Scope

This artifact checks S26 standalone fast mean reversion on the existing local
ZN 2024 validation artifacts. No provider call or new data download was made.

The S26 validation surface uses unit plumbing and nearest rounding, matching the
S26 2022-2023 TEST comparison surface. The S27 row below is the already-existing
2024 validation reference and uses its frozen M1-style ladder surface.

## Result

| Strategy | Surface | Gross PnL | Estimated ETF fees | Net after ETF fees | Position-change sides |
| --- | --- | ---: | ---: | ---: | ---: |
| S26 standalone | UNIT_PLUMBING_NEAREST | 3296.88 | 359.38 | 2937.50 | 238 |
| S27 reference | FROZEN_M1_STYLE_LADDER | 29968.75 | 5349.93 | 24618.82 | 3541 |

```text
S26_2022_2023_TEST_NET_AFTER_ETF_FEES_USD: -4617.30
S26_2024_VALIDATION_NET_AFTER_ETF_FEES_USD: 2937.50
S26_TEST_AND_VALIDATION_BOTH_NEGATIVE: NO
```

## Boundaries

- no new Databento/provider access;
- no new market data download;
- no OOS, Lockbox, Forward, deployment, trading, or promotion;
- no S27 V/Q/M or trend overlay used in S26;
- no parameter, cost, ladder, symbol, or window tuning.
