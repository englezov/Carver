# Carver S27 ZN Single-Instrument Backtest Readiness Gate Draft

Date: 2026-05-31

Status:

```text
PASS_S27_ZN_SINGLE_INSTRUMENT_BACKTEST_READINESS_GATE_NOT_BACKTEST
```

## Purpose

Define the next clean gate after completed S26/S27 forecast-only machinery: a readiness path for a later separately authorized S27 ZN single-instrument Development/Reconciliation backtest over 2022-2023.

This gate does not execute the backtest.

## Strategy Identity

```text
strategy_id: S27_SAFER_FAST_MEAN_REVERSION_ZN_DEV_RECON
book_strategy: Strategy twenty-seven, safer fast mean reversion
instrument_role: book worked-example family from S26/S27 path
row_id: APPENDIX_C_172_004
author_market_code: ZN
lane: SOURCE_NATIVE_FUTURES
```

## Preconditions

Required locked inputs before any later backtest execution:

```text
completed_forecast_machinery_audit: PASS_LOCAL_HOSTILE_AUDIT_NO_BLOCKING_FINDINGS
S27 forecast-series-only status: PASS_S27_REAL_HOURLY_FORECAST_SERIES_ONLY_HANDOFF_PLUMBING
position/execution/cost semantics lock: PASS_S27_ZN_POSITION_EXECUTION_COST_SEMANTICS_LOCK_NOT_BACKTEST
hourly archive window manifest: PROCESS_ONLY_S27_ZN_BACKTEST_HOURLY_ARCHIVE_WINDOW_MANIFEST_NOT_DATA_AUTHORIZATION
```

Locked target window:

```text
completed trading dates: 2022-01-01 through 2023-12-31
request envelope: 2021-12-31T00:00:00Z through 2024-01-01T00:00:00Z
raw-symbol chain: ZNH2, ZNM2, ZNU2, ZNZ2, ZNH3, ZNM3, ZNU3, ZNZ3, ZNH4
```

## Readiness Contract

The later backtest execution gate must lock and verify:

```text
one instrument only: ZN
one strategy only: S27 safer fast mean reversion
hourly completed bars only
local dated-contract chain only
no provider continuous fallback
provider condition AVAILABLE only
zero silent row skip
S26 forecast dependency present for every S27 row
EWMAC16 trend runtime present for every S27 row
V/Q/M volatility attenuation runtime present for every S27 row
position sizing uses M1 size_contracts base position
final capped forecast divided by 10 multiplies base position
no buffering
limit-style execution semantics only
commission-only Development/Reconciliation cost surface if cost values are locked
spread and market-order costs unresolved/fail-closed
```

## First Backtest Scope

```text
QUARANTINED_DEV_RECON_ZN_ONLY_S27_NO_OOS_NO_LOCKBOX_NO_PROMOTION
```

The first backtest may be used only to verify mechanics:

```text
row lineage
forecast-to-position transformation
position sanity
turnover mechanics
cost-field plumbing if cost values are explicitly locked
fail-closed behavior
```

It must not be used as alpha evidence.

## What Remains Closed

```text
portfolio backtest
Jumbo backtest
S26 standalone backtest
multi-instrument S27
parameter tuning
cost tuning
execution tuning
OOS
Lockbox
Forward
deployment
trading
promotion
alpha claim
```

## Non-Authorization

This draft authorizes no provider API access, no data download, no market-row parsing, no diagnostics, no backtests, no returns, no PnL, no positions, no orders, no fills, no costs, no carry, no OOS, no Lockbox, no Forward, no CFD adapters, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.
