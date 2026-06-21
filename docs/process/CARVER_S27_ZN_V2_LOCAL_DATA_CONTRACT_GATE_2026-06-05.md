# Carver S27 ZN V2 Local Data Contract Gate

Date: 2026-06-05

Status:

```text
PROCESS_ONLY_S27_ZN_V2_LOCAL_DATA_CONTRACT_GATE_NOT_RUNNER_AUTHORIZATION
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Purpose

Define the local row contract that any future S27 v2 file parser,
data-contract adapter, replay runner, diagnostic, or backtest must satisfy
before real local rows can be passed into the audited in-memory replay
primitives.

This is a process-only gate. It authorizes no provider/API access, no data
download, no file parsing, no diagnostic, no backtest, no OOS, no Lockbox, no
Forward, no tuning, no alpha claim, no promotion, no Git staging, no commit, no
push, no PR, no deployment, and no trading.

## Dependencies

Source lock:

```text
docs/process/CARVER_S27_ZN_BOOK_SOURCE_LOCK_2026-06-05.md
```

Source-lock re-audit:

```text
docs/process/CARVER_S27_ZN_SOURCE_LOCK_REAUDIT_RESULT_2026-06-05.md
```

Current v2 primitive/audit records:

```text
docs/process/CARVER_S27_ZN_V2_SOURCE_LOCK_IMPLEMENTATION_EXERCISE_2026-06-05.md
docs/process/CARVER_S27_ZN_V2_LOCAL_HOSTILE_AUDIT_RESULT_2026-06-05.md
```

Active implementation gate:

```text
S27_ZN_BOOK_SOURCE_LOCK_PASSED_FOR_V2_IMPLEMENTATION_EXERCISE
```

## Required Input Families

Any future parser or runner must provide these local row families before the
first replay step:

```text
S27_V2_LOCAL_DAILY_RUNTIME_SOURCE_ROWS
S27_V2_LOCAL_HOURLY_DECISION_AND_FILL_SOURCE_ROWS
S27_V2_LOCAL_SESSION_TRANSITION_ROWS
S27_V2_LOCAL_ROLL_BOUNDARY_ROWS
S27_V2_LOCAL_COST_PARAMETER_ROWS
S27_V2_LOCAL_PROVENANCE_ROWS
```

Rows must be local-cache rows only. Provider/API calls, provider refresh,
download, remote lookup, or silent row repair are not permitted by this gate.

## Daily Row Contract

Each daily row must map into `S27V2DailyRuntimeInput` and prove:

- `completed_trading_date` is an exact ISO calendar date.
- `completed_bar_timestamp` is timezone-aware UTC and date-aligned.
- `continuous_close` is finite and positive.
- `current_traded_contract_close` is finite and positive.
- `annual_percentage_sigma` is finite and positive.
- `annual_percentage_sigma_source_status` equals
  `STRATEGY3_OR_PREVALIDATED_ANNUAL_PERCENTAGE_SIGMA_SOURCE_LOCKED`.
- `source_status` equals
  `LOCAL_SYNTHETIC_OR_PREVALIDATED_COMPLETED_DAILY_ROW`.
- `level_compatibility_status` equals
  `DAILY_CONTINUOUS_HOURLY_CURRENT_LEVEL_COMPATIBILITY_PREVALIDATED`.

The row contract must fail closed if a daily row is missing, duplicated,
unordered, degraded, pending, unresolved, same-day/future for the hourly
decision, non-UTC, non-date-aligned, non-positive, or manually repaired outside
an explicit provenance row.

## Hourly Row Contract

Each hourly row must map into `S27V2HourlyRuntimeInput` and prove:

- `completed_bar_end_utc` is timezone-aware UTC and hour-aligned.
- `completed_trading_date` is an exact ISO calendar date.
- `raw_symbol` is non-empty.
- OHLC values, if carried by the local row shape, are finite and positive.
- High/low, if carried, bound open and close for row-integrity validation only.
- Limit-order execution must use the next completed hourly close. Intrabar
  high/low values are not fill authority for the S27 v2 source-faithful
  primitive.
- `provider_condition_status` equals
  `LOCAL_SYNTHETIC_OR_PREVALIDATED_COMPLETED_HOURLY_ROW`.

The row contract must fail closed if a decision row or its next fill row is
missing, duplicated, unordered, degraded, pending, unresolved, non-hour-aligned,
non-UTC, non-positive, inconsistent OHLC, or silently dropped.

## Daily-Hourly Bridge Contract

Before a replay step is allowed:

- the selected daily row must be the latest strict-prior daily runtime row for
  the hourly decision;
- the daily completed trading date must be before the hourly completed trading
  date;
- the daily completed timestamp must be before the hourly completed timestamp;
- the daily continuous price level and hourly current price level must carry
  the exact prevalidated compatibility status;
- the sigma bridge price must be the previous completed daily close of the
  currently traded contract;
- the annual percentage sigma used for V/Q/M and sigma-price bridge must be
  bound in the source-input and compatibility ledgers.

This gate does not assert that compatibility exists by string alone. A future
parser/adapter must emit a provenance row explaining why the daily continuous
level and hourly current contract level are compatible for this ZN source path.

## Forecast, Position, And Trend-Permission Contract

Before order generation is allowed:

- S27 trend permission is based on the post-fill target position sign, not raw
  order side.
- positive target positions require positive EWMAC trend.
- negative target positions require negative EWMAC trend.
- target position `0` is allowed for either nonzero trend direction and is the
  source-faithful flat/equilibrium boundary.
- zero EWMAC trend remains fail-closed.
- desired-position construction must use `RoundingPolicy.NEAREST`.
- non-nearest rounding policies are non-book-native scenario knobs and must
  fail closed in the S27 v2 source-faithful path.

## Session And Roll Contract

Each hourly transition must provide explicit row facts for:

- current session id;
- next session id;
- transition kind;
- current trading date;
- next trading date;
- current raw symbol;
- next raw symbol;
- roll handling status.

Transition labels must be supported by row facts:

- `NORMAL_ONE_HOUR` requires unchanged session id and unchanged trading date.
- `END_OF_DAY_CANCEL_RESET` requires advanced session id and advanced trading
  date.
- `OVERNIGHT_GAP_MARKET_RESET` requires advanced session id and advanced
  trading date.
- `ROLL_BOUNDARY` requires raw-symbol change and the explicit
  `ROLL_BOUNDARY_STATE_RESET_IMPLEMENTATION_ASSUMPTION_LOCKED` status.

Any missing, contradictory, inferred, or silently defaulted transition fact
fails closed.

Persistent working-limit carry across multiple normal decision rows remains
unresolved unless a later source-lock artifact explicitly authorizes and tests
that behavior. The current multi-row primitive fails closed on unresolved
carried working limits.

## Cost Contract

Any future replay runner must provide local cost inputs before the first fill:

- positive commission per contract;
- positive normal bid-ask spread;
- positive contract multiplier.

Cost treatment must remain:

```text
LIMIT_ORDER_FILL_COST = COMMISSION_ONLY
MARKET_ORDER_FILL_COST = COMMISSION_PLUS_NORMAL_BID_ASK_SPREAD
ALL_ORDERS_PAY_COMMISSION
```

Market orders without positive commission and positive spread fail closed.
Limit orders with spread costs fail closed.

## Required Output Families

A parser/runner that reaches replay must emit or preserve these artifact
families before any PnL interpretation:

```text
SOURCE_INPUT_MANIFEST
DAILY_HOURLY_CONTINUOUS_LEVEL_COMPATIBILITY_LEDGER
RUNTIME_REPLAY_LEDGER_EWMA5_EWMAC_SIGMA_VQM
FORECAST_REPLAY_LEDGER
DESIRED_POSITION_LEDGER
WORKING_ORDER_TRANSITION_LEDGER
LIMIT_ORDER_LEDGER
MARKET_ORDER_LEDGER
REMAINING_LIMIT_ORDER_LEDGER
CANCELED_LIMIT_ORDER_LEDGER
FILL_LEDGER
COMMISSION_LEDGER
SPREAD_COST_LEDGER
PNL_LEDGER
VALIDATION_LEDGER
PROVENANCE_AND_HASH_LEDGER
LOCAL_HOSTILE_AUDIT_RESULT
```

Empty artifact families must be represented explicitly with deterministic
provenance hashes.

## Required Local Hostile Audit Questions

Before any file parser, data-contract adapter, replay runner, diagnostic, or
backtest is trusted, a local hostile audit must answer:

1. Does the parser use only local rows and avoid provider/API/download paths?
2. Does every row map exactly into the v2 daily/hourly input dataclasses?
3. Does every hourly decision have exactly one next completed hourly fill row?
4. Is the strict-prior daily runtime selected without future leakage?
5. Does the compatibility ledger bind actual prices and sigma values, not only
   status strings?
6. Do session, overnight, EOD, and roll labels match row facts?
7. Are missing, duplicated, degraded, pending, unresolved, repaired, or silently
   dropped rows fail-closed?
8. Are all costs positive and assigned to the correct order type?
9. Do output ledgers preserve row-level provenance and SHA256 hashes?
10. Is there any old diagnostic runner, close-to-close target-position PnL,
    CFD adapter, stale import, or backtest path leak?

## Gate Decision

Current gate:

```text
S27_V2_LOCAL_DATA_CONTRACT_GATE_CREATED_PROCESS_ONLY_NOT_RUNNER_AUTHORIZATION
```

Next required gate:

```text
S27_V2_FILE_OR_DATA_CONTRACT_REPLAY_RUNNER_REQUIRES_SEPARATE_OPERATOR_AUTHORIZATION_AND_LOCAL_HOSTILE_AUDIT
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
