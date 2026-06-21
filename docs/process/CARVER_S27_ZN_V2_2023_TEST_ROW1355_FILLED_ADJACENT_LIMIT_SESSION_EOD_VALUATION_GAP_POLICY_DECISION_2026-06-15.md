# S27 V2 ZN 2023 TEST Row 1355 Filled Adjacent-Limit Session/EOD Valuation-Gap Policy Decision

Date: 2026-06-15

Status:

```text
ROW1355_FILLED_ADJACENT_LIMIT_SESSION_EOD_VALUATION_GAP_POLICY_DECIDED_PENDING_IMPLEMENTATION_NOT_RESULT
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Scope

This record covers the authorized local-only S27_V2 2023 TEST row-1355
filled adjacent-limit session/EOD valuation-gap policy decision gate.

The gate was limited to already-local 2023 TEST artifacts and audited S27_V2
machinery. It authorized no provider/API access, downloads, new data, broader
TEST continuation, VALIDATION, OOS, Lockbox, Forward, result interpretation,
PnL evaluation beyond mechanical construction, tuning, adapter/deployment/
trading/promotion, Git action, GPT packet preparation, or source-faithful
evidence claim.
## Inputs Inspected

- `src/carver/spine/s27_v2_replay/test_mechanical_run.py`
- `tests/test_s27_v2_2023_test_mechanical_run.py`
- `docs/researchops/s27_v2_local_replay_inputs/ZN/20260612_2023_test_declared_pack/hourly_decision_completed_bar.csv`
- `docs/researchops/s27_v2_local_replay_inputs/ZN/20260612_2023_test_declared_pack/hourly_fill_completed_bar.csv`
- `docs/researchops/s27_v2_local_replay_inputs/ZN/20260612_2023_test_declared_pack/valuation_mark_completed_bar.csv`
- `docs/researchops/s27_v2_local_replay_inputs/ZN/20260612_2023_test_declared_pack/session_calendar.csv`
- `docs/researchops/s27_v2_local_replay_inputs/ZN/20260612_2023_test_declared_pack/roll_calendar.csv`
- `docs/researchops/s27_v2_local_replay_runs/ZN/20260612_2023_test_mechanical_artifact_run/fail_closed_ledger.csv`
- `docs/process/CARVER_S27_ZN_V2_2023_TEST_ROW892_FILLED_ADJACENT_LIMIT_SESSION_EOD_POLICY_DECISION_2026-06-15.md`
- `docs/process/CARVER_S27_ZN_V2_2023_TEST_ROW892_SESSION_END_ADJACENT_LIMIT_IMPLEMENTATION_AND_LOCAL_AUDIT_2026-06-15.md`
- `docs/process/CARVER_S27_ZN_V2_2023_TEST_ROW1113_SESSION_END_MARKET_ORDER_VALUATION_GAP_POLICY_DECISION_2026-06-15.md`
- `docs/process/CARVER_S27_ZN_V2_2023_TEST_ROW1113_SESSION_END_MARKET_ORDER_VALUATION_GAP_IMPLEMENTATION_AND_LOCAL_AUDIT_2026-06-15.md`

No fresh PDF extraction was performed. The active source/process authority is
the existing S27_V2 source-lock and execution-policy record set.

## Row 1355 Facts

Current fail-closed row:

```text
row_index = 1355
raw_symbol = ZNM3
decision_timestamp_utc = 2023-03-29T20:00:00Z
starting_position_contracts = 7
desired_position_contracts = 8
position_change_contracts = 1
order_side = BUY
adjacent_target_position = 8
formula_limit_price = 114.49366645867451
limit_order_price = 114.484375
fill_candidate_timestamp_utc = 2023-03-29T21:00:00Z
fill_candidate_close = 114.46875
fill_executed = TRUE
same_session = FALSE
fail_closed_reason = SECONDARY_FILLED_ORDER_ACROSS_UNRESOLVED_SESSION_EOD_GAP_NOT_RESULT
row_hash = 80e097e1f326f2b0f860c1d0a806339b5e3889889488297ef22dd45bc96f05c5
```

The `same_session = FALSE` field in the current fail-closed row reflects the
older blocker logic comparing decision/fill/valuation as a triplet. The
declared source rows show decision and fill are in the same declared execution
session; the valuation mark is in the next declared session.

Declared source-row facts:

```text
decision:
  completed_timestamp_utc = 2023-03-29T20:00:00Z
  trading_date = 2023-03-29
  raw_symbol = ZNM3
  session_id = UTC_ZN_2023_TEST_2023-03-28T22:00:00Z_2023-03-29T21:00:00Z
  close_price = 114.515625
  source_row_hash = 8A0A69D496202FD89CD23B06A20C7A6BAC49386A57F3C6BC317D604307749ABA
  readiness_status = READY_COMPLETED_BAR_DATABENTO_2023_TEST

fill candidate:
  completed_timestamp_utc = 2023-03-29T21:00:00Z
  trading_date = 2023-03-29
  raw_symbol = ZNM3
  session_id = UTC_ZN_2023_TEST_2023-03-28T22:00:00Z_2023-03-29T21:00:00Z
  close_price = 114.46875
  source_row_hash = DF8396A2BF9115F9CA82B77D5FB04DD79E5A17F4C03CCAF724D18D947E4F7293
  readiness_status = READY_COMPLETED_BAR_DATABENTO_2023_TEST

valuation mark:
  completed_timestamp_utc = 2023-03-29T23:00:00Z
  trading_date = 2023-03-30
  raw_symbol = ZNM3
  session_id = UTC_ZN_2023_TEST_2023-03-29T22:00:00Z_2023-03-30T21:00:00Z
  close_price = 114.5
  source_row_hash = C66A52F44CC3BCB8368E336324C9B1DC165D32ACA56E89BF870C494698271645
  readiness_status = READY_COMPLETED_BAR_DATABENTO_2023_TEST_VALUATION_MARK
  valuation_convention_label = SOURCE_NATIVE_ENGINEERING_VALUATION_ASSUMPTION_NOT_BOOK_EXPLICIT
```

Session and roll facts:

```text
decision/fill same declared execution session = TRUE
fill candidate equals declared session end = TRUE
valuation mark belongs to next declared session = TRUE
immediate 2023-03-29T22:00:00Z same-symbol valuation row in declared pack = ABSENT
first same-symbol valuation mark after fill = 2023-03-29T23:00:00Z
roll transitions on decision/fill/valuation dates = NONE
```

## Policy Decision

Row 1355 is a filled `BUY 1` adjacent-limit row. It is not a market-order/TBBO
case and does not need market spread evidence.

The row-892 adjacent-limit precedent is close but does not directly cover row
1355. Row 892 requires the valuation mark to be the exact next completed
hourly row after the fill. Row 1355 does not satisfy that condition because
the immediate `2023-03-29T22:00:00Z` same-symbol valuation row is absent from
the declared valuation-mark row family and the selected mark is the first
available completed same-symbol row at `2023-03-29T23:00:00Z`.

The row-1113 valuation-gap precedent establishes the governance pattern for
this shape: when the immediate valuation mark is absent, the run may not
silently reuse an earlier session-end class. It must use a distinct bounded
local-only engineering convention and explicitly preserve the not-book-explicit
valuation label.

Therefore row 1355 may proceed only under the distinct bounded convention:

```text
SOURCE_NATIVE_ENGINEERING_SESSION_END_ADJACENT_LIMIT_FILL_WITH_NEXT_AVAILABLE_VALUATION_GAP_ASSUMPTION_NOT_BOOK_EXPLICIT
```

and fill rule:

```text
ONE_HOUR_CLOSE_ONLY_LIMIT_FILL_AT_DECLARED_SESSION_END_WITH_NEXT_AVAILABLE_VALUATION_GAP_ENGINEERING_CONVENTION_NOT_BOOK_EXPLICIT
```

This is not book-explicit Carver authority, not source-faithful evidence, not
result interpretation, and not a backtest/result claim. It is local-only
mechanical construction metadata for the exact row-1355 facts if implemented
under a separate authorization.

If any fact drifts, row 1355 must remain fail-closed.

## Required Implementation Conditions

A future implementation must require all of the following facts:

1. row index `1355`;
2. raw symbol `ZNM3`;
3. decision timestamp `2023-03-29T20:00:00Z`;
4. fill candidate timestamp `2023-03-29T21:00:00Z`;
5. valuation mark timestamp `2023-03-29T23:00:00Z`;
6. starting position `7`;
7. desired position `8`;
8. position change `BUY 1`;
9. adjacent target `8`;
10. formula limit `114.49366645867451`;
11. executable limit `114.484375`;
12. fill candidate close `114.46875`;
13. fill executes under the existing close-only BUY limit rule;
14. decision and fill candidate have the same declared execution session;
15. fill candidate timestamp equals the declared execution session end;
16. no immediate `2023-03-29T22:00:00Z` same-symbol valuation row exists in the declared valuation-mark row family;
17. valuation mark `2023-03-29T23:00:00Z` is the first available completed same-symbol valuation row after fill and belongs to the next declared session;
18. valuation label remains `SOURCE_NATIVE_ENGINEERING_VALUATION_ASSUMPTION_NOT_BOOK_EXPLICIT`;
19. no roll-boundary, raw-symbol drift, unresolved working-order carry, or degraded provider condition is present;
20. limit-fill commission-only cost treatment is preserved;
21. result/backtest/PnL-evaluation/source-faithful gates remain fail-closed.

## Inline Local Hostile Audit

Subagent audit was not used for this process-only policy gate because the
previous subagent attempt in this thread hit the Codex usage limit. An inline
local hostile audit checked the current code/process/artifact evidence.

Result:

```text
P0: none
P1: none
P2: none
P3: none blocking
```

Audit conclusions:

- row 1355 is not a missing-TBBO or market-order case;
- row 1355 is not covered by row 892 because row 892 binds an exact next-hour valuation mark;
- row 1355 is governance-compatible with row 1113 only if a distinct valuation-gap convention is used;
- declared source rows prove decision/fill same-symbol, same declared execution session, and fill at declared session end;
- declared valuation rows prove no immediate `2023-03-29T22:00:00Z` same-symbol valuation row and first available `2023-03-29T23:00:00Z` mark;
- no roll transition is present on decision/fill/valuation dates;
- no provider/API/download/new data/protected-window/Git/GPT/result/tuning/adapter/deployment/trading/promotion surface was used or authorized.

## Exact Next Authorization

```text
Operator authorizes S27_V2 2023 TEST row-1355 filled adjacent-limit session-end valuation-gap implementation gate, after the row-1355 policy decision gate, limited to already-local 2023 TEST artifacts and audited S27_V2 machinery.

This authorizes Codex to implement the bounded row-1355 policy only: bind the active TEST input pack/run artifacts; verify ZNM3 row 1355; verify decision 2023-03-29T20:00:00Z, starting position 7, desired position 8, BUY 1 adjacent-limit state; verify adjacent target 8, formula limit 114.49366645867451, executable limit 114.484375, fill candidate 2023-03-29T21:00:00Z, fill candidate close 114.46875, and close-only BUY limit fill execution; verify decision and fill candidate are same raw symbol, same declared execution session, and fill candidate is exactly the declared session end; verify no immediate 2023-03-29T22:00:00Z same-symbol completed valuation row exists in the declared valuation-mark row family; verify valuation mark 2023-03-29T23:00:00Z is the first available completed same-symbol valuation row after the fill and belongs to the next declared session; verify no roll boundary, raw-symbol drift, unresolved working-order carry, or degraded provider condition; emit deterministic local-only BUY 1 adjacent-limit order/fill/cost/mechanical-PnL metadata where evidence is sufficient; label the class SOURCE_NATIVE_ENGINEERING_SESSION_END_ADJACENT_LIMIT_FILL_WITH_NEXT_AVAILABLE_VALUATION_GAP_ASSUMPTION_NOT_BOOK_EXPLICIT and fill rule ONE_HOUR_CLOSE_ONLY_LIMIT_FILL_AT_DECLARED_SESSION_END_WITH_NEXT_AVAILABLE_VALUATION_GAP_ENGINEERING_CONVENTION_NOT_BOOK_EXPLICIT; preserve valuation label SOURCE_NATIVE_ENGINEERING_VALUATION_ASSUMPTION_NOT_BOOK_EXPLICIT; preserve result/backtest/source-faithful evidence fail-closed gates; continue only until the next genuine fail-closed blocker; run focused tests and one local hostile audit if available; and record process/current-state outputs.

No provider/API access, downloads, new data acquisition, broader TEST continuation beyond the next blocker, VALIDATION, OOS, Lockbox, Forward, result interpretation, PnL evaluation beyond mechanical construction, tuning, adapter/deployment/trading/promotion, Git actions, GPT packet preparation, or source-faithful evidence claim.

If row facts drift, if the 22:00 valuation-row absence cannot be proven from the declared pack, if the 23:00 mark is not the first available completed same-symbol valuation row after the fill, if roll/symbol/session/provider/working-state conditions drift, if not-book-explicit engineering labels are lost, if protected windows would be crossed, or if implementation requires provider/API/download/new data/Git/adapter/deployment/trading/promotion, Codex must fail closed and ask the operator.
```

## Current Status

```text
ROW1355_FILLED_ADJACENT_LIMIT_SESSION_EOD_VALUATION_GAP_POLICY_DECIDED_PENDING_IMPLEMENTATION_NOT_RESULT
```

The next step is the exact implementation gate above if the operator chooses
to proceed.

## Non-Authorization

This record authorizes no implementation, no TEST continuation, no provider/API
access, no downloads, no new data, no VALIDATION, no OOS, no Lockbox, no
Forward, no result interpretation, no PnL evaluation beyond mechanical
construction, no tuning, no adapter work, no deployment, no trading, no
promotion, no Git actions, no GPT packet preparation, and no source-faithful
evidence claim.
