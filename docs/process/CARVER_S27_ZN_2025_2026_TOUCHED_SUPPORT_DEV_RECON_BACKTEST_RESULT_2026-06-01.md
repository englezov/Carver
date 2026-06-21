# Carver S27 ZN 2025-2026 Touched-Support Dev/Recon Backtest

Status:

```text
FAIL_CLOSED_S27_ZN_2025_2026_TOUCHED_SUPPORT_PROVIDER_DEGRADED_DAYS_AVAILABLE_ROWS_ONLY_NOT_COMPLETE_BACKTEST
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Scope

This artifact uses Databento Historical only for the missing ZN hourly `ohlcv-1h` execution rows over `2025-01-01` through `2026-05-22`. It reuses the existing local daily runtime/V/Q/M support ledger through `2026-05-22`.

This is therefore:

```text
TOUCHED_SUPPORT_DEVELOPMENT_RECONCILIATION
NOT_LOCKBOX
NOT_PROMOTION
```

## Result

Effective hourly backtest window:

```text
2025-01-02 through 2026-05-22
```

- UNIT_NO_LADDER_SAME_INPUT: net=-10442.45, gross=-8562.50, recorded_fees=1879.95, daily_win_rate=0.517857
- M1_LADDER_SAME_INPUT: net=-25697.16, gross=-15593.75, recorded_fees=10103.41, daily_win_rate=0.613181
- DELTA_M1_LADDER_MINUS_UNIT_NO_LADDER: net=-15254.71, gross=-7031.25, recorded_fees=8223.46, daily_win_rate=0.607450

Provider-condition complete-window status:

```text
PRESERVED_FOR_DIAGNOSTIC_CONTEXT_NOT_COMPLETE_WINDOW_BACKTEST
```

Degraded provider dates inside the requested window:

```text
2025-09-17, 2025-09-24, 2025-11-28, 2026-03-15, 2026-03-16, 2026-04-10
```

## Yearly Summary

- 2025 UNIT_NO_LADDER_SAME_INPUT: net=-6243.19
- 2025 M1_LADDER_SAME_INPUT: net=-7222.12
- 2026 UNIT_NO_LADDER_SAME_INPUT: net=-4199.26
- 2026 M1_LADDER_SAME_INPUT: net=-18475.04

## Cost Boundary

Recorded fee model:

```text
ETF_PUBLIC_PER_SIDE_COMMISSION_ONLY_NO_SPREAD_NO_SLIPPAGE
```

Futures-realistic cost readiness:

```text
FAIL_CLOSED_FUTURES_REALISTIC_COST_READINESS_NOT_EXECUTED
```

The recorded fee model is not Lockbox-ready futures cost closure.

## Non-Authorization

No OOS, Lockbox, Forward, tuning, deployment, trading, promotion, Git staging, commit, push, PR update/opening, or remote repository operation is authorized by this result.
