# Carver Appendix C Risk FX Cost Carry-Leg Readiness Shape Gate Draft

Date: 2026-05-29

Status:

```text
PROCESS_ONLY_CARVER_APPENDIX_C_RISK_FX_COST_CARRY_LEG_READINESS_SHAPE_GATE_DRAFT_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Define the process-only boundary for future Appendix C annual risk, price risk, FX, cost, risk-adjusted cost, trend/carry eligibility, and carry curve-leg readiness.

This draft follows audited session/roll/completed-bar readiness execution. It does not resolve risk, FX, costs, carry legs, trend eligibility, carry eligibility, or market-data readiness.

## Lane Class

```text
SOURCE_NATIVE_FUTURES
```

No `CFD_DIRECT` or `CFD_ADAPTER` lane is opened.

## Current Inputs

Appendix C source universe:

```text
docs/researchops/portfolios/CARVER_APPENDIX_C_JUMBO_UNIVERSE_LOCK_2026-05-29.csv
Rows: 102
```

Contract identity artifact:

```text
docs/researchops/contract_identity/CARVER_APPENDIX_C_CONTRACT_IDENTITY_STATUS_2026-05-29.csv
SHA256: 5EA130CF855845B948E66881784990FE7F1DD41F765F95DF09A025DD673C85C2
```

Session/roll/completed-bar readiness artifact:

```text
docs/researchops/session_roll/CARVER_APPENDIX_C_SESSION_ROLL_COMPLETED_BAR_READINESS_STATUS_2026-05-29.csv
SHA256: A9EA3963304F6BFE5DA5C290BEC42095F85031D77736BCD95AC677DE465ABF16
```

Session/roll/completed-bar audit disposition:

```text
NO BLOCKING FINDINGS
AUDIT_DISPOSITION: PASS_PROCESS_SOURCE_SESSION_ROLL_COMPLETED_BAR_READINESS_EXECUTION_SCOPE
```

Current session/roll/completed-bar state:

```text
SESSION_ROLL_BLOCKED_NO_COMPLETED_BAR_POLICY: 41
SESSION_ROLL_BLOCKED_CONTRACT_IDENTITY: 61
SESSION_ROLL_READY_STATIC_PROCESS_LOCKED: 0
NO_MARKET_ROW_ACCESS: 102
production_session_roll_lock_status NOT_LOCKED: 102
```

## What This Draft Locks

This draft locks only the readiness shape:

- risk/FX/cost/carry-leg readiness is downstream of contract identity and session/roll/completed-bar readiness;
- no row can become risk/FX/cost/carry-leg ready while contract identity or session/roll/completed-bar readiness is blocked;
- annual risk and daily price risk must be explicitly source-native, completed-bar-only, timestamp-aligned, and no-lookahead before any strategy or portfolio computation consumes them;
- FX must have a source, timestamp convention, base/account currency relationship, and stale/missing policy before position-sizing inputs can be real;
- costs and risk-adjusted costs must have source-native commission, slippage, spread, turnover, annualization, and cost-unit conventions before trend/carry eligibility can be calculated;
- carry curve legs require source-native held/comparison contract availability, synchronized completed prices, expiry metadata, seasonal/wrong-sign policy, and fixed-month policy where applicable;
- no row may be silently dropped, substituted, reweighted, or promoted from synthetic readiness into real-data readiness.

## What This Draft Does Not Lock

This draft does not lock:

- annual percentage risk for any instrument;
- daily price risk for any instrument;
- volatility span, blend, warm-up, missing-bar, or no-lookahead proof for production risk estimates;
- FX source, FX rate, FX timestamp, or FX stale/missing policy;
- commission schedule;
- spread/slippage estimate;
- turnover estimate;
- risk-adjusted cost;
- 0.15 SR cost eligibility as a row-level production calculation;
- eligible EWMAC speed sets for production instruments;
- eligible carry span sets for production instruments;
- held carry contract;
- comparison carry contract;
- raw-carry sign convention by production instrument;
- expiry calendar or expiry-distance convention by instrument;
- fixed-month commodity policy;
- seasonal or wrong-sign carry policy;
- carry curve-leg availability;
- liquidity validation;
- minimum capital validation;
- real-data Development/Reconciliation readiness.

## Source Anchors Already Present In Process

M1 position sizing requires prevalidated risk, current held-contract price, multiplier, FX, capital, target risk, instrument weights, IDM, and timestamp alignment before producing desired exposure inputs.

```text
docs/process/CARVER_M1_POSITION_SIZING_AND_RISK_SCALING_MODULE_SPEC_2026-05-28.md
```

S09 daily price-risk conversion is source-shaped but does not lock upstream annual risk values for any instrument.

```text
docs/process/CARVER_S09_DAILY_PRICE_RISK_SOURCE_GATE_2026-05-29.md
```

M5 carry construction requires source-native curve contract identity, held/comparison contract roles, synchronized completed prices, expiry metadata, raw-carry sign convention, fixed-month and seasonal/wrong-sign policies, and price risk before carry can be constructed.

```text
docs/process/CARVER_M5_FUTURES_CURVE_AND_CARRY_CONSTRUCTION_MODULE_SPEC_2026-05-28.md
```

P05/P06/P07 synthetic portfolio conformance consumed locked synthetic or source-shaped price risk, FX, cost eligibility, and carry eligibility inputs. Those synthetic locks are not production readiness.

## Future Risk FX Cost Carry-Leg Artifact Fields

A future execution artifact must be machine-readable and preserve source row identity.

Minimum required fields:

- `row_id`;
- `appendix_table`;
- `source_group`;
- `descriptive_name`;
- `author_market_code`;
- `local_canonical_instrument_id`;
- `contract_identity_status`;
- `session_roll_readiness_status`;
- `risk_fx_cost_carry_leg_readiness_status`;
- `annual_risk_status`;
- `annual_risk_reference`;
- `daily_price_risk_status`;
- `daily_price_risk_reference`;
- `risk_no_lookahead_status`;
- `risk_timestamp_alignment_status`;
- `fx_source_status`;
- `fx_source_reference`;
- `fx_timestamp_policy_status`;
- `fx_stale_missing_policy_status`;
- `commission_status`;
- `commission_reference`;
- `spread_slippage_status`;
- `spread_slippage_reference`;
- `turnover_status`;
- `turnover_reference`;
- `risk_adjusted_cost_status`;
- `trend_eligibility_status`;
- `carry_eligibility_status`;
- `held_carry_contract_status`;
- `comparison_carry_contract_status`;
- `carry_curve_leg_availability_status`;
- `raw_carry_sign_policy_status`;
- `expiry_calendar_status`;
- `fixed_month_policy_status`;
- `seasonal_wrong_sign_policy_status`;
- `liquidity_status`;
- `minimum_capital_status`;
- `market_row_access_status`;
- `block_reason`;
- `notes`.

## Allowed Readiness Status Values

Future rows must use one of:

```text
RISK_FX_COST_CARRY_LEG_READY_STATIC_PROCESS_LOCKED
RISK_FX_COST_CARRY_LEG_REQUIRES_REVIEW
RISK_FX_COST_CARRY_LEG_BLOCKED_CONTRACT_IDENTITY
RISK_FX_COST_CARRY_LEG_BLOCKED_SESSION_ROLL_COMPLETED_BAR
RISK_FX_COST_CARRY_LEG_BLOCKED_NO_ANNUAL_RISK_EVIDENCE
RISK_FX_COST_CARRY_LEG_BLOCKED_NO_DAILY_PRICE_RISK_EVIDENCE
RISK_FX_COST_CARRY_LEG_BLOCKED_NO_FX_EVIDENCE
RISK_FX_COST_CARRY_LEG_BLOCKED_NO_COST_EVIDENCE
RISK_FX_COST_CARRY_LEG_BLOCKED_NO_RISK_ADJUSTED_COST_POLICY
RISK_FX_COST_CARRY_LEG_BLOCKED_TREND_ELIGIBILITY_UNRESOLVED
RISK_FX_COST_CARRY_LEG_BLOCKED_CARRY_ELIGIBILITY_UNRESOLVED
RISK_FX_COST_CARRY_LEG_BLOCKED_NO_CARRY_CURVE_LEG_EVIDENCE
RISK_FX_COST_CARRY_LEG_BLOCKED_LIQUIDITY_OR_MINIMUM_CAPITAL_UNRESOLVED
```

Default status for all rows before execution:

```text
RISK_FX_COST_CARRY_LEG_REQUIRES_REVIEW
```

Rows with blocked contract identity must remain:

```text
RISK_FX_COST_CARRY_LEG_BLOCKED_CONTRACT_IDENTITY
```

Rows with blocked session/roll/completed-bar readiness must remain:

```text
RISK_FX_COST_CARRY_LEG_BLOCKED_SESSION_ROLL_COMPLETED_BAR
```

unless a separate readiness gate resolves them first.

## Evidence Requirements

Acceptable evidence for a future execution gate:

- audited Appendix C universe artifact;
- audited provider mapping artifact;
- audited contract identity artifact;
- audited session/roll/completed-bar artifact;
- static source-native annual risk policy;
- static source-native daily price-risk construction policy;
- static FX source and timestamp policy;
- static commission schedule;
- static spread/slippage or cost model source;
- static turnover source for Strategy Nine, Strategy Ten, and Strategy Eleven eligibility;
- static risk-adjusted cost calculation policy;
- static eligible EWMAC speed-set rule;
- static eligible carry span-set rule;
- static held/comparison carry curve-leg availability evidence;
- static expiry calendar, fixed-month, and seasonal/wrong-sign policy evidence;
- static liquidity and minimum-capital policy evidence.

Forbidden as standalone authority:

- market rows;
- NinjaTrader historical export;
- provider API responses;
- chart display values;
- old QuantLab data-prep scripts;
- old CFD broker spread, swap, or session assumptions;
- synthetic P05/P06/P07 fixtures;
- performance results;
- diagnostics;
- backtests;
- informal memory.

## Risk Requirements

Future production risk readiness must define:

- whether annual percentage risk or daily price-point risk is consumed;
- how annual risk is estimated;
- how daily price risk is derived;
- warm-up and first usable date;
- no-lookahead proof;
- stale/missing/invalid price handling;
- timestamp alignment to completed bars;
- how risk estimates are invalidated when contract identity, session, roll, or back-adjustment rules change.

No annual risk or daily price risk may be consumed from a synthetic conformance fixture or from old QuantLab pipeline state.

## FX Requirements

Future production FX readiness must define:

- instrument currency;
- account/base currency;
- FX source;
- FX timestamp convention;
- FX completed-bar or source-publication convention;
- stale/missing policy;
- cross-rate policy;
- alignment with the instrument sizing timestamp.

No FX rate may be inferred from a broker CFD conversion, old worksheet, or historical result.

## Cost And Eligibility Requirements

Future production cost readiness must define:

- commission source and unit;
- spread/slippage source and unit;
- turnover source by strategy variation;
- risk-adjusted cost calculation;
- Strategy Nine EWMAC speed eligibility;
- Strategy Ten carry span eligibility;
- Strategy Eleven combined-rule eligibility;
- treatment of missing cost evidence;
- no post-result tuning or variation rescue.

The 0.15 SR threshold is a source-shaped rule already identified in process artifacts, but row-level eligibility still requires source-native cost and turnover evidence.

## Carry-Leg Requirements

Future production carry-leg readiness must define:

- held contract selection rule;
- comparison contract selection rule;
- synchronized completed prices for both legs;
- raw-carry sign convention;
- expiry calendar and expiry-distance convention;
- fixed-month commodity policy where required;
- seasonal and wrong-sign carry policy;
- sparse second-contract history policy;
- roll-day and curve-leg missing-data policy;
- whether the local provider can supply the required curve legs without substitution.

No carry-leg readiness may be inferred from a front-contract-only mapping.

## Relationship To Current Appendix C State

The current session/roll/completed-bar artifact has:

```text
SESSION_ROLL_READY_STATIC_PROCESS_LOCKED: 0
```

Therefore this draft does not claim any row is ready for risk/FX/cost/carry-leg execution.

The 102 Appendix C rows remain upstream-blocked until contract identity and session/roll/completed-bar readiness are resolved by separate gates.

## Relationship To Later Gates

Risk/FX/cost/carry-leg readiness must precede any real-data Development/Reconciliation gate for the complete Part One Jumbo portfolio.

It also precedes:

- diagnostics;
- backtests;
- OOS;
- Lockbox;
- Forward;
- deployment;
- trading;
- promotion.

This draft does not authorize any later gate.

## Audit Requirements

This draft should receive a lean regular hostile audit before being treated as locked.

Audit focus:

- the draft does not resolve risk, FX, costs, carry legs, or eligibility;
- the draft accurately carries the current Appendix C session/roll blocked state;
- no row becomes ready while upstream readiness is blocked;
- synthetic conformance inputs are not promoted into production readiness;
- no market-row parsing, NinjaTrader export, provider API access, diagnostics, backtests, old QuantLab active-pipeline use, CFD adapter work, deployment, trading, promotion, Opus/GPT execution, remote operation, remote push, or GitHub action is opened.

Regular hostile audit results should be preserved automatically as separate process-only audit-result records when the active authorization scope permits record creation.

## Next Proposed Authorization

```text
Operator authorizes one process-only Carver Appendix C risk/FX/cost/carry-leg
readiness execution gate using static risk, FX, cost, eligibility, and carry-leg
policy evidence.

Scope:
Create a process/source readiness artifact for Appendix C annual risk, price
risk, FX sources, costs, risk-adjusted costs, trend/carry eligibility, and carry
curve-leg availability using only audited static evidence. Resolve or fail-close
each row before any market-row access.

Allowed:
Read-only inspection of current Carver process artifacts, audited static CSV
artifacts, and explicitly named static risk/FX/cost/eligibility/carry-leg policy
evidence, plus creation of process/source documentation or a machine-readable
readiness artifact.

Forbidden:
No code edits, no tests, no real market data, no market-row parsing, no
NinjaTrader export, no provider API access unless separately specified as static
evidence access, no diagnostics, no backtests, no OOS, no Lockbox, no Forward,
no CFD adapters, no old QuantLab pipeline use, no tuning, no deployment, no
trading, no promotion, no Opus/GPT execution, no remote operations.
```

## Non-Authorization

This shape gate draft authorizes no code edits, no tests, no real market data, no market-row parsing, no NinjaTrader historical export, no provider API access, no diagnostics, no backtests, no returns, no PnL, no Sharpe, no drawdown, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old QuantLab pipeline use, no tuning, no deployment, no trading, no promotion, no risk/FX/cost/carry-leg execution, no market data readiness claim, no Opus/GPT execution, no remote push, and no GitHub action.
