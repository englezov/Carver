# Carver P05/P06/P07 Portfolio Shape And Readiness Gate Draft

Date: 2026-05-29

Status:

```text
PROCESS_ONLY_CARVER_P05_P06_P07_PORTFOLIO_SHAPE_READINESS_GATE_DRAFT_NOT_DATA_NOT_IMPLEMENTATION
```

## Purpose

Draft the next Part One portfolio graph gate after S11 combined carry/trend completion.

This draft maps P05, P06, and P07 into separately gated portfolio candidates and identifies the source atoms, data/readiness atoms, audit requirements, and fail-closed boundaries required before any implementation.

This draft does not authorize code edits, tests, real data, diagnostics, backtests, portfolio implementation, Opus execution, remote operations, deployment, trading, or promotion.

## Upstream State

Completed synthetic signal spine:

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

Existing portfolio machinery:

- M3 process spec defines the shared portfolio construction contract.
- P01/P02 synthetic package exists as an earlier exact-portfolio conformance path.
- P05 phase-1 construction conformance exists for `MES`, `ZN`, and `ZF` only.
- P05 phase-1 is not complete P05, not P06, not P07, and not the Jumbo portfolio.

## Candidate Portfolio Map

| Candidate | Role | Upstream signal dependency | Current status |
| --- | --- | --- | --- |
| P05 | Trend portfolio candidate | S09 trend forecast block | Phase-1 seed construction exists only for `MES / ZN / ZF`; complete P05 remains unresolved |
| P06 | Carry portfolio candidate | S10 carry forecast block | Not opened; complete portfolio shape and readiness unresolved |
| P07 | Combined trend/carry portfolio candidate | S11 combined carry/trend forecast block | Not opened; complete portfolio shape and readiness unresolved |

Each candidate must be treated as a separate complete portfolio candidate. No candidate may infer implementation authorization from a completed upstream signal block.

## Lane Classification

Default lane classification for all three candidates:

```text
SOURCE_NATIVE_FUTURES
```

No `CFD_DIRECT` or `CFD_ADAPTER` lane is opened by this draft. Any future CFD adapter work requires a separate adapter gate after source-native behavior exists.

## Portfolio Source Atoms Required Before Implementation

Before any P05, P06, or P07 implementation gate, the selected portfolio candidate must lock or explicitly block:

- portfolio identity and source pages;
- whether the candidate is standalone, source-native portfolio sleeve, or complete book portfolio;
- complete instrument universe;
- source-native contract identity for every member;
- local provider mapping requirements and no-substitution policy;
- asset class, group, and instrument taxonomy if handcrafted weights apply;
- instrument weights or deterministic weight-construction rule;
- IDM source, exact value, or blocked calculation policy;
- portfolio target-risk and capital-base policy;
- cost eligibility rule;
- liquidity eligibility rule;
- minimum-capital rule;
- data-availability rule;
- forecast dependency rule:
  - P05 uses locked S09 trend forecast outputs;
  - P06 uses locked S10 carry forecast outputs;
  - P07 uses locked S11 combined carry/trend forecast outputs;
- forecast-to-position convention and whether it is inherited from existing M1/M3 machinery or separately source-locked;
- completed-bar synchronization rule across members;
- missing-member and fail-closed behavior;
- portfolio aggregation boundary;
- prohibition on post-result instrument addition, removal, rescue, or reweighting.

## Data And Readiness Atoms Required Before Real-Data Work

Before any real data, readiness execution, diagnostic, or backtest, the selected portfolio candidate must separately lock:

- exact source-native provider IDs or approved local mappings for every member;
- intake route: direct daily bars or separately justified minute-derived fallback;
- session calendar and timezone artifacts;
- roll rule and back-adjustment artifacts for continuous futures use;
- completed daily bar convention;
- annual risk source and validation path;
- FX source and validation path;
- raw-response quarantine location and request/provider binding rules if API or chart data is used;
- data-window budget and evidence-stage label;
- explicit operator authorization for any real-data execution.

No such data or readiness execution is authorized by this draft.

## Candidate-Specific Boundaries

### P05 Trend Portfolio

P05 may later reuse the already-audited S09 forecast machinery and the phase-1 construction lessons, but complete P05 is not locked by the `MES / ZN / ZF` seed.

P05-specific unresolved atoms include:

- complete P05 instrument universe;
- whether the phase-1 seed members are a subset, a scaffold, or a separate readiness route;
- per-instrument eligible EWMAC speed sets;
- complete source-native provider mappings;
- complete instrument weights;
- IDM policy;
- cost and liquidity eligibility;
- roll/back-adjustment policy;
- missing-member behavior.

### P06 Carry Portfolio

P06 may later reuse the audited S10 carry forecast block as an upstream signal dependency.

P06-specific unresolved atoms include:

- complete P06 instrument universe;
- carry-eligible instruments and curve-leg availability;
- carry source assumptions by instrument family;
- fixed-month, seasonal, and wrong-sign carry policies where relevant;
- per-instrument carry forecast eligibility;
- complete source-native provider mappings;
- complete instrument weights;
- IDM policy;
- cost and liquidity eligibility;
- roll/back-adjustment policy;
- missing-member behavior.

### P07 Combined Trend/Carry Portfolio

P07 may later reuse the audited S11 combined carry/trend forecast block as an upstream signal dependency.

P07-specific unresolved atoms include:

- complete P07 instrument universe;
- relationship between P07 and P05/P06 member sets;
- whether P07 is built from S11 combined forecasts directly or from portfolio-level combination rules;
- complete source-native provider mappings;
- complete instrument weights;
- IDM policy;
- forecast dependency and synchronization across trend/carry components;
- cost and liquidity eligibility;
- roll/back-adjustment policy;
- missing-member behavior;
- separation from any later S11 portfolio execution or production deployment.

## Fail-Closed Boundaries

Any later implementation gate must fail closed if:

- lane class is not exactly `SOURCE_NATIVE_FUTURES`;
- complete portfolio identity is unresolved;
- any member identity or local mapping is unresolved;
- any Appendix C or broker code is treated as a local data identifier without a mapping lock;
- the P05 phase-1 seed is treated as complete P05;
- P06 or P07 is inferred from S10/S11 signal completion without a portfolio-specific brief;
- portfolio weights, IDM, target risk, capital base, or eligibility are unresolved;
- completed-bar synchronization is unresolved;
- missing-member behavior is unresolved;
- any real data, diagnostics, backtests, OOS, Lockbox, Forward, CFD adapter, deployment, trading, or promotion path is opened without separate authorization;
- any old `QuantLab_v3` active-pipeline artifact is used as authority;
- any portfolio member is added, dropped, rescued, reweighted, or tuned after seeing results.

## Rejected Interpretations

### P05 Phase-1 Equals Complete P05

Rejected.

```text
P05_PHASE1_SEED_IS_NOT_COMPLETE_P05
```

### S10 Completion Opens P06 Implementation

Rejected.

```text
S10_CARRY_SIGNAL_COMPLETION_IS_NOT_P06_PORTFOLIO_AUTHORIZATION
```

### S11 Completion Opens P07 Implementation

Rejected.

```text
S11_COMBINED_SIGNAL_COMPLETION_IS_NOT_P07_PORTFOLIO_AUTHORIZATION
```

### Synthetic Portfolio Shape Opens Real Data

Rejected.

```text
REAL_DATA_REQUIRES_SEPARATE_EXPLICIT_OPERATOR_AUTHORIZATION
```

### Regular Audit Requires Opus Or GPT

Rejected for this draft.

```text
REGULAR_HOSTILE_AUDIT_SHOULD_BE_LEAN_AND_SUBAGENT_WHEN_AVAILABLE
```

Opus or GPT should be reserved for large source-faithfulness audits, exact book-table disputes, production-facing source-lock claims, or other operator-authorized external audit packets.

## Audit Requirements

Before this draft is treated as locked, a regular hostile audit should verify:

- no implementation authorization is smuggled into the draft;
- P05 phase-1 is not inflated into complete P05;
- P06 and P07 remain unopened for implementation;
- all three candidates remain separate portfolio candidates;
- S09/S10/S11 are used only as upstream synthetic forecast dependencies;
- M3 is used as shared portfolio contract context, not as a substitute for a portfolio-specific source brief;
- source atoms and data/readiness atoms are separated;
- no real data, diagnostics, backtests, OOS, Lockbox, Forward, CFD adapters, old `QuantLab_v3` active-pipeline use, tuning, deployment, trading, promotion, Opus execution, remote operation, or GitHub action is opened.

## Suggested Regular Hostile Audit Prompt

```text
Operator authorizes exactly one regular hostile audit of the Carver P05/P06/P07
portfolio shape and readiness gate draft.

Scope:
Audit the process-only portfolio shape/readiness gate draft:
docs/process/CARVER_P05_P06_P07_PORTFOLIO_SHAPE_READINESS_GATE_DRAFT_2026-05-29.md

Allowed:
Read-only file inspection and concise audit findings.

Forbidden:
No file edits, no code tests, no real data, no market-row parsing, no
NinjaTrader export, no diagnostics, no backtests, no OOS, no Lockbox, no
Forward, no CFD adapters, no old QuantLab pipeline use, no tuning, no
deployment, no trading, no promotion, no portfolio implementation, no S11
implementation, no Opus execution, no remote operations.
```

## Non-Authorization

This draft authorizes no code edits, no tests, no real data, no market-row parsing, no NinjaTrader export, no diagnostics, no backtests, no returns, no PnL, no Sharpe, no drawdown, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old-adapter import, no old workspace pipeline use, no tuning, no deployment, no trading, no promotion, no portfolio implementation, no P05/P06/P07 implementation, no S11 implementation, no Opus execution, no remote push, and no GitHub action.
