# Carver S03 Buy And Hold With Variable Risk Scaling Candidate Brief

Date: 2026-05-28

Status:

```text
PROCESS_ONLY_CARVER_S03_BUY_AND_HOLD_WITH_VARIABLE_RISK_SCALING_BRIEF_DRAFT_NOT_DATA_NOT_STRATEGY_AUTHORIZATION
```

## Purpose

Create the process-only source-native futures candidate brief for Carver Strategy 3:

```text
S03_BUY_AND_HOLD_WITH_VARIABLE_RISK_SCALING
```

This brief inherits M0, S01, and S02. It records the source framing, classification, dependencies, locked process atoms, unresolved atoms, and next gates before any data work or implementation.

This brief is not a data lane, implementation lane, test lane, diagnostic lane, backtest lane, OOS lane, Lockbox lane, Forward lane, CFD adapter lane, deployment lane, trading lane, or promotion lane.

## Classification

| Field | Value |
| --- | --- |
| Strategy ID | S03 |
| Book strategy | Strategy three: Buy and hold, with positions scaled for variable risk |
| Book pages | `Carver.pdf`, PDF pages 93-117 |
| Lane class | `SOURCE_NATIVE_FUTURES` |
| Strategy label | `STANDALONE_CANDIDATE` |
| Timeframe family | Daily directional stack |
| Data posture | No data access authorized |
| Implementation posture | No implementation authorized |
| Evidence posture | No diagnostics or backtests authorized |

## Dependencies

S03 depends on:

- `docs/process/CARVER_M0_SOURCE_NATIVE_FUTURES_FOUNDATION_SPEC_2026-05-28.md`
- `docs/process/CARVER_LEAN_IMPLEMENTATION_AND_BACKTEST_DEFERRAL_RULE_2026-05-28.md`
- `docs/process/CARVER_SOURCE_NATIVE_TRANSLATION_ARCHITECTURE_GOAL_2026-05-28.md`
- `docs/researchops/handoffs/CARVER_BOOK_STRATEGY_AND_PORTFOLIO_INVENTORY_001_2026-05-28.md`
- `docs/researchops/candidates/CARVER_S01_BUY_AND_HOLD_SINGLE_CONTRACT_CANDIDATE_BRIEF_2026-05-28.md`
- `docs/researchops/candidates/CARVER_S02_BUY_AND_HOLD_WITH_RISK_SCALING_CANDIDATE_BRIEF_2026-05-28.md`

S03 is a prerequisite for:

- S04 buy-and-hold portfolio with variable risk position sizing.
- M1 position sizing and risk-scaling work once separately authorized.
- Later daily directional strategies that inherit Carver's variable-risk position sizing.
- Early portfolio examples that use S03-style variable risk scaling.

## Book Framing

Carver frames S03 as the fix for S02's fixed risk estimate. S02 hits the target risk only on average; S03 updates position size when recent volatility changes.

Source anchors:

- S03 starts as "Buy and hold with variable risk scaling" on `Carver.pdf`, PDF page 93.
- The chapter motivates S03 by showing that S02's realised risk varies materially through time, including calm periods and crisis periods, on PDF pages 93-94.
- Carver says recent volatility is relatively forecastable because volatility clusters, and that recent standard deviation over roughly the last month can forecast near-term risk on PDF pages 94-95.
- The chapter introduces moving-window standard deviation and notes that percentage risk is annualised, while daily price-point risk uses price changes without annualising the same way, on PDF page 95.
- Carver rejects a simple one-month window as noisy and chooses an exponentially weighted standard deviation to smooth estimates and reduce trading costs on PDF pages 95-96.
- Carver states that an EWMA with span 32 days is equivalent to about a one-month simple window and corresponds to lambda/alpha about 0.06061 on PDF page 97.
- From this point onward, Carver uses a blended volatility estimate: long-run volatility weight 0.3 and short-run exponentially weighted volatility weight 0.7, with span 32 days and half-life about 11 days. See `Carver.pdf`, PDF page 97.
- S03 uses the S02 position-sizing formula but replaces the fixed instrument risk with the variable standard-deviation estimate on PDF page 98.
- Variable risk scaling cuts positions when volatility rises and increases positions when volatility falls; the S&P 500 example cuts position sharply during 1987 despite the price fall on PDF pages 98-99.
- S03 introduces risk-adjusted costs as cost divided by annualised risk, expressed in Sharpe-ratio units, on PDF pages 99-102.
- The chapter separates holding/roll costs from other trading costs and defines annual turnover as the number of times average position is traded, excluding rolls, on PDF pages 102-103.
- Carver notes cost estimates should use current commissions and spreads and should be recalculated before trading, on PDF pages 104-105.
- Strategy three reduces fat tails and improves risk targeting versus S02, but does not produce a decisive performance boost on the S&P 500 example, on PDF pages 105-109.
- Carver warns that the 20% risk target may be too high for S03 if expected Sharpe ratios are below 0.40, and that S03 is mainly educational for many traders on PDF pages 109-110.
- For instrument choice, Carver emphasizes minimum capital, costs, and liquidity, while warning that historical Sharpe differences across instruments are not statistically reliable enough for selection on PDF pages 110-112.
- Carver introduces the trading speed limit: do not spend more than about one third of expected pre-cost Sharpe on costs; for S03 this implies excluding instruments with risk-adjusted cost per trade greater than about 0.01 SR units, on PDF page 112.
- Carver uses liquidity checks based on average volume in the most active expiry and daily volume in risk terms, with example thresholds of 100 contracts per day and USD 1.25 million per day in risk terms, on PDF pages 113-114.
- When choosing between S&P 500 e-mini and micro e-mini futures, Carver recommends the micro because costs and liquidity are similar while the micro gives more granular positions and lower minimum capital, on PDF page 114.
- The S03 trading plan states that all other elements are identical to S02, on PDF page 115.

## Candidate Interpretation

S03 is admitted as:

```text
STANDALONE_CANDIDATE
```

Its clean first role is to lock Carver's reusable variable-risk position-sizing machinery. It is still not a preferred final system, not a portfolio, and not alpha promotion.

S03 should be used to lock these source-native primitives:

- Recent-volatility forecasting.
- Exponentially weighted volatility estimation.
- Long-run and short-run volatility blending.
- Daily risk-scaled position recomputation.
- Whole-contract rounding under changing risk.
- Risk-adjusted cost calculation.
- Roll versus non-roll turnover treatment.
- Trading speed-limit eligibility.
- Liquidity and minimum-capital eligibility.
- Instrument-size choice where micro, mini, and full-size contracts exist.

S03 must not use historical best-instrument selection as strategy status. Instrument choice must be governed by source-native identity, minimum capital, cost, liquidity, and pre-locked eligibility rules.

## Candidate Rule Skeleton

The S03 source rule skeleton is:

```text
For one source-native futures instrument:
hold a long buy-and-hold exposure,
estimate current instrument risk from completed daily returns using the locked variable-risk method,
blend long-run and short-run risk according to the locked source rule,
calculate the desired contract count from capital, target risk, current variable risk,
current held-contract price, futures multiplier, and FX conversion,
round to a whole-contract position,
roll according to the locked source-native roll rule,
calculate PnL from completed daily back-adjusted price changes and the actual held position,
account for costs separately once a cost source is authorized.
```

No live rule, code rule, executable rule, test rule, diagnostic rule, or backtest rule is authorized by this skeleton.

## M0, S01, And S02 Inheritance

S03 inherits these M0 defaults:

- Lane class: `SOURCE_NATIVE_FUTURES`.
- Local data surface candidate: `NINJATRADER_SOURCE_NATIVE_FUTURES_DATA_SURFACE_CANDIDATE`.
- Local native timeframe first.
- Completed daily bars for the daily directional stack.
- No NinjaTrader export, parsing, subscription, brokerage connection, credential handling, order routing, or trading integration.
- No CFD adapter.
- No old QuantLab active authority.
- No implementation without separate implementation authorization.
- Synthetic/source-conformance tests only after a separate implementation authorization.
- No historical diagnostics or backtests without separate operator authorization.

S03 inherits these S01 primitives:

- Exact source-native instrument identity must be locked.
- Continuous-contract construction and roll rule must be locked.
- Back-adjusted price is the excess-return PnL input.
- Futures multiplier, tick size, tick value, instrument currency, base currency, and FX treatment must be locked.
- Costs remain separate and must come from an authorized cost source.
- Missing or invalid source atoms fail closed.

S03 inherits these S02 primitives:

- Available capital before position size.
- Target risk on capital.
- Current held-contract raw price for sizing.
- Daily optimal-position recomputation.
- Whole-contract rounding.
- Minimum capital and indivisibility constraints.
- Non-leaking risk-estimate rule for any future implementation.

S03 replaces S02's fixed risk input with a variable risk estimate. It does not open S04 portfolio construction.

## Preferred Initial Source Instrument

The book teaching example remains the S&P 500 micro future:

| Field | Candidate value |
| --- | --- |
| Instrument | S&P 500 micro future |
| Book/Appendix C code | `MES` |
| Exchange | GLOBEX |
| Currency | USD |
| Multiplier | 5 |
| Appendix C dataset first year | 1982, not necessarily actual MES trading history |
| Source page | `Carver.pdf`, PDF page 692 |

This is a source-preferred teaching candidate only. No data access is authorized.

As in S01 and S02, the Appendix C first-year field must not be treated as proof of actual MES trading history. Any future data lane must lock whether and how continuous history is represented. No backfill, substitution, or contract-size bridge is authorized by this brief.

## Required Atoms Before Data Work

S03 cannot proceed to data work until all S01 and S02 atoms and these S03-specific atoms are locked:

- Exact source-native instrument identity.
- Whether the initial instrument is `MES`, another S&P 500 futures contract, or a documented source-native historical bridge.
- Native data surface and native daily timeframe.
- Exchange session definition.
- Timezone.
- Completed daily bar close timestamp.
- Holiday calendar.
- Daily candle cut convention.
- Continuous-contract construction.
- Contract selection and roll rule.
- Back-adjustment method for PnL.
- Current held-contract raw price used for sizing.
- Treatment of raw futures price versus adjusted futures price.
- Futures multiplier.
- Tick size and tick value.
- Instrument currency and base/account currency.
- FX conversion rule and timestamp convention.
- Percentage-risk versus daily-price-point sizing form.
- Daily return or daily price-change construction used for variable risk.
- EWMA span and lambda/alpha convention.
- Long-run volatility definition.
- Short-run volatility definition.
- Long-run and short-run blend weights.
- Warm-up period and first usable date after volatility estimation.
- Treatment of missing returns, stale prices, gaps, limit moves, and zero or invalid volatility.
- Non-leaking rule for any risk estimate used outside a pure book-example conformance check.
- Requirement that any future risk estimate use only returns completed before the sizing timestamp.
- Annualisation convention.
- Target risk.
- Margin source used for target-risk constraint.
- Prudent crash-loss assumption used for target-risk constraint.
- Personal or operator risk-appetite assumption used for target-risk constraint.
- Expected Sharpe/Kelly assumption used for target-risk constraint.
- Capital base for position sizing.
- Fixed-capital versus current-account-value convention for future testing or operation.
- Contract-count rounding rule.
- Trade trigger rule after rounding.
- Minimum capital rule.
- Minimum starting contract-count policy.
- Cost source in `config/costs.json` once authorized.
- Spread, tick, commission, and market-impact policy.
- Risk-adjusted cost per trade definition.
- Roll frequency and roll-cost convention.
- Non-roll turnover definition.
- Trading speed-limit threshold.
- Instrument liquidity thresholds in contract-volume and risk-volume terms.
- Instrument-size selection rule when micro, mini, and full-size alternatives exist.
- Prohibition on post-result best-instrument selection or rescue.
- Evidence-window budget if a future diagnostic/backtest is requested.

## Locked Process Decisions

The following process decisions are locked by this brief:

- S03 remains process-only until separately authorized.
- S03 is `SOURCE_NATIVE_FUTURES`, not CFD.
- S03 is a daily directional-stack candidate.
- S03 uses completed daily bars only.
- S03 inherits S01 futures identity, roll, back-adjustment, multiplier, FX, and cost atoms.
- S03 inherits S02 target-risk position sizing and whole-contract rounding.
- S03 adds variable risk estimation and risk-adjusted cost atoms.
- S03 does not authorize S04 multi-instrument portfolio construction.
- S03 must prefer native daily futures candles when a future data lane is authorized.
- S03 must not reconstruct daily bars from 1-minute data by default.
- S03 must not use old QuantLab data-prep scripts, CFD adapters, broker-clock assumptions, or stale state.
- S03 must not select a best instrument after seeing historical performance.
- S03 must not treat historical performance as promotion evidence.
- A non-positive future S03 standalone result does not advance and must not be rescued by tuning.

## Explicitly Unresolved

The following remain unresolved and block data/implementation work:

- Exact source-native instrument identity.
- Whether the initial instrument is `MES`, another S&P 500 futures contract, or a documented source-native historical bridge.
- Exact source-native data source acceptance.
- Exact NinjaTrader symbol mapping.
- Exchange session definition.
- Timezone.
- Completed daily bar close timestamp.
- Holiday calendar.
- Daily candle cut convention.
- Exact roll calendar and roll timing.
- Exact continuous-contract/back-adjustment construction.
- Treatment of raw futures price versus adjusted futures price.
- Current held-contract raw price source for sizing.
- Futures multiplier.
- Tick size and tick value.
- Instrument currency and base/account currency.
- Exact FX conversion handling.
- Percentage-risk versus daily-price-point sizing form.
- Daily return or daily price-change construction used for variable risk.
- Exact EWMA span and lambda/alpha convention.
- Exact long-run volatility definition.
- Exact short-run volatility definition.
- Exact long-run and short-run blend weights.
- Warm-up period and first usable date after volatility estimation.
- Treatment of missing returns, stale prices, gaps, limit moves, and zero or invalid volatility.
- Non-leaking rule for any risk estimate used outside a pure book-example conformance check.
- Requirement that any future risk estimate use only returns completed before the sizing timestamp.
- Annualisation convention.
- Exact target risk.
- Margin source used for target-risk constraint.
- Prudent crash-loss assumption used for target-risk constraint.
- Personal or operator risk-appetite assumption used for target-risk constraint.
- Expected Sharpe/Kelly assumption used for target-risk constraint.
- Exact capital base for position sizing.
- Fixed-capital versus current-account-value convention for future testing or operation.
- Exact contract-count rounding rule.
- Trade trigger rule after rounding.
- Minimum capital rule.
- Minimum starting contract-count policy.
- Exact cost source in `config/costs.json`.
- Spread, tick, commission, and market-impact policy.
- Risk-adjusted cost per trade definition.
- Roll frequency and roll-cost convention.
- Non-roll turnover definition.
- Trading speed-limit threshold.
- Instrument liquidity thresholds in contract-volume and risk-volume terms.
- Instrument-size selection rule when micro, mini, and full-size alternatives exist.
- Fail-closed behavior for missing or invalid prices, rolls, multipliers, FX, risk estimates, costs, liquidity, or sizing inputs.
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

Before this S03 brief is treated as process-safe, it must receive a hostile audit by subagent.

Audit focus:

- M0 inheritance.
- S01 and S02 inheritance.
- Source-page faithfulness.
- No data or implementation leakage.
- No backtest or evidence leakage.
- No NinjaTrader operational leakage.
- No CFD or old QuantLab contamination.
- Correct `STANDALONE_CANDIDATE` interpretation.
- Correct separation from S04 portfolio construction.
- No historical best-instrument selection leakage.
- Completeness of unresolved atoms.

## Next Gate

If this S03 brief is accepted after hostile audit, the next possible process-only gate is:

```text
PROCESS_ONLY_CARVER_S04_BUY_AND_HOLD_PORTFOLIO_WITH_VARIABLE_RISK_POSITION_SIZING_BRIEF_DRAFT_NOT_DATA_NOT_STRATEGY_AUTHORIZATION
```

No S04 work is authorized by this S03 brief.

## Standing Non-Authorization

This file authorizes no data access, no market-row parsing, no implementation, no tests, no diagnostics, no backtests, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old-adapter import, no tuning, no deployment, no trading, and no promotion.
