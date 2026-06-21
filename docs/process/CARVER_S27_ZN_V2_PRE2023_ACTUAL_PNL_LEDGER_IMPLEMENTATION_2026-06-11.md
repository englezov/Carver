# S27_V2 Pre-2023 Actual PnL Ledger Implementation

Date: 2026-06-11

Status:

```text
S27_V2_PRE2023_DEVELOPMENT_RECON_ACTUAL_PNL_LEDGER_EMITTED_NOT_RESULT
```

Authorization:

```text
S27_V2_PRE2023_DEVELOPMENT_RECON_ACTUAL_PNL_LEDGER_IMPLEMENTATION_GATE
```

Implementation files:

```text
src/carver/spine/s27_v2_replay/pre2023_development_recon_actual_pnl.py
tests/test_s27_v2_pre2023_actual_pnl.py
```

Input artifacts:

```text
controlled_run = docs/researchops/s27_v2_local_replay_runs/ZN/20260611_pre2023_oldest_dev_recon_2022_controlled_run
valuation_mark_pack = docs/researchops/s27_v2_local_replay_inputs/ZN/20260611_pre2023_dev_recon_valuation_mark_znh2_20220103T03_declared_pack
```

Output artifacts:

```text
docs/researchops/s27_v2_local_replay_runs/ZN/20260611_pre2023_oldest_dev_recon_2022_actual_pnl_completion
```

Bound input hashes:

```text
controlled_run_bundle_sha256 = 7668d2f2212d382355efc00ca80e2345e7418b32661fc4c4612ede9ef6a0ad30
fill_ledger_sha256 = 6f6fcec85335f550cb33ce5278051a152ee8bd9a872cc9dcaefdc535637c7d55
commission_ledger_sha256 = 310283aef814594dfd780c6576d11e1b37a0376a62a5200efc90dbae1116d560
spread_cost_ledger_sha256 = ee4dd7216c5fd6cb8a802fb1883a9cd4ec3b802cfe208b6fab2b091f885b65ba
valuation_mark_manifest_sha256 = 735955f1e44e1107dbc64dd786fe7af7b52f88f17b75c7bd91708933a9e5c159
valuation_mark_completed_bar_sha256 = 9aa8b3999a80058342c8e40236b2a926a500355d6d5fed6f6877de4147961031
valuation_mark_local_audit_sha256 = 2e98d465b1db6b097888f7962cb011199a24da138c190025b59a3b30f3cd7797
```

Mechanical row:

```text
raw_symbol = ZNH2
fill_timestamp_utc = 2022-01-03T02:00:00Z
valuation_mark_completed_timestamp_utc = 2022-01-03T03:00:00Z
filled_order_side = BUY
fill_quantity = 8
position_after_fill = 8
fill_price = 130.421875
valuation_mark_close_price = 130.296875
contract_point_value = 1000.0 USD per full point
gross_pnl_amount = -1000.0 USD
commission_cost_amount = 18.4 USD
spread_cost_amount = 0.0 USD
total_cost_amount = 18.4 USD
net_pnl_amount = -1018.4 USD
```

Valuation convention:

```text
SOURCE_NATIVE_ENGINEERING_VALUATION_ASSUMPTION_NOT_BOOK_EXPLICIT
NEXT_COMPLETED_HOURLY_CLOSE_AFTER_FILL
```

The PnL row is mechanical local Development/Reconciliation ledger construction
only. It is not a result row, not a result-scored run, not result
interpretation, not PnL evaluation beyond mechanical row construction, and not
a source-faithful evidence claim.

Output hashes:

```text
actual_pnl_bundle_hash = 409ebaed618fd15bafb523a0b9c57fd38a54ca0110be04cf54925efda6a28349
actual_pnl_row_hash = 0a7a0b65997c643b63ca47b215d42c04466f83e19921defaad2bdb25812ba0f6
trusted_bundle_evidence_manifest_hash = a21766e2728d0a60caed54ef1f7a9278fe9ee598cdcff1dbe63c7b19c69d5c7b
```

Verification:

```text
python -m py_compile src\carver\spine\s27_v2_replay\pre2023_development_recon_actual_pnl.py
python -m pytest tests\test_s27_v2_pre2023_actual_pnl.py tests\test_s27_v2_pre2023_valuation_mark_pack.py tests\test_s27_v2_development_recon_run.py -q
72 passed
```

Non-authorizations preserved:

```text
NO_PROVIDER_API
NO_DOWNLOADS
NO_NEW_DATA_ACQUISITION
NO_TEST_ACCESS
NO_VALIDATION_ACCESS
NO_OOS
NO_LOCKBOX
NO_FORWARD
NO_RESULT_SCORED_RUN
NO_RESULT_INTERPRETATION
NO_PNL_EVALUATION_BEYOND_MECHANICAL_ROW_CONSTRUCTION
NO_TUNING
NO_ADAPTER_WORK
NO_DEPLOYMENT
NO_TRADING
NO_PROMOTION
NO_GIT_ACTIONS
NO_SOURCE_FAITHFUL_EVIDENCE_CLAIM
```

Next step:

```text
LOCAL_HOSTILE_AUDIT_OF_PRE2023_ACTUAL_PNL_LEDGER_IMPLEMENTATION
```

This implementation record does not authorize provider/API access, downloads,
new data acquisition, TEST, VALIDATION, OOS, Lockbox, Forward, result
interpretation, PnL evaluation beyond mechanical row construction, tuning,
adapter work, deployment, trading, promotion, Git actions, or source-faithful
evidence claims.
