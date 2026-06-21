# S27_V2 2023 TEST Row 1366 Market-Order TBBO Implementation And Local Audit

Date: 2026-06-17

Status:

```text
LOCAL_PASS_ROW1366_BOUNDED_TBBO_BOUND_AND_CONTINUED_TO_ROW1369_MARKET_SPREAD_BLOCKER_NOT_RESULT
```

## Authorization

Operator authorized `S27_V2 2023 TEST row-1366 bounded market-order TBBO evidence and mechanical continuation gate`, limited to already-local 2023 TEST artifacts and bounded DataBento TBBO evidence around the row-1366 ZNM3 market-order blocker only.

No provider/API access outside the bounded row-1366 TBBO quote window was authorized. No downloads or new data acquisition outside that window, broader TEST continuation beyond the next blocker, VALIDATION, OOS, Lockbox, Forward, result interpretation, PnL evaluation beyond mechanical construction, tuning, adapter/deployment/trading/promotion, Git actions, GPT packet preparation, or source-faithful evidence claim was authorized.

## TBBO Evidence

Tool added and executed:

```text
tools/databento/carver_s27_v2_2023_test_row1366_market_spread_tbbo_acquisition.py
```

The tool locks to the active fail-closed row `1366` before requesting provider data and refuses duplicate raw outputs.

Bounded request:

```text
row_index: 1366
raw_symbol: ZNM3
schema: tbbo
request_start_utc: 2023-03-30T09:59:55Z
request_end_utc: 2023-03-30T10:00:05Z
```

Evidence status:

```text
PASS_ROW1366_BOUNDED_DATABENTO_TBBO_SELECTED_NOT_RESULT
```

Selected quote:

```text
selected_quote_ts_event: 2023-03-30T09:59:58.009461457Z
quote_age_seconds: 1.9905390000000001
bid_px_00: 114.453125
ask_px_00: 114.46875
selected_executable_market_fill_price: 114.46875
executable_market_fill_price_source: ASK_PRICE_FOR_BUY_MARKET_ORDER
spread_points: 0.015625
selected_spread_row_hash: 44b57413135ca3df40b98fa511e2b2e918458e375cd07ab61b2b4d62f71ed70c
selected_spread_registry_sha256: 3C547F2965A6B6451112C6C2FACA00004240E389C33C1E94E556B78FE28F08F0
raw_dbn_sha256: 7E21D32C0F815558A0ED1D8F59D21663B016B3CD3CFD8E61C163ECFE199CB9A2
raw_csv_sha256: 7B5F3DA3592001257DA0F458EF0A234ACF8A42AA2CF4276D9A029321F75A9BEB
```

## Runner Binding

`src/carver/spine/s27_v2_replay/test_mechanical_run.py` was patched to include row `1366` in the active combined market-spread registry as:

```text
ROW1366_AT_OR_BEFORE_FILL_TBBO
```

Active combined registry binding:

```text
row_index: 1366
source_selected_spread_row_hash: 44b57413135ca3df40b98fa511e2b2e918458e375cd07ab61b2b4d62f71ed70c
combined_registry_row_hash: ee5b5d7473e19018e90ec87261355c89fe16bd2a25fcbd44e29f9208e1339fa6
combined_registry_sha256: fccd09f5033064d97e5d950494a4ded064ded795092b650fd499ac3d6b70819f
```

## Mechanical Continuation

The controlled 2023 TEST mechanical artifacts were rebuilt.

```text
candidate_row_count: 1369
supported_mechanical_row_count: 1368
fail_closed_row_index: 1369
fail_closed_reason: FAIL_CLOSED_MARKET_ORDER_SPREAD_EVIDENCE_UNAVAILABLE_FOR_CONTINUATION_NOT_RESULT
run_manifest_hash: 0d387c78de89aa5c6dc8bc57c9f48b6d56a182f073cc8f92fed115d5f9a46322
evidence_manifest_hash: 2e2f370b0db26b5edfa3d42ce7b9db04888f3db271de39a1290689e574a5a1f2
trusted_bundle_hash: f9b75188ad02fe4b602c68fe61aca8debaa7a5388732079005bff41af11d663a
run_bundle_hash: 5d3374a5f8d738e3b9aa29fe702c71fdc1802371b31c801a1eaca568e229b553
```

Row `1366` emitted deterministic local-only BUY 2 market-order/fill/cost/mechanical-PnL metadata:

```text
fill_timestamp_utc: 2023-03-30T10:00:00Z
fill_price: 114.46875
fill_price_provenance: MARKET_PRICE_FROM_SELECTED_TBBO_ASK_AT_OR_BEFORE_NEXT_COMPLETED_CLOSE
commission_amount: 4.6
spread_cost_amount: 0.0
total_cost_amount: 4.6
market_cost_accounting_convention: ASK_FILL_PRICE_WITH_NO_SEPARATE_SPREAD_COST
valuation_mark_timestamp_utc: 2023-03-30T11:00:00Z
valuation_mark_close_price: 114.484375
row_gross_pnl_amount: 156.25
row_net_pnl_amount: 151.65
ending_position_contracts: 6
result_status: FAIL_CLOSED_RESULT_ROW_NOT_EMITTED_NOT_AUTHORIZED
backtest_status: FAIL_CLOSED_BACKTEST_RESULT_NOT_EMITTED_NOT_AUTHORIZED
source_faithful_evidence_claimed: FALSE
```

Rows `1367` and `1368` emitted no-market/no-cost mechanical continuation rows. The next blocker is row `1369`:

```text
row_index: 1369
decision_timestamp_utc: 2023-03-30T12:00:00Z
raw_symbol: ZNM3
starting_position_contracts: 6
desired_position_contracts: 4
position_change_contracts: -2
order_side: SELL
fill_candidate_timestamp_utc: 2023-03-30T13:00:00Z
fail_closed_reason: FAIL_CLOSED_MARKET_ORDER_SPREAD_EVIDENCE_UNAVAILABLE_FOR_CONTINUATION_NOT_RESULT
```

## Verification

Passed:

```text
python -m py_compile src\carver\spine\s27_v2_replay\test_mechanical_run.py tests\test_s27_v2_2023_test_mechanical_run.py tools\databento\carver_s27_v2_2023_test_row1366_market_spread_tbbo_acquisition.py
row-1366 acquisition selected_rows=1 failed_rows=0
direct bundle validation: bundle_validate=PASS supported=1368 fail=1369
direct row-1366 readback assertions: PASS
```

Focused pytest was attempted:

```text
python -m pytest tests\test_s27_v2_2023_test_mechanical_run.py -k "pack_is_declared or mechanical_run_fails_closed or row547_cap_bound" -q
```

It timed out after 900 seconds, so no pytest PASS is claimed for this gate.

## Local Hostile Audit

Local hostile audit scope:

- row-1366 bounded provider access limited to the active quote window;
- selected quote is fresh, non-crossed, at-or-before-fill, and side-correct for BUY ask fill;
- row-1366 registry/source hash binding;
- no spread double-counting under ask-fill accounting;
- row-1366 mechanical metadata emission;
- row-1369 fail-closed boundary;
- result/backtest/source-faithful gates remain fail-closed.

Status:

```text
LOCAL_HOSTILE_AUDIT_PASS_NO_P0_P1_P2_P3_FINDINGS
```

Local hostile audit result:

```text
P0 findings: none
P1 findings: none
P2 findings: none
P3 findings: none
```

The local hostile audit verified row-1366 bounded provider acquisition, selected BUY ask quote binding at `2023-03-30T09:59:58.009461457Z`, raw bounded-window evidence, source selected row hash to combined registry hash binding, ask-fill/no-separate-spread accounting, row-1366 market/fill/cost/mechanical-PnL metadata, row-1369 fail-closed continuation, and result/backtest/source-faithful fail-closed gates. It found no Git/GPT/protected-window/forbidden-surface use.

## Current Status

```text
LOCAL_PASS_ROW1366_BOUNDED_TBBO_BOUND_AND_CONTINUED_TO_ROW1369_MARKET_SPREAD_BLOCKER_NOT_RESULT
```

The next useful gate is bounded TBBO spread evidence for row `1369` under the standing bounded market-order TBBO policy, or a consolidated deterministic requirements-ledger batch if row `1369` is part of a broader missing-TBBO set.

Provider/API access remains unauthorized unless separately and explicitly bounded to listed quote windows. Git, GPT packet preparation, protected-window access, result interpretation, tuning, source-faithful evidence claims, adapter/deployment/trading/promotion, and promotion remain unauthorized.
