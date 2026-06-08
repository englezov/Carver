# Carver S27 ZN V2 GPT Reaudit 54 Test Stop Rule Decision

Date: 2026-06-06

Status:

```text
PROCESS_ONLY_S27_V2_GPT_REAUDIT_STOP_RULE_DECISION_NOT_REPLAY_OR_BACKTEST_AUTHORIZATION
```

## Scope

This record classifies the GPT Extended Pro re-audit of the 54-test S27 V2 packet.

Authorized work remains process/local implementation review only. This record authorizes no provider/API use, no downloads, no parser/file replay, no diagnostics, no backtests, no OOS, no Lockbox, no Forward, no Git staging, no commit, and no push.

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Audit Classification

GPT confirmed:

- no remaining P0 in the intended bundled replay path;
- the adjacent-limit completeness remediation is real;
- direct fill now checks plan-bound raw symbol and session;
- no-context no-order states fail closed;
- stale overnight helper and nonzero roll behavior remain fail-closed;
- the attached synthetic suite reports 54 passing tests.

GPT's remaining P1 findings are now primarily provenance-boundary findings:

- fill/cost/PnL source-status gates are string-spoofable;
- canonical order-plan builder does not itself populate raw symbol/session provenance;
- `S27V2ForecastContext` remains a caller-constructible numeric context rather than a non-forgeable source-row artifact;
- public cost/PnL helpers can still be misused as close-to-close ledger builders if treated as source-faithful APIs.

## Stop Rule Decision

The repeated audit pattern has reached the expected cutoff:

```text
STOP_SYNTHETIC_PUBLIC_BOUNDARY_PATCH_LOOP
MOVE_TO_NON_FORGEABLE_REPLAY_PROVENANCE_DESIGN
```

Reason:

The remaining issues cannot be made genuinely source-faithful by adding more mutable status strings or ad hoc public-helper checks. They require a design change: future local-row replay must route through a single audited replay bundle with non-forgeable provenance objects, or the low-level helpers must be treated as private structural primitives rather than public source-faithful APIs.

## Remaining Design Gates

Before local-row replay implementation can proceed, design must explicitly decide:

- how source rows, forecast contexts, fills, costs, and PnL rows carry non-forgeable replay provenance;
- whether low-level helpers are made internal-only or require replay provenance tokens;
- how canonical order-plan rows bind raw symbol, session id, trading date, and source-row hashes;
- how ZN tick-size and limit-price rounding are source-locked;
- how persistent working-limit carry/modify behavior is represented;
- how next-session overnight target recomputation will work;
- how nonzero-position roll bridge behavior is source-locked or kept fail-closed;
- how Strategy 3 sigma provenance, level compatibility, spread units, session/roll calendars, and row hashes are proven.

## Current Evidence State

Latest synthetic verification state:

```text
python -m pytest tests\test_s27_v2_source_lock_synthetic.py -q
54 passed
```

Earlier records reporting 31, 36, 39, 44, or 50 tests are superseded for the current local slice.

## Non-Authorization

This decision does not authorize replay, parser work, diagnostics, backtests, OOS, Lockbox, Forward, tuning, alpha claims, promotion, deployment, trading, Git staging, commit, or push.
