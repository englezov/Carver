# Carver Appendix C Session Roll Completed-Bar Readiness Shape Gate Draft

Date: 2026-05-29

Status:

```text
PROCESS_ONLY_CARVER_APPENDIX_C_SESSION_ROLL_COMPLETED_BAR_READINESS_SHAPE_GATE_DRAFT_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Define the process-only boundary for future Appendix C session calendar, roll, back-adjustment, completed-bar timestamp, stale/missing bar, and alignment readiness.

This draft follows audited contract identity execution. It does not resolve sessions, rolls, completed bars, back-adjustment, stale/missing bar rules, or data readiness.

## Current Inputs

Contract identity status artifact:

```text
docs/researchops/contract_identity/CARVER_APPENDIX_C_CONTRACT_IDENTITY_STATUS_2026-05-29.csv
```

Contract identity audit disposition:

```text
NO BLOCKING FINDINGS
AUDIT_DISPOSITION: PASS_PROCESS_SOURCE_CONTRACT_IDENTITY_EXECUTION_SCOPE
```

Current contract identity state:

```text
CONTRACT_IDENTITY_REQUIRES_REVIEW: 41
CONTRACT_IDENTITY_BLOCKED_UNAVAILABLE: 59
CONTRACT_IDENTITY_BLOCKED_VARIANT_MISMATCH: 2
CONTRACT_IDENTITY_LOCKED_SOURCE_NATIVE: 0
```

## What This Draft Locks

This draft locks only the readiness shape:

- session/roll/completed-bar readiness is separate from contract identity;
- no row can become session-ready while contract identity is blocked;
- no row can become market-data-ready from static session/roll process wording alone;
- completed bars are mandatory for future data work;
- market-row parsing remains closed;
- roll and back-adjustment rules require explicit static evidence before any price series can be accepted;
- stale or missing bars must fail closed;
- no incomplete member may be dropped, substituted, or reweighted.

## What This Draft Does Not Lock

This draft does not lock:

- session calendar for any instrument;
- daily close timestamp;
- timezone alignment;
- holiday calendar;
- early close policy;
- completed-bar rule;
- roll trigger;
- roll calendar;
- roll price source;
- back-adjustment method;
- stale bar threshold;
- missing bar treatment;
- production continuous series;
- market data source;
- diagnostics;
- backtests;
- risk, FX, cost, or carry-leg readiness.

## Future Session Roll Completed-Bar Artifact Fields

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
- `session_calendar_status`;
- `session_calendar_reference`;
- `trading_hours_template`;
- `timezone_status`;
- `timezone_reference`;
- `daily_close_time_status`;
- `daily_close_time_reference`;
- `completed_bar_policy_status`;
- `completed_bar_policy_reference`;
- `holiday_calendar_status`;
- `holiday_calendar_reference`;
- `early_close_policy_status`;
- `early_close_policy_reference`;
- `roll_rule_status`;
- `roll_rule_reference`;
- `delivery_cycle_status`;
- `delivery_cycle_reference`;
- `back_adjustment_status`;
- `back_adjustment_reference`;
- `stale_bar_policy_status`;
- `missing_bar_policy_status`;
- `alignment_policy_status`;
- `market_row_access_status`;
- `block_reason`;
- `notes`.

## Allowed Readiness Status Values

Future rows must use one of:

```text
SESSION_ROLL_READY_STATIC_PROCESS_LOCKED
SESSION_ROLL_REQUIRES_REVIEW
SESSION_ROLL_BLOCKED_CONTRACT_IDENTITY
SESSION_ROLL_BLOCKED_NO_SESSION_EVIDENCE
SESSION_ROLL_BLOCKED_NO_ROLL_EVIDENCE
SESSION_ROLL_BLOCKED_NO_COMPLETED_BAR_POLICY
SESSION_ROLL_BLOCKED_NO_BACK_ADJUSTMENT_POLICY
SESSION_ROLL_BLOCKED_STALE_OR_MISSING_BAR_POLICY_UNRESOLVED
SESSION_ROLL_BLOCKED_ALIGNMENT_POLICY_UNRESOLVED
```

Default status for all rows before execution:

```text
SESSION_ROLL_REQUIRES_REVIEW
```

Rows with blocked contract identity must remain:

```text
SESSION_ROLL_BLOCKED_CONTRACT_IDENTITY
```

unless a separate contract identity gate resolves them first.

## Evidence Requirements

Acceptable evidence for a future execution gate:

- audited contract identity artifact;
- clean static provider instrument evidence;
- static provider session/trading-hours template evidence;
- static exchange trading calendar;
- static exchange holiday and early-close calendar;
- static provider roll-rule documentation;
- static exchange delivery cycle or last-trade/first-notice schedule;
- static back-adjustment policy document;
- manually reviewed source-native futures session/roll specification packet.

Forbidden as standalone authority:

- market rows;
- NinjaTrader historical export;
- chart display times;
- ad hoc timestamp observations;
- old QuantLab data-prep scripts;
- old CFD broker session assumptions;
- broker CFD symbol sessions;
- performance results;
- diagnostics;
- backtests;
- informal memory.

## Completed-Bar Policy Requirements

Future data work must use completed bars only.

A future readiness execution gate must define:

- what timestamp means for a daily bar;
- whether the timestamp is session date, close time, or file label;
- how completed status is verified before a bar is eligible;
- how holidays and early closes affect completed status;
- how stale bars are detected;
- how missing bars are detected;
- how mixed timezones are aligned.

No future artifact may treat a chart bar or provider export row as completed without an explicit completed-bar policy.

## Roll And Back-Adjustment Requirements

A future readiness execution gate must define:

- contract selection rule;
- roll trigger;
- roll date source;
- delivery cycle source;
- last trade or first notice handling when applicable;
- raw versus adjusted price fields;
- back-adjustment method;
- whether carry curve legs remain available after roll handling;
- how roll gaps are represented;
- how missing roll evidence blocks a row.

No roll or back-adjustment method may be inferred from old QuantLab scripts, old broker assumptions, or convenience defaults.

## Alignment Requirements

Future portfolio work must define alignment across all members before any real-data portfolio computation.

Required alignment atoms:

- common portfolio date index;
- instrument-local session date;
- completed-bar availability timestamp;
- timezone normalization;
- holiday and early close handling;
- stale bar treatment;
- missing bar treatment;
- fail-closed behavior when one member is missing.

No missing member may be dropped, substituted, or reweighted.

## Relationship To Contract Identity State

The current contract identity artifact has:

```text
CONTRACT_IDENTITY_LOCKED_SOURCE_NATIVE: 0
```

Therefore this draft does not claim any row is ready for session/roll execution.

The 41 review-required rows may only proceed to session/roll execution as review-required candidates. The 59 unavailable rows and 2 variant-blocked rows remain blocked.

## Relationship To Later Gates

Session/roll/completed-bar readiness must precede:

- risk, FX, cost, and carry-leg readiness;
- real-data Development/Reconciliation;
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

- the draft does not resolve sessions, rolls, completed bars, or back-adjustment;
- the draft accurately carries the contract identity status state;
- blocked contract identity rows remain blocked;
- completed bars are required before any data work;
- no market-row parsing, NinjaTrader export, provider API access, diagnostics, backtests, old QuantLab active-pipeline use, CFD adapter work, deployment, trading, promotion, Opus/GPT execution, remote operation, remote push, or GitHub action is opened.

Regular hostile audit results should be preserved automatically as separate process-only audit-result records.

## Next Proposed Authorization

```text
Operator authorizes one process-only Carver Appendix C session/roll/completed-bar
readiness execution gate using static session, roll, and completed-bar policy
evidence.

Scope:
Create a process/source readiness artifact for Appendix C session calendars,
completed-bar timestamp policy, roll rules, back-adjustment policy, stale/missing
bar policy, and alignment rules using only audited static evidence. Resolve or
fail-close each row before any market-row access.

Allowed:
Read-only inspection of current Carver process artifacts, audited static CSV
artifacts, and explicitly named static session/roll/calendar policy evidence,
plus creation of process/source documentation or a machine-readable readiness
artifact.

Forbidden:
No code edits, no tests, no real market data, no market-row parsing, no
NinjaTrader export, no provider API access unless separately specified as static
evidence access, no diagnostics, no backtests, no OOS, no Lockbox, no Forward,
no CFD adapters, no old QuantLab pipeline use, no tuning, no deployment, no
trading, no promotion, no Opus/GPT execution, no remote operations.
```

## Non-Authorization

This shape gate draft authorizes no code edits, no tests, no real market data, no market-row parsing, no NinjaTrader historical export, no provider API access, no diagnostics, no backtests, no returns, no PnL, no Sharpe, no drawdown, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old QuantLab pipeline use, no tuning, no deployment, no trading, no promotion, no session/roll/completed-bar execution, no risk/FX/cost/carry-leg readiness, no market data readiness claim, no Opus/GPT execution, no remote push, and no GitHub action.
