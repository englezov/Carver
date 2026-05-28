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
