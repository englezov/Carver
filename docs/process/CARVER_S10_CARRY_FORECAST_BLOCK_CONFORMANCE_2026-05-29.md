# Carver S10 Carry Forecast-Block Conformance

Date: 2026-05-29

Status:

```text
PROCESS_AND_SYNTHETIC_CODE_CARVER_S10_CARRY_FORECAST_BLOCK_CONFORMANCE_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Open exactly one process-and-synthetic-code implementation surface for the Carver Strategy Ten carry forecast block after the hostile-audited S10 carry forecast-block extension gate draft.

This surface starts from locked synthetic M5 risk-adjusted carry input history and emits:

```text
final capped S10 carry forecast output
```

It is not a real-data strategy, not a diagnostic, not a backtest, not a trading signal, not a position, not a portfolio result, and not performance evidence.

## Implemented Surface

Code:

```text
src/carver/spine/s10.py
```

Synthetic tests:

```text
tests/test_s10_carry_forecast_block_synthetic.py
```

Public objects:

```text
S10_CARRY_SPANS
S10_CARRY_SCALAR
S10_CARRY_FDM_ROWS
S10M5RiskAdjustedCarryInput
S10CarryForecastBlockSourceLocks
S10CarrySpanForecast
S10CarryForecastBlockRequest
S10CarryForecastBlockResult
s10_carry_rule_id
s10_carry_fdm_for_eligible_spans
s10_carry_forecast_block_conformance
```

## Lane Class

```text
SOURCE_NATIVE_FUTURES
```

No `CFD_DIRECT` or `CFD_ADAPTER` work is opened by this gate.

## Synthetic Forecast Pipeline

The implementation performs only this synthetic conformance transformation:

```text
locked M5 risk-adjusted carry input history
-> synthetic EWMA Carry5/20/60/120 smoothing
-> scalar 30 through M2 ForecastRuleInput
-> individual forecast cap 20 through M2
-> locked eligible carry span set
-> equal weights across eligible spans through M2
-> carry FDM by eligible span set
-> final combined cap 20 through M2
-> final capped S10 carry forecast output
```

The implementation reuses existing M2 forecast-block primitives:

```text
ForecastRuleInput
ForecastBlockRequest
combine_forecast_block
FORECAST_CAP
```

S10 adds only carry-specific constants, synthetic carry-input history validation, carry rule identifiers, and the S10 wrapper that enforces explicit S10 locks before calling M2.

## Locked Synthetic Values

Allowed carry spans:

```text
5
20
60
120
```

Carry scalar:

```text
30
```

Shared M2 synthetic forecast cap:

```text
20
```

Allowed eligible span sets and FDM rows:

| Eligible spans | Equal weight | FDM |
| --- | ---: | ---: |
| Carry5, Carry20, Carry60, Carry120 | 0.25 | 1.04 |
| Carry20, Carry60, Carry120 | 0.3333333333 | 1.03 |
| Carry60, Carry120 | 0.5 | 1.02 |
| Carry120 | 1.0 | 1.0 |

These are synthetic conformance locks only. Production source locks still require future narrow page-cited source extracts and audit.

## Explicit S10 Locks

The implementation follows the draft-audit forward constraint:

```text
DO_NOT_RELY_ON_M2_DEFAULT_LOCKED_ERGONOMICS
```

`S10CarryForecastBlockSourceLocks` requires explicit status for:

- M5 input provenance;
- carry input history;
- smoothing span set;
- scalar;
- cap;
- eligible span set;
- equal weights;
- FDM;
- output boundary.

Each must be `LOCKED` before the S10 wrapper calls M2.

## Outputs

The conformance result emits only:

- completed-bar timestamp;
- smoothed risk-adjusted carry forecasts for eligible spans;
- M2 forecast-block details for scalar, cap, equal weights, FDM, and final cap;
- final capped S10 carry forecast output.

The result explicitly carries:

```text
interpretable_trading_signal = False
performance_metrics = ()
position_outputs = ()
```

## Fail-Closed Behavior

The implementation fails closed when:

- lane class is not exactly `SOURCE_NATIVE_FUTURES`;
- any required S10 lock is unresolved;
- M5 carry input labels are not explicitly synthetic;
- M5 carry input status is unresolved;
- M5 input values are non-finite;
- input history is shorter than the largest requested eligible span;
- timestamps are naive, intraday, duplicated, unsorted, stale, or not on the synthetic daily cadence;
- eligible span set is empty, duplicated, unordered, contains unsupported spans, or lacks a source-permitted FDM row;
- scalar is not locked to 30;
- cap is not locked to the shared M2 synthetic cap;
- M2 scalar, cap, weight, FDM, or eligibility source status is unresolved;
- outputs attempt to include performance, trading, or position outputs.

## Explicit Non-Scope

This gate does not open:

- No real-data execution;
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
- production raw-carry sign conventions;
- production expiry calendars;
- production roll-day handling;
- fixed-month commodity rules;
- seasonal or wrong-sign policies;
- real-data cost eligibility;
- forecast-scaled position sizing;
- buffering or trade/no-trade decisions;
- S11 combined trend/carry;
- P06 Jumbo carry;
- P07 combined trend/carry portfolio.

## Verification

Authorized synthetic verification:

```text
python -m unittest tests.test_s10_carry_forecast_block_synthetic -v
```

Because this gate reuses shared M2 forecast-block primitives and adds exports, full synthetic regression may also be run as a broader synthetic-only regression check.

## Verification Result

Synthetic verification completed on 2026-05-29.

Focused S10 verification:

```text
python -m unittest tests.test_s10_carry_forecast_block_synthetic -v
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
124/124 passed
```

## Required Hostile Audit

Before this implemented surface is treated as process-safe, a hostile audit should verify:

- the code and tests match the authorized synthetic-only S10 carry forecast-block scope;
- S10 enforces explicit locks before calling M2 and does not rely on M2 default-`LOCKED` ergonomics;
- M2 is reused only for scalar, cap, equal weights, FDM, and final cap behavior;
- no real data, market-row parsing, diagnostics, backtests, OOS, Lockbox, Forward, CFD adapter, deployment, trading, promotion, or remote operation is opened;
- S10 stops at final capped carry forecast output;
- position sizing, buffering, trade/no-trade decisions, S11, P06, and P07 remain closed;
- synthetic conventions remain toy-only and do not claim production source locks.

## Suggested Hostile Audit Authorization Prompt

```text
Operator authorizes exactly one regular hostile audit of the Carver S10 carry
forecast-block conformance implementation.

Scope:
Audit the process-and-synthetic-code S10 carry forecast-block surface:
src/carver/spine/s10.py
tests/test_s10_carry_forecast_block_synthetic.py
docs/process/CARVER_S10_CARRY_FORECAST_BLOCK_CONFORMANCE_2026-05-29.md

Allowed:
Read-only file inspection and, if needed, synthetic-only test execution for:
python -m unittest tests.test_s10_carry_forecast_block_synthetic -v

Forbidden:
No file edits, no real data, no market-row parsing, no NinjaTrader export, no
diagnostics, no backtests, no returns, no PnL, no Sharpe, no drawdown, no OOS,
no Lockbox, no Forward, no CFD adapters, no Opus execution, no remote
operations, no deployment, no trading, no promotion, no production source
locks, no S11, and no P06/P07 portfolio work.
```

## Non-Authorization

This artifact authorizes no real-data execution, no market-row parsing, no NinjaTrader export, no diagnostics, no backtests, no returns, no PnL, no Sharpe, no drawdown, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old-adapter import, no old workspace pipeline use, no tuning, no deployment, no trading, no promotion, no production source locks, no forecast-scaled position sizing, no buffering or trade/no-trade decisions, no S11, no P06/P07 portfolio work, no remote push, and no GitHub action.
