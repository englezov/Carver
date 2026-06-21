# Carver S26 Fast Mean Reversion Execution Semantics Source Gate Draft

Date: 2026-05-31

Status:

```text
PROCESS_ONLY_S26_EXECUTION_SEMANTICS_SOURCE_GATE_DRAFT_SUPERSEDED_BY_SOURCE_LOCK_RESULT_NOT_TEST_NOT_BACKTEST
```

## Purpose

Define the source-faithful execution semantics that must be locked before any S26 or S27 strategy test.

This gate is design/source only. It does not run execution, diagnostics, backtests, positions, orders, fills, costs, or performance analysis.

Superseding result:

```text
docs/process/CARVER_S26_EXECUTION_SEMANTICS_SOURCE_LOCK_RESULT_2026-05-31.md
```

## Source Atoms To Lock

S26 source anchors from the S26/S27 source atom sheet and Opus audit:

```text
Carver p. 475: Part Four strategies use hourly data and can trade more frequently than daily strategies.
Carver pp. 479-480: S26 fast mean-reversion forecast is EWMA(5) equilibrium minus price, risk adjusted, scalar 9.3, capped at +/-20.
Carver p. 481: S26 has no buffering and may use limit rather than market orders.
Carver p. 476/478: holding period around one or two days, not HFT.
```

## Required Decisions Before Testing

The execution source gate must decide or fail-close:

```text
forecast availability timestamp: completed hourly bar only
signal availability: after derived_completed_bar_end_utc
order intent: limit-order style, not market-order assumption
buffering: closed / not used
execution cadence: source-faithful hourly cadence, no intrabar lookahead
position sizing: closed until separate sizing gate
cost model: closed until separate cost/execution gate
slippage/spread: closed until separate execution evidence gate
```

## Explicit Fail-Closed Rules

Fail closed if any future artifact:

- treats the S26 forecast row as tradable before the completed hourly bar timestamp;
- uses market-order fills as if Carver had specified them for S26;
- adds buffering;
- computes positions, contracts, orders, fills, costs, returns, diagnostics, or backtests;
- applies daily Parts One-Three forecast-combination machinery;
- reuses the G_R1B/G_R1C sigma runtime as a full S03 position-sizing estimate.

## Output Of This Future Gate

Allowed future output:

```text
S26_EXECUTION_SEMANTICS_SOURCE_LOCK
```

Implemented status:

```text
PASS_S26_EXECUTION_SEMANTICS_SOURCE_LOCK_DESIGN_ONLY_NOT_TEST_NOT_BACKTEST
```

Fields:

```text
hourly_completed_bar_policy
forecast_availability_policy
limit_order_semantics_policy
no_buffering_policy
no_market_order_cost_assumption_policy
test_boundary_status
```

## Non-Authorization

This draft authorizes no provider API access, no new data download, no market-row expansion, no real forecast-series execution, no diagnostics, no backtests, no returns, no PnL, no positions, no orders, no fills, no costs, no carry, no trend computation, no S27 real-data computation, no testing, no OOS, no Lockbox, no Forward, no CFD adapters, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.
