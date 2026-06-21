# Carver P07 Complete Combined Trend/Carry Portfolio Conformance

Date: 2026-05-29

Status:

```text
PROCESS_AND_SYNTHETIC_CODE_CARVER_P07_COMPLETE_COMBINED_TREND_CARRY_PORTFOLIO_CONFORMANCE_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Open exactly one process-and-synthetic-code conformance surface for the Carver P07 complete combined trend/carry portfolio shape after the hostile-audited P07 source packet.

P07 is a Carver process label for Strategy Eleven combined carry and trend applied to the Jumbo futures portfolio source frame. The source packet identifies Strategy Four portfolio construction machinery, Strategy Eleven combined forecast construction, and Appendix C Jumbo universe as the relevant book anchors.

This surface emits:

```text
complete-P07 desired position inputs only
```

It is not a real-data strategy, not a diagnostic, not a backtest, not a performance result, not a trading decision, not production source locking, and not portfolio execution.

## Implemented Surface

Code:

```text
src/carver/spine/p07.py
```

Synthetic tests:

```text
tests/test_p07_complete_combined_trend_carry_portfolio_synthetic.py
```

Public objects:

```text
P07_COMPLETE_COMBINED_TREND_CARRY_PORTFOLIO_ID
P07_FORECAST_DIVISOR
P07_JUMBO_REFERENCE_IDM
P07_BOOK_REFERENCE_TARGET_RISK
P07_STRATEGY_ELEVEN_COST_LIMIT_SR
P07CompleteCombinedPortfolioSourceLocks
P07SyntheticMember
P07SyntheticMarketInput
P07SyntheticS11CombinedForecastInput
P07CompleteCombinedPortfolioRequest
P07MemberDesiredPositionInput
P07CompleteCombinedPortfolioResult
p07_handcrafted_instrument_weights
p07_complete_combined_trend_carry_portfolio_conformance
```

## Lane Class

```text
SOURCE_NATIVE_FUTURES
```

No `CFD_DIRECT` or `CFD_ADAPTER` lane is opened.

## Source Packet Dependency

The implementation is bounded by:

```text
docs/process/CARVER_P07_SOURCE_EXTRACT_AND_SOURCE_FAITHFULNESS_PACKET_2026-05-29.md
docs/process/CARVER_P07_SOURCE_EXTRACT_AND_SOURCE_FAITHFULNESS_PACKET_HOSTILE_AUDIT_RESULT_2026-05-29.md
```

The source packet received:

```text
NO BLOCKING FINDINGS
AUDIT_DISPOSITION: PASS_PROCESS_ONLY_SOURCE_PACKET_SCOPE
```

The code does not transcribe Appendix C or claim the local 102-member Jumbo universe is production-ready. The tests use synthetic members with synthetic contract codes.

## Synthetic Pipeline

The implementation performs only this synthetic conformance transformation:

```text
locked synthetic P07 member identity and taxonomy
locked synthetic S11 combined carry/trend forecast outputs
locked synthetic or source-shaped capital, target risk, IDM, price risk, FX, and cost eligibility inputs
-> source-shaped top-down handcrafted instrument weights
-> final forecast cap validation
-> M1 position-sizing input arithmetic
-> complete-P07 desired position inputs only
```

The P07 source packet resolves the dependency shape to direct locked synthetic S11 combined forecasts. P07 does not combine P05 and P06 desired-position outputs.

## Explicit Locks

`P07CompleteCombinedPortfolioSourceLocks` requires explicit locked status for:

- S11 input provenance;
- member identity;
- member taxonomy;
- instrument weights;
- IDM;
- target risk and capital;
- price risk;
- FX;
- cost eligibility;
- forecast cap;
- position input boundary;
- output boundary.

Every field must be `LOCKED`; otherwise the gate fails closed.

## Source-Shaped Values

The module records these source-shaped constants:

| Constant | Value | Scope |
| --- | ---: | --- |
| `P07_JUMBO_REFERENCE_IDM` | 2.47 | Source-cited reference value for Jumbo, not a production data calculation. |
| `P07_BOOK_REFERENCE_TARGET_RISK` | 0.20 | Book reference target-risk value, not operator capital authorization. |
| `P07_STRATEGY_ELEVEN_COST_LIMIT_SR` | 0.15 | Strategy Eleven trading-rule eligibility threshold inherited from the multiple-rule framework. |
| `P07_FORECAST_DIVISOR` | 10.0 | Forecast-to-position input scale convention. |

The implementation does not calculate cost eligibility from real rows. It consumes prevalidated synthetic cost inputs and locked synthetic S11 forecast outputs.

## Outputs

For each synthetic P07 member, the result emits only:

- member id;
- contract identity;
- asset class and group;
- source-shaped instrument weight;
- final capped S11 combined carry/trend forecast;
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
- S11 combined forecast inputs are missing, duplicated, non-synthetic, uncapped, timestamp-misaligned, or reference an unknown member;
- price risk, FX, or cost eligibility inputs are not prevalidated;
- capital, target risk, or IDM is missing, non-positive, or timestamp-misaligned;
- handcrafted instrument weights do not sum to 1;
- the final S11 combined forecast exceeds the shared M2 cap;
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
- production trend calculation;
- production carry construction;
- Strategy Eleven Table 51 production row selection;
- Strategy Eleven Table 52 production FDM values;
- local cost eligibility calculation;
- session, roll, or back-adjustment readiness;
- FX data readiness;
- cost data readiness;
- liquidity validation;
- minimum-capital validation;
- silent member dropping or substitution;
- rounding or buffering as a trading decision;
- P05/P06 desired-position output combination;
- portfolio aggregation or execution.

## Verification

Authorized synthetic verification:

```text
python -m unittest tests.test_p07_complete_combined_trend_carry_portfolio_synthetic -v
```

Full synthetic regression may also be run as a synthetic-only regression check because this gate adds a new isolated spine module and module exports.

## Verification Result

Synthetic verification completed on 2026-05-29.

Focused P07 verification:

```text
python -m unittest tests.test_p07_complete_combined_trend_carry_portfolio_synthetic -v
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
155/155 passed
```

## Required Hostile Audit

Regular hostile audit should verify:

- code, tests, and this document match the authorized synthetic-only P07 scope;
- P07 remains a process alias for Strategy Eleven Jumbo combined carry/trend, not a book-native label;
- the implementation consumes locked synthetic S11 combined forecasts, not P05/P06 desired-position outputs;
- the implementation does not claim Appendix C production transcription or local provider readiness;
- synthetic member fixtures do not inflate toy members into complete production P07;
- source/data/readiness atoms remain separated;
- production trend and carry construction remain closed;
- missing members fail closed instead of being silently dropped, substituted, or reweighted;
- outputs stop at desired position inputs only;
- no real data, diagnostics, backtests, OOS, Lockbox, Forward, CFD adapters, old QuantLab active-pipeline use, deployment, trading, promotion, Opus/GPT execution, or remote operations are opened.

Regular hostile audit is lean subagent work under the current Carver process. Opus/GPT audit remains separately operator-authorized for larger source-faithfulness disputes or production-facing source locks.

## Non-Authorization

This artifact authorizes no real-data execution, no market-row parsing, no NinjaTrader export, no diagnostics, no backtests, no returns, no PnL, no Sharpe, no drawdown, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old-adapter import, no old workspace pipeline use, no tuning, no deployment, no trading, no promotion, no production source locks, no silent member dropping or substitution, no Opus/GPT execution, no remote push, and no GitHub action.
