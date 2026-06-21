# Carver S27 ZN V2 GPT Reaudit Cap-Edge Remediation

Date: 2026-06-06

Status:

```text
PROCESS_ONLY_S27_ZN_V2_GPT_REAUDIT_CAP_EDGE_REMEDIATION_COMPLETE_FOR_SYNTHETIC_PRIMITIVE_SLICE
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Purpose

Record the GPT re-audit finding that target-position trend permission was
directionally corrected but still had a cap-edge adjacent-order blocker, and
record the local remediation applied to the synthetic in-memory primitive
slice.

This document authorizes no provider/API access, data download, file parsing,
diagnostic, backtest, OOS, Lockbox, Forward, tuning, alpha claim, promotion,
Git staging, commit, push, PR, deployment, or trading.

## External Reaudit Verdict

The external re-audit verdict was:

```text
TARGET_POSITION_REMEDIATION_DIRECTIONALLY_CORRECT_BUT_NOT_COMPLETE
NOT_BACKTEST_READY
```

The remaining blocker was that adjacent order generation could abort on an
unpriceable cap-side candidate before emitting the opposite source-required
exit order.

## Remediated Findings

Finding:

```text
P0_CAP_EDGE_ADJACENT_CANDIDATE_ABORTS_SOURCE_REQUIRED_EXIT
```

Remediation:

- adjacent order generation now prechecks whether a candidate target position
  is trend-permitted and strictly inside the forecast cap before calling
  implied-price inversion;
- unpriceable cap-side candidates are skipped, not allowed to abort the entire
  order plan;
- uptrend `current_position=1`, `base_position_contracts=1`, target `0` emits
  sell-to-flat even though the opposite buy-side target would be at cap;
- downtrend `current_position=-1`, `base_position_contracts=1`, target `0`
  emits buy-to-flat even though the opposite sell-side target would be at cap.

Finding:

```text
P1_PUBLIC_FILL_AND_STATE_BOUNDARIES_ACCEPT_INTERNALLY_INCONSISTENT_ORDER_PLANS
```

Remediation:

- `open_s27_v2_working_order_state` validates order-plan internal consistency;
- `fill_s27_v2_order_plan_one_hour_lag` validates order-plan internal
  consistency before fills;
- limit orders must be one-contract adjacent orders whose side, quantity, and
  target position match the plan current position;
- market order side, quantity, and target must be internally consistent and
  target the desired rounded position;
- mixed market/limit plans and malformed order kinds/cost treatments fail
  closed.

## Verification

Commands run locally:

```text
python -m compileall -q src\carver\spine\s27_v2.py tests\test_s27_v2_source_lock_synthetic.py
python -m unittest tests.test_s27_v2_source_lock_synthetic
```

Observed result:

```text
PASS_COMPILE
PASS_36_SYNTHETIC_UNIT_TESTS
```

## Current Focused Hashes

| Artifact | SHA256 |
|---|---|
| `src/carver/spine/s27_v2.py` | `931A3FDA9EAC1C23C8201CECD295ECE3D68A610862F89AB811CD2DA2EACED4DB` |
| `tests/test_s27_v2_source_lock_synthetic.py` | `02854D87F7E7CF408C10F7BF8831E2B3BC5635F218073073674EC77D6A53068A` |

## Remaining Blockers

These still block any real local-row replay, diagnostic, backtest, or PnL
interpretation:

```text
EXTERNAL_REAUDIT_OF_CAP_EDGE_REMEDIATION
ROUNDING_HALF_TIE_CONVENTION_STILL_IMPLEMENTATION_ASSUMPTION
REAL_LOCAL_SOURCE_ROW_PROVENANCE_AND_FILE_HASHES_REQUIRED
PARSER_ADAPTER_HOSTILE_AUDIT_REQUIRED
STRATEGY3_SIGMA_ESTIMATOR_PROVENANCE_REQUIRED
DAILY_HOURLY_LEVEL_COMPATIBILITY_PROOF_REQUIRED
ROLL_MAP_AND_SESSION_CALENDAR_PROOF_REQUIRED
SPREAD_UNIT_PROOF_REQUIRED
CAPACITY_SPEED_LIMIT_ELIGIBILITY_REQUIRED
REALISTIC_LOCAL_ROW_REPLAY_REQUIRED
```

## Current Gate Decision

Current state:

```text
S27_V2_GPT_REAUDIT_CAP_EDGE_AND_ORDER_PLAN_CONSISTENCY_REMEDIATED_FOR_SYNTHETIC_PRIMITIVE_SLICE
```

Still not authorized:

```text
NO_PROVIDER_API
NO_DATA_DOWNLOAD
NO_FILE_PARSING
NO_DIAGNOSTIC
NO_BACKTEST
NO_OOS
NO_LOCKBOX
NO_FORWARD
NO_TUNING
NO_ALPHA_CLAIM
NO_PROMOTION
NO_GIT_STAGE_COMMIT_PUSH_PR
```
