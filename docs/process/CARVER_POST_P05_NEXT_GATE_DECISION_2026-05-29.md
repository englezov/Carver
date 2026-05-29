# Carver Post-P05 Next Gate Decision

Date: 2026-05-29

Status:

```text
PROCESS_ONLY_CARVER_POST_P05_NEXT_GATE_DECISION_NOT_DATA_NOT_IMPLEMENTATION
```

## Purpose

Decide the next clean gate after:

```text
PROCESS_AND_SYNTHETIC_CODE_CARVER_P05_PHASE1_PORTFOLIO_CONSTRUCTION_CONFORMANCE_NOT_DIAGNOSTIC_NOT_BACKTEST
```

Current completed state:

- S09 phase-1 multi-instrument forecast conformance for `MES`, `ZN`, and `ZF`.
- P05 phase-1 construction conformance for `MES`, `ZN`, and `ZF`.
- Synthetic test surface passing before this decision record.
- No real data, diagnostics, backtests, OOS, Lockbox, Forward, CFD adapters, deployment, trading, or promotion authorized.

This record is a decision artifact only. It does not authorize code implementation, tests, data access, diagnostics, backtests, or remote operations.

## Decision

The next clean gate should be:

```text
PROCESS_AND_SYNTHETIC_CODE_CARVER_S10_M5_CARRY_CONSTRUCTION_CONFORMANCE_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

The gate should build the first synthetic-only S10/M5 carry-construction conformance surface, using hand-built toy curve inputs and locked source atoms only.

It must remain `SOURCE_NATIVE_FUTURES`.

## Why This Gate

P05 phase-1 construction has used the available S09 forecast and M1/M3 construction machinery as far as the current no-real-data posture allows.

The next P05 expansion would require source-native data and portfolio facts that are still unresolved:

- exact Jumbo universe;
- provider IDs and local mappings beyond the phase-1 seed;
- roll and back-adjustment policy;
- per-instrument eligible EWMAC speeds;
- instrument weights;
- IDM policy;
- cost eligibility.

Those facts cannot be invented or inferred from the phase-1 scaffold.

S10 is the next book-native source family after S09, and M5 already defines the process contract for futures-curve and carry construction. A synthetic-only S10/M5 conformance gate advances the clean first-spine architecture without touching real market rows.

## Selected Gate Scope

The selected gate may, after separate implementation authorization, define code and tests for:

- held-contract identity supplied as a locked input;
- comparison-contract identity supplied as a locked input;
- synchronized completed daily prices for the two curve legs;
- expiry-distance annualization using a locked convention;
- raw carry sign convention supplied as a locked input;
- annualized carry;
- risk-adjusted carry using a prevalidated price-risk input;
- fail-closed blockage for unresolved lane, contract identity, timestamps, expiry distance, sign convention, price risk, seasonal/wrong-sign policy, or curve-leg availability.

The selected gate should stop at the M5 output into M2:

```text
risk-adjusted carry forecast input
```

It should not yet implement the full S10 smoothing/FDM/position stack unless a later gate explicitly opens that layer.

## Rejected Next Gates

### Real Phase-1 MES/ZN/ZF Export Or Readiness Execution

Rejected for now.

Reason:

```text
REAL_DATA_EXECUTION_REQUIRES_EXPLICIT_OPERATOR_AUTHORIZATION
```

No NinjaTrader export, market-row parsing, readiness run over real files, diagnostic, or backtest is authorized by this decision.

### P05 Jumbo Expansion

Rejected for now.

Reason:

```text
P05_JUMBO_UNIVERSE_AND_PORTFOLIO_ATOMS_REMAIN_UNRESOLVED
```

The phase-1 seed must not be inflated into complete P05 or treated as a substitute for the Jumbo book portfolio.

### CFD Adapter Work

Rejected.

Reason:

```text
CFD_ADAPTER_REQUIRES_SEPARATE_EXPLICIT_ADAPTER_GATE_AFTER_SOURCE_NATIVE_BEHAVIOR_EXISTS
```

No CFD broker-clock, symbol, spread, timestamp, old adapter, or old workspace assumption may enter this lane.

### S11 Combined Trend/Carry

Deferred.

Reason:

```text
S11_DEPENDS_ON_S10_CARRY_ATOM_LOCK
```

S11 should not open before the S10/M5 carry-construction output is source-locked at least synthetically.

## Required Hostile Audit

Before this decision is treated as locked, a hostile audit should verify:

- no stage-transition leakage into real data or backtesting;
- no P05 complete-portfolio overclaim;
- no CFD or old `QuantLab_v3` contamination;
- correct choice of S10/M5 before S11;
- correct stopping point at M5 risk-adjusted carry output, not full S10 performance;
- no post-result tuning surface.

## Hostile Audit Result

Subagent hostile audit completed on 2026-05-29.

Audit disposition:

- No blocking findings.
- The memo stays process-only and rejects real-data execution, P05 Jumbo inflation, CFD adapter work, old `QuantLab_v3` contamination, and premature S11 work.
- The selected S10/M5 next gate is process-safe under the current no-real-data posture.
- The selected stopping point remains M5 risk-adjusted carry output into M2, not full S10 smoothing, FDM, position construction, diagnostics, backtesting, or performance interpretation.
- No files were edited by the auditor.
- No real data, diagnostics, backtests, adapter work, old workspace access, or remote operations were performed.

## Non-Authorization

This record authorizes no data access, no market-row parsing, no NinjaTrader export, no implementation, no tests, no diagnostics, no backtests, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old-adapter import, no old workspace pipeline use, no tuning, no deployment, no trading, no promotion, no remote push, and no GitHub action.
