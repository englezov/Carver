# Carver S27 ZN 2022-2023 Retargeted Dev/Reconciliation Backtest Execution Result

Status:

```text
PASS_RETARGETED_S27_ZN_DEV_RECON_UNIT_PLUMBING_NO_COST_BACKTEST_NOT_ALPHA
```

Gate: `RETARGETED_S27_ZN_2022_2023_DEV_RECON_BACKTEST_EXECUTION`

## Result

- Requested archive window: `2022-01-01` through `2023-12-31`.
- Effective backtest window: `2022-01-04` through `2023-12-29`.
- Effective start reason: `FIRST_ROW_WITH_STRICT_PRIOR_DAILY_SIGMA_TREND_AND_V_Q_M_RUNTIME`.
- Source hourly rows: `20870`.
- Local continuous hourly rows: `11775`.
- Inactive dated-contract source rows explicitly ledgered: `9095`.
- S27 forecast rows: `11771`.
- Unit/no-cost backtest rows: `11770`.
- Gross no-cost PnL USD, unit plumbing only: `2968.75`.

## Boundary

This is a Development/Reconciliation mechanical execution only. It is not an alpha result, not a promoted backtest, not OOS, not Lockbox, not Forward, not deployment, not trading, and not a production sizing artifact.

Capital and real M1 position sizing remain blocked. The position series uses a one-contract unit base only to prove the forecast-to-position-to-PnL pipe. Costs remain fail-closed because no commission or spread-cost value was locked for this gate.
