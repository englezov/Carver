# Carver P05 Complete Trend Portfolio Source-Shape Gate Draft

Date: 2026-05-29

Status:

```text
PROCESS_ONLY_CARVER_P05_COMPLETE_TREND_PORTFOLIO_SOURCE_SHAPE_GATE_DRAFT_NOT_DATA_NOT_IMPLEMENTATION
```

## Purpose

Define the future complete P05 trend portfolio conformance boundary before any implementation.

This draft distinguishes complete P05 from the existing `MES / ZN / ZF` phase-1 construction seed, identifies unresolved P05 source atoms and data/readiness atoms, and defines audit requirements before any later implementation gate.

This draft does not authorize code edits, tests, real data, market-row parsing, NinjaTrader export, diagnostics, backtests, portfolio implementation, Opus execution, remote operations, deployment, trading, or promotion.

## Current State

The audited P05/P06/P07 shape-readiness decision selected P05 as the next portfolio chapter:

```text
P05_COMPLETE_TREND_PORTFOLIO_SOURCE_SHAPE_GATE_DRAFT
```

Existing P05-adjacent machinery:

- S09 trend forecast conformance exists at process-and-synthetic scope.
- P05 phase-1 construction conformance exists for `MES`, `ZN`, and `ZF`.
- M3 defines the shared multi-instrument portfolio construction contract.
- P05 phase-1 emits desired contract counts only and does not aggregate returns or interpret performance.

## Complete-P05 Boundary

Complete P05 is not the existing phase-1 seed.

The phase-1 seed is locked only to:

```text
MES / ZN / ZF
```

with the identity:

```text
P05_PHASE1_MES_ZN_ZF_SEED_CONSTRUCTION_NOT_COMPLETE_PORTFOLIO
```

Complete P05 must be opened as its own portfolio candidate and must not infer any complete-portfolio fact from the phase-1 seed.

## Candidate Classification

P05 classification for this draft:

```text
SOURCE_NATIVE_FUTURES
COMPLETE_TREND_PORTFOLIO_CANDIDATE
PROCESS_ONLY_SOURCE_SHAPE_NOT_IMPLEMENTATION
```

No `CFD_DIRECT` or `CFD_ADAPTER` lane is opened. Any future CFD adapter work requires a separate explicit adapter gate after source-native P05 behavior exists.

## Upstream Signal Dependency

Future complete P05 implementation, if separately authorized, may depend on locked S09 trend forecast outputs only.

The dependency boundary is:

```text
locked S09 trend forecasts
-> complete P05 portfolio construction context
-> future desired position inputs
```

This draft does not authorize real data, diagnostics, backtests, returns, PnL, Sharpe, drawdown, portfolio aggregation, execution, or performance interpretation.

## P05 Source Atoms Required Before Implementation

Before any complete-P05 implementation gate, the following atoms must be source-locked or explicitly blocked:

- complete P05 portfolio identity and source pages;
- source framing: standalone candidate, source-native portfolio sleeve, or complete book portfolio;
- complete P05 instrument universe;
- whether `MES / ZN / ZF` are complete members, seed members, or only phase-1 scaffold members;
- source-native contract identity for every P05 member;
- local provider mapping requirements and no-substitution policy for every member;
- asset class, group, and instrument taxonomy if handcrafted weights apply;
- instrument weights or deterministic weighting rule;
- IDM source, exact value, or calculation policy;
- IDM applicability check for the final P05 breadth;
- portfolio capital-base policy;
- portfolio target-risk policy;
- per-instrument eligible EWMAC speed set;
- speed/cost eligibility rule;
- liquidity eligibility rule;
- minimum-capital rule;
- data-availability rule;
- forecast-to-position convention;
- rounding policy;
- buffering or explicit decision to keep buffering closed;
- missing-member behavior;
- completed-bar synchronization rule across all members;
- portfolio aggregation boundary;
- no post-result member addition, removal, rescue, reweighting, or tuning.

## Data And Readiness Atoms Required Before Real-Data Work

Before any real data, readiness execution, diagnostic, or backtest, P05 must separately lock:

- exact source-native provider IDs or approved local mappings for every selected member;
- intake route: direct daily bars or separately justified minute-derived fallback;
- session calendar and timezone artifacts;
- roll rule artifacts;
- back-adjustment artifacts;
- completed daily bar convention;
- annual risk source and validation path;
- FX source and validation path;
- cost source and validation path;
- raw-response quarantine and request/provider binding rules if API or chart data is used;
- evidence-stage label and data-window budget;
- explicit operator authorization for real-data execution.

No such data or readiness execution is authorized by this draft.

## Future Synthetic Implementation Boundary

A later complete-P05 process-and-synthetic-code gate may be considered only after this source-shape draft passes hostile audit and implementation is separately authorized.

That later gate should stop at:

```text
complete-P05 desired position inputs
```

unless a separate gate explicitly opens aggregation or performance interpretation.

The implementation boundary should fail closed unless all selected P05 source atoms are locked and should not:

- parse real market rows;
- execute readiness;
- run diagnostics;
- run backtests;
- emit returns, PnL, Sharpe, drawdown, OOS, Lockbox, or Forward evidence;
- perform trade/no-trade decisions;
- deploy, trade, or promote.

## Rejected Interpretations

### Phase-1 Seed Equals Complete P05

Rejected.

```text
P05_PHASE1_SEED_IS_NOT_COMPLETE_P05
```

### Existing S09 Forecasts Lock Complete P05

Rejected.

```text
S09_FORECAST_COMPLETION_IS_NOT_COMPLETE_P05_PORTFOLIO_AUTHORIZATION
```

### Complete P05 Can Skip Source Shape

Rejected.

```text
P05_COMPLETE_SOURCE_SHAPE_REQUIRED_BEFORE_IMPLEMENTATION
```

### Process Draft Opens Real Data

Rejected.

```text
REAL_DATA_REQUIRES_SEPARATE_EXPLICIT_OPERATOR_AUTHORIZATION
```

### Process Draft Opens P06 Or P07

Rejected.

```text
P06_P07_REMAIN_SEPARATELY_GATED
```

## Fail-Closed Requirements For Later Gates

Any later implementation or data gate must fail closed if:

- lane class is not exactly `SOURCE_NATIVE_FUTURES`;
- complete P05 portfolio identity is unresolved;
- complete P05 source pages are unresolved;
- the full P05 universe is unresolved;
- any member identity, local mapping, roll rule, session, or back-adjustment atom is unresolved;
- any Appendix C or broker code is treated as a local provider identifier without mapping lock;
- instrument weights, IDM, capital base, target risk, cost eligibility, liquidity eligibility, or minimum-capital policy are unresolved;
- per-instrument EWMAC speeds or cost/speed eligibility are unresolved;
- missing-member behavior is unresolved;
- completed-bar synchronization is unresolved;
- the phase-1 seed is treated as complete P05;
- any old `QuantLab_v3` active-pipeline artifact is used as authority;
- any member is added, dropped, rescued, reweighted, or tuned after seeing results;
- any real data, diagnostics, backtests, OOS, Lockbox, Forward, CFD adapter, deployment, trading, or promotion path is opened without separate authorization.

## Audit Requirements

Before this draft is treated as locked, a regular hostile audit should verify:

- no implementation authorization is smuggled into the draft;
- complete P05 is not inferred from the `MES / ZN / ZF` phase-1 seed;
- P05 remains a separately gated complete trend portfolio candidate;
- P06 and P07 remain closed;
- source atoms and data/readiness atoms are separated;
- future implementation stops at desired position inputs unless separately authorized;
- no real data, diagnostics, backtests, OOS, Lockbox, Forward, CFD adapters, old `QuantLab_v3` active-pipeline use, tuning, deployment, trading, promotion, Opus execution, remote operation, or GitHub action is opened.

Regular hostile audit should be lean and subagent-based when available. Opus or GPT is not required for this draft unless the operator separately authorizes a larger source-faithfulness audit.

## Suggested Regular Hostile Audit Prompt

```text
Operator authorizes exactly one regular hostile audit of the Carver P05 complete
trend portfolio source-shape gate draft.

Scope:
Audit the process-only P05 source-shape gate draft:
docs/process/CARVER_P05_COMPLETE_TREND_PORTFOLIO_SOURCE_SHAPE_GATE_DRAFT_2026-05-29.md

Allowed:
Read-only file inspection and concise audit findings.

Forbidden:
No file edits, no code tests, no real data, no market-row parsing, no
NinjaTrader export, no diagnostics, no backtests, no OOS, no Lockbox, no
Forward, no CFD adapters, no old QuantLab pipeline use, no tuning, no
deployment, no trading, no promotion, no portfolio implementation, no P06/P07
implementation, no Opus execution, no remote operations.
```

## Non-Authorization

This draft authorizes no code edits, no tests, no real-data execution, no market-row parsing, no NinjaTrader export, no diagnostics, no backtests, no returns, no PnL, no Sharpe, no drawdown, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old-adapter import, no old workspace pipeline use, no tuning, no deployment, no trading, no promotion, no portfolio implementation, no P05/P06/P07 implementation, no Opus execution, no remote push, and no GitHub action.
