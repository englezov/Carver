# S09 And S27 Full Book Faithfulness Remediation Queue

Date: 2026-06-04

Status:

```text
PROCESS_ONLY_S09_S27_FULL_BOOK_FAITHFULNESS_REMEDIATION_QUEUE_NO_DATA_NO_BACKTEST_NO_PROVIDER_NO_GIT
```

## Operator Record

The operator identified that Strategy 27 also has book-faithfulness problems and that both Strategy 9 and Strategy 27 need future remediation before either can be described as completely book faithful.

This record parks that work explicitly.

## Strategy 9 Current Label

Current permissible label:

```text
SOURCE_NATIVE_FUTURES_STRATEGY_9_FORECAST_MACHINERY_FAITHFUL
FRACTIONAL_RESEARCH_BACKTEST_NOT_FULL_BOOK_EXECUTION_MODEL
```

Blocking gap:

Strategy 9 forecast machinery is book/source faithful, but the current validation backtest is a fractional contract-equivalent research diagnostic. It does not yet implement the full book execution model:

- capital;
- target risk;
- current risk;
- FX;
- price;
- instrument weight;
- IDM;
- average position;
- buffer `F = 0.10`;
- current-position-aware trade decision;
- whole-contract rounding.

Required future remediation:

```text
S09_FULL_BOOK_EXECUTION_MODEL_GATE
```

That gate must implement and audit the full Carver position-sizing and execution layer before any result is called a complete book-faithful Strategy 9 trading-plan result.

## Strategy 27 Current Label

Current permissible label:

```text
S27_SOURCE_NATIVE_FUTURES_CODE_BOUNDARY_DAILY_RUNTIME_LOCKED
NOT_YET_BOOK_FAITHFUL_S27_VALIDATION_OR_EXECUTION_RESULT
```

2026-06-04 implementation update:

`docs/process/CARVER_S27_BOOK_SOURCE_FAITHFULNESS_FIX_RESULT_2026-06-04.md` records the code-level fix:

- S26/S27 forecast handoff now requires a locked daily back-adjusted EWMA5 equilibrium runtime;
- S27 trend runtime now requires a daily EWMAC16/64 method label;
- S27 volatility attenuation runtime now requires a daily S13 ten-year V/Q/M method label;
- stale S27 executables that recompute S26 EWMA5 from hourly rows now fail closed.

Remaining blocking gaps:

1. The S26/S27 equilibrium must be supplied by prevalidated daily back-adjusted futures close runtime ledgers for any future S27 result. The code boundary now enforces this, but the future result gate still needs actual locked ledgers.

2. The Strategy 27 trend overlay must be daily Part One EWMAC16/64. Any executable path that computes the overlay from hourly points is not book faithful.

3. The volatility attenuation path must be source-complete: current volatility divided by a ten-year rolling average, historical quantile `Q`, and EWMA10 multiplier `M = EWMA10(2 - 1.5Q)`, all daily/no-lookahead and hash-bound before hourly use.

4. Current S27 state is ZN development/reconciliation scaffolding, not a book-level Strategy 27 fast-stack validation across the book's intended fast-strategy setting.

5. Position/execution/cost semantics remain readiness-only and are not yet the full book execution simulator.

Required future remediation:

```text
S27_FULL_BOOK_FAST_STACK_SOURCE_LOCK_GATE
```

That gate must separately lock:

- daily back-adjusted close history;
- daily EWMA5 equilibrium runtime;
- hourly current-price forecast timestamps;
- daily EWMAC16/64 trend runtime exposed safely to hourly forecasts;
- daily S03 volatility history;
- ten-year rolling average volatility;
- historical volatility quantile;
- EWMA10 volatility multiplier;
- no-lookahead provenance and SHA256 binding for every runtime;
- Strategy 26 dependency;
- Strategy 27 no-opposition-to-trend rule;
- final scalar/cap behavior;
- book execution semantics, including hourly completed bars, limit/market behavior, tick rounding, commissions, spread/market-order cost treatment, no buffering where the book requires no buffering, and capacity guards.

## Governance Boundary

Neither S09 nor S27 should be promoted, marketed, or described as a complete book-faithful trading implementation until its full book-faithfulness remediation gate is complete and separately audited.

The existing S09 VALIDATION collapse remains meaningful only under its current label:

```text
FRACTIONAL_RESEARCH_BACKTEST_NOT_FULL_BOOK_EXECUTION_MODEL
```

The existing S27 machinery remains meaningful only as source-native readiness/scaffolding until the daily-equilibrium, daily-trend, volatility-runtime, and execution layers are source-locked.

## Non-Authorization

This record authorizes no implementation, data access, parsing, provider/API call, diagnostic, backtest, OOS, Lockbox, Forward, deployment, trading, promotion, Git staging, commit, push, PR, or remote operation.
