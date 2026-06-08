# Carver S27 ZN V2 GPT Reaudit Target-Position Remediation

Date: 2026-06-06

Status:

```text
PROCESS_ONLY_S27_ZN_V2_GPT_REAUDIT_TARGET_POSITION_REMEDIATION_COMPLETE_FOR_SYNTHETIC_PRIMITIVE_SLICE
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Purpose

Record the GPT re-audit finding that the first S27 v2 trend-permission
remediation overcorrected into an order-side veto, and record the local
remediation applied to the synthetic in-memory primitive slice.

This document authorizes no provider/API access, data download, file parsing,
diagnostic, backtest, OOS, Lockbox, Forward, tuning, alpha claim, promotion,
Git staging, commit, push, PR, deployment, or trading.

## External Reaudit Verdict

The external re-audit verdict was:

```text
NOT_SOURCE_FAITHFUL_S27_EXECUTION
NOT_BACKTEST_READY
```

The main blocker was that S27 trend permission must be target-position/sign
based, not raw order-side based. In an uptrend, sell orders that reduce a long
to flat or to a smaller non-negative position can be source-required. In a
downtrend, buy orders that reduce a short to flat or to a smaller non-positive
position can be source-required.

## Remediated Findings

Finding:

```text
P0_ORDER_SIDE_VETO_SHOULD_BE_TARGET_POSITION_TREND_PERMISSION
```

Remediation:

- removed the order-side trend permission helper;
- added target-position trend permission;
- target `0` is allowed for either nonzero trend direction;
- positive target positions require positive EWMAC trend;
- negative target positions require negative EWMAC trend;
- adjacent limit generation now checks the post-fill target position;
- market fallback now checks the desired rounded target position;
- implied-price inversion now checks the target position rather than order
  side.

Finding:

```text
P0_ZERO_RAW_MEAN_REVERSION_FORECAST_SHOULD_FLATTEN_NOT_FAIL
```

Remediation:

- forecast replay no longer fails closed on zero raw/risk-adjusted
  mean-reversion forecast;
- zero forecast returns zero capped forecast and zero desired position;
- zero trend remains fail-closed.

Finding:

```text
P1_DIRECT_TRANSITION_FACT_VALIDATION_GAPS
```

Remediation:

- direct transition primitive now validates direct transition facts before any
  transition branch can return;
- normal direct transitions require unchanged session, unchanged trading date,
  and unchanged raw symbol;
- EOD and overnight direct transitions require advanced session and trading
  date plus unchanged raw symbol;
- direct roll boundaries require raw-symbol change;
- EOD transitions with pending market orders fail closed.

Finding:

```text
P2_ROUNDING_POLICY_NOT_LOCKED
```

Remediation:

- source-faithful desired-position construction now requires
  `RoundingPolicy.NEAREST`;
- non-nearest policies fail closed in the S27 v2 path.

## Verification

Commands run locally:

```text
python -m compileall -q src\carver\spine\s27_v2.py tests\test_s27_v2_source_lock_synthetic.py
python -m unittest tests.test_s27_v2_source_lock_synthetic
```

Observed result:

```text
PASS_COMPILE
PASS_34_SYNTHETIC_UNIT_TESTS
```

## Current Focused Hashes

| Artifact | SHA256 |
|---|---|
| `src/carver/spine/s27_v2.py` | `E319E7CAB4E8580DE07CDDAE24E74256C35D9B5389F90921125CAFCDF0A54B04` |
| `tests/test_s27_v2_source_lock_synthetic.py` | `6C294AC3900A181D8A797F8E339F6039C157C381B20C85DBED125FEAF21CAAFD` |

## Remaining Blockers

These still block any real local-row replay, diagnostic, backtest, or PnL
interpretation:

```text
EXTERNAL_REAUDIT_OF_TARGET_POSITION_REMEDIATION
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
S27_V2_GPT_REAUDIT_P0_TARGET_POSITION_AND_ZERO_BOUNDARY_REMEDIATED_FOR_SYNTHETIC_PRIMITIVE_SLICE
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
