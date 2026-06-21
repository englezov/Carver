# S27_V2 2023 TEST Row 1364 Market-Order TBBO Implementation And Local Audit

Date: 2026-06-17

Status:

```text
LOCAL_PASS_ROW1364_BOUNDED_TBBO_BOUND_AND_CONTINUED_TO_ROW1366_MARKET_SPREAD_BLOCKER_NOT_RESULT
```

## Authorization

Operator authorized `S27_V2 2023 TEST row-1364 bounded market-order TBBO evidence and mechanical continuation gate`, limited to already-local 2023 TEST artifacts and bounded DataBento TBBO evidence for the row-1364 `ZNM3` market-order blocker only.

No provider/API access outside the bounded row-1364 TBBO quote window, no downloads or new data outside that window, no broader TEST continuation beyond the next blocker, no VALIDATION, OOS, Lockbox, Forward, result interpretation, PnL evaluation beyond mechanical construction, tuning, adapter/deployment/trading/promotion, Git actions, GPT packet preparation, or source-faithful evidence claim was authorized.

## Bound Row-1364 Evidence

Tool added and executed:

```text
tools/databento/carver_s27_v2_2023_test_row1364_market_spread_tbbo_acquisition.py
```

The tool locks to the active fail-closed row in:

```text
docs/researchops/s27_v2_local_replay_runs/ZN/20260612_2023_test_mechanical_artifact_run/fail_closed_ledger.csv
```

Required active blocker facts:

```text
row_index: 1364
raw_symbol: ZNM3
decision_timestamp_utc: 2023-03-30T07:00:00Z
fill_candidate_timestamp_utc: 2023-03-30T08:00:00Z
starting_position_contracts: 6
desired_position_contracts: 4
position_change_contracts: -2
order_side: SELL
market_order_reason: BOOK_REQUIRED_TARGET_POSITION_GAP_GREATER_THAN_ONE_CONTRACT
fail_closed_reason: FAIL_CLOSED_MARKET_ORDER_SPREAD_EVIDENCE_UNAVAILABLE_FOR_CONTINUATION_NOT_RESULT
```

Bound provider request:

```text
dataset: GLBX.MDP3
schema: tbbo
stype_in: raw_symbol
symbol: ZNM3
request_start_utc: 2023-03-30T07:59:55Z
request_end_utc: 2023-03-30T08:00:05Z
```

Selected quote:

```text
selected_quote_ts_event: 2023-03-30T07:59:58.203532779Z
quote_age_seconds: 1.796468
bid_px_00: 114.640625
ask_px_00: 114.65625
selected SELL executable bid: 114.640625
full_spread_points: 0.015625
```

Evidence hashes:

```text
raw_dbn_sha256: 9FF8ADA9FCD9BC5A17C06C9271B299F19B0A2494E6C889573EF4A130E6C338A1
raw_csv_sha256: 9E5F47C7CF5490981B81B608C7FFC9BCDC63239C4D97FF2A11DE3602C72152D0
selected_spread_row_hash: 503a1a0c777b2ccdb6ff045499bdbc7edb136c79df72bf0542ecb869ccef7064
selected_spread_registry_sha256: 03E1C5CACB16353A049CAB39DE105CB20F9328B3DC42546AB3574F08A2F0F3AF
provider_condition_row_hash: 80491f70ebe397a0bc372918db7abf57ee23f7061b861e00a5feee161e56dcff
```

The active combined TBBO registry includes row `1364` as `ROW1364_AT_OR_BEFORE_FILL_TBBO`.

```text
combined_registry_row_hash_for_1364: 80dd0dd1dc186292ef56dab2d4802e553a95a20ea71e72b6317d64c0db64732e
combined_registry_sha256: 2321820c2b03b613ed449733102ade7058040e847082ecd2b70f7f91765f8a3c
```

## Mechanical Continuation Result

The controlled 2023 TEST mechanical artifact run now supports rows `1` through `1365` and fails closed at row `1366`.

Run bundle:

```text
candidate_row_count: 1366
supported_mechanical_row_count: 1365
fail_closed_row_index: 1366
fail_closed_reason: FAIL_CLOSED_MARKET_ORDER_SPREAD_EVIDENCE_UNAVAILABLE_FOR_CONTINUATION_NOT_RESULT
run_manifest_hash: 90773915c5b3db0488e1acefd73998f17ece77249b52e766d711992bb19964cf
evidence_manifest_hash: 3d366b10215058cd70fc115309d148ff934f61df4ec06c3d0acdd8f66278e84e
trusted_bundle_hash: a62b08930d7c567e6dfed620de9bacfbc92e5227c2ce04afe5151e6b3c1fcdf2
bundle_hash: fef2b2af4472932932ce94ec6e1d3e8d5d725e78a36cfd6d802d16462175c464
```

Row `1364` emits deterministic local-only SELL 2 market-order/fill/cost/mechanical-PnL metadata:

```text
fill_timestamp_utc: 2023-03-30T08:00:00Z
fill_price: 114.640625
commission_amount: 4.6 USD
spread_cost_amount: 0.0 USD
total_cost_amount: 4.6 USD
market_cost_accounting_convention: BID_FILL_PRICE_WITH_NO_SEPARATE_SPREAD_COST
valuation_mark_timestamp_utc: 2023-03-30T09:00:00Z
valuation_mark_close_price: 114.453125
row_gross_pnl_amount: -750.0
row_net_pnl_amount: -754.6
ending_position_contracts: 4
result_status: FAIL_CLOSED_RESULT_ROW_NOT_EMITTED_NOT_AUTHORIZED
backtest_status: FAIL_CLOSED_BACKTEST_RESULT_NOT_EMITTED_NOT_AUTHORIZED
source_faithful_evidence_claimed: FALSE
```

Row `1365` is a no-action/no-cost mechanical row.

The next blocker is row `1366`:

```text
raw_symbol: ZNM3
decision_timestamp_utc: 2023-03-30T09:00:00Z
fill_candidate_timestamp_utc: 2023-03-30T10:00:00Z
starting_position_contracts: 4
desired_position_contracts: 6
position_change_contracts: 2
order_side: BUY
fail_closed_reason: FAIL_CLOSED_MARKET_ORDER_SPREAD_EVIDENCE_UNAVAILABLE_FOR_CONTINUATION_NOT_RESULT
```

## Verification

Passed:

```text
python -m py_compile tools\databento\carver_s27_v2_2023_test_row1364_market_spread_tbbo_acquisition.py
python -m py_compile src\carver\spine\s27_v2_replay\test_mechanical_run.py tools\databento\carver_s27_v2_2023_test_row1364_market_spread_tbbo_acquisition.py
python -m py_compile tests\test_s27_v2_2023_test_mechanical_run.py src\carver\spine\s27_v2_replay\test_mechanical_run.py tools\databento\carver_s27_v2_2023_test_row1364_market_spread_tbbo_acquisition.py
```

The acquisition tool returned:

```text
PASS_ROW1364_BOUNDED_DATABENTO_TBBO_SELECTED_NOT_RESULT
selected_rows=1
failed_rows=0
```

Direct readback bundle validation passed:

```text
bundle_validate=PASS
supported=1365
fail=1366 FAIL_CLOSED_MARKET_ORDER_SPREAD_EVIDENCE_UNAVAILABLE_FOR_CONTINUATION_NOT_RESULT
```

No full pytest PASS is claimed for this gate.

## Local Hostile Audit

Local hostile audit scope:

- row-1364 bounded provider access limited to the active quote window;
- selected quote is fresh, non-crossed, at-or-before-fill, and side-correct for SELL bid fill;
- row-1364 registry/source hash binding;
- no spread double-counting under bid-fill accounting;
- row-1364 mechanical metadata emission;
- row-1366 fail-closed boundary;
- result/backtest/source-faithful gates remain fail-closed.

Status:

```text
LOCAL_HOSTILE_AUDIT_PASS_NO_P0_P1_P2_WITH_P3_PROVENANCE_CAVEAT_NOT_BLOCKING
```

Local hostile audit result:

```text
P0 findings: none
P1 findings: none
P2 findings: none
P3 findings: one provenance caveat, not blocking
```

The local hostile audit verified bounded row-1364 provider use, selected SELL bid quote binding at `2023-03-30T07:59:58.203532779Z`, combined registry binding, row-1364 market/fill/cost/mechanical-PnL metadata, row-1366 fail-closed continuation, and result/backtest/source-faithful fail-closed gates.

P3 provenance caveat:

```text
The row-1364 request manifest records the pre-continuation fail-closed ledger hash, but the live run directory now contains the post-continuation row-1366 fail-closed ledger. This is expected after continuation and is not a blocker, but the pre-continuation row-1364 fail-closed ledger bytes are not independently recoverable from the current named run directory alone.
```

## Current Status

```text
LOCAL_PASS_ROW1364_BOUNDED_TBBO_BOUND_AND_CONTINUED_TO_ROW1366_MARKET_SPREAD_BLOCKER_NOT_RESULT
```

The next useful gate is bounded TBBO spread evidence for row `1366` under the standing bounded market-order TBBO policy, or a consolidated deterministic requirements-ledger batch if row `1366` is part of a broader missing-TBBO set.

Provider/API access remains unauthorized unless separately and explicitly bounded to listed quote windows. Git, GPT packet preparation, protected-window access, result interpretation, tuning, source-faithful evidence claims, adapter/deployment/trading/promotion, and promotion remain unauthorized.
