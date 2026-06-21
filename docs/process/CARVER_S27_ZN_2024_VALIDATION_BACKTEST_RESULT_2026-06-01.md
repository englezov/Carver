# Carver S27 ZN 2024 Validation Backtest Result

Status:

```text
PASS_S27_ZN_2024_VALIDATION_BACKTEST_NOT_ALPHA
```

Gate: `S27_ZN_2024_VALIDATION_BACKTEST_FROZEN_FROM_INITIAL_TEST`

Frozen from initial ZN 2022-2023 test: S27 ZN M1-style sizing ladder, capital 100k, target risk 20%, weight 1, IDM 1, ZN multiplier 1000, ETF public per-side commission only.

## Result

- Requested window: `2024-01-01` through `2024-12-31`.
- Effective backtest window: `2024-01-02` through `2024-12-31`.
- S27 forecast rows: `5919`.
- Ladder rows: `5919`.
- Backtest rows: `5918`.
- Rounded position counts: `{-10: 5, -9: 8, -8: 6, -7: 15, -6: 17, -5: 28, -4: 64, -3: 112, -2: 259, -1: 611, 0: 3878, 1: 510, 2: 197, 3: 74, 4: 55, 5: 24, 6: 16, 7: 19, 8: 9, 9: 4, 10: 6, 11: 2}`.
- Position-change sides: `3541`.
- Roll-transition fee sides: `2`.
- Gross PnL: `$29968.75`.
- Estimated ETF fees: `$5349.93`.
- Net after ETF fees: `$24618.820000000003`.

## Boundary

This is the frozen 2024 validation backtest only. It is not OOS, not Lockbox, not Forward, not deployment, not trading, and not promotion. No parameter, symbol, cost, or sizing tuning is authorized by this result.
