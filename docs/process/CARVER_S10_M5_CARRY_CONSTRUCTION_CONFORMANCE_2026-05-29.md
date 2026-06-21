# Carver S10/M5 Carry Construction Conformance

Date: 2026-05-29

Status:

```text
PROCESS_AND_SYNTHETIC_CODE_CARVER_S10_M5_CARRY_CONSTRUCTION_CONFORMANCE_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Open exactly one synthetic-only implementation surface for M5 futures-curve carry construction after the hostile-audited S10/M5 draft gate.

The surface converts locked toy held/comparison futures contract prices, locked synthetic sign convention, locked expiry annualization, and prevalidated price risk into:

```text
risk-adjusted carry forecast input
```

This is an M5 output into later M2/S10 machinery. It is not a complete S10 forecast, not an interpretable trading signal, not a position, not a portfolio result, and not performance evidence.

## Implemented Surface

Code:

```text
src/carver/spine/m5.py
```

Synthetic tests:

```text
tests/test_s10_m5_carry_construction_synthetic.py
```

Public objects:

```text
M5CarryConstructionSourceLocks
M5RawCarrySignConvention
M5CarryConstructionRequest
M5CarryConstructionResult
m5_synthetic_carry_construction_conformance
```

## Lane Class

```text
SOURCE_NATIVE_FUTURES
```

No `CFD_DIRECT` or `CFD_ADAPTER` work is opened by this gate.

## Synthetic Convention

The implementation is locked only for toy synthetic conformance:

```text
raw_carry = sign_multiplier * (comparison_price - held_price)
annualization_factor = 1 / expiry_distance_years
annualized_carry = raw_carry * annualization_factor
risk_adjusted_carry = annualized_carry / price_risk
```

The sign multiplier, expiry distance, held/comparison contract roles, and price risk are supplied as locked synthetic inputs. They are not inferred from market data.

This convention does not settle production carry sign, production expiry calendars, production roll-day handling, production seasonal policy, production wrong-sign policy, source-native provider mapping, or any real-data source.

## Inputs

The conformance request requires:

- source-native instrument identity;
- held contract identity and contract month;
- comparison contract identity and contract month;
- synchronized completed daily prices for held and comparison contracts;
- locked raw-carry sign convention;
- locked expiry distance in years;
- locked prevalidated price-risk input;
- locked source-rule statuses for instrument identity, curve contracts, completed prices, sign convention, expiry distance, price risk, and seasonal/wrong-sign policy.

## Outputs

The conformance result emits only:

- instrument identity;
- held contract month;
- comparison contract month;
- sign-convention label;
- raw carry;
- expiry distance;
- annualization factor;
- annualized carry;
- risk-adjusted carry;
- timestamps used for the carry calculation.

The result explicitly carries:

```text
interpretable_trading_signal = False
performance_metrics = ()
position_outputs = ()
```

## Fail-Closed Behavior

The implementation fails closed when:

- lane class is not exactly `SOURCE_NATIVE_FUTURES`;
- any required source lock is unresolved;
- instrument, held contract, or comparison contract identity drifts;
- held and comparison contract months are not distinct;
- either curve leg is stale, partial, incomplete, intraday, naive, non-finite, or non-positive;
- held and comparison prices do not share the same completed daily timestamp;
- price risk is stale, non-finite, non-positive, or timestamp-misaligned;
- expiry distance is stale, non-finite, non-positive, or timestamp-misaligned;
- sign convention is unresolved, unnamed, non-finite, or not exactly `+1` or `-1`;
- the result attempts to emit performance, trading, or position outputs.

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
- S10 smoothing;
- S10 FDM;
- S10 caps;
- S10 cost eligibility;
- S10 position sizing;
- S11 combined trend/carry;
- P06 Jumbo carry;
- P07 combined trend/carry portfolio.

## Verification

Authorized synthetic verification:

```text
python -m unittest tests.test_s10_m5_carry_construction_synthetic -v
```

Full-suite synthetic verification may be run as a broader regression check, but this gate itself claims only the S10/M5 synthetic conformance surface.

## Hostile Audit Requirement

Before this implemented surface is treated as process-safe, a hostile audit should verify:

- the code and tests match the authorized synthetic-only M5 scope;
- no real data, market-row parsing, diagnostics, backtests, OOS, Lockbox, Forward, CFD adapter, deployment, trading, promotion, or remote operation is opened;
- M5 stops at risk-adjusted carry input into M2/S10 machinery;
- full S10 smoothing, FDM, caps, cost eligibility, position sizing, S11, P06, and P07 remain closed;
- synthetic conventions remain toy-only and do not claim production source locks;
- fail-closed behavior covers unresolved carry atoms and tuning-after-results risk.

## Hostile Audit Result

Subagent hostile audit completed on 2026-05-29.

Audit disposition:

- No blocking findings.
- The code and tests match the authorized synthetic-only M5 scope.
- M5 stops at risk-adjusted carry input into M2/S10 machinery.
- Source-native lane and source-lock fail-closed behavior are enforced.
- Completed daily bar and timestamp alignment are enforced.
- Real data, diagnostics, backtests, CFD adapters, S10 smoothing/FDM/caps/cost eligibility/position sizing, S11, P06, and P07 remain explicitly closed.
- The Opus escalation reminder is present and does not self-authorize Opus execution.
- Audit verification ran `python -m unittest tests.test_s10_m5_carry_construction_synthetic -v` and passed 8/8.
- No files were edited by the auditor.
- No real data, diagnostics, backtests, adapter work, NinjaTrader export, remote operations, or old workspace access were performed.

## Opus Escalation Reminder

Use an Opus hostile source-faithfulness audit before any future gate attempts to lock production carry interpretation from the book, including:

- raw carry sign conventions beyond toy synthetic labels;
- production expiry calendars or month-distance conventions;
- production roll-day handling;
- fixed-month commodity rules;
- seasonal or wrong-sign carry policies;
- full S10 smoothing, FDM, caps, cost eligibility, or forecast weighting;
- S11 combined trend/carry source weighting or FDM interpretation.

This reminder does not authorize Opus execution by itself.

## Next Boundary

After this gate, the next decision is whether to:

- extend to full S10 smoothing/FDM/caps/cost eligibility under a separate explicit gate; or
- keep S10 paused and open a separate process decision about S11 readiness.

Neither is authorized by this file.

## Non-Authorization

This artifact authorizes no real-data execution, no market-row parsing, no NinjaTrader export, no diagnostics, no backtests, no returns, no PnL, no Sharpe, no drawdown, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old-adapter import, no old workspace pipeline use, no tuning, no deployment, no trading, no promotion, no S10 smoothing/FDM/caps/cost eligibility/position sizing, no S11, no P06/P07 portfolio work, no remote push, and no GitHub action.
