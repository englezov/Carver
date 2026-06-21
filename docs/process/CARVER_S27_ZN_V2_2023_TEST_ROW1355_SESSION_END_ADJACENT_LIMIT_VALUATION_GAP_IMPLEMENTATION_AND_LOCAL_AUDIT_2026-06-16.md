# S27 V2 ZN 2023 TEST Row 1355 Session-End Adjacent-Limit Valuation-Gap Implementation And Local Audit

Date: 2026-06-16

Status:

```text
LOCAL_PASS_ROW1355_SESSION_END_ADJACENT_LIMIT_VALUATION_GAP_IMPLEMENTED_AND_CONTINUED_TO_ROW1356_MARKET_SPREAD_BLOCKER_NOT_RESULT
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Scope

This record covers the bounded S27_V2 2023 TEST row-1355 implementation gate.
The implementation is local-only mechanical construction metadata for an
already-declared 2023 TEST row. It is not book-explicit authority, not
source-faithful evidence, not result interpretation, and not a backtest/result
claim.

No provider/API access, downloads, new data acquisition, broader TEST
continuation beyond the next blocker, VALIDATION, OOS, Lockbox, Forward,
result interpretation, PnL evaluation beyond mechanical construction, tuning,
adapter/deployment/trading/promotion, Git action, GPT packet preparation, or
source-faithful evidence claim was authorized or performed.

## Implemented Convention

Class label:

```text
SOURCE_NATIVE_ENGINEERING_SESSION_END_ADJACENT_LIMIT_FILL_WITH_NEXT_AVAILABLE_VALUATION_GAP_ASSUMPTION_NOT_BOOK_EXPLICIT
```

Fill rule:

```text
ONE_HOUR_CLOSE_ONLY_LIMIT_FILL_AT_DECLARED_SESSION_END_WITH_NEXT_AVAILABLE_VALUATION_GAP_ENGINEERING_CONVENTION_NOT_BOOK_EXPLICIT
```

Row status:

```text
LOCAL_ENGINEERING_SESSION_END_ADJACENT_LIMIT_VALUATION_GAP_ROW_EMITTED_NOT_RESULT
```

## Bound Row-1355 Facts

- row index: `1355`
- raw symbol: `ZNM3`
- decision timestamp: `2023-03-29T20:00:00Z`
- starting position: `7`
- desired position: `8`
- position change: `BUY 1`
- adjacent target: `8`
- formula limit: `114.49366645867451`
- executable limit: `114.484375`
- fill candidate timestamp: `2023-03-29T21:00:00Z`
- fill candidate close: `114.46875`
- fill price: `114.484375`
- valuation mark timestamp: `2023-03-29T23:00:00Z`
- valuation mark close: `114.5`
- valuation label: `SOURCE_NATIVE_ENGINEERING_VALUATION_ASSUMPTION_NOT_BOOK_EXPLICIT`
- commission: `2.30 USD`
- spread cost: `0.00 USD`

Declared source rows prove:

- decision/fill same-symbol `ZNM3`;
- decision/fill same declared execution session
  `UTC_ZN_2023_TEST_2023-03-28T22:00:00Z_2023-03-29T21:00:00Z`;
- fill candidate exactly at declared session end;
- no immediate same-symbol `2023-03-29T22:00:00Z` valuation row in the declared valuation-mark family;
- first available completed same-symbol valuation row after fill is `2023-03-29T23:00:00Z`;
- no roll transition on the decision/fill/valuation dates.

## Code Changes

Patched:

- `src/carver/spine/s27_v2_replay/test_mechanical_run.py`
- `src/carver/spine/s27_v2_replay/pretest_machine_freeze.py`
- `tests/test_s27_v2_2023_test_mechanical_run.py`

The runner now recognizes the exact row-1355 valuation-gap adjacent-limit case
in both the pack-selection mechanics path and the artifact-emission path.

The bundle validator now rejects forged row-1355 order, no-market, transition,
fill, cost, or PnL artifacts even if row/evidence/trusted hashes are recomputed.

The machine-freeze guard now accepts only the exact row-1355 class while
preserving the general cross-session filled-order fail-closed guard.

## Artifact State

Run root:

```text
docs/researchops/s27_v2_local_replay_runs/ZN/20260612_2023_test_mechanical_artifact_run
```

Current run bundle:

- candidate rows: `1356`
- supported mechanical rows: `1355`
- fail-closed row: `1356`
- fail-closed reason: `FAIL_CLOSED_MARKET_ORDER_SPREAD_EVIDENCE_UNAVAILABLE_FOR_CONTINUATION_NOT_RESULT`
- bundle hash: `4b33f9c732d3550d0acc277d8b8d885597f114f9f5a410c25975245983cf6db2`
- run manifest hash: `c889320271f9c7d57005b8ee7bfb5b48a8fbabc0684ecb2c8b695e107c7e4a60`
- evidence manifest hash: `bdf1454b8d2e33eb4ef91f9b8da9d1b69625624956e9e1b621b961b3f892ecb5`
- trusted bundle hash: `0e372137d81cffacde6464ab99b74d6be0014ea949d1b8cbd82daef5d13fbcc8`

Row-1355 emitted row hashes:

- desired position: `18d695834af35751520d315f82e13c33a61ec05e3591e8ae1a1f7ad0df0896f0`
- limit order: `2d35132157e192414d76b18d0e847200b4a92eea0376eba4833823726535dc6c`
- no-market/order-status metadata: `9804cd704b7ff1457b2f09e81c839809e9ef1ee02c48e82ab52b840f6bf43066`
- working-order transition: `cf7c6ae54a6428fecac1b47926a5b656d176ddf18275b5bd80a43e5a8d6cf7a0`
- fill: `f8b1e96ed3203e1c9b01979a3135af6d74c1201f3663d88ef342dc36c8dfa65d`
- cost: `d506301b3d5539148d37c5e74ef0eb7bce5a3e92003bfe442375174a47b044f2`
- PnL: `2f681bc16896a0fbdc789d79db4c67de47ec80af27ea642137bc681599495b96`

Next fail-closed blocker:

```text
row_index = 1356
decision_timestamp_utc = 2023-03-29T23:00:00Z
raw_symbol = ZNM3
starting_position_contracts = 8
desired_position_contracts = 6
position_change_contracts = -2
order_side = SELL
adjacent_target_position = 7
market_order_required = TRUE
market_order_rows_emitted = FALSE
market_order_reason = BOOK_REQUIRED_TARGET_POSITION_GAP_GREATER_THAN_ONE_CONTRACT
fill_candidate_timestamp_utc = 2023-03-30T00:00:00Z
fill_candidate_close = 114.484375
fail_closed_reason = FAIL_CLOSED_MARKET_ORDER_SPREAD_EVIDENCE_UNAVAILABLE_FOR_CONTINUATION_NOT_RESULT
row_hash = 6415e932560733feb34a31b899da90a7fd1f698be5befaabeeecd61a6852a933
```

## Verification

Passed:

- `python -m py_compile src\carver\spine\s27_v2_replay\test_mechanical_run.py src\carver\spine\s27_v2_replay\pretest_machine_freeze.py tests\test_s27_v2_2023_test_mechanical_run.py`
- controlled rebuild via `build_2023_test_declared_pack()` and `run_2023_test_mechanical_artifacts()`
- internal `TestMechanicalRunBundle.validate()` during the rebuild
- direct row-1355 validator:
  - `row1355_direct_validation=PASS`
  - `row1355_mutation_rejections=PASS 7`
- compact artifact audit:
  - `artifact_hashes=PASS`
  - `row1355_artifact_binding=PASS`
  - `row1355_valuation_gap_absence_and_first_mark=PASS`
  - `row1356_next_blocker=PASS`

The direct mutation battery rejected mutations to row-1355 limit order price,
no-market engineering label, transition same-session flag, fill rule, cost
commission, PnL valuation timestamp, and PnL valuation label.

Not claimed:

- No full heavy pytest run is claimed for this record. The generated-bundle
  pytest path is slow enough that targeted validator and artifact/hash audits
  were used for local acceptance.
- No external GPT/Opus audit was performed or prepared.

## Inline Local Hostile Audit

- P0 findings: none.
- P1 findings: none.
- P2 findings: none.
- P3 notes:
  - The next blocker is a bounded-TBBO market-order spread evidence blocker at
    row `1356`, not a row-1355 adjacent-limit issue.

Audit conclusions:

- row 1355 is tightly bounded to declared source rows and exact convention
  labels;
- the `2023-03-29T22:00:00Z` valuation-row absence is actively checked;
- `2023-03-29T23:00:00Z` is the first available same-symbol valuation mark;
- row 1355 emits no market-order/TBBO rows;
- cost treatment remains commission-only for the limit fill;
- result/backtest/source-faithful gates remain fail-closed;
- no provider/API/download/new data/protected-window/Git/GPT/result/tuning/
  adapter/deployment/trading/promotion surface was introduced.

## Current Boundary

The row-1355 implementation is locally accepted for continuation to the next
gate. The controlled TEST mechanical run is now stopped at row `1356`, which
requires bounded TBBO spread evidence for a `SELL 2` market-order continuation
before further TEST continuation.

## Non-Authorization

This record authorizes no provider/API access, no downloads, no new data, no
broader TEST continuation, no VALIDATION, no OOS, no Lockbox, no Forward, no
result interpretation, no PnL evaluation beyond mechanical construction, no
tuning, no adapter work, no deployment, no trading, no promotion, no Git
actions, no GPT packet preparation, and no source-faithful evidence claim.
