# Carver First Portfolio Construction Gate Prep

Status: `PROCESS_ONLY_CARVER_FIRST_PORTFOLIO_CONSTRUCTION_GATE_PREP_NOT_AUTHORIZATION`

Date: 2026-05-29

## Purpose

Define the next safe gate after S09 phase-1 multi-instrument forecast conformance. The next gate is the first place where portfolio construction may be implemented, but only after separate operator authorization.

This prep artifact does not authorize portfolio construction, real-data execution, diagnostics, backtests, or promotion.

## Current Locked Inputs

- M0/M1/M2/M3/M5 process definitions exist for source-native futures.
- P01 and P02 portfolio definitions exist as book-faithful construction targets.
- Phase-1 daily manifest exists for the first small multi-asset seed set.
- Phase-1 executable roots are `MES`, `ZN`, and `ZF`; `QM`, `ZC`, and `MGC` remain declared but not executable until commodity/metal chain conventions are locked.
- S09 phase-1 multi-instrument forecast conformance exists for `MES / ZN / ZF`, forecast-only, with no returns or diagnostics.

## Proposed First Construction Surface

Name: `P05_PHASE1_S09_MULTI_INSTRUMENT_PORTFOLIO_CONSTRUCTION_CONFORMANCE`

The first construction surface should take already-built S09 forecast results for `MES`, `ZN`, and `ZF` and produce only source-native desired position inputs per instrument.

It may include:

- exact instrument identity checks,
- source-native lane checks,
- phase-1 root order checks,
- instrument weights for a declared phase-1 construction set,
- IDM/FDM source references,
- capital and target-risk source references,
- daily price risk / annual risk source references,
- per-instrument desired position calculation via M1,
- rounding and buffering placeholders if not source-locked.

It must not include:

- returns,
- PnL,
- Sharpe,
- drawdown,
- diagnostics,
- backtests,
- OOS,
- Lockbox,
- Forward,
- CFD adapters,
- old QuantLab imports,
- tuning,
- deployment,
- trading,
- promotion.

## Blocking Atoms Before Real Construction

- Phase-1 continuous readiness must be ready for `MES`, `ZN`, and `ZF`.
- Daily price-risk source must be locked per root, not synthetic unit risk.
- Capital base must be operator-authorized for construction conformance.
- Target risk must be source/operator locked for the construction example.
- Instrument weights must be declared as either a P01/P02/P05 subset or a separate phase-1 construction scaffold.
- IDM treatment must be locked for the chosen construction surface.
- Rounding and buffering must remain blocked or separately source-locked.
- No commodity leg may be silently omitted from P02; phase-1 is a seed construction surface, not the complete P02 portfolio.

## Suggested Next Authorization Prompt

```
Operator authorizes exactly one process-only/implementation gate for the Carver
P05 phase-1 S09 multi-instrument portfolio construction conformance surface.

Scope:
Clean Carver workspace only. Use the existing S09 phase-1 forecast-only
conformance surface for MES, ZN, and ZF. Build a fail-closed construction
surface that can convert already-validated S09 forecasts plus locked M1/M3
inputs into desired source-native position inputs for the phase-1 seed set.

Allowed:
Code contracts, synthetic tests, and process documentation for portfolio
construction conformance only.

Forbidden:
No real-data execution, no diagnostics, no backtests, no returns, no PnL,
no Sharpe, no drawdown, no OOS, no Lockbox, no Forward, no CFD adapters,
no old QuantLab imports, no tuning, no deployment, no trading, no promotion,
and no claim that MES/ZN/ZF is the complete P02 portfolio.

Required:
Completed bars only. Source-native futures only. Fail closed unless all source
atoms are locked. Use hostile audit before treating the surface as process-safe.

Required status:
PROCESS_AND_SYNTHETIC_CODE_CARVER_P05_PHASE1_PORTFOLIO_CONSTRUCTION_CONFORMANCE_NOT_DIAGNOSTIC_NOT_BACKTEST
```
