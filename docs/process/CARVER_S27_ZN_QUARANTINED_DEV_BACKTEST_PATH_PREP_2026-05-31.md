# Carver S27 ZN Quarantined Development Backtest Path Prep

Date: 2026-05-31

Status:

```text
PROCESS_ONLY_S27_ZN_DEV_RECON_BACKTEST_PATH_PREP_NOT_BACKTEST_AUTHORIZATION
```

## Purpose

Prepare the exact path for a later S27 ZN single-instrument Development/Reconciliation backtest without running it.

## Locked 2022-2023 Target Window

```text
target_completed_trading_date_start: 2022-01-01
target_completed_trading_date_end: 2023-12-31
request_start_utc: 2021-12-31T00:00:00Z
request_end_utc: 2024-01-01T00:00:00Z
raw-symbol chain: ZNH2, ZNM2, ZNU2, ZNZ2, ZNH3, ZNM3, ZNU3, ZNZ3, ZNH4
provider continuous fallback: CLOSED
```

## Later Execution Sequence

The next separately authorized execution chapter should proceed in this order:

1. Fetch or verify the longer ZN hourly Databento archive defined in `CARVER_S27_ZN_LONGER_HOURLY_DATABENTO_ARCHIVE_WINDOW_MANIFEST_2026-05-31.md`.
2. Preserve raw provider output, definition/symbology metadata, provider-condition metadata, request provenance, row validation, and SHA artifacts.
3. Construct or verify local dated-contract hourly lineage with no provider continuous fallback.
4. Recompute S26 hourly forecast rows over the exact target window.
5. Recompute S27 EWMAC16 trend and V/Q/M runtime rows with no lookahead.
6. Recompute S27 forecast rows with scalar `20.0`, cap `+/-20`, trend-opposition zeroing, no FDM, and no buffering.
7. Build prevalidated M1 base-position rows after capital, 20% target risk, no-lookahead annual risk estimate, ZN multiplier, USD FX, and timestamp alignment are locked.
8. Transform capped forecasts to desired positions through the locked bridge `forecast / 10 * prevalidated_base_position`; first-pass rounding remains `NEAREST` unless separately authorized.
9. Produce quarantined Development/Reconciliation backtest artifacts only if every row-level input passes.

## Required Output Families For Later Backtest

```text
raw_provider_output/
raw_provider_metadata/
sanitized_hourly_bars/
local_hourly_lineage/
s26_forecast_rows/
s27_trend_runtime_rows/
s27_vqm_runtime_rows/
s27_forecast_rows/
position_rows/
cost_rows_or_cost_fail_closed_record/
backtest_status/
validation/
hashes/
provenance/
local_hostile_audit/
```

## Required Labels

Every later artifact must carry:

```text
SOURCE_NATIVE_FUTURES
ZN_ONLY
S27_ONLY
DEVELOPMENT_RECONCILIATION_ONLY
NOT_OOS
NOT_LOCKBOX
NOT_FORWARD
NOT_DEPLOYMENT
NOT_TRADING
NOT_PROMOTION
NO_ALPHA_CLAIM
```

## Fail-Closed Conditions

The later backtest must fail closed on:

```text
missing dated-contract row
degraded or unresolved provider condition not explicitly allowed
duplicate hourly row
session/timestamp mismatch
roll-lineage ambiguity
S26 forecast row missing
S27 trend runtime row missing
S27 V/Q/M runtime row missing
forecast cap drift
forecast divisor drift
position sizing input missing
prevalidated M1 base-position row missing or timestamp-misaligned
forecast-to-position divisor drift
rounding policy drift
multiplier or FX unresolved
commission value missing when costed backtest is requested
spread or market-order cost assumption
OOS/Lockbox/Forward access
```

## Non-Authorization

This prep artifact authorizes no provider API access, no data download, no market-row parsing, no diagnostics, no backtests, no returns, no PnL, no forecasts, no positions, no orders, no fills, no costs, no carry, no OOS, no Lockbox, no Forward, no CFD adapters, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.
