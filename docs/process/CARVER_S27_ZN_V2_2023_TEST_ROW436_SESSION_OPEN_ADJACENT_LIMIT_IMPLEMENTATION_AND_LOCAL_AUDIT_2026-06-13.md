# S27_V2 2023 TEST Row 436 Session-Open Adjacent-Limit Implementation And Local Audit

Date: 2026-06-13

Status:

```text
LOCAL_PASS_2023_TEST_ROW436_SESSION_OPEN_ADJACENT_LIMIT_IMPLEMENTED_TO_ROW437_MARKET_TBBO_BLOCKER_NOT_RESULT
```

## Scope

Operator authorized a local-only row-436 adjacent-limit session/EOD policy decision and implementation gate after local PASS on class-level TEST continuation to row 436.

Scope was limited to already-local 2023 ZN TEST artifacts and audited S27_V2 machinery for the exact row/class:

```text
raw_symbol: ZNH3
decision_timestamp_utc: 2023-01-30T21:00:00Z
starting_position_contracts: 24
desired_position_contracts: 23
position_change_contracts: -1
order_side: SELL
adjacent_target_position: 23
limit_order_price: 114.296875
fill_candidate_timestamp_utc: 2023-01-30T22:00:00Z
fill_candidate_close: 114.40625
fill_executed: TRUE
same_session: FALSE
```

This record authorizes no provider/API access, downloads, new data, VALIDATION, OOS, Lockbox, Forward, result interpretation, PnL evaluation beyond mechanical construction, tuning, adapter work, deployment, trading, promotion, Git action, GPT packet preparation, or source-faithful evidence claim.

## Policy Decision

Row 436 is a filled adjacent-limit order across a session boundary. It is not a market-order TBBO/spread case.

The implementation keeps the row explicitly local-only and engineering-labeled:

```text
SOURCE_NATIVE_ENGINEERING_SESSION_OPEN_ADJACENT_LIMIT_FILL_ASSUMPTION_NOT_BOOK_EXPLICIT
ONE_HOUR_CLOSE_ONLY_LIMIT_FILL_WITH_SESSION_OPEN_ENGINEERING_CONVENTION_NOT_BOOK_EXPLICIT
LOCAL_ENGINEERING_SESSION_OPEN_ADJACENT_LIMIT_FILL_ROW_EMITTED_NOT_RESULT
```

This is not book-explicit Carver authority, not source-faithful evidence, not result interpretation, and not a backtest/result claim.

## Code Changes

Patched:

```text
src/carver/spine/s27_v2_replay/test_mechanical_run.py
src/carver/spine/s27_v2_replay/pretest_machine_freeze.py
tests/test_s27_v2_2023_test_mechanical_run.py
```

The TEST runner now accepts the row-436 class only when the bounded facts match: ZNH3 raw-symbol consistency, decision at declared session end, fill at next declared session start, fill/mark session continuity, mark after fill, position change of exactly one contract, side matching signed position change, no market-order emission, engineering convention labels preserved, and result/backtest/source-faithful gates fail closed.

The machine-freeze guard now rejects filled orders across unresolved session/EOD gaps unless the already-bounded session-open market-reset class or this row-436 session-open adjacent-limit class validates.

Focused tests now assert row-436 emitted artifacts and reject self-consistent forged row/hash mutations across order, no-market, transition, fill, cost, and PnL ledgers.

## Row 436 Emitted Artifacts

The regenerated run emitted:

```text
limit_order_ledger.csv row 436:
  SELL 1, adjacent target 23, formula 114.29396275895618, limit 114.296875

no_market_order_ledger.csv row 436:
  market_order_required FALSE
  market_order_rows_emitted FALSE
  market_fallback_status NOT_REQUIRED_LIMIT_ORDER_FILLED
  engineering_convention_label SOURCE_NATIVE_ENGINEERING_SESSION_OPEN_ADJACENT_LIMIT_FILL_ASSUMPTION_NOT_BOOK_EXPLICIT

working_order_transition_ledger.csv row 436:
  starting position 24
  ending position 23
  same_session FALSE

fill_ledger.csv row 436:
  fill_executed TRUE
  fill_rule ONE_HOUR_CLOSE_ONLY_LIMIT_FILL_WITH_SESSION_OPEN_ENGINEERING_CONVENTION_NOT_BOOK_EXPLICIT
  fill_candidate_close 114.40625
  fill_price 114.296875
  fill_quantity 1
  position_after_fill 23

cost_ledger.csv row 436:
  commission_amount 2.3
  spread_cost_amount 0.0
  total_cost_amount 2.3
  currency USD

pnl_ledger.csv row 436:
  valuation_mark_timestamp_utc 2023-01-31T00:00:00Z
  valuation_mark_close_price 114.34375
  valuation_convention_label SOURCE_NATIVE_ENGINEERING_VALUATION_ASSUMPTION_NOT_BOOK_EXPLICIT
  ending_position_contracts 23
  result/backtest/source-faithful gates fail closed
```

Mechanical PnL fields are construction metadata only:

```text
existing_position_gross_pnl: -1500.0
fill_gross_pnl: -46.875
row_gross_pnl_amount: -1546.875
row_net_pnl_amount: -1549.175
cumulative_gross_pnl_amount: 3500.0
cumulative_commission_amount: 834.8999999999999
cumulative_spread_amount: 0.0
cumulative_net_pnl_amount: 2665.1000000000004
```

These are not result interpretation and not PnL evaluation.

## Current Run State

The regenerated controlled 2023 TEST mechanical artifact run now supports rows 1 through 436 and fails closed at row 437:

```text
candidate_row_count: 437
supported_mechanical_row_count: 436
fail_closed_row_index: 437
fail_closed_reason: FAIL_CLOSED_MARKET_ORDER_SPREAD_EVIDENCE_UNAVAILABLE_FOR_CONTINUATION_NOT_RESULT
```

Row 437 facts:

```text
decision_timestamp_utc: 2023-01-31T00:00:00Z
raw_symbol: ZNH3
starting_position_contracts: 23
desired_position_contracts: 19
position_change_contracts: -4
order_side: SELL
market_order_required: TRUE
market_order_rows_emitted: FALSE
market_order_reason: BOOK_REQUIRED_TARGET_POSITION_GAP_GREATER_THAN_ONE_CONTRACT
fill_candidate_timestamp_utc: 2023-01-31T01:00:00Z
fail_closed_reason: FAIL_CLOSED_MARKET_ORDER_SPREAD_EVIDENCE_UNAVAILABLE_FOR_CONTINUATION_NOT_RESULT
```

Row 437 emits no market order, fill, cost, PnL, result, backtest, or source-faithful evidence row.

## Artifact Hashes

```text
run_manifest.json: CDB8388118EF801F5A5CB22364C8F11BCBC4322797F6F229C4AA695E9DD84112
evidence_manifest.json: 4FEF572398E1FE9C93D0C24ACE0A4D0A50744B05A6BC394DECD7D14A5B16C2DF
trusted_bundle.json: 299780B988D51A504841AB5FB4BECFD6DC0E22EC24ED1CB966831E67E1898515
run_bundle.json: 9FF75EF0A4D4090CC59C0AA500ED83B9101DAB2BE522B9B7A0B3EC2C335767D5
SHA256SUMS.csv: 78EA885F4F3F82D570E5CDA58CDEC77AAD5372202396BA6BF2B544CADA003D30
```

## Verification

Passed:

```text
python -m pytest tests\test_s27_v2_2023_test_mechanical_run.py -q
107 passed in 557.94s

python -m pytest tests\test_s27_v2_pretest_development_recon_completion.py tests\test_s27_v2_2023_test_mechanical_run.py -q
168 passed in 410.95s
```

## Local Hostile Audit

One read-only local hostile-audit subagent returned:

```text
Verdict: PASS
P0 findings: None
P1 findings: None
P2 findings: None
```

The audit confirmed row 436 is tightly bound to the emitted artifacts, the engineering/not-book-explicit label is preserved, row 437 remains the next fail-closed blocker, package-root exports do not leak the TEST runner, `runner.py` remains fail-closed, and no provider/API/download/protected-window/Git/result/source-faithful claim surface was introduced.

## Current Status

```text
LOCAL_PASS_2023_TEST_ROW436_SESSION_OPEN_ADJACENT_LIMIT_IMPLEMENTED_TO_ROW437_MARKET_TBBO_BLOCKER_NOT_RESULT
```

The next useful local gate is row-437 bounded market-order TBBO evidence and market-order continuation under the standing bounded TBBO policy or a fresh equivalent authorization.

External GPT/Opus audits remain deferred until a consolidated checkpoint unless separately authorized.
