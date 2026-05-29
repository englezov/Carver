# Carver P06 Source Extract And Source-Faithfulness Packet

Date: 2026-05-29

Status:

```text
PROCESS_ONLY_CARVER_P06_SOURCE_EXTRACT_AND_SOURCE_FAITHFULNESS_PACKET_NOT_DATA_NOT_IMPLEMENTATION
```

## Purpose

Identify the narrow book source range needed to decide the complete-P06 carry portfolio shape before any synthetic complete-P06 conformance code.

This packet is process-only. It records source anchors and source-faithfulness constraints for:

- complete-P06 carry portfolio identity;
- complete-P06 universe;
- source framing;
- instrument weights;
- IDM;
- target-risk and capital policy;
- carry span eligibility;
- carry-specific production blockers;
- missing-member behavior;
- implementation blockers.

It does not authorize code edits, tests, real-data execution, market-row parsing, NinjaTrader export, diagnostics, backtests, OOS, Lockbox, Forward, CFD adapters, old QuantLab pipeline use, tuning, deployment, trading, promotion, portfolio implementation, P07 implementation, Opus/GPT execution, remote operations, remote push, or GitHub action.

## Inputs Inspected

Required Carver guardrail files were inspected before this packet:

```text
README.md
docs/mission/CARVER_SOURCE_NATIVE_RESEARCH_CHARTER_2026-05-28.md
docs/process/CLEAN_WORKSPACE_MIGRATION_RECORD_2026-05-28.md
docs/process/LANE_CLASSIFICATION_AND_ADAPTER_QUARANTINE_RULES_2026-05-28.md
```

P06 and upstream process trail inspected:

```text
docs/process/CARVER_POST_P05_COMPLETE_TREND_PORTFOLIO_NEXT_STEP_DECISION_2026-05-29.md
docs/process/CARVER_P06_COMPLETE_CARRY_PORTFOLIO_SOURCE_SHAPE_GATE_DRAFT_2026-05-29.md
docs/process/CARVER_P05_SOURCE_EXTRACT_AND_SOURCE_FAITHFULNESS_PACKET_2026-05-29.md
docs/process/CARVER_P05_COMPLETE_TREND_PORTFOLIO_CONFORMANCE_2026-05-29.md
docs/process/CARVER_S10_CARRY_FORECAST_BLOCK_CONFORMANCE_2026-05-29.md
GPT/OPUS_47_S10_CARRY_SOURCE_FAITHFULNESS_AUDIT_PACK_2026-05-29/05_S10_CARRY_SOURCE_EXTRACT_PACK.md
```

Local source inspected:

```text
C:\Users\openclaw\Desktop\Carver\Carver.pdf
```

Page references below are PDF page numbers from the local `Carver.pdf`, matching the convention used in the S10 source extract packet.

## Source Range

P06 is not a book-native label. It is a Carver-process label for the complete Strategy Ten multiple-carry Jumbo portfolio shape.

The source basis is:

| Source area | PDF pages | Packet use |
| --- | ---: | --- |
| Strategy Ten basic carry | 232-259 | Carry source framing, curve carry construction, smoothing spans, scalar, caps, cost eligibility, equal carry-span weights, carry FDM, and aggregate Jumbo carry result framing. |
| Strategy Four portfolio construction machinery | 118-144 | Multi-instrument risk-scaled portfolio framing, handcrafted instrument weights, IDM, Jumbo capital framing, target-risk policy, cost/liquidity/minimum-capital constraints. |
| Appendix C Jumbo universe | 690-695 | Complete 102-instrument Jumbo portfolio list, grouped by asset class, with descriptive names, broker market codes, exchange, currency, multiplier, and first year in the author's data. |
| Strategy Three cost and risk-sizing preliminaries | 70-88 and 95-115 | Risk-target, annual risk, minimum capital, risk-adjusted cost, and liquidity vocabulary inherited by later portfolio machinery. |
| Strategy Nine multiple-rule framework | 201-227 | The method Strategy Ten explicitly reuses for selecting cheap enough rule variations, equal forecast weights, FDM application, and position-sizing handoff. |

## Source-Faithfulness Findings

### P06 Identity

Source status:

```text
SOURCE_RANGE_LOCKED_PROCESS_LABEL_NOT_BOOK_LABEL
```

The book does not name a portfolio `P06`. The Carver process label `P06` refers to Strategy Ten basic carry applied across the Jumbo futures portfolio source frame.

Narrow source anchors:

- PDF pages 232-233 introduce Strategy Ten as basic carry, distinct from trend following, and frame it as trading one or more instruments with variable-risk-scaled positions driven by forecasted carry strength.
- PDF pages 248-253 construct the multiple-carry forecast block using cheap-enough carry variations, equal forecast weights, and carry FDM.
- PDF pages 257-259 evaluate Strategy Ten carry at aggregate Jumbo portfolio level and compare it with Strategy Four long-only and Strategy Nine multiple trend.
- PDF pages 141-143 define the Jumbo portfolio as the large institutional portfolio used for aggregate strategy evaluation throughout the book.

Audit implication:

```text
P06_MUST_BE_DESCRIBED_AS_PROCESS_ALIAS_FOR_STRATEGY_TEN_JUMBO_CARRY_PORTFOLIO
```

Do not state that the book itself names a `P06` portfolio. Do not treat S10 signal completion alone as complete P06.

### Source Framing

Source status:

```text
SOURCE_NATIVE_FUTURES_COMPLETE_BOOK_PORTFOLIO_CANDIDATE
```

The relevant book material is futures-native. Strategy Ten measures carry from futures contract prices and Appendix C lists futures market codes, exchanges, currencies, multipliers, and first data years. P06 is not `CFD_DIRECT` and not `CFD_ADAPTER`.

Audit implication:

```text
CFD_DIRECT_AND_CFD_ADAPTER_REMAIN_CLOSED
```

Any CFD translation requires a later separate adapter gate after source-native P06 behavior exists.

### Complete Universe

Source status:

```text
SOURCE_RANGE_LOCKED_UNIVERSE_TRANSCRIPTION_REQUIRED_BEFORE_PRODUCTION_CLAIMS
```

Appendix C is the required universe source. PDF page 690 states that Tables 172 to 183 are the complete 102-instrument Jumbo portfolio list. PDF pages 690-695 contain the table material.

Required narrow material:

| Appendix C table | Asset class / group | PDF pages |
| --- | --- | ---: |
| Table 172 | US bond and interest rate futures | 690-691 |
| Table 173 | Other bond and interest rate futures | 691 |
| Table 174 | US equity index futures | 691-692 |
| Table 175 | European equity index futures | 692 |
| Table 176 | European stock sector futures | 692 |
| Table 177 | Asian equity index futures | 693 |
| Table 178 | Volatility futures | 693 |
| Table 179 | Major FX futures | 693-694 |
| Table 180 | Cross and EM FX futures | 694 |
| Table 181 | Metal and crypto futures | 694 |
| Table 182 | Energy futures | 695 |
| Table 183 | Agricultural futures | 695 |

Strategy Ten's aggregate Jumbo carry results support using the Jumbo portfolio source frame for P06. They do not by themselves transcribe local provider identifiers, roll rules, curve-leg availability, or production readiness for all 102 members.

Implementation implication:

```text
COMPLETE_P06_REQUIRES_APPENDIX_C_TRANSCRIPTION_OR_LOCKED_SYNTHETIC_MEMBER_FIXTURE
```

A synthetic conformance surface may use locked synthetic members to test P06 shape. It must not claim production complete-P06 readiness without a separate Appendix C transcription/readiness artifact.

### Instrument Weights

Source status:

```text
METHOD_SOURCE_LOCKED_EXACT_COMPLETE_102_WEIGHTS_NOT_YET_TRANSCRIBED
```

PDF pages 128-135 define instrument weights as risk-capital allocations across instrument sub-strategies. PDF pages 131-134 describe the top-down handcrafting method:

- equal allocation by asset class;
- equal allocation by group within asset class;
- equal allocation by instrument within group;
- optional intermediate grouping where needed.

PDF page 141 says the Jumbo portfolio instrument weights were constructed using the handcrafting method.

Implementation implication:

```text
P06_WEIGHT_ENGINE_CAN_BE_SYNTHETIC_ONLY_BUT_COMPLETE_WEIGHTS_REQUIRE_LOCKED_GROUP_TAXONOMY
```

A toy conformance surface may test the top-down weighting contract using a locked synthetic taxonomy. A complete 102-instrument P06 production claim must first lock the Appendix C taxonomy and any group-layer interpretation used to reproduce the Jumbo handcrafting method.

### IDM

Source status:

```text
SOURCE_LOCKED_FOR_JUMBO_REFERENCE_VALUE_AND_APPROXIMATION_TABLE
```

PDF pages 122-123 introduce the instrument diversification multiplier as the position-scaling correction for diversification across instruments. PDF page 135 provides approximate IDM values by instrument count. PDF page 141 reports that the Jumbo portfolio IDM comes out at 2.47.

Implementation implication:

```text
SYNTHETIC_CONFORMANCE_MAY_REQUIRE_EXPLICIT_LOCKED_IDM
```

Complete-P06 synthetic code should fail closed unless the request explicitly locks whether it is using:

- the source Jumbo reference IDM of 2.47;
- the approximate table by member count;
- or a synthetic toy IDM declared solely for conformance testing.

No real-data correlation or IDM calculation is authorized here.

### Target Risk And Capital Policy

Source status:

```text
SOURCE_LOCKED_FOR_BOOK_REFERENCE_POLICY_OPERATOR_CAPITAL_STILL_CLOSED
```

PDF pages 70-80 introduce target-risk position sizing for futures. PDF pages 141-143 frame the Jumbo portfolio as an institutional-scale example using about USD 50 million so minimum-capital constraints do not bind. PDF pages 143-144 state that the book uses a 20% annual standard deviation target and gives breadth-based guidance for lower or higher targets.

Implementation implication:

```text
TARGET_RISK_CAN_BE_SOURCE_REFERENCED_CAPITAL_AMOUNT_REQUIRES_EXPLICIT_OPERATOR_LOCK
```

A synthetic conformance surface may use declared toy capital and locked target risk for arithmetic shape only. It must not imply that real capital, margin, readiness, tradability, or deployment has been approved.

### Carry Construction And Forecast Block

Source status:

```text
UPSTREAM_S10_SYNTHETIC_SURFACE_COMPLETED_PRODUCTION_CARRY_LOCKS_STILL_CLOSED
```

The completed S10/M5 and S10 carry forecast-block surfaces already cover the synthetic signal path:

```text
M5 risk-adjusted carry input
-> Carry5/20/60/120 smoothing
-> scalar 30
-> forecast caps
-> eligible carry span set
-> equal weights
-> carry FDM
-> final capped S10 carry forecast output
```

P06 may consume locked synthetic S10 carry forecast outputs in a later implementation gate, but P06 must not recalculate production carry from real futures curve legs.

Relevant source anchors:

- PDF pages 238-241 cover two-contract carry measurement, annualization, and risk adjustment.
- PDF pages 242-247 cover noisy carry, seasonal carry, wrong-sign risks, and selected smoothing spans.
- PDF pages 247-248 cover scalar and forecast cap context.
- PDF pages 248-253 cover carry span cost eligibility, equal weights, and carry FDM rows.

Implementation implication:

```text
P06_CAN_CONSUME_LOCKED_SYNTHETIC_S10_OUTPUTS_NOT_PRODUCTION_CURVE_DATA
```

### Carry Span Eligibility

Source status:

```text
SOURCE_LOCKED_FOR_STRATEGY_TEN_CONFORMANCE_DATA_ELIGIBILITY_STILL_PREVALIDATED_INPUT
```

PDF page 247 selects four carry trading rule variations:

```text
Carry5
Carry20
Carry60
Carry120
```

PDF pages 248-253 say the carry variations cheap enough for the instrument are selected, then equal forecast weights are used across the selected variations.

PDF page 249 provides average turnover references for each carry span:

| Carry span | Turnover per year |
| --- | ---: |
| Carry5 | 5.75 |
| Carry20 | 3.12 |
| Carry60 | 1.82 |
| Carry120 | 1.22 |

PDF page 253 provides carry FDM rows:

| Eligible carry set | Equal weight | FDM |
| --- | ---: | ---: |
| Carry5, Carry20, Carry60, Carry120 | 0.25 | 1.04 |
| Carry20, Carry60, Carry120 | 0.333 | 1.03 |
| Carry60, Carry120 | 0.5 | 1.02 |
| Carry120 | 1.0 | 1.0 |

Implementation implication:

```text
P06_ELIGIBLE_CARRY_SET_MUST_BE_LOCKED_PER_MEMBER_OR_SYNTHETIC_TOY_DECLARED
```

No real-data cost calculation is authorized. A synthetic conformance surface may consume prevalidated synthetic carry span eligibility flags, but must not calculate them from market rows.

### Carry-Specific Production Blockers

Source status:

```text
PRODUCTION_CARRY_ATOMS_UNRESOLVED_FOR_P06
```

The S10 source material identifies production hazards that must not be collapsed into toy conformance:

- held and comparison contract role for each instrument;
- raw-carry sign convention by instrument family;
- expiry month or day-count annualization convention;
- roll-day handling;
- fixed-month commodity policy;
- seasonal carry handling;
- wrong-sign carry policy for affected bond and equity futures;
- second-contract or nearer-contract availability;
- stale or sparse second-contract history;
- poor data feed handling;
- instrument-specific carry exclusion or suppression if source-justified;
- completed-bar synchronization across held and comparison curve legs;
- cost, liquidity, FX, annual risk, and price-risk validation.

Implementation implication:

```text
PRODUCTION_P06_CARRY_REQUIRES_SEPARATE_SOURCE_AND_DATA_READINESS_GATES
```

The next synthetic P06 surface, if opened, must consume locked synthetic S10 outputs. It must not open production carry construction.

### P06 Aggregate Result Framing

Source status:

```text
SOURCE_CONTEXT_NOT_LOCAL_EVIDENCE
```

PDF pages 257-259 show the book's aggregate Jumbo portfolio results for Strategy Ten carry and compare them with Strategy Four and Strategy Nine. This source context supports the P06 identity as a complete Jumbo carry portfolio candidate.

It is not local Carver evidence. It does not authorize diagnostics, backtests, returns, PnL, Sharpe, drawdown, OOS, Lockbox, Forward, trading, deployment, promotion, or claims about local alpha.

Audit implication:

```text
BOOK_PERFORMANCE_TABLES_ARE_SOURCE_FRAMING_NOT_CARVER_PERFORMANCE_RESULTS
```

### Missing-Member Behavior

Source status:

```text
UNRESOLVED_FOR_RUNTIME_COMPLETE_P06
```

The source supports these constraints:

- PDF page 141 defines the Jumbo portfolio as the instruments meeting liquidity and cost thresholds and having sufficient source data in the author's dataset.
- PDF pages 248-253 require carry variations to be cheap enough for a given instrument before inclusion in the combined forecast.
- PDF pages 242-246 identify carry quality issues that can be instrument-specific, especially seasonal and wrong-sign hazards.

This packet does not find a production runtime policy for local missing members, unavailable contracts, failed provider mapping, stale bars, missing curve legs, missing expiry calendars, missing FX, missing costs, missing annual risk, or missing price risk.

Implementation implication:

```text
MISSING_MEMBER_POLICY_MUST_FAIL_CLOSED_UNLESS_SEPARATELY_LOCKED
```

Synthetic conformance can model missing members only as explicit fail-closed cases. It may not silently drop, substitute, reweight, or rescue a missing member.

## Locked For A Narrow Synthetic Conformance Gate

If this packet passes regular hostile audit, the following atoms are narrow enough for a future process-and-synthetic-code P06 conformance surface:

- P06 is a process alias for Strategy Ten basic carry over the Jumbo portfolio source frame.
- The lane is `SOURCE_NATIVE_FUTURES`.
- The complete universe source is Appendix C Tables 172-183, PDF pages 690-695.
- Instrument weighting method is top-down handcrafting.
- Jumbo IDM reference is 2.47; approximate IDM table exists on PDF page 135.
- Book reference target risk is 20% annual standard deviation, with breadth guidance on PDF pages 143-144.
- Book reference Jumbo capital context is about USD 50 million, not operator capital authorization.
- Strategy Ten carry spans are 5, 20, 60, and 120 business days.
- Strategy Ten carry scalar is 30 and forecast cap context is inherited from the forecast-block machinery.
- Carry span turnover references are source-cited on PDF page 249.
- Eligible carry spans receive equal forecast weights.
- Carry FDM rows are source-cited on PDF page 253.
- P06 may consume locked synthetic S10 carry forecast outputs and emit desired position inputs only.

## Still Blocked Before Complete-P06 Implementation Claims

The following remain blocked or require separate artifacts:

- exact complete 102-member Appendix C transcription or hash-bound machine-readable universe;
- local provider mapping for every member;
- source-native contract identity for every member;
- session calendar and completed-bar rule for every member and curve leg;
- roll and back-adjustment artifacts;
- held/comparison contract source and availability for every carry member;
- expiry calendar or month-distance artifact for every curve-leg pair;
- production raw-carry sign convention by instrument family;
- fixed-month commodity policy;
- seasonal and wrong-sign carry policy;
- annual risk and daily price-risk source for every member;
- FX source for non-USD members;
- cost source and risk-adjusted cost for every member;
- per-member carry span eligibility from prevalidated costs;
- liquidity validation;
- minimum-capital validation;
- exact group taxonomy for complete 102-member handcrafting weights;
- whether synthetic complete-P06 uses source Jumbo IDM 2.47, table approximation, or a toy locked IDM;
- operator capital base if any non-toy capital is used;
- local missing-member behavior beyond fail-closed rejection;
- rounding and buffering;
- trade/no-trade decisions;
- aggregation, returns, PnL, Sharpe, drawdown, diagnostics, backtests, OOS, Lockbox, Forward, deployment, trading, or promotion.

## Synthetic Implementation Shape Allowed Only After Audit

After a regular hostile audit with no blocking findings, the next possible gate may be a process-and-synthetic-code P06 conformance surface that:

- consumes locked synthetic S10 carry forecast outputs only;
- consumes a locked synthetic member set and taxonomy, or a separately locked Appendix C transcription;
- consumes locked synthetic or source-shaped capital, target risk, IDM, price risk, FX, and carry eligibility inputs;
- applies P06 source-shaped handcrafting weights, carry span eligibility, equal Strategy Ten forecast weights, Strategy Ten carry FDM, caps, and position-sizing input arithmetic;
- emits complete-P06 desired position inputs only;
- fails closed on unresolved source atoms or missing required inputs.

That future surface must not claim production P06 behavior unless all production source and data/readiness atoms are separately locked.

## Audit Requirements

Regular hostile audit should verify:

- this packet does not quote broad book text;
- page references match the local `Carver.pdf`;
- P06 is not falsely described as a book label;
- Strategy Ten signal completion is not treated as complete P06 portfolio authorization;
- Appendix C is treated as the universe source, not as local provider readiness;
- weights, IDM, target risk, capital, carry eligibility, carry FDM, and caps are separated from data/readiness atoms;
- carry-specific production blockers remain closed;
- missing-member behavior remains fail-closed and unresolved for production;
- no implementation, real data, diagnostics, backtests, CFD adapters, Opus/GPT execution, remote operations, deployment, trading, or promotion are authorized.

Opus/GPT audit is not required for this packet unless the operator wants an external source-faithfulness review before opening the implementation gate.

## Next Authorization Prompt If Implementation Is Opened

Use this only after the source packet receives a no-blocking regular hostile audit.

```text
Operator authorizes exactly one process-and-synthetic-code gate for the Carver
P06 complete carry portfolio synthetic conformance surface.

Scope:
Clean Carver workspace only. Implement a tiny synthetic-only P06 surface that
consumes locked synthetic S10 carry forecasts, locked synthetic P06 member
identity/taxonomy, locked synthetic or source-cited instrument weights, locked
IDM, locked target risk/capital inputs, prevalidated synthetic price risk/FX/cost
eligibility, eligible carry span sets, Strategy Ten equal forecast weights,
Strategy Ten carry FDM, and final forecast caps, and emits complete-P06 desired
position inputs only.

Required status:
PROCESS_AND_SYNTHETIC_CODE_CARVER_P06_COMPLETE_CARRY_PORTFOLIO_CONFORMANCE_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST

Allowed:
Code contracts, synthetic tests, and process documentation for P06 complete
carry portfolio conformance only.

Forbidden:
No real data, no market-row parsing, no NinjaTrader export, no diagnostics,
no backtests, no returns, no PnL, no Sharpe, no drawdown, no OOS, no Lockbox,
no Forward, no CFD adapters, no old QuantLab imports, no tuning, no deployment,
no trading, no promotion, no production source locks, no silent member dropping
or substitution, no P07 portfolio work, no Opus/GPT execution, no remote
operations.
```

## Non-Authorization

This packet authorizes no code edits, no tests, no real-data execution, no market-row parsing, no NinjaTrader export, no diagnostics, no backtests, no returns, no PnL, no Sharpe, no drawdown, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old-adapter import, no old workspace pipeline use, no tuning, no deployment, no trading, no promotion, no portfolio implementation, no P06/P07 implementation, no Opus/GPT execution, no remote push, and no GitHub action.
