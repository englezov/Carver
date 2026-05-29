# Carver Part One Jumbo Portfolio Universe/Readiness Shape Gate Draft

Date: 2026-05-29

Status:

```text
PROCESS_ONLY_CARVER_PART_ONE_JUMBO_PORTFOLIO_UNIVERSE_READINESS_SHAPE_GATE_DRAFT_NOT_DATA_NOT_IMPLEMENTATION
```

## Purpose

Define the shared Appendix C / Jumbo portfolio universe and local readiness boundary after completed Part One P05/P06/P07 synthetic conformance and Opus 4.7 strategy/portfolio source-faithfulness pass.

This is a process-only gate draft. It does not transcribe the full Appendix C universe into production data, does not map provider symbols, does not inspect market rows, does not run diagnostics, does not run backtests, and does not authorize any implementation.

## Inputs Inspected

Required Carver guardrail files:

```text
README.md
docs/mission/CARVER_SOURCE_NATIVE_RESEARCH_CHARTER_2026-05-28.md
docs/process/CLEAN_WORKSPACE_MIGRATION_RECORD_2026-05-28.md
docs/process/LANE_CLASSIFICATION_AND_ADAPTER_QUARANTINE_RULES_2026-05-28.md
```

Post-P07 and Opus context:

```text
docs/process/CARVER_POST_P07_COMPLETE_COMBINED_TREND_CARRY_PORTFOLIO_NEXT_STEP_DECISION_2026-05-29.md
docs/process/CARVER_OPUS_47_NOT_PREVIOUSLY_AUDITED_STRATEGY_PORTFOLIO_AUDIT_RESULT_2026-05-29.md
docs/process/CARVER_P07_COMPLETE_COMBINED_TREND_CARRY_PORTFOLIO_CONFORMANCE_2026-05-29.md
docs/process/CARVER_P07_SOURCE_EXTRACT_AND_SOURCE_FAITHFULNESS_PACKET_2026-05-29.md
```

Local source:

```text
C:\Users\openclaw\Desktop\Carver\Carver.pdf
```

Narrow PDF inspection used Appendix C PDF pages 690-695 only.

## Current State

The Part One synthetic signal and portfolio graph is complete at process-and-synthetic-code scope:

```text
S09 trend forecast block
S10 carry construction and carry forecast block
S11 combined carry/trend forecast block
P05 complete trend portfolio synthetic conformance
P06 complete carry portfolio synthetic conformance
P07 complete combined trend/carry portfolio synthetic conformance
```

The latest Opus 4.7 strategy/portfolio audit recorded:

```text
BLOCKING_FINDINGS: NO
AUDIT_DISPOSITION: PASS_NOT_PREVIOUSLY_OPUS_AUDITED_STRATEGY_PORTFOLIO_SCOPE
```

Opus confirmed that Appendix C is the complete Jumbo universe source, but not local provider readiness.

## Gate Decision

The next clean Part One chapter is:

```text
PART_ONE_JUMBO_PORTFOLIO_UNIVERSE_AND_READINESS_SHAPE_GATE_DRAFT
```

This gate should create the map needed before any future real-data or production-facing implementation work can be safely authorized.

It should not create the implementation itself.

## Source Universe Anchor

Appendix C is the source universe anchor for the Jumbo portfolio.

PDF page 690 states that Tables 172 to 183 are the complete list of all 102 instruments in the Jumbo portfolio, broken down by asset class.

The source table fields are:

- descriptive instrument name;
- broker market code used by the author;
- exchange;
- currency;
- futures multiplier used by the author;
- first year when the instrument appears in the author's dataset.

The source also warns that:

- market codes may vary across brokers;
- author market codes may differ from official exchange codes;
- the instrument may be available on other exchanges;
- other multiplier variants may exist;
- first year in the author's dataset is not necessarily the first trading year.

These warnings are readiness blockers, not cosmetic footnotes.

## Appendix C Table Range

The complete Jumbo universe source range is:

| Table | Source group | PDF pages | Readiness meaning |
| --- | --- | ---: | --- |
| 172 | US bond and interest rate futures | 690-691 | Requires source-native contract identity and provider mapping. |
| 173 | Other bond and interest rate futures | 691 | Requires source-native contract identity, currency, exchange, and session readiness. |
| 174 | US equity index futures | 691-692 | Requires ticker provenance and no substitution between micro/mini/full variants. |
| 175 | European equity index futures | 692 | Requires exchange, currency, FX, and provider mapping readiness. |
| 176 | European stock sector futures | 692 | Requires sector futures provider coverage and taxonomy readiness. |
| 177 | Asian equity index futures | 693 | Requires exchange, currency, session, and provider coverage readiness. |
| 178 | Volatility futures | 693 | Requires source-native volatility futures identity and roll/session readiness. |
| 179 | Major FX futures | 693-694 | Requires currency-pair futures identity and contract multiplier readiness. |
| 180 | Cross and EM FX futures | 694 | Requires currency and provider mapping checks, especially non-USD quote conventions. |
| 181 | Metal and crypto futures | 694 | Requires metal/crypto futures identity, multiplier, and source-native data readiness. |
| 182 | Energy futures | 695 | Requires energy contract identity, carry-leg readiness, and seasonal/wrong-sign caution where relevant. |
| 183 | Agricultural futures | 695 | Requires agriculture contract identity, roll, seasonality, and carry-readiness caution. |

## Required Universe Artifact Before Data Work

Before any future real-data or production-facing P05/P06/P07 work, Carver should create a separate Appendix C universe artifact.

That artifact should be one of:

```text
PROCESS_ONLY_APPENDIX_C_TRANSCRIPTION_PACKET
```

or

```text
HASH_BOUND_MACHINE_READABLE_APPENDIX_C_UNIVERSE
```

Minimum required fields:

- Appendix C table number;
- source PDF page;
- asset class / source group;
- descriptive name exactly as used in source;
- author broker market code;
- exchange;
- currency;
- multiplier;
- first year in author's dataset;
- local canonical instrument id, if separately authorized;
- local provider symbol, if separately authorized;
- provider mapping status;
- source-native lane status;
- substitution policy;
- readiness status.

This draft does not create that transcription.

## Lane Classification

The only lane for the next Appendix C/Jumbo readiness chapter is:

```text
SOURCE_NATIVE_FUTURES
```

Rejected lanes:

```text
CFD_DIRECT
CFD_ADAPTER
```

Any CFD translation remains closed until source-native futures behavior exists and a separate CFD adapter gate is explicitly authorized.

## Local Provider Mapping Boundary

Appendix C broker market codes are not automatically local provider symbols.

Future readiness work must explicitly decide, member by member:

- whether the local provider has the source-native futures contract;
- whether the provider symbol maps to the same descriptive instrument;
- whether the exchange matches or is an accepted source-native equivalent;
- whether the contract multiplier matches the source or has an explicitly locked conversion;
- whether currency and quote conventions match;
- whether micro/mini/full variants are preserved without substitution;
- whether the first available local year is sufficient for the intended gate;
- whether missing members fail closed.

No unavailable contract may be silently replaced by a nearby symbol, CFD, ETF, full-size variant, micro variant, cash index, continuous synthetic proxy, or old QuantLab convenience mapping.

## Contract Identity Atoms

Each future production-facing member needs locked contract identity:

- source descriptive name;
- source broker market code;
- official/local provider symbol;
- exchange;
- currency;
- multiplier;
- tick size and tick value, if required by local sizing or cost work;
- contract family and delivery month pattern;
- first source year and first local available year;
- active/inactive status;
- source-native lane declaration.

None of these are locked by the completed synthetic P05/P06/P07 surfaces.

## Session, Roll, And Completed-Bar Atoms

Before any market-row parsing or strategy computation, each member must have:

- completed-bar definition;
- timezone convention;
- session calendar;
- holiday handling;
- daily close convention;
- continuous futures construction rule;
- roll trigger;
- back-adjustment rule;
- stale/missing-bar policy;
- timestamp alignment policy across instruments;
- source-native futures validation status.

The Carver standing rule remains:

```text
COMPLETED_BARS_ONLY
```

This gate draft does not authorize parsing rows to determine these atoms.

## Risk, FX, And Cost Readiness

Future readiness work must separately lock:

- annual risk source;
- daily price risk source;
- risk units and price units;
- FX source for non-USD members and non-USD contracts;
- FX timestamp alignment;
- commission source;
- spread/slippage source;
- risk-adjusted cost calculation;
- cost eligibility inputs for Strategy Nine, Strategy Ten, and Strategy Eleven;
- minimum capital constraints;
- liquidity constraints;
- missing risk/FX/cost fail-closed behavior.

Synthetic P05/P06/P07 consumed prevalidated toy risk, FX, and cost inputs. That is not production readiness.

## Trend Eligibility Readiness

Trend-side readiness inherits Strategy Nine constraints.

Future P05/P07 real-data work must lock:

- EWMAC2, EWMAC4, EWMAC8, EWMAC16, EWMAC32, and EWMAC64 eligibility;
- source-cited scalars and caps;
- per-member cost-speed eligibility;
- Strategy Nine FDM row selection;
- final trend forecast cap;
- no post-result tuning of speed sets or eligibility.

The `0.15 SR` cost-units threshold is book-verified at PDF page 216, but production use remains blocked until the threshold and per-member cost/turnover inputs are transcribed as machine-readable locks.

## Carry Eligibility Readiness

Carry-side readiness inherits Strategy Ten constraints.

Future P06/P07 real-data work must lock:

- held contract role;
- comparison contract role;
- raw-carry sign convention by instrument family;
- expiry distance and annualization convention;
- fixed-month treatment;
- seasonal and wrong-sign policy;
- curve-leg availability;
- Carry5, Carry20, Carry60, and Carry120 eligibility;
- carry scalar and cap;
- Strategy Ten carry FDM row selection;
- cost eligibility for carry variations;
- no post-result tuning of carry spans or eligibility.

The completed S10/M5 and S10 forecast-block surfaces are synthetic conformance only. They do not production-lock carry construction for Appendix C members.

## Combined Trend/Carry Readiness

P07 inherits Strategy Eleven constraints from S11.

Future P07 real-data work must lock:

- direct dependency on S11 combined forecasts;
- no combination of P05 and P06 desired-position outputs;
- trend/carry style grouping;
- 60/40 style mix;
- top-down eligible-rule weights;
- Table 51 row selection;
- Table 52 FDM row or interpolation policy;
- final combined forecast cap;
- synchronization of trend and carry forecast timestamps.

Table 51 is book-verified at PDF page 268. Table 52 and its interpolation policy are book-verified at PDF page 269. Production use remains blocked until they are transcribed as machine-readable locks.

## Portfolio Construction Readiness

Future P05/P06/P07 readiness must separately lock:

- complete Appendix C member set;
- exact member taxonomy used for top-down handcrafted weights;
- instrument weights;
- IDM policy;
- target risk;
- operator capital, if non-toy capital is ever used;
- forecast divisor / position-sizing convention;
- rounding policy;
- buffering policy;
- trade/no-trade policy;
- aggregation policy.

Synthetic P05/P06/P07 emitted desired position inputs only. They did not authorize portfolio execution.

## Missing-Member Policy

Default missing-member behavior:

```text
FAIL_CLOSED_NO_DROP_NO_SUBSTITUTE_NO_REWEIGHT
```

This applies to missing:

- Appendix C member;
- provider symbol;
- contract identity;
- session calendar;
- completed bar;
- roll artifact;
- risk input;
- FX input;
- cost input;
- trend forecast;
- carry forecast;
- S11 combined forecast;
- curve leg.

Any future alternative missing-member behavior requires separate operator authorization and source/governance justification before implementation.

## What This Gate Opens

This draft opens only a process chapter for deciding readiness shape.

Allowed next artifacts after audit may include:

- Appendix C transcription/source packet;
- provider mapping readiness packet;
- source-native contract identity packet;
- risk/FX/cost readiness packet;
- trend/carry eligibility readiness packet;
- a later process-only decision on whether any real-data gate is safe to open.

Each would require its own authorization.

## What Remains Closed

Still closed:

- code edits;
- tests;
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
- old QuantLab active-pipeline use;
- tuning;
- deployment;
- trading;
- promotion;
- production source locks not explicitly listed as process-source anchors;
- provider data access;
- GitHub push or remote operation.

## Rejected Interpretations

### Appendix C Equals Provider Readiness

Rejected.

Reason:

```text
SOURCE_UNIVERSE_IS_NOT_LOCAL_PROVIDER_MAPPING
```

Appendix C identifies the book universe. It does not prove local symbol availability, continuous contract construction, FX, cost, risk, liquidity, or completed-bar readiness.

### P05/P06/P07 Synthetic Completion Equals Production Portfolio Completion

Rejected.

Reason:

```text
SYNTHETIC_CONFORMANCE_IS_NOT_PRODUCTION_READINESS
```

The completed surfaces validate shape only.

### Missing Members Can Be Dropped Or Reweighted

Rejected.

Reason:

```text
COMPLETE_BOOK_PORTFOLIO_IDENTITY_REQUIRES_FAIL_CLOSED_MISSING_MEMBER_BEHAVIOR
```

Dropping, substituting, or reweighting members would create a different portfolio unless separately source-locked and operator-authorized.

### Old QuantLab Can Supply Mappings

Rejected.

Reason:

```text
OLD_QUANTLAB_ACTIVE_PIPELINE_AND_ADAPTER_STATE_REMAINS_QUARANTINED
```

Old files may not become active authority without deliberate clean reintroduction, hash binding, and a separate Carver artifact.

## Audit Requirements

This draft should receive a lean regular hostile audit, preferably by subagent, before it is treated as locked.

Audit focus:

- no implementation, data, diagnostic, backtest, OOS, deployment, trading, or promotion authorization is smuggled into the draft;
- Appendix C is treated as source universe only, not provider readiness;
- P05/P06/P07 synthetic surfaces remain synthetic conformance only;
- complete 102-member universe identity is preserved;
- missing members fail closed;
- no silent substitution, member dropping, or reweighting is allowed;
- `SOURCE_NATIVE_FUTURES` is the only lane;
- CFD adapter work and old `QuantLab_v3` active-pipeline use remain closed;
- production source locks are distinguished from process source anchors and machine-readable future locks;
- no Opus/GPT execution or remote operation is opened.

Regular hostile audit results should be automatically preserved as a separate process-only audit-result file under the lean Carver process.

Opus/GPT audit is not required for this process-only readiness draft unless the operator separately requests an external source-faithfulness review or a production-facing source lock dispute emerges.

## Next Proposed Authorization

If this draft passes lean hostile audit, the next clean gate is likely an Appendix C transcription/source packet, not a data gate.

```text
Operator authorizes one process-only Carver Appendix C Jumbo universe
transcription/source packet.

Scope:
Create a process-only source packet that transcribes or otherwise records the
Appendix C Tables 172-183 Jumbo universe fields needed for later readiness
work, including table number, PDF page, descriptive name, author market code,
exchange, currency, multiplier, first source data year, asset group, and
machine-readable lock requirements before any provider mapping or data work.

Allowed:
Read-only inspection of current Carver process artifacts and local Carver.pdf,
plus creation of one process source/transcription packet artifact.

Forbidden:
No code edits, no tests, no real data, no market-row parsing, no NinjaTrader
export, no diagnostics, no backtests, no OOS, no Lockbox, no Forward, no CFD
adapters, no old QuantLab pipeline use, no tuning, no deployment, no trading,
no promotion, no Opus/GPT execution, no remote operations.
```

## Non-Authorization

This gate draft authorizes no code edits, no tests, no real-data execution, no market-row parsing, no NinjaTrader export, no diagnostics, no backtests, no returns, no PnL, no Sharpe, no drawdown, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old-adapter import, no old workspace pipeline use, no tuning, no deployment, no trading, no promotion, no portfolio execution, no production data readiness claim, no Opus/GPT execution, no remote push, and no GitHub action.
