# S27_V2 First-Populated Input Pack P3 Hardening Local Audit Result

Date: 2026-06-09

Status:

```text
LOCAL_HOSTILE_AUDIT_PASS_NO_P0_P1_P2
```

Authorization:

```text
S27_V2_LOCAL_ONLY_FIRST_POPULATED_ZN_INPUT_PACK_P3_HARDENING_AND_BUILD
```

## Scope

Local hostile audit covered:

```text
src/carver/spine/s27_v2_replay/executable_replay.py
tests/test_s27_v2_local_replay_slice1.py
docs/researchops/s27_v2_local_replay_inputs/ZN/20260609_first_populated_dev_recon_znh2_20220103_multirow_declared_pack
docs/process/CARVER_S27_ZN_V2_FIRST_POPULATED_INPUT_PACK_P3_HARDENING_BUILD_RECORD_2026-06-09.md
docs/process/CARVER_S27_ZN_V2_TRUST_ROOT_DESIGN_CURRENT_STATE_AND_AUTHORIZATION_QUEUE_2026-06-06.md
```

## Subagent Results

Code hardening audit:

```text
PASS
No P0/P1/P2 blockers found.
Phase 2 now binds level-row prices to the exact Phase 1 provenance row hash, not row membership plus first price.
Regression test covers a multi-row forged-index case.
No forbidden execution surfaces found.
```

Declared pack/process-boundary audit:

```text
PASS
No P0/P1/P2 blockers found.
Pack declares SOURCE_NATIVE_FUTURES, exactly seven row-family CSVs plus support files, local-only boundaries, corrected first-post-populated rule, no source-faithful evidence claim, and fail-closed caveats for V/Q/M, sigma, level, and policy evidence.
No forbidden execution surfaces found.
```

## Verification Already Completed

Focused parser verification:

```text
DAILY_CONTINUOUS_COMPLETED_BAR,64
DAILY_CURRENT_CONTRACT_COMPLETED_BAR,1
HOURLY_DECISION_COMPLETED_BAR,8
HOURLY_FILL_COMPLETED_BAR,8
SESSION_CALENDAR,1
ROLL_CALENDAR,1
COST_PARAMETER,1
```

Focused tests:

```text
python -m pytest tests\test_s27_v2_local_replay_slice1.py -q
68 passed
```

Compile check:

```text
python -m compileall -q src\carver\spine\s27_v2_replay\executable_replay.py tests\test_s27_v2_local_replay_slice1.py
PASS
```

## Carried Caveats

The new multi-row declared input pack is construction input only. It is not a source-faithful replay evidence claim.

The local R2 V/Q/M ledger ends at `2020-12-21`, while the selected hourly decision row is `2022-01-03T05:00:00Z`. Runtime work must remain fail-closed unless V/Q/M is recomputed or source-locked under S27_V2 authority.

The selected daily sigma is carried from an already-local forecast sigma bridge row to satisfy the current parser schema. That does not source-lock Strategy 3 sigma.

## Non-Authorization

This audit result does not authorize provider/API access, downloads, new data acquisition, OOS, Lockbox, Forward, backtests, result-scored runs, result interpretation, PnL/result evaluation, tuning, adapter work, deployment, trading, promotion, Git actions, or source-faithful evidence claims.
