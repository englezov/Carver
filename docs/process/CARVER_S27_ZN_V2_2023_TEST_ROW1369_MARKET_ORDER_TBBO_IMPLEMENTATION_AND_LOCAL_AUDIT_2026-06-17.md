# S27_V2 2023 TEST Row 1369 Market-Order TBBO Implementation And Local Audit

Date: 2026-06-17

Status:

```text
LOCAL_PASS_ROW1369_BOUNDED_TBBO_BOUND_AND_CONTINUED_TO_ROW1370_MARKET_SPREAD_BLOCKER_NOT_RESULT
```

## Authorization

Operator authorized `S27_V2 2023 TEST row-1369 bounded market-order TBBO evidence and mechanical continuation gate`, limited to already-local 2023 TEST artifacts and bounded DataBento TBBO evidence around the row-1369 ZNM3 market-order blocker only.

No provider/API access outside the bounded row-1369 TBBO quote window was authorized. No downloads or new data acquisition outside that window, broader TEST continuation beyond the next blocker, VALIDATION, OOS, Lockbox, Forward, result interpretation, PnL evaluation beyond mechanical construction, tuning, adapter/deployment/trading/promotion, Git actions, GPT packet preparation, or source-faithful evidence claim was authorized.

## TBBO Evidence

Tool added and executed:

```text
tools/databento/carver_s27_v2_2023_test_row1369_market_spread_tbbo_acquisition.py
```

The tool locks to the active fail-closed row `1369` before requesting provider data and refuses duplicate raw outputs.

Bounded request:

```text
row_index: 1369
raw_symbol: ZNM3
schema: tbbo
request_start_utc: 2023-03-30T12:59:55Z
request_end_utc: 2023-03-30T13:00:05Z
```

Evidence status:

```text
PASS_ROW1369_BOUNDED_DATABENTO_TBBO_SELECTED_NOT_RESULT
```

Selected quote:

```text
selected_quote_ts_event: 2023-03-30T12:59:58.996330651Z
quote_age_seconds: 1.0036700000000001
bid_px_00: 114.3125
ask_px_00: 114.328125
selected_executable_market_fill_price: 114.3125
executable_market_fill_price_source: BID_PRICE_FOR_SELL_MARKET_ORDER
spread_points: 0.015625
selected_spread_row_hash: 0d8704ac17bcf659aed916eedf787ec6eeda47d126439e2efc742dc6aecaf7c3
selected_spread_registry_sha256: 26AA19744051CA638AD89572EDBA61175F326A770A91D9F1A2D92FC152CE5A80
raw_dbn_sha256: B254A30D90B7D389FE915042658EB6C3D9C1C5CDD749F3B4D032CB4883379D36
raw_csv_sha256: 2D8376F5449403A010A546C0DA846FC28B265623BB5EB4D81BD050C3B4C0787C
```

## Runner Binding

`src/carver/spine/s27_v2_replay/test_mechanical_run.py` was patched to include row `1369` in the active combined market-spread registry as:

```text
ROW1369_AT_OR_BEFORE_FILL_TBBO
```

Active combined registry binding:

```text
row_index: 1369
source_selected_spread_row_hash: 0d8704ac17bcf659aed916eedf787ec6eeda47d126439e2efc742dc6aecaf7c3
combined_registry_row_hash: 1b8b50fe5aed31312922f4d0bbc19e3c79e6dd6b8bf63aff90b43c7f4ba7f447
combined_registry_sha256: 325323e2994a2c50fa1c48128387a4bcfe7571ccf01c0f0894e65343334d065f
```

## Mechanical Continuation

The controlled 2023 TEST mechanical artifacts were rebuilt.

```text
candidate_row_count: 1370
supported_mechanical_row_count: 1369
fail_closed_row_index: 1370
fail_closed_reason: FAIL_CLOSED_MARKET_ORDER_SPREAD_EVIDENCE_UNAVAILABLE_FOR_CONTINUATION_NOT_RESULT
run_manifest_hash: 7844d2fd9b81e9fd1aa3263fd7f60c6efac4ad71fd1ec343c9aa9c408cea6af2
evidence_manifest_hash: 46853c1e77a218920a4fcd0d6b26cbd3aee80f8bd827b7b313e243e55cc886a8
trusted_bundle_hash: f6ad99000eea92510437bd9d1879dce7023629755bbd05c4295bdd7d2b11469b
run_bundle_hash: a5ff16732c454f69b9212525dd7a8757f7a767903983de1d3647fbded0f7f681
```

Row `1369` emitted deterministic local-only SELL 2 market-order/fill/cost/mechanical-PnL metadata:

```text
fill_timestamp_utc: 2023-03-30T13:00:00Z
fill_price: 114.3125
fill_price_provenance: MARKET_PRICE_FROM_SELECTED_TBBO_BID_AT_OR_BEFORE_NEXT_COMPLETED_CLOSE
commission_amount: 4.6
spread_cost_amount: 0.0
total_cost_amount: 4.6
market_cost_accounting_convention: BID_FILL_PRICE_WITH_NO_SEPARATE_SPREAD_COST
valuation_mark_timestamp_utc: 2023-03-30T14:00:00Z
valuation_mark_close_price: 114.390625
row_gross_pnl_amount: 218.75
row_net_pnl_amount: 214.15
ending_position_contracts: 4
result_status: FAIL_CLOSED_RESULT_ROW_NOT_EMITTED_NOT_AUTHORIZED
backtest_status: FAIL_CLOSED_BACKTEST_RESULT_NOT_EMITTED_NOT_AUTHORIZED
source_faithful_evidence_claimed: FALSE
```

The next blocker is row `1370`:

```text
row_index: 1370
decision_timestamp_utc: 2023-03-30T13:00:00Z
raw_symbol: ZNM3
starting_position_contracts: 4
desired_position_contracts: 8
position_change_contracts: 4
order_side: BUY
fill_candidate_timestamp_utc: 2023-03-30T14:00:00Z
fail_closed_reason: FAIL_CLOSED_MARKET_ORDER_SPREAD_EVIDENCE_UNAVAILABLE_FOR_CONTINUATION_NOT_RESULT
```

## Verification

Passed:

```text
python -m py_compile src\carver\spine\s27_v2_replay\test_mechanical_run.py tests\test_s27_v2_2023_test_mechanical_run.py tools\databento\carver_s27_v2_2023_test_row1369_market_spread_tbbo_acquisition.py
row-1369 acquisition selected_rows=1 failed_rows=0
direct bundle validation: bundle_validate=PASS supported=1369 fail=1370
direct row-1369 readback assertions: PASS
row1369_snapshot_manifest_check=PASS
row1369_direct_artifact_readback=PASS supported_boundary=1369 next_fail_row=1370
```

No pytest PASS is claimed for this gate.

## Local Hostile Audit

Local hostile audit scope:

- row-1369 bounded provider access limited to the active quote window;
- selected quote is fresh, non-crossed, at-or-before-fill, and side-correct for SELL bid fill;
- row-1369 registry/source hash binding;
- no spread double-counting under bid-fill accounting;
- row-1369 mechanical metadata emission;
- row-1370 fail-closed boundary;
- result/backtest/source-faithful gates remain fail-closed.

Initial local hostile audit status:

```text
LOCAL_HOSTILE_AUDIT_FAIL_P1_MUTABLE_FAIL_CLOSED_LEDGER_PROVENANCE_NOT_RESULT
```

The initial local hostile audit found no row arithmetic or forbidden-surface blocker, but raised one P1: the row-1369 request manifest declared the pre-continuation active `fail_closed_ledger.csv` hash while the live run directory had already advanced to the row-1370 fail-closed ledger. That made the provider-request authority dependent on a mutable artifact path.

Remediation:

```text
active_fail_closed_ledger_snapshot: docs/researchops/s27_v2_market_spread_evidence/ZN/20260617_2023_test_row1369_market_order_tbbo/manifest/20260617_S27_V2_2023_TEST_ROW1369_MARKET_ORDER_TBBO_active_fail_closed_ledger_snapshot.csv
active_fail_closed_ledger_snapshot_sha256: F61B67912744D6591D024829C53EA4D0872A16AE96AF35E6A578D3C24343C0B9
request_manifest_sha256_after_snapshot_binding: 54F9350304F3B05951958C68ED94BFA6B47A0C5A1647791CEE234A2F2F466EF8
```

`tools/databento/carver_s27_v2_2023_test_row1369_market_spread_tbbo_acquisition.py` now writes an active fail-closed snapshot before the provider request path and writes the snapshot with explicit bytes to avoid Windows newline translation drift.

Re-audit status:

```text
LOCAL_HOSTILE_REAUDIT_PASS_AFTER_P1_PROVENANCE_REMEDIATION_NO_P0_P1_P2_P3_FINDINGS
```

The re-audit verified that the snapshot bytes hash to `F61B67912744D6591D024829C53EA4D0872A16AE96AF35E6A578D3C24343C0B9`, the row-1369 selected TBBO quote/registry/combined hash remains bound, row `1369` emits the expected SELL 2 market/fill/cost/mechanical-PnL metadata, row `1370` remains the fail-closed blocker, and result/backtest/source-faithful gates remain fail-closed.

## Current Status

```text
LOCAL_PASS_ROW1369_BOUNDED_TBBO_BOUND_AND_CONTINUED_TO_ROW1370_MARKET_SPREAD_BLOCKER_AFTER_PROVENANCE_REMEDIATION_NOT_RESULT
```

The next useful gate is bounded TBBO spread evidence for row `1370` under the standing bounded market-order TBBO policy, or a consolidated deterministic requirements-ledger batch if row `1370` is part of a broader missing-TBBO set.

Provider/API access remains unauthorized unless separately and explicitly bounded to listed quote windows. Git, GPT packet preparation, protected-window access, result interpretation, tuning, source-faithful evidence claims, adapter/deployment/trading/promotion, and promotion remain unauthorized.
