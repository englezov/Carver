# Carver S10 Basic Carry Candidate Brief

Date: 2026-05-28

Status:

```text
PROCESS_ONLY_CARVER_S10_BASIC_CARRY_CANDIDATE_BRIEF_DRAFT_NOT_DATA_NOT_STRATEGY_AUTHORIZATION
```

## Purpose

Create the process-only source-native futures candidate brief for Carver Strategy 10:

```text
S10_BASIC_CARRY
```

This brief inherits M0, S01, S02, S03, S04, P01, P02, and S09. It records the source framing, classification, dependencies, locked process atoms, unresolved atoms, and next gates before any data work or implementation.

This brief is not a data lane, implementation lane, test lane, diagnostic lane, backtest lane, OOS lane, Lockbox lane, Forward lane, CFD adapter lane, deployment lane, trading lane, or promotion lane.

## Classification

| Field | Value |
| --- | --- |
| Strategy ID | S10 |
| Book strategy | Strategy ten: Basic carry |
| Book pages | `Carver.pdf`, PDF pages 232-260 |
| Lane class | `SOURCE_NATIVE_FUTURES` |
| Strategy label | `STANDALONE_CANDIDATE` |
| Timeframe family | Daily directional forecast stack |
| Data posture | No data access authorized |
| Implementation posture | No implementation authorized |
| Evidence posture | No diagnostics or backtests authorized |

## Dependencies

S10 depends on:

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

S10 is a prerequisite for:

- S11 combined carry and trend.
- P06 Jumbo carry portfolio.
- P07 Jumbo combined trend/carry portfolio.
- Later carry refinements, including accurate carry and cross-sectional carry, if separately authorized.

## Book Framing

Carver frames S10 as the first standalone carry strategy. Carry is a source of excess return distinct from trend, but potentially more hazardous and less positively skewed.

Source anchors:

- S10 starts as "Basic carry" on `Carver.pdf`, PDF page 232.
- Carver defines carry as the component of futures excess return over and above spot price changes on PDF pages 232-233.
- The chapter states that back-adjusted price incorporates both spot returns and carry, but carry can be predicted independently on PDF page 232.
- Carver describes asset-class carry sources: dividends minus funding for equities, bond yield minus repo for bonds, interest-rate differentials for FX, futures-curve convergence for STIR and volatility, storage/funding costs for metals, and convenience yield for other commodities on PDF pages 233-237.
- Carver warns that carry can look like free money but exposes the trader to spot drag and negative-skew risks on PDF page 237.
- Expected carry can be measured by comparing futures prices rather than requiring spot prices, using either a nearer contract or a further-out contract depending on what is held and available on PDF pages 238-239.
- Carver notes that daily closing futures prices for two contracts are synchronized because both contracts trade on the same exchange on PDF page 238.
- The raw carry price difference must be annualized using the time between expiries, approximated by month differences, on PDF page 240.
- Annualized carry is risk-adjusted by dividing by annualized standard deviation in price units, or equivalently by using percentage volatility and current price, on PDF pages 240-241.
- Carver treats risk-adjusted carry as a forecast because it is an expected annual return divided by annualized risk, equivalent to an expected Sharpe ratio, on PDF page 241.
- The chapter identifies sparse second-contract history, noisy curve differences, and poor data feeds as practical carry-estimation problems on PDF pages 242-243.
- Seasonal commodity, bond, and non-US equity carry issues are source concerns: Natural Gas seasonality may be real and measurable, while some Bund/Bobl/Bono and non-US equity front/second-contract estimates can have the wrong sign due to seasonal structure on PDF pages 243-246.
- To reduce noise and seasonal effects, Carver smooths carry forecasts with EWMA spans of 5, 20, 60, and 120 business days on PDF pages 246-247.
- Carver uses a single carry forecast scalar of 30 for all four carry variations, then caps forecasts, on PDF pages 247-248.
- Carry variations are selected by cost/speed eligibility, then combined with equal forecast weights across remaining eligible carry spans on PDF pages 248-253.
- Table 40 gives carry span turnover estimates: Carry5 5.75, Carry20 3.12, Carry60 1.82, Carry120 1.22 on PDF page 249.
- Table 45 gives carry FDM rows: Carry5/20/60/120 weight 0.25 FDM 1.04; Carry20/60/120 weight 0.333 FDM 1.03; Carry60/120 weight 0.5 FDM 1.02; Carry120 weight 1.0 FDM 1.0 on PDF page 253.
- Carver concludes that carry has decent but lower outright performance than trend, lower beta, mixed skew, and correlation of about 0.36 with S09 trend, motivating S11 combined trend/carry on PDF pages 257-259.
- The S10 trading-plan spillover states that all other elements are identical to S09 and that the optimal position is constructed and traded as required every day on PDF page 260.

## Candidate Interpretation

S10 is admitted as:

```text
STANDALONE_CANDIDATE
```

S10 is the first source-native carry forecast family in the clean pipeline. It is not a deployment candidate, not a promotion artifact, and not evidence of alpha.

S10 should be used to lock these source-native primitives:

- Futures-curve carry measurement.
- Held-contract versus nearer/further comparison rule.
- Expiry-distance annualization.
- Risk-adjusted carry as forecast.
- Carry forecast smoothing.
- Carry forecast scalar.
- Forecast cap.
- Carry span cost eligibility.
- Equal forecast weights across eligible carry spans.
- Carry FDM.
- Seasonal and wrong-sign carry blockages.
- Forecast-scaled position sizing inherited from S09.

S10 must not tune carry spans, forecast scalar, forecast weights, FDM, caps, cost thresholds, seasonal exceptions, instruments, or curve-leg choices after seeing results.

## Candidate Rule Skeleton

The S10 source rule skeleton is:

```text
For each eligible source-native futures instrument:
identify the held contract and comparison contract according to the locked source rule,
calculate raw carry from completed daily futures prices for synchronized contracts,
annualize raw carry using the locked expiry-distance convention,
risk-adjust annualized carry using the locked volatility estimate,
smooth carry forecasts across the locked Carry5/20/60/120 spans,
scale and cap each carry forecast according to locked source rules,
drop any carry span that fails the pre-locked trading-rule cost rule,
assign equal forecast weights across remaining allowed carry spans,
combine capped forecasts with those forecast weights,
apply the locked carry FDM for the allowed span set,
cap the combined forecast,
calculate the forecast-scaled optimal position using inherited sizing,
apply the locked buffer rule,
leave any portfolio aggregation and cost accounting to a separately authorized child lane.
```

No live rule, code rule, executable rule, test rule, diagnostic rule, backtest rule, OOS rule, Lockbox rule, Forward rule, or promotion rule is authorized by this skeleton.

## Source Forecast Parameters

S10 source parameters to lock before data work:

| Item | Source value | Source |
| --- | --- | --- |
| Carry spans | 5, 20, 60, 120 business days | PDF page 247 |
| Carry forecast scalar | 30 | PDF page 247 |
| Forecast cap per carry span | Absolute value 20 | PDF page 248 |
| Combined forecast cap | Absolute value 20 after FDM | inherited from S09 method on PDF pages 221-222; S10 FDM handoff on PDF page 253 |
| Forecast-weight method | Equal weights across remaining cheap-enough carry variations | PDF pages 248-253 |

Turnover estimates from Table 40:

| Carry span | Turnover per year |
| --- | ---: |
| Carry5 | 5.75 |
| Carry20 | 3.12 |
| Carry60 | 1.82 |
| Carry120 | 1.22 |

FDM source rows from Table 45:

| Allowed carry spans | Forecast weight per span | FDM |
| --- | ---: | ---: |
| Carry5, 20, 60, 120 | 0.25 | 1.04 |
| Carry20, 60, 120 | 0.333 | 1.03 |
| Carry60, 120 | 0.5 | 1.02 |
| Carry120 | 1.0 | 1.0 |

These values are source parameters for process locking only. This brief does not authorize recomputation, optimization, data inspection, or backtesting.

## Inherited Machinery

S10 inherits:

- M0 source-native futures defaults and non-authorization.
- S01 futures identity, roll, back-adjustment, multiplier, FX, and cost atoms.
- S02 target-risk position sizing and whole-contract rounding.
- S03 variable risk estimation, non-leaking risk rule, and risk-adjusted cost atoms.
- S04 instrument weights, IDM, portfolio breadth, and multi-instrument aggregation atoms.
- S09 forecast weights, FDM, forecast cap, forecast-scaled position sizing, speed eligibility, and buffer discipline.

S10 does not authorize recalculating any inherited atom from data.

## Required Atoms Before Data Work

S10 cannot proceed to data work until all inherited atoms and these S10-specific atoms are locked:

- Exact source-native instrument universe for any S10 candidate or portfolio child.
- Exact local symbol mapping for every instrument and every curve contract needed.
- Exchange session, timezone, completed daily bar close, holiday calendar, and daily candle cut for every contract.
- Completed-bar synchronization rule across held and comparison contracts.
- Held-contract selection rule per instrument.
- Comparison-contract selection rule: nearer contract, further-out contract, or documented blockage.
- Expiry calendar and month-distance convention.
- Rule for fixed-month commodities such as December WTI Crude, Wheat, or Corn where source requires it.
- Rule for instruments where only front contract is liquid and second contract is used for carry estimation.
- Rule for sparse second-contract history and roll-day-only carry estimates.
- Back-adjustment method for PnL and raw contract price source for carry.
- Raw price versus adjusted price convention for carry and PnL.
- Variable risk estimate in price units or equivalent percentage form.
- Annualization convention for raw carry.
- Risk-adjusted carry definition.
- Seasonal carry handling and fail-closed rules for known wrong-sign estimates.
- Carry span set.
- EWMA smoothing convention for carry spans.
- Carry forecast scalar.
- Individual forecast cap.
- Cost-per-trade source and risk-adjusted cost rule.
- Turnover table or separately locked source for carry span eligibility.
- Rule for dropping too-expensive carry spans per instrument.
- Forecast-weight construction.
- Carry FDM lookup table and exact row-selection rule.
- Combined forecast cap after FDM.
- Forecast-scaled position sizing formula.
- Buffer zone rule inherited from forecast machinery.
- Treatment of instruments with no eligible carry span or no usable curve data.
- Instrument weights and IDM if running a multi-instrument S10 portfolio.
- Portfolio aggregation convention if running a portfolio child.
- Cost source in `config/costs.json` once authorized.
- Prohibition on post-result span, scalar, weight, FDM, cap, buffer, cost-threshold, curve-leg, seasonal, or instrument tuning.
- Evidence-window budget if a future diagnostic/backtest is requested.

## Locked Process Decisions

The following process decisions are locked by this brief:

- S10 remains process-only until separately authorized.
- S10 is `SOURCE_NATIVE_FUTURES`, not CFD.
- S10 is a daily directional forecast strategy.
- S10 uses completed daily bars only.
- S10 is a `STANDALONE_CANDIDATE` at the basic carry family level.
- S10 does not authorize S11 combined trend/carry, S15 accurate carry, S20 cross-sectional carry, or P06 Jumbo carry.
- S10 does not authorize local data inspection, implementation, tests, diagnostics, or backtests.
- S10 must prefer native daily futures candles when a future data lane is authorized.
- S10 must not reconstruct daily bars from 1-minute data by default.
- S10 must not use old QuantLab data-prep scripts, CFD adapters, broker-clock assumptions, or stale state.
- S10 must not select, drop, rescue, or reweight carry spans or instruments after seeing results.
- S10 must not treat historical performance as promotion evidence.
- A non-positive future S10 result does not advance and must not be rescued by tuning.

## Explicitly Unresolved

The following remain unresolved and block data/implementation work:

- Exact source-native instrument universe.
- Exact local symbol mapping for every instrument and every curve contract needed.
- Exchange session, timezone, completed daily bar close, holiday calendar, and daily candle cut for every contract.
- Completed-bar synchronization rule across held and comparison contracts.
- Exact held-contract selection rule per instrument.
- Exact comparison-contract selection rule per instrument.
- Expiry calendar and month-distance convention.
- Fixed-month commodity rule where applicable.
- Sparse second-contract history rule.
- Exact continuous-contract/back-adjustment construction per instrument.
- Raw price versus adjusted price convention for carry and PnL.
- Variable risk estimate in price units or equivalent percentage form.
- Annualization convention for raw carry.
- Risk-adjusted carry definition.
- Seasonal carry handling and fail-closed rules for known wrong-sign estimates.
- Exact carry span set lock.
- EWMA smoothing convention for carry spans.
- Carry forecast scalar lock.
- Individual forecast cap lock.
- Cost-per-trade source and risk-adjusted cost rule.
- Turnover table or separately locked source for carry span eligibility.
- Rule for dropping too-expensive carry spans per instrument.
- Forecast-weight construction lock.
- Carry FDM lookup table and exact row-selection rule.
- Combined forecast cap after FDM.
- Forecast-scaled position sizing formula.
- Buffer zone rule inherited from forecast machinery.
- Treatment of instruments with no eligible carry span or no usable curve data.
- Instrument weights and IDM if running a multi-instrument S10 portfolio.
- Portfolio aggregation convention if running a portfolio child.
- Exact cost source in `config/costs.json`.
- Fail-closed behavior for missing or invalid prices, rolls, expiries, curve contracts, multipliers, FX, risk estimates, costs, speed eligibility, forecast scalar, FDM, buffers, or sizing inputs.
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

Before this S10 brief is treated as process-safe, it must receive a hostile audit by subagent.

Audit focus:

- M0, S01, S02, S03, S04, P01, P02, and S09 inheritance.
- Source-page faithfulness.
- No data or implementation leakage.
- No backtest or evidence leakage.
- No NinjaTrader operational leakage.
- No CFD or old QuantLab contamination.
- Correct `STANDALONE_CANDIDATE` interpretation for the S10 carry family.
- Correct separation from S11, S15, S20, and P06.
- No span, scalar, weight, FDM, cap, buffer, threshold, curve-leg, seasonal, or instrument tuning after results.
- Completeness of curve-data, carry-estimation, and unresolved atoms.

## Next Gate

If this S10 brief is accepted after hostile audit, the next possible process-only gate is:

```text
PROCESS_ONLY_CARVER_S11_COMBINED_CARRY_AND_TREND_CANDIDATE_BRIEF_DRAFT_NOT_DATA_NOT_STRATEGY_AUTHORIZATION
```

No S11 work is authorized by this S10 brief.

## Standing Non-Authorization

This file authorizes no data access, no market-row parsing, no implementation, no tests, no diagnostics, no backtests, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old-adapter import, no tuning, no deployment, no trading, and no promotion.
