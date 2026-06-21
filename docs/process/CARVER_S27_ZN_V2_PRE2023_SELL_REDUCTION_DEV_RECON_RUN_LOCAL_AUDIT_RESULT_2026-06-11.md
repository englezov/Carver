# S27_V2 Pre-2023 Sell-Side/Reduction Development/Reconciliation Run Local Audit Result

Date: 2026-06-11

Status:

```text
LOCAL_HOSTILE_AUDIT_PASS
```

Scope:

```text
S27_V2 local-only pre-2023 sell-side/reduction Development/Reconciliation run gate
```

Artifacts audited:

```text
tools/databento/carver_s27_v2_pre2023_sell_reduction_dev_recon_pack.py
src/carver/spine/s27_v2_replay/pre2023_sell_reduction_development_recon_run.py
tests/test_s27_v2_pre2023_sell_reduction_development_recon.py
docs/researchops/s27_v2_local_replay_inputs/ZN/20260611_pre2023_sell_reduction_dev_recon_2022_first_reduction_declared_pack
docs/researchops/s27_v2_local_replay_runs/ZN/20260611_pre2023_sell_reduction_dev_recon_2022_first_reduction_run
docs/process/CARVER_S27_ZN_V2_PRE2023_SELL_REDUCTION_DEV_RECON_RUN_IMPLEMENTATION_2026-06-11.md
```

## Local Audit Summary

Two read-only hostile subagents were run.

Governance/window audit:

```text
PASS_NO_P0_P1_P2_P3_FINDINGS
```

Mechanical ledger/hash audit:

```text
PASS_NO_P0_P1_P2_P3_FINDINGS
```

## Verified Boundary

The checkpoint reaches the first carried-position reduction intent:

```text
row_index = 44
starting_position_contracts = 34
desired_position_contracts = 33
position_change_contracts = -1
order_side = SELL
order_quantity = 1
adjacent_target_position = 33
limit_order_price = 130.046875
fill_candidate_close = 128.0625
fill_executed = FALSE
ending_position_contracts = 34
working_state_after = UNFILLED_LIMIT_ORDER_NOT_CARRIED_FAIL_CLOSED_WORKING_ORDER_LIFECYCLE
```

This proves sell-side order-intent generation and conservative no-fill/fail-closed lifecycle handling for the first sell-side reduction attempt. It does not claim a filled sell reduction.

## Hashes

Pack manifest SHA256:

```text
611DF2F8A6AB08A2B2B62E39FDFC3FA883F0196A2A0FA9CE0572FAA1131045F6
```

Run hashes:

```text
8cd3fcb3626522c27287e659ddd81c8a6ab4217ce6eb502ce07089f94bb617e8  internal bundle hash
2D01A1A3540CECAF34CE33CB4C915D012E3D1139A2354117735E9DE5223B62B6  run_bundle.json byte SHA256
FDA1EA56ACFA253C6804B15F8F018668904A1040B1CFD4879334BE9819F1708C  run_manifest.json
ED497B806447E3C6741E881C3ED5DE430B4147BA4D60D80491F83503DC8DE3C2  evidence_manifest.json
A7B29AA3652683B3FD38BAC1C1BA869938873D2C292145D91F246973B13EB978  trusted_bundle.json
```

Mechanical totals:

```text
row_count = 44
final_position_contracts = 34
cumulative_gross_pnl_amount = -74515.625
cumulative_commission_amount = 78.2
cumulative_spread_amount = 0.0
cumulative_net_pnl_amount = -74593.825
```

## Focused Verification

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

This local audit does not authorize provider/API access, downloads, new data acquisition, TEST, VALIDATION, OOS, Lockbox, Forward, result interpretation, PnL evaluation beyond mechanical row construction, tuning, adapter work, deployment, trading, promotion, Git action, or source-faithful evidence claim.
