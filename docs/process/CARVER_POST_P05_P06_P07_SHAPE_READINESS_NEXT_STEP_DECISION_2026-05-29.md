# Carver Post-P05/P06/P07 Shape-Readiness Next-Step Decision

Date: 2026-05-29

Status:

```text
PROCESS_ONLY_CARVER_POST_P05_P06_P07_SHAPE_READINESS_NEXT_STEP_DECISION_NOT_DATA_NOT_IMPLEMENTATION
```

## Purpose

Decide the next clean portfolio gate after the audited P05/P06/P07 portfolio shape and readiness draft.

This is a sequencing record only. It does not authorize P05, P06, or P07 implementation, code edits, tests, real data, diagnostics, backtests, Opus execution, remote operations, deployment, trading, or promotion.

## Current State

The P05/P06/P07 shape and readiness draft has passed regular hostile audit:

```text
NO BLOCKING FINDINGS
AUDIT_DISPOSITION: PASS_PROCESS_ONLY_DRAFT_SCOPE
```

The audited draft records:

- P05, P06, and P07 are separate portfolio candidates;
- P05 depends on the S09 trend forecast block;
- P06 depends on the S10 carry forecast block;
- P07 depends on the S11 combined carry/trend forecast block;
- P05 phase-1 construction for `MES / ZN / ZF` is a seed scaffold only;
- source atoms and data/readiness atoms remain separated;
- no real data, diagnostics, backtests, CFD adapters, portfolio implementation, deployment, trading, or promotion is open.

## Decision

The next clean portfolio chapter should open P05 first, but not by jumping directly into implementation.

The next gate should be:

```text
P05_COMPLETE_TREND_PORTFOLIO_SOURCE_SHAPE_GATE_DRAFT
```

This gate should be process-only. It should define the future implementation boundary for complete P05 trend portfolio conformance and decide exactly what must be source-locked before a later P05 implementation gate.

## Why P05 First

P05 is the nearest clean continuation because:

- S09 trend forecast conformance already exists;
- P05 phase-1 construction conformance already proves a small construction scaffold for `MES / ZN / ZF`;
- the audited readiness draft explicitly rejects treating phase-1 as complete P05, which means the next useful work is to define complete P05 rather than drift into P06 or P07;
- P06 still requires complete carry-portfolio source shape and carry eligibility work;
- P07 should wait until P05 and P06 portfolio shapes are better understood, because it depends on combined trend/carry portfolio interpretation rather than only a completed S11 signal block.

The intended implementation order is therefore:

```text
P05 first
P06 second
P07 third
```

This is a sequencing preference, not implementation authorization.

## Selected Next Gate Scope

The selected P05 process gate draft should:

- define complete P05 portfolio identity and source-page requirements;
- distinguish complete P05 from the existing `MES / ZN / ZF` phase-1 seed;
- identify the full P05 instrument universe or record it as unresolved;
- identify P05 source-native contract identity requirements;
- identify local provider mapping requirements;
- identify P05 instrument weights or deterministic weighting rule;
- identify IDM, target-risk, capital-base, cost, liquidity, and minimum-capital atoms;
- identify per-instrument eligible EWMAC speed requirements;
- identify roll, back-adjustment, session, and completed-bar synchronization atoms;
- define missing-member and fail-closed behavior;
- define the later synthetic implementation boundary, if safe;
- define the hostile audit requirement before any implementation.

The selected gate should not:

- implement P05;
- run tests;
- inspect real market rows;
- execute readiness;
- run diagnostics or backtests;
- open P06 or P07 implementation;
- open CFD adapter work;
- use old `QuantLab_v3` active pipelines;
- deploy, trade, or promote.

## Rejected Next Gates

### Open P05 Implementation Immediately

Rejected.

Reason:

```text
P05_COMPLETE_SOURCE_SHAPE_NOT_LOCKED
```

The phase-1 seed is useful but incomplete. Complete P05 still needs a portfolio-specific source-shape gate before implementation.

### Open P06 First

Rejected for near-term sequencing.

Reason:

```text
P06_SHOULD_FOLLOW_P05_PORTFOLIO_SHAPE_DISCIPLINE
```

S10 carry conformance is complete at synthetic scope, but P06 has no portfolio-specific process draft yet. P05 is closer because its phase-1 scaffold already exercises portfolio construction mechanics.

### Open P07 First

Rejected.

Reason:

```text
P07_DEPENDS_ON_COMBINED_PORTFOLIO_INTERPRETATION_AFTER_P05_AND_P06
```

S11 completion is a signal-block completion, not a complete P07 portfolio authorization.

### Open Real Data Or Evidence Work

Rejected.

Reason:

```text
REAL_DATA_AND_EVIDENCE_WORK_REQUIRES_SEPARATE_EXPLICIT_AUTHORIZATION
```

No NinjaTrader export, market-row parsing, diagnostics, backtests, OOS, Lockbox, Forward, CFD adapters, deployment, trading, or promotion is authorized by this decision.

## Audit Requirements

The future P05 complete trend portfolio source-shape gate draft should receive a regular hostile audit, preferably by subagent, before it is treated as locked.

Audit focus:

- P05 phase-1 is not inflated into complete P05;
- complete P05 source atoms are clearly listed or explicitly blocked;
- P06 and P07 remain closed;
- source atoms and data/readiness atoms remain separated;
- no implementation authorization is smuggled into the process draft;
- no real data, diagnostics, backtests, OOS, Lockbox, Forward, CFD adapter, deployment, trading, or promotion is opened;
- old `QuantLab_v3` remains quarantined from active pipelines.

Opus or GPT is not required for this next process-only decision or a normal draft audit. Opus/GPT should be reserved for larger operator-authorized source-faithfulness audits, exact book-table disputes, or production-facing source-lock claims.

## Next Proposed Authorization

```text
Operator authorizes one process-only Carver P05 complete trend portfolio
source-shape gate draft.

Scope:
Create a process-only P05 gate draft that defines the future complete P05 trend
portfolio conformance boundary, distinguishes complete P05 from the existing
MES/ZN/ZF phase-1 seed, identifies unresolved P05 source atoms and
data/readiness atoms, and defines audit requirements before implementation.

Allowed:
Read-only inspection of current Carver process artifacts and creation of one
process gate draft artifact.

Forbidden:
No code edits, no tests, no real data, no market-row parsing, no NinjaTrader
export, no diagnostics, no backtests, no OOS, no Lockbox, no Forward, no CFD
adapters, no old QuantLab pipeline use, no tuning, no deployment, no trading,
no promotion, no portfolio implementation, no P06/P07 implementation, no Opus
execution, no remote operations.
```

## Non-Authorization

This decision authorizes no code edits, no tests, no real data, no market-row parsing, no NinjaTrader export, no diagnostics, no backtests, no returns, no PnL, no Sharpe, no drawdown, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old-adapter import, no old workspace pipeline use, no tuning, no deployment, no trading, no promotion, no portfolio implementation, no P05/P06/P07 implementation, no S11 implementation, no Opus execution, no remote push, and no GitHub action.
