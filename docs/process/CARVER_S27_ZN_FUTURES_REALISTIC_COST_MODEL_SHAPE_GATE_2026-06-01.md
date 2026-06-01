# Carver S27 ZN Futures-Realistic Cost Model Shape Gate

Status:

```text
PROCESS_ONLY_FUTURES_REALISTIC_COST_MODEL_SHAPE_GATE_NOT_EXECUTED
```

## Purpose

Define the cost-model evidence and execution shape required to close Opus CRITICAL-1 before any Lockbox or promotional interpretation of the S27 ZN result.

This is a shape gate only. It performs no provider API access, no new data download, no market-row parsing, no diagnostics, no backtest, no new forecast execution, no position execution, no cost execution, no OOS, no Lockbox, no Forward, no tuning, no deployment, no trading, no promotion, and no Git operation.

## Lane

```text
SOURCE_NATIVE_FUTURES
```

## Blocking Finding Addressed

Opus finding:

```text
CRITICAL-1: Cost model not futures-realistic
```

Existing cost lock:

```text
docs/process/CARVER_S27_ZN_POSITION_EXECUTION_COST_SEMANTICS_LOCK_2026-05-31.md
Status: PASS_S27_ZN_POSITION_EXECUTION_COST_SEMANTICS_LOCK_NOT_BACKTEST
```

That lock allowed only a clearly labeled Development/Reconciliation commission surface. It did not close spread, slippage, limit-order fill quality, exchange fees, broker fees, routing, margin/funding assumptions, or breakeven-cost sensitivity.

## Required Cost Components

The later execution gate must lock all of the following before running any cost-adjusted robustness or Lockbox-facing statistic:

| Component | Required disposition |
|---|---|
| Exchange fee | `LOCKED_FROM_STATIC_FEE_SOURCE` or `FAIL_CLOSED` |
| Clearing/NFA/regulatory fees | `LOCKED_FROM_STATIC_FEE_SOURCE` or `FAIL_CLOSED` |
| Broker commission | `LOCKED_FROM_ACCOUNT_OR_PUBLIC_STATIC_SOURCE` or `FAIL_CLOSED` |
| ZN minimum tick value | `LOCKED_FROM_CONTRACT_SPEC` |
| ZN bid/ask spread assumption | `LOCKED_FROM_STATIC_OR_EMPIRICAL_SOURCE` or scenario-grid only |
| Slippage model | locked scenario grid in ticks |
| Limit-order fill model | deterministic fill-probability scenario or fail-closed if not modeled |
| Order-routing assumption | `LOCKED_STATIC_ROUTING_ASSUMPTION` or `NOT_APPLICABLE_WITH_RATIONALE` or `FAIL_CLOSED` |
| Margin/funding assumption | `LOCKED_STATIC_MARGIN_FUNDING_ASSUMPTION` or `NOT_APPLICABLE_WITH_RATIONALE` or `FAIL_CLOSED` |
| Roll-transition cost policy | explicit close/open side accounting |
| Fee application side count | machine-verified against position changes |
| Unit/no-ladder cost sensitivity | required |
| M1-ladder cost sensitivity | required |

## Minimum Scenario Grid

The first futures-realistic cost execution must report at least:

```text
commission_only_current_dev_recon_reference
fees_plus_0_tick_spread_slippage
fees_plus_0_25_tick_per_side
fees_plus_0_50_tick_per_side
fees_plus_1_00_tick_per_side
limit_fill_100_percent
limit_fill_75_percent
limit_fill_50_percent
breakeven_cost_per_side
```

If a scenario cannot be sourced or modeled without invention, it must be marked:

```text
UNRESOLVED_FAIL_CLOSED_NOT_USED_FOR_PASS_FAIL
```

## Source-Faithfulness Boundary

Carver S26/S27 discusses limit-order-aware execution for fast mean reversion. Therefore:

- market-order-only spread/slippage must not be silently treated as source-faithful;
- fill probability and non-fill risk must be explicit;
- a no-fill or partial-fill model may reduce trade count and PnL, but it must not tune entries or exits after seeing results;
- order-routing and margin/funding must be locked, explicitly ruled not applicable with rationale, or fail-closed;
- the result must remain labeled Development/Reconciliation until a separately authorized Lockbox gate exists.

## Cost-Adjusted Metrics Required Before Lockbox

For both `UNIT_NO_LADDER` and `M1_LADDER`, the execution gate must report:

- gross PnL;
- commission/fee PnL impact;
- spread/slippage PnL impact by scenario;
- non-fill PnL impact by scenario;
- net PnL;
- signal-attributable net PnL;
- breakeven cost per side;
- trade/side count;
- average cost per side;
- year/sub-period cost attribution.

## Fail-Closed Rules

The cost execution must fail closed if:

- any cost source is not declared;
- tick value or multiplier is missing;
- fee side count cannot be reconciled;
- unit/no-ladder and M1-ladder variants are blended;
- cost assumptions are changed after seeing robustness results;
- a prop-firm/platform cost is substituted for source-native futures cost without an adapter gate;
- a CFD spread or CFD broker-clock assumption is used in this source-native lane.
- routing or margin/funding is omitted without an explicit `NOT_APPLICABLE_WITH_RATIONALE` or `FAIL_CLOSED` status.

## Exit Criteria

This cost chapter can close CRITICAL-1 only when:

```text
FUTURES_REALISTIC_COST_MODEL_SHA_PINNED
UNIT_AND_M1_LADDER_COST_SENSITIVITY_REPORTED
BREAKEVEN_COST_REPORTED
ROUTING_AND_MARGIN_FUNDING_DISPOSITION_RECORDED
NO_CFD_OR_PROP_ADAPTER_SUBSTITUTION
NO_LOCKBOX_OPENED
```

## Non-Authorization

This shape gate authorizes no:

```text
provider API access
new data download
market-row parsing
new diagnostics
new backtests
new forecasts
new positions
cost execution
OOS
Lockbox
Forward
CFD adapters
old QuantLab active-pipeline use
tuning
deployment
trading
promotion
Git staging
commit
push
PR update
remote operations
```
