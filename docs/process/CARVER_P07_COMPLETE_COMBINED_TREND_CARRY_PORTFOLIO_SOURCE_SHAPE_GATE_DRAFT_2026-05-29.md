# Carver P07 Complete Combined Trend/Carry Portfolio Source-Shape Gate Draft

Date: 2026-05-29

Status:

```text
PROCESS_ONLY_CARVER_P07_COMPLETE_COMBINED_TREND_CARRY_PORTFOLIO_SOURCE_SHAPE_GATE_DRAFT_NOT_DATA_NOT_IMPLEMENTATION
```

## Purpose

Define the future complete P07 combined trend/carry portfolio conformance boundary before any implementation.

This draft distinguishes P07 portfolio work from the already-completed S11 combined carry/trend signal block, identifies unresolved P07 source atoms and data/readiness atoms, and defines audit requirements before any later implementation gate.

This draft does not authorize code edits, tests, real data, market-row parsing, NinjaTrader export, diagnostics, backtests, portfolio implementation, Opus/GPT execution, remote operations, deployment, trading, or promotion.

## Current State

Completed upstream signal machinery:

```text
S09 trend forecast block
S10 carry construction
S10 carry forecast block
S11 combined carry/trend forecast block
```

Completed adjacent portfolio machinery:

```text
P05 complete trend portfolio synthetic conformance
P06 complete carry portfolio synthetic conformance
```

Recent sequencing decision:

```text
docs/process/CARVER_POST_P06_COMPLETE_CARRY_PORTFOLIO_NEXT_STEP_DECISION_2026-05-29.md
```

That decision selected:

```text
P07_COMPLETE_COMBINED_TREND_CARRY_PORTFOLIO_SOURCE_SHAPE_GATE_DRAFT
```

## P07 Boundary

P07 is not S11.

S11 completion proves a synthetic combined signal path:

```text
locked S09 trend forecast-block outputs
locked S10 carry forecast-block outputs
-> explicit style grouping
-> 60/40 style mix
-> top-down forecast weights
-> eligible rule set
-> S11 FDM
-> final capped S11 combined carry/trend forecast output
```

P07, if later implemented, is a complete combined trend/carry portfolio candidate that must add portfolio-specific source shape:

```text
locked combined trend/carry signal dependency
-> complete P07 portfolio member universe
-> P07 weights / IDM / target-risk / capital context
-> P07 member eligibility and readiness policy
-> future desired position inputs only
```

No P07 portfolio fact may be inferred merely from S11 signal completion.

## Candidate Classification

P07 classification for this draft:

```text
SOURCE_NATIVE_FUTURES
COMPLETE_COMBINED_TREND_CARRY_PORTFOLIO_CANDIDATE
PROCESS_ONLY_SOURCE_SHAPE_NOT_IMPLEMENTATION
```

No `CFD_DIRECT` or `CFD_ADAPTER` lane is opened. Any future CFD adapter work requires a separate explicit adapter gate after source-native P07 behavior exists.

## Upstream Signal Dependency

Future P07 implementation, if separately authorized, may depend on locked synthetic combined trend/carry signal outputs only after source-shape work decides the source-faithful dependency form.

The unresolved dependency question is:

```text
Does P07 consume locked S11 combined forecasts directly,
or does P07 combine P05 and P06 portfolio-level outputs through a separate
source rule?
```

Until a source packet or equivalent source-faithfulness record resolves that question, the only safe P07 statement is:

```text
P07_REQUIRES_A_SOURCE_SHAPED_COMBINED_TREND_CARRY_PORTFOLIO_DEPENDENCY
```

This draft does not authorize real data, diagnostics, backtests, returns, PnL, Sharpe, drawdown, portfolio aggregation, execution, or performance interpretation.

## P07 Source Atoms Required Before Implementation

Before any complete-P07 implementation gate, the following atoms must be source-locked or explicitly blocked:

- complete P07 portfolio identity and source pages;
- source framing: standalone candidate, source-native portfolio sleeve, complete book portfolio, or process alias;
- relationship between P07 and Strategy Eleven combined carry/trend;
- relationship between P07 and the already-completed P05 and P06 portfolio surfaces;
- whether P07 consumes S11 combined forecasts directly or combines P05/P06 portfolio-level outputs through another source rule;
- complete P07 instrument universe;
- whether P07 uses the Jumbo universe, a combined trend/carry eligible subset, or another source-defined universe;
- source-native contract identity for every P07 member;
- local provider mapping requirements and no-substitution policy for every member;
- asset class, group, and instrument taxonomy if handcrafted weights apply;
- instrument weights or deterministic weighting rule;
- IDM source, exact value, approximation table, or calculation policy;
- IDM applicability check for the final P07 breadth;
- portfolio capital-base policy;
- portfolio target-risk policy;
- trend component eligibility per member;
- carry component eligibility per member;
- combined trend/carry eligibility policy for members where one component is unavailable;
- EWMAC speed eligibility rule if P07 inherits Strategy Nine trend variation eligibility;
- carry span eligibility rule if P07 inherits Strategy Ten carry variation eligibility;
- style mix, forecast weights, FDM, and cap policy if P07 consumes combined forecasts directly;
- portfolio-level trend/carry combination rule if P07 combines P05 and P06 outputs;
- forecast-to-position convention;
- source treatment of members with no eligible trend rule, no eligible carry rule, or no combined rule;
- liquidity eligibility rule;
- minimum-capital rule;
- data-availability rule;
- completed-bar synchronization across members and across trend/carry components;
- rounding policy;
- buffering or explicit decision to keep buffering closed;
- missing-member behavior;
- portfolio aggregation boundary;
- no post-result member addition, removal, rescue, reweighting, trend/carry policy change, or tuning.

## Data And Readiness Atoms Required Before Real-Data Work

Before any real data, readiness execution, diagnostic, or backtest, P07 must separately lock:

- exact source-native provider IDs or approved local mappings for every selected member;
- intake route: direct daily bars or separately justified minute-derived fallback;
- session calendar and timezone artifacts;
- roll rule artifacts;
- back-adjustment artifacts;
- completed daily bar convention;
- annual risk and daily price-risk source and validation path;
- FX source and validation path;
- cost source and validation path;
- liquidity source and validation path;
- trend forecast readiness for every selected member;
- carry forecast readiness for every selected member where carry is required;
- held and comparison contract price source for every carry member if production carry is ever opened;
- expiry calendar or month-distance artifact for every curve-leg pair if production carry is ever opened;
- raw-response quarantine and request/provider binding rules if API or chart data is used;
- evidence-stage label and data-window budget;
- explicit operator authorization for real-data execution.

No such data or readiness execution is authorized by this draft.

## Source-Faithfulness Work Required

The completed P05 and P06 source packets are useful adjacent context. They do not by themselves open P07 implementation.

Before a complete-P07 synthetic implementation gate, a P07 source extract/source-faithfulness packet should identify the narrow book source material needed to decide:

- whether P07 is a book-native portfolio, a process alias, or a complete combined portfolio candidate inferred from source structure;
- whether P07 should be anchored primarily in Strategy Eleven combined forecasts, P05/P06 portfolio outputs, or another portfolio-level source rule;
- the P07 universe relationship to the Jumbo portfolio and to the P05/P06 member sets;
- whether P07 can inherit Strategy Four portfolio construction machinery, Jumbo handcrafted weights, IDM, target risk, and capital context;
- whether P07 inherits Strategy Nine trend eligibility and Strategy Ten carry eligibility separately or uses a combined eligibility rule;
- source treatment of members with trend-only, carry-only, or no combined forecast availability;
- style mix, FDM, and cap policy at the portfolio boundary;
- missing-member, no-substitution, and fail-closed behavior;
- the exact implementation boundary for a synthetic-only conformance surface.

The likely source areas are Strategy Four portfolio construction machinery, Strategy Nine multiple trend following, Strategy Ten basic carry, Strategy Eleven combined carry/trend, and Appendix C Jumbo universe. This draft does not inspect the book and does not lock those source ranges.

## Future Synthetic Implementation Boundary

A later complete-P07 process-and-synthetic-code gate may be considered only after this source-shape draft passes lean hostile audit and a source packet or equivalent source-faithfulness record resolves enough P07 source atoms.

That later gate should stop at:

```text
complete-P07 desired position inputs
```

unless a separate gate explicitly opens aggregation or performance interpretation.

The implementation boundary should fail closed unless all selected P07 source atoms are locked and should not:

- parse real market rows;
- execute readiness;
- run diagnostics;
- run backtests;
- emit returns, PnL, Sharpe, drawdown, OOS, Lockbox, or Forward evidence;
- calculate production trend or carry from real market rows;
- silently drop or substitute members;
- perform trade/no-trade decisions;
- deploy, trade, or promote.

## Rejected Interpretations

### S11 Completion Equals P07

Rejected.

```text
S11_COMBINED_SIGNAL_COMPLETION_IS_NOT_P07_PORTFOLIO_AUTHORIZATION
```

### P05 And P06 Completion Equals P07

Rejected.

```text
P05_P06_COMPLETION_IS_NOT_P07_COMBINED_PORTFOLIO_AUTHORIZATION
```

### P07 Can Skip Source Shape

Rejected.

```text
P07_COMPLETE_SOURCE_SHAPE_REQUIRED_BEFORE_IMPLEMENTATION
```

### P07 Can Choose S11 Direct Forecasts Without Source Review

Rejected.

```text
P07_S11_DIRECT_FORECAST_DEPENDENCY_REQUIRES_SOURCE_SHAPE
```

### P07 Can Combine P05 And P06 Portfolio Outputs Without Source Review

Rejected.

```text
P07_P05_P06_PORTFOLIO_OUTPUT_DEPENDENCY_REQUIRES_SOURCE_SHAPE
```

### Process Draft Opens Real Data

Rejected.

```text
REAL_DATA_REQUIRES_SEPARATE_EXPLICIT_OPERATOR_AUTHORIZATION
```

## Fail-Closed Requirements For Later Gates

Any later implementation or data gate must fail closed if:

- lane class is not exactly `SOURCE_NATIVE_FUTURES`;
- complete P07 portfolio identity is unresolved;
- complete P07 source pages are unresolved;
- the P07 universe or explicit combined eligible subset is unresolved;
- the dependency on S11 forecasts or P05/P06 portfolio outputs is unresolved;
- any member identity, local mapping, roll rule, session, back-adjustment, or carry curve-leg source atom is unresolved;
- any Appendix C or broker code is treated as a local provider identifier without mapping lock;
- instrument weights, IDM, capital base, target risk, cost eligibility, liquidity eligibility, or minimum-capital policy are unresolved;
- trend and carry eligibility are unresolved for any selected member;
- missing-member behavior is unresolved;
- completed-bar synchronization across members and trend/carry components is unresolved;
- S11 signal completion is treated as complete P07;
- P05 and P06 completion are treated as complete P07;
- production carry construction is inferred from the toy M5/S10 surfaces;
- any old `QuantLab_v3` active-pipeline artifact is used as authority;
- any member is added, dropped, rescued, reweighted, or tuned after seeing results;
- any real data, diagnostics, backtests, OOS, Lockbox, Forward, CFD adapter, deployment, trading, or promotion path is opened without separate authorization.

## Audit Requirements

Before this draft is treated as locked, a regular hostile audit should verify:

- no implementation authorization is smuggled into the draft;
- P07 is not inferred from S11 combined signal completion;
- P07 is not inferred from P05/P06 portfolio completion;
- P07 remains a separately gated complete combined trend/carry portfolio candidate;
- source atoms and data/readiness atoms are separated;
- the S11-direct dependency and P05/P06-output dependency remain unresolved until source-shaped;
- future implementation stops at desired position inputs unless separately authorized;
- no real data, diagnostics, backtests, OOS, Lockbox, Forward, CFD adapters, old `QuantLab_v3` active-pipeline use, tuning, deployment, trading, promotion, Opus/GPT execution, remote operation, or GitHub action is opened.

Regular hostile audit should be lean and subagent-based when available. Under the current lean Carver process, regular audit-result preservation is a separate process-only record and does not require Opus/GPT. Opus or GPT is reserved for larger source-faithfulness disputes, exact book-table disputes, production-facing source-lock claims, or operator-authorized external audit packets.

## Suggested Regular Hostile Audit Prompt

Under the current lean process, regular hostile audits may be delegated to a subagent without a separate operator form. If a written prompt is useful, use:

```text
Regular hostile audit, read-only. Scope: audit the process-only P07 complete
combined trend/carry portfolio source-shape gate draft:
docs/process/CARVER_P07_COMPLETE_COMBINED_TREND_CARRY_PORTFOLIO_SOURCE_SHAPE_GATE_DRAFT_2026-05-29.md

Allowed:
Read-only file inspection and concise audit findings.

Forbidden:
No file edits, no code tests, no real data, no market-row parsing, no
NinjaTrader export, no diagnostics, no backtests, no OOS, no Lockbox, no
Forward, no CFD adapters, no old QuantLab pipeline use, no tuning, no
deployment, no trading, no promotion, no portfolio implementation, no
Opus/GPT execution, no remote operations.
```

## Next Proposed Authorization

Use this only after the source-shape draft receives no blocking findings.

```text
Operator authorizes one process-only Carver P07 source extract and
source-faithfulness packet.

Scope:
Create a process-only P07 source packet that identifies the exact book source
range and narrow source material needed to decide complete-P07 combined
trend/carry portfolio identity, universe, source framing, relationship to S11,
relationship to P05/P06, weights, IDM, target-risk/capital policy, trend/carry
eligibility, dependency shape, missing-member behavior, and implementation
blockers before any synthetic complete-P07 conformance code.

Allowed:
Read-only inspection of current Carver process artifacts and local Carver.pdf,
plus creation of one process source packet artifact.

Forbidden:
No code edits, no tests, no real data, no market-row parsing, no NinjaTrader
export, no diagnostics, no backtests, no OOS, no Lockbox, no Forward, no CFD
adapters, no old QuantLab pipeline use, no tuning, no deployment, no trading,
no promotion, no portfolio implementation, no Opus/GPT execution, no remote
operations.
```

## Non-Authorization

This draft authorizes no code edits, no tests, no real-data execution, no market-row parsing, no NinjaTrader export, no diagnostics, no backtests, no returns, no PnL, no Sharpe, no drawdown, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old-adapter import, no old workspace pipeline use, no tuning, no deployment, no trading, no promotion, no portfolio implementation, no P07 implementation, no Opus/GPT execution, no remote push, and no GitHub action.
