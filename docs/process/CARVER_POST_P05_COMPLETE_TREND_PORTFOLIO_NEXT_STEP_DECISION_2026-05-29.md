# Carver Post-P05 Complete Trend Portfolio Next-Step Decision

Date: 2026-05-29

Status:

```text
PROCESS_ONLY_CARVER_POST_P05_COMPLETE_TREND_PORTFOLIO_NEXT_STEP_DECISION_NOT_DATA_NOT_IMPLEMENTATION
```

## Purpose

Decide the next clean portfolio gate after the audited P05 complete trend portfolio synthetic conformance surface.

This is a sequencing record only. It does not authorize code edits, tests, real data, market-row parsing, NinjaTrader export, diagnostics, backtests, OOS, Lockbox, Forward, CFD adapters, old QuantLab pipeline use, tuning, deployment, trading, promotion, P06/P07 implementation, Opus/GPT execution, remote operations, remote push, or GitHub action.

## Current State

Completed P05 implementation-shape chapter:

```text
PROCESS_AND_SYNTHETIC_CODE_CARVER_P05_COMPLETE_TREND_PORTFOLIO_CONFORMANCE_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

Implemented artifacts:

```text
src/carver/spine/p05.py
tests/test_p05_complete_trend_portfolio_synthetic.py
docs/process/CARVER_P05_COMPLETE_TREND_PORTFOLIO_CONFORMANCE_2026-05-29.md
```

Regular hostile audit result preserved:

```text
NO BLOCKING FINDINGS
AUDIT_DISPOSITION: PASS_PROCESS_AND_SYNTHETIC_CODE_SCOPE
```

The P05 surface is complete only at process-and-synthetic-code scope. It:

- treats P05 as the Carver process alias for Strategy Nine multiple trend following over the Jumbo futures portfolio source frame;
- consumes locked synthetic S09 trend forecast outputs;
- applies source-shaped handcrafted weights, eligible EWMAC speed sets, equal Strategy Nine forecast weights, Strategy Nine FDM rows, caps, and M1 position-sizing input arithmetic;
- emits complete-P05 desired position inputs only;
- keeps Appendix C production transcription, local provider mappings, real data, diagnostics, backtests, portfolio execution, deployment, trading, and promotion closed.

## Decision

The next clean portfolio chapter should open P06 carry portfolio source-shape work.

Selected next gate:

```text
P06_COMPLETE_CARRY_PORTFOLIO_SOURCE_SHAPE_GATE_DRAFT
```

This next gate should be process-only. It should define the future complete P06 carry portfolio conformance boundary before any implementation, distinguish P06 from the already-completed S10 carry signal block, identify unresolved P06 portfolio source atoms and data/readiness atoms, and define audit requirements before any later synthetic implementation gate.

## Why P06 Next

P06 is the clean continuation because:

- P05 trend portfolio synthetic conformance is now completed and audited;
- S10 carry construction and S10 carry forecast-block synthetic conformance are already completed upstream;
- P06 is the carry-portfolio counterpart to P05 and should receive the same disciplined source-shape treatment before implementation;
- opening P06 now keeps the Part One portfolio graph moving in order: trend portfolio, carry portfolio, then combined trend/carry portfolio;
- P07 should wait until P06 has at least a source-shape record, because P07 depends on combined trend/carry portfolio interpretation and must not be inferred merely from S11 signal-block completion.

## Selected Gate Scope

The P06 source-shape gate draft should:

- define P06 portfolio identity and source-page requirements;
- determine whether P06 is a complete book portfolio candidate, a source-native portfolio sleeve, or another source-framed object;
- distinguish P06 from S10 carry signal completion;
- identify the complete P06 instrument universe if source-supported, or record it as unresolved;
- identify whether P06 uses the same Jumbo universe as P05, a carry-eligible subset, or another source-defined universe;
- identify source-native contract identity requirements for every future member;
- identify local provider mapping requirements and no-substitution policy;
- identify instrument weights or deterministic weighting rule;
- identify IDM, target-risk, capital-base, cost, liquidity, and minimum-capital atoms;
- identify carry-specific atoms: curve-leg availability, held/comparison contract roles, expiry annualization, fixed-month policies, seasonal and wrong-sign carry handling, and per-instrument carry eligibility;
- identify completed-bar synchronization across members and curve legs;
- define missing-member and fail-closed behavior;
- define whether a narrow P06 source extract/source-faithfulness packet is needed before implementation;
- define the later synthetic implementation boundary if safe;
- define regular hostile audit requirements.

The selected gate should not:

- implement P06;
- run tests;
- inspect real market rows;
- parse market data;
- execute readiness;
- run diagnostics or backtests;
- open P07 implementation;
- open CFD adapter work;
- use old `QuantLab_v3` active pipelines;
- deploy, trade, or promote.

## Rejected Next Gates

### Open P06 Implementation Immediately

Rejected.

Reason:

```text
P06_PORTFOLIO_SOURCE_SHAPE_NOT_LOCKED
```

S10 carry signal conformance is complete, but P06 portfolio identity, universe, weights, IDM, target-risk/capital policy, carry-specific member eligibility, and missing-member behavior remain portfolio-level atoms. They must be source-shaped or explicitly blocked before implementation.

### Open P07 Before P06

Rejected for near-term sequencing.

Reason:

```text
P07_DEPENDS_ON_P05_AND_P06_PORTFOLIO_SHAPES
```

S11 combined carry/trend signal conformance is complete, but P07 is a portfolio candidate. It should not be opened before P06 carry portfolio shape is understood.

### Open Real Data Or Readiness Execution

Rejected.

Reason:

```text
REAL_DATA_REQUIRES_SEPARATE_EXPLICIT_OPERATOR_AUTHORIZATION
```

No NinjaTrader export, market-row parsing, provider probe, readiness run, diagnostic, backtest, OOS, Lockbox, Forward, CFD adapter, deployment, trading, or promotion is authorized by this decision.

### Treat P05 Completion As Portfolio Evidence

Rejected.

Reason:

```text
P05_SYNTHETIC_CONFORMANCE_IS_NOT_DATA_EVIDENCE
```

P05 completion proves process-and-synthetic-code shape only. It is not returns, PnL, Sharpe, drawdown, OOS, Lockbox, Forward, production readiness, deployment, trading, or promotion evidence.

### Use Old QuantLab For P06

Rejected.

Reason:

```text
OLD_QUANTLAB_ACTIVE_PIPELINES_REMAIN_QUARANTINED
```

The old workspace may not be used for active P06 pipelines, adapters, data-prep scripts, or source authority.

## Audit Requirements

The future P06 source-shape gate draft should receive a regular hostile audit, preferably by subagent, before it is treated as locked.

Audit focus:

- no P06 implementation authorization is smuggled into the draft;
- P06 is not inferred from S10 signal completion alone;
- P07 remains closed;
- source atoms and data/readiness atoms remain separated;
- carry-specific policies remain unresolved unless narrowly source-cited;
- no production source locks are claimed without a source packet or larger operator-authorized audit;
- no real data, diagnostics, backtests, OOS, Lockbox, Forward, CFD adapter, old `QuantLab_v3` active-pipeline use, tuning, deployment, trading, promotion, Opus/GPT execution, remote operation, remote push, or GitHub action is opened.

Opus/GPT is not required for the next process-only P06 source-shape draft unless the operator separately authorizes a larger source-faithfulness review.

## Next Proposed Authorization

```text
Operator authorizes one process-only Carver P06 complete carry portfolio
source-shape gate draft.

Scope:
Create a process-only P06 gate draft that defines the future complete P06 carry
portfolio conformance boundary, distinguishes P06 portfolio work from the
already-completed S10 carry signal block, identifies unresolved P06 source atoms
and data/readiness atoms, and defines audit requirements before implementation.

Allowed:
Read-only inspection of current Carver process artifacts and creation of one
process gate draft artifact.

Forbidden:
No code edits, no tests, no real data, no market-row parsing, no NinjaTrader
export, no diagnostics, no backtests, no OOS, no Lockbox, no Forward, no CFD
adapters, no old QuantLab pipeline use, no tuning, no deployment, no trading,
no promotion, no portfolio implementation, no P07 implementation, no Opus/GPT
execution, no remote operations.
```

## Non-Authorization

This decision authorizes no code edits, no tests, no real-data execution, no market-row parsing, no NinjaTrader export, no diagnostics, no backtests, no returns, no PnL, no Sharpe, no drawdown, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old-adapter import, no old workspace pipeline use, no tuning, no deployment, no trading, no promotion, no portfolio implementation, no P06/P07 implementation, no Opus/GPT execution, no remote push, and no GitHub action.
