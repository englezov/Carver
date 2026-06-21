# Carver S27 ZN Backtest Readiness Local Lean Hostile Audit

Date: 2026-05-31

Mode: Local hostile audit over the S27 ZN backtest readiness artifacts. No provider API access, no data download, no market-row parsing, no diagnostics, no backtests, no forecasts, no positions, no costs, no deployment, no trading, no promotion, no Git operations.

## Audited Artifacts

```text
docs/process/CARVER_S26_S27_COMPLETED_FORECAST_MACHINERY_LOCAL_HOSTILE_AUDIT_2026-05-31.md
docs/process/CARVER_S27_ZN_SINGLE_INSTRUMENT_BACKTEST_READINESS_GATE_DRAFT_2026-05-31.md
docs/process/CARVER_S27_ZN_POSITION_EXECUTION_COST_SEMANTICS_LOCK_2026-05-31.md
docs/process/CARVER_S27_ZN_LONGER_HOURLY_DATABENTO_ARCHIVE_WINDOW_MANIFEST_2026-05-31.md
docs/process/CARVER_S27_ZN_QUARANTINED_DEV_BACKTEST_PATH_PREP_2026-05-31.md
src/carver/spine/s26_s27.py
tests/test_s26_s27_fast_mean_reversion_synthetic.py
```

## Critical

None.

No audited artifact executes or authorizes:

```text
provider API access
data download
market-row parsing
diagnostics
backtests
returns
PnL
positions
orders
fills
costs
OOS
Lockbox
Forward
deployment
trading
promotion
Git operations
```

## High

None.

The readiness path is narrow:

```text
strategy: S27 only
instrument: ZN only
row_id: APPENDIX_C_172_004 only
lane: SOURCE_NATIVE_FUTURES only
window manifest: 2022-01-01 through 2023-12-31 completed trading dates
request envelope: 2021-12-31T00:00:00Z through 2024-01-01T00:00:00Z
raw-symbol chain: ZNH2, ZNM2, ZNU2, ZNZ2, ZNH3, ZNM3, ZNU3, ZNZ3, ZNH4
provider continuous fallback: CLOSED
```

## Medium

None blocking.

The position/execution/cost semantics lock explicitly prepares position output but does not compute it. It requires a later execution gate to lock capital, target risk, annual risk estimate, multiplier, FX, rounding, and any commission value before positions or costs can be emitted.

## Low

The first backtest path is still a Development/Reconciliation mechanics check, not evidence of performance. The documents repeat `NO_ALPHA_CLAIM`, `NOT_OOS`, `NOT_LOCKBOX`, `NOT_FORWARD`, and `NOT_PROMOTION`.

## Disposition

```text
BLOCKING_FINDINGS: NO
AUDIT_DISPOSITION: PASS_S27_ZN_BACKTEST_READINESS_PATH_NOT_BACKTEST
```

## Non-Authorization

This audit result authorizes no provider API access, no data download, no market-row parsing, no diagnostics, no backtests, no returns, no PnL, no forecasts, no positions, no orders, no fills, no costs, no carry, no OOS, no Lockbox, no Forward, no CFD adapters, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.
