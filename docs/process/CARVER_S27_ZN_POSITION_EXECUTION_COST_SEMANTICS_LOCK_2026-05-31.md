# Carver S27 ZN Position, Execution, And Cost Semantics Lock

Date: 2026-05-31

Status:

```text
PASS_S27_ZN_POSITION_EXECUTION_COST_SEMANTICS_LOCK_NOT_BACKTEST
```

## Purpose

Lock the source-faithful position, execution, and cost semantics required before any later S27 ZN backtest execution gate.

This artifact does not compute positions, returns, costs, PnL, diagnostics, or backtests.

## Position Sizing Path

The later backtest must use the existing Carver M1 sizing primitive:

```text
size_contracts(
  capital,
  target_risk,
  current_held_price,
  annual_risk_estimate,
  multiplier,
  fx_rate,
  instrument_weight,
  idm
)
```

Locked interpretation:

```text
base_position = M1 size_contracts output
forecast_multiplier = final_capped_forecast / 10
desired_unrounded_position = base_position.unrounded_contracts * forecast_multiplier
desired_rounded_position = locked rounding policy applied to desired_unrounded_position
```

The code path now preserves this as a narrow prevalidated bridge:

```text
s27_zn_desired_position_from_prevalidated_base(...)
```

That bridge does not run M1 sizing itself and does not read market rows. It accepts only a prevalidated M1 base-position artifact whose timestamp matches the S27 forecast row, then applies `final_capped_forecast / 10` and the explicitly locked first Dev/Reconciliation rounding policy.

## Required Test-Gate Locks

Before any position output, the later execution gate must explicitly lock:

```text
capital
annual target risk = 20% book default unless separately source-justified
current held price
S03-style annual percentage risk estimate
ZN contract multiplier
USD FX rate
single-instrument ZN weight = 1
single-instrument IDM = 1
rounding policy
forecast-to-position divisor = 10
```

For the first 2022-2023 ZN Development/Reconciliation backtest path, the in-code plumbing is locked to:

```text
prevalidated M1 base position required
rounding policy = NEAREST unless separately authorized
position output status = PASS_S27_ZN_DESIRED_POSITION_PLUMBING_PREVALIDATED_NOT_BACKTEST
no diagnostics / no backtest / no returns / no PnL / no costs emitted by the position bridge
```

## Execution Semantics

Locked interpretation:

```text
hourly completed bars only
forecast available only after completed-bar end
no intrabar lookahead
no buffering
limit-style execution semantics only
no market-order fill model
```

## Cost Semantics

Locked interpretation:

```text
commission-only Development/Reconciliation cost surface may be used only if the commission value is explicitly locked
spread costs remain unresolved
market-order cost assumptions remain prohibited
if cost evidence is missing, the backtest must fail closed or run a clearly labeled no-cost plumbing variant
```

## Machine Contract

Implemented validator status:

```text
S27_ZN_POSITION_EXECUTION_COST_SEMANTICS_LOCK_STATUS =
PASS_S27_ZN_POSITION_EXECUTION_COST_SEMANTICS_LOCK_NOT_BACKTEST
```

The validator rejects:

```text
non-SOURCE_NATIVE_FUTURES lanes
direct forecast-as-position shortcuts
tuned target risk
implicit portfolio IDM imports
lookahead risk estimates
optional multiplier/FX
forecast divisor drift
implicit rounding
missing or timestamp-misaligned prevalidated M1 base position
non-NEAREST rounding in the first ZN Dev/Reconciliation bridge
buffering
market-order spread-cost assumptions
any diagnostics/backtests/returns/PnL/positions/orders/fills/cost outputs
```

## Non-Authorization

This lock authorizes no provider API access, no data download, no market-row parsing, no diagnostics, no backtests, no returns, no PnL, no positions, no orders, no fills, no costs, no carry, no OOS, no Lockbox, no Forward, no CFD adapters, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.
