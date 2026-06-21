# Carver S27 ZN V2 GPT Reaudit Market Fallback Remediation

Date: 2026-06-06

Status:

```text
PROCESS_ONLY_S27_ZN_V2_GPT_REAUDIT_MARKET_FALLBACK_REMEDIATION_COMPLETE_FOR_SYNTHETIC_PRIMITIVE_SLICE
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Purpose

Record the GPT re-audit finding that the cap-edge remediation still allowed a
desired-side-at-cap candidate to be skipped while returning only an opposite
limit order, and record the local remediation applied to the synthetic
in-memory primitive slice.

This document authorizes no provider/API access, data download, file parsing,
diagnostic, backtest, OOS, Lockbox, Forward, tuning, alpha claim, promotion,
Git staging, commit, push, PR, deployment, or trading.

## External Reaudit Verdict

The external re-audit verdict was:

```text
CAP_EDGE_EXIT_CASES_FIXED_BUT_MARKET_FALLBACK_STILL_WRONG_WHEN_DESIRED_SIDE_IS_AT_CAP
NOT_BACKTEST_READY
```

The blocker was that fallback was keyed to `no limit orders at all`, rather
than `no executable route toward the desired rounded position`.

## Remediated Findings

Finding:

```text
P0_DESIRED_ADJACENT_SIDE_SKIPPED_AT_CAP_SUPPRESSED_MARKET_FALLBACK_WHEN_OPPOSITE_LIMIT_EXISTED
```

Remediation:

- order planning now checks whether any produced limit order reaches the
  desired rounded position;
- if the desired gap is nonzero and no limit order reaches the desired target,
  the planner returns a market fallback toward the desired target;
- the unrelated opposite limit order is not emitted in that fallback plan;
- uptrend `base_position_contracts=1`, `current_position=1`,
  `capped_forecast=15.1`, desired target `2` now emits a buy market fallback;
- downtrend `base_position_contracts=1`, `current_position=-1`,
  `capped_forecast=-15.1`, desired target `-2` now emits a sell market
  fallback.

Finding:

```text
P1_PLAN_LEVEL_FORGED_LIMIT_PLAN_WITH_LARGE_DESIRED_GAP_ACCEPTED
```

Remediation:

- order-plan validation now rejects limit-order plans with desired gap greater
  than one;
- limit-order plans with nonzero desired gap must include an order whose
  target position equals the desired rounded position;
- order plans with nonzero desired gap and no orders fail closed.

Finding:

```text
P1_DIRECT_IMPLIED_PRICE_AT_CAP_FAILURE_NOT_TESTED
```

Remediation:

- tests now directly assert `implied_price_for_target_position` fails closed
  for target positions at the forecast cap boundary in both directions under
  the packet's strict-inside limit-price convention.

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
| `src/carver/spine/s27_v2.py` | `16C73F7C5BAAF73FF538DFBC051F24D6826903CA3B3E08007361D7CD9412F253` |
| `tests/test_s27_v2_source_lock_synthetic.py` | `CA181E79173767C4679C161BDC33ED1C93A810ED55F6B7881388A70CB96DBC65` |

## Remaining Blockers

These still block any real local-row replay, diagnostic, backtest, or PnL
interpretation:

```text
EXTERNAL_REAUDIT_OF_MARKET_FALLBACK_REMEDIATION
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
S27_V2_GPT_REAUDIT_MARKET_FALLBACK_AND_PLAN_LEVEL_VALIDATION_REMEDIATED_FOR_SYNTHETIC_PRIMITIVE_SLICE
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
