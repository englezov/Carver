# CARVER S27 ZN V2 2023 TEST Row 1378 Post-Fill TBBO Pack Exhaustion Implementation

Date: 2026-06-21

Status: LOCAL_PASS_ROW1378_POST_FILL_TBBO_PACK_EXHAUSTED_MECHANICAL_ARTIFACTS_NOT_RESULT

Authorization:
S27_V2 2023 TEST row-1378 post-fill TBBO engineering convention and declared-pack completion gate.

Scope:
This record covers only the already-local 2023 TEST row-1378 ZNM3 market-order spread evidence binding, deterministic TEST mechanical artifact completion for the current declared 1378-row pack, and fast incremental verifier pack-exhausted terminal-state update.

## Bound Row-1378 Evidence

Accepted engineering label:
`ROW1378_FIRST_POST_FILL_TBBO_QUOTE_SPREAD_EVIDENCE_ENGINEERING_CONVENTION_NOT_BOOK_EXPLICIT`

Selected quote:
- row_index: 1378
- raw_symbol: ZNM3
- decision_timestamp_utc: 2023-03-30T23:00:00Z
- fill_timestamp_utc: 2023-03-31T00:00:00Z
- selected_quote_ts_event: 2023-03-31T00:00:00.183796035Z
- quote_lag_seconds: 0.183796035
- bid_px_00: 114.515625
- ask_px_00: 114.53125
- selected SELL executable bid: 114.515625

Bound selected registry:
`docs/researchops/s27_v2_market_spread_evidence/ZN/20260621_2023_test_row1378_post_fill_tbbo_engineering_convention/ledger/20260621_S27_V2_2023_TEST_ROW1378_POST_FILL_TBBO_ENGINEERING_selected_spread_registry.csv`

The selected row binds raw DBN and raw CSV hashes from the already-acquired failed-window retry evidence. No provider/API access, download, or new data acquisition was performed under the post-fill binding gate.

## Mechanical Artifact Result

The active 2023 TEST mechanical artifact run was rebuilt after adding row-1378 evidence to the combined TBBO registry:

- candidate_row_count: 1378
- supported_mechanical_row_count: 1378
- fail_closed_row_index: 0
- fail_closed_reason: `NO_FAIL_CLOSED_BLOCKER_DECLARED_PACK_EXHAUSTED_NOT_RESULT`
- final_position_contracts: 3

Row 1378 emitted deterministic local-only market-order/fill/cost/mechanical-PnL metadata with bid-fill/no-separate-spread accounting. Result/backtest/source-faithful evidence remains fail-closed.

## Fast Incremental Verifier Update

The fast incremental verifier now treats the current row-703 trust baseline plus rows 704-1378 as the completed segment:

- segment_start_row_index: 704
- segment_end_row_index: 1378
- segment_row_count: 675
- terminal_fail_row_index: 0
- terminal_fail_reason: `NO_FAIL_CLOSED_BLOCKER_DECLARED_PACK_EXHAUSTED_NOT_RESULT`
- missing TBBO requirements: 0
- ending_position_contracts: 3

The terminal state is represented by a hash-bound pack-exhausted sentinel row, not by a forged fail-closed row.

## Verification

Focused local verification run:

- `python -m pytest tests/test_s27_v2_test_incremental_runner.py -q` -> 15 passed
- `python -m pytest tests/test_s27_v2_fast_segment_emitter.py -q` -> 7 passed
- `python -m pytest tests/test_s27_v2_fast_execution_state.py -q` -> 10 passed
- `python -m pytest tests/test_s27_v2_fast_runner_cache.py -q -x` -> 16 passed
- `python -m pytest tests/test_s27_v2_fast_generated_segment_assembler.py -q` -> 8 passed
- `python -m pytest tests/test_s27_v2_fast_evidence_planner.py -q` -> 7 passed
- `python -m pytest tests/test_s27_v2_fast_order_generator.py tests/test_s27_v2_fast_downstream_generator.py -q` -> 26 passed

Combined fast-family run before the final order/downstream expectation patch produced 86 passed and 2 stale-count expectation failures; those two tests were patched and rerun successfully.

Final smoke:

- FAST: segment rows 675, terminal_fail_row_index 0, missing TBBO requirements 0, ending position 3
- MECH: candidate rows 1378, supported rows 1378, fail_closed_row_index 0, fail_closed reason `NO_FAIL_CLOSED_BLOCKER_DECLARED_PACK_EXHAUSTED_NOT_RESULT`, final position 3

## Non-Authorizations Preserved

No result interpretation, performance evaluation, tuning, source-faithful evidence claim, promotion, deployment, trading, Git action, VALIDATION/OOS/Lockbox/Forward access, adapter work, or broader TEST pack expansion is authorized or claimed by this record.
