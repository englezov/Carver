# Carver Pre-Opus Definition Completion Record

Date: 2026-05-28

Status:

```text
PROCESS_ONLY_CARVER_PRE_OPUS_DEFINITION_COMPLETION_RECORD_NOT_DATA_NOT_IMPLEMENTATION_AUTHORIZATION
```

## Purpose

Record that the current clean Carver daily source-native definition layer is complete enough to submit to a separate source-faithfulness audit, before any Opus audit execution, data work, implementation, tests, diagnostics, backtests, OOS, Lockbox, Forward, CFD adapter work, old QuantLab import, tuning, deployment, trading, or promotion.

This record is a process artifact only. It does not approve code, data inspection, NinjaTrader export, market-row parsing, historical evaluation, strategy computation, or portfolio reconstruction beyond the already drafted process briefs.

## Scope

This completion record covers the current first-spine definition set:

- M0 source-native futures foundation.
- M1 position sizing and risk scaling.
- M2 forecast-block architecture.
- M3 multi-instrument portfolio construction.
- M5 futures curve and carry construction.
- S01 buy-and-hold single contract.
- S02 buy-and-hold with risk scaling.
- S03 buy-and-hold with variable risk scaling.
- S04 buy-and-hold portfolio with variable risk position sizing.
- P01 risk parity example portfolio.
- P02 All Weather example portfolio.
- S09 multiple trend following.
- S10 basic carry.
- S11 combined carry and trend.

The record does not cover Part Two and Part Three extensions after S11, Part Four fast-stack strategies, Part Five relative-value strategies, later Jumbo portfolios, CFD adapter work, or implementation/data gates.

## Definition Coverage Matrix

| Artifact | Role | Definition disposition before Opus audit |
| --- | --- | --- |
| `docs/process/CARVER_M0_SOURCE_NATIVE_FUTURES_FOUNDATION_SPEC_2026-05-28.md` | Foundation defaults and hard boundaries | Present; declares `SOURCE_NATIVE_FUTURES`, completed-bar rule, source-native instrument identity, data-surface non-authorization, old workspace quarantine, and no-code/no-data posture. |
| `docs/process/CARVER_M1_POSITION_SIZING_AND_RISK_SCALING_MODULE_SPEC_2026-05-28.md` | Shared sizing/risk module | Present; hostile-audited and patched; pre-validates risk estimates, timestamp alignment, context-applicable portfolio/forecast inputs, and M1/M2 trade-decision boundary. |
| `docs/process/CARVER_M2_FORECAST_BLOCK_ARCHITECTURE_MODULE_SPEC_2026-05-28.md` | Shared forecast-block module | Present; hostile-audited and patched; now explicitly declares `SOURCE_NATIVE_FUTURES`; keeps S07/S08 as forecast-building components rather than standalone advancements. |
| `docs/process/CARVER_M3_MULTI_INSTRUMENT_PORTFOLIO_CONSTRUCTION_MODULE_SPEC_2026-05-28.md` | Shared portfolio construction module | Present; hostile-audited and patched; enforces portfolio independence, source-native lane class, local mapping caution, and no silent substitution. |
| `docs/process/CARVER_M5_FUTURES_CURVE_AND_CARRY_CONSTRUCTION_MODULE_SPEC_2026-05-28.md` | Shared futures curve/carry module | Present; hostile-audited and patched; requires source-native lane class, raw carry sign convention, synchronized completed curve legs, and seasonal/wrong-sign fail-closed rules. |
| `docs/researchops/candidates/CARVER_S01_BUY_AND_HOLD_SINGLE_CONTRACT_CANDIDATE_BRIEF_2026-05-28.md` | First standalone baseline candidate | Present; `SOURCE_NATIVE_FUTURES`; process-only; establishes single-contract futures identity and excess-return/back-adjustment atoms. |
| `docs/researchops/candidates/CARVER_S02_BUY_AND_HOLD_WITH_RISK_SCALING_CANDIDATE_BRIEF_2026-05-28.md` | Risk-scaled standalone candidate | Present; `SOURCE_NATIVE_FUTURES`; process-only; adds target risk, current held-contract price, multiplier, FX, fixed-risk sizing, rounding, and minimum-capital atoms. |
| `docs/researchops/candidates/CARVER_S03_BUY_AND_HOLD_WITH_VARIABLE_RISK_SCALING_CANDIDATE_BRIEF_2026-05-28.md` | Variable-risk standalone candidate | Present; `SOURCE_NATIVE_FUTURES`; process-only; adds non-leaking variable risk estimate and S03 volatility atoms. |
| `docs/researchops/candidates/CARVER_S04_BUY_AND_HOLD_PORTFOLIO_WITH_VARIABLE_RISK_POSITION_SIZING_CANDIDATE_BRIEF_2026-05-28.md` | Portfolio construction candidate gateway | Present; `SOURCE_NATIVE_FUTURES`; process-only; adds instrument weights, IDM, portfolio breadth, and complete-portfolio separation. |
| `docs/researchops/portfolios/CARVER_P01_RISK_PARITY_EXAMPLE_PORTFOLIO_BRIEF_2026-05-28.md` | First complete book portfolio | Present; `SOURCE_NATIVE_FUTURES`; process-only; locks the two-instrument risk-parity example as a separate portfolio brief. |
| `docs/researchops/portfolios/CARVER_P02_ALL_WEATHER_EXAMPLE_PORTFOLIO_BRIEF_2026-05-28.md` | Second complete book portfolio | Present; `SOURCE_NATIVE_FUTURES`; process-only; locks the six-instrument All Weather example as a separate portfolio brief. |
| `docs/researchops/candidates/CARVER_S09_MULTIPLE_TREND_FOLLOWING_CANDIDATE_BRIEF_2026-05-28.md` | First core trend forecast candidate | Present; `SOURCE_NATIVE_FUTURES`; process-only; captures EWMAC variations, forecast scalars, speed eligibility, FDM, caps, and S07/S08 sleeve treatment. |
| `docs/researchops/candidates/CARVER_S10_BASIC_CARRY_CANDIDATE_BRIEF_2026-05-28.md` | First core carry forecast candidate | Present; `SOURCE_NATIVE_FUTURES`; process-only; captures carry curve construction, carry smoothing, scalar/cap/FDM, seasonality, and wrong-sign blockages. |
| `docs/researchops/candidates/CARVER_S11_COMBINED_CARRY_AND_TREND_CANDIDATE_BRIEF_2026-05-28.md` | First combined trend/carry candidate | Present; `SOURCE_NATIVE_FUTURES`; process-only; combines S09 and S10 forecast blocks while blocking P07 and later parts. |

## Gap Assessment

No missing definition artifact remains for the current daily first spine listed above.

The following are intentionally unresolved gates, not definition-completion blockers:

- Local source-native data-surface acceptance.
- Local symbol mapping between Appendix C broker codes and NinjaTrader or other local data labels.
- Roll calendar and exchange-session lock.
- Cost-source file creation and lane-specific cost lock.
- Concrete target-risk and capital-base choices for any future executable run.
- Rounding, buffering, and trade/no-trade implementation details.
- EWMA warm-up, Table 51 row selection, Table 52 interpolation policy, and synthetic conformance examples.
- Carry curve leg availability, raw carry sign convention per instrument, expiry calendar source, fixed-month commodity table, and wrong-sign/seasonal blockage table.

These gates must remain closed before data work or implementation. They are suitable questions for later implementation-gate or data-surface artifacts, not for the Opus source-faithfulness audit itself.

## Out-Of-Scope Definitions

The following definitions are intentionally not complete under this record:

- M4 normalised-price and asset-class module for later Part Three variants.
- M6 synthetic-instrument module for relative-value spreads/triplets.
- M7 hourly/fast-stack module for S26/S27.
- M8 risk-management overlay module.
- S05-S08 as standalone candidate briefs; they remain forecast/sleeve components under S09/M2 framing.
- S12-S30 and P03-P14.
- Any CFD adapter or broker translation work.
- Any implementation skeleton, source code, tests, diagnostics, backtests, or local data inspection.

## Pre-Opus Completion Claim

The current first-spine definition layer is complete enough to ask an external source-faithfulness auditor whether the translation is faithful to Carver's book.

The next clean gate should be a separate Opus source-faithfulness audit gate. That future gate should inspect the book and the artifacts listed in this record, then answer whether the definitions describe the strategies, portfolios, labels, stack boundaries, unresolved atoms, and non-authorization rules faithfully.

This record does not authorize the Opus audit execution by itself.

## Required Hostile Audit

Before this definition-completion record and the material M2 lane-class patch are treated as process-safe, a subagent hostile audit must verify:

- The current definition set is complete only for the stated first spine.
- The record does not smuggle in implementation, data, tests, diagnostics, backtests, OOS, Lockbox, Forward, CFD adapter work, old QuantLab imports, tuning, deployment, trading, or promotion.
- M2's new lane-class language is consistent with the source-native spine and does not open a data lane.
- Out-of-scope modules and later strategies remain blocked rather than silently treated as complete.

## Hostile Audit Result

Subagent hostile audit completed on 2026-05-28.

Audit disposition:

- No blocking findings.
- The record is process-safe and truthful for the stated first spine only: M0/M1/M2/M3/M5, S01/S02/S03/S04, P01/P02, S09/S10/S11.
- The record does not authorize Opus audit execution; a separate future Opus audit gate remains required.
- The record does not authorize code, data, tests, diagnostics, backtests, OOS, Lockbox, Forward, CFD adapter work, old QuantLab imports, tuning, deployment, trading, or promotion.
- Later modules, strategies, portfolios, fast-stack work, RV-stack work, and CFD adapter work remain out of scope.
- The M2 lane-class patch is consistent with the source-native spine and does not open data or adapter work.

Verdict: the first-spine definition layer is process-safe before creating the separate Opus audit gate.

## Standing Non-Authorization

This file authorizes no data access, no market-row parsing, no implementation, no tests, no diagnostics, no backtests, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old-adapter import, no tuning, no deployment, no trading, and no promotion.
