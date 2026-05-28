# Carver S11 Combined Carry And Trend Candidate Brief

Date: 2026-05-28

Status:

```text
PROCESS_ONLY_CARVER_S11_COMBINED_CARRY_AND_TREND_CANDIDATE_BRIEF_DRAFT_NOT_DATA_NOT_STRATEGY_AUTHORIZATION
```

## Purpose

Create the process-only source-native futures candidate brief for Carver Strategy 11:

```text
S11_COMBINED_CARRY_AND_TREND
```

This brief inherits M0, S01, S02, S03, S04, P01, P02, S09, and S10. It records the source framing, classification, dependencies, locked process atoms, unresolved atoms, and next gates before any data work or implementation.

This brief is not a data lane, implementation lane, test lane, diagnostic lane, backtest lane, OOS lane, Lockbox lane, Forward lane, CFD adapter lane, deployment lane, trading lane, or promotion lane.

## Classification

| Field | Value |
| --- | --- |
| Strategy ID | S11 |
| Book strategy | Strategy eleven: Combined carry and trend |
| Book pages | `Carver.pdf`, PDF pages 264-275 |
| Lane class | `SOURCE_NATIVE_FUTURES` |
| Strategy label | `STANDALONE_CANDIDATE` |
| Timeframe family | Daily directional forecast stack |
| Data posture | No data access authorized |
| Implementation posture | No implementation authorized |
| Evidence posture | No diagnostics or backtests authorized |

## Dependencies

S11 depends on:

- `docs/process/CARVER_M0_SOURCE_NATIVE_FUTURES_FOUNDATION_SPEC_2026-05-28.md`
- `docs/process/CARVER_LEAN_IMPLEMENTATION_AND_BACKTEST_DEFERRAL_RULE_2026-05-28.md`
- `docs/process/CARVER_SOURCE_NATIVE_TRANSLATION_ARCHITECTURE_GOAL_2026-05-28.md`
- `docs/researchops/handoffs/CARVER_BOOK_STRATEGY_AND_PORTFOLIO_INVENTORY_001_2026-05-28.md`
- `docs/researchops/candidates/CARVER_S01_BUY_AND_HOLD_SINGLE_CONTRACT_CANDIDATE_BRIEF_2026-05-28.md`
- `docs/researchops/candidates/CARVER_S02_BUY_AND_HOLD_WITH_RISK_SCALING_CANDIDATE_BRIEF_2026-05-28.md`
- `docs/researchops/candidates/CARVER_S03_BUY_AND_HOLD_WITH_VARIABLE_RISK_SCALING_CANDIDATE_BRIEF_2026-05-28.md`
- `docs/researchops/candidates/CARVER_S04_BUY_AND_HOLD_PORTFOLIO_WITH_VARIABLE_RISK_POSITION_SIZING_CANDIDATE_BRIEF_2026-05-28.md`
- `docs/researchops/portfolios/CARVER_P01_RISK_PARITY_EXAMPLE_PORTFOLIO_BRIEF_2026-05-28.md`
- `docs/researchops/portfolios/CARVER_P02_ALL_WEATHER_EXAMPLE_PORTFOLIO_BRIEF_2026-05-28.md`
- `docs/researchops/candidates/CARVER_S09_MULTIPLE_TREND_FOLLOWING_CANDIDATE_BRIEF_2026-05-28.md`
- `docs/researchops/candidates/CARVER_S10_BASIC_CARRY_CANDIDATE_BRIEF_2026-05-28.md`

S11 is a prerequisite for:

- P07 Jumbo combined trend/carry portfolio.
- Part Two and Part Three forecast-block extensions that combine with S09, S10, and S11.
- Later allocation overlays, if separately authorized.

## Book Framing

Carver frames S11 as the final Part One forecast-block construction: combine trend and carry because all forecasts are calibrated to a common scale.

Source anchors:

- S11 starts as "Combined carry and trend" on `Carver.pdf`, PDF page 264.
- Carver recaps the path from single-contract holding, to risk scaling, to multi-instrument portfolios, to forecast-based trend rules, to carry forecasts on PDF page 264.
- S11 is defined as trading one or more instruments with variable-risk position sizing and scaling positions according to a combined forecast that is a weighted average of carry and trend forecasts on PDF page 264.
- Carver introduces the building-block, "Lego" style forecast architecture on PDF page 265, stating that scaled trading-rule forecasts can be combined because they share a common scale.
- The S11 building blocks are S09 trend variations EWMAC2, EWMAC4, EWMAC8, EWMAC16, EWMAC32, EWMAC64, and S10 carry variations Carry5, Carry20, Carry60, Carry120 on PDF page 265.
- For each block, Carver calculates a raw forecast, scales it to average absolute value 10, and caps it at absolute value 20 on PDF page 265.
- S11 first selects forecasting rules that do not exceed the pre-locked S09/S10 cost-speed eligibility threshold, using turnover tables and the instrument's risk-adjusted cost per trade on PDF pages 265-266. This brief carries 0.15 SR units as source context from S09, but the exact quote/page must be re-page-audited before implementation.
- Forecast weights use the top-down method: allocate by style, then trading rule, then rule variation on PDF page 266.
- Carver classifies trend as divergent and carry as convergent on PDF page 266.
- Carver uses a 60% trend and 40% carry split in the chapter, noting it is his own trading-system proportion and that other choices are possible on PDF pages 266-267.
- S11 includes worked source examples for top-down allocation across style, rule, and variation. The previously recorded Eurodollar-specific 30%/30% trend allocation is not treated as locked authority here; exact example rows and pages must be re-page-audited before implementation so they are not confused with later normalised-trend examples.
- Table 51 is recorded as the source table for forecast-weight examples, but its exact table number, rows, and page labels must be re-page-audited before implementation.
- Table 52 is recorded as the source table for approximate FDM values by number of trading rules, but its exact table number, rows, and page labels must be re-page-audited before implementation. Interpolation remains blocked unless separately operator-locked before data work.
- Once the combined forecast has the correct scale, Carver applies the usual procedure for capping, position sizing, and buffering on PDF page 270.
- S11 evaluates combined trend/carry against long-only, S09 trend, and S10 carry in the Jumbo portfolio, but this brief treats those results as source context only and not evidence or promotion on PDF pages 270-274.
- Carver concludes that S11 is the culmination of Part One and that Parts Two and Three can combine additional forecast strategies with S09, S10, and S11. Parts Four and Five do not fit this forecasting framework on PDF page 274.
- The S11 trading plan states that all other elements are identical to S09 and S10 on PDF page 275.

## Candidate Interpretation

S11 is admitted as:

```text
STANDALONE_CANDIDATE
```

S11 is the first complete combined-forecast family in the clean pipeline. It is not a deployment candidate, not a promotion artifact, and not evidence of alpha.

S11 should be used to lock these source-native primitives:

- Forecast-block compatibility across styles.
- Divergent/convergent style grouping.
- Trend building blocks inherited from S09.
- Carry building blocks inherited from S10.
- Style-level forecast weights.
- Rule-level and variation-level top-down weights.
- Trading-rule speed eligibility across trend and carry.
- Generic FDM table by number of rules.
- Combined forecast cap.
- Forecast-scaled position sizing inherited from S09/S10.
- Buffering inherited from the forecast machinery.

S11 must not tune the trend/carry mix, eligible rules, forecast weights, FDM, caps, buffers, cost thresholds, seasonal exceptions, instruments, or curve-leg choices after seeing results.

## Candidate Rule Skeleton

The S11 source rule skeleton is:

```text
For each eligible source-native futures instrument:
construct all eligible S09 trend forecasts and S10 carry forecasts from completed daily inputs,
drop any forecasting rule variation that fails the pre-locked speed/cost rule,
allocate source-locked style weights between divergent trend and convergent carry,
allocate within each style, rule, and rule variation using the locked top-down method,
combine capped forecasts using the locked forecast weights,
apply the locked FDM for the number of remaining trading rules,
cap the combined forecast,
calculate the forecast-scaled optimal position using inherited sizing,
apply the locked buffer rule,
leave any portfolio aggregation and cost accounting to a separately authorized child lane.
```

No live rule, code rule, executable rule, test rule, diagnostic rule, backtest rule, OOS rule, Lockbox rule, Forward rule, or promotion rule is authorized by this skeleton.

## Source Forecast Parameters

S11 source parameters to lock before data work:

| Item | Source value | Source |
| --- | --- | --- |
| Trend style | Divergent | PDF page 266 |
| Carry style | Convergent | PDF page 266 |
| Source style mix | 60% trend, 40% carry | PDF pages 266-267 |
| Speed limit | Pre-locked S09/S10 cost-speed eligibility threshold; 0.15 SR units carried as source context pending exact quote/page re-audit | PDF pages 265-266 plus S09 source pages, pending re-page audit |
| Trend variations | EWMAC2, 4, 8, 16, 32, 64 | PDF page 265 |
| Carry variations | Carry5, 20, 60, 120 | PDF page 265 |
| Forecast scaling | Average absolute value 10 | PDF page 265 |
| Individual forecast cap | Absolute value 20 | PDF page 265 |
| Combined forecast cap | Usual cap after FDM | PDF page 270, inherited S09 pages 221-222 |

Table 51 is recorded as the source forecast-weight example table for eligible rule sets, and Table 52 is recorded as the approximate FDM table by number of trading rules. Their exact table numbers, rows, and page labels must be re-page-audited before implementation. Carver's interpolation language also requires a separate operator lock before data work. These tables are source parameters for process locking only. This brief does not authorize recomputation, optimization, data inspection, or backtesting.

## Inherited Machinery

S11 inherits:

- M0 source-native futures defaults and non-authorization.
- S01 futures identity, roll, back-adjustment, multiplier, FX, and cost atoms.
- S02 target-risk position sizing and whole-contract rounding.
- S03 variable risk estimation, non-leaking risk rule, and risk-adjusted cost atoms.
- S04 instrument weights, IDM, portfolio breadth, and multi-instrument aggregation atoms.
- S09 EWMAC trend forecasts, forecast scalars, speed eligibility, forecast weights, FDM, caps, forecast-scaled sizing, and buffer discipline.
- S10 carry curve construction, smoothing spans, carry scalar, carry FDM, seasonal/wrong-sign blockage, and curve-data atoms.

S11 does not authorize recalculating any inherited atom from data.

## Required Atoms Before Data Work

S11 cannot proceed to data work until all inherited atoms and these S11-specific atoms are locked:

- Exact source-native instrument universe for any S11 candidate or portfolio child.
- Exact local symbol mapping for every instrument and every carry curve contract needed.
- Exchange session, timezone, completed daily bar close, holiday calendar, and daily candle cut for every instrument and curve contract.
- Completed-bar synchronization rule across price, trend, and carry inputs.
- S09 trend forecast atom lock for every instrument.
- S10 carry forecast atom lock for every instrument.
- Rule for instruments where no eligible trend variation remains.
- Rule for instruments where no eligible carry variation remains.
- Rule for instruments where one style is unavailable but the other style is available.
- Source style mix: 60/40 or documented operator/source blockage.
- Top-down style/rule/variation forecast-weight construction.
- Table 51 row-selection rule or documented blockage.
- Table 51 exact table-number/page-label verification.
- Table 52 FDM row-selection rule by number of remaining rules.
- Table 52 exact table-number/page-label verification.
- Whether Table 52 interpolation is allowed or explicitly blocked.
- Combined forecast cap after FDM.
- Forecast-scaled position sizing formula.
- Buffer zone rule inherited from forecast machinery.
- Instrument weights and IDM if running a multi-instrument S11 portfolio.
- Portfolio aggregation convention if running a portfolio child.
- Cost source in `config/costs.json` once authorized.
- Prohibition on post-result mix, rule, weight, FDM, cap, buffer, cost-threshold, curve-leg, seasonal, or instrument tuning.
- Evidence-window budget if a future diagnostic/backtest is requested.

## Locked Process Decisions

The following process decisions are locked by this brief:

- S11 remains process-only until separately authorized.
- S11 is `SOURCE_NATIVE_FUTURES`, not CFD.
- S11 is a daily directional combined-forecast strategy.
- S11 uses completed daily bars only.
- S11 is a `STANDALONE_CANDIDATE` at the combined trend/carry family level.
- S11 does not authorize P07 Jumbo combined trend/carry portfolio.
- S11 does not authorize Part Two, Part Three, Part Four, or Part Five.
- S11 does not authorize local data inspection, implementation, tests, diagnostics, or backtests.
- S11 must prefer native daily futures candles when a future data lane is authorized.
- S11 must not reconstruct daily bars from 1-minute data by default.
- S11 must not use old QuantLab data-prep scripts, CFD adapters, broker-clock assumptions, or stale state.
- S11 must not select, drop, rescue, or reweight styles, rules, variations, or instruments after seeing results.
- S11 must not treat historical performance as promotion evidence.
- A non-positive future S11 result does not advance and must not be rescued by tuning.

## Explicitly Unresolved

The following remain unresolved and block data/implementation work:

- Exact source-native instrument universe.
- Exact local symbol mapping for every instrument and every carry curve contract needed.
- Exchange session, timezone, completed daily bar close, holiday calendar, and daily candle cut for every instrument and curve contract.
- Completed-bar synchronization rule across price, trend, and carry inputs.
- S09 trend forecast atom lock for every instrument.
- S10 carry forecast atom lock for every instrument.
- Rule for instruments where no eligible trend variation remains.
- Rule for instruments where no eligible carry variation remains.
- Rule for instruments where one style is unavailable but the other style is available.
- Source style mix lock.
- Top-down style/rule/variation forecast-weight construction.
- Table 51 row-selection rule.
- Table 51 exact table-number/page-label verification.
- Table 52 FDM row-selection rule by number of remaining rules.
- Table 52 exact table-number/page-label verification.
- Whether Table 52 interpolation is allowed or explicitly blocked.
- Combined forecast cap after FDM.
- Forecast-scaled position sizing formula.
- Buffer zone rule inherited from forecast machinery.
- Instrument weights and IDM if running a multi-instrument S11 portfolio.
- Portfolio aggregation convention if running a portfolio child.
- Exact cost source in `config/costs.json`.
- Fail-closed behavior for missing or invalid prices, rolls, expiries, curve contracts, multipliers, FX, risk estimates, costs, speed eligibility, forecast scalars, FDM, buffers, style weights, or sizing inputs.
- Evidence-window budget if a future diagnostic/backtest is requested.
- Exact synthetic conformance examples for later implementation testing.
- Whether any book numeric examples are sufficient for source-example conformance tests.

## Forbidden Work

This brief authorizes none of the following:

- Data export.
- Market-row parsing.
- NinjaTrader export or subscription work.
- NinjaTrader brokerage/account/credential/order-routing setup.
- Implementation.
- Unit tests.
- Synthetic tests.
- Diagnostics.
- Backtests.
- OOS, Lockbox, or Forward access.
- CFD adapter work.
- Old adapter import.
- Tuning.
- Deployment.
- Trading.
- Promotion.

## Hostile Audit Requirement

Before this S11 brief is treated as process-safe, it must receive a hostile audit by subagent.

Audit focus:

- M0, S01, S02, S03, S04, P01, P02, S09, and S10 inheritance.
- Source-page faithfulness.
- No data or implementation leakage.
- No backtest or evidence leakage.
- No NinjaTrader operational leakage.
- No CFD or old QuantLab contamination.
- Correct `STANDALONE_CANDIDATE` interpretation for the S11 combined trend/carry family.
- Correct separation from P07 and later book parts.
- No style mix, rule, weight, FDM, cap, buffer, threshold, curve-leg, seasonal, or instrument tuning after results.
- Completeness of combined-forecast and unresolved atoms.

## Next Gate

If this S11 brief is accepted after hostile audit, the next possible process-only gate is not pre-authorized by this brief.

The likely next clean architecture step is a shared module consolidation memo for M1/M2/M3/M5, but that requires separate operator authorization.

## Standing Non-Authorization

This file authorizes no data access, no market-row parsing, no implementation, no tests, no diagnostics, no backtests, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old-adapter import, no tuning, no deployment, no trading, and no promotion.
