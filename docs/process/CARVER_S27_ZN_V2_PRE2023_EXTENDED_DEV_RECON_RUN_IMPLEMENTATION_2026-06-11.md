# S27_V2 Pre-2023 Extended Development/Reconciliation Run Implementation

Date: 2026-06-11

Status:

```text
S27_V2_PRE2023_EXTENDED_DEVELOPMENT_RECON_RUN_EMITTED_NOT_RESULT
```

Authorization:

```text
S27_V2_LOCAL_ONLY_EXTENDED_PRE2023_DEVELOPMENT_RECON_RUN_GATE
```

Artifact-bound authorization label:

```text
S27_V2_CONSOLIDATED_LOCAL_ONLY_PRE2023_EXTENDED_DEVELOPMENT_RECON_IMPLEMENTATION_AND_RUN_GATE
```

The operator authorization text names the local-only extended run gate. The code, declared input manifest, and run manifest bind the artifact authority with the consolidated implementation-and-run label above. The two labels refer to the same scoped gate; the artifact-bound label is the one enforced by code and manifests.

## Scope

This record covers the local-only extended pre-2023 Development/Reconciliation checkpoint after local/GPT/GitHub-head PASS on the four-row broader checkpoint.

The selected slice uses already-local pre-2023 ZN files only. It preserves 2023 for TEST. Pre-2022 data is used only as strict-prior warmup/evidence.

No provider/API access, downloads, new data acquisition, TEST, VALIDATION, OOS, Lockbox, Forward, result interpretation, PnL evaluation beyond mechanical row construction, tuning, adapter work, deployment, trading, promotion, Git action, or source-faithful evidence claim is authorized or performed by this record.

## Files

Code:

```text
tools/databento/carver_s27_v2_pre2023_extended_dev_recon_pack.py
src/carver/spine/s27_v2_replay/pre2023_extended_development_recon_run.py
tests/test_s27_v2_pre2023_extended_development_recon.py
```

Declared input pack:

```text
docs/researchops/s27_v2_local_replay_inputs/ZN/20260611_pre2023_extended_dev_recon_2022_minimum_extended_declared_pack
```

Run artifact root:

```text
docs/researchops/s27_v2_local_replay_runs/ZN/20260611_pre2023_extended_dev_recon_2022_minimum_extended_run
```

## Selection

Selected decision/fill/valuation triples:

```text
2022-01-03T01:00:00Z / 2022-01-03T02:00:00Z / 2022-01-03T03:00:00Z
2022-01-03T03:00:00Z / 2022-01-03T04:00:00Z / 2022-01-03T05:00:00Z
2022-01-03T05:00:00Z / 2022-01-03T06:00:00Z / 2022-01-03T07:00:00Z
2022-01-03T07:00:00Z / 2022-01-03T08:00:00Z / 2022-01-03T09:00:00Z
2022-01-04T00:00:00Z / 2022-01-04T01:00:00Z / 2022-01-04T02:00:00Z
2022-01-04T02:00:00Z / 2022-01-04T03:00:00Z / 2022-01-04T04:00:00Z
2022-01-04T04:00:00Z / 2022-01-04T05:00:00Z / 2022-01-04T06:00:00Z
2022-01-04T06:00:00Z / 2022-01-04T07:00:00Z / 2022-01-04T08:00:00Z
2022-01-04T08:00:00Z / 2022-01-04T09:00:00Z / 2022-01-04T10:00:00Z
2022-01-04T10:00:00Z / 2022-01-04T11:00:00Z / 2022-01-04T12:00:00Z
```

Stop reason:

```text
NEXT_STRICT_TWO_HOUR_DECISION_FILL_MARK_SEQUENCE_BREAKS_AFTER_2022-01-04T10:00:00Z_BECAUSE_2022-01-04T13:00:00Z_IS_MISSING
```

## Pack Hashes

```text
A2DD529AFD54EA7783F0C3AE935999381909B759D924079A420EAADBEE770965  S27_V2_PRE2023_EXTENDED_DEV_RECON_DECLARED_INPUT_PACK_MANIFEST.json
F44FC85A853E5B139DC632EA7C22FDE8F4DDB0F1056CA84C6BB3DAF91F3D79E1  hourly_decision_completed_bar.csv
6A7B10984205046E62375AB08EE9A22C0F9733897E3D2B03D7D0E8538D9974ED  hourly_fill_completed_bar.csv
C49E7786B247D3B09357A13D75775CB07EFB7E5F160DA995C9B3DB4D363D6167  valuation_mark_completed_bar.csv
BEAD246E435B351EA8663FAC2047E2B2B9982A618CBCCB435080333953EFF482  session_calendar.csv
```

## Run Summary

Mechanical ledger summary:

```text
row_count = 10
position_state = 0 -> 8 -> 12 -> 14 -> 15 -> 33 -> 33 -> 33 -> 33 -> 33 -> 33
cumulative_gross_pnl_amount = -30312.5
cumulative_commission_amount = 75.89999999999999
cumulative_spread_amount = 0.0
cumulative_net_pnl_amount = -30388.4
```

Rows 1-5 emit filled BUY limit rows. Rows 6-10 emit no-order/no-fill metadata because desired position equals current position at `33`.

Run hashes:

```text
0b012c95a94de0dfcecf383282b24ad02c4644ec03b6f4c82102d7d30a9fa053  internal bundle hash
2E75A7340D7C80E9E6B96EAFB06E5568E8CFCF96BDD6D32E1569DCA5DB9DF877  run_bundle.json byte SHA256
C07C31A1323F7933B076D4246164BB103FD3FAE3330CEC129616279B3776F49D  run_manifest.json
B73F8AB4F2C914C1286B8C4BBBBD542C1ED1D45440D38ACE2BE7FE41B8889FF4  evidence_manifest.json
A1471A983FDADA5E707908B23022EF7D054743F3E4CF2FB6D6E233F083B7AEE4  trusted_bundle.json
```

## Verification

Commands:

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

## Non-Authorization

This checkpoint is local mechanical Development/Reconciliation ledger construction only. It is not a result-scored run, result interpretation, PnL evaluation beyond mechanical row construction, tuning evidence, promotion evidence, or source-faithful evidence claim.
