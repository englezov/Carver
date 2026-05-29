# Carver Post-P06 Complete Carry Portfolio Next-Step Decision

Date: 2026-05-29

Status:

```text
PROCESS_ONLY_CARVER_POST_P06_COMPLETE_CARRY_PORTFOLIO_NEXT_STEP_DECISION_NOT_DATA_NOT_IMPLEMENTATION
```

## Purpose

Decide the next clean portfolio gate after the audited P06 complete carry portfolio synthetic conformance surface.

This is a sequencing record only. It does not authorize code edits, tests, real data, market-row parsing, NinjaTrader export, diagnostics, backtests, OOS, Lockbox, Forward, CFD adapters, old QuantLab pipeline use, tuning, deployment, trading, promotion, P07 implementation, Opus/GPT execution, remote operations, remote push, or GitHub action.

## Current State

Completed portfolio-shape chapters:

```text
P05 complete trend portfolio synthetic conformance
P06 complete carry portfolio synthetic conformance
```

Completed signal dependencies:

```text
S09 trend forecast block
S10 carry construction
S10 carry forecast block
S11 combined carry/trend forecast block
```

P06 implementation artifacts:

```text
src/carver/spine/p06.py
tests/test_p06_complete_carry_portfolio_synthetic.py
docs/process/CARVER_P06_COMPLETE_CARRY_PORTFOLIO_CONFORMANCE_2026-05-29.md
```

P06 regular hostile audit result:

```text
NO BLOCKING FINDINGS
AUDIT_DISPOSITION: PASS_PROCESS_AND_SYNTHETIC_CODE_SCOPE
```

The P06 surface is complete only at process-and-synthetic-code scope. It:

- treats P06 as the Carver process alias for Strategy Ten basic carry over the Jumbo futures portfolio source frame;
- consumes locked synthetic S10 carry forecast outputs;
- applies source-shaped handcrafted weights, eligible carry span sets, equal Strategy Ten forecast weights, Strategy Ten carry FDM rows, caps, and M1 position-sizing input arithmetic;
- emits complete-P06 desired position inputs only;
- keeps production carry construction, Appendix C transcription, local provider mappings, real data, diagnostics, backtests, portfolio execution, deployment, trading, and promotion closed.

## Decision

The next clean portfolio chapter should open P07 combined trend/carry portfolio source-shape work.

Selected next gate:

```text
P07_COMPLETE_COMBINED_TREND_CARRY_PORTFOLIO_SOURCE_SHAPE_GATE_DRAFT
```

This next gate should be process-only. It should define the future complete P07 combined trend/carry portfolio conformance boundary before any implementation, distinguish P07 portfolio work from the already-completed S11 combined carry/trend signal block, identify unresolved P07 portfolio source atoms and data/readiness atoms, and define audit requirements before any later synthetic implementation gate.

## Why P07 Next

P07 is the clean continuation because:

- P05 complete trend portfolio synthetic conformance is now completed and audited;
- P06 complete carry portfolio synthetic conformance is now completed and audited;
- S11 combined carry/trend signal conformance is already completed upstream;
- P07 is the combined-portfolio counterpart to P05 and P06 and should receive the same disciplined source-shape treatment before implementation;
- opening P07 now keeps the Part One portfolio graph moving in order: trend portfolio, carry portfolio, combined trend/carry portfolio;
- P07 should not be inferred merely from S11 signal-block completion, because P07 must lock portfolio identity, universe, weights, IDM, target-risk/capital policy, member readiness, missing-member behavior, and portfolio output boundaries.

## Selected Gate Scope

The P07 source-shape gate draft should:

- define P07 portfolio identity and source-page requirements;
- determine whether P07 is a complete book portfolio candidate, a source-native portfolio sleeve, or another source-framed object;
- distinguish P07 from S11 combined carry/trend signal completion;
- identify the complete P07 instrument universe if source-supported, or record it as unresolved;
- identify whether P07 uses the same Jumbo universe as P05 and P06, a combined eligible subset, or another source-defined universe;
- identify the relationship between P07, P05, P06, and S11;
- identify whether P07 consumes locked S11 combined forecasts directly or combines P05/P06 portfolio-level outputs through another source rule;
- identify source-native contract identity requirements for every future member;
- identify local provider mapping requirements and no-substitution policy;
- identify instrument weights or deterministic weighting rule;
- identify IDM, target-risk, capital-base, cost, liquidity, and minimum-capital atoms;
- identify trend/carry synchronization requirements and eligible rule dependencies;
- identify completed-bar synchronization across members and forecast components;
- define missing-member and fail-closed behavior;
- define whether a narrow P07 source extract/source-faithfulness packet is needed before implementation;
- define the later synthetic implementation boundary if safe;
- define regular hostile audit requirements.

The selected gate should not:

- implement P07;
- run tests;
- inspect real market rows;
- parse market data;
- execute readiness;
- run diagnostics or backtests;
- open CFD adapter work;
- use old `QuantLab_v3` active pipelines;
- deploy, trade, or promote.

## Rejected Next Gates

### Open P07 Implementation Immediately

Rejected.

Reason:

```text
P07_PORTFOLIO_SOURCE_SHAPE_NOT_LOCKED
```

S11 combined carry/trend signal conformance is complete, but P07 portfolio identity, universe, weights, IDM, target-risk/capital policy, member eligibility, synchronization, and missing-member behavior remain portfolio-level atoms. They must be source-shaped or explicitly blocked before implementation.

### Treat S11 Completion As P07

Rejected.

Reason:

```text
S11_COMBINED_SIGNAL_COMPLETION_IS_NOT_P07_PORTFOLIO_AUTHORIZATION
```

S11 emits a final capped combined forecast output only. It does not emit portfolio desired position inputs, portfolio readiness, aggregation, returns, PnL, diagnostics, backtests, deployment, trading, or promotion evidence.

### Treat P05 And P06 Completion As P07

Rejected.

Reason:

```text
P05_P06_COMPLETION_IS_NOT_P07_COMBINED_PORTFOLIO_AUTHORIZATION
```

P05 and P06 prove trend and carry portfolio synthetic shapes separately. They do not decide P07 combined-portfolio identity, whether P07 uses S11 direct forecasts or another portfolio-level combination rule, or the missing-member behavior for combined trend/carry members.

### Open Real Data Or Readiness Execution

Rejected.

Reason:

```text
REAL_DATA_REQUIRES_SEPARATE_EXPLICIT_OPERATOR_AUTHORIZATION
```

No NinjaTrader export, market-row parsing, provider probe, readiness run, diagnostic, backtest, OOS, Lockbox, Forward, CFD adapter, deployment, trading, or promotion is authorized by this decision.

### Use Old QuantLab For P07

Rejected.

Reason:

```text
OLD_QUANTLAB_ACTIVE_PIPELINES_REMAIN_QUARANTINED
```

The old workspace may not be used for active P07 pipelines, adapters, data-prep scripts, or source authority.

## Audit Requirements

The future P07 source-shape gate draft should receive a regular hostile audit, preferably by subagent, before it is treated as locked.

Audit focus:

- no P07 implementation authorization is smuggled into the draft;
- P07 is not inferred from S11 signal completion alone;
- P05 and P06 completion are not treated as P07 authorization;
- source atoms and data/readiness atoms remain separated;
- combined trend/carry portfolio dependencies remain unresolved unless narrowly source-cited;
- no production source locks are claimed without a source packet or larger operator-authorized audit;
- no real data, diagnostics, backtests, OOS, Lockbox, Forward, CFD adapter, old `QuantLab_v3` active-pipeline use, tuning, deployment, trading, promotion, Opus/GPT execution, remote operation, remote push, or GitHub action is opened.

Regular hostile audit results should be preserved automatically as separate process-only audit-result records under the current lean Carver process. Opus/GPT is not required for the next process-only P07 source-shape draft unless the operator separately authorizes a larger source-faithfulness review.

## Next Proposed Authorization

```text
Operator authorizes one process-only Carver P07 complete combined trend/carry
portfolio source-shape gate draft.

Scope:
Create a process-only P07 gate draft that defines the future complete P07
combined trend/carry portfolio conformance boundary, distinguishes P07
portfolio work from the already-completed S11 combined carry/trend signal
block, identifies unresolved P07 source atoms and data/readiness atoms, and
defines audit requirements before implementation.

Allowed:
Read-only inspection of current Carver process artifacts and creation of one
process gate draft artifact.

Forbidden:
No code edits, no tests, no real data, no market-row parsing, no NinjaTrader
export, no diagnostics, no backtests, no OOS, no Lockbox, no Forward, no CFD
adapters, no old QuantLab pipeline use, no tuning, no deployment, no trading,
no promotion, no portfolio implementation, no Opus/GPT execution, no remote
operations.
```

## Non-Authorization

This decision authorizes no code edits, no tests, no real-data execution, no market-row parsing, no NinjaTrader export, no diagnostics, no backtests, no returns, no PnL, no Sharpe, no drawdown, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old-adapter import, no old workspace pipeline use, no tuning, no deployment, no trading, no promotion, no portfolio implementation, no P07 implementation, no Opus/GPT execution, no remote push, and no GitHub action.
