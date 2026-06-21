# Carver P05 Implementation-Readiness Decision

Date: 2026-05-29

Status:

```text
PROCESS_ONLY_CARVER_P05_IMPLEMENTATION_READINESS_DECISION_NOT_DATA_NOT_IMPLEMENTATION
```

## Purpose

Decide whether the completed P05 source-shape draft has locked enough information to open a synthetic complete-P05 conformance implementation surface.

This decision is process-only. It authorizes no code edits, tests, real data, diagnostics, backtests, portfolio implementation, Opus/GPT execution, remote operations, deployment, trading, or promotion.

## Current State

Completed P05 source-shape draft:

```text
docs/process/CARVER_P05_COMPLETE_TREND_PORTFOLIO_SOURCE_SHAPE_GATE_DRAFT_2026-05-29.md
```

Regular hostile audit result:

```text
NO BLOCKING FINDINGS
AUDIT_DISPOSITION: PASS_PROCESS_ONLY_DRAFT_SCOPE
```

The draft correctly establishes:

- complete P05 is not the existing `MES / ZN / ZF` phase-1 seed;
- P05 remains a separately gated complete trend portfolio candidate;
- P06 and P07 remain closed;
- source atoms and data/readiness atoms are separated;
- any future synthetic implementation should stop at complete-P05 desired position inputs unless separately authorized.

## Decision

Enough is not yet locked to open a synthetic complete-P05 implementation surface.

The next clean gate should be:

```text
P05_SOURCE_EXTRACT_AND_SOURCE_FAITHFULNESS_PACKET
```

This next gate should remain process-only unless separately expanded. It should extract the narrow source material needed to lock or explicitly block the complete-P05 source atoms before any process-and-synthetic-code complete-P05 implementation.

## Why Implementation Is Not Ready

The source-shape draft deliberately leaves these implementation-critical atoms unresolved:

- complete P05 portfolio identity and source pages;
- complete P05 instrument universe;
- whether `MES / ZN / ZF` are complete members, seed members, or only phase-1 scaffold members;
- source-native contract identity for every P05 member;
- local provider mapping requirements and no-substitution policy;
- instrument weights or deterministic weighting rule;
- IDM source, exact value, or calculation policy;
- target-risk and capital-base policy;
- per-instrument eligible EWMAC speed set;
- speed/cost eligibility rule;
- liquidity, minimum-capital, and data-availability rules;
- forecast-to-position convention;
- rounding and buffering policy;
- missing-member behavior;
- completed-bar synchronization across all members;
- portfolio aggregation boundary.

Opening synthetic complete-P05 implementation now would either invent these atoms or silently downgrade complete P05 into the existing phase-1 scaffold. Both are rejected.

## Selected Next Gate Scope

The selected source-extract/source-faithfulness packet should:

- identify the exact book section and page range governing P05;
- extract or summarize only narrow, necessary source material;
- identify complete-P05 portfolio identity and source framing;
- determine whether P05 is a standalone candidate, source-native portfolio sleeve, or complete book portfolio;
- identify the complete P05 universe if source-supported, or record the universe as unresolved;
- identify any source-stated weights, IDM, target risk, capital base, and eligibility rules;
- identify any source-stated EWMAC speed/cost eligibility rules for P05;
- identify whether complete-P05 implementation can be synthetic-only without production source locks;
- list any atoms that must remain blocked before implementation;
- prepare a regular hostile audit or, if source ambiguity is large, an operator-authorized Opus/GPT source-faithfulness audit.

## Rejected Next Gates

### Open Synthetic Complete-P05 Implementation Now

Rejected.

Reason:

```text
P05_COMPLETE_SOURCE_ATOMS_NOT_LOCKED
```

### Treat MES/ZN/ZF Phase-1 As Complete P05

Rejected.

Reason:

```text
P05_PHASE1_SEED_IS_NOT_COMPLETE_P05
```

### Open Real Data Or Readiness Execution

Rejected.

Reason:

```text
REAL_DATA_REQUIRES_SEPARATE_EXPLICIT_OPERATOR_AUTHORIZATION
```

### Open P06 Or P07 Implementation

Rejected.

Reason:

```text
P06_P07_REMAIN_SEPARATELY_GATED
```

## Audit Requirements

Regular hostile audits remain lean and may be delegated to a subagent when useful without a separate operator authorization.

Opus/GPT execution remains separately operator-authorized and should be reserved for:

- large source-faithfulness disputes;
- exact book-table or page disputes;
- production-facing source-lock claims;
- audit packets intended for external model review.

Before any complete-P05 synthetic implementation gate is opened, the readiness record must show either:

- a narrow P05 source extract and regular hostile audit with no blocking findings; or
- an operator-authorized Opus/GPT source-faithfulness audit with no blocking findings if the source atoms remain ambiguous.

## Closed Boundaries

This decision keeps closed:

- code edits;
- tests;
- real data;
- market-row parsing;
- NinjaTrader export;
- diagnostics;
- backtests;
- returns;
- PnL;
- Sharpe;
- drawdown;
- OOS;
- Lockbox;
- Forward;
- CFD adapters;
- old `QuantLab_v3` active-pipeline use;
- tuning;
- deployment;
- trading;
- promotion;
- portfolio implementation;
- P05/P06/P07 implementation;
- Opus/GPT execution;
- remote operations.

## Next Proposed Authorization

```text
Operator authorizes one process-only Carver P05 source extract and
source-faithfulness packet.

Scope:
Create a process-only P05 source packet that identifies the exact book source
range and narrow source material needed to decide complete-P05 portfolio
identity, universe, source framing, weights, IDM, target-risk/capital policy,
eligible EWMAC speed/cost rules, missing-member behavior, and implementation
blockers before any synthetic complete-P05 conformance code.

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

This decision authorizes no code edits, no tests, no real-data execution, no market-row parsing, no NinjaTrader export, no diagnostics, no backtests, no returns, no PnL, no Sharpe, no drawdown, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old-adapter import, no old workspace pipeline use, no tuning, no deployment, no trading, no promotion, no portfolio implementation, no P05/P06/P07 implementation, no Opus/GPT execution, no remote push, and no GitHub action.
