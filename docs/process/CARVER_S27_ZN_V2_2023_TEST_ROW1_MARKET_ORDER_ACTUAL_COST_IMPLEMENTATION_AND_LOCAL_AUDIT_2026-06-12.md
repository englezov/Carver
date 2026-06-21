# S27 V2 2023 TEST Row 1 Market Order Actual Cost Implementation And Local Audit

Date: 2026-06-12

Status:

```text
LOCAL_PASS_MARKET_ORDER_ACTUAL_COST_EMITTED_NOT_PNL_NOT_RESULT
```

## Scope

Operator authorized a narrow local-only implementation gate for the audited 2023 TEST row-1 `BUY 2` market fill after bounded DataBento TBBO spread evidence PASS.

This gate is limited to cost-accounting convention binding and actual market-order cost-row emission for row 1 only.

Unauthorized in this gate:

- provider/API access beyond the already completed bounded TBBO evidence;
- downloads or new data acquisition;
- VALIDATION, OOS, Lockbox, or Forward access;
- broader TEST continuation;
- actual PnL/result emission;
- result interpretation or PnL evaluation;
- tuning;
- adapter work;
- deployment, trading, or promotion;
- Git actions;
- source-faithful evidence claims.

## Bound TBBO Evidence

Selected bounded DataBento TBBO evidence:

```text
source_root = docs/researchops/s27_v2_market_spread_evidence/ZN/20260612_2023_test_row1_znh3_tbbo
selected_quote_ts_event = 2023-01-03T00:59:57.009985Z
raw_symbol = ZNH3
bid = 112.546875
ask = 112.5625
full_spread_points = 0.015625
point_value_usd = 1000.0
full_spread_value_per_contract = 15.625
row1_quantity = 2
selected_row_hash = c910df21177b2e1aa0cfcd5edadd03be38f130e8b06cb8f4b2bca79bf8390d0b
selected_spread_ledger_sha256 = C3A2A0BDD59E03E8C362F63D791B870609D1AF1177144D7E78406DAEC6CA8343
```

The audited market-fill metadata price is `112.5625`, which equals the selected TBBO ask.

## Accounting Convention

Chosen convention:

```text
ASK_FILL_PRICE_WITH_NO_SEPARATE_SPREAD_COST
```

Rationale:

The market fill price is already the selected ask. Charging a separate bid/ask spread cost on top of an ask fill would double count the spread for this local row-1 accounting surface.

This is a cost-accounting convention for local mechanical artifact construction. It is not a result interpretation, tuning decision, promotion evidence, or source-faithful evidence claim.

## Implementation

Patched file:

```text
src/carver/spine/s27_v2_replay/test_mechanical_run.py
```

Key behavior:

- loads the selected TBBO spread ledger from the bounded evidence directory;
- requires exactly the selected quote fields and row hash;
- requires the row-1 market fill price to equal the selected TBBO ask;
- emits one row-1 actual cost row for the market order;
- keeps PnL/result/backtest/source-faithful evidence fail-closed.

Focused test file:

```text
tests/test_s27_v2_2023_test_mechanical_run.py
```

The test now checks the actual cost row, TBBO evidence binding, no package-root export leak, and fail-closed PnL/result boundary.

## Emitted Cost Row

Run artifact root:

```text
docs/researchops/s27_v2_local_replay_runs/ZN/20260612_2023_test_mechanical_artifact_run
```

Cost ledger:

```text
cost_ledger_sha256 = 2B66C192BFE70585356FAAED688DCFD1D3FF7FCFA111E31405C84F11091D8B7A
row_index = 1
cost_policy_id = S27_V2_ZN_ACCEPTED_INFERRED_RETAIL_FUTURES_COST_2026_06_11
order_cost_type = MARKET_ORDER_BUY_ASK_FILL_ACTUAL_COST_NOT_PNL
commission_amount = 4.6
spread_cost_amount = 0.0
total_cost_amount = 4.6
currency = USD
market_cost_accounting_convention = ASK_FILL_PRICE_WITH_NO_SEPARATE_SPREAD_COST
spread_cost_reason = NO_SEPARATE_SPREAD_COST_BECAUSE_MARKET_FILL_PRICE_EQUALS_SELECTED_TBBO_ASK
tbbo_quote_ts_event = 2023-01-03T00:59:57.009985Z
tbbo_bid_px = 112.546875
tbbo_ask_px = 112.5625
tbbo_full_spread_points = 0.015625
tbbo_full_spread_value_per_contract = 15.625
tbbo_selected_spread_row_hash = c910df21177b2e1aa0cfcd5edadd03be38f130e8b06cb8f4b2bca79bf8390d0b
tbbo_selected_spread_ledger_sha256 = c3a2a0bdd59e03e8c362f63d791b870609d1af1177144d7e78406daec6ca8343
row_status = LOCAL_MARKET_ORDER_ACTUAL_COST_ROW_EMITTED_NOT_PNL_NOT_RESULT
row_hash = 1be6578237e8e9c10d9a0ed2560dc583827e7be96ed84e3d0a0eefca8314bd7d
```

Related refreshed artifact hashes:

```text
market_fill_metadata_ledger_sha256 = 68628061635976AB46FD89676BBF3E7270C0903E9054CE5176434D6581782779
fail_closed_ledger_sha256 = 8BEE579FC18EB564989B594AB20845C363F52A90BE6277BDEA3FF8F985CD929A
run_manifest_sha256 = D6731B2A4FFB9333713244ED53C37B8B42F25396FF346185EC8BC2F7F4DCEC8A
evidence_manifest_sha256 = D1D88BF84645ECAAEE53C0DB8EADF1111612CFA957E47C819D7415BE8761C384
trusted_bundle_sha256 = F5910E4768B119ED17BA57280408DF7EB2E1FCB653B7415CC8C4CA0AE4932C35
```

## Fail-Closed Boundary

The row-1 fail-closed ledger now records:

```text
market_order_rows_emitted = TRUE
market_fill_metadata_rows_emitted = TRUE
market_spread_cost_status = PASS_DATABENTO_TBBO_ASK_FILL_NO_SEPARATE_SPREAD_COST_NOT_PNL
secondary_fail_closed_reason = MARKET_ORDER_FILL_AND_ACTUAL_COST_EMITTED_PNL_RESULT_FAIL_CLOSED_NOT_AUTHORIZED
fail_closed_reason = FAIL_CLOSED_PNL_RESULT_NOT_AUTHORIZED_AFTER_MARKET_ORDER_COST_EMITTED_NOT_RESULT
result_status = FAIL_CLOSED_RESULT_ROW_NOT_EMITTED_NOT_AUTHORIZED
backtest_status = FAIL_CLOSED_BACKTEST_RESULT_NOT_EMITTED_NOT_AUTHORIZED
source_faithful_evidence_claimed = FALSE
```

No actual PnL ledger row, result row, validation result row, broader TEST continuation, or source-faithful evidence claim is emitted by this gate.

## Verification

Focused local verification passed:

```text
python -m py_compile src\carver\spine\s27_v2_replay\test_mechanical_run.py tests\test_s27_v2_2023_test_mechanical_run.py
python -m pytest tests\test_s27_v2_2023_test_mechanical_run.py -q
20 passed
python -m pytest tests\test_s27_v2_pretest_development_recon_completion.py tests\test_s27_v2_2023_test_mechanical_run.py -q
81 passed
```

The latest direct focused test rerun returned:

```text
python -m pytest tests\test_s27_v2_2023_test_mechanical_run.py -q
20 passed in 3.00s
```

## Local Hostile Audit

Two read-only local hostile-audit subagents returned PASS:

1. Cost-binding audit:
   - no P0/P1/P2/P3 findings;
   - verified selected TBBO quote fields;
   - verified the implementation requires fill price to equal selected ask;
   - verified `ASK_FILL_PRICE_WITH_NO_SEPARATE_SPREAD_COST`;
   - verified commission `4.6`, spread `0.0`, total `4.6`;
   - verified selected row hash and selected spread ledger SHA binding;
   - verified PnL/result fail-closed boundary.

2. Forbidden-surface and gate-boundary audit:
   - no P0/P1/P2/P3 findings;
   - verified no provider/API/download path in the runner;
   - verified protected-window exclusions;
   - verified row-1 bounded TEST continuation;
   - verified no PnL/result emission beyond headers;
   - verified no source-faithful evidence claim;
   - verified no package-root export leak;
   - verified fail-closed status after actual cost emission.

## Current Status

```text
LOCAL_PASS_MARKET_ORDER_ACTUAL_COST_EMITTED_PENDING_EXTERNAL_AUDIT_NOT_PNL_NOT_RESULT
```

Recommended next gate:

```text
S27_V2 GPT 5.5 external hostile audit packet for the locally passed TEST row-1 market-order actual-cost implementation
```

No PnL/result continuation, broader TEST continuation, Git action, or source-faithful evidence claim is authorized by this record.
