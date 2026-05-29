# Carver Post-S10/M5 Next Step Decision

Date: 2026-05-29

Status:

```text
PROCESS_ONLY_CARVER_POST_S10_M5_NEXT_STEP_DECISION_NOT_DATA_NOT_IMPLEMENTATION
```

## Purpose

Decide the next clean roadmap branch after the hostile-audited S10/M5 synthetic carry-construction surface.

Current completed state:

- Post-P05 next-gate decision selected S10/M5 carry construction.
- S10/M5 implementation gate draft received a no-blocking-findings hostile audit.
- S10/M5 synthetic M5 conformance code and tests exist.
- Implemented S10/M5 surface received a no-blocking-findings hostile audit.
- M5 now emits only a synthetic risk-adjusted carry forecast input into later M2/S10 machinery.
- No real data, diagnostics, backtests, OOS, Lockbox, Forward, CFD adapters, deployment, trading, promotion, remote push, or old workspace pipeline use is authorized.

This record is a decision artifact only. It does not authorize code edits, tests, data access, diagnostics, backtests, Opus execution, or remote operations.

## Decision

The next clean branch should be:

```text
S10_CARRY_FORECAST_BLOCK_EXTENSION_BEFORE_S11
```

Do not open S11 implementation or S11 conformance yet.

Reason:

```text
S11_DEPENDS_ON_S10_CARRY_FORECAST_ATOM_LOCK
```

The current M5 surface stops at risk-adjusted carry input. S11 requires usable S10 carry forecast blocks, including the carry smoothing spans, scalar, caps, forecast weighting, FDM, and treatment of unavailable carry variations. Those atoms are not implemented or source-locked by the current M5 gate.

## Selected Next Gate Shape

The next possible process gate should draft a full S10 carry forecast-block extension, still synthetic-only, that connects:

```text
M5 risk-adjusted carry input
-> Carry5/20/60/120 smoothing inputs
-> carry scalar
-> individual caps
-> locked eligible carry span set
-> equal weights across eligible carry spans
-> carry FDM
-> final capped S10 carry forecast output
```

The future gate should remain `SOURCE_NATIVE_FUTURES` and should stop before:

- forecast-scaled position sizing;
- buffering and trade/no-trade decisions;
- S11 trend/carry combination;
- P06 Jumbo carry portfolio;
- P07 combined trend/carry portfolio;
- real data, diagnostics, or backtests.

## Opus Requirement Before Production Source Locks

Because the next S10 extension touches book source interpretation, an Opus hostile source-faithfulness audit is required before any future gate treats the following as production source-locked:

- raw carry sign conventions beyond toy synthetic labels;
- production expiry calendars or month-distance conventions;
- production roll-day handling;
- fixed-month commodity rules;
- seasonal or wrong-sign carry policies;
- full S10 smoothing spans, scalar, caps, cost eligibility, FDM, or forecast weighting;
- any S11 source weighting, style allocation, or FDM interpretation.

A regular hostile audit is sufficient for this process-only decision record, but not for production carry interpretation locks.

This record does not authorize Opus execution by itself.

## Rejected Branches

### Open S11 Now

Rejected for now.

Reason:

```text
S10_CARRY_FORECAST_BLOCK_NOT_YET_LOCKED
```

S11 combines trend and carry building blocks. Opening S11 before the S10 carry forecast block exists would force S11 to depend on an incomplete carry sleeve.

### Open P06 Or P07

Rejected.

Reason:

```text
PORTFOLIO_CHILDREN_REQUIRE_SOURCE_LOCKED_MEMBER_STRATEGIES_AND_PORTFOLIO_ATOMS
```

P06 and P07 remain complete portfolio candidates. They require source-locked member strategies, instrument universe, provider mappings, roll/session/cost rules, weights, IDM, and evidence-window budget. None are authorized here.

### Real Data Or Diagnostics

Rejected.

Reason:

```text
REAL_DATA_AND_DIAGNOSTICS_REQUIRE_SEPARATE_OPERATOR_AUTHORIZATION
```

No market-row parsing, NinjaTrader export, diagnostics, backtests, OOS, Lockbox, Forward, or evidence-window work is authorized.

### CFD Adapter Work

Rejected.

Reason:

```text
CFD_ADAPTER_REQUIRES_SEPARATE_EXPLICIT_ADAPTER_GATE_AFTER_SOURCE_NATIVE_BEHAVIOR_EXISTS
```

No CFD broker-clock, symbol, spread, timestamp, old adapter, or old workspace assumption may enter this lane.

## Required Hostile Audit

Before this decision is treated as locked, a hostile audit should verify:

- no implementation authorization is smuggled into the decision;
- S10 carry forecast-block extension before S11 is process-safe;
- S11, P06, P07, real data, diagnostics, backtests, CFD adapters, deployment, trading, promotion, and remote operations remain closed;
- the Opus requirement is present for future production carry interpretation locks and is not self-authorizing;
- no tuning-after-results surface is opened;
- no old `QuantLab_v3` contamination exists.

## Suggested Audit Authorization Prompt

```text
Operator authorizes exactly one regular hostile audit of the Carver
post-S10/M5 next-step decision artifact:

docs/process/CARVER_POST_S10_M5_NEXT_STEP_DECISION_2026-05-29.md

Scope:
Audit the process-only decision to extend S10 carry forecast-block machinery
before opening S11. Verify that S11, P06, P07, real data, diagnostics,
backtests, CFD adapters, Opus execution, remote operations, deployment,
trading, promotion, tuning, and old QuantLab use remain closed.

Allowed:
Read-only file inspection and concise audit findings.

Forbidden:
No file edits, no code tests, no real data, no market-row parsing, no
NinjaTrader export, no diagnostics, no backtests, no CFD adapters, no Opus
execution, no remote operations, and no access to
C:\Users\openclaw\Desktop\QuantLab_v3.
```

## Non-Authorization

This record authorizes no code edits, no tests, no data access, no market-row parsing, no NinjaTrader export, no diagnostics, no backtests, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old-adapter import, no old workspace pipeline use, no tuning, no deployment, no trading, no promotion, no S10 implementation, no S11, no P06/P07 portfolio work, no Opus execution, no remote push, and no GitHub action.
