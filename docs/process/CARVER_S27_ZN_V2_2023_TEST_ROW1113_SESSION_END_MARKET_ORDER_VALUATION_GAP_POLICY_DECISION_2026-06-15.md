# S27 V2 ZN 2023 TEST Row 1113 Session-End Market-Order Valuation-Gap Policy Decision

Date: 2026-06-15

Status:

```text
ROW1113_SESSION_END_MARKET_ORDER_VALUATION_GAP_POLICY_DECIDED_PENDING_IMPLEMENTATION_NOT_RESULT
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Scope

This record covers the authorized local-only S27_V2 2023 TEST row-1113
session-end market-order valuation-gap policy decision gate.

The gate was limited to already-local 2023 TEST artifacts and audited S27_V2
machinery. It authorized no provider/API access, downloads, new data, broader
TEST continuation, VALIDATION, OOS, Lockbox, Forward, result interpretation,
PnL evaluation beyond mechanical construction, tuning, adapter/deployment/
trading/promotion, Git action, GPT packet preparation, or source-faithful
evidence claim.

## Inputs Inspected

- `docs/researchops/s27_v2_local_replay_inputs/ZN/20260612_2023_test_declared_pack/hourly_decision_completed_bar.csv`
- `docs/researchops/s27_v2_local_replay_inputs/ZN/20260612_2023_test_declared_pack/hourly_fill_completed_bar.csv`
- `docs/researchops/s27_v2_local_replay_inputs/ZN/20260612_2023_test_declared_pack/valuation_mark_completed_bar.csv`
- `docs/researchops/s27_v2_local_replay_inputs/ZN/20260612_2023_test_declared_pack/session_calendar.csv`
- `docs/researchops/s27_v2_local_replay_inputs/ZN/20260612_2023_test_declared_pack/roll_calendar.csv`
- `docs/researchops/s27_v2_local_replay_runs/ZN/20260612_2023_test_mechanical_artifact_run/fail_closed_ledger.csv`
- `docs/researchops/s27_v2_market_spread_evidence/ZN/20260612_2023_test_market_order_tbbo_requirements_discovery/market_order_tbbo_requirements.csv`
- `docs/researchops/s27_v2_market_spread_evidence/ZN/20260612_2023_test_combined_market_order_tbbo_registry/combined_market_order_tbbo_registry.csv`
- `docs/process/CARVER_S27_ZN_V2_2023_TEST_ROW303_SESSION_EOD_MARKET_ORDER_POLICY_GATE_2026-06-12.md`
- `docs/process/CARVER_S27_ZN_V2_2023_TEST_ROW391_SESSION_END_MARKET_ORDER_IMPLEMENTATION_AND_LOCAL_AUDIT_2026-06-13.md`
- `docs/process/CARVER_S27_ZN_V2_2023_TEST_ROW892_FILLED_ADJACENT_LIMIT_SESSION_EOD_POLICY_DECISION_2026-06-15.md`
- `src/carver/spine/s27_v2_replay/test_mechanical_run.py`

No fresh PDF extraction was performed. The active source/process authority is
the existing S27_V2 source-lock and execution-policy record set.

## Row 1113 Facts

Current fail-closed row:

```text
row_index = 1113
raw_symbol = ZNM3
decision_timestamp_utc = 2023-03-14T20:00:00Z
starting_position_contracts = -17
desired_position_contracts = -15
position_change_contracts = 2
order_side = BUY
market_order_required = TRUE
market_order_rows_emitted = FALSE
market_order_reason = BOOK_REQUIRED_TARGET_POSITION_GAP_GREATER_THAN_ONE_CONTRACT
fill_candidate_timestamp_utc = 2023-03-14T21:00:00Z
fill_candidate_close = 113.46875
market_fill_price_provenance = FAIL_CLOSED_MARKET_ORDER_ACROSS_UNRESOLVED_SESSION_EOD_GAP
secondary_fail_closed_reason = SECONDARY_FILLED_ORDER_ACROSS_UNRESOLVED_SESSION_EOD_GAP_NOT_RESULT
row_status = LOCAL_2023_TEST_MARKET_ORDER_SESSION_EOD_FAIL_CLOSED_NOT_RESULT
```

Declared source-row facts:

```text
decision row hash = 8167C5179B756116C7A6D9963603CB5423EC067A9FA1E97F074A81B4CF283D4C
fill row hash = 88788DABC4B85CEED4978940B2C539DAA1C2B882EE5BBC9DF45C2A62E790465C
valuation mark row hash = 641E4852FB8C1A9844D1ED5206CDC69FF245D9351A4E20B75194D641BD9096F8
```

Session facts:

```text
decision_session_id = UTC_ZN_2023_TEST_2023-03-13T22:00:00Z_2023-03-14T21:00:00Z
fill_candidate_session_id = UTC_ZN_2023_TEST_2023-03-13T22:00:00Z_2023-03-14T21:00:00Z
valuation_mark_session_id = UTC_ZN_2023_TEST_2023-03-14T22:00:00Z_2023-03-15T21:00:00Z
decision/fill same declared execution session = TRUE
fill candidate equals declared session end = TRUE
valuation mark timestamp = 2023-03-14T23:00:00Z
immediate 2023-03-14T22:00:00Z valuation row in declared pack = ABSENT
```

The row is not a missing-spread blocker. Row 1113 has already-bound fresh
TBBO evidence:

```text
source_evidence_type = STANDING_BATCH_AT_OR_BEFORE_FILL_TBBO
selected_quote_ts_event = 2023-03-14T20:59:59.840382723Z
quote_age_seconds = 0.15961800000000001
bid_px_00 = 113.453125
ask_px_00 = 113.46875
selected BUY executable ask = 113.46875
selection_status = PASS_FRESH_NON_CROSSED_TBBO_QUOTE_SELECTED_NOT_RESULT
```

## Policy Decision

Row 1113 is a full-gap market-order row because the desired position moves
from `-17` to `-15`, so `abs(position_change_contracts) > 1`.

Prior bounded session-end market-order precedents, including rows 303 and 391,
only authorize a market fill at declared session end when the valuation mark is
the exact next completed hourly row after the fill. Row 1113 does not satisfy
that prior condition because the immediate `2023-03-14T22:00:00Z` valuation
row is absent from the declared local pack and the selected valuation mark is
the next available completed same-symbol row at `2023-03-14T23:00:00Z`.

Therefore row 1113 may not be treated as ordinary same-session execution or as
the already accepted row-303/row-391 class. It also should not be forced into
a no-fill/cancellation result, because the market-order fill candidate is
present, same-symbol, in the same declared execution session, and exactly at
the declared session end with fresh side-specific TBBO evidence.

The policy decision is to allow implementation only under a distinct bounded
local-only engineering convention:

```text
SOURCE_NATIVE_ENGINEERING_SESSION_END_MARKET_ORDER_FILL_WITH_NEXT_AVAILABLE_VALUATION_GAP_ASSUMPTION_NOT_BOOK_EXPLICIT
```

This convention is not book-explicit authority, not source-faithful evidence,
not result interpretation, and not a backtest/result claim. It exists only to
permit local-only mechanical construction for the exact row-1113 valuation-gap
facts after fail-closed verification.

Under a separately authorized implementation gate, row 1113 may emit
market-order, fill, cost, and mechanical PnL metadata only if all of the
following hold:

1. The row is exactly row `1113`, `ZNM3`, decision `2023-03-14T20:00:00Z`.
2. Starting position is `-17`, desired position is `-15`, and signed position
   change is `BUY 2`.
3. Decision and fill rows are same-symbol and same declared execution session.
4. Fill candidate timestamp is exactly `2023-03-14T21:00:00Z` and equals the
   declared session end.
5. No immediate `2023-03-14T22:00:00Z` valuation row exists in the declared
   valuation-mark row family.
6. Valuation mark `2023-03-14T23:00:00Z` is the first available completed
   same-symbol valuation row after the fill and belongs to the next declared
   session.
7. Valuation label remains
   `SOURCE_NATIVE_ENGINEERING_VALUATION_ASSUMPTION_NOT_BOOK_EXPLICIT`.
8. No roll-boundary, raw-symbol drift, unresolved working-order carry, or
   degraded provider condition is present.
9. Row-1113 TBBO evidence is already bound, fresh, non-crossed, at-or-before
   fill, and side-specific to the BUY ask.
10. Bid/ask spread is not double-counted when the selected ask is used as the
    market fill price.
11. Result, backtest, PnL-evaluation, and source-faithful evidence gates remain
    fail-closed.

If any condition fails, row 1113 must remain fail-closed.

## Local Hostile Audit

One read-only local hostile-audit subagent returned:

```text
PASS_NO_P0_P1_P2
```

The audit confirmed:

- row-1113 TBBO evidence is bound, fresh, non-crossed, and side-specific to
  the BUY ask;
- decision `2023-03-14T20:00:00Z` and fill candidate
  `2023-03-14T21:00:00Z` are same-symbol and same declared execution session;
- fill candidate `2023-03-14T21:00:00Z` is exactly the declared session end;
- next declared session starts at `2023-03-14T22:00:00Z`;
- declared valuation mark for row 1113 is `2023-03-14T23:00:00Z`, with no
  row-1113 `2023-03-14T22:00:00Z` valuation mark present;
- row-303/row-391 precedents do not cover this case because they require the
  valuation mark to be the exact next completed hourly row after fill;
- row-892 supports using a distinct bounded local-only convention rather than
  silently reusing a nearby class when the session-end valuation shape changes;
- forbidden result/backtest/source-faithful, protected-window, provider/API,
  download, Git, tuning, adapter/deployment/trading/promotion surfaces remain
  closed.

## Exact Next Authorization

```text
Operator authorizes S27_V2 2023 TEST row-1113 session-end market-order valuation-gap implementation gate, after the row-1113 policy decision gate, limited to already-local 2023 TEST artifacts, audited S27_V2 machinery, and already-bound TBBO evidence.

This authorizes Codex to implement the bounded row-1113 policy only: bind the active TEST input pack/run artifacts; verify ZNM3 row 1113; verify decision 2023-03-14T20:00:00Z, starting position -17, desired position -15, BUY 2 full-gap market-order state; verify fill candidate 2023-03-14T21:00:00Z is the exact next completed hourly row, same raw symbol, same declared execution session, and exactly the declared session end; verify no immediate 2023-03-14T22:00:00Z completed valuation row exists in the declared valuation-mark row family; verify valuation mark 2023-03-14T23:00:00Z is the first available completed same-symbol valuation row after the fill and belongs to the next declared session; verify no roll boundary, raw-symbol drift, unresolved working-order carry, or degraded provider condition; consume already-bound row-1113 BUY ask TBBO evidence at selected quote 2023-03-14T20:59:59.840382723Z with ask 113.46875; emit deterministic local-only BUY 2 market-order/fill/cost/mechanical-PnL metadata where evidence is sufficient; label the class SOURCE_NATIVE_ENGINEERING_SESSION_END_MARKET_ORDER_FILL_WITH_NEXT_AVAILABLE_VALUATION_GAP_ASSUMPTION_NOT_BOOK_EXPLICIT and preserve valuation label SOURCE_NATIVE_ENGINEERING_VALUATION_ASSUMPTION_NOT_BOOK_EXPLICIT; preserve result/backtest/source-faithful evidence fail-closed gates; continue only until the next genuine fail-closed blocker; run focused tests and one local hostile audit; and record process/current-state outputs.

No provider/API access, downloads, new data acquisition, broader TEST continuation beyond the next blocker, VALIDATION, OOS, Lockbox, Forward, result interpretation, PnL evaluation beyond mechanical construction, tuning, adapter/deployment/trading/promotion, Git actions, GPT packet preparation, or source-faithful evidence claim.

If row facts drift, if the 22:00 valuation-row absence cannot be proven from the declared pack, if the 23:00 mark is not the first available completed same-symbol valuation row after the fill, if TBBO/cost evidence is missing or degraded, if the not-book-explicit engineering labels are lost, if protected windows would be crossed, or if implementation requires provider/API/download/new data/Git/adapter/deployment/trading/promotion, Codex must fail closed and ask the operator.
```

## Current Status

```text
ROW1113_SESSION_END_MARKET_ORDER_VALUATION_GAP_POLICY_DECIDED_PENDING_IMPLEMENTATION_NOT_RESULT
```

The next step is the exact implementation gate above, if the operator chooses
to proceed.

## Non-Authorization

This record authorizes no implementation, no TEST continuation, no provider/API
access, no downloads, no new data, no VALIDATION, no OOS, no Lockbox, no
Forward, no result interpretation, no PnL evaluation beyond mechanical
construction, no tuning, no adapter work, no deployment, no trading, no
promotion, no Git actions, no GPT packet preparation, and no source-faithful
evidence claim.
