# S27 V2 ZN 2023 TEST Row 304 Session EOD Policy Gate

Date: 2026-06-12

Status:

```text
PROCESS_ONLY_ROW304_SESSION_EOD_POLICY_DECISION_FAIL_CLOSED_NOT_IMPLEMENTATION_NOT_RESULT
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Scope

This record covers the authorized local-only S27_V2 2023 TEST row-304
session/EOD policy gate after local PASS on the bounded row-303 session-end
market-order implementation.

The gate is limited to already-local 2023 TEST artifacts and source/process
records. It authorizes no provider/API access, downloads, new data, broader
TEST continuation, VALIDATION, OOS, Lockbox, Forward, result interpretation,
PnL evaluation beyond mechanical row construction, tuning, adapter/deployment/
trading/promotion, Git action, GPT packet preparation, or source-faithful
evidence claim.

## Inputs Inspected

- `docs/process/CARVER_S27_ZN_V2_MARKET_ORDER_POLICY_SOURCE_LOCK_AND_IMPLEMENTATION_PLAN_2026-06-12.md`
- `docs/process/CARVER_S27_ZN_V2_GPT_REAUDIT_TARGET_POSITION_REMEDIATION_2026-06-06.md`
- `docs/process/CARVER_S27_ZN_V2_SOURCE_LOCK_IMPLEMENTATION_EXERCISE_2026-06-05.md`
- `docs/process/CARVER_S27_ZN_V2_2023_TEST_ROW303_SESSION_EOD_MARKET_ORDER_POLICY_GATE_2026-06-12.md`
- `docs/process/CARVER_S27_ZN_V2_2023_TEST_ROW303_SESSION_END_MARKET_ORDER_IMPLEMENTATION_AND_LOCAL_AUDIT_2026-06-12.md`
- `docs/researchops/s27_v2_local_replay_inputs/ZN/20260612_2023_test_declared_pack/hourly_decision_completed_bar.csv`
- `docs/researchops/s27_v2_local_replay_inputs/ZN/20260612_2023_test_declared_pack/hourly_fill_completed_bar.csv`
- `docs/researchops/s27_v2_local_replay_inputs/ZN/20260612_2023_test_declared_pack/valuation_mark_completed_bar.csv`
- `docs/researchops/s27_v2_local_replay_inputs/ZN/20260612_2023_test_declared_pack/session_calendar.csv`
- `docs/researchops/s27_v2_local_replay_runs/ZN/20260612_2023_test_mechanical_artifact_run/fail_closed_ledger.csv`
- `docs/researchops/s27_v2_market_spread_evidence/ZN/20260612_2023_test_combined_market_order_tbbo_registry/combined_market_order_tbbo_registry.csv`

No fresh PDF extraction was performed. The active book/source authority is the
existing source-lock and execution-policy process record.

## Row 304 Facts

Current fail-closed row:

```text
row_index = 304
raw_symbol = ZNH3
decision_timestamp_utc = 2023-01-20T21:00:00Z
starting_position_contracts = 7
desired_position_contracts = 9
position_change_contracts = 2
order_side = BUY
market_order_required = TRUE
market_order_rows_emitted = FALSE
market_order_reason = BOOK_REQUIRED_TARGET_POSITION_GAP_GREATER_THAN_ONE_CONTRACT
fill_candidate_timestamp_utc = 2023-01-20T22:00:00Z
fill_candidate_close = 115.046875
valuation_mark_timestamp_utc = 2023-01-23T00:00:00Z
same_session = FALSE
fail_closed_reason = SECONDARY_FILLED_ORDER_ACROSS_UNRESOLVED_SESSION_EOD_GAP_NOT_RESULT
```

Session facts:

```text
decision_session_id = UTC_ZN_2023_TEST_2023-01-19T22:00:00Z_2023-01-20T21:00:00Z
fill_candidate_session_id = UTC_ZN_2023_TEST_2023-01-20T22:00:00Z_2023-01-21T21:00:00Z
valuation_mark_session_id = UTC_ZN_2023_TEST_2023-01-22T22:00:00Z_2023-01-23T21:00:00Z
```

Row 304 is materially different from row 303:

- row 303 decision was before session end and the fill candidate was exactly at
  the same session end;
- row 304 decision is itself at the prior session end;
- row 304 fill candidate is the next session open/completed row;
- row 304 valuation mark skips to the next available completed hourly row after
  the weekend/session gap.

Combined TBBO evidence exists for row 304:

```text
selected_quote_ts_event = 2023-01-20T21:59:59.924187905Z
bid_px_00 = 115.046875
ask_px_00 = 115.0625
selected_executable_market_fill_price = 115.0625
selection_status = PASS_FRESH_NON_CROSSED_TBBO_QUOTE_SELECTED_NOT_RESULT
```

Therefore the blocker is not missing TBBO evidence. The blocker is the
unresolved session/EOD/overnight policy shape.

## Policy Decision

The row-303 exception must not be generalized to row 304.

Existing source/process records support:

- EOD cancellation/reset for remaining working limit orders;
- overnight/session-gap handling as a separate policy surface;
- fail-closed behavior when session/EOD or valuation policy is unresolved;
- EOD transitions with pending market orders fail closed unless separately
  source-locked.

They do not currently source-lock a TEST-safe rule that converts a decision at
the exact session close into a next-session market fill and a post-weekend
valuation mark. The row also crosses three distinct session ids across
decision, fill candidate, and valuation mark.

Decision:

```text
ROW304_REMAINS_FAIL_CLOSED_PENDING_EXPLICIT_OVERNIGHT_SESSION_OPEN_MARKET_POLICY_NOT_RESULT
```

No implementation change is authorized or required by this policy record. The
current fail-closed runner behavior is correct for row 304 under the available
source/process evidence.

## Next Exact Authorization

```text
Operator authorizes S27_V2 2023 TEST overnight/session-open market-order policy source-lock gate, after row-304 policy decision, limited to resolving the row-304 class before any further TEST continuation.

Scope is limited to source-locking or explicitly fail-closing the policy for market-order-required rows where the decision timestamp is at a declared session end, the fill candidate is in the next declared session, and the valuation mark may be separated by a weekend/session gap. Codex may inspect current S27_V2 code/tests/process records, existing Carver.pdf/source-lock execution notes, session calendar evidence, and local TEST artifacts to determine whether a source-native rule supports next-session market reset/fill, cancellation/no-fill, deferred decision handling, or strict fail-closed treatment. It may produce process/current-state records, focused tests only if needed, one local hostile audit, and the exact next implementation authorization if a bounded policy is source-locked.

No provider/API access, downloads, new data, broader TEST continuation, VALIDATION, OOS, Lockbox, Forward, result interpretation, PnL evaluation beyond mechanical row construction, tuning, adapter/deployment/trading/promotion, Git actions, GPT packet preparation, or source-faithful evidence claim.

If the source/process evidence cannot support a bounded row-304 class policy, Codex must keep row 304 fail-closed and ask the operator before any broader TEST continuation.
```

## Current Status

```text
ROW304_SESSION_EOD_POLICY_FAIL_CLOSED_PENDING_OVERNIGHT_SESSION_OPEN_SOURCE_LOCK_NOT_RESULT
```

The next useful gate is the overnight/session-open market-order policy
source-lock gate above.

## Non-Authorization

This record authorizes no implementation, no TEST continuation, no provider/API
access, no downloads, no new data, no VALIDATION, no OOS, no Lockbox, no
Forward, no result interpretation, no PnL evaluation, no tuning, no adapter
work, no deployment, no trading, no promotion, no Git actions, no GPT packet
preparation, and no source-faithful evidence claim.
