# Carver S27 Pure ES M1-Style Sizing Ladder Dev/Reconciliation Backtest Result

Status:

```text
PASS_S27_PURE_ES_M1_STYLE_LADDER_DEV_RECON_BACKTEST_NOT_ALPHA
```

Gate: `S27_PURE_ES_M1_STYLE_SIZING_LADDER_DEV_RECON_BACKTEST`

- Capital: `$100000.0`.
- Target risk: `0.2`.
- ES multiplier: `50.0`.
- Forecast-to-position divisor: `10.0`.
- Cost status: `PURE_ES_COST_NOT_LOCKED_ZERO_PLACEHOLDER_NO_SPREAD_OR_SLIPPAGE`.

- Effective window: `2022-01-03` through `2023-12-29`.
- Forecast rows: `11777`.
- Ladder rows: `11777`.
- Backtest rows: `11776`.
- Rounded position counts: `{-2: 8, -1: 236, 0: 10878, 1: 539, 2: 109, 3: 7}`.
- Gross PnL: `$-46862.5`.
- Estimated fees: `$0.0`.
- Net after fees: `$-46862.5`.

This applies the same M1-style sizing ladder semantics used by the completed ZN ladder gate to pure ES. It is still Development/Reconciliation only: no OOS, Lockbox, Forward, deployment, trading, promotion, alpha claim, or production cost lock. It does not implement Carver limit-order fill quality; it only fixes the crude unit-plumbing position sizing issue.
