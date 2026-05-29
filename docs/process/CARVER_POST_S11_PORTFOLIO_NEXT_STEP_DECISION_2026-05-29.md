# Carver Post-S11 Portfolio Next-Step Decision

Date: 2026-05-29

Status:

```text
PROCESS_ONLY_CARVER_POST_S11_PORTFOLIO_NEXT_STEP_DECISION_NOT_DATA_NOT_IMPLEMENTATION
```

## Purpose

Decide the next clean gate after S11 combined carry/trend completion.

This decision exists only to sequence the Part One portfolio graph after the synthetic signal spine has reached S11. It does not authorize portfolio implementation, code edits, tests, data access, diagnostics, backtests, Opus execution, remote operations, trading, or promotion.

## Current State

Completed process-and-synthetic signal spine:

```text
S09 trend forecast block
S10 carry construction
S10 carry forecast block
S11 combined carry/trend forecast block
```

S11 implementation hostile audit result:

```text
NO BLOCKING FINDINGS
AUDIT_DISPOSITION: PASS_PROCESS_AND_SYNTHETIC_CODE_SCOPE
```

Existing portfolio state:

- M3 portfolio construction process spec exists and has a subagent hostile audit result.
- P01/P02 process records exist as early portfolio definitions.
- P05 phase-1 construction conformance exists for `MES`, `ZN`, and `ZF`.
- P05 phase-1 is a seed construction scaffold only, not complete P05 and not the Jumbo portfolio.
- P06 and P07 remain unopened as complete portfolio candidates.

## Decision

The next clean gate should be:

```text
P05_P06_P07_PORTFOLIO_SHAPE_AND_READINESS_GATE_DRAFT
```

The gate should be process-only. It should map the next Part One portfolio chapter from the completed S09/S10/S11 synthetic forecast spine into separately gated portfolio candidates:

```text
P05 trend portfolio shape/readiness
P06 carry portfolio shape/readiness
P07 combined trend/carry portfolio shape/readiness
```

The draft should not implement any portfolio. It should decide the required source atoms, audit requirements, and fail-closed boundaries before any later P05, P06, or P07 code gate.

## Why This Gate

S11 closes the synthetic signal combination layer, but portfolio work still has unresolved atoms that cannot be inferred from the signal spine:

- complete portfolio identity and source pages for P05, P06, and P07;
- complete instrument universe for each portfolio;
- source-native contract identity and local mapping for every member;
- roll and back-adjustment rules;
- instrument weights or deterministic weighting rules;
- IDM policy and applicability;
- target-risk and capital-base policy;
- cost, liquidity, minimum-capital, and data-availability eligibility rules;
- completed-bar synchronization across members;
- missing-member and fail-closed portfolio behavior;
- portfolio aggregation boundaries;
- audit requirements before implementation.

The current P05 phase-1 scaffold covers only `MES / ZN / ZF` and must not be inflated into complete P05. P06 and P07 require their own complete portfolio shape/readiness locks before implementation.

## Selected Gate Scope

The selected process draft should:

- identify P05, P06, and P07 as separate portfolio candidates;
- classify each as `SOURCE_NATIVE_FUTURES` unless later source evidence proves otherwise;
- record S09, S10, and S11 as synthetic forecast-block dependencies only;
- keep real portfolio construction, sizing, buffering, aggregation, and execution closed;
- list source atoms required before implementation;
- list data/readiness atoms required before any real-data work;
- define regular subagent hostile-audit requirements for the draft and any later implementation;
- identify when an Opus or GPT source-faithfulness audit is needed for larger source-table or book-fidelity disputes;
- preserve the old `QuantLab_v3` quarantine and CFD adapter boundary.

## Rejected Next Gates

### Open P07 Implementation Now

Rejected.

Reason:

```text
P07_COMPLETE_PORTFOLIO_ATOMS_REMAIN_UNRESOLVED
```

S11 supplies a synthetic combined forecast output. It does not lock a P07 universe, weights, IDM, eligibility, synchronization, aggregation, data lane, sizing, buffering, or execution policy.

### Open P06 Implementation Now

Rejected.

Reason:

```text
P06_CARRY_PORTFOLIO_ATOMS_REMAIN_UNRESOLVED
```

S10 supplies synthetic carry forecast-block conformance. It does not lock complete P06 portfolio construction or readiness.

### Expand P05 Phase-1 Into Complete P05 By Inference

Rejected.

Reason:

```text
P05_PHASE1_SEED_IS_NOT_COMPLETE_P05
```

The `MES / ZN / ZF` phase-1 scaffold is useful machinery, but complete P05 must be separately source-locked.

### Open Real Data, Diagnostics, Backtests, Or Adapters

Rejected.

Reason:

```text
REAL_DATA_AND_EVIDENCE_WORK_REQUIRES_SEPARATE_EXPLICIT_AUTHORIZATION
```

No NinjaTrader export, market-row parsing, readiness run, diagnostic, backtest, OOS, Lockbox, Forward, CFD adapter, deployment, trading, or promotion is authorized by this decision.

## Audit Requirements

The next process-only portfolio shape/readiness draft should receive a regular hostile audit, preferably by subagent, before it is treated as locked.

Audit focus:

- no implementation authorization smuggled into the draft;
- no complete-portfolio overclaim from P05 phase-1;
- no P06 or P07 implementation by inference from S10/S11;
- no real-data, diagnostic, backtest, OOS, Lockbox, Forward, CFD, deployment, trading, or promotion leakage;
- correct separation of signal-block completion from portfolio readiness;
- correct use of M3 as shared portfolio construction contract, not as a substitute for a portfolio-specific brief;
- no old `QuantLab_v3` active-pipeline use;
- clear distinction between regular subagent hostile audits and larger Opus/GPT source-faithfulness audits.

Opus or GPT audit is not required for this process-only next-step decision. It should be reserved for larger source-faithfulness questions, exact book-table disputes, or production-facing source-lock claims.

## Next Proposed Authorization

```text
Operator authorizes one process-only Carver P05/P06/P07 portfolio shape and
readiness gate draft.

Scope:
Create a process-only gate draft that maps the post-S11 Part One portfolio
graph into separately gated P05, P06, and P07 portfolio candidates. The draft
must identify unresolved portfolio source atoms, data/readiness atoms, audit
requirements, and fail-closed boundaries before any implementation.

Allowed:
Read-only inspection of current Carver process artifacts and creation of one
process gate draft artifact.

Forbidden:
No code edits, no tests, no real data, no market-row parsing, no NinjaTrader
export, no diagnostics, no backtests, no OOS, no Lockbox, no Forward, no CFD
adapters, no old QuantLab pipeline use, no tuning, no deployment, no trading,
no promotion, no portfolio implementation, no S11 implementation, no Opus
execution, no remote operations.
```

## Non-Authorization

This decision authorizes no code edits, no tests, no real data, no market-row parsing, no NinjaTrader export, no diagnostics, no backtests, no returns, no PnL, no Sharpe, no drawdown, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old-adapter import, no old workspace pipeline use, no tuning, no deployment, no trading, no promotion, no portfolio implementation, no P05/P06/P07 implementation, no Opus execution, no remote push, and no GitHub action.
