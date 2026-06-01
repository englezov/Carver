# Carver S27 ZN Touched-History Development/Reconciliation Backtest

Status:

```text
PASS_S27_ZN_TOUCHED_HISTORY_DEV_RECON_BACKTEST_NOT_LOCKBOX_NOT_PROMOTION
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Scope

This artifact recomputes and summarizes existing local S27 ZN hourly backtest evidence only. It is explicitly:

```text
NOT_LOCKBOX
NOT_PROMOTION
NO_NEW_PROVIDER_ACCESS
NO_NEW_DATA_DOWNLOAD
```

## Usable Hourly Evidence

```text
2022-01-04 through 2024-12-31
```

The requested touched-history outer boundary through `2026-05-22` is not fully source-frequency executable because the post-2024 local evidence is daily runtime/VQM support only, not hourly S27 backtest rows.

## Summary

- UNIT_NO_LADDER_SAME_INPUT: net=9048.16, gross=11421.88, recorded_fees=2373.72, daily_win_rate=0.559908
- M1_LADDER_SAME_INPUT: net=29961.45, gross=40312.50, recorded_fees=10351.05, daily_win_rate=0.634286
- DELTA_M1_LADDER_MINUS_UNIT_NO_LADDER: net=20913.30, gross=28890.62, recorded_fees=7977.33, daily_win_rate=0.613734

## Coverage Boundary

```text
FAIL_CLOSED_NO_LOCAL_HOURLY_S27_BACKTEST_ROWS_DAILY_RUNTIME_SUPPORT_ONLY
```

Local extended support reaches 2026-05-22 for daily runtime/VQM only; S27 source-frequency backtest requires hourly bars.

## Cost Boundary

Recorded fee model:

```text
ETF_PUBLIC_PER_SIDE_COMMISSION_ONLY_NO_SPREAD_NO_SLIPPAGE
```

Futures-realistic cost status:

```text
FAIL_CLOSED_FUTURES_REALISTIC_COST_READINESS_NOT_EXECUTED
```

This run does not close futures-realistic cost readiness and does not open Lockbox.

## Non-Authorization

This artifact authorizes no provider API access, no data download, no OOS, no Lockbox, no Forward, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, and no remote operations.
