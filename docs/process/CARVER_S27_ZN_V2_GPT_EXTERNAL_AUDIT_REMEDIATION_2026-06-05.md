# Carver S27 ZN V2 GPT External Audit Remediation

Date: 2026-06-05

Status:

```text
PROCESS_ONLY_S27_ZN_V2_GPT_EXTERNAL_AUDIT_REMEDIATION_COMPLETE_FOR_SYNTHETIC_PRIMITIVE_SLICE
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Purpose

Record the external GPT 5.5 Extended Pro audit findings for the S27 ZN v2
source-lock implementation exercise and the local remediation applied to the
in-memory synthetic primitive slice.

This document authorizes no provider/API access, data download, file parsing,
diagnostic, backtest, OOS, Lockbox, Forward, tuning, alpha claim, promotion,
Git staging, commit, push, PR, deployment, or trading.

## External Audit Verdict

The external audit verdict was:

```text
NOT_COMPLETE_SOURCE_FAITHFUL_S27_IMPLEMENTATION
SOURCE_LOCK_PRIMITIVE_IMPLEMENTATION_EXERCISE_ONLY
```

The audit accepted that the current-row forecast chain and scalar treatment
were mostly faithful, but rejected execution/data replay source-faithfulness
before PnL interpretation.

## Remediated P0 Findings

Finding:

```text
P0_S27_TREND_VETO_NOT_PRESERVED_IN_ADJACENT_LIMIT_ORDER_GENERATION
```

Remediation:

- `S27V2ForecastContext` now carries `trend_forecast`.
- `build_s27_v2_order_plan` suppresses adjacent limit sides not permitted by
  the EWMAC trend sign.
- market fallback cases also require the requested side to be trend-permitted.
- `implied_price_for_target_position` fails closed if the inverse target would
  imply a side vetoed by S27 trend permission.
- tests now assert that an uptrend creates only the buy-side adjacent limit and
  a downtrend creates only the sell-side adjacent limit.

Finding:

```text
P0_LIMIT_FILL_SIMULATION_USED_OHLC_HIGH_LOW_INSTEAD_OF_NEXT_COMPLETED_CLOSE
```

Remediation:

- `fill_s27_v2_order_plan_one_hour_lag` now fills buy limits only when the
  next completed hourly close is at or below the limit price.
- sell limits fill only when the next completed hourly close is at or above
  the limit price.
- high/low may remain present in synthetic/local row validation, but high/low
  are not execution fill authority for the v2 primitive.
- tests now prove that intrabar high/low touches do not create a fill when the
  next completed close does not cross the limit.

Finding:

```text
P0_END_OF_DAY_CANCEL_RESET_FILLED_BEFORE_CANCELING_LIMITS
```

Remediation:

- `END_OF_DAY_CANCEL_RESET` now cancels all working limits before any next
  price can be eligible for fill.
- the transition returns no fills, preserves the current position, and records
  canceled working limits.
- overnight gap market reset remains a separate transition case.
- tests now prove that an EOD transition cancels a limit even when the next
  completed close would otherwise have filled it.

## Remediated P1 Findings

Finding:

```text
P1_PREVALIDATED_STATUS_FIELDS_DEFAULTED_TO_SUCCESS
```

Remediation:

- daily row, hourly row, level-compatibility, and annual-percentage-sigma
  source statuses now default to explicit fail-closed sentinel values.
- tests/helper constructors must pass exact ready/provenance statuses.
- tests now prove default-constructed daily/hourly rows fail closed.

Finding:

```text
P1_ONE_STEP_REPLAY_COULD_NOT_PROVE_LATEST_STRICT_PRIOR_DAILY_RUNTIME
```

Remediation:

- direct one-step forecast/replay primitives now require the explicit
  `CALLER_CERTIFIED_LATEST_STRICT_PRIOR_DAILY_RUNTIME` status.
- multi-row replay still performs the latest strict-prior selection internally
  and passes that certification into each step.
- tests now prove direct forecast replay fails closed without the
  certification.

Finding:

```text
P1_PERCENTAGE_SIGMA_SOURCE_NOT_LOCKED_TO_STRATEGY3_OR_PREVALIDATED_SOURCE
```

Remediation:

- daily input/runtime rows now carry
  `STRATEGY3_OR_PREVALIDATED_ANNUAL_PERCENTAGE_SIGMA_SOURCE_LOCKED`.
- forecast replay fails closed if the runtime sigma-source status diverges
  from the input row status.
- source-input and compatibility ledgers now bind the annual-percentage-sigma
  source status.

## Verification

Commands run locally:

```text
python -m compileall -q src\carver\spine\s27_v2.py tests\test_s27_v2_source_lock_synthetic.py
python -m unittest tests.test_s27_v2_source_lock_synthetic
```

Observed result:

```text
PASS_COMPILE
PASS_33_SYNTHETIC_UNIT_TESTS
```

## Remaining Non-Remediated External Audit Concerns

These remain outside the current implementation exercise and still block real
PnL interpretation:

```text
REAL_LOCAL_SOURCE_ROW_PROVENANCE_AND_FILE_HASHES_REQUIRED
PARSER_ADAPTER_HOSTILE_AUDIT_REQUIRED
STRATEGY3_SIGMA_ESTIMATOR_PROVENANCE_REQUIRED
DAILY_HOURLY_LEVEL_COMPATIBILITY_PROOF_REQUIRED
ROLL_MAP_AND_SESSION_CALENDAR_PROOF_REQUIRED
SPREAD_UNIT_PROOF_REQUIRED
CAPACITY_SPEED_LIMIT_ELIGIBILITY_REQUIRED
REALISTIC_LOCAL_ROW_REPLAY_REQUIRED
EXTERNAL_REAUDIT_REQUIRED_AFTER_REMEDIATION_PACKET
```

## Current Gate Decision

Current state:

```text
S27_V2_GPT_EXTERNAL_AUDIT_P0_P1_CODE_REMEDIATIONS_COMPLETE_FOR_SYNTHETIC_PRIMITIVE_SLICE
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
