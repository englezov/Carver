# Carver S10/M5 Carry Construction Implementation Gate Draft

Date: 2026-05-29

Status:

```text
PROCESS_ONLY_CARVER_S10_M5_CARRY_CONSTRUCTION_IMPLEMENTATION_GATE_DRAFT_NOT_AUTHORIZATION
```

## Purpose

Draft the next implementation gate after the hostile-audited post-P05 phase-1 decision:

```text
PROCESS_AND_SYNTHETIC_CODE_CARVER_S10_M5_CARRY_CONSTRUCTION_CONFORMANCE_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

This draft defines the first proposed S10/M5 synthetic carry-construction surface. It does not itself authorize code edits, tests, data access, diagnostics, backtests, or remote operations.

This draft is not process-safe until it receives a hostile audit.

## Current Locked Context

- The clean workspace is `C:\Users\openclaw\Desktop\Carver`.
- The old `C:\Users\openclaw\Desktop\QuantLab_v3` workspace remains forbidden for active pipeline work.
- S09 phase-1 multi-instrument forecast conformance exists for `MES`, `ZN`, and `ZF`.
- P05 phase-1 portfolio construction conformance exists for `MES`, `ZN`, and `ZF`.
- The post-P05 decision memo selected S10/M5 synthetic carry construction as the next clean gate and received a no-blocking-findings hostile audit.
- No real data, diagnostics, backtests, OOS, Lockbox, Forward, CFD adapters, deployment, trading, promotion, or remote push are authorized.

## Lane Class

```text
SOURCE_NATIVE_FUTURES
```

No `CFD_DIRECT` or `CFD_ADAPTER` work is opened by this draft.

## Proposed Implementation Surface

After explicit operator authorization, the gate may add a tiny synthetic-only M5 surface that takes:

- one source-native instrument identity;
- one held futures contract identity;
- one comparison futures contract identity;
- one completed-bar timestamp shared by both curve legs;
- synchronized completed daily prices for the held and comparison contracts;
- a locked raw-carry sign convention;
- a locked expiry-distance annualization convention;
- a positive expiry distance;
- a prevalidated price-risk input aligned to the same completed bar;
- locked seasonal/wrong-sign policy for the synthetic fixture;
- locked source-rule statuses for all required atoms.

The surface may emit only:

- held contract identity;
- comparison contract identity;
- raw carry price difference with sign-convention label;
- expiry distance used;
- annualized carry;
- risk-adjusted carry;
- carry timestamp and input timestamps;
- blockage reason when construction fails closed.

The intended terminal output is:

```text
risk-adjusted carry forecast input
```

That output is an M5 input into later M2/S10 machinery. It is not a complete S10 forecast, not an interpretable trading signal, and not performance evidence.

## Explicit Synthetic Convention

The synthetic conformance surface should use hand-built toy curve rows only.

The implementation may define a locked toy convention such as:

```text
raw_carry = sign_multiplier * (comparison_price - held_price)
annualized_carry = raw_carry * annualization_factor
risk_adjusted_carry = annualized_carry / price_risk
```

Where each of the following is supplied as a locked synthetic input rather than inferred from market data:

- `sign_multiplier`;
- `annualization_factor` or the expiry-distance fields used to derive it;
- `price_risk`;
- held/comparison contract roles.

This convention is allowed only for synthetic conformance. It does not settle production carry sign, production expiry calendars, production roll-day handling, production seasonal rules, or any real-data source.

## Required Fail-Closed Behavior

The future implementation must fail closed if:

- lane class is not exactly `SOURCE_NATIVE_FUTURES`;
- any source-rule status is unresolved;
- instrument identity is missing or non-source-native;
- held contract identity is missing or drifts from the request;
- comparison contract identity is missing or drifts from the request;
- held and comparison contracts are the same contract when a distinct comparison is required;
- either price is missing, non-finite, non-positive, stale, or partial;
- held and comparison timestamps are not the same completed daily bar;
- the completed bar is incomplete, naive, or intraday;
- raw-carry sign convention is unresolved;
- expiry distance or annualization convention is unresolved, zero, negative, non-finite, or stale;
- price-risk input is unresolved, stale, non-finite, or non-positive;
- seasonal/wrong-sign policy is unresolved for a synthetic case that requires it;
- any CFD, ETF, adjacent proxy, old adapter, old broker-clock assumption, or old `QuantLab_v3` symbol is supplied;
- the result attempts to emit returns, PnL, Sharpe, drawdown, diagnostics, backtest metrics, positions, smoothing, FDM, caps, costs, or portfolio aggregation.

## Explicit Non-Scope

This gate draft does not open:

- full S10 Carry5/20/60/120 smoothing;
- carry forecast scalar `30`;
- carry span caps;
- carry FDM rows;
- carry span cost eligibility;
- forecast weighting;
- forecast-scaled position sizing;
- buffering or trade/no-trade decisions;
- P06 Jumbo carry portfolio;
- P07 combined trend/carry portfolio;
- S11 combined trend/carry;
- real curve data;
- provider mapping;
- NinjaTrader export;
- market-row parsing;
- diagnostics or backtests.

Those require separate future gates.

## Suggested Code Surface After Authorization

If the operator authorizes implementation, keep the write set narrow:

```text
src/carver/spine/m5.py
tests/test_s10_m5_carry_construction_synthetic.py
docs/process/CARVER_S10_M5_CARRY_CONSTRUCTION_CONFORMANCE_2026-05-29.md
src/carver/spine/__init__.py
```

The code should reuse existing M0 concepts where possible:

- `LaneClass`;
- `CarverBlocked`;
- `CompletedBar`;
- `SourceRuleStatus`;
- finite-positive validation patterns;
- source-native lane guards.

The test surface should use only toy synthetic values and should verify:

- one positive carry construction case;
- one negative carry construction case;
- exact timestamp alignment;
- completed daily bar enforcement;
- source-native lane enforcement;
- unresolved source-rule rejection;
- invalid price/risk/expiry rejection;
- sign-convention lock enforcement;
- no performance or position output.

## Hostile Audit Requirement

Before this draft gate is treated as process-safe, a hostile audit should verify:

- no implementation authorization is smuggled into the draft;
- no real data or market-row parsing is opened;
- no diagnostics, backtests, OOS, Lockbox, Forward, deployment, trading, or promotion leakage exists;
- no CFD adapter or old `QuantLab_v3` contamination exists;
- M5 stops at risk-adjusted carry input into M2;
- full S10 smoothing, FDM, caps, cost eligibility, position sizing, and S11 remain closed;
- synthetic conventions are clearly synthetic and do not claim production source locks;
- fail-closed rules cover unresolved carry atoms and tuning-after-results risk.

## Hostile Audit Result

Subagent hostile audit completed on 2026-05-29.

Audit disposition:

- No blocking findings.
- The draft does not smuggle implementation authorization.
- The draft does not open real data, market-row parsing, diagnostics, backtests, OOS, Lockbox, Forward, deployment, trading, promotion, CFD adapter work, old `QuantLab_v3` use, NinjaTrader export, or remote operations.
- The draft stops M5 at risk-adjusted carry input into M2/S10 machinery.
- Full S10 smoothing, FDM, caps, cost eligibility, position sizing, S11, P06, and P07 remain closed.
- The synthetic convention is clearly toy-only and does not claim production source locks.
- Fail-closed rules cover unresolved carry atoms and block performance or tuning-adjacent outputs.
- No files were edited by the auditor.

## Suggested Authorization Prompt

```text
Operator authorizes exactly one process-and-synthetic-code gate for the Carver
S10/M5 carry construction conformance surface.

Scope:
Clean Carver workspace only. Implement a tiny synthetic-only M5 surface that
converts locked toy held/comparison futures contract prices, locked sign
convention, locked expiry annualization, and prevalidated price risk into a
risk-adjusted carry forecast input.

Allowed:
Code contracts, synthetic tests, and process documentation for M5 carry
construction conformance only.

Forbidden:
No real-data execution, no market-row parsing, no NinjaTrader export, no
diagnostics, no backtests, no returns, no PnL, no Sharpe, no drawdown, no OOS,
no Lockbox, no Forward, no CFD adapters, no old QuantLab imports, no tuning, no
deployment, no trading, no promotion, no S10 smoothing/FDM/caps/cost eligibility,
no S11, and no P06/P07 portfolio work.

Required:
Completed bars only. Source-native futures only. Fail closed unless all source
atoms are locked. Use hostile audit before treating the surface as process-safe.

Required status:
PROCESS_AND_SYNTHETIC_CODE_CARVER_S10_M5_CARRY_CONSTRUCTION_CONFORMANCE_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Non-Authorization

This draft authorizes no code edits, no tests, no data access, no market-row parsing, no NinjaTrader export, no diagnostics, no backtests, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old-adapter import, no old workspace pipeline use, no tuning, no deployment, no trading, no promotion, no remote push, and no GitHub action.
