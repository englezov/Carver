# Carver S10 Carry Forecast-Block Extension Gate Draft Audit Prompt

Date: 2026-05-29

Status:

```text
PROCESS_ONLY_CARVER_S10_CARRY_FORECAST_BLOCK_GATE_DRAFT_AUDIT_PROMPT_NOT_AUDIT_AUTHORIZATION_NOT_IMPLEMENTATION
```

## Purpose

Preserve the ready-to-run authorization and task prompt for one regular hostile audit of the S10 carry forecast-block extension gate draft.

This file does not authorize the audit by itself. The operator must explicitly authorize the audit in the thread before a subagent or auditor is used.

## Authorization Prompt

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

## Auditor Task

After explicit operator authorization, ask the auditor to inspect:

```text
docs/process/CARVER_S10_CARRY_FORECAST_BLOCK_EXTENSION_GATE_DRAFT_2026-05-29.md
docs/process/CARVER_S10_M5_OPUS_47_SOURCE_FAITHFULNESS_AUDIT_RESULT_2026-05-29.md
docs/process/CARVER_STRATEGY_TEN_CARRY_CHAPTER_COMPLETION_TRACKER_2026-05-29.md
```

The auditor should verify:

- the S10 carry forecast-block extension draft does not authorize implementation;
- the draft correctly follows the Opus 4.7 S10/M5 pass;
- the Opus 4.7 low findings are converted into forward constraints;
- the draft uses existing M2 forecast-block primitives as the preferred implementation path;
- S10 implementation remains behind separate explicit operator authorization;
- S11, P06, P07, real data, diagnostics, backtests, OOS, Lockbox, Forward, CFD adapters, deployment, trading, promotion, remote operations, tuning, and old `QuantLab_v3` active-pipeline use remain closed;
- the chapter completion tracker accurately describes the current done and pending state.

## Required Output

The auditor should return findings ordered by severity.

If there are no blocking findings, the auditor should say:

```text
NO BLOCKING FINDINGS
AUDIT_DISPOSITION: PASS_PROCESS_ONLY_DRAFT_SCOPE
```

If blocked, the auditor should identify the blocking file, issue, why it matters, and required fix.

## Non-Authorization

This prompt file authorizes no file edits, no code tests, no real-data execution, no market-row parsing, no NinjaTrader export, no diagnostics, no backtests, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old workspace pipeline use, no tuning, no deployment, no trading, no promotion, no S10 implementation, no S11, no P06/P07 portfolio work, no hostile audit execution, no Opus execution, no remote push, and no GitHub action.
