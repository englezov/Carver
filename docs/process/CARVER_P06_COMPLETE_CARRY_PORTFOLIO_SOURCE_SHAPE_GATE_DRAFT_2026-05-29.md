# Carver P06 Complete Carry Portfolio Source-Shape Gate Draft

Date: 2026-05-29

Status:

```text
PROCESS_ONLY_CARVER_P06_COMPLETE_CARRY_PORTFOLIO_SOURCE_SHAPE_GATE_DRAFT_NOT_DATA_NOT_IMPLEMENTATION
```

## Purpose

Define the future complete P06 carry portfolio conformance boundary before any implementation.

This draft distinguishes P06 portfolio work from the already-completed S10 carry signal block, identifies unresolved P06 source atoms and data/readiness atoms, and defines audit requirements before any later implementation gate.

This draft does not authorize code edits, tests, real data, market-row parsing, NinjaTrader export, diagnostics, backtests, portfolio implementation, P07 implementation, Opus/GPT execution, remote operations, deployment, trading, or promotion.

## Current State

Completed upstream signal machinery:

```text
S10/M5 carry construction conformance
S10 carry forecast-block conformance
```

Completed adjacent portfolio machinery:

```text
P05 complete trend portfolio synthetic conformance
```

Recent sequencing decision:

```text
docs/process/CARVER_POST_P05_COMPLETE_TREND_PORTFOLIO_NEXT_STEP_DECISION_2026-05-29.md
```

That decision selected:

```text
P06_COMPLETE_CARRY_PORTFOLIO_SOURCE_SHAPE_GATE_DRAFT
```

## P06 Boundary

P06 is not S10.

S10 completion proves a synthetic carry signal path:

```text
M5 risk-adjusted carry input
-> Carry5/20/60/120 smoothing
-> scalar 30
-> caps
-> eligible span set
-> equal weights
-> carry FDM
-> final capped S10 carry forecast output
```

P06, if later implemented, is a complete carry portfolio candidate that must add portfolio-specific source shape:

```text
locked S10 carry forecast outputs
-> complete P06 portfolio member universe
-> P06 weights / IDM / target-risk / capital context
-> P06 member eligibility and readiness policy
-> future desired position inputs only
```

No P06 fact may be inferred merely from S10 signal completion.

## Candidate Classification

P06 classification for this draft:

```text
SOURCE_NATIVE_FUTURES
COMPLETE_CARRY_PORTFOLIO_CANDIDATE
PROCESS_ONLY_SOURCE_SHAPE_NOT_IMPLEMENTATION
```

No `CFD_DIRECT` or `CFD_ADAPTER` lane is opened. Any future CFD adapter work requires a separate explicit adapter gate after source-native P06 behavior exists.

## Upstream Signal Dependency

Future P06 implementation, if separately authorized, may depend on locked S10 carry forecast-block outputs only.

The dependency boundary is:

```text
locked S10 carry forecasts
-> complete P06 portfolio construction context
-> future desired position inputs
```

This draft does not authorize real data, diagnostics, backtests, returns, PnL, Sharpe, drawdown, portfolio aggregation, execution, or performance interpretation.

## P06 Source Atoms Required Before Implementation

Before any complete-P06 implementation gate, the following atoms must be source-locked or explicitly blocked:

- complete P06 portfolio identity and source pages;
- source framing: standalone candidate, source-native portfolio sleeve, or complete book portfolio;
- relationship between P06 and Strategy Ten basic carry;
- complete P06 instrument universe;
- whether P06 uses the Jumbo universe, a carry-eligible subset, or another source-defined universe;
- source-native contract identity for every P06 member;
- local provider mapping requirements and no-substitution policy for every member;
- asset class, group, and instrument taxonomy if handcrafted weights apply;
- instrument weights or deterministic weighting rule;
- IDM source, exact value, approximation table, or calculation policy;
- IDM applicability check for the final P06 breadth;
- portfolio capital-base policy;
- portfolio target-risk policy;
- per-instrument eligible carry span set;
- carry span cost/turnover eligibility rule;
- carry FDM row policy for partial eligibility;
- carry forecast-to-position convention;
- source treatment of members with no eligible carry span;
- carry-eligible curve-leg availability requirements;
- held/comparison contract role rule;
- production raw-carry sign convention by instrument family;
- production expiry calendar or annualization convention;
- production roll-day handling;
- fixed-month commodity policy;
- seasonal carry handling;
- wrong-sign carry policy for bonds, equities, or other affected instruments;
- liquidity eligibility rule;
- minimum-capital rule;
- data-availability rule;
- completed-bar synchronization across members and curve legs;
- rounding policy;
- buffering or explicit decision to keep buffering closed;
- missing-member behavior;
- portfolio aggregation boundary;
- no post-result member addition, removal, rescue, reweighting, carry-policy change, or tuning.

## Data And Readiness Atoms Required Before Real-Data Work

Before any real data, readiness execution, diagnostic, or backtest, P06 must separately lock:

- exact source-native provider IDs or approved local mappings for every selected member;
- intake route: direct daily bars or separately justified minute-derived fallback;
- session calendar and timezone artifacts;
- roll rule artifacts;
- back-adjustment artifacts;
- completed daily bar convention;
- held and comparison contract price source for each carry member;
- expiry calendar or month-distance artifact for every curve-leg pair;
- annual risk and daily price-risk source and validation path;
- FX source and validation path;
- cost source and validation path;
- liquidity source and validation path;
- raw-response quarantine and request/provider binding rules if API or chart data is used;
- evidence-stage label and data-window budget;
- explicit operator authorization for real-data execution.

No such data or readiness execution is authorized by this draft.

## Source-Faithfulness Work Required

The existing S10 source extract packet is sufficient to explain the S10 signal block at synthetic scope. It is not enough by itself to open complete P06 implementation.

Before a complete-P06 synthetic implementation gate, a P06 source extract/source-faithfulness packet should identify the narrow book source material needed to decide:

- whether P06 is a complete book portfolio candidate or another process alias;
- the P06 universe relationship to the Jumbo portfolio and carry-eligible instruments;
- source treatment of instruments with unavailable or unreliable carry;
- source treatment of fixed-month, seasonal, and wrong-sign carry issues at portfolio scope;
- P06 instrument weights, IDM, target-risk, capital, cost, liquidity, and minimum-capital policy;
- whether P06 may reuse P05-style top-down handcrafting, the Strategy Four Jumbo framing, or requires a separate carry-specific weighting rule;
- the exact implementation boundary for a synthetic-only conformance surface.

## Future Synthetic Implementation Boundary

A later complete-P06 process-and-synthetic-code gate may be considered only after this source-shape draft passes hostile audit and a source packet or equivalent source-faithfulness record resolves enough P06 source atoms.

That later gate should stop at:

```text
complete-P06 desired position inputs
```

unless a separate gate explicitly opens aggregation or performance interpretation.

The implementation boundary should fail closed unless all selected P06 source atoms are locked and should not:

- parse real market rows;
- execute readiness;
- run diagnostics;
- run backtests;
- emit returns, PnL, Sharpe, drawdown, OOS, Lockbox, or Forward evidence;
- calculate production carry from real curve legs;
- silently drop or substitute members;
- perform trade/no-trade decisions;
- deploy, trade, or promote.

## Rejected Interpretations

### S10 Completion Equals P06

Rejected.

```text
S10_CARRY_SIGNAL_COMPLETION_IS_NOT_P06_PORTFOLIO_AUTHORIZATION
```

### P05 Trend Portfolio Locks P06 Carry Portfolio

Rejected.

```text
P05_TREND_PORTFOLIO_COMPLETION_IS_NOT_P06_CARRY_PORTFOLIO_AUTHORIZATION
```

### P06 Can Skip Source Shape

Rejected.

```text
P06_COMPLETE_SOURCE_SHAPE_REQUIRED_BEFORE_IMPLEMENTATION
```

### Process Draft Opens Real Data

Rejected.

```text
REAL_DATA_REQUIRES_SEPARATE_EXPLICIT_OPERATOR_AUTHORIZATION
```

### Process Draft Opens P07

Rejected.

```text
P07_REMAINS_SEPARATELY_GATED
```

## Fail-Closed Requirements For Later Gates

Any later implementation or data gate must fail closed if:

- lane class is not exactly `SOURCE_NATIVE_FUTURES`;
- complete P06 portfolio identity is unresolved;
- complete P06 source pages are unresolved;
- the full P06 universe or explicit carry-eligible subset is unresolved;
- any member identity, local mapping, roll rule, session, back-adjustment, or curve-leg source atom is unresolved;
- any Appendix C or broker code is treated as a local provider identifier without mapping lock;
- instrument weights, IDM, capital base, target risk, cost eligibility, liquidity eligibility, or minimum-capital policy are unresolved;
- per-instrument carry span eligibility is unresolved;
- fixed-month, seasonal, or wrong-sign carry policy is unresolved where relevant;
- production carry construction is inferred from the toy M5 surface;
- missing-member behavior is unresolved;
- completed-bar synchronization across members and curve legs is unresolved;
- S10 signal completion is treated as complete P06;
- any old `QuantLab_v3` active-pipeline artifact is used as authority;
- any member is added, dropped, rescued, reweighted, or tuned after seeing results;
- any real data, diagnostics, backtests, OOS, Lockbox, Forward, CFD adapter, deployment, trading, or promotion path is opened without separate authorization.

## Audit Requirements

Before this draft is treated as locked, a regular hostile audit should verify:

- no implementation authorization is smuggled into the draft;
- P06 is not inferred from S10 carry signal completion;
- P05 completion is not treated as P06 authorization;
- P07 remains closed;
- P06 remains a separately gated complete carry portfolio candidate;
- source atoms and data/readiness atoms are separated;
- carry-specific production atoms remain unresolved unless a narrow source packet later locks them;
- future implementation stops at desired position inputs unless separately authorized;
- no real data, diagnostics, backtests, OOS, Lockbox, Forward, CFD adapters, old `QuantLab_v3` active-pipeline use, tuning, deployment, trading, promotion, Opus/GPT execution, remote operation, or GitHub action is opened.

Regular hostile audit should be lean and subagent-based when available. Opus or GPT is not required for this draft unless the operator separately authorizes a larger source-faithfulness audit.

## Suggested Regular Hostile Audit Prompt

Under the current lean process, regular hostile audits may be delegated to a subagent without a separate operator form. If a written prompt is useful, use:

```text
Regular hostile audit, read-only. Scope: audit the process-only P06 complete
carry portfolio source-shape gate draft:
docs/process/CARVER_P06_COMPLETE_CARRY_PORTFOLIO_SOURCE_SHAPE_GATE_DRAFT_2026-05-29.md

Allowed:
Read-only file inspection and concise audit findings.

Forbidden:
No file edits, no code tests, no real data, no market-row parsing, no
NinjaTrader export, no diagnostics, no backtests, no OOS, no Lockbox, no
Forward, no CFD adapters, no old QuantLab pipeline use, no tuning, no
deployment, no trading, no promotion, no portfolio implementation, no P07
implementation, no Opus/GPT execution, no remote operations.
```

## Next Proposed Authorization

Use this only after the source-shape draft receives no blocking findings.

```text
Operator authorizes one process-only Carver P06 source extract and
source-faithfulness packet.

Scope:
Create a process-only P06 source packet that identifies the exact book source
range and narrow source material needed to decide complete-P06 carry portfolio
identity, universe, source framing, weights, IDM, target-risk/capital policy,
carry span eligibility, carry-specific production blockers, missing-member
behavior, and implementation blockers before any synthetic complete-P06
conformance code.

Allowed:
Read-only inspection of current Carver process artifacts and local Carver.pdf,
plus creation of one process source packet artifact.

Forbidden:
No code edits, no tests, no real data, no market-row parsing, no NinjaTrader
export, no diagnostics, no backtests, no OOS, no Lockbox, no Forward, no CFD
adapters, no old QuantLab pipeline use, no tuning, no deployment, no trading,
no promotion, no portfolio implementation, no P07 implementation, no Opus/GPT
execution, no remote operations.
```

## Non-Authorization

This draft authorizes no code edits, no tests, no real-data execution, no market-row parsing, no NinjaTrader export, no diagnostics, no backtests, no returns, no PnL, no Sharpe, no drawdown, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old-adapter import, no old workspace pipeline use, no tuning, no deployment, no trading, no promotion, no portfolio implementation, no P06/P07 implementation, no Opus/GPT execution, no remote push, and no GitHub action.
