# Carver S27 ZN Mechanical Verification Result

Status:

```text
PASS_S27_ZN_MECHANICAL_VERIFICATION_DEV_RECON
```

## Scope

This verifier recomputes the S27 ZN path from existing local artifacts only: hourly continuous rows, daily runtime rows, forecast rows, ladder rows, position rows, and backtest rows. It does not call providers, download data, open OOS/Lockbox/Forward, tune, deploy, trade, or promote.

## Summary

| Period | Stage | Checks | Net After Fees | Episodes | Episode Win Rate | Fee Sides | Max Runtime Lag |
|---|---|---:|---:|---:|---:|---:|---:|
| ZN_2022_2023_INITIAL_TEST | INITIAL_TEST | 40/40 | 5342.630000000004 | 1015 | 0.6334975369458128 | 3312 | 1 |
| ZN_2024_VALIDATION | VALIDATION | 40/40 | 24618.820000000003 | 699 | 0.6781115879828327 | 3543 | 1 |

## What Was Independently Recomputed

- S26 EWMA(5) raw forecast from hourly continuous closes.
- S27 daily EWMAC(16,64) trend runtime from daily continuous closes.
- S27 V/Q/M EWMA(10) multiplier from daily quantile rows.
- S27 adjusted raw forecast, sigma-price bridge, scalar 20.0, cap +/-20.
- M1-style base position, forecast multiplier, desired unrounded and rounded position.
- Close-to-close hourly gross PnL, ETF fee sides, roll-transition fee sides, and net PnL.
- Runtime lag, provider-condition, roll-event, and no-promotion boundaries.

## Disposition

```text
BLOCKING_FINDINGS: NO
AUDIT_DISPOSITION: PASS_S27_ZN_MECHANICAL_VERIFICATION_DEV_RECON
```

This is a Development/Reconciliation mechanical-verification disposition only. It is not an alpha claim and does not authorize OOS, Lockbox, Forward, tuning, deployment, trading, or promotion.
