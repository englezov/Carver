# Carver S02 Buy And Hold With Risk Scaling Candidate Brief

Date: 2026-05-28

Status:

```text
PROCESS_ONLY_CARVER_S02_BUY_AND_HOLD_WITH_RISK_SCALING_BRIEF_DRAFT_NOT_DATA_NOT_STRATEGY_AUTHORIZATION
```

## Purpose

Create the process-only source-native futures candidate brief for Carver Strategy 2:

```text
S02_BUY_AND_HOLD_WITH_RISK_SCALING
```

This brief inherits M0 and S01. It records the source framing, classification, dependencies, locked process atoms, unresolved atoms, and next gates before any data work or implementation.

This brief is not a data lane, implementation lane, test lane, diagnostic lane, backtest lane, OOS lane, Lockbox lane, Forward lane, CFD adapter lane, deployment lane, trading lane, or promotion lane.

## Classification

| Field | Value |
| --- | --- |
| Strategy ID | S02 |
| Book strategy | Strategy two: Buy and hold, with positions scaled for risk |
| Book pages | `Carver.pdf`, PDF pages 67-92 |
| Lane class | `SOURCE_NATIVE_FUTURES` |
| Strategy label | `STANDALONE_CANDIDATE` |
| Timeframe family | Daily directional stack |
| Data posture | No data access authorized |
| Implementation posture | No implementation authorized |
| Evidence posture | No diagnostics or backtests authorized |

## Dependencies

S02 depends on:

- `docs/process/CARVER_M0_SOURCE_NATIVE_FUTURES_FOUNDATION_SPEC_2026-05-28.md`
- `docs/process/CARVER_LEAN_IMPLEMENTATION_AND_BACKTEST_DEFERRAL_RULE_2026-05-28.md`
- `docs/process/CARVER_SOURCE_NATIVE_TRANSLATION_ARCHITECTURE_GOAL_2026-05-28.md`
- `docs/researchops/handoffs/CARVER_BOOK_STRATEGY_AND_PORTFOLIO_INVENTORY_001_2026-05-28.md`
- `docs/researchops/candidates/CARVER_S01_BUY_AND_HOLD_SINGLE_CONTRACT_CANDIDATE_BRIEF_2026-05-28.md`

S02 is a prerequisite for:

- S03 buy-and-hold with variable risk scaling.
- S04 buy-and-hold portfolio with variable risk position sizing.
- M1 position sizing and risk-scaling work once separately authorized.
- Later daily directional strategies that inherit Carver's position sizing machinery.

## Book Framing

Carver frames S02 as the first correction to S01's fixed one-contract posture. Instead of selecting a contract count first and then asking how much capital is needed, S02 starts with capital and calculates an appropriate position size from instrument risk.

Source anchors:

- S02 starts as "Buy and hold with risk scaling" on `Carver.pdf`, PDF page 67.
- The chapter explicitly changes the order of reasoning: given capital first, calculate position size second, with instrument risk as the key input on PDF page 67.
- The chapter scope includes measuring risk, position scaling, target risk, compounding of returns for performance evaluation, and minimum capital on PDF page 68.
- Risk for a single contract is measured as annualised standard deviation of returns, then translated into currency terms using current price, futures multiplier, and notional exposure on PDF pages 68-70.
- The sizing equation uses the price of the expiry currently held, not the back-adjusted price, and includes an FX rate for currency translation on PDF page 70.
- The chapter defines target risk as annualised percentage standard deviation on capital, then equates target currency risk to position risk to derive the required contract count on PDF pages 70-71.
- The book also gives an alternative formulation using daily risk in price points from daily back-adjusted price differences, noting that this helps when the current futures price is negative, on PDF page 72.
- The target-risk discussion says the final target should be the most conservative of margin capacity, prudent loss tolerance, personal risk appetite, and expected-performance/Kelly considerations on PDF pages 73-79.
- Carver uses a relatively conservative 20% annualised risk target for the rest of the book on PDF page 79.
- The S02 example recalculates the required optimal position daily from current futures price and FX rate, then rounds the contract count, on PDF pages 79-80.
- The book states that S02's example uses an average standard deviation over the entire available period, and its footnote flags that as forward-looking/in-sample because it would not have been known at the start; any future implementation must lock a non-leaking risk convention or remain blocked. See `Carver.pdf`, PDF pages 80 and 92.
- Carver describes his futures trading style as continuous position recalculation, usually once per day in this book, rather than discrete entry/exit trading, on PDF pages 80-81.
- For performance reporting, S02 uses fixed notional capital and non-compounded percentage returns, while warning that real-money position sizing should reduce after losses by using current account value as the notional capital on PDF pages 82-84.
- The chapter introduces minimum capital because futures contracts are indivisible, and recommends enough capital to begin with at least four contracts as a rule of thumb on PDF pages 85-87.
- Carver concludes that risk targeting improves the S01 framing but remains flawed because risk varies over time, skew and fat tails remain, and S03 will address time-varying risk on PDF page 90.

## Candidate Interpretation

S02 is admitted as:

```text
STANDALONE_CANDIDATE
```

Its clean first role is to lock Carver's single-instrument risk-scaling mechanics. It is not a preferred final system, not a portfolio, and not alpha promotion.

S02 should be used to lock these source-native primitives:

- Available capital before position size.
- Annualised percentage risk of the instrument.
- Currency risk per contract.
- Target risk on capital.
- Futures multiplier.
- Current held-contract price for sizing.
- FX conversion between instrument and account currency.
- Daily optimal-position recomputation.
- Whole-contract rounding.
- Fixed-capital non-compounded performance-reporting convention.
- Minimum capital and indivisibility constraints.

S02 does not authorize variable volatility estimation over time. That is S03 territory.

## Candidate Rule Skeleton

The S02 source rule skeleton is:

```text
For one source-native futures instrument:
hold a long buy-and-hold exposure,
calculate the desired contract count from capital, target risk, instrument risk,
current held-contract price, futures multiplier, and FX conversion,
round to a whole-contract position,
roll according to the locked source-native roll rule,
calculate PnL from completed daily back-adjusted price changes and the actual held position,
account for costs separately once a cost source is authorized.
```

No live rule, code rule, executable rule, test rule, diagnostic rule, or backtest rule is authorized by this skeleton.

## M0 And S01 Inheritance

S02 inherits these M0 defaults:

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

S02 inherits these S01 primitives:

- Exact source-native instrument identity must be locked.
- Continuous-contract construction and roll rule must be locked.
- Back-adjusted price is the excess-return PnL input.
- Futures multiplier, tick size, tick value, instrument currency, base currency, and FX treatment must be locked.
- Costs remain separate and must come from an authorized cost source.
- Missing or invalid source atoms fail closed.

S02 adds risk-scaling machinery on top of S01. It does not replace S01's futures construction atoms.

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

As in S01, the Appendix C first-year field must not be treated as proof of actual MES trading history. Any future data lane must lock whether and how continuous history is represented. No backfill, substitution, or contract-size bridge is authorized by this brief.

## Required Atoms Before Data Work

S02 cannot proceed to data work until all S01 atoms and these S02-specific atoms are locked:

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
- Annualised instrument-risk definition.
- Whether percentage-risk or daily-price-point risk is the locked S02 sizing form.
- Risk-estimation input series.
- Risk-estimation window or fixed source estimate for S02.
- Non-leaking rule for any risk estimate used outside a pure book-example conformance check.
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
- Treatment of zero, missing, stale, or invalid risk estimates.
- Treatment of zero, missing, stale, or invalid prices, multipliers, FX rates, rolls, or costs.
- Cost source in `config/costs.json` once authorized.
- Commission, spread, and extra turnover treatment.
- Evidence-window budget if a future diagnostic/backtest is requested.

## Locked Process Decisions

The following process decisions are locked by this brief:

- S02 remains process-only until separately authorized.
- S02 is `SOURCE_NATIVE_FUTURES`, not CFD.
- S02 is a daily directional-stack candidate.
- S02 uses completed daily bars only.
- S02 inherits S01 futures identity, roll, back-adjustment, multiplier, FX, and cost atoms.
- S02 adds fixed-risk position sizing and whole-contract rounding.
- S02 does not authorize S03's time-varying volatility estimator.
- S02 must prefer native daily futures candles when a future data lane is authorized.
- S02 must not reconstruct daily bars from 1-minute data by default.
- S02 must not use old QuantLab data-prep scripts, CFD adapters, broker-clock assumptions, or stale state.
- S02 must not treat historical performance as promotion evidence.
- A non-positive future S02 standalone result does not advance and must not be rescued by tuning.

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
- Annualised instrument-risk definition.
- Percentage-risk versus daily-price-point sizing form.
- Risk-estimation input series.
- Risk-estimation window or fixed source estimate for S02.
- Non-leaking rule for any risk estimate used outside a pure book-example conformance check.
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
- Commission, spread, and extra turnover treatment.
- Fail-closed behavior for missing or invalid prices, rolls, multipliers, FX, risk estimates, costs, or negative/zero sizing inputs.
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

Before this S02 brief is treated as process-safe, it must receive a hostile audit by subagent.

Audit focus:

- M0 inheritance.
- S01 inheritance.
- Source-page faithfulness.
- No data or implementation leakage.
- No backtest or evidence leakage.
- No NinjaTrader operational leakage.
- No CFD or old QuantLab contamination.
- Correct `STANDALONE_CANDIDATE` interpretation.
- Correct separation from S03 variable risk scaling.
- Completeness of unresolved atoms.

## Next Gate

If this S02 brief is accepted after hostile audit, the next possible process-only gate is:

```text
PROCESS_ONLY_CARVER_S03_BUY_AND_HOLD_WITH_VARIABLE_RISK_SCALING_BRIEF_DRAFT_NOT_DATA_NOT_STRATEGY_AUTHORIZATION
```

No S03 work is authorized by this S02 brief.

## Standing Non-Authorization

This file authorizes no data access, no market-row parsing, no implementation, no tests, no diagnostics, no backtests, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old-adapter import, no tuning, no deployment, no trading, and no promotion.
