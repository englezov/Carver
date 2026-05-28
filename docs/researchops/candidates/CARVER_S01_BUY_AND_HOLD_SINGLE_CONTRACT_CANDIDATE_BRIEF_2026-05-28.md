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
