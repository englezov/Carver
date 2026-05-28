# Carver S09 Multiple Trend Following Candidate Brief

Date: 2026-05-28

Status:

```text
PROCESS_ONLY_CARVER_S09_MULTIPLE_TREND_FOLLOWING_BRIEF_DRAFT_NOT_DATA_NOT_STRATEGY_AUTHORIZATION
```

## Purpose

Create the process-only source-native futures candidate brief for Carver Strategy 9:

```text
S09_MULTIPLE_TREND_FOLLOWING
```

This brief inherits M0, S01, S02, S03, S04, P01, and P02. It records the source framing, classification, dependencies, locked process atoms, unresolved atoms, and next gates before any data work or implementation.

This brief is not a data lane, implementation lane, test lane, diagnostic lane, backtest lane, OOS lane, Lockbox lane, Forward lane, CFD adapter lane, deployment lane, trading lane, or promotion lane.

## Classification

| Field | Value |
| --- | --- |
| Strategy ID | S09 |
| Book strategy | Strategy nine: Multiple trend following rules |
| Book pages | `Carver.pdf`, PDF pages 201-227 |
| Lane class | `SOURCE_NATIVE_FUTURES` |
| Strategy label | `STANDALONE_CANDIDATE` |
| Timeframe family | Daily directional forecast stack |
| Data posture | No data access authorized |
| Implementation posture | No implementation authorized |
| Evidence posture | No diagnostics or backtests authorized |

## Dependencies

S09 depends on:

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

S09 also depends on source mechanics introduced before S09:

- S07 slow trend with trend strength: used as EWMAC64.
- S08 fast trend with trend strength: used as EWMAC16.

S07 and S08 are not advanced as standalone candidates by this S09 brief. They are admitted only as source components inside the multiple-trend family unless separately authorized.

S09 is a prerequisite for:

- S11 combined trend and carry.
- P05 Jumbo multiple trend portfolio.
- P07 Jumbo combined trend/carry portfolio.
- Later forecast-block machinery that uses forecast weights, FDM, forecast caps, and buffered position sizing.

## Book Framing

Carver frames S09 as the first core multiple-forecast trend-following strategy. Instead of choosing a single trend speed, S09 combines several EWMAC trend filters to diversify across trend horizons.

Source anchors:

- S09 starts as "Multiple trend following rules" on `Carver.pdf`, PDF page 201.
- Carver motivates S09 by noting that diversifying across uncorrelated trading strategies can improve performance, just as S04 diversifies across instruments, on PDF page 201.
- The chapter defines S09 as trading one or more instruments with variable-risk position sizing, calculating forecasts for different speeds of trend filter, and placing positions from the combined forecast on PDF pages 201-202.
- The selected EWMAC filter set is EWMAC64, EWMAC32, EWMAC16, EWMAC8, EWMAC4, and EWMAC2, where EWMACn means EWMAC(n, 4n), on PDF pages 202-203.
- Carver excludes EWMAC1 as too expensive for almost all futures instruments and avoids filters slower than EWMAC64 because they become too correlated with long-only exposure and trade too rarely for evaluation on PDF pages 202-203.
- S09 uses the same position sizing and management rules as S08: raw crossover, risk-normalised forecast, forecast scalar, forecast cap, optimal risk-adjusted unrounded position, buffer zone, and trade/no-trade decision on PDF page 203.
- Table 29 gives forecast scalars for the six EWMAC speeds on PDF page 204.
- Carver says the same volatility estimate can be used across trend speeds, but the S09 text references an estimate around 30 to 35 days while S03 locked span 32; this must be reconciled before implementation. See `Carver.pdf`, PDF pages 204-205 and S03 source pages 95-97.
- S09 combines capped forecasts by weighted average, using forecast weights that sum to 1 and are non-negative on PDF pages 208-209.
- Carver prefers averaging capped forecasts rather than raw forecasts or independent systems, because capped averaging avoids one extreme filter dominating the combined forecast and allows netting on PDF page 208.
- Forecast weights depend on expected pre-cost performance, trading costs, and diversification/correlation, but Carver warns against overfitting and against using the single best filter on PDF pages 209-215.
- For S09, Carver removes trading rules that are too expensive for a given instrument and then allocates equal forecast weights across the remaining trend variations using a top-down method on PDF pages 215-220.
- Carver applies a trading-rule cost/speed eligibility rule when deciding which EWMAC variations are cheap enough for an instrument. This brief records 0.15 SR units as source context, but the exact quote and page reference must be re-page-audited before implementation. See PDF pages 216-218 and the general cost-speed rule on PDF page 112.
- Table 35 gives annual turnover estimates for each trend filter: EWMAC2 98.5, EWMAC4 50.2, EWMAC8 25.4, EWMAC16 13.2, EWMAC32 7.6, and EWMAC64 5.2 on PDF pages 217-218.
- Table 36 gives forecast weights and forecast diversification multiplier (`FDM`) for each allowed set of trend filters on PDF page 221.
- Carver applies FDM to the combined forecast and then caps the combined forecast again at plus/minus 20 before position sizing on PDF pages 221-222.
- S09's performance discussion says multiple trend improves on individual trend filters in aggregate, but also warns against declaring trend following dead from losing years and points toward diversifying beyond trend in S10 on PDF pages 222-227.
- The S09 trading plan states that all other elements are identical to S08 on PDF page 227.

## Candidate Interpretation

S09 is admitted as:

```text
STANDALONE_CANDIDATE
```

S09 is the first major source-native trend-following alpha family in the clean pipeline. It is not a deployment candidate, not a promotion artifact, and not evidence of alpha.

S09 should be used to lock these source-native primitives:

- EWMAC forecast construction.
- Multiple trend speed set.
- Forecast scalars.
- Forecast capping.
- Forecast weights.
- Trading-rule cost eligibility.
- Forecast diversification multiplier.
- Combined forecast cap.
- Forecast-scaled position sizing.
- Buffering and trade/no-trade decision inherited from the prior trend machinery.
- Separation between trend component sleeves and the combined S09 family.

S09 must not tune filter speeds, forecast weights, FDM, caps, buffers, cost thresholds, or eligible instruments after seeing results.

## Candidate Rule Skeleton

The S09 source rule skeleton is:

```text
For each eligible source-native futures instrument:
construct the allowed EWMAC trend forecasts from completed daily prices,
scale and cap each individual forecast according to locked source rules,
drop any trend speed that fails the pre-locked trading-rule cost rule,
assign equal forecast weights across remaining allowed trend speeds,
combine capped forecasts with those forecast weights,
apply the locked FDM for the allowed trend-speed set,
cap the combined forecast,
calculate the forecast-scaled optimal position using inherited S03/S04 sizing,
apply the locked buffer rule,
roll according to the locked source-native roll rule,
leave any portfolio aggregation and cost accounting to a separately authorized child lane.
```

No live rule, code rule, executable rule, test rule, diagnostic rule, backtest rule, OOS rule, Lockbox rule, Forward rule, or promotion rule is authorized by this skeleton.

## Source Forecast Parameters

S09 source parameters to lock before data work:

| Item | Source value | Source |
| --- | --- | --- |
| EWMAC speed set | 2, 4, 8, 16, 32, 64 where EWMACn = EWMAC(n, 4n) | PDF pages 202-203 |
| Forecast cap per filter | Absolute value 20 | PDF pages 203, 209 |
| Combined forecast cap | Absolute value 20 after FDM | PDF pages 221-222 |
| Trading-rule speed limit | 0.15 SR units recorded as source context; exact quote/page must be re-page-audited before implementation | PDF pages 216-218 pending re-page audit; general cost-speed rule on PDF page 112 |
| Forecast-weight method | Equal weights across remaining cheap-enough trend variations | PDF pages 215-220 |

Forecast scalars from Table 29:

| Filter | Scalar |
| --- | ---: |
| EWMAC2 | 12.1 |
| EWMAC4 | 8.53 |
| EWMAC8 | 5.95 |
| EWMAC16 | 4.10 |
| EWMAC32 | 2.79 |
| EWMAC64 | 1.91 |

Turnover estimates from Table 35:

| Filter | Turnover per year |
| --- | ---: |
| EWMAC2 | 98.5 |
| EWMAC4 | 50.2 |
| EWMAC8 | 25.4 |
| EWMAC16 | 13.2 |
| EWMAC32 | 7.6 |
| EWMAC64 | 5.2 |

FDM source rows from Table 36:

| Allowed filters | Forecast weight per filter | FDM |
| --- | ---: | ---: |
| EWMAC2, 4, 8, 16, 32, 64 | 0.167 | 1.26 |
| EWMAC4, 8, 16, 32, 64 | 0.2 | 1.19 |
| EWMAC8, 16, 32, 64 | 0.25 | 1.13 |
| EWMAC16, 32, 64 | 0.333 | 1.08 |
| EWMAC32, 64 | 0.50 | 1.03 |
| EWMAC64 | 1.0 | 1.0 |

These values are source parameters for process locking only. This brief does not authorize recomputation, optimization, data inspection, or backtesting.

## Inherited Machinery

S09 inherits:

- M0 source-native futures defaults and non-authorization.
- S01 futures identity, roll, back-adjustment, multiplier, FX, and cost atoms.
- S02 target-risk position sizing and whole-contract rounding.
- S03 variable risk estimation, non-leaking risk rule, and risk-adjusted cost atoms.
- S04 instrument weights, IDM, portfolio breadth, and multi-instrument aggregation atoms.
- P01/P02 complete-portfolio reconstruction discipline where S09 later feeds portfolio work.

S09 does not authorize recalculating any inherited atom from data.

## Required Atoms Before Data Work

S09 cannot proceed to data work until all inherited atoms and these S09-specific atoms are locked:

- Exact source-native instrument universe for any S09 candidate or portfolio child.
- Exact local symbol mapping for every instrument.
- Exchange session, timezone, completed daily bar close, holiday calendar, and daily candle cut for every instrument.
- Continuous-contract construction and roll rule per instrument.
- Back-adjustment method per instrument.
- Raw price versus adjusted price convention for EWMAC and PnL.
- Current held-contract raw price source for sizing.
- Variable risk estimate per instrument using only returns completed before each sizing timestamp.
- Reconciliation of S03 span 32 versus S09 text around 30 to 35 days for the shared volatility estimate.
- EWMAC input price series.
- EWMA calculation convention and warm-up behavior.
- EWMAC speed set.
- Forecast scalar table.
- Individual forecast cap.
- Forecast-weight construction.
- Trading-rule speed-limit rule.
- Cost-per-trade source and risk-adjusted cost rule.
- Turnover table or separately locked source for speed eligibility.
- Rule for dropping too-expensive EWMAC variations per instrument.
- FDM lookup table and exact row-selection rule.
- Combined forecast cap after FDM.
- Forecast-scaled position sizing formula.
- Buffer zone rule inherited from S08/source trend machinery.
- Treatment of instruments with no eligible trend speed.
- Instrument weights and IDM if running a multi-instrument S09 portfolio.
- Portfolio aggregation convention if running a portfolio child.
- Cost source in `config/costs.json` once authorized.
- Prohibition on post-result filter-speed, weight, FDM, cap, buffer, cost-threshold, or instrument tuning.
- Evidence-window budget if a future diagnostic/backtest is requested.

## Locked Process Decisions

The following process decisions are locked by this brief:

- S09 remains process-only until separately authorized.
- S09 is `SOURCE_NATIVE_FUTURES`, not CFD.
- S09 is a daily directional forecast strategy.
- S09 uses completed daily bars only.
- S09 is a `STANDALONE_CANDIDATE` at the combined multiple-trend family level.
- S07 and S08 are not advanced as standalone candidates by this brief.
- S09 does not authorize S10 carry, S11 combined trend/carry, or P05 Jumbo multiple trend.
- S09 does not authorize local data inspection, implementation, tests, diagnostics, or backtests.
- S09 must prefer native daily futures candles when a future data lane is authorized.
- S09 must not reconstruct daily bars from 1-minute data by default.
- S09 must not use old QuantLab data-prep scripts, CFD adapters, broker-clock assumptions, or stale state.
- S09 must not select, drop, rescue, or reweight filters after seeing results.
- S09 must not treat historical performance as promotion evidence.
- A non-positive future S09 result does not advance and must not be rescued by tuning.

## Explicitly Unresolved

The following remain unresolved and block data/implementation work:

- Exact source-native instrument universe.
- Exact local symbol mapping for every instrument.
- Exchange session, timezone, completed daily bar close, holiday calendar, and daily candle cut for every instrument.
- Exact roll calendar and roll timing per instrument.
- Exact continuous-contract/back-adjustment construction per instrument.
- Raw price versus adjusted price convention for EWMAC and PnL.
- Current held-contract raw price source for sizing.
- Futures multiplier, tick size, tick value, instrument currency, base/account currency, and FX conversion per instrument.
- Variable risk estimate per instrument.
- Reconciliation of S03 span 32 versus S09 text around 30 to 35 days for the shared volatility estimate.
- EWMAC input price series.
- EWMA calculation convention and warm-up behavior.
- Exact EWMAC speed set lock.
- Exact forecast scalar table lock.
- Individual forecast cap lock.
- Forecast-weight construction lock.
- Trading-rule speed-limit rule lock.
- Cost-per-trade source and risk-adjusted cost rule.
- Turnover table or separately locked source for speed eligibility.
- Rule for dropping too-expensive EWMAC variations per instrument.
- FDM lookup table and exact row-selection rule.
- Combined forecast cap after FDM.
- Forecast-scaled position sizing formula.
- Buffer zone rule inherited from S08/source trend machinery.
- Treatment of instruments with no eligible trend speed.
- Instrument weights and IDM if running a multi-instrument S09 portfolio.
- Portfolio aggregation convention if running a portfolio child.
- Exact cost source in `config/costs.json`.
- Fail-closed behavior for missing or invalid prices, rolls, multipliers, FX, risk estimates, costs, speed eligibility, forecast scalars, FDM, buffers, or sizing inputs.
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

Before this S09 brief is treated as process-safe, it must receive a hostile audit by subagent.

Audit focus:

- M0, S01, S02, S03, S04, P01, and P02 inheritance.
- Source-page faithfulness.
- No data or implementation leakage.
- No backtest or evidence leakage.
- No NinjaTrader operational leakage.
- No CFD or old QuantLab contamination.
- Correct `STANDALONE_CANDIDATE` interpretation for the combined S09 family.
- Correct non-advancement of S07/S08 as standalone candidates.
- Correct separation from S10, S11, and P05.
- No filter, weight, FDM, cap, buffer, threshold, or instrument tuning after results.
- Completeness of unresolved atoms.

## Next Gate

If this S09 brief is accepted after hostile audit, the next possible process-only gate is:

```text
PROCESS_ONLY_CARVER_S10_BASIC_CARRY_CANDIDATE_BRIEF_DRAFT_NOT_DATA_NOT_STRATEGY_AUTHORIZATION
```

No S10 work is authorized by this S09 brief.

## Standing Non-Authorization

This file authorizes no data access, no market-row parsing, no implementation, no tests, no diagnostics, no backtests, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old-adapter import, no tuning, no deployment, no trading, and no promotion.
