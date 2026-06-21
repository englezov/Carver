# S27_V2 Pre-2023 Sell-Side/Reduction Development/Reconciliation Run Implementation

Date: 2026-06-11

Status:

```text
S27_V2_PRE2023_SELL_REDUCTION_DEVELOPMENT_RECON_RUN_EMITTED_NOT_RESULT
```

Authorization:

```text
S27_V2_LOCAL_ONLY_PRE2023_SELL_SIDE_REDUCTION_DEVELOPMENT_RECON_GATE
```

Artifact-bound authorization label:

```text
S27_V2_CONSOLIDATED_LOCAL_ONLY_PRE2023_SELL_REDUCTION_DEVELOPMENT_RECON_IMPLEMENTATION_AND_RUN_GATE
```

## Scope

This record covers the local-only pre-2023 sell-side/reduction Development/Reconciliation checkpoint after GPT 5.5 external PASS on the extended buy-side checkpoint.

The selected slice uses already-local pre-2023 ZN files only. It preserves 2023 for TEST. Pre-2022 data is used only as strict-prior warmup/evidence.

No provider/API access, downloads, new data acquisition, TEST, VALIDATION, OOS, Lockbox, Forward, result interpretation, PnL evaluation beyond mechanical row construction, tuning, adapter work, deployment, trading, promotion, Git action, or source-faithful evidence claim is authorized or performed by this record.

## Files

Code:

```text
tools/databento/carver_s27_v2_pre2023_sell_reduction_dev_recon_pack.py
src/carver/spine/s27_v2_replay/pre2023_sell_reduction_development_recon_run.py
tests/test_s27_v2_pre2023_sell_reduction_development_recon.py
```

Declared input pack:

```text
docs/researchops/s27_v2_local_replay_inputs/ZN/20260611_pre2023_sell_reduction_dev_recon_2022_first_reduction_declared_pack
```

Run artifact root:

```text
docs/researchops/s27_v2_local_replay_runs/ZN/20260611_pre2023_sell_reduction_dev_recon_2022_first_reduction_run
```

## Selection

Selection rule:

```text
MINIMUM_OLDEST_2022_SELL_REDUCTION_DEV_RECON_FIRST_REDUCTION_SEGMENT_AFTER_WARMUPS_PRESERVE_2023_FOR_TEST
```

The selected pack contains forty-four decision/fill/valuation triples from `2022-01-03T01:00:00Z` through the first carried-position reduction intent at `2022-01-24T01:00:00Z`.

Stop reason:

```text
FIRST_CARRIED_POSITION_REDUCTION_AT_2022-01-24T01:00:00Z_WITH_CURRENT_34_DESIRED_33
```

The final row is a sell-side intent row, not a filled reduction row.

## Sell-Side Boundary

Final row:

```text
row_index = 44
starting_position_contracts = 34
desired_position_contracts = 33
position_change_contracts = -1
order_side = SELL
order_quantity = 1
adjacent_target_position = 33
formula_limit_price = 130.03172667686832
limit_order_price = 130.046875
fill_candidate_close = 128.0625
fill_executed = FALSE
ending_position_contracts = 34
working_state_after = UNFILLED_LIMIT_ORDER_NOT_CARRIED_FAIL_CLOSED_WORKING_ORDER_LIFECYCLE
```

The sell limit is rounded conservatively upward to the next tick. The one-hour close-only sell-limit rule does not fill because the fill candidate close is below the sell limit. The unfilled working-order lifecycle is therefore explicitly fail-closed/not-carried for this Development/Reconciliation mechanics checkpoint.

## Pack Hashes

```text
611DF2F8A6AB08A2B2B62E39FDFC3FA883F0196A2A0FA9CE0572FAA1131045F6  S27_V2_PRE2023_SELL_REDUCTION_DEV_RECON_DECLARED_INPUT_PACK_MANIFEST.json
FD84BEBA1FB4BAF272A1AE483E0E36A43FEA84010E1E8383E9C6AF9F10AA6627  hourly_decision_completed_bar.csv
171D30772528D74B7FA296C2EC10183D6B74B7C61020BFDAD2C10EF24DDF06B2  hourly_fill_completed_bar.csv
156B24FDFDA78DAA0090BBF678DA2238A656C3D66FFEDB0A85253E733D89E1ED  valuation_mark_completed_bar.csv
546F1F4F136C0771ACF4708EFFF3CEB68739FC5E6F60BA1EE70AC80CFA775312  session_calendar.csv
```

## Run Summary

Mechanical ledger summary:

```text
row_count = 44
final_position_contracts = 34
cumulative_gross_pnl_amount = -74515.625
cumulative_commission_amount = 78.19999999999999
cumulative_spread_amount = 0.0
cumulative_net_pnl_amount = -74593.825
```

Run hashes:

```text
8cd3fcb3626522c27287e659ddd81c8a6ab4217ce6eb502ce07089f94bb617e8  internal bundle hash
2D01A1A3540CECAF34CE33CB4C915D012E3D1139A2354117735E9DE5223B62B6  run_bundle.json byte SHA256
FDA1EA56ACFA253C6804B15F8F018668904A1040B1CFD4879334BE9819F1708C  run_manifest.json
ED497B806447E3C6741E881C3ED5DE430B4147BA4D60D80491F83503DC8DE3C2  evidence_manifest.json
A7B29AA3652683B3FD38BAC1C1BA869938873D2C292145D91F246973B13EB978  trusted_bundle.json
```

## Verification

Commands:

```text
python -m py_compile tools\databento\carver_s27_v2_pre2023_sell_reduction_dev_recon_pack.py src\carver\spine\s27_v2_replay\pre2023_sell_reduction_development_recon_run.py
python -m pytest tests\test_s27_v2_pre2023_sell_reduction_development_recon.py -q
python -m pytest tests\test_s27_v2_pre2023_broader_development_recon.py tests\test_s27_v2_pre2023_extended_development_recon.py tests\test_s27_v2_pre2023_sell_reduction_development_recon.py -q
```

Results:

```text
py_compile PASS
20 passed
66 passed
```

## Non-Authorization

This checkpoint is local mechanical Development/Reconciliation ledger construction only. It is not a result-scored run, result interpretation, PnL evaluation beyond mechanical row construction, tuning evidence, promotion evidence, or source-faithful evidence claim.
