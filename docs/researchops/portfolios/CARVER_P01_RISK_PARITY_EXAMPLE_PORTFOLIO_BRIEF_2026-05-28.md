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
