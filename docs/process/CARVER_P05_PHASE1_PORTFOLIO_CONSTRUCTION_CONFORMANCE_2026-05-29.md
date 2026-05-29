# Carver P05 Phase-1 Portfolio Construction Conformance

Status: `PROCESS_AND_SYNTHETIC_CODE_CARVER_P05_PHASE1_PORTFOLIO_CONSTRUCTION_CONFORMANCE_NOT_DIAGNOSTIC_NOT_BACKTEST`

Date: 2026-05-29

## Purpose

Build the first source-native construction conformance surface that converts already-validated S09 phase-1 forecasts into desired per-instrument position inputs for MES / ZN / ZF.

This is a phase-1 seed construction scaffold. It is not complete P02, not complete P05, not the Jumbo portfolio, and not alpha evidence.

## Scope

The code surface is locked to:

- Lane class: `SOURCE_NATIVE_FUTURES`
- Roots: `MES`, `ZN`, `ZF`
- Input forecast source: `S09Phase1MultiInstrumentConformanceResult`
- Portfolio identity: `P05_PHASE1_MES_ZN_ZF_SEED_CONSTRUCTION_NOT_COMPLETE_PORTFOLIO`
- Seed scaffold weights: equal one-third weights for MES / ZN / ZF only
- Forecast-to-position convention: final capped forecast divided by `10`
- M1 base sizing inputs: capital, target risk, current held-contract price, annual risk estimate, multiplier, FX, instrument weight, and IDM
- S09 daily price-risk consistency check: current held price times annual percentage risk divided by `sqrt(256)`

The surface emits desired contract counts only. It does not aggregate returns or interpret performance.

## Explicit Non-Authorization

No returns, PnL, Sharpe, drawdown, diagnostics, backtests, OOS, Lockbox, Forward, CFD adapters, old QuantLab imports, tuning, deployment, trading, promotion, real-data execution, or remote push are authorized by this artifact.

## Complete-Portfolio Boundary

MES / ZN / ZF is a construction seed set only.

It must not be described as complete P02 because P02 also requires QM, ZC, and MGC.

It must not be described as complete P05 because P05 requires a separately locked Jumbo universe, source-native provider mapping, per-instrument eligible EWMAC speed sets, instrument weights, IDM policy, roll/back-adjustment policy, and cost eligibility.

## Gate Behaviour

The code must fail closed when:

- S09 input is not forecast-only,
- S09 roots are missing, extra, or out of order,
- S09 input row count or source contract months drift from the locked phase-1 forecast surface,
- forecast timestamps are not aligned across MES / ZN / ZF,
- portfolio id is not the locked phase-1 seed id,
- portfolio roots are not exactly MES / ZN / ZF in order,
- contract identity drifts,
- capital, target risk, IDM, FX, risk, weight, daily price risk, or forecast-to-position source locks are unresolved,
- capital, target risk, IDM, price, risk, FX, or daily price-risk timestamps are stale,
- daily price risk does not match the locked S09 conversion,
- any non-source-native lane is supplied.

## Next Boundary

The next possible gate is either:

- real phase-1 export/readiness execution for MES / ZN / ZF under a separate explicit data authorization, or
- extension of the construction scaffold to additional source-locked instruments after their chain conventions are locked.

Neither is authorized here.
