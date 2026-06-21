# Carver S27 ZN V/Q/M Ten-Year Vol History And Runtime Shape Gate Draft

Date: 2026-05-31

Status:

```text
PROCESS_ONLY_S27_ZN_V_Q_M_TEN_YEAR_VOL_HISTORY_AND_RUNTIME_SHAPE_GATE_DRAFT_NOT_DATA_AUTHORIZATION
```

## Purpose

Define the next clean gate needed to unblock S27 V/Q/M volatility attenuation for the ZN worked-example path.

This is a process-only draft. It does not authorize provider access, data download, market-row parsing, S27 forecast execution, diagnostics, backtests, positions, costs, carry, deployment, trading, promotion, or Git operations.

## Source Requirement

S27 requires the S13-style volatility attenuation mechanism:

```text
sigma_i_t: current estimated percentage standard deviation from Strategy 3
V_i_t: current sigma_i_t divided by the ten-year rolling average sigma for the same instrument
Q_i_t: historical quantile point of V_i_t for the same instrument
M_i_t: EWMA span 10 of 2 - 1.5 * Q_i_t
```

The output of this future gate is only a prevalidated runtime ledger:

```text
one S27 V/Q/M vol_multiplier runtime row per existing S26 hourly forecast row
```

## Required Data Shape

Lane:

```text
SOURCE_NATIVE_FUTURES
```

Instrument:

```text
book worked-example surface: US 10-year future / ZN
```

Minimum history requirement:

```text
At least ten years of source-native daily risk-history context before each S26 forecast row, plus enough earlier warm-up rows to compute Strategy-3-style sigma_i_t without lookahead.
```

Data source decision must be explicit before execution:

```text
Databento GLBX.MDP3 dated-contract chain
or another source-native provider
or fail-closed
```

Provider-built continuous symbols remain closed unless separately authorized and source-audited:

```text
NO_PROVIDER_BUILT_CONTINUOUS_SOURCE_AUTHORITY_BY_DEFAULT
```

## Required Execution Shape For A Later Gate

A future execution gate must produce or fail-close:

```text
dated-contract chain manifest
contract lifecycle evidence
roll-plan ledger
local back-adjusted continuous daily risk-history series
provider-condition ledger
Strategy-3-style sigma_i_t ledger
ten-year rolling-average sigma ledger
relative volatility V_i_t ledger
historical quantile Q_i_t ledger
EWMA(10) M_i_t runtime ledger
one runtime row aligned to each S26 hourly forecast row
provenance and SHA256 artifacts
lean hostile audit record
```

## Alignment Rules

No-lookahead:

```text
For an S26 hourly forecast row at completed trading date D, every daily risk-history input used for sigma, ten-year average, V, Q, and M must be strictly before D unless a separately source-locked completed-date convention proves otherwise.
```

Runtime row key:

```text
row_id
author_market_code
instrument_id
raw_symbol
as_of
vol_multiplier
runtime_status
method_status
no_lookahead_status
source_artifact_sha256
```

Required runtime statuses:

```text
runtime_status: PREVALIDATED_S27_V_Q_M_VOL_ATTENUATION_RUNTIME_VALUE
method_status: LOCKED_S13_STYLE_V_Q_M_ATTENUATION_RUNTIME
no_lookahead_status: PASS_NO_LOOKAHEAD
```

## Fail-Closed Rules

The future gate must fail closed if:

```text
ten-year rolling average cannot be computed
historical V distribution is too short or ambiguous
Q quantile method is not source-locked
roll lineage is incomplete
provider condition rows are degraded/unresolved without an exclusion policy
runtime count differs from S26 forecast-row count
runtime timestamps do not match S26 forecast timestamps
identity drifts from the ZN worked-example row
any neutral/default multiplier is inserted
any diagnostics/backtests/positions/costs/carry are emitted
```

## Explicitly Closed

```text
NO_DATA_AUTHORIZATION_BY_THIS_DRAFT
NO_DATABENTO_CALL_BY_THIS_DRAFT
NO_MARKET_ROW_PARSING_BY_THIS_DRAFT
NO_S27_FORECAST_EXECUTION_BY_THIS_DRAFT
NO_STRATEGY_TEST
NO_DIAGNOSTIC
NO_BACKTEST
NO_POSITION
NO_COST
NO_CARRY
NO_OOS
NO_LOCKBOX
NO_FORWARD
NO_DEPLOYMENT
NO_TRADING
NO_PROMOTION
NO_GIT_OPERATION
```

## Next Decision

```text
NEXT_GATE: S27_ZN_V_Q_M_TEN_YEAR_VOL_HISTORY_DATABENTO_EXECUTION_OR_FAIL_CLOSED_DECISION
```

That next gate must explicitly state the provider, symbols/contracts or discovery method, date range, schema, output root, and budget/risk boundary before any provider call.
