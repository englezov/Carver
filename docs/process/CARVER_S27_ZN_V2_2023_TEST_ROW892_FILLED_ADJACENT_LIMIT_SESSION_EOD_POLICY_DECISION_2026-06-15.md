# S27 V2 2023 TEST Row 892 Filled Adjacent-Limit Session/EOD Policy Decision

Date: 2026-06-15

Status:

```text
ROW892_FILLED_ADJACENT_LIMIT_SESSION_EOD_POLICY_DECIDED_PENDING_IMPLEMENTATION_NOT_RESULT
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Scope

Operator authorized a process-only S27_V2 2023 TEST row-892 filled adjacent-limit session/EOD policy decision gate after local PASS on the row-701 roll-boundary no-new-order suppression implementation and continuation to row `892`.

Scope was limited to already-local 2023 TEST artifacts and audited S27_V2 machinery. This gate authorized no provider/API access, downloads, new data acquisition, broader TEST continuation, VALIDATION, OOS, Lockbox, Forward, result interpretation, PnL evaluation beyond mechanical construction, tuning, adapter/deployment/trading/promotion, Git actions, GPT packet preparation, or source-faithful evidence claim.

## Inputs Inspected

```text
docs/process/CARVER_S27_ZN_V2_2023_TEST_ROW436_SESSION_OPEN_ADJACENT_LIMIT_IMPLEMENTATION_AND_LOCAL_AUDIT_2026-06-13.md
docs/process/CARVER_S27_ZN_V2_2023_TEST_ROW391_SESSION_END_MARKET_ORDER_IMPLEMENTATION_AND_LOCAL_AUDIT_2026-06-13.md
docs/process/CARVER_S27_ZN_V2_2023_TEST_ROW303_SESSION_EOD_MARKET_ORDER_POLICY_GATE_2026-06-12.md
docs/process/CARVER_S27_ZN_V2_2023_TEST_ROW701_ROLL_BOUNDARY_SUPPRESSION_IMPLEMENTATION_AND_CONTINUATION_LOCAL_AUDIT_2026-06-14.md
src/carver/spine/s27_v2_replay/test_mechanical_run.py
docs/researchops/s27_v2_local_replay_inputs/ZN/20260612_2023_test_declared_pack/hourly_decision_completed_bar.csv
docs/researchops/s27_v2_local_replay_inputs/ZN/20260612_2023_test_declared_pack/hourly_fill_completed_bar.csv
docs/researchops/s27_v2_local_replay_inputs/ZN/20260612_2023_test_declared_pack/valuation_mark_completed_bar.csv
docs/researchops/s27_v2_local_replay_inputs/ZN/20260612_2023_test_declared_pack/session_calendar.csv
docs/researchops/s27_v2_local_replay_inputs/ZN/20260612_2023_test_declared_pack/roll_calendar.csv
docs/researchops/s27_v2_local_replay_runs/ZN/20260612_2023_test_mechanical_artifact_run/fail_closed_ledger.csv
```

No fresh PDF extraction was performed. No provider/API access was used.

## Row 892 Facts

Fail-closed row:

```text
row_index: 892
raw_symbol: ZNM3
decision_timestamp_utc: 2023-02-28T20:00:00Z
starting_position_contracts: 0
desired_position_contracts: -1
position_change_contracts: -1
order_side: SELL
adjacent_target_position: -1
formula_limit_price: 111.6707138465356
limit_order_price: 111.671875
fill_candidate_timestamp_utc: 2023-02-28T21:00:00Z
fill_candidate_close: 111.671875
fill_executed: TRUE
same_session: FALSE
fail_closed_reason: SECONDARY_FILLED_ORDER_ACROSS_UNRESOLVED_SESSION_EOD_GAP_NOT_RESULT
source_faithful_evidence_claimed: FALSE
```

Important clarification:

```text
The fail_closed_ledger.csv same_session field is FALSE because the current adjacent-limit blocker logic compares decision, fill, and valuation sessions together.

For row 892, decision and fill candidate are in the same declared execution session. The valuation mark is the exact next completed hourly row in the next declared session.
```

Declared source rows:

```text
decision:
  completed_timestamp_utc: 2023-02-28T20:00:00Z
  trading_date: 2023-02-28
  raw_symbol: ZNM3
  session_id: UTC_ZN_2023_TEST_2023-02-27T22:00:00Z_2023-02-28T21:00:00Z
  readiness_status: READY_COMPLETED_BAR_DATABENTO_2023_TEST
  close_price: 111.671875
  source_row_hash: 74D7B81AD25FC523A5724A00CFE3EF755D095760B868173CED1C0F901FDDE838

fill candidate:
  completed_timestamp_utc: 2023-02-28T21:00:00Z
  trading_date: 2023-02-28
  raw_symbol: ZNM3
  session_id: UTC_ZN_2023_TEST_2023-02-27T22:00:00Z_2023-02-28T21:00:00Z
  readiness_status: READY_COMPLETED_BAR_DATABENTO_2023_TEST
  close_price: 111.671875
  source_row_hash: 84A635A885E8CD16243380DC2DC3C60EE3E5081E955AF22D7F61F111B1606537

valuation mark:
  completed_timestamp_utc: 2023-02-28T22:00:00Z
  trading_date: 2023-02-28
  raw_symbol: ZNM3
  session_id: UTC_ZN_2023_TEST_2023-02-28T22:00:00Z_2023-03-01T21:00:00Z
  readiness_status: READY_COMPLETED_BAR_DATABENTO_2023_TEST_VALUATION_MARK
  close_price: 111.546875
  source_row_hash: 5CEF6C5AFC343C89C7B11EF12DC3EAD130C719F84ECEB11D46084FB265239319
  valuation_convention_label: SOURCE_NATIVE_ENGINEERING_VALUATION_ASSUMPTION_NOT_BOOK_EXPLICIT
```

Session calendar evidence:

```text
execution_session_id: UTC_ZN_2023_TEST_2023-02-27T22:00:00Z_2023-02-28T21:00:00Z
execution_session_start_utc: 2023-02-27T22:00:00Z
execution_session_end_utc: 2023-02-28T21:00:00Z
next_session_id: UTC_ZN_2023_TEST_2023-02-28T22:00:00Z_2023-03-01T21:00:00Z
next_session_start_utc: 2023-02-28T22:00:00Z
```

Roll calendar evidence:

```text
No declared roll transition is present on 2023-02-28.
The February declared roll transition is 2023-02-16.
```

Relevant file hashes:

```text
hourly_decision_completed_bar.csv: 8389e712fe8575188069d6cc43a0f8273dd838f74eed0f9c621bdb20fb81dd9a
hourly_fill_completed_bar.csv: d75ecd49bfb29b94426e4e05a46886e915d5bfdf7385707dc4e165b8ea53a662
valuation_mark_completed_bar.csv: 749d676e107f88de208961f463e0e2bf7cf56618cf5d361ac2cd31fa3afc175f
session_calendar.csv: ade26e241ba85888fbf39e02f0a3f4d36a8f6e5ab7e2f6f088e56d0d6a1d37b8
roll_calendar.csv: 9ca1eae6942250133e026f7ffd66bfd6f087cfee76ab0f3369a3ec9b1f9cf341
fail_closed_ledger.csv: 80ae11340816a33ae07de3a4cd657c378c82391b5fd0e2d8193292c19d656a16
```

## Policy Decision

Row `892` is not a market-order/TBBO case and does not need market spread evidence. It is a filled `SELL 1` adjacent-limit order where:

- decision and fill candidate share the same declared execution session;
- fill candidate is the exact completed bar at the declared session end;
- fill candidate close equals the executable limit price;
- valuation mark is the exact next completed hourly row after the fill and belongs to the next declared session;
- raw symbol remains `ZNM3` across decision, fill, and valuation rows;
- no roll boundary is present;
- result/backtest/source-faithful gates remain fail closed.

The existing row-436 precedent is close but not identical. Row 436 is a session-open adjacent-limit fill where the decision is at prior session end and the fill occurs at next session open. Row 892 is a session-end adjacent-limit fill where decision and fill are in the same execution session and only valuation crosses into the next session.

Therefore the decision is:

```text
ROW892_SESSION_END_ADJACENT_LIMIT_FILL_ALLOWED_WITH_NEXT_SESSION_ENGINEERING_VALUATION_PENDING_IMPLEMENTATION_NOT_RESULT
```

A future implementation may proceed only as a new bounded local-only engineering convention, not as an unqualified reuse of row 436:

```text
SOURCE_NATIVE_ENGINEERING_SESSION_END_ADJACENT_LIMIT_FILL_ASSUMPTION_NOT_BOOK_EXPLICIT
ONE_HOUR_CLOSE_ONLY_LIMIT_FILL_AT_DECLARED_SESSION_END_WITH_NEXT_SESSION_VALUATION_ENGINEERING_CONVENTION_NOT_BOOK_EXPLICIT
```

This is not book-explicit Carver authority, not source-faithful evidence, not result interpretation, and not a backtest/result claim.

## Required Implementation Conditions

Any implementation must require all of the following facts:

1. row index `892`;
2. raw symbol `ZNM3`;
3. decision timestamp `2023-02-28T20:00:00Z`;
4. fill candidate timestamp `2023-02-28T21:00:00Z`;
5. valuation mark timestamp `2023-02-28T22:00:00Z`;
6. decision and fill candidate have the same declared execution session id;
7. fill candidate timestamp equals the declared execution session end;
8. valuation mark is the exact next completed hourly row after the fill and is in the next declared session;
9. no roll-transition date is present on the selected decision/fill/valuation date;
10. starting position `0`;
11. desired position `-1`;
12. position change `-1`;
13. order side `SELL`;
14. order quantity `1`;
15. adjacent target `-1`;
16. formula limit `111.6707138465356`;
17. executable limit `111.671875`;
18. fill candidate close `111.671875`;
19. fill executed under close-only limit fill by equality;
20. commission-only limit-fill cost treatment;
21. accepted valuation label `SOURCE_NATIVE_ENGINEERING_VALUATION_ASSUMPTION_NOT_BOOK_EXPLICIT`;
22. result/backtest/source-faithful gates fail closed.

If any fact drifts, the runner must remain fail closed and ask the operator.

## Local Hostile Audit

Read-only local hostile-audit subagent `Herschel` returned:

```text
P0: none
P1: none
P2: same_session is ambiguous in the current blocker ledger
```

The P2 is a wording and authorization-shape issue: row `892` decision/fill are same declared execution session, but the current fail-closed row records `same_session = FALSE` because the existing blocker checks decision/fill/valuation as a triplet. This record resolves the ambiguity by requiring future authorization and implementation to state:

```text
decision/fill same declared execution session;
valuation next completed row in next declared session.
```

The audit recommended a bounded local-only engineering convention distinct from row 436 and confirmed no provider/API/download/Git/GPT/result/tuning action was performed.

## Exact Next Authorization

```text
Operator authorizes S27_V2 2023 TEST row-892 session-end adjacent-limit implementation gate, after the row-892 filled adjacent-limit session/EOD policy decision gate, limited to already-local 2023 TEST artifacts and audited S27_V2 machinery.

This authorizes Codex to implement the bounded row-892 policy only: bind the active TEST input pack/run artifacts; verify ZNM3 row 892; verify decision 2023-02-28T20:00:00Z and fill candidate 2023-02-28T21:00:00Z are in the same declared execution session; verify the fill candidate timestamp equals the declared execution session end; verify valuation mark 2023-02-28T22:00:00Z is the exact next completed hourly row after the fill and belongs to the next declared session; verify no roll boundary/raw-symbol/provider condition drift; emit deterministic local-only SELL 1 adjacent-limit order/fill/cost/mechanical-PnL metadata where evidence is sufficient; label the class SOURCE_NATIVE_ENGINEERING_SESSION_END_ADJACENT_LIMIT_FILL_ASSUMPTION_NOT_BOOK_EXPLICIT and the fill rule ONE_HOUR_CLOSE_ONLY_LIMIT_FILL_AT_DECLARED_SESSION_END_WITH_NEXT_SESSION_VALUATION_ENGINEERING_CONVENTION_NOT_BOOK_EXPLICIT; preserve result/backtest/source-faithful evidence fail-closed gates; continue only until the next genuine fail-closed blocker; run focused tests and one local hostile audit; and record process/current-state outputs.

No provider/API access, downloads, new data acquisition, broader TEST continuation beyond the next blocker, VALIDATION, OOS, Lockbox, Forward, result interpretation, PnL evaluation beyond mechanical construction, tuning, adapter/deployment/trading/promotion, Git actions, GPT packet preparation, or source-faithful evidence claim.

If row facts drift, if decision/fill are not the same declared execution session, if fill is not exactly at declared session end, if valuation mark is not the exact next completed hourly row in the next declared session, if roll/symbol/provider conditions drift, if a working-order carry or market/TBBO condition becomes required, or if implementation requires provider/API/download/new data/protected-window access/Git/adapter/deployment/trading/promotion, Codex must fail closed and ask the operator.
```

## Non-Authorizations

This record authorizes no implementation, no TEST continuation, no provider/API access, no downloads, no new data acquisition, no VALIDATION, no OOS, no Lockbox, no Forward, no result interpretation, no PnL evaluation beyond mechanical construction, no tuning, no adapter work, no deployment, no trading, no promotion, no Git actions, no GPT packet preparation, and no source-faithful evidence claim.
