# Carver P05 Source Extract And Source-Faithfulness Packet

Date: 2026-05-29

Status:

```text
PROCESS_ONLY_CARVER_P05_SOURCE_EXTRACT_AND_SOURCE_FAITHFULNESS_PACKET_NOT_DATA_NOT_IMPLEMENTATION
```

## Purpose

Identify the narrow book source range needed to decide the complete-P05 trend portfolio shape before any synthetic complete-P05 conformance code.

This packet is process-only. It records source anchors and source-faithfulness constraints for:

- complete-P05 portfolio identity;
- complete-P05 universe;
- source framing;
- instrument weights;
- IDM;
- target-risk and capital policy;
- eligible EWMAC speed and cost rules;
- missing-member behavior;
- implementation blockers.

It does not authorize code edits, tests, real-data execution, market-row parsing, NinjaTrader export, diagnostics, backtests, OOS, Lockbox, Forward, CFD adapters, old QuantLab pipeline use, tuning, deployment, trading, promotion, portfolio implementation, Opus/GPT execution, remote operations, remote push, or GitHub action.

## Inputs Inspected

Required Carver guardrail files were inspected before this packet:

```text
README.md
docs/mission/CARVER_SOURCE_NATIVE_RESEARCH_CHARTER_2026-05-28.md
docs/process/CLEAN_WORKSPACE_MIGRATION_RECORD_2026-05-28.md
docs/process/LANE_CLASSIFICATION_AND_ADAPTER_QUARANTINE_RULES_2026-05-28.md
```

P05 process trail inspected:

```text
docs/process/CARVER_P05_COMPLETE_TREND_PORTFOLIO_SOURCE_SHAPE_GATE_DRAFT_2026-05-29.md
docs/process/CARVER_P05_COMPLETE_TREND_PORTFOLIO_SOURCE_SHAPE_GATE_DRAFT_HOSTILE_AUDIT_RESULT_2026-05-29.md
docs/process/CARVER_P05_IMPLEMENTATION_READINESS_DECISION_2026-05-29.md
docs/researchops/portfolios/CARVER_P05_JUMBO_MULTIPLE_TREND_PORTFOLIO_SHAPE_GATE_2026-05-29.md
```

Local source inspected:

```text
C:\Users\openclaw\Desktop\Carver\Carver.pdf
```

Page references below are PDF page numbers from the local `Carver.pdf`, matching the convention used in the S10 source extract packet.

## Source Range

The complete-P05 source range is not a single contiguous page block.

P05 is a Carver-process label for the complete Jumbo multiple-trend portfolio shape. The source basis is:

| Source area | PDF pages | Packet use |
| --- | ---: | --- |
| Strategy Four portfolio construction machinery | 118-144 | Multi-instrument risk-scaled portfolio framing, hand-crafted instrument weights, IDM, Jumbo capital framing, target-risk policy, cost/liquidity/minimum-capital constraints. |
| Strategy Nine multiple trend following | 201-227 | Multiple EWMAC trend forecast variations, speed eligibility, equal forecast weights, trend FDM, final combined forecast cap, and position-sizing handoff. |
| Appendix C Jumbo universe | 690-695 | Complete 102-instrument Jumbo portfolio list, grouped by asset class, with descriptive names, broker market codes, exchange, currency, multiplier, and first year in the author's data. |
| Strategy Three cost and liquidity preliminaries | 110-115 | Instrument-level cost threshold, liquidity threshold discussion, and minimum-capital constraints that Strategy Four and Strategy Nine reuse. |
| Strategy Two/Three risk sizing foundation | 70-88 and 95-115 | Underlying risk target, variable risk estimate, minimum capital, and risk-adjusted cost vocabulary inherited by P05. |

## Source-Faithfulness Findings

### P05 Identity

Source status:

```text
SOURCE_RANGE_LOCKED_PROCESS_LABEL_NOT_BOOK_LABEL
```

The book does not name a portfolio `P05`. The Carver process label `P05` refers to the complete source-native futures portfolio shape formed by applying Strategy Nine multiple trend following across the Jumbo futures portfolio.

Narrow source anchors:

- PDF pages 201-202 introduce Strategy Nine as multiple trend following over one or more instruments, with positions scaled for variable risk and based on a combined forecast.
- PDF pages 222-227 evaluate Strategy Nine using both median-instrument and aggregate Jumbo portfolio results.
- PDF pages 141-143 define the Jumbo portfolio as a large, 102-instrument institutional portfolio used throughout the book for aggregate strategy evaluation.

Audit implication:

```text
P05_MUST_BE_DESCRIBED_AS_PROCESS_ALIAS_FOR_STRATEGY_NINE_JUMBO_TREND_PORTFOLIO
```

Do not state that the book itself names a `P05` portfolio. Do not inflate the existing MES/ZN/ZF phase-1 seed into complete P05.

### Source Framing

Source status:

```text
SOURCE_NATIVE_FUTURES_COMPLETE_BOOK_PORTFOLIO_CANDIDATE
```

The relevant book material is futures-native. Appendix C lists futures market codes, exchanges, currencies, multipliers, and first data years. Strategy Nine is framed as a futures trading strategy that uses completed trend forecasts and later position sizing. It is not a CFD-direct or CFD-adapter source.

Audit implication:

```text
CFD_DIRECT_AND_CFD_ADAPTER_REMAIN_CLOSED
```

### Complete Universe

Source status:

```text
SOURCE_RANGE_LOCKED_UNIVERSE_TRANSCRIPTION_REQUIRED_BEFORE_IMPLEMENTATION
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

MES, ZN, and ZF appear in Appendix C, but their presence does not make the existing phase-1 seed equal to complete P05.

Implementation implication:

```text
COMPLETE_P05_REQUIRES_APPENDIX_C_TRANSCRIPTION_OR_HASH_BOUND_MACHINE_READABLE_UNIVERSE
```

The next synthetic implementation gate may not invent the complete universe. It must either consume a locked synthetic toy universe explicitly marked as a conformance fixture, or wait for a separate Appendix C transcription/readiness artifact before claiming complete 102-member shape.

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
P05_WEIGHT_ENGINE_CAN_BE_SYNTHETIC_ONLY_BUT_COMPLETE_WEIGHTS_REQUIRE_LOCKED_GROUP_TAXONOMY
```

A toy conformance surface may test the top-down weighting contract using a locked synthetic taxonomy. A complete 102-instrument P05 implementation must first lock the Appendix C taxonomy and any group-layer interpretation used to reproduce the Jumbo handcrafting method.

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

Complete-P05 synthetic code should fail closed unless the request explicitly locks whether it is using:

- the source Jumbo reference IDM of 2.47;
- the approximate table by member count;
- or a synthetic toy IDM declared solely for conformance testing.

No real-data correlation or IDM calculation is authorized here.

### Target Risk And Capital Policy

Source status:

```text
SOURCE_LOCKED_FOR_BOOK_REFERENCE_POLICY_OPERATOR_CAPITAL_STILL_CLOSED
```

PDF pages 70-80 introduce target-risk position sizing for futures. PDF pages 141-143 frame the Jumbo portfolio as an institutional-scale example using about $50 million so minimum-capital constraints do not bind. PDF pages 143-144 state that the book uses a 20% annual standard deviation target and gives breadth-based guidance for lower or higher targets.

Implementation implication:

```text
TARGET_RISK_CAN_BE_SOURCE_REFERENCED_CAPITAL_AMOUNT_REQUIRES_EXPLICIT_OPERATOR_LOCK
```

A synthetic conformance surface may use declared toy capital and locked target risk for arithmetic shape only. It must not imply that real capital, margin, readiness, tradability, or deployment has been approved.

### Eligible EWMAC Speed And Cost Rules

Source status:

```text
SOURCE_LOCKED_FOR_STRATEGY_NINE_CONFORMANCE
```

PDF pages 201-202 list the Strategy Nine EWMAC variations:

```text
EWMAC2, EWMAC4, EWMAC8, EWMAC16, EWMAC32, EWMAC64
```

These correspond to the short/long span pairs:

```text
2/8, 4/16, 8/32, 16/64, 32/128, 64/256
```

PDF pages 216-218 set the Strategy Nine trading-rule cost eligibility threshold at 0.15 SR units and provide the average turnover estimates:

```text
EWMAC2  = 98.5
EWMAC4  = 50.2
EWMAC8  = 25.4
EWMAC16 = 13.2
EWMAC32 = 7.6
EWMAC64 = 5.2
```

PDF page 218 notes that if no EWMAC variation is cheap enough for an instrument, that instrument cannot be traded in Strategy Nine.

Implementation implication:

```text
P05_ELIGIBLE_SPEED_SET_MUST_BE_LOCKED_PER_INSTRUMENT_OR_SYNTHETIC_TOY_DECLARED
```

No real-data cost calculation is authorized. A synthetic conformance surface may consume prevalidated synthetic cost eligibility flags, but must not calculate them from market rows.

### Forecast Weights, Trend FDM, And Forecast Cap

Source status:

```text
SOURCE_LOCKED_FOR_STRATEGY_NINE_FORECAST_BLOCK_HANDOFF
```

PDF pages 218-220 describe top-down forecast weighting for Strategy Nine:

- one style: divergent;
- one rule: trend following with EWMAC;
- equal weights across eligible EWMAC variations.

PDF page 221 provides the Strategy Nine FDM and forecast-weight rows:

| Eligible EWMAC set | Weight per variation | FDM |
| --- | ---: | ---: |
| 2, 4, 8, 16, 32, 64 | 0.167 | 1.26 |
| 4, 8, 16, 32, 64 | 0.2 | 1.19 |
| 8, 16, 32, 64 | 0.25 | 1.13 |
| 16, 32, 64 | 0.333 | 1.08 |
| 32, 64 | 0.50 | 1.03 |
| 64 | 1.0 | 1.0 |

PDF pages 221-222 say the combined forecast is capped at +/-20 before the position-sizing handoff.

Implementation implication:

```text
SYNTHETIC_P05_CAN_CONSUME_LOCKED_S09_OUTPUTS_AND_APPLY_P05_ELIGIBILITY_WEIGHT_FDM_CAP_CONTRACTS
```

It still must not emit returns, PnL, Sharpe, drawdown, diagnostics, backtests, OOS, Lockbox, Forward, or trading decisions.

### Missing-Member Behavior

Source status:

```text
UNRESOLVED_FOR_RUNTIME_COMPLETE_P05
```

The source supports two relevant constraints:

- PDF page 141 defines the Jumbo portfolio as the instruments meeting liquidity/cost thresholds and having at least one year of data in the author's dataset.
- PDF page 218 says an instrument with no eligible EWMAC variations cannot be traded in Strategy Nine.

The source packet does not find a production runtime policy for local missing members, unavailable contracts, failed provider mapping, stale data, missing completed bars, missing FX, missing costs, or missing annual risk.

Implementation implication:

```text
MISSING_MEMBER_POLICY_MUST_FAIL_CLOSED_UNLESS_SEPARATELY_LOCKED
```

Synthetic conformance can model missing members only as explicit fail-closed cases. It may not silently drop, substitute, reweight, or rescue a missing member.

## Locked For A Narrow Synthetic Conformance Gate

If this packet passes regular hostile audit, the following atoms are narrow enough for a future process-and-synthetic-code P05 conformance surface:

- P05 is a process alias for Strategy Nine multiple trend following over the Jumbo portfolio source frame.
- The lane is `SOURCE_NATIVE_FUTURES`.
- The complete universe source is Appendix C Tables 172-183, PDF pages 690-695.
- Instrument weighting method is top-down handcrafting.
- Jumbo IDM reference is 2.47; approximate IDM table exists on PDF page 135.
- Book reference target risk is 20% annual standard deviation, with breadth guidance on PDF pages 143-144.
- Strategy Nine EWMAC variations are 2/8, 4/16, 8/32, 16/64, 32/128, and 64/256.
- Strategy Nine trading-rule cost eligibility threshold is 0.15 SR units.
- Eligible variations receive equal forecast weights.
- Strategy Nine FDM rows are source-cited on PDF page 221.
- Combined forecast cap is +/-20 before position sizing.

## Still Blocked Before Complete-P05 Implementation Claims

The following remain blocked or require separate artifacts:

- exact complete 102-member Appendix C transcription or hash-bound machine-readable universe;
- local provider mapping for every member;
- source-native contract identity for every member;
- session calendar and completed-bar rule for every member;
- roll and back-adjustment artifacts;
- annual risk and daily price-risk source for every member;
- FX source for non-USD members;
- cost source and risk-adjusted cost for every member;
- liquidity validation;
- minimum-capital validation;
- exact group taxonomy for complete 102-member handcrafting weights;
- whether synthetic complete-P05 uses source Jumbo IDM 2.47, table approximation, or a toy locked IDM;
- operator capital base if any non-toy capital is used;
- local missing-member behavior beyond fail-closed rejection;
- rounding and buffering;
- trade/no-trade decisions;
- aggregation, returns, PnL, Sharpe, drawdown, diagnostics, backtests, OOS, Lockbox, Forward, deployment, trading, or promotion.

## Synthetic Implementation Shape Allowed Only After Audit

After a regular hostile audit with no blocking findings, the next possible gate may be a process-and-synthetic-code P05 conformance surface that:

- consumes locked synthetic S09 forecast outputs only;
- consumes a locked synthetic member set and taxonomy, or a separately locked Appendix C transcription;
- consumes prevalidated synthetic annual risk, price risk, FX, costs, eligibility, capital, target risk, and IDM inputs;
- applies P05 source-shaped handcrafting weights, EWMAC eligibility, equal forecast weights, FDM, cap, and position-sizing input arithmetic;
- emits desired position inputs only;
- fails closed on unresolved source atoms or missing required inputs.

That future surface must not claim production P05 behavior unless all production source and data/readiness atoms are separately locked.

## Audit Requirements

Regular hostile audit should verify:

- this packet does not quote broad book text;
- page references match the local `Carver.pdf`;
- P05 is not falsely described as a book label;
- Appendix C is treated as the universe source, not as local provider readiness;
- the MES/ZN/ZF phase-1 seed is not inflated into complete P05;
- weights, IDM, target risk, EWMAC eligibility, FDM, and caps are separated from data/readiness atoms;
- missing-member behavior remains fail-closed and unresolved for production;
- no implementation, real data, diagnostics, backtests, CFD adapters, Opus/GPT execution, remote operations, deployment, trading, or promotion are authorized.

Opus/GPT audit is not required for this packet unless the operator wants an external source-faithfulness review before opening the implementation gate.

## Next Authorization Prompt If Implementation Is Opened

Use this only after the source packet receives a no-blocking regular hostile audit.

```text
Operator authorizes exactly one process-and-synthetic-code gate for the Carver
P05 complete trend portfolio synthetic conformance surface.

Scope:
Clean Carver workspace only. Implement a tiny synthetic-only P05 surface that
consumes locked synthetic S09 trend forecasts, locked synthetic P05 member
identity/taxonomy, locked synthetic or source-cited instrument weights, locked
IDM, locked target risk/capital inputs, prevalidated synthetic price risk/FX/cost
eligibility, eligible EWMAC speed sets, Strategy Nine equal forecast weights,
Strategy Nine FDM, and final forecast caps, and emits complete-P05 desired
position inputs only.

Required status:
PROCESS_AND_SYNTHETIC_CODE_CARVER_P05_COMPLETE_TREND_PORTFOLIO_CONFORMANCE_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST

Allowed:
Code contracts, synthetic tests, and process documentation for P05 complete
trend portfolio conformance only.

Forbidden:
No real data, no market-row parsing, no NinjaTrader export, no diagnostics,
no backtests, no returns, no PnL, no Sharpe, no drawdown, no OOS, no Lockbox,
no Forward, no CFD adapters, no old QuantLab imports, no tuning, no deployment,
no trading, no promotion, no production source locks, no silent member dropping
or substitution, no P06/P07 portfolio work, no Opus/GPT execution, no remote
operations.
```

## Non-Authorization

This packet authorizes no code edits, no tests, no real-data execution, no market-row parsing, no NinjaTrader export, no diagnostics, no backtests, no returns, no PnL, no Sharpe, no drawdown, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old-adapter import, no old workspace pipeline use, no tuning, no deployment, no trading, no promotion, no portfolio implementation, no P05/P06/P07 implementation, no Opus/GPT execution, no remote push, and no GitHub action.
