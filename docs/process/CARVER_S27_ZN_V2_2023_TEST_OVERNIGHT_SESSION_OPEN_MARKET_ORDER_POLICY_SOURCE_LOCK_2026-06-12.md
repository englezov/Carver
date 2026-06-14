# S27 V2 ZN 2023 TEST Overnight Session-Open Market-Order Policy Source Lock

Date: 2026-06-12

Status:

```text
PROCESS_ONLY_OVERNIGHT_SESSION_OPEN_MARKET_ORDER_POLICY_SOURCE_LOCK_FAIL_CLOSED_NOT_RESULT
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Scope

This record covers the authorized S27_V2 2023 TEST overnight/session-open
market-order policy source-lock gate after the row-304 policy decision.

Scope is limited to resolving or explicitly fail-closing the row-304 class
before any further TEST continuation:

- market-order-required rows;
- decision timestamp at a declared session end;
- fill candidate in the next declared session;
- valuation mark potentially separated by a weekend/session gap.

This record authorizes no implementation, no provider/API access, no downloads,
no new data, no broader TEST continuation, no VALIDATION, no OOS, no Lockbox,
no Forward, no result interpretation, no PnL evaluation beyond mechanical row
construction, no tuning, no adapter/deployment/trading/promotion, no Git action,
no GPT packet preparation, and no source-faithful evidence claim.

## Inputs Inspected

- `docs/process/CARVER_S27_ZN_V2_2023_TEST_ROW304_SESSION_EOD_POLICY_GATE_2026-06-12.md`
- `docs/process/CARVER_S27_ZN_V2_2023_TEST_ROW303_SESSION_EOD_MARKET_ORDER_POLICY_GATE_2026-06-12.md`
- `docs/process/CARVER_S27_ZN_V2_2023_TEST_ROW303_SESSION_END_MARKET_ORDER_IMPLEMENTATION_AND_LOCAL_AUDIT_2026-06-12.md`
- `docs/process/CARVER_S27_ZN_V2_MARKET_ORDER_POLICY_SOURCE_LOCK_AND_IMPLEMENTATION_PLAN_2026-06-12.md`
- `docs/process/CARVER_S27_ZN_V2_SOURCE_LOCK_IMPLEMENTATION_EXERCISE_2026-06-05.md`
- `docs/process/CARVER_S27_ZN_V2_GPT_REAUDIT_TARGET_POSITION_REMEDIATION_2026-06-06.md`
- `docs/researchops/s27_v2_local_replay_inputs/ZN/20260612_2023_test_declared_pack/hourly_decision_completed_bar.csv`
- `docs/researchops/s27_v2_local_replay_inputs/ZN/20260612_2023_test_declared_pack/hourly_fill_completed_bar.csv`
- `docs/researchops/s27_v2_local_replay_inputs/ZN/20260612_2023_test_declared_pack/valuation_mark_completed_bar.csv`
- `docs/researchops/s27_v2_local_replay_runs/ZN/20260612_2023_test_mechanical_artifact_run/fail_closed_ledger.csv`
- `docs/researchops/s27_v2_market_spread_evidence/ZN/20260612_2023_test_combined_market_order_tbbo_registry/combined_market_order_tbbo_registry.csv`

No fresh PDF extraction was performed. The active book/source authority for this
gate is the existing source-lock and execution-policy record trail.

## Row 304 Class Facts

The current row-304 blocker is:

```text
row_index = 304
raw_symbol = ZNH3
decision_timestamp_utc = 2023-01-20T21:00:00Z
starting_position_contracts = 7
desired_position_contracts = 9
position_change_contracts = 2
order_side = BUY
market_order_required = TRUE
market_order_reason = BOOK_REQUIRED_TARGET_POSITION_GAP_GREATER_THAN_ONE_CONTRACT
fill_candidate_timestamp_utc = 2023-01-20T22:00:00Z
valuation_mark_timestamp_utc = 2023-01-23T00:00:00Z
same_session = FALSE
fail_closed_reason = SECONDARY_FILLED_ORDER_ACROSS_UNRESOLVED_SESSION_EOD_GAP_NOT_RESULT
```

The session shape is:

```text
decision_session_id = UTC_ZN_2023_TEST_2023-01-19T22:00:00Z_2023-01-20T21:00:00Z
fill_candidate_session_id = UTC_ZN_2023_TEST_2023-01-20T22:00:00Z_2023-01-21T21:00:00Z
valuation_mark_session_id = UTC_ZN_2023_TEST_2023-01-22T22:00:00Z_2023-01-23T21:00:00Z
```

Combined TBBO evidence exists for row 304:

```text
selected_quote_ts_event = 2023-01-20T21:59:59.924187905Z
bid_px_00 = 115.046875
ask_px_00 = 115.0625
selected_executable_market_fill_price = 115.0625
selection_status = PASS_FRESH_NON_CROSSED_TBBO_QUOTE_SELECTED_NOT_RESULT
```

Therefore this gate is not blocked by missing bid/ask evidence. It is blocked
by unresolved overnight/session-open market-order policy and post-weekend
valuation handling.

## Source-Lock Assessment

Existing process/source-lock records support these high-level concepts:

- end-of-day transitions cancel remaining working limit orders;
- overnight/session-gap handling is a distinct policy surface;
- overnight-gap transitions may require market reset orders toward desired
  rounded position;
- EOD and overnight transitions require advanced session/trading-date facts;
- EOD transitions with pending market orders fail closed unless separately
  source-locked;
- unresolved session/EOD, roll, valuation, degraded-provider, and market-spread
  states must remain fail-closed.

Those records are not sufficient to source-lock the exact row-304 class as an
executable TEST rule. The unresolved points are:

- whether a decision at the exact declared session end is actionable at that
  timestamp or must be deferred;
- whether the next declared session-open completed hourly row may be used as
  the fill row for that decision;
- whether an overnight/weekend gap changes the market reset rule;
- whether the row should be treated as cancellation/no-fill, deferred decision,
  immediate next-session market reset, or strict fail-closed;
- whether the post-weekend valuation mark may be accepted under the current
  engineering valuation convention for this session-open class.

The row-303 exception is not precedent for row 304. Row 303 was bounded to a
same-symbol decision/fill pair inside the same declared session, with the fill
candidate exactly at session end and the valuation mark as the exact next
completed hourly row. Row 304 starts at session end, crosses into the next
declared session for fill, and reaches a later post-weekend valuation mark.

## Decision

Decision:

```text
ROW304_OVERNIGHT_SESSION_OPEN_MARKET_ORDER_POLICY_SOURCE_LOCK_INSUFFICIENT_FAIL_CLOSED_NOT_RESULT
```

The correct current behavior is to keep row 304 fail-closed. No code patch,
runner continuation, fill emission, cost emission, PnL emission, result
emission, or TEST continuation is authorized by this record.

## Next Exact Authorization

If the operator wants to proceed without fresh book-attached source evidence,
the next gate should be an explicit engineering-convention decision gate:

```text
Operator authorizes S27_V2 2023 TEST row-304 overnight/session-open engineering market-reset policy decision gate, after the overnight/session-open source-lock gate failed closed, limited to accepting or rejecting a clearly labeled local-only engineering convention for the row-304 class.

Scope is limited to row 304 / the row-304 class where a market-order-required decision occurs at declared session end, the fill candidate is the next declared session-open completed hourly row, and the valuation mark is the next available completed hourly row after a weekend/session gap. Codex may inspect current S27_V2 code/tests/process records, session calendar evidence, combined TBBO registry evidence, and local TEST artifacts to decide whether to accept a convention labeled SOURCE_NATIVE_ENGINEERING_SESSION_OPEN_MARKET_RESET_ASSUMPTION_NOT_BOOK_EXPLICIT, or keep the row fail-closed.

This gate may produce process/current-state records, focused tests only if needed, one local hostile audit, and the exact next implementation authorization if the engineering convention is accepted.

No provider/API access, downloads, new data, broader TEST continuation, VALIDATION, OOS, Lockbox, Forward, result interpretation, PnL evaluation beyond mechanical row construction, tuning, adapter/deployment/trading/promotion, Git actions, GPT packet preparation, or source-faithful evidence claim.

If the engineering convention is rejected or cannot be bounded tightly to row 304/session-open facts, Codex must keep row 304 fail-closed and ask the operator before any broader TEST continuation.
```

Alternative: attach/verify `Carver.pdf` and run a GPT 5.5 external source-lock
audit specifically on row-304 overnight/session-open market reset mechanics
before accepting any engineering convention.

## Current Status

```text
ROW304_REMAINS_FAIL_CLOSED_PENDING_OPERATOR_DECISION_ON_ENGINEERING_CONVENTION_OR_EXTERNAL_SOURCE_LOCK_NOT_RESULT
```

## Non-Authorization

This record authorizes no implementation, no TEST continuation, no provider/API
access, no downloads, no new data, no VALIDATION, no OOS, no Lockbox, no
Forward, no result interpretation, no PnL evaluation beyond mechanical row
construction, no tuning, no adapter work, no deployment, no trading, no
promotion, no Git actions, no GPT packet preparation, and no source-faithful
evidence claim.
