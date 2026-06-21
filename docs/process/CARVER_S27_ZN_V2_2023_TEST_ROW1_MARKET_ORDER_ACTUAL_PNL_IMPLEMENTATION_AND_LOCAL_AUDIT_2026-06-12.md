# S27 V2 2023 TEST Row 1 Market Order Actual PnL Implementation And Local Audit

Date: 2026-06-12

Status:

```text
LOCAL_PASS_ROW1_MARKET_ORDER_MECHANICAL_PNL_EMITTED_NOT_RESULT
```

## Scope

Operator authorized a narrow local-only S27_V2 TEST row-1 actual PnL mechanical ledger gate after GPT 5.5 PASS on the row-1 market-order actual-cost packet.

This gate is limited to the audited 2023 TEST row-1 `BUY 2` market fill and audited actual cost row. It does not authorize broader TEST continuation, result interpretation, PnL evaluation beyond mechanical row construction, source-faithful evidence claims, provider/API access, downloads, new data, Git actions, tuning, adapter work, deployment, trading, or promotion.

## Bound Inputs

The row-1 inputs are already declared local TEST pack rows:

```text
decision_timestamp = 2023-01-03T00:00:00Z
fill_timestamp = 2023-01-03T01:00:00Z
valuation_mark_timestamp = 2023-01-03T02:00:00Z
raw_symbol = ZNH3
order_side = BUY
fill_quantity = 2
fill_price = 112.5625
valuation_mark_close = 112.59375
valuation_convention_label = SOURCE_NATIVE_ENGINEERING_VALUATION_ASSUMPTION_NOT_BOOK_EXPLICIT
audited_total_cost = 4.6 USD
```

The valuation convention remains engineering/local-only and not book-explicit source-faithful evidence.

## Implementation

Patched files:

```text
src/carver/spine/s27_v2_replay/test_mechanical_run.py
src/carver/spine/s27_v2_replay/pretest_machine_freeze.py
tests/test_s27_v2_2023_test_mechanical_run.py
```

The row-1 market-order branch now emits:

- runtime evidence metadata row;
- forecast metadata row;
- desired-position metadata row;
- market-order plan row, with limit-order fields `NOT_APPLICABLE_MARKET_ORDER_FULL_GAP`;
- locked market-order execution status row;
- working-order transition row;
- market-order fill row;
- already-audited actual cost row;
- one mechanical PnL row;
- validation metadata row;
- terminal fail-closed row preventing result/backtest/source-faithful evidence.

The shared machine-freeze guard was tightened for market-order rows. `LOCKED_MARKET_ORDER_EXECUTED_FULL_GAP` is accepted only if:

- market order is required and emitted;
- `abs(position_change_contracts) > 1`;
- order quantity equals the full position gap;
- fill quantity equals the full position gap;
- fill is executed;
- same-session/working-state guards still pass.

## Mechanical PnL Row

Run artifact:

```text
docs/researchops/s27_v2_local_replay_runs/ZN/20260612_2023_test_mechanical_artifact_run/pnl_ledger.csv
```

Emitted row:

```text
row_index = 1
valuation_mark_timestamp_utc = 2023-01-03T02:00:00Z
valuation_mark_close_price = 112.59375
valuation_convention_label = SOURCE_NATIVE_ENGINEERING_VALUATION_ASSUMPTION_NOT_BOOK_EXPLICIT
existing_position_gross_pnl = 0.0
fill_gross_pnl = 62.5
row_gross_pnl_amount = 62.5
row_net_pnl_amount = 57.9
cumulative_gross_pnl_amount = 62.5
cumulative_commission_amount = 4.6
cumulative_spread_amount = 0.0
cumulative_net_pnl_amount = 57.9
ending_position_contracts = 2
result_status = FAIL_CLOSED_RESULT_ROW_NOT_EMITTED_NOT_AUTHORIZED
backtest_status = FAIL_CLOSED_BACKTEST_RESULT_NOT_EMITTED_NOT_AUTHORIZED
pnl_evaluation_status = MECHANICAL_PNL_ROW_CONSTRUCTION_ONLY_NOT_RESULT_INTERPRETATION
source_faithful_evidence_claimed = FALSE
row_status = LOCAL_MARKET_ORDER_MECHANICAL_PNL_ROW_EMITTED_NOT_RESULT
row_hash = ad92556f4411f1ab98bcda27e5be005dbe1b248f34a319e0fd4cb9f84f89c8e0
```

Arithmetic:

```text
signed_fill = +2
fill_gross_pnl = 2 * (112.59375 - 112.5625) * 1000 = 62.5
row_net_pnl = 62.5 - 4.6 = 57.9
```

## Refreshed Artifact Hashes

```text
pnl_ledger_sha256 = 6B7BC481D4ACC7F55DAB766D174B2D91710F0EBC2C1A9A36D88D28AF7FF689BE
fail_closed_ledger_sha256 = BCD3C1268C2639BB87CBBDF61FD602075C9ACF4A606E2253A3971CE24F83F07E
run_manifest_sha256 = EE76B0346D3A987AEA61DFA89689BAFBFE6313C2C1EDE261F0A5EB54A1888592
evidence_manifest_sha256 = AC78C254756F80CD93A519A0F9F1C7F844168506D24AEB9E0FAA231790817DD0
trusted_bundle_sha256 = 6BE6CDCA66634134C70E4F0734D3942B3B04750BBE5722C605C69D3DF405F901
run_bundle_sha256 = 7086948C4D059B75B167FA61CDF884FCBD3218B4FA0510832249BACF5DB3A807
SHA256SUMS_sha256 = 3DA4D46AE479DE924FC897F92F51333EDCFCC8D8BA18F5A8A7F840F9A2871F6A
```

The run bundle records:

```text
supported_mechanical_row_count = 1
fail_closed_row_index = 1
final_position_contracts = 2
cumulative_gross_pnl_amount = 62.5
cumulative_commission_amount = 4.6
cumulative_spread_amount = 0.0
cumulative_net_pnl_amount = 57.9
fail_closed_reason = FAIL_CLOSED_RESULT_NOT_AUTHORIZED_AFTER_MARKET_ORDER_PNL_EMITTED_NOT_RESULT
```

## Verification

Focused verification passed:

```text
python -m py_compile src\carver\spine\s27_v2_replay\test_mechanical_run.py src\carver\spine\s27_v2_replay\pretest_machine_freeze.py tests\test_s27_v2_2023_test_mechanical_run.py
python -m pytest tests\test_s27_v2_2023_test_mechanical_run.py -q
22 passed
python -m pytest tests\test_s27_v2_pretest_development_recon_completion.py tests\test_s27_v2_2023_test_mechanical_run.py -q
83 passed
```

## Local Hostile Audit

Two read-only local hostile-audit subagents were used.

PnL/hash-chain audit:

```text
PASS_NO_P0_P1_P2_P3
```

It verified:

- row-1 `BUY 2` market order;
- fill timestamp, quantity, price, and source row hash;
- valuation mark timestamp and close;
- audited cost binding;
- gross/net PnL arithmetic;
- ending position;
- result/backtest/source-faithful fail-closed statuses;
- pack, run, evidence, trusted, and bundle hash binding.

Boundary audit initially found one P2:

```text
P2_LOCKED_MARKET_ORDER_STATUS_NOT_BOUND_TO_FULL_GAP_AND_QUANTITY_PROOF
```

Patch:

- `pretest_machine_freeze.py` now requires locked market-order status to bind full-gap position change, order quantity, fill quantity, and executed fill;
- regression tests reject forged non-full-gap locked market-order status and mismatched full-gap quantity.

Post-patch verification:

```text
python -m pytest tests\test_s27_v2_2023_test_mechanical_run.py -q
22 passed
python -m pytest tests\test_s27_v2_pretest_development_recon_completion.py tests\test_s27_v2_2023_test_mechanical_run.py -q
83 passed
```

No remaining local P0/P1/P2 finding is known inside this gate.

## Current Status

```text
LOCAL_PASS_ROW1_MARKET_ORDER_MECHANICAL_PNL_PENDING_EXTERNAL_AUDIT_NOT_RESULT
```

Recommended next step is a GPT 5.5 narrow external hostile audit packet for the row-1 actual PnL mechanical ledger gate. Broader TEST continuation remains unauthorized until that audit passes and the operator separately authorizes continuation.
