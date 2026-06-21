# Carver S11 Combined Carry/Trend Gate Draft

Date: 2026-05-29

Status:

```text
PROCESS_ONLY_CARVER_S11_COMBINED_CARRY_TREND_GATE_DRAFT_NOT_DATA_NOT_IMPLEMENTATION
```

## Purpose

Draft the next clean S11 gate after Strategy Ten carry completion:

```text
S11_COMBINED_CARRY_TREND_PROCESS_GATE_DRAFT
```

This draft defines the future process-and-synthetic-code conformance boundary for Carver Strategy 11, combined carry and trend.

It does not authorize code edits, tests, real data, diagnostics, backtests, S11 implementation, P05/P06/P07 portfolio work, Opus execution, or remote operations.

## Current Dependencies

S11 may build only on the clean Carver process-and-synthetic surfaces already recorded:

- M2 forecast-block architecture;
- S09/M2 synthetic trend forecast-block machinery;
- S09 phase-1 multi-instrument forecast conformance surface;
- S10/M5 synthetic carry construction;
- S10 carry forecast-block conformance surface;
- S10 carry forecast-block hostile-audit pass;
- Post-S10 S11 next-step decision.

S10 is currently complete only at process-and-synthetic scope:

```text
S10_CARRY_FORECAST_BLOCK_SOURCE_FAITHFUL_SYNTHETIC_CONFORMANCE_AUDITED
```

This does not create production source locks, real-data authority, position sizing authority, buffering authority, or portfolio authority.

## Future Synthetic Surface Shape

If separately authorized later, the S11 synthetic conformance surface should consume prevalidated synthetic S09 and S10 forecast-block outputs and emit exactly one S11 combined forecast output.

Proposed future synthetic-only transformation:

```text
locked synthetic S09 trend forecast block outputs
locked synthetic S10 carry forecast block outputs
-> locked style grouping: trend = divergent, carry = convergent
-> locked style mix: 60% trend / 40% carry
-> locked top-down style/rule/variation weights
-> locked eligible rule set after predeclared speed/cost eligibility
-> locked S11 FDM row by remaining trading-rule count
-> final combined forecast cap through M2
-> final capped S11 combined carry/trend forecast output
```

The future surface must stop at:

```text
final capped S11 combined carry/trend forecast output
```

It must not emit:

- interpretable trading signals;
- position sizes;
- buffered trade/no-trade decisions;
- portfolio weights;
- portfolio returns;
- diagnostics;
- performance metrics;
- backtest outputs;
- promotion evidence.

## Source-Faithfulness Boundary

S11 source framing is currently process-only and must remain source-audited before implementation.

Known source anchors from the S11 candidate brief and M2 spec:

- S11 source chapter: `Carver.pdf`, PDF pages 264-275;
- building-block compatibility across scaled forecasts: pages 264-265;
- trend variations: EWMAC2, EWMAC4, EWMAC8, EWMAC16, EWMAC32, EWMAC64;
- carry variations: Carry5, Carry20, Carry60, Carry120;
- trend style: divergent;
- carry style: convergent;
- source style mix: 60% trend / 40% carry;
- top-down style/rule/variation weighting;
- final combined forecast cap.

These remain process references, not production locks.

## Unresolved Source Atoms

The following atoms must remain unresolved until source-audited and separately locked:

- Table 51 forecast-weight rows, book-verified at PDF page 268 but not yet machine-locked for production use;
- Table 52 FDM rows and interpolation policy, book-verified at PDF page 269 but not yet machine-locked for production use;
- whether Table 52 interpolation is allowed or explicitly blocked;
- exact S11 worked-example row/page handling;
- inherited S09 `0.15 SR` speed/cost threshold, book-verified at PDF page 216 but not yet machine-locked for production use;
- exact S11 top-down weighting rule for partial eligible rule sets;
- exact handling when one style has no eligible rule and the other remains eligible;
- exact handling when one or more instruments lack carry inputs;
- exact completed-bar synchronization across trend and carry inputs;
- exact fail-closed behavior for missing S09 or S10 forecast-block outputs;
- exact synthetic conformance examples for future tests.

None of these atoms may be inferred from this draft.

## Proposed Future Locks

A later S11 implementation gate, if authorized, should require explicit S11 locks before calling any shared M2 machinery.

Required future lock families:

- S09 input provenance lock;
- S10 input provenance lock;
- source-native lane lock;
- completed-bar timestamp lock;
- style grouping lock;
- style mix lock;
- top-down weighting lock;
- eligible rule-set lock;
- cost/speed eligibility lock;
- S11 FDM lock;
- combined cap lock;
- output-boundary lock.

The future S11 wrapper must not rely on default-`LOCKED` ergonomics inherited from shared machinery.

## Fail-Closed Requirements

A future S11 conformance surface must fail closed when:

- lane class is not exactly `SOURCE_NATIVE_FUTURES`;
- any required S11 lock is unresolved;
- S09 or S10 inputs are missing, stale, duplicated, unordered, or timestamp-misaligned;
- any input is not explicitly synthetic in a synthetic conformance gate;
- trend or carry style labels are missing or inconsistent with the locked source grouping;
- style weights do not sum to 1;
- source style mix differs from the locked source/audit decision;
- top-down weights are missing, negative, inconsistent, or not source-locked;
- eligible trend/carry rule sets are empty without a predeclared fail-closed fallback;
- S11 FDM row selection is unresolved;
- Table 51/Table 52 source locks remain unresolved for the requested behavior;
- combined cap is not locked to the shared M2 cap behavior;
- outputs attempt to include positions, buffered trades, portfolio aggregation, performance, diagnostics, backtests, or promotion fields.

## S09 And S10 Boundaries

S11 may combine S09 and S10 forecast-block outputs only after those outputs are declared valid inputs for the S11 gate.

S11 must not:

- recompute S09 from real market rows;
- recompute S10 from real futures curves;
- settle production carry sign conventions;
- settle production roll calendars;
- expand S09 or S10 eligibility rules after seeing results;
- reinterpret S09 or S10 source atoms by inference;
- treat synthetic conformance outputs as production evidence.

## P05/P06/P07 Boundary

P05, P06, and P07 remain closed.

This S11 gate draft does not authorize:

- P05 full Jumbo multiple-trend portfolio work;
- P06 Jumbo carry portfolio work;
- P07 Jumbo combined trend/carry portfolio work;
- instrument weighting;
- IDM selection;
- portfolio aggregation;
- portfolio evidence windows;
- portfolio diagnostics or backtests.

P07 may only be considered after a separately authorized and audited S11 path exists.

## Audit Requirement

This process draft should receive a regular hostile audit before any S11 implementation gate is drafted.

Audit focus:

- no S11 implementation authorization is smuggled into the draft;
- S09 and S10 are used only as already-audited synthetic dependencies;
- S11 source atoms remain unresolved where they are not yet locked;
- Table 51/Table 52 production machine locks remain blocked before production-facing implementation, although the table pages are book-verified;
- the `0.15 SR` speed/cost threshold is book-verified at PDF page 216 but remains blocked for production use until machine-locked;
- S11 stops at final capped forecast output in any future synthetic gate;
- position sizing, buffering, P05/P06/P07, real data, diagnostics, backtests, deployment, trading, and promotion remain closed;
- Opus is not executed by this draft.

Opus is not required for this process-only draft audit. Opus is recommended later if source tables, page labels, row selection, or weighting remain ambiguous after regular hostile audit.

## Suggested Hostile Audit Authorization Prompt

```text
Operator authorizes exactly one regular hostile audit of the Carver S11
combined carry/trend gate draft.

Scope:
Audit the process-only S11 combined carry/trend gate draft:
docs/process/CARVER_S11_COMBINED_CARRY_TREND_GATE_DRAFT_2026-05-29.md

Allowed:
Read-only file inspection and concise audit findings.

Forbidden:
No file edits, no code tests, no real data, no market-row parsing, no
NinjaTrader export, no diagnostics, no backtests, no OOS, no Lockbox, no
Forward, no CFD adapters, no old QuantLab pipeline use, no tuning, no
deployment, no trading, no promotion, no S11 implementation, no P05/P06/P07
implementation, no Opus execution, no remote operations.
```

## Non-Authorization

This draft authorizes no code edits, no tests, no real data, no market-row parsing, no NinjaTrader export, no diagnostics, no backtests, no returns, no PnL, no Sharpe, no drawdown, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old-adapter import, no old workspace pipeline use, no tuning, no deployment, no trading, no promotion, no S11 implementation, no P05/P06/P07 implementation, no Opus execution, no remote push, and no GitHub action.
