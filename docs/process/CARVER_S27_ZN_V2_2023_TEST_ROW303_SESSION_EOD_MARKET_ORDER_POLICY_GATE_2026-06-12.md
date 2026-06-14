# S27 V2 ZN 2023 TEST Row 303 Session EOD Market-Order Policy Gate

Date: 2026-06-12

Status:

```text
PROCESS_ONLY_ROW303_SESSION_EOD_MARKET_ORDER_POLICY_DECISION_NOT_IMPLEMENTATION_NOT_RESULT
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Scope

This record covers the authorized local-only S27_V2 2023 TEST row-303
session/EOD market-order policy gate after local PASS on the combined TBBO
registry and mechanical continuation to row 303.

The gate is limited to already-local 2023 TEST artifacts and source/process
records. It authorizes no provider/API access, downloads, new data, broader
TEST continuation beyond row-303 policy, VALIDATION, OOS, Lockbox, Forward,
result interpretation, PnL evaluation, tuning, adapter/deployment/trading,
promotion, Git action, GPT packet preparation, or source-faithful evidence
claim.

## Inputs Inspected

- `docs/process/CARVER_S27_ZN_V2_MARKET_ORDER_POLICY_SOURCE_LOCK_AND_IMPLEMENTATION_PLAN_2026-06-12.md`
- `docs/process/CARVER_S27_ZN_V2_GPT_EXTERNAL_AUDIT_REMEDIATION_2026-06-05.md`
- `docs/process/CARVER_S27_ZN_V2_GPT_REAUDIT_TARGET_POSITION_REMEDIATION_2026-06-06.md`
- `docs/process/CARVER_S27_ZN_V2_SOURCE_LOCK_IMPLEMENTATION_EXERCISE_2026-06-05.md`
- `docs/process/CARVER_S27_ZN_V2_2023_TEST_COMBINED_TBBO_REGISTRY_AND_CONTINUATION_IMPLEMENTATION_AND_LOCAL_AUDIT_2026-06-12.md`
- `src/carver/spine/s27_v2_replay/test_mechanical_run.py`
- `src/carver/spine/s27_v2_replay/pretest_machine_freeze.py`
- `docs/researchops/s27_v2_local_replay_inputs/ZN/20260612_2023_test_declared_pack/hourly_decision_completed_bar.csv`
- `docs/researchops/s27_v2_local_replay_inputs/ZN/20260612_2023_test_declared_pack/hourly_fill_completed_bar.csv`
- `docs/researchops/s27_v2_local_replay_inputs/ZN/20260612_2023_test_declared_pack/valuation_mark_completed_bar.csv`
- `docs/researchops/s27_v2_local_replay_inputs/ZN/20260612_2023_test_declared_pack/session_calendar.csv`
- `docs/researchops/s27_v2_local_replay_runs/ZN/20260612_2023_test_mechanical_artifact_run/fail_closed_ledger.csv`

No fresh PDF extraction was performed. The active book/source authority is the
existing source-lock and execution-policy process record.

## Row 303 Facts

Current fail-closed row:

```text
row_index = 303
raw_symbol = ZNH3
decision_timestamp_utc = 2023-01-20T20:00:00Z
starting_position_contracts = 5
desired_position_contracts = 7
position_change_contracts = 2
order_side = BUY
market_order_required = TRUE
market_order_rows_emitted = FALSE
market_order_reason = BOOK_REQUIRED_TARGET_POSITION_GAP_GREATER_THAN_ONE_CONTRACT
fill_candidate_timestamp_utc = 2023-01-20T21:00:00Z
fill_candidate_close = 115.015625
valuation_mark_timestamp_utc = 2023-01-20T22:00:00Z
same_session = FALSE
fail_closed_reason = SECONDARY_FILLED_ORDER_ACROSS_UNRESOLVED_SESSION_EOD_GAP_NOT_RESULT
```

Session facts:

```text
decision_session_id = UTC_ZN_2023_TEST_2023-01-19T22:00:00Z_2023-01-20T21:00:00Z
fill_candidate_session_id = UTC_ZN_2023_TEST_2023-01-19T22:00:00Z_2023-01-20T21:00:00Z
valuation_mark_session_id = UTC_ZN_2023_TEST_2023-01-20T22:00:00Z_2023-01-21T21:00:00Z
```

The decision and fill-candidate rows are in the same declared session. The fill
candidate is exactly the completed bar at that session close. The valuation mark
row is the next completed hourly row after the fill and belongs to the next
declared session.

## Policy Decision

Row 303 is not an adjacent-limit working-order case. It is a full-gap
market-order case because the desired position moves from `5` to `7`, so
`abs(position_change_contracts) > 1`.

The existing source-lock and process records support:

- full-gap market-order handling where the target-position gap is greater than
  one contract;
- one-hour-lag market-order fill decision using the exact next completed hourly
  row;
- EOD cancellation/reset for remaining working limit orders;
- overnight/session-gap handling as a separate policy surface;
- fail-closed behavior when session/EOD or valuation policy is unresolved.

They do not support inventing a cancellation/no-fill result for a full-gap
market order merely because the valuation mark is in the next session. They
also do not support silently treating this as an ordinary same-session row,
because the valuation mark crosses the declared session boundary.

Therefore the policy decision is:

```text
ROW303_SESSION_END_MARKET_FILL_ALLOWED_WITH_NEXT_SESSION_ENGINEERING_VALUATION_PENDING_IMPLEMENTATION_NOT_RESULT
```

Under a separately authorized implementation gate, row 303 may emit
market-order, fill, cost, and mechanical PnL metadata only if all of the
following hold:

1. The row is a full-gap market-order case with
   `abs(position_change_contracts) > 1`.
2. The market-order side matches the signed position change.
3. The decision row and fill-candidate row have the same raw symbol and same
   declared session id.
4. The fill-candidate timestamp equals the declared session end timestamp.
5. The fill candidate is the exact next completed hourly row after the decision.
6. No unresolved working limit order is carried into the row.
7. No roll boundary or raw-symbol change is present.
8. Market-order TBBO/cost evidence is bound by the combined registry or another
   separately authorized local evidence record.
9. The valuation mark is the exact next completed hourly row after the fill,
   with the already accepted valuation label:

```text
SOURCE_NATIVE_ENGINEERING_VALUATION_ASSUMPTION_NOT_BOOK_EXPLICIT
```

This is a local-only Development/TEST mechanical construction convention. It
is not book-explicit, not result interpretation, not PnL evaluation beyond
mechanical row construction, and not a source-faithful evidence claim.

If any condition above fails, the runner must keep row 303 fail-closed. The
policy does not authorize broader session/EOD behavior, next-session deferred
fills, EOD market resets, working-order carry, roll-boundary execution, or
result/backtest emission.

## Exact Next Authorization

```text
Operator authorizes S27_V2 2023 TEST row-303 session-end market-order implementation gate, after the row-303 session/EOD market-order policy decision gate, limited to already-local 2023 TEST artifacts and already-acquired TBBO evidence.

This authorizes Codex to implement the row-303 bounded policy only: bind the active TEST input pack/run artifacts, verify the ZNH3 row-303 full-gap BUY 2 market-order state, verify decision 2023-01-20T20:00:00Z and fill candidate 2023-01-20T21:00:00Z are same-symbol/same-session with the fill candidate exactly at session end, verify valuation mark 2023-01-20T22:00:00Z is the exact next completed hourly row after the fill and label it SOURCE_NATIVE_ENGINEERING_VALUATION_ASSUMPTION_NOT_BOOK_EXPLICIT, consume the combined TBBO registry for row-303 market cost evidence, emit deterministic local-only market-order/fill/cost/mechanical-PnL metadata where evidence is sufficient, preserve result/backtest/source-faithful evidence fail-closed gates, continue only until the next fail-closed blocker, run focused tests and one local hostile audit, and record process/current-state outputs.

No provider/API access, downloads, new data, broader TEST continuation beyond the next blocker, VALIDATION, OOS, Lockbox, Forward, result interpretation, PnL evaluation beyond mechanical row construction, tuning, adapter/deployment/trading/promotion, Git actions, GPT packet preparation, or source-faithful evidence claim.

If the row is not exactly the bounded row-303 session-end case, if TBBO/cost evidence is missing or degraded, if the valuation mark is not the exact next completed hourly row, if a roll/symbol/session condition drifts, or if implementation requires provider/API/download/new data/protected-window access/Git/adapter/deployment/trading/promotion, Codex must fail closed and ask the operator.
```

## Current Status

```text
ROW303_SESSION_END_MARKET_FILL_POLICY_DECIDED_PENDING_IMPLEMENTATION_NOT_RESULT
```

The next step is the exact implementation gate above, if the operator chooses
to proceed.

## Non-Authorization

This record authorizes no implementation, no TEST rerun, no provider/API
access, no downloads, no new data, no VALIDATION, no OOS, no Lockbox, no
Forward, no result interpretation, no PnL evaluation, no tuning, no adapter
work, no deployment, no trading, no promotion, no Git actions, no GPT packet
preparation, and no source-faithful evidence claim.
