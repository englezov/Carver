# S27_V2 2023 TEST Row 1356 Post-Fill TBBO Engineering Implementation And Local Audit

Date: 2026-06-16

Status:

```text
LOCAL_PASS_ROW1356_POST_FILL_TBBO_ENGINEERING_BOUND_AND_CONTINUED_TO_ROW1364_MARKET_SPREAD_BLOCKER_NOT_RESULT
```

## Authorization

Operator authorized `S27_V2 2023 TEST row-1356 post-fill TBBO engineering convention implementation and mechanical continuation gate`, limited to already-local 2023 TEST artifacts and already-acquired row-1356 TBBO evidence.

No provider/API access, downloads, new data acquisition, broader TEST continuation beyond the next blocker, VALIDATION, OOS, Lockbox, Forward, result interpretation, PnL evaluation beyond mechanical construction, tuning, adapter/deployment/trading/promotion, Git actions, GPT packet preparation, or source-faithful evidence claim was authorized.

## Bound Evidence

Implementation added:

```text
tools/databento/carver_s27_v2_2023_test_row1356_tbbo_engineering_convention_binding.py
```

The tool is local-only for this gate. It reads already-acquired row-1356 TBBO evidence from:

```text
docs/researchops/s27_v2_market_spread_evidence/ZN/20260616_2023_test_row1356_market_order_tbbo
```

It verifies the previously acquired raw provider file hashes:

```text
raw DBN SHA256: E6D5A558A453532EEA88F81C3501A7EF8EC2E0CD5D3F30BAF3197AA0C106F9EF
raw CSV SHA256: AC539F45B3A4D24F6018A33B1182FBE74AA4788A748151778DDE995F4B2216CC
```

It binds the accepted row-specific engineering convention:

```text
ROW1356_FIRST_POST_FILL_TBBO_QUOTE_SPREAD_EVIDENCE_ENGINEERING_CONVENTION_NOT_BOOK_EXPLICIT
```

Selected quote:

```text
row_index: 1356
raw_symbol: ZNM3
fill_timestamp_utc: 2023-03-30T00:00:00Z
selected_quote_ts_event: 2023-03-30T00:00:00.099806785Z
quote_lag_seconds: 0.099806785
bid_px_00: 114.484375
ask_px_00: 114.5
selected SELL executable bid: 114.484375
full_spread_points: 0.015625
point_value_usd: 1000
```

The selected-spread row hash is:

```text
072e5ed6e19b747b5ba78665686626d7d2403101f9a0adadc183088434dfcc77
```

The row-1356 engineering selected-spread registry SHA256 is:

```text
BF13FF221721410BB02DAB8067C03EBC4C01DDFBD6A57BA66D223CBCCBA4D79E
```

The active combined TBBO registry SHA256 consumed by the TEST mechanical run is:

```text
bbdaca4acf36ba6fc0ed3a403f30658164ed645ab57104222404d3745c30f4f4
```

## Implementation

`src/carver/spine/s27_v2_replay/test_mechanical_run.py` now includes the row-1356 post-fill TBBO engineering registry in the active combined market-spread registry.

The runner validates the selected row back to the raw CSV with row-specific rules:

- row index must be `1356`;
- fill timestamp must be `2023-03-30T00:00:00Z`;
- selected quote timestamp must be `2023-03-30T00:00:00.099806785Z`;
- bid/ask must be `114.484375` / `114.5`;
- evidence type must be `ROW1356_FIRST_POST_FILL_TBBO_ENGINEERING_CONVENTION`;
- selection status must be `PASS_ROW1356_FIRST_POST_FILL_TBBO_ENGINEERING_QUOTE_SELECTED_NOT_RESULT`;
- label must remain not-book-explicit.

## Mechanical Continuation Result

The controlled 2023 TEST mechanical artifact run now supports rows `1` through `1363` and fails closed at row `1364`.

Run bundle:

```text
candidate_row_count: 1364
supported_mechanical_row_count: 1363
fail_closed_row_index: 1364
fail_closed_reason: FAIL_CLOSED_MARKET_ORDER_SPREAD_EVIDENCE_UNAVAILABLE_FOR_CONTINUATION_NOT_RESULT
run_manifest_hash: 8ca4df6b86891de852d2b0d3dd71b29990b945ab16e1ec2217511093cc0bb7bc
evidence_manifest_hash: 05b4924fc308c941a53651404be160f19c6039ba99836ae6a52738a4ae76d179
trusted_bundle_hash: 85f09cc4a2d8864486af164906ac8698cf10843908b212886c001b09e0971feb
bundle_hash: e6cb138af78d1c7532417e9d77f8f6a6a7710c3fd22c593bf4012335ef7cb9a6
```

Row `1356` emits deterministic local-only SELL 2 market-order/fill/cost/mechanical-PnL metadata:

```text
decision_timestamp_utc: 2023-03-29T23:00:00Z
fill_timestamp_utc: 2023-03-30T00:00:00Z
starting_position_contracts: 8
desired_position_contracts: 6
position_change_contracts: -2
order_side: SELL
fill_quantity: 2
fill_price: 114.484375
commission_amount: 4.6 USD
spread_cost_amount: 0.0 USD
total_cost_amount: 4.6 USD
market_cost_accounting_convention: BID_FILL_PRICE_WITH_NO_SEPARATE_SPREAD_COST
valuation_mark_timestamp_utc: 2023-03-30T01:00:00Z
valuation_mark_close_price: 114.4375
result_status: FAIL_CLOSED_RESULT_ROW_NOT_EMITTED_NOT_AUTHORIZED
backtest_status: FAIL_CLOSED_BACKTEST_RESULT_NOT_EMITTED_NOT_AUTHORIZED
source_faithful_evidence_claimed: FALSE
```

The row `1364` blocker is:

```text
raw_symbol: ZNM3
decision_timestamp_utc: 2023-03-30T07:00:00Z
fill_candidate_timestamp_utc: 2023-03-30T08:00:00Z
starting_position_contracts: 6
desired_position_contracts: 4
position_change_contracts: -2
order_side: SELL
fail_closed_reason: FAIL_CLOSED_MARKET_ORDER_SPREAD_EVIDENCE_UNAVAILABLE_FOR_CONTINUATION_NOT_RESULT
```

## Verification

Passed:

```text
python -m py_compile tools\databento\carver_s27_v2_2023_test_row1356_tbbo_engineering_convention_binding.py src\carver\spine\s27_v2_replay\test_mechanical_run.py
python -m py_compile tests\test_s27_v2_2023_test_mechanical_run.py src\carver\spine\s27_v2_replay\test_mechanical_run.py tools\databento\carver_s27_v2_2023_test_row1356_tbbo_engineering_convention_binding.py
```

The binding script returned:

```text
PASS_ROW1356_POST_FILL_TBBO_ENGINEERING_CONVENTION_BOUND_NOT_RESULT
selected_rows=1
```

Direct readback bundle validation passed:

```text
bundle_validate=PASS
supported=1363
fail=1364 FAIL_CLOSED_MARKET_ORDER_SPREAD_EVIDENCE_UNAVAILABLE_FOR_CONTINUATION_NOT_RESULT
```

Focused pytest was run for three existing TEST assertions. It rebuilt the artifacts and initially failed only because the expected active combined TBBO registry SHA had changed after adding row `1356`. The expected aggregate hash was updated from the prior registry hash to:

```text
bbdaca4acf36ba6fc0ed3a403f30658164ed645ab57104222404d3745c30f4f4
```

No full pytest PASS is claimed for this gate.

## Local Hostile Audit

Local hostile audit scope:

- exact row-1356 post-fill quote binding;
- preservation of the not-book-explicit engineering label;
- no provider/API/download/new data path in the binding/continuation gate;
- row-1356 SELL 2 market/fill/cost/PnL mechanical metadata;
- no spread double-counting under bid-fill accounting;
- row-1364 fail-closed boundary;
- result/backtest/source-faithful gates remain fail-closed.

Status:

```text
LOCAL_HOSTILE_AUDIT_PASS_NO_P0_P1_P2_P3_FINDINGS
```

The spawned read-only local hostile-audit subagent returned:

```text
No P0/P1/P2/P3 findings.
```

## Current Status

```text
LOCAL_PASS_ROW1356_POST_FILL_TBBO_ENGINEERING_BOUND_AND_CONTINUED_TO_ROW1364_MARKET_SPREAD_BLOCKER_NOT_RESULT
```

The next useful gate is bounded TBBO spread evidence for row `1364` under the standing bounded market-order TBBO policy, or a consolidated missing-market-order TBBO acquisition if row `1364` is part of a broader deterministic requirements ledger.

Provider/API access remains unauthorized unless separately and explicitly bounded to listed quote windows. Git, GPT packet preparation, protected-window access, result interpretation, PnL evaluation beyond mechanical construction, tuning, source-faithful evidence claims, adapter/deployment/trading/promotion, and promotion remain unauthorized.
