# Carver S27 Real-Hourly Forecast-Only Handoff Plumbing Result

Date: 2026-05-31

Status:

```text
PROCESS_AND_CODE_S27_REAL_HOURLY_FORECAST_ONLY_HANDOFF_PLUMBING_COMPLETE_NOT_REAL_EXECUTION
```

## Scope

This record preserves the S27 forecast-only plumbing added after the S26 G_R1C forecast-series plumbing.

Implemented code:

```text
src/carver/spine/s26_s27.py
tests/test_s26_s27_fast_mean_reversion_synthetic.py
src/carver/spine/__init__.py
```

The S27 handoff consumes prevalidated runtime rows only:

```text
S26 forecast-only row
S27 EWMAC16 trend-overlay runtime row
S27 V/Q/M volatility-attenuation runtime row
```

It does not compute unresolved real-data dependencies by itself.

## Source-Faithful Boundary

The handoff preserves the source design:

```text
S27 depends on S26
S27 mean-reversion forecast must not oppose trend
S27 uses its Chapter 27 scalar around 20 and the common forecast cap +/-20
S27 uses no forecast-combination FDM
S27 remains forecast-only, not diagnostic/backtest/position output
```

2026-06-01 clarification:

```text
The previous phrase "inherits S26 scalar 9.3" was stale wording.
S26 keeps scalar 9.3.
S27 uses the Chapter 27 p. 502 scalar around 20 after the trend overlay and volatility multiplier.
```

## Runtime Lock Requirements

Before real S27 execution can occur, separate gates must produce:

```text
prevalidated no-lookahead S26 forecast-only series rows
prevalidated no-lookahead EWMAC16 trend-overlay runtime rows
prevalidated no-lookahead S13-style V/Q/M attenuation runtime rows
hash-shaped provenance for each runtime source artifact
```

The handoff fail-closes malformed SHA256 provenance, unresolved source locks, stale runtime timestamps, and out-of-envelope volatility multipliers.

Post-audit hardening:

```text
S27 verifies the S26 input row identity/source-lock contract before handoff.
S26 raw Databento hourly source hashes must be 64-hex SHA256 values.
S27 stale trend-runtime and stale V/Q/M-runtime timestamps fail closed.
S27 trend and V/Q/M runtime rows are instrument-bound to the paired S26 forecast row.
```

## Verification

Synthetic/unit verification only:

```text
python -m unittest tests.test_s26_s27_fast_mean_reversion_synthetic -v
```

Result:

```text
24 focused S26/S27 tests passed after post-audit hardening
179 full repository tests passed after post-audit hardening
secret scan for Databento-style keys: no matches
```

## Non-Authorization

This result authorizes no provider API access, no new data download, no market-row expansion, no real S27 execution, no diagnostics, no backtests, no returns, no PnL, no positions, no orders, no fills, no costs, no carry, no testing, no OOS, no Lockbox, no Forward, no CFD adapters, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.
