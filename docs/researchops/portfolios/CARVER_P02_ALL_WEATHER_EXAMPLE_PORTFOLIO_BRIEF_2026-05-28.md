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
