# CARVER S27 V2 2023 TEST Row 1113 Session-End Market-Order Valuation-Gap Implementation And Local Audit - 2026-06-15

## Status

`LOCAL_PASS_ROW1113_SESSION_END_MARKET_ORDER_VALUATION_GAP_IMPLEMENTED_AND_CONTINUED_TO_ROW1355_SESSION_EOD_BLOCKER_NOT_RESULT`

## Scope

This record covers the bounded S27_V2 2023 TEST row-1113 implementation gate only. The implemented class is:

`SOURCE_NATIVE_ENGINEERING_SESSION_END_MARKET_ORDER_FILL_WITH_NEXT_AVAILABLE_VALUATION_GAP_ASSUMPTION_NOT_BOOK_EXPLICIT`

The class is not book-explicit authority, not source-faithful evidence, not result interpretation, and not a backtest/result claim.

## Bound Row-1113 Facts

- Instrument lane: `SOURCE_NATIVE_FUTURES`
- Raw symbol: `ZNM3`
- Row index: `1113`
- Decision timestamp: `2023-03-14T20:00:00Z`
- Starting position: `-17`
- Desired position: `-15`
- Position change: `BUY 2`
- Fill candidate timestamp: `2023-03-14T21:00:00Z`
- Fill candidate status: same raw symbol, same declared execution session, exactly declared session end
- Immediate valuation mark absence: no declared same-symbol `2023-03-14T22:00:00Z` valuation row
- Valuation mark timestamp: `2023-03-14T23:00:00Z`
- Valuation status: first available completed same-symbol valuation row after fill, next declared session
- Valuation label: `SOURCE_NATIVE_ENGINEERING_VALUATION_ASSUMPTION_NOT_BOOK_EXPLICIT`
- TBBO selected quote: `2023-03-14T20:59:59.840382723Z`
- TBBO bid/ask: `113.453125` / `113.46875`
- BUY executable ask fill price: `113.46875`
- Commission: `4.60 USD`
- Spread cost: `0.00 USD` under ask-fill/no-separate-spread accounting

## Implementation Summary

`src/carver/spine/s27_v2_replay/test_mechanical_run.py` now includes a row-1113-bounded helper and validator path for session-end market-order fills where the immediate next-hour valuation mark is absent from the declared valuation row family and the first available completed same-symbol mark is in the next declared session.

The validator binds:

- exact row index, timestamps, raw symbol, side, quantity, starting/target positions;
- same-session decision/fill and fill-at-session-end facts;
- absence of the immediate `2023-03-14T22:00:00Z` valuation mark and first available `2023-03-14T23:00:00Z` valuation mark;
- selected at-or-before-fill TBBO quote timestamp and BUY ask price;
- market-fill metadata side, quantity, price, provenance, session flag, spread-cost status, and target position;
- PnL valuation timestamp, valuation close, valuation label, ending position, and fail-closed result/backtest/source-faithful gates.

The run was rebuilt and now supports rows `1` through `1354`, failing closed at row `1355`.

## Artifact State

Run root:

`docs/researchops/s27_v2_local_replay_runs/ZN/20260612_2023_test_mechanical_artifact_run`

Current run bundle:

- candidate rows: `1355`
- supported mechanical rows: `1354`
- fail-closed row: `1355`
- fail-closed reason: `SECONDARY_FILLED_ORDER_ACROSS_UNRESOLVED_SESSION_EOD_GAP_NOT_RESULT`
- bundle hash: `25f2f05e9ff24d7573a34d0bae86c36c61728c4ca1115da47139a60013c3e363`
- run manifest hash: `a5e9185a9996d581697365e11b95a92c530e88d7af0d1d32d884c2d880bb330c`
- evidence manifest hash: `cf37a0d1bc3ccb2f3b6d70dd9d0567e7dcd36f01a7aeff92600eb7ec3435abca`
- trusted bundle hash: `2e5dadbb6aca76736679c969bff9cf1402b88a421b3fd421ce5938a47bc23a65`

Row-1113 emitted row hashes:

- market order: `ab8bf2681ab8b4f8e468836584be4d438721aff27952f75b16a7789e01f6f9c0`
- no-market/order-status metadata: `1b63e14f274db8782d933796250800f16324479b6fe5c3e676d3c71e259e127d`
- market fill metadata: `fd43fa35c1dd5adc77679c17b19174293d8396ab9847b45dc662d4dc1890ae67`
- working-order transition: `70863b6b6f1586c52901a9fd8b92697d8ecb2d5624e805acc588b602d403aba4`
- fill ledger: `d2275e7bb28984013729d97c9ec4221b6018c3303342ca897ec7d5d938038f15`
- cost ledger: `507e4c75c3e649917552dd3d79957694745b3bb5a178af8e0c35c4c542efbb14`
- PnL ledger: `18ae02c36b64d7ac1ca62dafad471c4686481e2de197dff079dcc703c7d1b723`

Next fail-closed blocker:

- row index: `1355`
- raw symbol: `ZNM3`
- decision timestamp: `2023-03-29T20:00:00Z`
- fail row hash: `80e097e1f326f2b0f860c1d0a806339b5e3889889488297ef22dd45bc96f05c5`
- fail-closed reason: `SECONDARY_FILLED_ORDER_ACROSS_UNRESOLVED_SESSION_EOD_GAP_NOT_RESULT`

## Verification

Passed:

- `python -m py_compile src\carver\spine\s27_v2_replay\test_mechanical_run.py src\carver\spine\s27_v2_replay\pretest_machine_freeze.py tests\test_s27_v2_2023_test_mechanical_run.py`
- Direct row-1113 validator:
  - `row1113_direct_validation=PASS`
  - `row1113_mutation_rejections=PASS 7`
- Compact artifact audit:
  - `artifact_hashes=PASS`
  - `row1113_artifact_binding=PASS`
  - `row1113_valuation_gap_absence_and_first_mark=PASS`
  - `row1355_next_blocker=PASS`

The direct mutation battery rejected mutations to row-1113 market-order label, no-market label, market-fill timestamp, market-fill price, transition same-session flag, PnL valuation timestamp, and PnL valuation label.

Not claimed:

- A focused pytest slice was attempted, but the generated-bundle validation path timed out after 600 seconds. No pytest PASS is claimed for that slow path in this record.
- A subagent local hostile audit was attempted, but the Codex usage limit prevented the subagent from running. The local hostile audit was therefore performed inline with the targeted verifier scripts above.

## Inline Local Hostile Audit Result

- P0 findings: none.
- P1 findings: none.
- P2 findings: none.
- P3 notes:
  - The full generated-bundle pytest path remains very slow for this checkpoint. The targeted validator and artifact/hash audits were used for local acceptance.
  - The next blocker at row `1355` appears to be an adjacent-limit session/EOD valuation-gap class, not a row-1113 market-order issue.

## Current Boundary

The row-1113 implementation is locally accepted for continuation to the next gate. The controlled TEST mechanical run is now stopped at row `1355`, which requires a separate row-1355 adjacent-limit session/EOD valuation-gap policy decision before further continuation.

## Non-Authorizations Preserved

This implementation did not authorize provider/API access, downloads, new data acquisition, broader TEST continuation beyond the next blocker, VALIDATION, OOS, Lockbox, Forward, result interpretation, PnL evaluation beyond mechanical construction, tuning, adapter work, deployment, trading, promotion, Git actions, GPT packet preparation, or source-faithful evidence claims.
