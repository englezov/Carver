# Carver S27 ZN 2022-2023 Development/Reconciliation Backtest Execution Gate Draft

Date: 2026-05-31

Status:

```text
PROCESS_ONLY_EXECUTION_GATE_DRAFT_NOT_AUTHORIZATION
```

## Purpose

Define the exact separately authorized execution surface for the first bounded S27 ZN single-instrument Development/Reconciliation backtest over 2022-2023.

This draft does not authorize provider API access, data download, market-row parsing, forecasts, positions, costs, diagnostics, backtests, Git operations, or promotion.

## Locked Scope For Later Authorization

```text
lane: SOURCE_NATIVE_FUTURES
strategy: S27_SAFER_FAST_MEAN_REVERSION
instrument: US 10-year Note futures
author_market_code: ZN
row_id: APPENDIX_C_172_004
test_label: DEVELOPMENT_RECONCILIATION_ONLY
alpha_claim: NO_ALPHA_CLAIM
oos_status: NOT_OOS
lockbox_status: NOT_LOCKBOX
forward_status: NOT_FORWARD
promotion_status: NOT_PROMOTION
```

## Provider Request Surface

If and only if a later operator execution gate explicitly opens provider access, the data request is locked to:

```text
provider: DATABENTO_HISTORICAL
dataset: GLBX.MDP3
schema: ohlcv-1h
stype_in: raw_symbol
request_start_utc: 2021-12-31T00:00:00Z
request_end_utc: 2024-01-01T00:00:00Z
target_completed_trading_date_start: 2022-01-01
target_completed_trading_date_end: 2023-12-31
raw_symbols: ZNH2, ZNM2, ZNU2, ZNZ2, ZNH3, ZNM3, ZNU3, ZNZ3, ZNH4
continuous_contracts: FORBIDDEN
expanded_symbols: FORBIDDEN
```

## Output Quarantine Root

All later execution artifacts must live under:

```text
docs/researchops/s26_s27_backtest_readiness/ZN_S27_SINGLE_INSTRUMENT/2022-01-01_2023-12-31/
```

Required output families for a later authorized execution:

```text
raw_provider_output/
raw_provider_metadata/
provider_condition_metadata/
sanitized_hourly_bars/
local_hourly_lineage/
roll_plan/
adjustments/
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

## Local Lineage Rules

The execution must construct a local dated-contract hourly lineage from the locked ZN raw-symbol chain only.

```text
provider_built_continuous_contract: FORBIDDEN
silent_substitution: FORBIDDEN
silent_drop: FORBIDDEN
silent_reweight: FORBIDDEN
missing_row_policy: FAIL_CLOSED_ZERO_SILENT_ROW_SKIP
provider_condition_policy: AVAILABLE_OR_NORMAL_ONLY_UNLESS_AUDITED_EXCEPTION
roll_policy: LOCKED_LOCAL_DETERMINISTIC_ROLL_RULE_REQUIRED
back_adjustment_policy: LOCKED_LOCAL_ADDITIVE_BACK_ADJUSTMENT_REQUIRED
completed_bar_policy: COMPLETED_HOURLY_BARS_ONLY
lookahead_policy: NO_LOOKAHEAD
```

## Forecast And Backtest Sequence

The later execution gate must run in this order:

1. Preserve raw provider output, metadata, provider-condition records, provenance, validation, and hashes.
2. Sanitize only the locked `ohlcv-1h` ZN rows into quarantine hourly bars.
3. Build local hourly dated-contract lineage and fail closed on unresolved roll or adjustment inputs.
4. Recompute S26 hourly forecast rows from source-faithful hourly completed bars.
5. Recompute S27 EWMAC(16,64) trend runtime rows from locked local continuous daily input with no lookahead.
6. Recompute S27 V/Q/M attenuation rows from locked volatility history with no lookahead.
7. Recompute S27 forecast rows with scalar `20.0`, cap `+/-20`, no FDM, no buffering, and trend-opposition zeroing.
8. Build prevalidated M1 base-position rows only after capital, target risk, annual risk estimate, ZN multiplier, USD FX, and timestamp alignment are locked.
9. Apply the locked S27 position bridge: `desired_unrounded_position = prevalidated_base_position * (final_capped_forecast / 10)`, with first Dev/Reconciliation rounding locked to `NEAREST` unless separately authorized.
10. Emit costs only if a commission-only value is explicitly locked; otherwise emit a cost fail-closed record rather than invented costs.
11. Emit a Development/Reconciliation backtest status record with no alpha claim.

## Fail-Closed Conditions

The later execution must fail closed if any of the following occur:

```text
Databento request differs from locked dataset/schema/symbols/window
any continuous-contract request is attempted
any non-ZN symbol is requested or parsed
any required raw symbol is missing
any target completed hourly bar is missing, duplicate, stale, malformed, or session-misaligned
provider condition is degraded, unavailable, or unresolved without a separately audited exception
local roll lineage cannot be proven
local additive adjustment cannot be reproduced
S26 forecast row is missing
S27 trend runtime row is missing
S27 V/Q/M runtime row is missing
position sizing input is missing
prevalidated M1 base-position row is missing or timestamp-misaligned
forecast-to-position divisor differs from 10
rounding policy differs from locked first-pass NEAREST policy without separate authorization
cost value is missing when a costed backtest is requested
spread or market-order cost model is introduced
OOS, Lockbox, Forward, deployment, trading, promotion, or alpha claim appears
```

## Non-Authorization

This draft authorizes no provider API access, no data download, no market-row parsing, no diagnostics, no backtests, no returns, no PnL, no forecasts, no positions, no orders, no fills, no costs, no carry, no OOS, no Lockbox, no Forward, no CFD adapters, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.
