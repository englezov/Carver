# First Spine Candidate And Portfolio Briefs

Generated: 2026-05-28

Status:

```text
PROCESS_ONLY_OPUS_UPLOAD_CONTEXT_NOT_DATA_NOT_IMPLEMENTATION_AUTHORIZATION
```

This file is an upload-context bundle generated from clean Carver repo-local artifacts. It authorizes no data access, no market-row parsing, no implementation, no tests, no diagnostics, no backtests, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old QuantLab import, no tuning, no deployment, no trading, and no promotion.

---

## Source File: `docs/researchops/candidates/CARVER_S01_BUY_AND_HOLD_SINGLE_CONTRACT_CANDIDATE_BRIEF_2026-05-28.md`

# Carver S01 Buy And Hold Single Contract Candidate Brief

Date: 2026-05-28

Status:

```text
PROCESS_ONLY_CARVER_S01_BUY_AND_HOLD_SINGLE_CONTRACT_BRIEF_DRAFT_NOT_DATA_NOT_STRATEGY_AUTHORIZATION
```

## Purpose

Create the process-only source-native futures candidate brief for Carver Strategy 1:

```text
S01_BUY_AND_HOLD_SINGLE_CONTRACT
```

This brief inherits M0 and records the source framing, classification, dependencies, locked process atoms, unresolved atoms, and next gates before any data work or implementation.

This brief is not a data lane, implementation lane, test lane, diagnostic lane, backtest lane, OOS lane, Lockbox lane, Forward lane, CFD adapter lane, deployment lane, trading lane, or promotion lane.

## Classification

| Field | Value |
| --- | --- |
| Strategy ID | S01 |
| Book strategy | Strategy one: Buy and hold, single contract |
| Book pages | `Carver.pdf`, PDF pages 21-66 |
| Lane class | `SOURCE_NATIVE_FUTURES` |
| Strategy label | `STANDALONE_CANDIDATE` |
| Timeframe family | Daily directional stack |
| Data posture | No data access authorized |
| Implementation posture | No implementation authorized |
| Evidence posture | No diagnostics or backtests authorized |

## Dependencies

S01 depends on:

- `docs/process/CARVER_M0_SOURCE_NATIVE_FUTURES_FOUNDATION_SPEC_2026-05-28.md`
- `docs/process/CARVER_LEAN_IMPLEMENTATION_AND_BACKTEST_DEFERRAL_RULE_2026-05-28.md`
- `docs/process/CARVER_SOURCE_NATIVE_TRANSLATION_ARCHITECTURE_GOAL_2026-05-28.md`
- `docs/researchops/handoffs/CARVER_BOOK_STRATEGY_AND_PORTFOLIO_INVENTORY_001_2026-05-28.md`

S01 is a prerequisite for:

- S02 buy-and-hold with risk scaling.
- S03 buy-and-hold with variable risk scaling.
- S04 buy-and-hold portfolio with variable risk position sizing.
- M1 position sizing and risk-scaling work once separately authorized.

## Book Framing

Carver frames S01 as the simplest possible futures strategy: buy and hold a single futures contract. The teaching example begins with the S&P 500 future as exposure to the equity risk premium, then extends the same mechanics to other futures and asset classes.

Source anchors:

- S01 starts as "Buy and hold, single contract" on `Carver.pdf`, PDF page 21.
- The book describes the first strategy as buying and holding a single futures contract on PDF page 23.
- The first teaching instrument is the S&P 500 future, with the micro S&P 500 future used as the small-contract example on PDF pages 23-25.
- S01 introduces futures multipliers, tick size, tick value, expiry dates, rolling, back-adjusted futures prices, trading costs, profit calculation, capital, and performance assessment on PDF page 23.
- The book initially tests daily data using daily closing prices for each contract expiry date on PDF page 30.
- Back-adjustment is used to represent the profit and loss from constantly holding and rolling one futures contract while excluding trading costs, which are considered separately, on PDF pages 30-31.
- The adjusted futures price is an excess-return series that includes spot and carry, not a total-return series, on PDF pages 33-34.
- Profit in instrument currency is price change times futures multiplier, with base-currency conversion when needed, on PDF pages 34-35.
- The book warns that backtests can be overstated and can create in-sample fitting risk on PDF pages 37-40.
- Carver concludes S01 is useful for understanding the raw materials used by later strategies, but risky as a lone practical strategy because instrument selection and raw risk are difficult, on PDF pages 62-63.

## Candidate Interpretation

S01 is admitted as:

```text
STANDALONE_CANDIDATE
```

However, its first clean role is foundational conformance, not alpha promotion.

S01 should be used to lock the mechanical primitives of source-native futures handling:

- One-contract position.
- Futures multiplier.
- Contract expiry and roll.
- Back-adjusted price.
- Excess-return PnL.
- Costs as a separate atom.
- Capital and percentage-return convention.
- Performance-statistic definitions for later source conformance.

S01 is not a preferred final system, not a portfolio, and not evidence of alpha.

## Candidate Rule Skeleton

The S01 source rule skeleton is:

```text
For one source-native futures instrument:
hold a constant long position of one contract,
roll according to a locked source-native roll rule,
calculate PnL from completed daily back-adjusted price changes,
apply the futures multiplier,
convert to base currency if required,
account for costs separately once a cost source is authorized.
```

No live rule, code rule, executable rule, test rule, or backtest rule is authorized by this skeleton.

## M0 Inheritance

S01 inherits these M0 defaults:

- Lane class: `SOURCE_NATIVE_FUTURES`.
- Local data surface candidate: `NINJATRADER_SOURCE_NATIVE_FUTURES_DATA_SURFACE_CANDIDATE`.
- Local native timeframe first.
- Completed daily bars for the daily directional stack.
- No NinjaTrader export, parsing, subscription, brokerage connection, credential handling, or trading integration.
- No CFD adapter.
- No old QuantLab active authority.
- No implementation without separate implementation authorization.
- Synthetic/source-conformance tests only after a separate implementation authorization.
- No historical diagnostics or backtests without separate operator authorization.

## Preferred Initial Source Instrument

The book teaching example is:

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

The S&P 500 micro contract itself began trading later than the full historical S&P futures history, and Appendix C's first-year field is a dataset field rather than proof of actual MES trading history. Any future data lane must lock whether and how continuous history is represented. No backfill, substitution, or contract-size bridge is authorized by this brief.

## Required Atoms Before Data Work

S01 cannot proceed to data work until these atoms are locked:

- Exact source-native instrument identity.
- Whether the initial instrument is `MES`, another S&P 500 futures contract, or a documented source-native historical bridge.
- Exchange session definition.
- Timezone.
- Completed daily bar close timestamp.
- Holiday calendar.
- Daily candle cut convention.
- Native data surface and timeframe.
- Continuous-contract construction.
- Contract selection and roll rule.
- Back-adjustment method.
- Treatment of raw futures price versus adjusted futures price.
- Futures multiplier.
- Tick size and tick value.
- Instrument currency and base currency.
- FX conversion rule if instrument currency differs from base currency.
- Cost source.
- Commission and spread treatment.
- Capital convention for percentage returns.
- Notional exposure convention.
- Fail-closed behavior for missing prices, missing rolls, missing multipliers, missing FX, missing costs, or negative adjusted prices.
- Evidence-window budget if a future diagnostic/backtest is requested.

## Locked Process Decisions

The following process decisions are locked by this brief:

- S01 remains process-only until separately authorized.
- S01 is `SOURCE_NATIVE_FUTURES`, not CFD.
- S01 uses completed daily bars only.
- S01 must prefer native daily futures candles when a future data lane is authorized.
- S01 must not reconstruct daily bars from 1-minute data by default.
- S01 must not use old QuantLab data-prep scripts, CFD adapters, broker-clock assumptions, or stale state.
- S01 must not treat historical performance as promotion evidence.
- A non-positive future S01 standalone result does not advance and must not be rescued by tuning.

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
- Futures multiplier.
- Tick size and tick value.
- Instrument currency and base currency.
- Exact cost source in `config/costs.json`.
- Commission and spread treatment.
- Exact base currency and FX conversion handling.
- Exact capital convention for percentage-return reporting.
- Notional exposure convention.
- Fail-closed behavior for missing prices, missing rolls, missing multipliers, missing FX, missing costs, or negative adjusted prices.
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

Before this S01 brief is treated as process-safe, it must receive a hostile audit by subagent.

Audit focus:

- M0 inheritance.
- Source-page faithfulness.
- No data or implementation leakage.
- No backtest or evidence leakage.
- No NinjaTrader operational leakage.
- No CFD or old QuantLab contamination.
- Correct `STANDALONE_CANDIDATE` interpretation.
- Completeness of unresolved atoms.

## Next Gate

If this S01 brief is accepted after hostile audit, the next possible process-only gate is:

```text
PROCESS_ONLY_CARVER_S02_BUY_AND_HOLD_WITH_RISK_SCALING_BRIEF_DRAFT_NOT_DATA_NOT_STRATEGY_AUTHORIZATION
```

No S02 work is authorized by this S01 brief.

## Standing Non-Authorization

This file authorizes no data access, no market-row parsing, no implementation, no tests, no diagnostics, no backtests, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old-adapter import, no tuning, no deployment, no trading, and no promotion.


---

## Source File: `docs/researchops/candidates/CARVER_S02_BUY_AND_HOLD_WITH_RISK_SCALING_CANDIDATE_BRIEF_2026-05-28.md`

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


---

## Source File: `docs/researchops/candidates/CARVER_S03_BUY_AND_HOLD_WITH_VARIABLE_RISK_SCALING_CANDIDATE_BRIEF_2026-05-28.md`

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


---

## Source File: `docs/researchops/candidates/CARVER_S04_BUY_AND_HOLD_PORTFOLIO_WITH_VARIABLE_RISK_POSITION_SIZING_CANDIDATE_BRIEF_2026-05-28.md`

# Carver S04 Buy And Hold Portfolio With Variable Risk Position Sizing Candidate Brief

Date: 2026-05-28

Status:

```text
PROCESS_ONLY_CARVER_S04_BUY_AND_HOLD_PORTFOLIO_WITH_VARIABLE_RISK_POSITION_SIZING_BRIEF_DRAFT_NOT_DATA_NOT_STRATEGY_AUTHORIZATION
```

## Purpose

Create the process-only source-native futures candidate brief for Carver Strategy 4:

```text
S04_BUY_AND_HOLD_PORTFOLIO_WITH_VARIABLE_RISK_POSITION_SIZING
```

This brief inherits M0, S01, S02, and S03. It records the source framing, classification, dependencies, locked process atoms, unresolved atoms, and next gates before any data work or implementation.

This brief is not a data lane, implementation lane, test lane, diagnostic lane, backtest lane, OOS lane, Lockbox lane, Forward lane, CFD adapter lane, deployment lane, trading lane, or promotion lane.

## Classification

| Field | Value |
| --- | --- |
| Strategy ID | S04 |
| Book strategy | Strategy four: Buy and hold portfolio with variable risk position sizing |
| Book pages | `Carver.pdf`, PDF pages 118-144 |
| Lane class | `SOURCE_NATIVE_FUTURES` |
| Strategy label | `STANDALONE_CANDIDATE` |
| Portfolio role | Gateway to complete portfolio briefs P01-P04 |
| Timeframe family | Daily directional portfolio stack |
| Data posture | No data access authorized |
| Implementation posture | No implementation authorized |
| Evidence posture | No diagnostics or backtests authorized |

## Dependencies

S04 depends on:

- `docs/process/CARVER_M0_SOURCE_NATIVE_FUTURES_FOUNDATION_SPEC_2026-05-28.md`
- `docs/process/CARVER_LEAN_IMPLEMENTATION_AND_BACKTEST_DEFERRAL_RULE_2026-05-28.md`
- `docs/process/CARVER_SOURCE_NATIVE_TRANSLATION_ARCHITECTURE_GOAL_2026-05-28.md`
- `docs/researchops/handoffs/CARVER_BOOK_STRATEGY_AND_PORTFOLIO_INVENTORY_001_2026-05-28.md`
- `docs/researchops/candidates/CARVER_S01_BUY_AND_HOLD_SINGLE_CONTRACT_CANDIDATE_BRIEF_2026-05-28.md`
- `docs/researchops/candidates/CARVER_S02_BUY_AND_HOLD_WITH_RISK_SCALING_CANDIDATE_BRIEF_2026-05-28.md`
- `docs/researchops/candidates/CARVER_S03_BUY_AND_HOLD_WITH_VARIABLE_RISK_SCALING_CANDIDATE_BRIEF_2026-05-28.md`

S04 is a prerequisite for:

- P01 risk parity example portfolio.
- P02 All Weather example portfolio.
- P03 generalized risk premia portfolio construction.
- P04 Jumbo buy-and-hold portfolio.
- Later Jumbo strategy portfolios that inherit instrument weights, IDM, selection constraints, and portfolio risk targeting.

## Book Framing

Carver frames S04 as the move from single-instrument S03 to diversified multi-instrument futures portfolios. Each sub-strategy is a version of S03 trading a different instrument. Because each sub-strategy is risk-scaled, the instrument capital allocation is also intended to be the risk allocation.

Source anchors:

- S04 starts as "Buy and hold portfolio with variable risk position sizing" on `Carver.pdf`, PDF page 118.
- The chapter states that each capital chunk is used to trade a sub-strategy, with each sub-strategy being a version of S03 trading a different instrument, on PDF page 118.
- The chapter scope includes risk parity, All Weather, a generic version for any number of instruments, the Jumbo portfolio, multi-instrument risk scaling, minimum capital, instrument selection, and capital allocation on PDF pages 118-119.
- The risk parity variation allocates equally to S&P 500 micro futures and US 10-year bond futures, then generalizes S03 position sizing by multiplying capital by the instrument weight on PDF pages 119-120.
- Carver introduces the instrument diversification multiplier (`IDM`) to correct for diversification and scale the aggregate portfolio toward the target risk on PDF pages 122-123.
- The All Weather variation uses instrument weights of 25% S&P 500 micro, 12.5% US 10-year, 12.5% US 5-year, 12.5% WTI Crude Oil mini, 12.5% Corn, and 25% Gold micro. The definition pack records IDM 1.81 as source context for the book example, but the exact value/page quote must be re-page-audited before implementation. See PDF pages 124-126.
- The generalized risk premia portfolio uses the same S03 criteria for selecting instruments: risk-adjusted cost below 0.01 SR units, average daily volume of at least 100 contracts, risk-volume threshold, and minimum capital for at least four contracts on PDF page 127.
- S04 modifies the minimum-capital formula so that portfolio instrument weights and IDM affect the required account capital on PDF pages 127-128.
- Carver treats instrument weights as risk-capital allocation across sub-strategies, not ordinary cash allocation across assets, on PDF page 128.
- Carver says instrument weights can be assigned with a handcrafting method that first allocates equally across asset classes, then groups, then instruments on PDF pages 130-135.
- Table 16 supplies approximate IDM values by number of instruments and warns that the table assumes a relatively diversified instrument set on PDF page 135.
- Carver gives an automatic instrument-selection procedure based on possible instruments, lowest cost first instrument, trial portfolios, weights, IDM, minimum capital checks, expected SR from costs/correlations, and a 10% expected-SR stop rule on PDF pages 135-140.
- For the algorithm, Carver assumes equal pre-cost SR across instruments so that post-cost SR depends on costs, rather than choosing instruments from historical realised Sharpe ratios, on PDF pages 137-139.
- The Jumbo portfolio uses 102 instruments meeting liquidity and cost thresholds and at least one year of data, assumes USD 50 million capital, and uses handcrafted weights. The definition pack records IDM 2.47 as source context for the book example, but the exact value/page quote must be re-page-audited before implementation. See PDF page 141.
- Carver uses the S04 framework later to present both median single-instrument results and aggregate Jumbo portfolio results on PDF pages 141-143.
- Carver advises risk targets by portfolio breadth: 10% for a single instrument, interpolate between 10% and 20% for two to six instruments, 20% only if all seven asset classes are represented, and up to 25% only if at least two instruments from each asset class are present. See `Carver.pdf`, PDF pages 143-144.
- The S04 trading plan states that all other elements are identical to S03 on PDF page 144.

## Candidate Interpretation

S04 is admitted as:

```text
STANDALONE_CANDIDATE
```

S04 is standalone at the strategy-family level because it is a complete multi-instrument buy-and-hold portfolio construction. It is also the gateway for separate complete portfolio briefs. P01, P02, P03, and P04 must be reconstructed independently and not inferred from isolated sleeve results.

S04 should be used to lock these source-native primitives:

- Multi-instrument sub-strategy construction from S03.
- Instrument weights as risk-capital weights.
- Portfolio-level target risk.
- Instrument diversification multiplier.
- Portfolio minimum-capital rule.
- Top-down handcrafting of instrument weights.
- Cost and liquidity eligibility.
- Portfolio breadth and target-risk constraints.
- Fail-closed behavior when an instrument is unavailable or fails eligibility.
- Separation between candidate brief and complete portfolio reconstruction brief.

S04 must not use historical best-instrument selection as strategy status. Instrument inclusion must be governed by pre-locked source-native identity, cost, liquidity, minimum-capital, diversification, and portfolio-construction rules.

## Candidate Rule Skeleton

The S04 source rule skeleton is:

```text
For a source-native futures instrument set:
assign each eligible instrument a pre-locked instrument weight,
run an S03-style long buy-and-hold variable-risk sub-strategy per instrument,
scale each instrument position by instrument weight and IDM,
round each instrument position according to the locked rule,
roll each instrument according to its locked source-native roll rule,
aggregate completed daily PnL across instruments,
account for costs separately once a cost source is authorized.
```

No live rule, code rule, executable rule, test rule, diagnostic rule, portfolio backtest rule, or promotion rule is authorized by this skeleton.

## M0, S01, S02, And S03 Inheritance

S04 inherits these M0 defaults:

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

S04 inherits these S01 primitives:

- Exact source-native instrument identity must be locked.
- Continuous-contract construction and roll rule must be locked.
- Back-adjusted price is the excess-return PnL input.
- Futures multiplier, tick size, tick value, instrument currency, base currency, and FX treatment must be locked.
- Costs remain separate and must come from an authorized cost source.
- Missing or invalid source atoms fail closed.

S04 inherits these S02 primitives:

- Available capital before position size.
- Target risk on capital.
- Current held-contract raw price for sizing.
- Daily optimal-position recomputation.
- Whole-contract rounding.
- Minimum capital and indivisibility constraints.
- Non-leaking risk-estimate rule for any future implementation.

S04 inherits these S03 primitives:

- Variable risk estimate.
- EWMA span and lambda/alpha convention.
- Long-run and short-run volatility blend.
- Risk-adjusted cost per trade.
- Roll versus non-roll turnover.
- Trading speed limit.
- Liquidity eligibility.
- Instrument-size selection where alternatives exist.

S04 adds multi-instrument portfolio construction, instrument weights, IDM, and portfolio breadth rules. It does not authorize P01, P02, P03, or P04 reconstruction by itself.

## Book-Named Portfolio Children

S04 opens the source context for these later portfolio briefs:

| Portfolio | Book framing | Source pages | Status in this brief |
| --- | --- | --- | --- |
| P01 | Risk parity example: S&P 500 micro plus US 10-year bond futures | PDF pages 119-123 | Not authorized; separate portfolio brief required |
| P02 | All Weather example: six instruments across stocks, bonds, commodities, and gold | PDF pages 124-126 | Not authorized; separate portfolio brief required |
| P03 | Generalized risk premia construction | PDF pages 127-140 | Not authorized; separate portfolio brief required |
| P04 | Jumbo buy-and-hold portfolio | PDF pages 141-144 plus Appendix C | Not authorized; separate portfolio brief required |

No complete portfolio is locked by this S04 candidate brief.

## Preferred Initial Source Instruments

The S04 chapter directly names these teaching instruments:

| Role | Instrument | Book/Appendix C market code | Exchange | Currency | Multiplier | Source |
| --- | --- | --- | --- | --- | --- | --- |
| Risk parity equity leg | S&P 500 micro future | `MES` | GLOBEX | USD | 5 | PDF pages 119-120, 692 |
| Risk parity bond leg | US 10-year bond future | `ZN` | ECBOT | USD | 1000 | PDF pages 119-120, 691 |
| All Weather bond leg | US 5-year bond future | `ZF` | ECBOT | USD | 1000 | PDF pages 124-126, 691 |
| All Weather energy leg | WTI Crude Oil mini future | `QM` | NYMEX | USD | 500 | PDF pages 124-126, 695 |
| All Weather agriculture leg | Corn future | `ZC` | ECBOT | USD | 5000 | PDF pages 124-126, 695 |
| All Weather metal leg | Gold micro future | `MGC` | NYMEX | USD | 10 | PDF pages 124-126, 694 |

These are source-preferred teaching candidates only. No data access is authorized.

Appendix C says these market codes are the codes used by Carver's broker and may differ across brokers or official exchange codes. Any future data lane must lock exact local symbol mapping, source-native contract identity, roll rules, and whether Appendix C codes match local NinjaTrader symbols. No silent substitution, CFD proxy, ETF proxy, or old QuantLab symbol is authorized by this brief.

## Required Atoms Before Data Work

S04 cannot proceed to data work until all S01, S02, and S03 atoms and these S04-specific atoms are locked:

- Exact source-native instrument universe for the candidate or portfolio child.
- Exact local symbol mapping for every instrument.
- Exchange session, timezone, completed daily bar close, holiday calendar, and daily candle cut for every instrument.
- Continuous-contract construction and roll rule per instrument.
- Back-adjustment method per instrument.
- Current held-contract raw price source per instrument for sizing.
- Futures multiplier, tick size, tick value, instrument currency, base/account currency, and FX conversion per instrument.
- Variable risk estimate per instrument using only returns completed before each sizing timestamp.
- Instrument weight table or deterministic weight-construction rule.
- Portfolio-level capital base.
- Portfolio-level target risk.
- Portfolio breadth rule used to justify target risk.
- IDM source: book table, source example, or separately authorized calculation.
- IDM fail-closed behavior if instrument set is not diversified enough for table use.
- Instrument eligibility rules: cost, liquidity, minimum capital, and source availability.
- Risk-adjusted cost threshold.
- Contract-volume threshold.
- Risk-volume threshold.
- Minimum four-contract rule and portfolio minimum-capital formula.
- Instrument-size selection rule for micro/mini/full-size alternatives.
- Top-down asset-class/group/instrument classification table if using handcrafted weights.
- Correlation matrix source if using the automatic selection algorithm.
- Pre-cost SR assumption if using the automatic selection algorithm.
- Expected-SR stop rule if using the automatic selection algorithm.
- Requirement that correlation matrices and expected-SR inputs be pre-locked before any future market-data inspection.
- Prohibition on post-result best-instrument selection or rescue.
- Fail-closed rule for missing instruments, missing costs, insufficient liquidity, insufficient capital, or unresolved source identity.
- Portfolio aggregation convention for completed daily PnL.
- Cost source in `config/costs.json` once authorized.
- Evidence-window budget if a future diagnostic/backtest is requested.

## Locked Process Decisions

The following process decisions are locked by this brief:

- S04 remains process-only until separately authorized.
- S04 is `SOURCE_NATIVE_FUTURES`, not CFD.
- S04 is a daily directional portfolio-stack candidate.
- S04 uses completed daily bars only.
- S04 inherits S01 futures identity, roll, back-adjustment, multiplier, FX, and cost atoms.
- S04 inherits S02 target-risk position sizing and whole-contract rounding.
- S04 inherits S03 variable risk estimation and risk-adjusted cost atoms.
- S04 adds instrument weights, IDM, portfolio breadth rules, and multi-instrument aggregation.
- S04 does not authorize P01, P02, P03, or P04 as complete portfolio artifacts.
- S04 must prefer native daily futures candles when a future data lane is authorized.
- S04 must not reconstruct daily bars from 1-minute data by default.
- S04 must not use old QuantLab data-prep scripts, CFD adapters, broker-clock assumptions, or stale state.
- S04 must not select a best instrument after seeing historical performance.
- S04 must not treat historical performance as promotion evidence.
- A non-positive future S04 standalone/portfolio result does not advance and must not be rescued by tuning.

## Explicitly Unresolved

The following remain unresolved and block data/implementation work:

- Exact source-native instrument universe for any S04 child.
- Exact local symbol mapping for every instrument.
- Whether book examples use exact local instruments or documented source-native historical bridges.
- Exchange session, timezone, completed daily bar close, holiday calendar, and daily candle cut for every instrument.
- Exact roll calendar and roll timing per instrument.
- Exact continuous-contract/back-adjustment construction per instrument.
- Treatment of raw futures price versus adjusted futures price per instrument.
- Current held-contract raw price source per instrument for sizing.
- Futures multiplier, tick size, tick value, instrument currency, base/account currency, and FX conversion per instrument.
- Variable risk estimate per instrument.
- EWMA span and lambda/alpha convention if not inherited unchanged.
- Long-run and short-run volatility definitions if not inherited unchanged.
- Warm-up period and first usable date per instrument.
- Instrument weight table or deterministic weight-construction rule.
- Portfolio-level capital base.
- Portfolio-level target risk.
- Portfolio breadth rule used to justify target risk.
- IDM source and exact IDM value/rule.
- Source-example IDM value/page verification for P02 and Jumbo before treating those numbers as locked authority.
- Diversification validity of any approximate IDM table use.
- Instrument eligibility rules: cost, liquidity, minimum capital, and source availability.
- Exact risk-adjusted cost threshold.
- Exact contract-volume threshold.
- Exact risk-volume threshold.
- Minimum four-contract rule and portfolio minimum-capital formula.
- Instrument-size selection rule for micro/mini/full-size alternatives.
- Top-down asset-class/group/instrument classification table if using handcrafted weights.
- Correlation matrix source if using the automatic selection algorithm.
- Pre-cost SR assumption if using the automatic selection algorithm.
- Expected-SR stop rule if using the automatic selection algorithm.
- Requirement that correlation matrices and expected-SR inputs be pre-locked before any future market-data inspection.
- Fail-closed behavior for missing or invalid prices, rolls, multipliers, FX, risk estimates, costs, liquidity, capital, weights, IDM, or sizing inputs.
- Exact cost source in `config/costs.json`.
- Portfolio aggregation convention for completed daily PnL.
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

Before this S04 brief is treated as process-safe, it must receive a hostile audit by subagent.

Audit focus:

- M0 inheritance.
- S01, S02, and S03 inheritance.
- Source-page faithfulness.
- No data or implementation leakage.
- No backtest or evidence leakage.
- No NinjaTrader operational leakage.
- No CFD or old QuantLab contamination.
- Correct `STANDALONE_CANDIDATE` interpretation with gateway-to-portfolio role.
- Correct separation from P01, P02, P03, and P04 complete portfolio briefs.
- No historical best-instrument selection leakage.
- Completeness of unresolved atoms.

## Next Gate

If this S04 brief is accepted after hostile audit, the next possible process-only gate is:

```text
PROCESS_ONLY_CARVER_P01_RISK_PARITY_EXAMPLE_PORTFOLIO_BRIEF_DRAFT_NOT_DATA_NOT_STRATEGY_AUTHORIZATION
```

No P01 work is authorized by this S04 brief.

## Standing Non-Authorization

This file authorizes no data access, no market-row parsing, no implementation, no tests, no diagnostics, no backtests, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old-adapter import, no tuning, no deployment, no trading, and no promotion.


---

## Source File: `docs/researchops/portfolios/CARVER_P01_RISK_PARITY_EXAMPLE_PORTFOLIO_BRIEF_2026-05-28.md`

# Carver P01 Risk Parity Example Portfolio Brief

Date: 2026-05-28

Status:

```text
PROCESS_ONLY_CARVER_P01_RISK_PARITY_EXAMPLE_PORTFOLIO_BRIEF_DRAFT_NOT_DATA_NOT_STRATEGY_AUTHORIZATION
```

## Purpose

Create the process-only source-native futures portfolio brief for Carver Portfolio 1:

```text
P01_RISK_PARITY_EXAMPLE_PORTFOLIO
```

This brief inherits M0, S01, S02, S03, and S04. It reconstructs the P01 source framing and required atoms before any data work, implementation, test, diagnostic, backtest, OOS, Lockbox, Forward, CFD adapter, deployment, trading, or promotion.

This is a complete portfolio reconstruction brief. It is not inferred from standalone sleeve results.

## Classification

| Field | Value |
| --- | --- |
| Portfolio ID | P01 |
| Book portfolio | Risk parity example portfolio |
| Book pages | `Carver.pdf`, PDF pages 119-123 |
| Lane class | `SOURCE_NATIVE_FUTURES` |
| Portfolio type | Two-instrument risk parity example |
| Member strategy machinery | S03 variable-risk buy-and-hold, wrapped by S04 portfolio construction |
| Timeframe family | Daily directional portfolio stack |
| Data posture | No data access authorized |
| Implementation posture | No implementation authorized |
| Evidence posture | No diagnostics or backtests authorized |

## Dependencies

P01 depends on:

- `docs/process/CARVER_M0_SOURCE_NATIVE_FUTURES_FOUNDATION_SPEC_2026-05-28.md`
- `docs/process/CARVER_LEAN_IMPLEMENTATION_AND_BACKTEST_DEFERRAL_RULE_2026-05-28.md`
- `docs/process/CARVER_SOURCE_NATIVE_TRANSLATION_ARCHITECTURE_GOAL_2026-05-28.md`
- `docs/researchops/handoffs/CARVER_BOOK_STRATEGY_AND_PORTFOLIO_INVENTORY_001_2026-05-28.md`
- `docs/researchops/candidates/CARVER_S01_BUY_AND_HOLD_SINGLE_CONTRACT_CANDIDATE_BRIEF_2026-05-28.md`
- `docs/researchops/candidates/CARVER_S02_BUY_AND_HOLD_WITH_RISK_SCALING_CANDIDATE_BRIEF_2026-05-28.md`
- `docs/researchops/candidates/CARVER_S03_BUY_AND_HOLD_WITH_VARIABLE_RISK_SCALING_CANDIDATE_BRIEF_2026-05-28.md`
- `docs/researchops/candidates/CARVER_S04_BUY_AND_HOLD_PORTFOLIO_WITH_VARIABLE_RISK_POSITION_SIZING_CANDIDATE_BRIEF_2026-05-28.md`

P01 is a prerequisite example for:

- P02 All Weather example portfolio.
- P03 generalized risk premia portfolio construction.
- P04 Jumbo buy-and-hold portfolio.
- Any later portfolio brief that uses instrument weights and IDM.

## Book Framing

Carver frames P01 as the first concrete S04 variation: a futures risk parity portfolio combining equity beta and bond duration.

Source anchors:

- The risk parity variation begins on `Carver.pdf`, PDF page 119.
- The book contrasts ordinary 60/40 cash allocation with futures-based risk allocation, noting that equities have higher risk than bonds on PDF page 119.
- Carver says S03 provides the method to construct a risk parity portfolio that can be leveraged to hit a required risk target or return expectation on PDF page 119.
- The P01 example splits total capital equally: 50% to the S&P 500 micro future and 50% to the US 10-year bond future on PDF page 120.
- The position-sizing formula generalizes S03 by applying the instrument weight to portfolio capital for each instrument on PDF page 120.
- In the book example, total capital is USD 1,000,000 and target risk is 20% on PDF page 120.
- Table 12 shows individual and aggregate results before IDM, and Carver explains that aggregate risk is below target because the two sub-strategy returns are not perfectly correlated on PDF pages 120-122.
- Carver introduces the instrument diversification multiplier (`IDM`) to scale positions so expected aggregate risk reaches target on PDF page 122.
- The book derives a rough IDM of 1.32 by dividing the 20% target risk by 15.1% realised aggregate risk in the example on PDF page 122.
- Table 13 shows the risk parity example after applying IDM 1.32, with aggregate standard deviation near 20% on PDF pages 122-123.
- Carver notes that leverage and costs rise with IDM, while risk-adjusted statistics are mostly unchanged except for rounding effects on PDF page 123.

## Portfolio Interpretation

P01 is a complete source-native futures portfolio reconstruction:

```text
SOURCE_NATIVE_FUTURES_PORTFOLIO_RECONSTRUCTION
```

P01 is not a standalone single-instrument candidate and not a sleeve result. It is the smallest complete book portfolio and should be used to lock the end-to-end portfolio mechanics before larger portfolio examples.

P01 should be used to lock these source-native portfolio primitives:

- Two instrument identities.
- Equal 50/50 instrument weights.
- S03 variable-risk sub-strategy per instrument.
- Portfolio-level capital base.
- Portfolio-level target risk.
- IDM application.
- Completed daily PnL aggregation across instruments.
- Portfolio cost aggregation.
- Fail-closed behavior when either leg is unavailable or unresolved.

## Portfolio Rule Skeleton

The P01 source rule skeleton is:

```text
For S&P 500 micro futures and US 10-year bond futures:
assign each instrument 50% portfolio weight,
run an S03-style long buy-and-hold variable-risk sub-strategy for each leg,
scale each leg by its instrument weight and the locked IDM rule,
round each leg according to the locked rule,
roll each leg according to its locked source-native roll rule,
aggregate completed daily PnL across both legs,
account for costs separately once a cost source is authorized.
```

No live rule, code rule, executable rule, test rule, diagnostic rule, backtest rule, OOS rule, Lockbox rule, Forward rule, or promotion rule is authorized by this skeleton.

## Inherited Machinery

P01 inherits:

- M0 source-native futures defaults and non-authorization.
- S01 futures identity, roll, back-adjustment, multiplier, FX, and cost atoms.
- S02 target-risk position sizing and whole-contract rounding.
- S03 variable risk estimation, non-leaking risk rule, and risk-adjusted cost atoms.
- S04 instrument weights, IDM, portfolio breadth, and multi-instrument aggregation atoms.

P01 does not authorize recalculating any inherited atom from data.

## Source-Named Instruments

The P01 book example uses:

| Role | Instrument | Book/Appendix C market code | Exchange | Currency | Multiplier | Source |
| --- | --- | --- | --- | --- | --- | --- |
| Equity risk premium leg | S&P 500 micro future | `MES` | GLOBEX | USD | 5 | PDF pages 119-120, 692 |
| Bond duration leg | US 10-year bond future | `ZN` | ECBOT | USD | 1000 | PDF pages 119-120, 691 |

Appendix C says these market codes are the codes used by Carver's broker and may differ across brokers or official exchange codes. Any future data lane must lock exact local symbol mapping, source-native contract identity, roll rules, and whether Appendix C codes match local NinjaTrader symbols. No silent substitution, CFD proxy, ETF proxy, adjacent ticker, or old QuantLab symbol is authorized by this brief.

## Source Portfolio Parameters

The P01 book example records:

| Field | Book example value | Status |
| --- | --- | --- |
| Instrument weights | 50% S&P 500 micro, 50% US 10-year bond | Source example only; must be locked before data |
| Capital | USD 1,000,000 | Source example only; operator capital rule unresolved |
| Target risk | 20% annualised standard deviation | Source example only; portfolio breadth rule unresolved |
| IDM | 1.32 | Source example only; use or recomputation must be explicitly locked |

The IDM value in the book is derived from example realised aggregate risk. This brief does not authorize calculating IDM from local historical market data. Any future IDM source must be pre-locked before market-data inspection or remain blocked.

## Required Atoms Before Data Work

P01 cannot proceed to data work until all inherited atoms and these P01-specific atoms are locked:

- Exact source-native identity for `MES` or documented source-native S&P 500 historical bridge.
- Exact source-native identity for `ZN` or documented source-native US 10-year historical bridge.
- Exact local NinjaTrader symbol mapping for both instruments.
- Exchange session, timezone, completed daily bar close, holiday calendar, and daily candle cut for both instruments.
- Daily bar synchronization rule across both instruments.
- Continuous-contract construction and roll rule for both instruments.
- Back-adjustment method for PnL for both instruments.
- Current held-contract raw price source for sizing for both instruments.
- Futures multiplier, tick size, tick value, instrument currency, base/account currency, and FX conversion for both instruments.
- Variable risk estimate per instrument using only returns completed before each sizing timestamp.
- Instrument weights: 50% / 50% or a documented source-rule blockage.
- Portfolio-level capital base.
- Portfolio-level target risk.
- Portfolio breadth rule used to justify target risk.
- IDM source and exact IDM value/rule.
- Pre-lock rule for any IDM calculation from correlations or realised aggregate risk.
- Contract-count rounding rule per leg.
- Portfolio aggregation convention for completed daily PnL.
- Portfolio cost aggregation rule.
- Cost source in `config/costs.json` once authorized.
- Fail-closed rule if either leg is missing, ineligible, too expensive, too illiquid, undercapitalized, or source-unresolved.
- Evidence-window budget if a future diagnostic/backtest is requested.

## Locked Process Decisions

The following process decisions are locked by this brief:

- P01 remains process-only until separately authorized.
- P01 is `SOURCE_NATIVE_FUTURES`, not CFD.
- P01 is a daily directional portfolio reconstruction.
- P01 uses completed daily bars only.
- P01 is reconstructed independently and not inferred from sleeve or standalone results.
- P01 does not authorize P02, P03, or P04.
- P01 does not authorize local data inspection or IDM calculation.
- P01 must prefer native daily futures candles when a future data lane is authorized.
- P01 must not reconstruct daily bars from 1-minute data by default.
- P01 must not use old QuantLab data-prep scripts, CFD adapters, broker-clock assumptions, or stale state.
- P01 must not select, drop, rescue, or reweight legs after seeing results.
- P01 must not treat historical performance as promotion evidence.
- A non-positive future P01 result does not advance and must not be rescued by tuning.

## Explicitly Unresolved

The following remain unresolved and block data/implementation work:

- Exact source-native identity for the equity leg.
- Exact source-native identity for the bond leg.
- Whether either leg requires a documented source-native historical bridge.
- Exact local NinjaTrader symbol mapping for both instruments.
- Exchange session, timezone, completed daily bar close, holiday calendar, and daily candle cut for both instruments.
- Daily bar synchronization rule across both instruments.
- Exact roll calendar and roll timing for both instruments.
- Exact continuous-contract/back-adjustment construction for both instruments.
- Treatment of raw futures price versus adjusted futures price for both instruments.
- Current held-contract raw price source for sizing for both instruments.
- Futures multiplier, tick size, tick value, instrument currency, base/account currency, and FX conversion for both instruments.
- Variable risk estimate per instrument.
- Warm-up period and first usable date per instrument.
- Instrument weights lock.
- Portfolio-level capital base.
- Portfolio-level target risk.
- Portfolio breadth rule used to justify target risk.
- IDM source and exact IDM value/rule.
- Pre-lock rule for any IDM calculation from correlations or realised aggregate risk.
- Exact contract-count rounding rule per leg.
- Portfolio aggregation convention for completed daily PnL.
- Portfolio cost aggregation rule.
- Exact cost source in `config/costs.json`.
- Fail-closed behavior for missing or invalid prices, rolls, multipliers, FX, risk estimates, costs, liquidity, capital, weights, IDM, synchronization, or sizing inputs.
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

Before this P01 brief is treated as process-safe, it must receive a hostile audit by subagent.

Audit focus:

- M0, S01, S02, S03, and S04 inheritance.
- Source-page faithfulness.
- No data or implementation leakage.
- No backtest or evidence leakage.
- No NinjaTrader operational leakage.
- No CFD or old QuantLab contamination.
- Correct complete-portfolio reconstruction interpretation.
- Correct separation from P02, P03, and P04.
- No IDM recalculation or historical-result leakage.
- Completeness of unresolved atoms.

## Next Gate

If this P01 brief is accepted after hostile audit, the next possible process-only gate is:

```text
PROCESS_ONLY_CARVER_P02_ALL_WEATHER_EXAMPLE_PORTFOLIO_BRIEF_DRAFT_NOT_DATA_NOT_STRATEGY_AUTHORIZATION
```

No P02 work is authorized by this P01 brief.

## Standing Non-Authorization

This file authorizes no data access, no market-row parsing, no implementation, no tests, no diagnostics, no backtests, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old-adapter import, no tuning, no deployment, no trading, and no promotion.


---

## Source File: `docs/researchops/portfolios/CARVER_P02_ALL_WEATHER_EXAMPLE_PORTFOLIO_BRIEF_2026-05-28.md`

# Carver P02 All Weather Example Portfolio Brief

Date: 2026-05-28

Status:

```text
PROCESS_ONLY_CARVER_P02_ALL_WEATHER_EXAMPLE_PORTFOLIO_BRIEF_DRAFT_NOT_DATA_NOT_STRATEGY_AUTHORIZATION
```

## Purpose

Create the process-only source-native futures portfolio brief for Carver Portfolio 2:

```text
P02_ALL_WEATHER_EXAMPLE_PORTFOLIO
```

This brief inherits M0, S01, S02, S03, S04, and P01. It reconstructs the P02 source framing and required atoms before any data work, implementation, test, diagnostic, backtest, OOS, Lockbox, Forward, CFD adapter, deployment, trading, or promotion.

This is a complete portfolio reconstruction brief. It is not inferred from standalone sleeve results.

## Classification

| Field | Value |
| --- | --- |
| Portfolio ID | P02 |
| Book portfolio | All Weather example portfolio |
| Book pages | `Carver.pdf`, PDF pages 124-127 |
| Lane class | `SOURCE_NATIVE_FUTURES` |
| Portfolio type | Six-instrument All Weather example |
| Member strategy machinery | S03 variable-risk buy-and-hold, wrapped by S04 portfolio construction |
| Timeframe family | Daily directional portfolio stack |
| Data posture | No data access authorized |
| Implementation posture | No implementation authorized |
| Evidence posture | No diagnostics or backtests authorized |

## Dependencies

P02 depends on:

- `docs/process/CARVER_M0_SOURCE_NATIVE_FUTURES_FOUNDATION_SPEC_2026-05-28.md`
- `docs/process/CARVER_LEAN_IMPLEMENTATION_AND_BACKTEST_DEFERRAL_RULE_2026-05-28.md`
- `docs/process/CARVER_SOURCE_NATIVE_TRANSLATION_ARCHITECTURE_GOAL_2026-05-28.md`
- `docs/researchops/handoffs/CARVER_BOOK_STRATEGY_AND_PORTFOLIO_INVENTORY_001_2026-05-28.md`
- `docs/researchops/candidates/CARVER_S01_BUY_AND_HOLD_SINGLE_CONTRACT_CANDIDATE_BRIEF_2026-05-28.md`
- `docs/researchops/candidates/CARVER_S02_BUY_AND_HOLD_WITH_RISK_SCALING_CANDIDATE_BRIEF_2026-05-28.md`
- `docs/researchops/candidates/CARVER_S03_BUY_AND_HOLD_WITH_VARIABLE_RISK_SCALING_CANDIDATE_BRIEF_2026-05-28.md`
- `docs/researchops/candidates/CARVER_S04_BUY_AND_HOLD_PORTFOLIO_WITH_VARIABLE_RISK_POSITION_SIZING_CANDIDATE_BRIEF_2026-05-28.md`
- `docs/researchops/portfolios/CARVER_P01_RISK_PARITY_EXAMPLE_PORTFOLIO_BRIEF_2026-05-28.md`

P02 is a prerequisite example for:

- P03 generalized risk premia portfolio construction.
- P04 Jumbo buy-and-hold portfolio.
- Later portfolio briefs that use asset-class buckets, sub-buckets, instrument weights, and IDM.

## Book Framing

Carver frames P02 as an All Weather extension of risk parity, adding assets that may hedge inflation and reduce dependence on the historical equity/bond correlation regime.

Source anchors:

- The All Weather variation begins on `Carver.pdf`, PDF page 124.
- Carver presents the classic All Weather cash-weight recipe as background, then distinguishes his own futures implementation on PDF pages 124-125.
- Carver states that his instrument weights reflect risk allocations rather than cash weights, because futures positions are scaled by expected standard deviation on PDF page 125.
- The P02 instrument weights are built by splitting capital into four equal buckets: stocks, bonds, commodities, and gold; then splitting bonds and commodities into two instruments each on PDF page 125.
- The P02 source weights are 25% S&P 500 micro, 12.5% US 10-year, 12.5% US 5-year, 12.5% WTI Crude Oil mini, 12.5% Corn, and 25% Gold micro on PDF page 125.
- Carver uses the same position-sizing formula as P01/S04, replacing instrument weights and instrument-specific parameters as appropriate on PDF page 125.
- The definition pack records IDM 1.81 as source context for this All Weather portfolio and the related aggregate results, but the exact value/page quote must be re-page-audited before implementation. See PDF pages 125-127.
- Tables 14 and 15 present individual and aggregate All Weather results on PDF pages 126-127; exact IDM references inside those tables must be re-page-audited before the value is quoted as locked authority.
- Carver notes the overall portfolio risk is close to the 20% target, so IDM is doing its job in the book example on PDF page 126.
- Carver warns that added diversification can still drag performance if added instruments have lower Sharpe ratios, and that backtest results should not be trusted blindly on PDF page 127.

## Portfolio Interpretation

P02 is a complete source-native futures portfolio reconstruction:

```text
SOURCE_NATIVE_FUTURES_PORTFOLIO_RECONSTRUCTION
```

P02 is not a standalone single-instrument candidate and not a sleeve result. It is the first source-defined cross-asset, six-instrument example and should be used to lock asset-bucket and sub-bucket weight handling before generalized risk premia and Jumbo portfolio work.

P02 should be used to lock these source-native portfolio primitives:

- Six source-native futures instrument identities.
- Four top-level buckets: stocks, bonds, commodities, and gold.
- Split sub-buckets for bonds and commodities.
- Instrument weights as risk allocations, not ordinary cash allocations.
- S03 variable-risk sub-strategy per instrument.
- Portfolio-level capital base.
- Portfolio-level target risk.
- IDM application.
- Completed daily PnL aggregation across six instruments.
- Portfolio cost aggregation.
- Fail-closed behavior when any leg is unavailable or unresolved.

## Portfolio Rule Skeleton

The P02 source rule skeleton is:

```text
For the six source-named All Weather futures instruments:
assign each instrument its source weight,
run an S03-style long buy-and-hold variable-risk sub-strategy for each leg,
scale each leg by its instrument weight and the locked IDM rule,
round each leg according to the locked rule,
roll each leg according to its locked source-native roll rule,
aggregate completed daily PnL across all six legs,
account for costs separately once a cost source is authorized.
```

No live rule, code rule, executable rule, test rule, diagnostic rule, backtest rule, OOS rule, Lockbox rule, Forward rule, or promotion rule is authorized by this skeleton.

## Inherited Machinery

P02 inherits:

- M0 source-native futures defaults and non-authorization.
- S01 futures identity, roll, back-adjustment, multiplier, FX, and cost atoms.
- S02 target-risk position sizing and whole-contract rounding.
- S03 variable risk estimation, non-leaking risk rule, and risk-adjusted cost atoms.
- S04 instrument weights, IDM, portfolio breadth, and multi-instrument aggregation atoms.
- P01 complete-portfolio reconstruction discipline and no-IDM-recalculation discipline.

P02 does not authorize recalculating any inherited atom from data.

## Source-Named Instruments And Weights

The P02 book example uses:

| Bucket | Instrument | Weight | Book/Appendix C market code | Exchange | Currency | Multiplier | Source |
| --- | --- | ---: | --- | --- | --- | ---: | --- |
| Stocks | S&P 500 micro future | 25.0% | `MES` | GLOBEX | USD | 5 | PDF pages 125, 692 |
| Bonds | US 10-year bond future | 12.5% | `ZN` | ECBOT | USD | 1000 | PDF pages 125, 691 |
| Bonds | US 5-year bond future | 12.5% | `ZF` | ECBOT | USD | 1000 | PDF pages 125, 691 |
| Commodities | WTI Crude Oil mini future | 12.5% | `QM` | NYMEX | USD | 500 | PDF pages 125, 695 |
| Commodities | Corn future | 12.5% | `ZC` | ECBOT | USD | 5000 | PDF pages 125, 695 |
| Gold | Gold micro future | 25.0% | `MGC` | NYMEX | USD | 10 | PDF pages 125, 694 |

Appendix C says these market codes are the codes used by Carver's broker and may differ across brokers or official exchange codes. Any future data lane must lock exact local symbol mapping, source-native contract identity, roll rules, and whether Appendix C codes match local NinjaTrader symbols. No silent substitution, CFD proxy, ETF proxy, adjacent ticker, or old QuantLab symbol is authorized by this brief.

## Source Portfolio Parameters

The P02 book example records:

| Field | Book example value | Status |
| --- | --- | --- |
| Instrument weights | 25%, 12.5%, 12.5%, 12.5%, 12.5%, 25% | Source example only; must be locked before data |
| Bucket structure | Stocks 25%, bonds 25%, commodities 25%, gold 25% | Source example only; must be locked before data |
| Target risk | 20% annualised standard deviation | Source example only; portfolio breadth rule unresolved |
| IDM | 1.81 recorded as source context pending exact quote/page re-audit | Source example only; use or recomputation must be explicitly locked |

The IDM value in the book is a source example. This brief does not authorize calculating IDM from local historical market data. Any future IDM source must be pre-locked before market-data inspection or remain blocked.

## Required Atoms Before Data Work

P02 cannot proceed to data work until all inherited atoms and these P02-specific atoms are locked:

- Exact source-native identity for each of the six instruments.
- Whether any leg requires a documented source-native historical bridge.
- Exact local NinjaTrader symbol mapping for every instrument.
- Exchange session, timezone, completed daily bar close, holiday calendar, and daily candle cut for every instrument.
- Daily bar synchronization rule across all six instruments.
- Continuous-contract construction and roll rule for every instrument.
- Back-adjustment method for PnL for every instrument.
- Current held-contract raw price source for sizing for every instrument.
- Futures multiplier, tick size, tick value, instrument currency, base/account currency, and FX conversion for every instrument.
- Variable risk estimate per instrument using only returns completed before each sizing timestamp.
- Instrument weights exactly as source-framed or a documented source-rule blockage.
- Bucket and sub-bucket structure.
- Portfolio-level capital base.
- Portfolio-level target risk.
- Portfolio breadth rule used to justify target risk.
- IDM source and exact IDM value/rule.
- Exact IDM 1.81 source quote/page verification before treating that number as locked authority.
- Pre-lock rule for any IDM calculation from correlations or realised aggregate risk.
- Contract-count rounding rule per leg.
- Portfolio aggregation convention for completed daily PnL.
- Portfolio cost aggregation rule.
- Cost source in `config/costs.json` once authorized.
- Fail-closed rule if any leg is missing, ineligible, too expensive, too illiquid, undercapitalized, or source-unresolved.
- Evidence-window budget if a future diagnostic/backtest is requested.

## Locked Process Decisions

The following process decisions are locked by this brief:

- P02 remains process-only until separately authorized.
- P02 is `SOURCE_NATIVE_FUTURES`, not CFD.
- P02 is a daily directional portfolio reconstruction.
- P02 uses completed daily bars only.
- P02 is reconstructed independently and not inferred from sleeve or standalone results.
- P02 does not authorize P03 or P04.
- P02 does not authorize local data inspection or IDM calculation.
- P02 must prefer native daily futures candles when a future data lane is authorized.
- P02 must not reconstruct daily bars from 1-minute data by default.
- P02 must not use old QuantLab data-prep scripts, CFD adapters, broker-clock assumptions, or stale state.
- P02 must not select, drop, rescue, or reweight legs after seeing results.
- P02 must not treat historical performance as promotion evidence.
- A non-positive future P02 result does not advance and must not be rescued by tuning.

## Explicitly Unresolved

The following remain unresolved and block data/implementation work:

- Exact source-native identity for each of the six instruments.
- Whether any leg requires a documented source-native historical bridge.
- Exact local NinjaTrader symbol mapping for every instrument.
- Exchange session, timezone, completed daily bar close, holiday calendar, and daily candle cut for every instrument.
- Daily bar synchronization rule across all six instruments.
- Exact roll calendar and roll timing for every instrument.
- Exact continuous-contract/back-adjustment construction for every instrument.
- Treatment of raw futures price versus adjusted futures price for every instrument.
- Current held-contract raw price source for sizing for every instrument.
- Futures multiplier, tick size, tick value, instrument currency, base/account currency, and FX conversion for every instrument.
- Variable risk estimate per instrument.
- Warm-up period and first usable date per instrument.
- Instrument weights lock.
- Bucket and sub-bucket structure lock.
- Portfolio-level capital base.
- Portfolio-level target risk.
- Portfolio breadth rule used to justify target risk.
- IDM source and exact IDM value/rule.
- Exact IDM 1.81 source quote/page verification before treating that number as locked authority.
- Pre-lock rule for any IDM calculation from correlations or realised aggregate risk.
- Exact contract-count rounding rule per leg.
- Portfolio aggregation convention for completed daily PnL.
- Portfolio cost aggregation rule.
- Exact cost source in `config/costs.json`.
- Fail-closed behavior for missing or invalid prices, rolls, multipliers, FX, risk estimates, costs, liquidity, capital, weights, buckets, IDM, synchronization, or sizing inputs.
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

Before this P02 brief is treated as process-safe, it must receive a hostile audit by subagent.

Audit focus:

- M0, S01, S02, S03, S04, and P01 inheritance.
- Source-page faithfulness.
- No data or implementation leakage.
- No backtest or evidence leakage.
- No NinjaTrader operational leakage.
- No CFD or old QuantLab contamination.
- Correct complete-portfolio reconstruction interpretation.
- Correct separation from P03 and P04.
- No IDM recalculation or historical-result leakage.
- Correct instrument mappings and weights.
- Completeness of unresolved atoms.

## Next Gate

If this P02 brief is accepted after hostile audit, the next possible process-only gate is:

```text
PROCESS_ONLY_CARVER_S09_MULTIPLE_TREND_FOLLOWING_CANDIDATE_BRIEF_DRAFT_NOT_DATA_NOT_STRATEGY_AUTHORIZATION
```

No S09 work is authorized by this P02 brief.

## Standing Non-Authorization

This file authorizes no data access, no market-row parsing, no implementation, no tests, no diagnostics, no backtests, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old-adapter import, no tuning, no deployment, no trading, and no promotion.


---

## Source File: `docs/researchops/candidates/CARVER_S09_MULTIPLE_TREND_FOLLOWING_CANDIDATE_BRIEF_2026-05-28.md`

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


---

## Source File: `docs/researchops/candidates/CARVER_S10_BASIC_CARRY_CANDIDATE_BRIEF_2026-05-28.md`

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


---

## Source File: `docs/researchops/candidates/CARVER_S11_COMBINED_CARRY_AND_TREND_CANDIDATE_BRIEF_2026-05-28.md`

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

