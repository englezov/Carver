# Carver S27 Pure ES Source-Native Futures 2022-2023 Result

Status:

```text
PASS_S27_PURE_ES_SOURCE_NATIVE_FUTURES_DEV_RECON_NOT_ALPHA
```

Gate: `S27_PURE_ES_SOURCE_NATIVE_FUTURES_DEV_RECON`

This run reuses the already cached ES Databento provider CSV files from the ES-to-MES gate. No Databento client was created and no new provider API call was made in this pure ES run.

## Result

| Root | Window | Forecast Rows | Backtest Rows | Gross | Costs | Net | Cost Boundary |
|---|---|---:|---:|---:|---:|---:|---|
| ES | 2022-01-03 to 2023-12-29 | 11777 | 11776 | -45537.5 | 0.0 | -45537.5 | NOT_LOCKED_ZERO_PLACEHOLDER_NO_SPREAD_NO_SLIPPAGE |

Pure ES means ES signal and ES execution/PnL plumbing. It is not ES-to-MES and not CFD. This is Development/Reconciliation machinery evidence only, not alpha, OOS, Lockbox, Forward, deployment, trading, promotion, or production sizing/cost lock.

Important interpretation warning: the gross/net dollars above are unit-plumbing dollars from rounded forecast exposure (`capped_forecast / 10`, nearest integer), not an account-sized return series. This run can hold up to two ES contracts because proper Carver account sizing (`forecast -> risk target -> instrument risk -> capital -> contract multiplier -> rounded position`) is not locked in this artifact. It must not be quoted as a `-45%` account result.
