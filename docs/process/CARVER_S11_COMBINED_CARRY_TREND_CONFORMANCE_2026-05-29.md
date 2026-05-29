# Carver S11 Combined Carry/Trend Conformance

Date: 2026-05-29

Status:

```text
PROCESS_AND_SYNTHETIC_CODE_CARVER_S11_COMBINED_CARRY_TREND_CONFORMANCE_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Open exactly one process-and-synthetic-code conformance surface for Carver Strategy Eleven combined carry/trend after the hostile-audited S11 gate draft.

This surface consumes locked synthetic S09 trend forecast-block outputs and locked synthetic S10 carry forecast-block outputs, then emits:

```text
final capped S11 combined carry/trend forecast output
```

It is not a real-data strategy, not a diagnostic, not a backtest, not a trading signal, not a position, not a portfolio result, and not performance evidence.

## Implemented Surface

Code:

```text
src/carver/spine/s11.py
```

Synthetic tests:

```text
tests/test_s11_combined_carry_trend_synthetic.py
```

Public objects:

```text
S11ForecastStyle
S11_SOURCE_STYLE_WEIGHTS
S11CombinedCarryTrendSourceLocks
S11SyntheticForecastInput
S11CombinedForecastRuleResult
S11CombinedCarryTrendConformanceRequest
S11CombinedCarryTrendConformanceResult
s11_combined_carry_trend_conformance
```

## Lane Class

```text
SOURCE_NATIVE_FUTURES
```

No `CFD_DIRECT` or `CFD_ADAPTER` work is opened by this gate.

## Synthetic Forecast Pipeline

The implementation performs only this synthetic conformance transformation:

```text
locked synthetic S09 trend forecast-block outputs
locked synthetic S10 carry forecast-block outputs
-> explicit S11 style grouping: trend = divergent, carry = convergent
-> explicit S11 60/40 style mix
-> explicit top-down style/rule/variation weights
-> locked eligible rule set
-> locked synthetic S11 FDM
-> final combined forecast cap through shared M2 cap behavior
-> final capped S11 combined carry/trend forecast output
```

The S11 implementation uses the shared M2 forecast cap value and cap function:

```text
FORECAST_CAP
cap_forecast
```

It does not use M2 equal-weight combination because S11 requires top-down style/rule/variation weights.

## Explicit S11 Locks

`S11CombinedCarryTrendSourceLocks` requires explicit status for:

- S09 input provenance;
- S10 input provenance;
- style grouping;
- style mix;
- top-down forecast weights;
- eligible rule set;
- S11 FDM;
- combined cap;
- output boundary.

Each must be `LOCKED` before the S11 wrapper constructs the combined forecast.

## Synthetic Values

Style grouping:

| Style | Synthetic label |
| --- | --- |
| Trend | `TREND_DIVERGENT` |
| Carry | `CARRY_CONVERGENT` |

Style mix:

| Style | Weight |
| --- | ---: |
| Trend | 0.60 |
| Carry | 0.40 |

The 60/40 mix is a synthetic conformance lock for this gate. It is not a production source lock and must remain subject to future source-faithfulness audit before any production-facing use.

S11 FDM is supplied as a locked synthetic request input with a synthetic label and a locked remaining-rule count. This gate does not lock Table 52 production values, interpolation policy, table rows, table page labels, or worked examples.

## Outputs

The conformance result emits only:

- completed-bar timestamp;
- per-rule input capped forecast;
- style, rule, variation, and top-down weights;
- pre-FDM combined forecast;
- locked synthetic S11 FDM;
- post-FDM combined forecast;
- final capped S11 combined carry/trend forecast output.

The result explicitly carries:

```text
interpretable_trading_signal = False
performance_metrics = ()
position_outputs = ()
```

## Fail-Closed Behavior

The implementation fails closed when:

- lane class is not exactly `SOURCE_NATIVE_FUTURES`;
- any required S11 lock is unresolved;
- any synthetic input label does not start with `synthetic_`;
- any S09/S10 synthetic input source is unresolved;
- any input timestamp is not aligned to the completed bar;
- any completed bar is incomplete, intraday, or timezone-naive;
- any input forecast is non-finite;
- any input forecast is not already capped to the shared M2 cap;
- any trend input does not use an `EWMAC` rule id;
- any carry input does not use a `Carry` rule id;
- the eligible rule set is empty, duplicated, missing, extra, or out of order versus supplied inputs;
- both trend and carry styles are not present;
- style weights do not match the explicit 60/40 style mix;
- top-down weights do not sum to 1;
- top-down weights do not sum to the locked style weights inside each style;
- S11 FDM is non-positive, non-finite, not synthetic-labeled, or does not match the locked eligible rule count;
- outputs attempt to include performance, trading, or position fields.

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
- Table 51 production row selection, although the table page is book-verified at PDF page 268;
- Table 52 production FDM values, although the table page is book-verified at PDF page 269;
- Table 52 interpolation policy, although the interpolation language is book-verified at PDF page 269;
- production use of the `0.15 SR` cost-units threshold, although the source threshold is book-verified at PDF page 216;
- forecast-scaled position sizing;
- buffering or trade/no-trade decisions;
- S11 portfolio execution;
- P05/P06/P07 portfolio work.

## Verification

Authorized synthetic verification:

```text
python -m unittest tests.test_s11_combined_carry_trend_synthetic -v
```

Because this gate adds a new module export and uses shared M2 cap behavior, full synthetic regression may also be run as a broader synthetic-only regression check.

## Verification Result

Synthetic verification completed on 2026-05-29.

Focused S11 verification:

```text
python -m unittest tests.test_s11_combined_carry_trend_synthetic -v
```

Result:

```text
7/7 passed
```

Full synthetic regression:

```text
python -m unittest discover -s tests -v
```

Result:

```text
131/131 passed
```

## Required Hostile Audit

Before this implemented surface is treated as process-safe, a hostile audit should verify:

- the code and tests match the authorized synthetic-only S11 combined carry/trend conformance scope;
- S11 enforces explicit locks before combining inputs;
- S11 uses abstract synthetic S09/S10 forecast-block fixtures rather than instrument-specific phase-1 optics;
- S11 does not rely on M2 equal-weight combination for top-down weighting;
- final cap uses shared M2 cap behavior;
- no real data, market-row parsing, diagnostics, backtests, OOS, Lockbox, Forward, CFD adapter, deployment, trading, promotion, remote operation, or old QuantLab active-pipeline use is opened;
- S11 stops at final capped combined forecast output;
- position sizing, buffering, trade/no-trade decisions, P05/P06/P07, production source locks, and Table 51/Table 52 production locks remain closed.

## Suggested Hostile Audit Authorization Prompt

```text
Operator authorizes exactly one regular hostile audit of the Carver S11 combined
carry/trend conformance implementation.

Scope:
Audit the process-and-synthetic-code S11 combined carry/trend surface:
src/carver/spine/s11.py
tests/test_s11_combined_carry_trend_synthetic.py
docs/process/CARVER_S11_COMBINED_CARRY_TREND_CONFORMANCE_2026-05-29.md

Allowed:
Read-only file inspection and, if needed, synthetic-only test execution for:
python -m unittest tests.test_s11_combined_carry_trend_synthetic -v

Forbidden:
No file edits, no real data, no market-row parsing, no NinjaTrader export, no
diagnostics, no backtests, no returns, no PnL, no Sharpe, no drawdown, no OOS,
no Lockbox, no Forward, no CFD adapters, no Opus execution, no remote
operations, no deployment, no trading, no promotion, no production source locks,
no forecast-scaled position sizing, no buffering or trade/no-trade decisions,
no S11 portfolio execution, and no P05/P06/P07 portfolio work.
```

## Non-Authorization

This artifact authorizes no real-data execution, no market-row parsing, no NinjaTrader export, no diagnostics, no backtests, no returns, no PnL, no Sharpe, no drawdown, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old-adapter import, no old workspace pipeline use, no tuning, no deployment, no trading, no promotion, no production source locks, no forecast-scaled position sizing, no buffering or trade/no-trade decisions, no S11 portfolio execution, no P05/P06/P07 portfolio work, no Opus execution, no remote push, and no GitHub action.
