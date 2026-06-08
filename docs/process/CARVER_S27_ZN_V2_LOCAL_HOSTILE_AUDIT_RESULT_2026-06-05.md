# Carver S27 ZN V2 Local Hostile Audit Result

Date: 2026-06-05

Status:

```text
PROCESS_ONLY_S27_ZN_V2_LOCAL_HOSTILE_AUDIT_PASS_WITH_REMEDIATION_STATE_MACHINE_REPLAY_STEP_AND_MULTI_ROW_SLICES_ADDED
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Authorization

Operator authorization:

```text
Operator authorizes local hostile audit of S27_V2 source-lock implementation slice, no provider/API, no downloads, no backtests, no OOS/Lockbox/Forward, no git actions.
```

This record authorizes no provider/API access, no data download, no diagnostic,
no backtest, no OOS, no Lockbox, no Forward, no tuning, no alpha claim, no
promotion, no Git staging, no commit, no push, no PR, no deployment, and no
trading.

## Scope

Audited files:

```text
src/carver/spine/s27_v2.py
tests/test_s27_v2_source_lock_synthetic.py
docs/process/CARVER_S27_ZN_BOOK_SOURCE_LOCK_2026-06-05.md
docs/process/CARVER_S27_ZN_SOURCE_LOCK_REAUDIT_RESULT_2026-06-05.md
docs/process/CARVER_S27_ZN_V2_LOCAL_DATA_CONTRACT_GATE_2026-06-05.md
```

Subagent sidecar:

```text
019e9724-3b85-7f31-ae05-565fc391a7a5 Lovelace
```

The subagent performed read-only audit work and reported no edits.

## Findings

Finding 1:

```text
P1_SOURCE_ROW_FAIL_CLOSED_GATES_TOO_WEAK
```

Daily and hourly row status fields accepted any non-empty string. This could
allow degraded, pending, unresolved, or otherwise non-ready rows into replay.

Disposition:

```text
REMEDIATED
```

The v2 module now requires exact daily and hourly readiness statuses before row
use.

Finding 2:

```text
P1_DAILY_HOURLY_LEVEL_COMPATIBILITY_AND_SIGMA_BRIDGE_PROOF_UNDERREPRESENTED
```

The first v2 slice did not carry an explicit daily/hourly level compatibility
status through runtime rows and did not fail closed if a manually supplied
daily runtime row drifted from the daily input.

Disposition:

```text
REMEDIATED_FOR_CURRENT_SLICE
```

The daily input and runtime rows now carry exact level compatibility status.
Forecast replay fails closed if runtime current traded contract close or annual
percentage sigma differs from the daily input.

Finding 3:

```text
P1_WORKING_ORDER_SESSION_EOD_OVERNIGHT_GAP_MACHINERY_ONLY_SKETCHED
```

The first v2 slice emits adjacent orders and one-hour-lag fills, but does not
yet implement persistent working-order state, end-of-day cancellation as a
state transition, session boundaries, overnight gap market-order handling, roll
interaction, or realistic working-order replay across rows.

Initial disposition:

```text
NOT_REMEDIATED_BLOCKS_ROW_REPLAY_EXPANSION
```

The current v2 code remains an implementation exercise slice only. Row-replay
expansion is blocked until this machinery is implemented and tested.

Follow-up disposition:

```text
REMEDIATED_FOR_STATE_MACHINE_PRIMITIVE_SLICE
```

The v2 module now includes working-order/session transition primitives that:

- open working-order state from an order plan;
- transition exactly one completed hour at a time;
- carry remaining limits across normal same-session transitions;
- cancel remaining limits on end-of-day reset;
- cancel limits and use market reset orders on overnight-gap transitions;
- fail closed on raw-symbol changes unless an explicit roll-boundary transition
  is supplied;
- fail closed on roll-boundary transitions unless the explicit
  `ROLL_BOUNDARY_STATE_RESET_IMPLEMENTATION_ASSUMPTION_LOCKED` status is used;
- cancel working limits at that explicit roll reset without claiming a
  book-native roll execution rule.

This does not yet authorize realistic row replay or any backtest; it supplies
the state-machine primitive needed before a later row-replay implementation can
be built and audited.

Replay-step follow-up disposition:

```text
REMEDIATED_FOR_REPLAY_STEP_LEDGER_BUNDLE_SLICE
```

The v2 module now includes a deterministic one-step replay ledger bundle that
uses caller-supplied local or synthetic rows only. It emits source-input,
daily/hourly compatibility, runtime, forecast, desired-position, order, fill,
commission, spread-cost, PnL, validation, and provenance-hash ledgers for one
decision row and its next completed hourly fill row.

The first hostile re-audit of this replay-step slice found:

```text
P1_SOURCE_INPUT_PROVENANCE_DID_NOT_BIND_FILL_ROW_SOURCE_INPUT
P2_COMPATIBILITY_LEDGER_WAS_ASSERTION_ONLY
P2_DIRECT_ZERO_COST_MARKET_FILL_LEAKAGE
P3_TRADING_DATES_COMPARED_AS_UNVALIDATED_STRINGS
TEST_GAP_FULL_PROVENANCE_FAMILY_ASSERTIONS
TEST_GAP_MARKET_SPREAD_BUNDLE_PATH
```

Follow-up re-audit sidecar:

```text
019e9737-9a24-7a51-942b-26087e440a2a Locke
```

The re-audit reported that all previously reported replay-step findings were
remediated for the current slice. The remediation adds:

- daily, decision-hourly, and fill-hourly OHLC/status binding in the
  source-input manifest;
- value binding in the compatibility ledger for daily continuous close, current
  traded-contract close, hourly current price, sigma bridge price, and annual
  percentage sigma;
- fill-hour row readiness validation;
- deterministic provenance hash rows for empty artifact families;
- direct cost-ledger rejection of malformed externally supplied market fills;
- exact ISO calendar-date validation for daily and hourly trading dates;
- bundle-level tests for market orders and spread-cost ledger rows.

## Multi-Row Replay Slice Audit

Multi-row hostile audit sidecar:

```text
019e974a-26d7-7861-acef-a28310e6a0ed Nietzsche
```

The first hostile audit of the multi-row replay slice found:

```text
P1_SESSION_TRANSITIONS_WERE_CALLER_LABELS_NOT_FACTS
P1_MARKET_ORDER_LEDGER_COULD_DIVERGE_FROM_ACTUAL_TRANSITION
P2_EXPLICIT_EMPTY_ROLL_STATUS_INPUT_DEFAULTED_TO_NO_ROLL
TEST_GAP_FALSE_EOD_OVERNIGHT_LABELS
TEST_GAP_OVERNIGHT_MARKET_ORDER_PROVENANCE
TEST_GAP_ROLL_BOUNDARY_WITH_PLAN_MARKET_ORDERS
TEST_GAP_EMPTY_ROLL_STATUSES
```

Follow-up disposition:

```text
REMEDIATED_FOR_MULTI_ROW_REPLAY_PLUMBING_SLICE
```

The re-audit reported no remaining blocker from the previously reported
multi-row findings. The remediation adds:

- transition-fact gates before step ledger construction;
- normal transition checks for unchanged session and trading date;
- EOD and overnight transition checks for advanced session and trading date;
- roll-boundary checks for raw-symbol change plus the explicit roll reset
  assumption;
- market-order ledger rows that reflect executed transition market orders;
- suppression of unexecuted plan market orders on roll-boundary resets;
- explicit rejection of malformed empty `roll_handling_statuses=()`;
- tests for false EOD/overnight labels, overnight market-order provenance,
  roll-boundary plan-market suppression, and empty roll statuses.

Finding 4:

```text
P2_ZERO_COST_LEAKAGE_ALLOWED
```

The first v2 slice allowed zero commission and zero normal spread. That could
silently recreate no-cost diagnostic assumptions.

Disposition:

```text
REMEDIATED
```

Fill simulation now requires positive commission per contract and positive
normal bid-ask spread.

Finding 5:

```text
P2_ZERO_EWMAC_TREND_CASE_UNDERTESTED
```

The code failed closed on zero trend or zero mean-reversion sign, but tests
only covered zero mean-reversion.

Disposition:

```text
REMEDIATED
```

Synthetic tests now cover zero EWMAC trend fail-closed behavior.

## Positive Audit Checks

The local hostile audit found no explicit old CFD adapter, close-to-close
target-position backtest runner, or stale S27 diagnostic runner leak inside
`src/carver/spine/s27_v2.py`.

The following remain directionally source-faithful in the current slice:

- S27 scalar is book-estimated `AROUND_20`, implementation-frozen at `20.0`,
  not represented as source-exact.
- Forecast replay follows raw forecast, sigma-price bridge, risk-adjusted
  forecast, EWMAC veto, V/Q/M multiplier, scalar, and cap order.
- V/Q/M uses percentage sigma, ten-year rolling mean where available,
  expanding quantile history, and EWMA span 10.
- Desired position uses capped forecast divided by `10` times base position.
- Limit fills are commission-only.
- Market fills are commission plus normal bid-ask spread.
- One-hour-lag fills are required.
- Same-bar dual limit-side touches fail closed.

## Verification

Commands run:

```text
python -m unittest tests.test_s27_v2_source_lock_synthetic
python -m compileall -q src\carver\spine\s27_v2.py tests\test_s27_v2_source_lock_synthetic.py
```

Result:

```text
PASS_31_SYNTHETIC_UNIT_TESTS
PASS_COMPILE
```

Current hashes:

| File | SHA256 |
|---|---|
| `src/carver/spine/s27_v2.py` | `567FC91106CBDE05A876708497C5A1C9290828A29A6A3B93AC0CD4386BEF751F` |
| `tests/test_s27_v2_source_lock_synthetic.py` | `E46D12D2DE03B9B1E5CEFDB3A4ACB1C9BE66BC2BBB430C63632905AA3E267225` |

## Gate Decision

Current v2 slice gate:

```text
S27_V2_SOURCE_LOCK_IMPLEMENTATION_SLICE_LOCAL_AUDIT_REMEDIATED_WITH_STATE_MACHINE_REPLAY_STEP_AND_MULTI_ROW_PRIMITIVES
```

Next required gate:

```text
S27_V2_FILE_OR_DATA_CONTRACT_REPLAY_RUNNER_REQUIRES_SEPARATE_OPERATOR_AUTHORIZATION_AND_LOCAL_HOSTILE_AUDIT
```

Required process gate before that runner:

```text
docs/process/CARVER_S27_ZN_V2_LOCAL_DATA_CONTRACT_GATE_2026-06-05.md
```

Still not authorized:

```text
NO_PROVIDER_API
NO_DATA_DOWNLOAD
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

Existing S27 result artifacts remain:

```text
DIAGNOSTIC_ONLY_FAILURE_MAP_MATERIAL
```
