# Carver P05 Complete Trend Portfolio Conformance

Date: 2026-05-29

Status:

```text
PROCESS_AND_SYNTHETIC_CODE_CARVER_P05_COMPLETE_TREND_PORTFOLIO_CONFORMANCE_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Open exactly one process-and-synthetic-code conformance surface for the Carver P05 complete trend portfolio shape after the hostile-audited P05 source packet.

P05 is a Carver process label for Strategy Nine multiple trend following applied to the Jumbo futures portfolio source frame. The source packet identifies Strategy Four portfolio construction machinery, Strategy Nine trend forecast combination, and Appendix C Jumbo universe as the relevant book anchors.

This surface emits:

```text
complete-P05 desired position inputs only
```

It is not a real-data strategy, not a diagnostic, not a backtest, not a performance result, not a trading decision, not production source locking, and not portfolio execution.

## Implemented Surface

Code:

```text
src/carver/spine/p05.py
```

Synthetic tests:

```text
tests/test_p05_complete_trend_portfolio_synthetic.py
```

Public objects:

```text
P05_COMPLETE_TREND_PORTFOLIO_ID
P05_FORECAST_DIVISOR
P05_JUMBO_REFERENCE_IDM
P05_BOOK_REFERENCE_TARGET_RISK
P05_STRATEGY_NINE_COST_LIMIT_SR
P05_EWMAC_TURNOVER_BY_SPAN
P05CompleteTrendPortfolioSourceLocks
P05SyntheticMember
P05SyntheticMarketInput
P05SyntheticS09TrendForecastInput
P05EligibleEWMACSet
P05CompleteTrendPortfolioRequest
P05MemberDesiredPositionInput
P05CompleteTrendPortfolioResult
p05_handcrafted_instrument_weights
p05_complete_trend_portfolio_conformance
```

## Lane Class

```text
SOURCE_NATIVE_FUTURES
```

No `CFD_DIRECT` or `CFD_ADAPTER` lane is opened.

## Source Packet Dependency

The implementation is bounded by:

```text
docs/process/CARVER_P05_SOURCE_EXTRACT_AND_SOURCE_FAITHFULNESS_PACKET_2026-05-29.md
```

The source packet received:

```text
AUDIT_DISPOSITION: PASS_PROCESS_ONLY_SOURCE_PACKET_SCOPE
```

The code does not transcribe Appendix C or claim the local 102-member Jumbo universe is production-ready. The tests use synthetic members with synthetic contract codes.

## Synthetic Pipeline

The implementation performs only this synthetic conformance transformation:

```text
locked synthetic P05 member identity and taxonomy
locked synthetic S09 EWMAC forecast-block outputs
locked synthetic or source-cited capital, target risk, IDM, price risk, FX, and cost eligibility inputs
-> source-shaped top-down handcrafted instrument weights
-> per-member eligible EWMAC speed set
-> Strategy Nine equal forecast weights across eligible EWMAC variations
-> Strategy Nine FDM row for the eligible speed set
-> final forecast cap through shared M2 cap behavior
-> M1 position-sizing input arithmetic
-> complete-P05 desired position inputs only
```

## Explicit Locks

`P05CompleteTrendPortfolioSourceLocks` requires explicit locked status for:

- S09 input provenance;
- member identity;
- member taxonomy;
- instrument weights;
- IDM;
- target risk and capital;
- price risk;
- FX;
- cost eligibility;
- eligible EWMAC speed sets;
- forecast weights;
- trend FDM;
- forecast cap;
- position input boundary;
- output boundary.

Every field must be `LOCKED`; otherwise the gate fails closed.

## Source-Shaped Values

The module records these source-shaped constants:

| Constant | Value | Scope |
| --- | ---: | --- |
| `P05_JUMBO_REFERENCE_IDM` | 2.47 | Source-cited reference value for Jumbo, not a production data calculation. |
| `P05_BOOK_REFERENCE_TARGET_RISK` | 0.20 | Book reference target-risk value, not operator capital authorization. |
| `P05_STRATEGY_NINE_COST_LIMIT_SR` | 0.15 | Strategy Nine cost eligibility threshold, used as a source-shaped boundary. |
| `P05_FORECAST_DIVISOR` | 10.0 | Forecast-to-position input scale convention. |

Strategy Nine EWMAC turnover references:

| EWMAC span | Turnover |
| ---: | ---: |
| 2 | 98.5 |
| 4 | 50.2 |
| 8 | 25.4 |
| 16 | 13.2 |
| 32 | 7.6 |
| 64 | 5.2 |

The implementation does not calculate cost eligibility from real rows. It consumes a locked eligible speed set and prevalidated synthetic cost inputs.

## Outputs

For each synthetic P05 member, the result emits only:

- member id;
- contract identity;
- asset class and group;
- source-shaped instrument weight;
- eligible EWMAC spans;
- S09 forecast block arithmetic;
- final capped P05 forecast;
- forecast multiplier;
- M1 base sizing result;
- desired unrounded contracts;
- desired rounded contracts.

The result explicitly carries:

```text
is_synthetic_conformance = True
production_source_locked = False
interpretable_performance = False
performance_metrics = ()
return_outputs = ()
pnl_outputs = ()
trading_orders = ()
```

## Fail-Closed Behavior

The implementation fails closed when:

- lane class is not exactly `SOURCE_NATIVE_FUTURES`;
- the completed bar is incomplete, intraday, or timezone-naive;
- any required source lock is unresolved;
- member identity, taxonomy, or contract identity is unresolved;
- member ids are missing, duplicated, or drift from contract codes;
- market inputs do not exactly match the member set and order;
- S09 forecast inputs are missing, duplicated, uncapped, timestamp-misaligned, non-synthetic, or reference an unknown member;
- eligible EWMAC speed sets are missing, duplicated, out of order, unsupported, or not one of the Strategy Nine FDM rows;
- forecast inputs do not exactly match each member's eligible EWMAC speed set;
- price risk, FX, or cost eligibility inputs are not prevalidated;
- capital, target risk, or IDM is missing, non-positive, or timestamp-misaligned;
- handcrafted instrument weights do not sum to 1;
- the final forecast exceeds the shared M2 cap;
- outputs attempt to include returns, PnL, performance metrics, trading orders, production source locks, or non-synthetic claims.

## Explicit Non-Scope

This gate does not open:

- No real data;
- market-row parsing;
- NinjaTrader export;
- diagnostics;
- backtests;
- returns;
- PnL;
- Sharpe;
- drawdown;
- OOS;
- Lockbox;
- Forward;
- CFD adapters;
- old QuantLab imports;
- tuning;
- deployment;
- trading;
- promotion;
- production source locks;
- Appendix C transcription;
- local provider mapping;
- session, roll, or back-adjustment readiness;
- FX data readiness;
- cost data readiness;
- liquidity validation;
- minimum-capital validation;
- silent member dropping or substitution;
- rounding or buffering as a trading decision;
- P06/P07 portfolio work.

## Verification

Authorized synthetic verification:

```text
python -m unittest tests.test_p05_complete_trend_portfolio_synthetic -v
```

Full synthetic regression may also be run as a synthetic-only regression check because this gate adds a new isolated spine module.

## Verification Result

Synthetic verification completed on 2026-05-29.

Focused P05 verification:

```text
python -m unittest tests.test_p05_complete_trend_portfolio_synthetic -v
```

Result:

```text
8/8 passed
```

Full synthetic regression:

```text
python -m unittest discover -s tests -v
```

Result:

```text
139/139 passed
```

## Required Hostile Audit

Regular hostile audit should verify:

- code, tests, and this document match the authorized synthetic-only P05 scope;
- P05 remains a process alias for Strategy Nine Jumbo trend, not a book-native label;
- the implementation does not claim Appendix C production transcription or local provider readiness;
- synthetic member fixtures do not inflate MES/ZN/ZF phase-1 into complete P05;
- source/data/readiness atoms remain separated;
- missing members fail closed instead of being silently dropped, substituted, or reweighted;
- outputs stop at desired position inputs only;
- no real data, diagnostics, backtests, OOS, Lockbox, Forward, CFD adapters, old QuantLab active-pipeline use, deployment, trading, promotion, Opus/GPT execution, or remote operations are opened.

Regular hostile audit is lean subagent work under the current Carver process. Opus/GPT audit remains separately operator-authorized for larger source-faithfulness disputes or production-facing source locks.

## Non-Authorization

This artifact authorizes no real-data execution, no market-row parsing, no NinjaTrader export, no diagnostics, no backtests, no returns, no PnL, no Sharpe, no drawdown, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old-adapter import, no old workspace pipeline use, no tuning, no deployment, no trading, no promotion, no production source locks, no silent member dropping or substitution, no P06/P07 portfolio work, no Opus/GPT execution, no remote push, and no GitHub action.
