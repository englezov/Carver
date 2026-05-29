# Carver P07 Source Extract And Source-Faithfulness Packet

Date: 2026-05-29

Status:

```text
PROCESS_ONLY_CARVER_P07_SOURCE_EXTRACT_AND_SOURCE_FAITHFULNESS_PACKET_NOT_DATA_NOT_IMPLEMENTATION
```

## Purpose

Identify the narrow book source range needed to decide the complete-P07 combined trend/carry portfolio shape before any synthetic complete-P07 conformance code.

This packet is process-only. It records source anchors and source-faithfulness constraints for:

- complete-P07 combined trend/carry portfolio identity;
- complete-P07 universe;
- source framing;
- relationship to S11;
- relationship to P05 and P06;
- instrument weights;
- IDM;
- target-risk and capital policy;
- trend and carry eligibility;
- dependency shape;
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

P07 and upstream process trail inspected:

```text
docs/process/CARVER_P07_COMPLETE_COMBINED_TREND_CARRY_PORTFOLIO_SOURCE_SHAPE_GATE_DRAFT_2026-05-29.md
docs/process/CARVER_P07_COMPLETE_COMBINED_TREND_CARRY_PORTFOLIO_SOURCE_SHAPE_GATE_DRAFT_HOSTILE_AUDIT_RESULT_2026-05-29.md
docs/process/CARVER_P05_SOURCE_EXTRACT_AND_SOURCE_FAITHFULNESS_PACKET_2026-05-29.md
docs/process/CARVER_P06_SOURCE_EXTRACT_AND_SOURCE_FAITHFULNESS_PACKET_2026-05-29.md
docs/process/CARVER_S11_COMBINED_CARRY_TREND_CONFORMANCE_2026-05-29.md
```

Local source inspected:

```text
C:\Users\openclaw\Desktop\Carver\Carver.pdf
```

PDF text extraction used `pypdf` because `pdfplumber` was not installed in the local environment. Page references below are PDF page numbers from the local `Carver.pdf`, matching the convention used in the P05, P06, and S10 source packets.

## Source Range

P07 is not a book-native label. It is a Carver-process label for the complete Strategy Eleven combined carry/trend Jumbo portfolio shape.

The source basis is:

| Source area | PDF pages | Packet use |
| --- | ---: | --- |
| Strategy Eleven combined carry and trend | 264-275 | Combined trend/carry source identity, building-block forecast dependency, 60/40 style mix, top-down forecast weights, FDM table, capping/position-sizing handoff, and aggregate Jumbo combined result framing. |
| Strategy Four portfolio construction machinery | 118-144 | Multi-instrument risk-scaled portfolio framing, handcrafted instrument weights, IDM, Jumbo capital framing, target-risk policy, cost/liquidity/minimum-capital constraints. |
| Strategy Nine multiple trend following | 201-227 | EWMAC trend variations, trend cost eligibility, trend forecast weights, trend FDM, final trend forecast cap, and position-sizing handoff inherited by the trend side of Strategy Eleven. |
| Strategy Ten basic carry | 232-259 | Carry variations, carry cost eligibility, carry forecast weights, carry FDM, final carry forecast cap, carry production blockers, and aggregate Jumbo carry framing inherited by the carry side of Strategy Eleven. |
| Appendix C Jumbo universe | 690-695 | Complete 102-instrument Jumbo portfolio list, grouped by asset class, with descriptive names, broker market codes, exchange, currency, multiplier, and first year in the author's data. |
| Strategy Two/Three risk sizing and cost preliminaries | 70-88 and 95-115 | Risk-target, annual risk, minimum capital, risk-adjusted cost, and liquidity vocabulary inherited by later portfolio machinery. |

## Source-Faithfulness Findings

### P07 Identity

Source status:

```text
SOURCE_RANGE_LOCKED_PROCESS_LABEL_NOT_BOOK_LABEL
```

The book does not name a portfolio `P07`. The Carver process label `P07` refers to Strategy Eleven combined carry and trend applied across the Jumbo futures portfolio source frame.

Narrow source anchors:

- PDF page 264 introduces Strategy Eleven as the final Part One strategy combining trend and carry because the forecasts share a common scale.
- PDF pages 265-269 define the building-block forecast set: Strategy Nine EWMAC trend variations plus Strategy Ten smoothed carry variations.
- PDF pages 270-271 evaluate Strategy Eleven first by median instrument and then at aggregate Jumbo portfolio level.
- PDF pages 141-143 define the Jumbo portfolio as the large institutional portfolio used for aggregate strategy evaluation throughout the book.

Audit implication:

```text
P07_MUST_BE_DESCRIBED_AS_PROCESS_ALIAS_FOR_STRATEGY_ELEVEN_JUMBO_COMBINED_TREND_CARRY_PORTFOLIO
```

Do not state that the book itself names a `P07` portfolio. Do not treat S11 signal completion alone as complete P07.

### Source Framing

Source status:

```text
SOURCE_NATIVE_FUTURES_COMPLETE_BOOK_PORTFOLIO_CANDIDATE
```

The relevant book material is futures-native. Strategy Eleven combines futures trading-rule forecasts derived from Strategy Nine trend and Strategy Ten carry. Appendix C lists futures market codes, exchanges, currencies, multipliers, and first data years. P07 is not `CFD_DIRECT` and not `CFD_ADAPTER`.

Audit implication:

```text
CFD_DIRECT_AND_CFD_ADAPTER_REMAIN_CLOSED
```

Any CFD translation requires a later separate adapter gate after source-native P07 behavior exists.

### Dependency Shape

Source status:

```text
SOURCE_LOCKED_FOR_DIRECT_COMBINED_FORECAST_DEPENDENCY_NOT_P05_P06_OUTPUT_COMBINATION
```

PDF pages 264-265 frame Strategy Eleven as combining trading-rule forecasts because trend and carry forecasts are calibrated to a common scale. PDF pages 265-269 list the trend and carry forecast building blocks and describe applying the Strategy Nine top-down forecast-weighting method to those blocks.

The source therefore supports a direct combined-forecast dependency:

```text
Strategy Nine trend forecasts
Strategy Ten carry forecasts
-> Strategy Eleven combined forecast
-> cap / position sizing handoff
```

It does not support combining completed P05 and P06 portfolio desired-position outputs as the P07 source dependency.

Implementation implication:

```text
P07_SYNTHETIC_CONFORMANCE_SHOULD_CONSUME_LOCKED_SYNTHETIC_S11_COMBINED_FORECAST_OUTPUTS
```

The completed P05 and P06 portfolio surfaces remain adjacent portfolio-shape precedents. They are not inputs to P07 unless a later source artifact separately proves a portfolio-output combination rule.

### Complete Universe

Source status:

```text
SOURCE_RANGE_LOCKED_UNIVERSE_TRANSCRIPTION_REQUIRED_BEFORE_PRODUCTION_CLAIMS
```

Strategy Eleven aggregate evaluation uses the same Jumbo portfolio framing as the earlier Part One portfolio chapters. Appendix C is the required universe source. PDF page 690 states that Tables 172 to 183 are the complete 102-instrument Jumbo portfolio list. PDF pages 690-695 contain the table material.

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

Implementation implication:

```text
COMPLETE_P07_REQUIRES_APPENDIX_C_TRANSCRIPTION_OR_LOCKED_SYNTHETIC_MEMBER_FIXTURE
```

A synthetic conformance surface may use locked synthetic members to test P07 shape. It must not claim production complete-P07 readiness without a separate Appendix C transcription/readiness artifact.

### Instrument Weights

Source status:

```text
METHOD_SOURCE_LOCKED_EXACT_COMPLETE_102_WEIGHTS_NOT_YET_TRANSCRIBED
```

PDF pages 128-135 define instrument weights as risk-capital allocations across instrument sub-strategies. PDF pages 131-134 describe the top-down handcrafting method. PDF page 141 says the Jumbo portfolio instrument weights were constructed using that method.

Strategy Eleven does not introduce a different instrument-weighting method for the combined trend/carry portfolio. The source-faithful P07 assumption is therefore inheritance from Strategy Four Jumbo portfolio construction unless a later source audit finds a narrower exception.

Implementation implication:

```text
P07_WEIGHT_ENGINE_CAN_BE_SYNTHETIC_ONLY_BUT_COMPLETE_WEIGHTS_REQUIRE_LOCKED_GROUP_TAXONOMY
```

A toy conformance surface may test the top-down weighting contract using a locked synthetic taxonomy. A complete 102-instrument P07 production claim must first lock the Appendix C taxonomy and any group-layer interpretation used to reproduce the Jumbo handcrafting method.

### IDM

Source status:

```text
SOURCE_LOCKED_FOR_JUMBO_REFERENCE_VALUE_AND_APPROXIMATION_TABLE
```

PDF pages 122-123 introduce the instrument diversification multiplier as the position-scaling correction for diversification across instruments. PDF page 135 provides approximate IDM values by instrument count. PDF page 141 reports that the Jumbo portfolio IDM comes out at 2.47.

Strategy Eleven does not introduce a new portfolio IDM rule. The source-faithful P07 assumption is therefore inheritance from the Strategy Four Jumbo portfolio construction machinery unless a later source audit finds a narrower exception.

Implementation implication:

```text
SYNTHETIC_CONFORMANCE_MAY_REQUIRE_EXPLICIT_LOCKED_IDM
```

Complete-P07 synthetic code should fail closed unless the request explicitly locks whether it is using:

- the source Jumbo reference IDM of 2.47;
- the approximate table by member count;
- or a synthetic toy IDM declared solely for conformance testing.

No real-data correlation or IDM calculation is authorized here.

### Target Risk And Capital Policy

Source status:

```text
SOURCE_LOCKED_FOR_BOOK_REFERENCE_POLICY_OPERATOR_CAPITAL_STILL_CLOSED
```

PDF pages 70-80 introduce target-risk position sizing for futures. PDF pages 141-143 frame the Jumbo portfolio as an institutional-scale example using about USD 50 million so minimum-capital constraints do not bind. PDF pages 143-144 state that the book uses a 20% annual standard deviation target and gives breadth guidance for lower or higher targets.

Strategy Eleven does not introduce a different target-risk or capital-base rule for the combined trend/carry portfolio.

Implementation implication:

```text
TARGET_RISK_CAN_BE_SOURCE_REFERENCED_CAPITAL_AMOUNT_REQUIRES_EXPLICIT_OPERATOR_LOCK
```

A synthetic conformance surface may use declared toy capital and locked target risk for arithmetic shape only. It must not imply that real capital, margin, readiness, tradability, or deployment has been approved.

### Trend And Carry Building Blocks

Source status:

```text
SOURCE_LOCKED_FOR_STRATEGY_ELEVEN_FORECAST_BUILDING_BLOCKS
```

PDF page 265 lists the Strategy Eleven forecast building blocks:

- Strategy Nine EWMAC trend variations: EWMAC2, EWMAC4, EWMAC8, EWMAC16, EWMAC32, and EWMAC64.
- Strategy Ten smoothed carry variations: Carry5, Carry20, Carry60, and Carry120.

PDF pages 265-266 say Strategy Eleven selects the subset of forecasting rules that do not exceed the 0.15 SR speed limit using the turnover figures from the Strategy Nine and Strategy Ten tables and the instrument's risk-adjusted cost per trade.

Implementation implication:

```text
P07_TREND_AND_CARRY_ELIGIBILITY_MUST_BE_LOCKED_PER_MEMBER_OR_SYNTHETIC_TOY_DECLARED
```

No real-data cost calculation is authorized. A synthetic conformance surface may consume prevalidated synthetic eligibility flags, but must not calculate them from market rows.

### Style Mix, Forecast Weights, FDM, And Cap

Source status:

```text
SOURCE_LOCKED_FOR_STRATEGY_ELEVEN_SYNTHETIC_CONFORMANCE
```

PDF pages 266-268 apply the top-down weighting method:

- two styles: divergent trend and convergent carry;
- one trading rule inside each style: EWMAC trend and smoothed carry;
- 60% style allocation to trend and 40% to carry;
- equal allocation across eligible variations within each style/rule.

PDF pages 268-269 provide forecast-weight rows for selected combinations of EWMAC and carry variations. PDF page 269 provides the Strategy Eleven general FDM table by number of trading rules and states that intermediate values can be interpolated if necessary.

PDF page 270 says that after the combined forecast has the correct scale, the usual procedure is capping, position-sizing calculation, and buffering.

Implementation implication:

```text
SYNTHETIC_P07_CAN_CONSUME_LOCKED_S11_OUTPUTS_AND_APPLY_P07_PORTFOLIO_POSITION_INPUT_CONTRACTS
```

If a later synthetic P07 gate consumes already-combined locked S11 outputs, it should not recalculate Strategy Eleven Table 51/Table 52 internally unless that is explicitly authorized as part of the P07 surface. It should stop at complete-P07 desired position inputs and keep buffering, trade/no-trade decisions, aggregation, returns, PnL, Sharpe, drawdown, diagnostics, backtests, OOS, Lockbox, Forward, deployment, trading, and promotion closed.

### Aggregate Jumbo Result Framing

Source status:

```text
SOURCE_CONTEXT_NOT_LOCAL_EVIDENCE
```

PDF pages 270-274 evaluate Strategy Eleven with median instrument tables and aggregate Jumbo portfolio tables. This source context supports the P07 identity as a complete Jumbo combined trend/carry portfolio candidate.

It is not local Carver evidence. It does not authorize diagnostics, backtests, returns, PnL, Sharpe, drawdown, OOS, Lockbox, Forward, trading, deployment, promotion, or claims about local alpha.

Audit implication:

```text
BOOK_PERFORMANCE_TABLES_ARE_SOURCE_FRAMING_NOT_CARVER_PERFORMANCE_RESULTS
```

### Missing-Member Behavior

Source status:

```text
UNRESOLVED_FOR_RUNTIME_COMPLETE_P07
```

The source supports these constraints:

- PDF page 141 defines the Jumbo portfolio as instruments meeting liquidity and cost thresholds and having sufficient source data in the author's dataset.
- PDF pages 265-266 require forecasting-rule variations to be cheap enough for a given instrument before inclusion.
- PDF page 270 proceeds from a correctly scaled combined forecast to capping, position sizing, and buffering.

This packet does not find a production runtime policy for local missing members, unavailable contracts, failed provider mapping, stale bars, missing completed bars, missing trend forecasts, missing carry forecasts, missing curve legs, missing FX, missing costs, missing annual risk, or missing price risk.

Implementation implication:

```text
MISSING_MEMBER_POLICY_MUST_FAIL_CLOSED_UNLESS_SEPARATELY_LOCKED
```

Synthetic conformance can model missing members only as explicit fail-closed cases. It may not silently drop, substitute, reweight, or rescue a missing member.

## Locked For A Narrow Synthetic Conformance Gate

If this packet passes regular hostile audit, the following atoms are narrow enough for a future process-and-synthetic-code P07 conformance surface:

- P07 is a process alias for Strategy Eleven combined carry and trend over the Jumbo portfolio source frame.
- The lane is `SOURCE_NATIVE_FUTURES`.
- The complete universe source is Appendix C Tables 172-183, PDF pages 690-695.
- Instrument weighting method is top-down handcrafting inherited from Strategy Four.
- Jumbo IDM reference is 2.47; approximate IDM table exists on PDF page 135.
- Book reference target risk is 20% annual standard deviation, with breadth guidance on PDF pages 143-144.
- Book reference Jumbo capital context is about USD 50 million, not operator capital authorization.
- P07 dependency shape is direct Strategy Eleven combined forecasts, not P05/P06 portfolio-output combination.
- Strategy Eleven trend building blocks are EWMAC2, EWMAC4, EWMAC8, EWMAC16, EWMAC32, and EWMAC64.
- Strategy Eleven carry building blocks are Carry5, Carry20, Carry60, and Carry120.
- Strategy Eleven uses the 0.15 SR speed limit framework for selecting eligible forecasting rules.
- Strategy Eleven style grouping is divergent trend and convergent carry.
- Strategy Eleven source mix is 60% trend and 40% carry.
- Eligible variations receive equal weights inside their style/rule allocation.
- Strategy Eleven FDM is sourced from Table 52 by number of trading rules.
- The combined forecast is capped before position sizing.
- P07 may consume locked synthetic S11 combined forecast outputs and emit desired position inputs only.

## Still Blocked Before Complete-P07 Implementation Claims

The following remain blocked or require separate artifacts:

- exact complete 102-member Appendix C transcription or hash-bound machine-readable universe;
- local provider mapping for every member;
- source-native contract identity for every member;
- session calendar and completed-bar rule for every member;
- roll and back-adjustment artifacts;
- annual risk and daily price-risk source for every member;
- FX source for non-USD members;
- cost source and risk-adjusted cost for every member;
- trend forecast readiness for every member;
- carry forecast readiness for every member where carry is required;
- production carry construction and curve-leg availability for every carry member;
- production raw-carry sign convention by instrument family;
- fixed-month, seasonal, and wrong-sign carry policies where relevant;
- per-member trend and carry eligibility from prevalidated costs;
- liquidity validation;
- minimum-capital validation;
- exact group taxonomy for complete 102-member handcrafting weights;
- whether synthetic complete-P07 uses source Jumbo IDM 2.47, table approximation, or a toy locked IDM;
- operator capital base if any non-toy capital is used;
- local missing-member behavior beyond fail-closed rejection;
- rounding and buffering;
- trade/no-trade decisions;
- aggregation, returns, PnL, Sharpe, drawdown, diagnostics, backtests, OOS, Lockbox, Forward, deployment, trading, or promotion.

## Synthetic Implementation Shape Allowed Only After Audit

After a regular hostile audit with no blocking findings, the next possible gate may be a process-and-synthetic-code P07 conformance surface that:

- consumes locked synthetic S11 combined carry/trend forecast outputs only;
- consumes a locked synthetic member set and taxonomy, or a separately locked Appendix C transcription;
- consumes locked synthetic or source-shaped capital, target risk, IDM, price risk, FX, and eligibility inputs;
- applies P07 source-shaped handcrafting weights, IDM, target-risk/capital arithmetic, final forecast cap validation, and position-sizing input arithmetic;
- emits complete-P07 desired position inputs only;
- fails closed on unresolved source atoms or missing required inputs.

That future surface must not claim production P07 behavior unless all production source and data/readiness atoms are separately locked.

## Audit Requirements

Regular hostile audit should verify:

- this packet does not quote broad book text;
- page references match the local `Carver.pdf`;
- P07 is not falsely described as a book label;
- Strategy Eleven signal completion is not treated as complete P07 portfolio authorization;
- P05 and P06 desired-position outputs are not treated as the P07 dependency;
- Appendix C is treated as the universe source, not as local provider readiness;
- weights, IDM, target risk, capital, trend/carry eligibility, FDM, and caps are separated from data/readiness atoms;
- carry-specific production blockers remain closed;
- missing-member behavior remains fail-closed and unresolved for production;
- no implementation, real data, diagnostics, backtests, CFD adapters, Opus/GPT execution, remote operations, deployment, trading, or promotion are authorized.

Opus/GPT audit is not required for this packet unless the operator wants an external source-faithfulness review before opening the implementation gate.

## Next Authorization Prompt If Implementation Is Opened

Use this only after the source packet receives a no-blocking regular hostile audit.

```text
Operator authorizes exactly one process-and-synthetic-code gate for the Carver
P07 complete combined trend/carry portfolio synthetic conformance surface.

Scope:
Clean Carver workspace only. Implement a tiny synthetic-only P07 surface that
consumes locked synthetic S11 combined trend/carry forecasts, locked synthetic
P07 member identity/taxonomy, locked synthetic or source-shaped instrument
weights, locked IDM, locked target risk/capital inputs, prevalidated synthetic
price risk/FX/cost eligibility, final forecast caps, and emits complete-P07
desired position inputs only.

Required status:
PROCESS_AND_SYNTHETIC_CODE_CARVER_P07_COMPLETE_COMBINED_TREND_CARRY_PORTFOLIO_CONFORMANCE_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST

Allowed:
Code contracts, synthetic tests, and process documentation for P07 complete
combined trend/carry portfolio conformance only.

Forbidden:
No real data, no market-row parsing, no NinjaTrader export, no diagnostics,
no backtests, no returns, no PnL, no Sharpe, no drawdown, no OOS, no Lockbox,
no Forward, no CFD adapters, no old QuantLab imports, no tuning, no deployment,
no trading, no promotion, no production source locks, no silent member dropping
or substitution, no Opus/GPT execution, no remote operations.
```

## Non-Authorization

This packet authorizes no code edits, no tests, no real-data execution, no market-row parsing, no NinjaTrader export, no diagnostics, no backtests, no returns, no PnL, no Sharpe, no drawdown, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old-adapter import, no old workspace pipeline use, no tuning, no deployment, no trading, no promotion, no portfolio implementation, no P07 implementation, no Opus/GPT execution, no remote push, and no GitHub action.
