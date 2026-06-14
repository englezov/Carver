# S27 V2 ZN 2023 TEST Row 304 Overnight Session-Open Engineering Market-Reset Policy Decision

Date: 2026-06-12

Status:

```text
PROCESS_ONLY_ROW304_ENGINEERING_SESSION_OPEN_MARKET_RESET_POLICY_ACCEPTED_NOT_IMPLEMENTATION_NOT_RESULT
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Scope

This record covers the authorized S27_V2 2023 TEST row-304 overnight/session-open
engineering market-reset policy decision gate after the source-lock gate failed
closed.

The gate is limited to accepting or rejecting a clearly labeled local-only
engineering convention for the row-304 class:

- market-order-required row;
- decision timestamp is the declared session end;
- fill candidate is the next declared session-open completed hourly row;
- valuation mark is the next available completed hourly row after a
  weekend/session gap.

This record authorizes no implementation, no provider/API access, no downloads,
no new data, no broader TEST continuation, no VALIDATION, no OOS, no Lockbox,
no Forward, no result interpretation, no PnL evaluation beyond mechanical row
construction, no tuning, no adapter/deployment/trading/promotion, no Git action,
no GPT packet preparation, and no source-faithful evidence claim.

## Inputs Inspected

- `docs/process/CARVER_S27_ZN_V2_2023_TEST_OVERNIGHT_SESSION_OPEN_MARKET_ORDER_POLICY_SOURCE_LOCK_2026-06-12.md`
- `docs/process/CARVER_S27_ZN_V2_2023_TEST_ROW304_SESSION_EOD_POLICY_GATE_2026-06-12.md`
- `docs/process/CARVER_S27_ZN_V2_2023_TEST_ROW303_SESSION_EOD_MARKET_ORDER_POLICY_GATE_2026-06-12.md`
- `docs/process/CARVER_S27_ZN_V2_SOURCE_LOCK_IMPLEMENTATION_EXERCISE_2026-06-05.md`
- `docs/process/CARVER_S27_ZN_V2_GPT_REAUDIT_PUBLIC_BOUNDARY_REMEDIATION_2026-06-06.md`
- `docs/process/CARVER_S27_ZN_V2_MARKET_ORDER_POLICY_SOURCE_LOCK_AND_IMPLEMENTATION_PLAN_2026-06-12.md`
- `docs/researchops/s27_v2_local_replay_inputs/ZN/20260612_2023_test_declared_pack/hourly_decision_completed_bar.csv`
- `docs/researchops/s27_v2_local_replay_inputs/ZN/20260612_2023_test_declared_pack/hourly_fill_completed_bar.csv`
- `docs/researchops/s27_v2_local_replay_inputs/ZN/20260612_2023_test_declared_pack/valuation_mark_completed_bar.csv`
- `docs/researchops/s27_v2_local_replay_runs/ZN/20260612_2023_test_mechanical_artifact_run/fail_closed_ledger.csv`
- `docs/researchops/s27_v2_market_spread_evidence/ZN/20260612_2023_test_combined_market_order_tbbo_registry/combined_market_order_tbbo_registry.csv`

No fresh PDF extraction was performed. The active source-lock result remains
that the row-304 class is not book-explicitly locked.

## Row 304 Facts

The bounded row facts are:

```text
row_index = 304
raw_symbol = ZNH3
decision_timestamp_utc = 2023-01-20T21:00:00Z
decision_session_id = UTC_ZN_2023_TEST_2023-01-19T22:00:00Z_2023-01-20T21:00:00Z
starting_position_contracts = 7
desired_position_contracts = 9
position_change_contracts = 2
order_side = BUY
market_order_required = TRUE
market_order_reason = BOOK_REQUIRED_TARGET_POSITION_GAP_GREATER_THAN_ONE_CONTRACT
fill_candidate_timestamp_utc = 2023-01-20T22:00:00Z
fill_candidate_session_id = UTC_ZN_2023_TEST_2023-01-20T22:00:00Z_2023-01-21T21:00:00Z
fill_candidate_close = 115.046875
valuation_mark_timestamp_utc = 2023-01-23T00:00:00Z
valuation_mark_session_id = UTC_ZN_2023_TEST_2023-01-22T22:00:00Z_2023-01-23T21:00:00Z
valuation_mark_close = 115.03125
valuation_convention_label = SOURCE_NATIVE_ENGINEERING_VALUATION_ASSUMPTION_NOT_BOOK_EXPLICIT
same_session = FALSE
```

Combined TBBO evidence for the row is already local and selected:

```text
selected_quote_ts_event = 2023-01-20T21:59:59.924187905Z
quote_age_seconds = 0.075813000000000005
bid_px_00 = 115.046875
ask_px_00 = 115.0625
selected_executable_market_fill_price = 115.0625
spread_points = 0.015625
selected_spread_row_hash = ae269be40a140d4784891ccd4b6f7b347304090343d2f36a1e5f835d809255c3
selection_status = PASS_FRESH_NON_CROSSED_TBBO_QUOTE_SELECTED_NOT_RESULT
```

## Source-Lock Boundary

The source-lock gate concluded:

```text
ROW304_OVERNIGHT_SESSION_OPEN_MARKET_ORDER_POLICY_SOURCE_LOCK_INSUFFICIENT_FAIL_CLOSED_NOT_RESULT
```

That conclusion is preserved. This engineering decision does not convert the
row-304 class into book-explicit or source-faithful authority.

The relevant tension is:

- source/process notes say overnight gaps can cancel working limits and use
  market reset orders toward desired rounded position;
- a later remediation says overnight reset must fail closed until a
  next-session recomputed desired-position primitive exists;
- row 304 currently uses the prior session-end desired-position artifact and
  does not recompute a next-session target from next-session source rows.

Therefore any accepted policy must be labeled as engineering-only and must not
claim book-native overnight reset authority.

## Decision

Decision:

```text
ROW304_ENGINEERING_SESSION_OPEN_MARKET_RESET_CONVENTION_ACCEPTED_PENDING_IMPLEMENTATION_NOT_RESULT
```

Accepted convention label:

```text
SOURCE_NATIVE_ENGINEERING_SESSION_OPEN_MARKET_RESET_ASSUMPTION_NOT_BOOK_EXPLICIT
```

The convention is accepted only as local-only TEST mechanical construction
metadata. It means:

1. A row whose decision timestamp equals a declared session end may carry the
   already-computed prior-session target position into a session-open market
   reset only when the case is explicitly bounded and audited.
2. The fill candidate must be the exact next completed hourly row and the start
   of the next declared session for the same raw symbol.
3. The row must have no roll boundary, no raw-symbol change, no unresolved
   working limit order carry, no degraded provider condition, and no missing
   TBBO evidence.
4. Market fill price must come from the side-specific selected executable TBBO
   quote already bound in the combined registry.
5. The valuation mark must be the next available completed hourly valuation row
   after the weekend/session gap and must retain the existing engineering
   valuation label.
6. Result, backtest, source-faithful evidence, tuning, deployment, promotion,
   and trading gates remain fail-closed.

If any condition above fails, row 304 and the class must remain fail-closed.

## Non-Claims

This decision is not:

- book-explicit Carver execution authority;
- source-faithful evidence;
- a result or backtest result;
- performance interpretation;
- authorization for broader TEST continuation beyond the next fail-closed
  blocker;
- authorization to use VALIDATION, OOS, Lockbox, or Forward;
- authorization to tune, deploy, trade, promote, push to GitHub, or prepare a
  GPT packet.

## Exact Next Authorization

```text
Operator authorizes S27_V2 2023 TEST row-304 overnight/session-open engineering market-reset implementation gate, after acceptance of the engineering convention, limited to already-local 2023 TEST artifacts and already-acquired TBBO evidence.

This authorizes Codex to implement the bounded row-304 policy only: bind the active TEST input pack/run artifacts; verify the ZNH3 row-304 full-gap BUY 2 market-order state; verify decision 2023-01-20T21:00:00Z is exactly the prior declared session end; verify fill candidate 2023-01-20T22:00:00Z is the exact next completed hourly row and next declared session-open row for the same raw symbol; verify no roll boundary, no raw-symbol change, no unresolved working limit carry, and no degraded provider condition; consume the combined TBBO registry row-304 BUY ask fill evidence at 115.0625; use the convention SOURCE_NATIVE_ENGINEERING_SESSION_OPEN_MARKET_RESET_ASSUMPTION_NOT_BOOK_EXPLICIT; verify valuation mark 2023-01-23T00:00:00Z is the next available completed hourly valuation row after the weekend/session gap and remains labeled SOURCE_NATIVE_ENGINEERING_VALUATION_ASSUMPTION_NOT_BOOK_EXPLICIT; emit deterministic local-only market-order/fill/cost/mechanical-PnL metadata where evidence is sufficient; preserve result/backtest/source-faithful evidence fail-closed gates; continue only until the next fail-closed blocker; run focused tests and one local hostile audit; and record process/current-state outputs.

No provider/API access, downloads, new data, broader TEST continuation beyond the next blocker, VALIDATION, OOS, Lockbox, Forward, result interpretation, PnL evaluation beyond mechanical row construction, tuning, adapter/deployment/trading/promotion, Git actions, GPT packet preparation, or source-faithful evidence claim.

If the row is not exactly the bounded row-304 session-open case, if TBBO/cost evidence is missing or degraded, if the valuation mark is not the next available completed hourly row after the weekend/session gap, if roll/symbol/session/provider conditions drift, if a next-session recomputed desired-position primitive becomes required, or if implementation requires provider/API/download/new data/protected-window access/Git/adapter/deployment/trading/promotion, Codex must fail closed and ask the operator.
```

## Current Status

```text
ROW304_ENGINEERING_SESSION_OPEN_MARKET_RESET_POLICY_ACCEPTED_PENDING_IMPLEMENTATION_NOT_RESULT
```

## Non-Authorization

This record authorizes no implementation, no TEST continuation, no provider/API
access, no downloads, no new data, no VALIDATION, no OOS, no Lockbox, no
Forward, no result interpretation, no PnL evaluation beyond mechanical row
construction, no tuning, no adapter work, no deployment, no trading, no
promotion, no Git actions, no GPT packet preparation, and no source-faithful
evidence claim.
