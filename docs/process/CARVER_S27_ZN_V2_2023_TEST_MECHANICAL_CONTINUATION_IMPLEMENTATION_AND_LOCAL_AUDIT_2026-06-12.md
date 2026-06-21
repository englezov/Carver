# S27_V2 2023 TEST Mechanical Continuation Implementation And Local Audit

Date: 2026-06-12

Status:

```text
LOCAL_PASS_PENDING_GPT55_EXTERNAL_AUDIT_NOT_RESULT
```

## Authorization

Operator authorized:

```text
S27_V2 controlled local-only 2023 TEST mechanical continuation gate
```

Scope is limited to already-local 2023 ZN TEST input files and audited S27_V2 machinery after GPT 5.5 PASS on the row-1 market-order actual-PnL machine-freeze P2 remediation.

This remains mechanical artifact construction only. It does not authorize result interpretation, performance evaluation, tuning, source-faithful evidence claims, promotion, deployment, trading, Git actions, provider/API access, downloads, new data, VALIDATION, OOS, Lockbox, or Forward.

## Implementation Summary

Patched:

```text
src/carver/spine/s27_v2_replay/test_mechanical_run.py
tests/test_s27_v2_2023_test_mechanical_run.py
```

The TEST pack builder and runner now treat the GPT-passed row-1 full-gap market order as a supported mechanical row, then continue to the next selected completed bar.

The row-1 path remains bound to the previously audited bounded DataBento TBBO evidence:

```text
row_index = 1
decision_timestamp_utc = 2023-01-03T00:00:00Z
raw_symbol = ZNH3
starting_position_contracts = 0
desired_position_contracts = 2
position_change_contracts = 2
order_side = BUY
order_quantity = 2
fill_timestamp_utc = 2023-01-03T01:00:00Z
fill_price = 112.5625
valuation_mark_timestamp_utc = 2023-01-03T02:00:00Z
valuation_mark_close = 112.59375
commission = 4.6
spread = 0.0
gross_pnl = 62.5
net_pnl = 57.9
```

The continuation stops at row 2 because the next target-position change is another full-gap market order, and no bounded TBBO spread evidence is authorized or bound for that non-row-1 market order:

```text
row_index = 2
decision_timestamp_utc = 2023-01-03T01:00:00Z
raw_symbol = ZNH3
starting_position_contracts = 2
desired_position_contracts = 0
position_change_contracts = -2
order_side = SELL
market_order_required = TRUE
market_order_rows_emitted = FALSE
fail_closed_reason = FAIL_CLOSED_MARKET_ORDER_SPREAD_EVIDENCE_UNAVAILABLE_FOR_CONTINUATION_NOT_RESULT
market_spread_cost_status = FAIL_CLOSED_BOUNDED_TBBO_SPREAD_EVIDENCE_REQUIRED_FOR_NON_ROW1_MARKET_ORDER
secondary_fail_closed_reason = MARKET_ORDER_CONTINUATION_REQUIRES_SEPARATE_BOUNDED_SPREAD_EVIDENCE
```

This prevents accidental reuse of row-1 TBBO spread evidence for later market orders.

## Artifact State

Input pack:

```text
docs/researchops/s27_v2_local_replay_inputs/ZN/20260612_2023_test_declared_pack
candidate_row_count = 2
supported_mechanical_row_count = 1
test_window_start = 2023-01-03T00:00:00Z
test_window_fail_closed_timestamp = 2023-01-03T01:00:00Z
```

Run output:

```text
docs/researchops/s27_v2_local_replay_runs/ZN/20260612_2023_test_mechanical_artifact_run
candidate_row_count = 2
supported_mechanical_row_count = 1
fail_closed_row_index = 2
final_position_contracts = 2
cumulative_gross_pnl_amount = 62.5
cumulative_commission_amount = 4.6
cumulative_spread_amount = 0.0
cumulative_net_pnl_amount = 57.9
```

Current key hashes:

```text
run_manifest_sha256 = 31042850DFC5CA93E8B7D9061C8F9CDD62658E7EB730F8E2F1681450E894DC47
evidence_manifest_sha256 = 39248EA18E145C61F464A734CA6ABFB6140E1AAC849F76C64398A35CA05F0D7E
trusted_bundle_sha256 = DE9F006D1D9656117367FDC0AFA550654032DF459662166ECD13BF375B8B611B
run_bundle_sha256 = B891720857E8A32311E790886079242AE08B6D72BBEA52F34BB2533750463F41
pnl_ledger_sha256 = 6B7BC481D4ACC7F55DAB766D174B2D91710F0EBC2C1A9A36D88D28AF7FF689BE
fail_closed_ledger_sha256 = B8455605B2795D26A495A245004DCDAE1CDEA8E3D4BF1C5BEBBA73DFFFD1A91B
SHA256SUMS_sha256 = 974037C2809DCC2816DB6FF9B1FA2BDB49EB6AF2BC0BCBC6A9EF0A3D564A97FF
```

## Verification

Focused verification passed:

```text
python -m py_compile src\carver\spine\s27_v2_replay\test_mechanical_run.py src\carver\spine\s27_v2_replay\pretest_machine_freeze.py tests\test_s27_v2_2023_test_mechanical_run.py
python -m pytest tests\test_s27_v2_2023_test_mechanical_run.py -q
35 passed
python -m pytest tests\test_s27_v2_pretest_development_recon_completion.py tests\test_s27_v2_2023_test_mechanical_run.py -q
96 passed
```

## Local Hostile Audit Finding And Patch

Two read-only local hostile-audit subagents initially found the same P2:

```text
P2_STALE_SUPPORTED_MARKET_ROW_VALIDATION_AFTER_CONTINUATION
```

Finding:

- actual artifacts were correct;
- row 1 remained supported as the audited `BUY 2` market-order/TBBO/cost/PnL row;
- row 2 correctly fail-closed before another unaudited market order;
- however, `TestMechanicalRunBundle.validate()` only checked row-1 market/TBBO/cost bindings when `fail_closed_reason == FAIL_CLOSED_RESULT_NOT_AUTHORIZED_AFTER_MARKET_ORDER_PNL_EMITTED_NOT_RESULT`;
- after continuation, the terminal fail reason became `FAIL_CLOSED_MARKET_ORDER_SPREAD_EVIDENCE_UNAVAILABLE_FOR_CONTINUATION_NOT_RESULT`, so that post-hoc validation block was stale.

Patch:

- supported market rows are now validated whenever `market_order_ledger.csv` or `market_fill_metadata_ledger.csv` has rows, independent of the later fail-closed reason;
- row-1 market order remains locked to `BUY 2`;
- row-1 market fill remains locked to quantity `2` and position after fill `2`;
- row-1 cost remains locked to selected TBBO row hash `c910df21177b2e1aa0cfcd5edadd03be38f130e8b06cb8f4b2bca79bf8390d0b`;
- row-1 cost remains locked to selected TBBO ledger hash `c3a2a0bdd59e03e8c362f63d791b870609d1af1177144d7e78406daec6ca8343`;
- row-1 spread cost remains `0.0` under `ASK_FILL_PRICE_WITH_NO_SEPARATE_SPREAD_COST`.

Regression tests now reject forged:

- market-order quantity;
- market-fill target position;
- selected TBBO row hash;
- selected TBBO ledger hash;
- row-1 spread cost.

Local hostile re-audit found the altered-row half closed but identified a remaining omission bypass:

- both `market_order_ledger.csv` and `market_fill_metadata_ledger.csv` could be header-only while `no_market_order_ledger.csv` still claimed `market_order_required = TRUE` and `market_order_rows_emitted = TRUE`;
- evidence-manifest ledger hashes were not yet directly checked against current artifact bytes during bundle validation.

Second patch:

- `TestMechanicalRunBundle.validate()` now validates every evidence-manifest `ledger_hashes` entry against current artifact bytes;
- it reads `no_market_order_ledger.csv` and requires supported row count binding;
- it derives emitted market row indices from `no_market_order_ledger.csv`;
- emitted market indices must match `market_order_ledger.csv`, `market_fill_metadata_ledger.csv`, and same-row `cost_ledger.csv`;
- self-consistent omission of both market ledgers is rejected;
- current-byte artifact mutation is rejected through evidence-manifest hash binding;
- self-consistent market-order quantity forgery remains rejected.

Additional regression tests cover:

- current-byte mutation with stale evidence ledger hash;
- self-consistent omission of both supported market ledgers;
- self-consistent row-1 market-order quantity forgery.

## Current Status

```text
LOCAL_PASS_PENDING_GPT55_EXTERNAL_AUDIT_NOT_RESULT
```

Final local hostile re-audit returned:

```text
PASS_NO_P0_P1_P2
```

Both read-only local hostile-audit subagents confirmed that the stale validation-boundary P2, evidence-hash omission path, and self-consistent no-market downgrade plus market-ledger omission path are closed.

The next useful step is a GPT 5.5 external hostile-audit packet for this two-row TEST mechanical continuation checkpoint.

## Non-Authorizations

This record does not authorize provider/API access, downloads, new data acquisition, VALIDATION, OOS, Lockbox, Forward, result interpretation, PnL evaluation beyond mechanical row construction, tuning, adapter work, deployment, trading, promotion, Git actions, or source-faithful evidence claims.
