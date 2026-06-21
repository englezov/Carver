# S27_V2 2023 TEST Row 1370 Market-Order TBBO Implementation And Local Audit

Date: 2026-06-20

Status:

```text
LOCAL_PASS_ROW1370_BOUNDED_TBBO_BOUND_AND_CONTINUED_TO_ROW1374_MARKET_SPREAD_BLOCKER_NOT_RESULT
```

## Authorization

Operator authorized `S27_V2 2023 TEST row-1370 bounded market-order TBBO evidence and mechanical continuation gate`, limited to already-local 2023 TEST artifacts and bounded DataBento TBBO evidence around the row-1370 ZNM3 market-order blocker only.

No provider/API access outside the bounded row-1370 TBBO quote window was authorized. No downloads or new data acquisition outside that window, broader TEST continuation beyond the next blocker, VALIDATION, OOS, Lockbox, Forward, result interpretation, PnL evaluation beyond mechanical construction, tuning, adapter/deployment/trading/promotion, Git actions, GPT packet preparation, or source-faithful evidence claim was authorized.

## TBBO Evidence

Tool added and executed:

```text
tools/databento/carver_s27_v2_2023_test_row1370_market_spread_tbbo_acquisition.py
```

The tool locks to the active fail-closed row `1370` before requesting provider data, writes an immutable active fail-closed snapshot, and refuses duplicate raw outputs.

Bounded request:

```text
row_index: 1370
raw_symbol: ZNM3
schema: tbbo
request_start_utc: 2023-03-30T13:59:55Z
request_end_utc: 2023-03-30T14:00:05Z
```

Evidence status:

```text
PASS_ROW1370_BOUNDED_DATABENTO_TBBO_SELECTED_NOT_RESULT
```

Selected quote:

```text
selected_quote_ts_event: 2023-03-30T13:59:59.466320757Z
quote_age_seconds: 0.53368000000000004
bid_px_00: 114.390625
ask_px_00: 114.40625
selected_executable_market_fill_price: 114.40625
executable_market_fill_price_source: ASK_PRICE_FOR_BUY_MARKET_ORDER
spread_points: 0.015625
source_selected_spread_row_hash: daa424db76a8ed89bf443f719ad2f9f7799858b980a94113d1edb82d940dc3a2
selected_spread_registry_sha256: 7C1AC865683EB5FE374EEE878BD38EEA4E0D715C5AA88F17D3E5AEFB73D75A86
raw_dbn_sha256: E0B088959911229986E1FF1949532B788954FB536221FD01FD2F340CFF420134
raw_csv_sha256: 7BC142FCE6CD62A8E0CF6549CD2F785E731D7CACB15976A2C4843A328C6AF2B9
active_fail_closed_ledger_snapshot_sha256: 280BDC64801670C113DFA467F29125A0689EB4C83C67A8A09E018DCC81FBFF5A
```

## Runner Binding

`src/carver/spine/s27_v2_replay/test_mechanical_run.py` was patched to include row `1370` in the active combined market-spread registry as:

```text
ROW1370_AT_OR_BEFORE_FILL_TBBO
```

Active combined registry binding:

```text
row_index: 1370
source_selected_spread_row_hash: daa424db76a8ed89bf443f719ad2f9f7799858b980a94113d1edb82d940dc3a2
combined_registry_row_hash: c5360ecad0ad1b2afef1decafa17ce630484078a60c5b54d1eeb23c336f7aae3
combined_registry_sha256: a247a6a81cb5b539ac99d5800a41b485c588227003d57feb03adafa73b538a13
```

## Mechanical Continuation

The controlled 2023 TEST mechanical artifacts were rebuilt and validated.

```text
candidate_row_count: 1374
supported_mechanical_row_count: 1373
fail_closed_row_index: 1374
fail_closed_reason: FAIL_CLOSED_MARKET_ORDER_SPREAD_EVIDENCE_UNAVAILABLE_FOR_CONTINUATION_NOT_RESULT
run_manifest_hash: c75b458928a722f0662d57788303377d391356302d1366134becace1d7e93dc6
evidence_manifest_hash: 9bab7d0a2446522cd42717f05c64ae6d3a9adc15493e7088fb49dd289fab1908
trusted_bundle_hash: f68c4dda14723ff4fc6f3224d7ce4fed0b7b89c23288aa27d39697df5a092f7c
run_bundle_hash: 2cbd0aefaef07b3ae0686bda0d0c8e9df0d5c828c36898a00198f7da81e6750e
```

Row `1370` emitted deterministic local-only BUY 4 market-order/fill/cost/mechanical-PnL metadata:

```text
fill_timestamp_utc: 2023-03-30T14:00:00Z
fill_price: 114.40625
fill_price_provenance: MARKET_PRICE_FROM_SELECTED_TBBO_ASK_AT_OR_BEFORE_NEXT_COMPLETED_CLOSE
commission_amount: 9.2
spread_cost_amount: 0.0
total_cost_amount: 9.2
market_cost_accounting_convention: ASK_FILL_PRICE_WITH_NO_SEPARATE_SPREAD_COST
valuation_mark_timestamp_utc: 2023-03-30T15:00:00Z
valuation_mark_close_price: 114.46875
row_gross_pnl_amount: 562.5
row_net_pnl_amount: 553.3
ending_position_contracts: 8
result_status: FAIL_CLOSED_RESULT_ROW_NOT_EMITTED_NOT_AUTHORIZED
backtest_status: FAIL_CLOSED_BACKTEST_RESULT_NOT_EMITTED_NOT_AUTHORIZED
source_faithful_evidence_claimed: FALSE
```

Rows `1371` through `1373` also became mechanically supported after row `1370` was unblocked. Row `1371` is an adjacent-limit filled row; rows `1372` and `1373` are non-market mechanical continuation rows.

The next blocker is row `1374`:

```text
row_index: 1374
decision_timestamp_utc: 2023-03-30T17:00:00Z
raw_symbol: ZNM3
starting_position_contracts: 7
desired_position_contracts: 5
position_change_contracts: -2
order_side: SELL
fill_candidate_timestamp_utc: 2023-03-30T18:00:00Z
fail_closed_reason: FAIL_CLOSED_MARKET_ORDER_SPREAD_EVIDENCE_UNAVAILABLE_FOR_CONTINUATION_NOT_RESULT
```

## Verification

Passed:

```text
python -m py_compile src\carver\spine\s27_v2_replay\test_mechanical_run.py tests\test_s27_v2_2023_test_mechanical_run.py tools\databento\carver_s27_v2_2023_test_row1370_market_spread_tbbo_acquisition.py
row-1370 acquisition selected_rows=1 failed_rows=0
bundle_validate=PASS candidate=1374 supported=1373 fail=1374
row1370_focused_artifact_verification=PASS
```

No full pytest PASS is claimed for this gate.

## Local Hostile Audit

Local hostile audit returned:

```text
PASS_WITH_NON_BLOCKING_P3_DATE_TYPO_REMEDIATED
```

Findings:

```text
P0: none
P1: none
P2: none
P3: row-1370 evidence process-record template initially emitted Date: 2026-06-17 instead of 2026-06-20; remediated in the tool and generated process record.
```

The audit confirmed bounded provider access, active fail-closed snapshot/hash binding, fresh/non-crossed at-or-before-fill BUY ask quote selection, row-1370 combined registry binding, ask-fill/no-separate-spread accounting, result/backtest/source-faithful fail-closed gates, row-1374 boundary, and no forbidden provider/API/download/new data/protected-window/Git/tuning/adapter/deployment/trading/promotion/source-faithful surface beyond the authorized bounded quote window.

## Current Status

```text
LOCAL_PASS_ROW1370_BOUNDED_TBBO_BOUND_AND_CONTINUED_TO_ROW1374_MARKET_SPREAD_BLOCKER_NOT_RESULT
```

The next useful gate is bounded TBBO spread evidence for row `1374` under the standing bounded market-order TBBO policy, or a consolidated deterministic requirements-ledger batch if row `1374` is part of a broader missing-TBBO set.

Provider/API access remains unauthorized unless separately and explicitly bounded to listed quote windows. Git, GPT packet preparation, protected-window access, result interpretation, tuning, source-faithful evidence claims, adapter/deployment/trading/promotion, and promotion remain unauthorized.
