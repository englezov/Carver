# Carver Source-Native Translation Architecture Goal

Date: 2026-05-28

Status:

```text
PROCESS_ONLY_CARVER_SOURCE_NATIVE_TRANSLATION_ARCHITECTURE_GOAL_NOT_DATA_NOT_STRATEGY_AUTHORIZATION
```

## Purpose

This record accepts the Opus source-translation architecture as the working goal for the clean Carver workspace, with corrections noted below.

The goal is to use the Carver book as source authority, translate book strategies into locked source-native futures candidate briefs, reconstruct complete book portfolios separately, and keep all data, implementation, testing, backtesting, OOS, Lockbox, Forward, CFD adapter, deployment, trading, and promotion work behind explicit future authorization gates.

## Accepted Architecture

The accepted high-level path is:

```text
Carver.pdf
-> M0 Source-Native Futures Foundation Spec
-> shared modules M1-M3
-> standalone/sleeve/overlay strategy briefs
-> complete portfolio reconstruction briefs
-> later separate fast-stack and RV-stack briefs only if explicitly authorized
```

The architecture is process-only. It is not a data lane, strategy lane, test lane, backtest lane, OOS lane, Lockbox lane, Forward lane, CFD adapter lane, deployment lane, trading lane, or promotion lane.

## Corrected Source Notes

The Opus architecture is accepted with these corrections and guardrails:

1. Forecast-block / "Lego" source reference:
   - The working source anchor is Strategy 11, especially the combined trend/carry building-block discussion around Carver PDF pages 264-265.
   - The Opus reference to page 406 for the "Lego" architecture is not accepted as-is and must be page-audited before any candidate brief quotes it.

2. Page references:
   - Opus page references are useful planning aids, not locked citation authority.
   - Every candidate brief or portfolio brief must re-check its own source pages against `Carver.pdf` before becoming a locked artifact.

3. S29 and S30:
   - Strategy 29, Cross instrument triplets, is admitted as source-native futures material but parked as:

```text
PARKED_NOT_STANDALONE
```

   - Strategy 30, Calendar trading strategies, is admitted as source-native futures material but parked as:

```text
PARKED_NOT_STANDALONE
```

   - They should be reconstructed only through their relative-value portfolio/synthetic-instrument context, not treated as clean standalone alpha candidates.

4. S28:
   - Strategy 28, Cross instrument spreads, remains eligible for a future source-native relative-value brief, but only with explicit caveats about synthetic-instrument complexity, costs, leverage, and the separate RV stack.

## Working Module Goal

The reusable translation modules are the durable goal of the process:

| Module | Working name | Role |
| --- | --- | --- |
| M0 | Source-Native Futures Foundation Spec | Completed bars, source-native contract identity, roll/calendar rules, back-adjustment, costs, FX, target risk, sizing, rounding, eligibility, evidence-window guard. |
| M1 | Position Sizing And Risk Scaling | Capital, risk target, volatility estimate, position sizing, IDM, rounding, buffering boundary. |
| M2 | Forecast-Block Architecture | Raw forecast, scaling, cap, forecast weights, diversification multiplier, speed/cost eligibility, buffering. |
| M3 | Multi-Instrument Portfolio Construction | Instrument weights, asset-class grouping, IDM, eligibility, minimum capital, sleeve fail-closed behavior. |
| M4 | Asset-Class And Normalised-Price Module | Normalised prices, asset-class membership, cross-sectional aggregation. |
| M5 | Futures Curve And Carry Module | Held/near/far contract logic, carry, carry smoothing, accurate carry, synthetic spot, multi-expiry availability. |
| M6 | Synthetic-Instrument RV Module | Spread/triplet construction, hedge ratios, synthetic prices, leg synchronization, leverage/cost treatment. |
| M7 | Hourly Fast-Stack Module | Hourly completed bars, daily equilibrium update, no-buffering rule, fast-stack separation. |
| M8 | Risk-Management Overlay Module | Risk-management lattice only; not alpha evidence and not promotion authority. |

## Accepted First Ten Brief Goal

The working first-ten sequence is accepted as the planning goal, subject to one-at-a-time operator authorization:

1. M0 Source-Native Futures Foundation Spec.
2. S01 Buy-and-hold, single contract.
3. S02 Buy-and-hold with risk scaling.
4. S03 Buy-and-hold with variable risk scaling.
5. S04 Buy-and-hold portfolio with variable risk position sizing.
6. P01 Risk parity example portfolio.
7. P02 All Weather example portfolio.
8. S09 Multiple trend following rules.
9. S10 Basic carry.
10. S11 Combined carry and trend.

S05-S08 are intentionally treated as source-native portfolio sleeves or building blocks rather than first-order standalone alpha candidates.

## Standing Rules

- Every future lane must declare exactly one class before data work:

```text
SOURCE_NATIVE_FUTURES
CFD_DIRECT
CFD_ADAPTER
```

- The default class for Carver book strategy translation is `SOURCE_NATIVE_FUTURES` unless the book source explicitly says otherwise.
- CFD adapter work remains quarantined and requires a separate explicit adapter gate after source-native behavior exists.
- Complete book portfolios must be reconstructed separately from individual sleeve results.
- A sleeve failing standalone is not family death if the book frames it as portfolio material.
- Parked/not-standalone is not failed alpha.
- No old QuantLab_v3 adapters, broker-clock assumptions, data-prep scripts, contaminated results, stale pipeline state, TEST/VALIDATION/Lockbox state, or convenience shortcuts are active authority.
- No data export, market-row parsing, implementation, tests/backtests, diagnostics, OOS, Lockbox, Forward, CFD adapter execution, tuning, deployment, trading, or promotion is authorized by this file.
- No diagnostic or backtest over 2 years may be run without explicit operator approval.
- Completed bars only.
- No tuning parameters, thresholds, filters, exits, symbols, costs, or windows after seeing results.

## Next Goal Gate

The next recommended authorization remains:

```text
Operator authorizes exactly one process-only Carver brief drafting pass for
the Source-Native Futures Foundation Spec (Module M0).

Purpose:
Lock M0 atoms as a single process artifact. No subsequent briefs.

Scope:
Inspect only Carver.pdf and repo-local clean mission/process artifacts.
Draft a process artifact only. No market data, no computation,
no strategy implementation, no parsing, no tests, no diagnostics,
no backtests, no OOS, no Lockbox, no Forward, no CFD adapter,
no old-adapter import, no tuning, no deployment, no trading, no promotion.

Forbidden:
Any work on S01 or any later brief until M0 is operator-locked.

Required status:
PROCESS_ONLY_CARVER_M0_FOUNDATION_BRIEF_DRAFT_NOT_DATA_NOT_STRATEGY_AUTHORIZATION
```

