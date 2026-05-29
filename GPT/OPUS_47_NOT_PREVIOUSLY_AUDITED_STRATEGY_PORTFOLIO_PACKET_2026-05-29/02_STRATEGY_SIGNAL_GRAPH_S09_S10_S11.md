# Strategy Signal Graph: S09, S10, S11

Date: 2026-05-29

Status:

```text
OPUS_47_AUDIT_INPUT_STRATEGY_SIGNAL_GRAPH_S09_S10_S11_NOT_DATA_NOT_BACKTEST
```

## Purpose

Summarize the not-yet-Opus-audited Carver signal graph after the early definition audit and the S10/M5 Opus 4.7 audit.

This file is an audit input only. It authorizes no implementation, tests, data work, diagnostics, backtests, OOS, Lockbox, Forward, CFD adapters, deployment, trading, or promotion.

## Source Chapters To Inspect

Use `00_Carver.pdf` as source authority.

Primary source areas:

| Area | PDF pages | Audit use |
| --- | ---: | --- |
| Strategy Nine multiple trend following | 201-227 | EWMAC variations, trend scalars, forecast caps, speed/cost eligibility, equal weights, FDM, position-sizing handoff, aggregate Jumbo trend context. |
| Strategy Ten basic carry | 232-259 | M5 carry construction, carry smoothing, scalar 30, caps, carry span eligibility, carry FDM, aggregate Jumbo carry context. |
| Strategy Eleven combined carry and trend | 264-275 | Combined trend/carry building blocks, 60/40 style mix, top-down weights, S11 FDM, cap, position-sizing handoff, aggregate Jumbo combined context. |
| Strategy Two/Three preliminaries | 70-88, 95-115 | Target risk, variable risk, costs, risk-adjusted cost, minimum capital, liquidity vocabulary. |
| Strategy Four portfolio machinery | 118-144 | Position sizing, instrument weights, IDM, Jumbo reference frame, target-risk policy. |

## Prior Opus Boundary

S10/M5 carry construction was separately audited by Opus 4.7:

```text
docs/process/CARVER_S10_M5_OPUS_47_SOURCE_FAITHFULNESS_AUDIT_RESULT_2026-05-29.md
AUDIT_DISPOSITION: PASS_PROCESS_AND_SYNTHETIC_SCOPE
```

That audit covered only the M5 synthetic carry-construction surface and the post-M5 decision. It did not cover the later S10 carry forecast-block implementation, S11 combined forecast implementation, or portfolio surfaces.

## S09 Synthetic Trend Conformance

Main process artifact:

```text
docs/process/CARVER_S09_M2_SYNTHETIC_IMPLEMENTATION_GATE_2026-05-29.md
```

Status:

```text
PROCESS_AND_SYNTHETIC_CODE_CARVER_S09_M2_FORECAST_GATE_NOT_DATA_NOT_BACKTEST
```

S09/M2 synthetic surface covers:

- M2 forecast-block arithmetic.
- S09 EWMAC trend forecasts from completed daily close inputs.
- EWMAC speed set: `2, 4, 8, 16, 32, 64`.
- Synthetic convention: `EWMACn = EWMAC(n, 4n)`.
- Table 29 forecast scalars: `12.1, 8.53, 5.95, 4.10, 2.79, 1.91`.
- Individual forecast cap: absolute value `20`.
- S09 Table 36 FDM rows for allowed speed sets.
- Final combined forecast cap: absolute value `20`.
- Completed daily bars only.

Boundary:

- It does not open real data.
- It does not compute cost eligibility from market rows.
- It does not run diagnostics or backtests.
- It does not implement P05.
- The `0.15 SR` cost-units threshold is book-verified at PDF page 216, but it has not yet been transcribed as a hash-bound machine-readable production lock; per-instrument cost eligibility derived from real prevalidated costs and turnover policy remains closed.

Audit result:

```text
docs/process/CARVER_S09_M2_SYNTHETIC_IMPLEMENTATION_HOSTILE_AUDIT_2026-05-29.md
```

This was a regular hostile audit, not Opus.

Opus should verify:

- S09 source values and unresolved atoms are faithfully represented.
- Synthetic EWMAC conventions are not mislabeled as production warm-up policy.
- S09 output remains a forecast block, not a backtest or trading strategy result.

## S10 Carry Forecast-Block After M5

Main process artifact:

```text
docs/process/CARVER_S10_CARRY_FORECAST_BLOCK_CONFORMANCE_2026-05-29.md
```

Status:

```text
PROCESS_AND_SYNTHETIC_CODE_CARVER_S10_CARRY_FORECAST_BLOCK_CONFORMANCE_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

Implemented surface:

```text
src/carver/spine/s10.py
tests/test_s10_carry_forecast_block_synthetic.py
```

Synthetic pipeline:

```text
locked M5 risk-adjusted carry input history
-> synthetic EWMA Carry5/20/60/120 smoothing
-> scalar 30 through M2
-> individual forecast cap 20 through M2
-> locked eligible carry span set
-> equal weights across eligible spans through M2
-> carry FDM by eligible span set
-> final combined cap 20 through M2
-> final capped S10 carry forecast output
```

Verification:

```text
Focused S10 synthetic tests: 7/7 passed
Full synthetic regression at that gate: 124/124 passed
```

Lean hostile audit:

```text
docs/process/CARVER_S10_CARRY_FORECAST_BLOCK_CONFORMANCE_HOSTILE_AUDIT_RESULT_2026-05-29.md
NO BLOCKING FINDINGS
AUDIT_DISPOSITION: PASS_PROCESS_AND_SYNTHETIC_CODE_SCOPE
```

Boundary:

- S10 stops at final capped carry forecast output.
- It does not emit positions, returns, PnL, Sharpe, drawdown, diagnostics, or backtests.
- It does not open production carry source locks.
- It consumes synthetic M5 history and explicit locks.
- Position sizing, buffering, trade/no-trade decisions, S11, P06, and P07 remain closed at this gate.

Opus should verify:

- S10 after M5 properly follows the prior Opus M5 forward constraints.
- Carry5/20/60/120, scalar 30, caps, equal weights, FDM rows, and output boundary are source-faithful at synthetic conformance scope.
- Production carry atoms remain unresolved where they should.

## S11 Combined Carry/Trend Conformance

Main process artifact:

```text
docs/process/CARVER_S11_COMBINED_CARRY_TREND_CONFORMANCE_2026-05-29.md
```

Status:

```text
PROCESS_AND_SYNTHETIC_CODE_CARVER_S11_COMBINED_CARRY_TREND_CONFORMANCE_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

Implemented surface:

```text
src/carver/spine/s11.py
tests/test_s11_combined_carry_trend_synthetic.py
```

Synthetic pipeline:

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

Verification:

```text
Focused S11 synthetic tests: 7/7 passed
Full synthetic regression at that gate: 131/131 passed
```

Lean hostile audit:

```text
docs/process/CARVER_S11_COMBINED_CARRY_TREND_CONFORMANCE_HOSTILE_AUDIT_RESULT_2026-05-29.md
NO BLOCKING FINDINGS
AUDIT_DISPOSITION: PASS_PROCESS_AND_SYNTHETIC_CODE_SCOPE
```

Boundary:

- S11 stops at final capped combined forecast output.
- It does not emit positions, returns, PnL, diagnostics, backtests, or portfolio outputs.
- Table 51 production row selection remains closed.
- Table 52 production FDM values and interpolation remain closed.
- Exact 0.15 SR quote/page verification remains closed for production source locks.
- P05/P06/P07 portfolio work is separate.

Opus should verify:

- S11 correctly consumes S09 and S10 forecast-block outputs rather than portfolio outputs.
- 60/40, top-down weights, eligible rule set, FDM, and cap are source-faithful at synthetic conformance scope.
- The implementation does not smuggle production Table 51/Table 52 locks.

## Strategy Graph Claim Under Audit

The current Carver signal graph is:

```text
S09 trend forecast block
S10 M5 carry construction
S10 carry forecast block
-> S11 combined carry/trend forecast block
```

This graph is complete only at process-and-synthetic-code scope.

It is not:

- real-data readiness;
- diagnostics;
- backtests;
- performance evidence;
- source-native deployment readiness;
- trading authorization;
- promotion evidence.

## Key Unresolved Production Atoms

S09:

- `0.15 SR` cost-units threshold sourced at PDF page 216; synthetic implementation has not yet transcribed it as a hash-bound machine-readable production lock.
- Production EWMA warm-up and data policy.
- Per-instrument eligible speed calculation from prevalidated costs.
- Production sessions, rolls, risk, FX, and costs.

S10:

- Production held/comparison contract role.
- Production raw-carry sign convention by instrument family.
- Expiry calendar/day-count.
- Roll-day handling.
- Fixed-month commodity policy.
- Seasonal and wrong-sign carry policy.
- Production cost eligibility and curve-leg availability.

S11:

- Table 51 forecast-weight rows verified at PDF page 268; production row selection still requires a hash-bound machine-readable lock.
- Table 52 FDM rows and interpolation policy verified at PDF page 269; production row selection and interpolation use still require a hash-bound machine-readable lock.
- Per-member trend/carry eligibility and synchronization.
- Production buffering and trade/no-trade boundary.

## Non-Authorization

This file authorizes no code edits, no tests, no data access, no market-row parsing, no NinjaTrader export, no diagnostics, no backtests, no returns, no PnL, no Sharpe, no drawdown, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Opus execution by itself, no remote push, and no GitHub action.
