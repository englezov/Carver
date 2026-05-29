# Carver S10 Carry Forecast-Block Extension Gate Draft

Date: 2026-05-29

Status:

```text
PROCESS_ONLY_CARVER_S10_CARRY_FORECAST_BLOCK_EXTENSION_GATE_DRAFT_NOT_IMPLEMENTATION_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Draft the next Strategy Ten gate after the Opus 4.7 pass on the S10/M5 synthetic carry-construction surface.

This is a process-only gate draft. It does not authorize implementation, tests, data access, diagnostics, backtests, Opus execution, or remote operations.

## Prior Evidence

Completed local prerequisites:

- S10/M5 synthetic carry-construction conformance exists.
- S10/M5 emits only a risk-adjusted carry forecast input.
- Regular hostile audit of implemented S10/M5 surface found no blocking issues.
- Opus 4.7 hostile source-faithfulness audit returned:

```text
AUDIT_DISPOSITION: PASS_PROCESS_AND_SYNTHETIC_SCOPE
```

Audit result record:

```text
docs/process/CARVER_S10_M5_OPUS_47_SOURCE_FAITHFULNESS_AUDIT_RESULT_2026-05-29.md
```

Bounded source pack:

```text
GPT/OPUS_47_S10_CARRY_SOURCE_FAITHFULNESS_AUDIT_PACK_2026-05-29/05_S10_CARRY_SOURCE_EXTRACT_PACK.md
```

## Lane Class

Future work under this draft remains:

```text
SOURCE_NATIVE_FUTURES
```

No `CFD_DIRECT` or `CFD_ADAPTER` lane is opened.

## Draft Gate Name

```text
PROCESS_AND_SYNTHETIC_CODE_CARVER_S10_CARRY_FORECAST_BLOCK_CONFORMANCE_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Intended Synthetic Surface

If separately authorized, the implementation gate should build a tiny synthetic-only S10 carry forecast block that consumes locked synthetic carry inputs and emits one final capped S10 carry forecast output.

Pipeline:

```text
locked M5 risk-adjusted carry input history
-> Carry5/20/60/120 smoothed carry forecasts
-> scalar 30
-> individual forecast caps through M2
-> locked eligible carry span set
-> equal weights across eligible spans
-> carry FDM by eligible span set
-> final combined forecast cap through M2
-> final capped S10 carry forecast output
```

This surface remains synthetic conformance machinery only. It is not a real-data strategy, backtest, diagnostic, trading signal, position, portfolio, performance result, or promotion artifact.

The implementation should prefer the existing M2 forecast-block primitives where possible, especially `ForecastRuleInput`, `ForecastBlockRequest`, `combine_forecast_block`, and the shared forecast cap behavior. S10 should add only the carry-specific source table, smoothing-history validation, and rule identifiers needed to feed M2.

## Source Atoms Allowed For Synthetic Locking

The next implementation gate may synthetically lock:

- four carry smoothing spans:

```text
5, 20, 60, 120
```

- carry scalar:

```text
30
```

- shared synthetic forecast cap through M2:

```text
20
```

- eligible span sets:

```text
Carry5, Carry20, Carry60, Carry120
Carry20, Carry60, Carry120
Carry60, Carry120
Carry120
```

- equal weights within each eligible span set;
- carry FDM values:

```text
1.04
1.03
1.02
1.0
```

The cap value may be treated as a shared M2 synthetic forecast-block constant for this synthetic gate. It is not a production source lock for S10 carry until the future narrow source extract for scalar and cap values is created and audited.

## Required Forward Constraints

The Opus 4.7 low findings are binding forward constraints for this draft.

### Explicit Locks

The future implementation must avoid default-`LOCKED` ergonomics for new S10 source locks.

Any S10 carry forecast-block request should require explicit lock status for:

- M5 input provenance;
- carry input history completeness;
- smoothing span set;
- scalar;
- cap;
- eligible span set;
- equal weights;
- FDM;
- output boundary.

### Synthetic Labels

Synthetic conventions must be visibly marked as synthetic in code, tests, and docs.

Production labels, real instrument interpretation, and real-data source authority remain disallowed.

### Abstract Fixtures

Synthetic tests should use abstract contract or instrument identities rather than `ZN`, `MES`, or other real-looking symbols unless a separate process record justifies the presentation risk.

### Separate Audit Records

The future implementation gate and hostile-audit results should be separate files.

The implementation conformance artifact may reference audit results but should not embed the current audit verdict as its own pass claim.

## Required Fail-Closed Behavior

Future synthetic implementation should fail closed when:

- lane class is not exactly `SOURCE_NATIVE_FUTURES`;
- any required S10 carry atom is unresolved;
- M5 input timestamps are incomplete, unsorted, duplicated, stale, or non-daily;
- the available input history is insufficient for the requested smoothing span;
- an ineligible smoothing span is requested;
- eligible span set is empty or not one of the source-permitted sets;
- forecast weights are not equal within the eligible span set;
- FDM does not match the eligible span set;
- scalar is not locked to 30;
- individual or final cap is not locked to the shared M2 synthetic cap value;
- cap is missing, unresolved, non-positive, or inconsistently applied;
- outputs attempt to include position sizing, buffering, trade/no-trade decisions, performance metrics, returns, PnL, Sharpe, drawdown, diagnostics, backtests, or portfolio results.

## Explicit Non-Scope

This draft does not open:

- real-data execution;
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
- production raw-carry sign locks;
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

## Source Extracts Needed Before Production Locks

The current source pack is enough for this process draft and for a synthetic-only implementation gate.

Before production source locks, create narrow page-cited extracts for:

- production raw-carry sign convention by instrument class;
- production annualization day-count rule;
- production seasonal and wrong-sign policy;
- production smoothing span rationale;
- production scalar and cap values;
- production cost and turnover eligibility rule;
- production equal forecast weights and FDM;
- S11 trend/carry combination, only after S11 is explicitly opened.

Do not add the entire book to any process artifact or audit packet.

## Required Hostile Audit

Before this draft is treated as locked, a regular hostile audit should verify:

- the draft does not authorize implementation;
- Opus 4.7 findings are correctly converted into forward constraints;
- the selected S10 carry forecast-block extension is the correct next chapter step after S10/M5;
- S10 implementation remains behind a separate explicit operator authorization;
- S11, P06, P07, real data, diagnostics, backtests, CFD adapters, deployment, trading, promotion, remote operations, tuning, and old `QuantLab_v3` active-pipeline use remain closed.

## Suggested Implementation Authorization Prompt

```text
Operator authorizes exactly one process-and-synthetic-code gate for the
Carver S10 carry forecast-block conformance surface.

Scope:
Clean Carver workspace only. Implement a tiny synthetic-only S10 carry
forecast block that consumes locked M5 risk-adjusted carry input history
and produces Carry5/20/60/120 smoothed forecasts, scalar 30 application,
forecast caps, locked eligible carry span set, equal weights, carry FDM,
and one final capped S10 carry forecast output.

Required status:
PROCESS_AND_SYNTHETIC_CODE_CARVER_S10_CARRY_FORECAST_BLOCK_CONFORMANCE_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST

Allowed:
Code contracts, synthetic tests, and process documentation for S10 carry
forecast-block conformance only.

Forbidden:
No real-data execution, no market-row parsing, no NinjaTrader export, no
diagnostics, no backtests, no returns, no PnL, no Sharpe, no drawdown, no
OOS, no Lockbox, no Forward, no CFD adapters, no old QuantLab imports, no
tuning, no deployment, no trading, no promotion, no production source locks,
no S11, and no P06/P07 portfolio work.
```

## Suggested Draft Audit Authorization Prompt

```text
Operator authorizes exactly one regular hostile audit of the Carver
S10 carry forecast-block extension gate draft:

docs/process/CARVER_S10_CARRY_FORECAST_BLOCK_EXTENSION_GATE_DRAFT_2026-05-29.md

Scope:
Audit the process-only draft for source-faithful Strategy Ten completion
sequencing and governance boundaries.

Allowed:
Read-only file inspection and concise audit findings.

Forbidden:
No file edits, no code tests, no real data, no market-row parsing, no
NinjaTrader export, no diagnostics, no backtests, no CFD adapters, no Opus
execution, no remote operations, and no access to
C:\Users\openclaw\Desktop\QuantLab_v3.
```

## Non-Authorization

This draft authorizes no code edits, no tests, no data access, no market-row parsing, no NinjaTrader export, no diagnostics, no backtests, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old-adapter import, no old workspace pipeline use, no tuning, no deployment, no trading, no promotion, no S10 implementation, no S11, no P06/P07 portfolio work, no Opus execution, no remote push, and no GitHub action.
