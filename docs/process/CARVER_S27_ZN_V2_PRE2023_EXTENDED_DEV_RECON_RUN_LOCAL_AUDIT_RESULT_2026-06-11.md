# S27_V2 Pre-2023 Extended Development/Reconciliation Run Local Audit Result

Date: 2026-06-11

Status:

```text
LOCAL_HOSTILE_AUDIT_PASS_AFTER_P2_RECORD_LABEL_PATCH
```

Scope:

```text
S27_V2 local-only extended pre-2023 Development/Reconciliation run gate
```

Artifacts audited:

```text
tools/databento/carver_s27_v2_pre2023_extended_dev_recon_pack.py
src/carver/spine/s27_v2_replay/pre2023_extended_development_recon_run.py
tests/test_s27_v2_pre2023_extended_development_recon.py
docs/researchops/s27_v2_local_replay_inputs/ZN/20260611_pre2023_extended_dev_recon_2022_minimum_extended_declared_pack
docs/researchops/s27_v2_local_replay_runs/ZN/20260611_pre2023_extended_dev_recon_2022_minimum_extended_run
docs/process/CARVER_S27_ZN_V2_PRE2023_EXTENDED_DEV_RECON_RUN_IMPLEMENTATION_2026-06-11.md
```

## Local Audit Summary

Two read-only hostile subagents were run.

The mechanical ledger/hash audit returned `PASS` with no P0/P1/P2/P3 findings. It verified the ten-row decision/fill/valuation plan, strict timestamp ordering, two-session split, pack/run hash binding, state carry `0 -> 8 -> 12 -> 14 -> 15 -> 33` followed by five no-order rows, limit fills, commission costs, PnL arithmetic, and final totals.

The governance/window audit found one P2 record-integrity issue: the implementation record named the operator's short-form authorization label while code/manifests bind the consolidated artifact authorization label.

## P2 Patch

Patched:

```text
docs/process/CARVER_S27_ZN_V2_PRE2023_EXTENDED_DEV_RECON_RUN_IMPLEMENTATION_2026-06-11.md
```

Patch disposition:

```text
DOCUMENTATION_LABEL_BINDING_PATCH_APPLIED_AND_REAUDITED_PASS
```

The implementation record now preserves the operator authorization label and separately records the artifact-bound authorization label enforced by code, declared input manifest, and run manifest:

```text
S27_V2_CONSOLIDATED_LOCAL_ONLY_PRE2023_EXTENDED_DEVELOPMENT_RECON_IMPLEMENTATION_AND_RUN_GATE
```

Narrow re-audit result:

```text
PASS_NO_REMAINING_FINDINGS
```

## Verified Outputs

Pack manifest SHA256:

```text
A2DD529AFD54EA7783F0C3AE935999381909B759D924079A420EAADBEE770965
```

Run hashes:

```text
0b012c95a94de0dfcecf383282b24ad02c4644ec03b6f4c82102d7d30a9fa053  internal bundle hash
2E75A7340D7C80E9E6B96EAFB06E5568E8CFCF96BDD6D32E1569DCA5DB9DF877  run_bundle.json byte SHA256
C07C31A1323F7933B076D4246164BB103FD3FAE3330CEC129616279B3776F49D  run_manifest.json
B73F8AB4F2C914C1286B8C4BBBBD542C1ED1D45440D38ACE2BE7FE41B8889FF4  evidence_manifest.json
A1471A983FDADA5E707908B23022EF7D054743F3E4CF2FB6D6E233F083B7AEE4  trusted_bundle.json
```

Mechanical totals:

```text
row_count = 10
final_position_contracts = 33
cumulative_gross_pnl_amount = -30312.5
cumulative_commission_amount = 75.9
cumulative_spread_amount = 0.0
cumulative_net_pnl_amount = -30388.4
```

## Focused Verification

```text
python -m py_compile tools\databento\carver_s27_v2_pre2023_extended_dev_recon_pack.py src\carver\spine\s27_v2_replay\pre2023_extended_development_recon_run.py
python -m pytest tests\test_s27_v2_pre2023_extended_development_recon.py -q
python -m pytest tests\test_s27_v2_pre2023_broader_development_recon.py tests\test_s27_v2_pre2023_extended_development_recon.py -q
```

Results:

```text
py_compile PASS
23 passed
46 passed
```

## P3 Note

The focused tests regenerate artifacts before asserting them. This is retained as non-blocking P3 because the read-only hostile audit separately inspected the generated pack/run artifacts without rewriting them.

## Non-Authorization

This local audit does not authorize provider/API access, downloads, new data acquisition, TEST, VALIDATION, OOS, Lockbox, Forward, result interpretation, PnL evaluation beyond mechanical row construction, tuning, adapter work, deployment, trading, promotion, Git action, or source-faithful evidence claim.
