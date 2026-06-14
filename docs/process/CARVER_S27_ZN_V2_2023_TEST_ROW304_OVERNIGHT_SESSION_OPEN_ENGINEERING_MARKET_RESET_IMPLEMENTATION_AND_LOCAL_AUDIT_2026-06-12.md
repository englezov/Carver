# CARVER S27 ZN V2 2023 TEST Row 304 Overnight Session-Open Engineering Market-Reset Implementation And Local Audit

Date: 2026-06-12

Status:

```text
LOCAL_PASS_2023_TEST_ROW304_ENGINEERING_SESSION_OPEN_MARKET_RESET_IMPLEMENTED_NOT_RESULT
```

## Authorization

Operator authorized the bounded S27_V2 2023 TEST row-304 overnight/session-open engineering market-reset implementation gate after acceptance of the engineering convention.

Scope was limited to already-local 2023 TEST artifacts and already-acquired TBBO evidence.

No provider/API access, downloads, new data, broader TEST continuation beyond the declared pack, VALIDATION, OOS, Lockbox, Forward, result interpretation, PnL evaluation beyond mechanical row construction, tuning, adapter/deployment/trading/promotion, Git actions, GPT packet preparation, or source-faithful evidence claim was authorized.

## Implemented Boundary

The patch implements only the bounded row-304 case:

```text
row_index = 304
raw_symbol = ZNH3
decision_timestamp_utc = 2023-01-20T21:00:00Z
fill_timestamp_utc = 2023-01-20T22:00:00Z
valuation_mark_timestamp_utc = 2023-01-23T00:00:00Z
starting_position_contracts = 7
desired_position_contracts = 9
position_change_contracts = 2
order_side = BUY
order_quantity = 2
```

The engineering convention label is:

```text
SOURCE_NATIVE_ENGINEERING_SESSION_OPEN_MARKET_RESET_ASSUMPTION_NOT_BOOK_EXPLICIT
```

This label is emitted and validated in both:

```text
no_market_order_ledger.csv
market_order_ledger.csv
```

The valuation convention remains:

```text
SOURCE_NATIVE_ENGINEERING_VALUATION_ASSUMPTION_NOT_BOOK_EXPLICIT
```

This is local Development/Reconciliation/TEST mechanical construction metadata only. It is not book-explicit authority, not source-faithful evidence, not result interpretation, and not a backtest result.

## Artifact State

Run root:

```text
docs/researchops/s27_v2_local_replay_runs/ZN/20260612_2023_test_mechanical_artifact_run
```

Run manifest state:

```text
candidate_row_count = 304
supported_mechanical_row_count = 304
fail_closed_row_index = 0
fail_closed_reason = NO_FAIL_CLOSED_BLOCKER_DECLARED_PACK_EXHAUSTED_NOT_RESULT
```

Row 304 emitted:

```text
market_order_rows_emitted = TRUE
market_fallback_status = LOCKED_MARKET_ORDER_EXECUTED_FULL_GAP
fill_price = 115.0625
tbbo_quote_ts_event = 2023-01-20T21:59:59.924187905Z
tbbo_bid_px = 115.046875
tbbo_ask_px = 115.0625
commission_amount = 4.6
spread_cost_amount = 0.0
total_cost_amount = 4.6
valuation_mark_close_price = 115.03125
row_gross_pnl_amount = -171.875
row_net_pnl_amount = -176.475
cumulative_net_pnl_amount = 5897.225
```

All PnL fields remain mechanical construction fields only. Result, backtest, PnL evaluation beyond mechanical construction, and source-faithful evidence gates remain fail-closed.

## Hashes

```text
run_manifest.json = 6822c1e832bf49beb2665d832355370ea107e4fc2ca7a9b2a8c18637071c1abb
evidence_manifest.json = e50f7587c829fedb14e6119799156862f9c9d9e70e0c4da333adb55e2903f31c
trusted_bundle.json = 019a0570ff221fa8a4c24661a058084ad94033005c66b22485bf5ed701fd4c88
no_market_order_ledger.csv = bc8bcad27afe0e7351b96f934ef87bf909bef42f835ea1f1cc38231522d41ada
market_order_ledger.csv = e45aa4833c3271def9a49015e81d023112f9b8f245f31d9dcdcdc823e5621a34
market_fill_metadata_ledger.csv = d2f2ca7e6ca0ac05431b4d3d1beadb7588bf9595bd55ec0c00a61bd661085ccf
working_order_transition_ledger.csv = 8199d5aaf90df3383e1924bb7c3236cc5a1094dd7a42bc7b86fcfb87d19778f6
fill_ledger.csv = a0153c2f217edc472503fe23f904876b98b2358e97e8c0d6b36944e510ae5cb2
cost_ledger.csv = cc9116536da20bfc892064c5924c4a484cafac71471f26f835344390ef1e64d2
pnl_ledger.csv = 2ec664e5ac50d829732a104a4cc6f1f7c0fffec2ce6425253c481aac28d83443
fail_closed_ledger.csv = a877e520543a7ea2a3337eaddf14e24b7444f781477e236f657a89470edbac70
```

## Verification

Commands run:

```text
python -m py_compile src\carver\spine\s27_v2_replay\test_mechanical_run.py src\carver\spine\s27_v2_replay\pretest_machine_freeze.py tests\test_s27_v2_2023_test_mechanical_run.py
python -m pytest tests\test_s27_v2_2023_test_mechanical_run.py -q
python -m pytest tests\test_s27_v2_pretest_development_recon_completion.py tests\test_s27_v2_2023_test_mechanical_run.py -q
```

Results:

```text
py_compile PASS
tests\test_s27_v2_2023_test_mechanical_run.py: 59 passed
paired pretest/2023 TEST focused suites: 120 passed
```

## Local Hostile Audit

One read-only local hostile-audit subagent first found:

```text
P1: row-304 self-consistent forgery rejection incomplete
P2: accepted engineering convention label not emitted in artifacts
```

The implementation was hardened in the same bounded row-304 scope:

- `no_market_order_ledger.csv` now emits and validates `engineering_convention_label`;
- `market_order_ledger.csv` now emits and validates `engineering_convention_label`;
- row-304 no-market state is validated by the accepting bundle path;
- row-304 transition working-state fields are validated;
- row-304 fill rule, fill price, quantity, and position are validated;
- self-consistent forged-artifact tests now cover no-market, market-order, market-fill, transition, fill, cost, and PnL row-304 mutations.

The same local hostile-audit subagent re-audited the hardening and returned:

```text
P0: None
P1: None
P2: None
P3: None
Prior P1: closed
Prior P2: closed
```

## Current State

Current status:

```text
LOCAL_PASS_2023_TEST_ROW304_ENGINEERING_SESSION_OPEN_MARKET_RESET_IMPLEMENTED_PACK_EXHAUSTED_NOT_RESULT
```

The declared 304-row TEST pack is now fully supported mechanically under the accepted local engineering convention. The terminal state is pack exhaustion, not a new blocker.

This does not authorize broader TEST continuation into any new pack/window, VALIDATION, OOS, Lockbox, Forward, result interpretation, PnL evaluation beyond mechanical construction, source-faithful evidence claims, tuning, adapter/deployment/trading/promotion, Git actions, GPT packet preparation, or promotion.

## Next Gate

Recommended next gate:

```text
S27_V2_2023_TEST_ROW304_COMPLETION_GPT55_AUDIT_OR_NEXT_TEST_WINDOW_PLANNING_GATE
```

The next gate should decide whether to prepare a GPT 5.5 audit packet for the completed 304-row TEST mechanical artifact pack, or to plan the next strictly bounded TEST window with the same protected-window and non-result boundaries.
