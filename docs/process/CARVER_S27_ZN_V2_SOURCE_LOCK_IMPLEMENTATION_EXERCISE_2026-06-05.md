# Carver S27 ZN V2 Source-Lock Implementation Exercise

Date: 2026-06-05

Status:

```text
PROCESS_ONLY_S27_ZN_V2_SOURCE_LOCK_IMPLEMENTATION_EXERCISE_UNIT_PASS_NOT_BACKTEST
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Authorization

Operator authorization:

```text
Operator authorizes S27_V2 source-lock implementation exercise, no provider/API, no downloads, no backtests, no OOS/Lockbox/Forward, no git actions.
```

This record authorizes no provider/API access, no data download, no diagnostic,
no backtest, no OOS, no Lockbox, no Forward, no tuning, no alpha claim, no
promotion, no Git staging, no commit, no push, no PR, no deployment, and no
trading.

## Source-Lock Dependency

Implementation follows:

```text
docs/process/CARVER_S27_ZN_BOOK_SOURCE_LOCK_2026-06-05.md
docs/process/CARVER_S27_ZN_SOURCE_LOCK_REAUDIT_RESULT_2026-06-05.md
docs/process/CARVER_S27_ZN_V2_LOCAL_DATA_CONTRACT_GATE_2026-06-05.md
```

The active gate is:

```text
S27_ZN_BOOK_SOURCE_LOCK_PASSED_FOR_V2_IMPLEMENTATION_EXERCISE
```

## Files Added

| File | Purpose | SHA256 |
|---|---|---|
| `src/carver/spine/s27_v2.py` | ZN-first S27 v2 source-lock primitives for daily runtime replay, forecast replay, desired position, adjacent limit-order plan, market-order cases, working-order/session transition state, one-hour-lag fills, row-replay step ledger bundles, multi-row replay aggregation over caller-supplied rows, cost ledgers, PnL ledgers, validation rows, and deterministic row hashes. | `567FC91106CBDE05A876708497C5A1C9290828A29A6A3B93AC0CD4386BEF751F` |
| `tests/test_s27_v2_source_lock_synthetic.py` | Synthetic unit tests for source-lock scalar, application order, sigma bridge, V/Q/M, strict-prior daily/hourly alignment, source-row readiness, level compatibility, zero-sign fail-closed behavior, desired position sizing, adjacent limit orders, cap-bound market cases, market orders, working-order/session transitions, roll-boundary fail-closed/reset assumption, one-hour-lag fills, both-side limit-touch ambiguity, positive cost enforcement, replay step ledger bundles, multi-row replay aggregation, transition-fact gates, validation/provenance hashes, cost ledgers, ISO trading-date gates, direct malformed-fill rejection, market/spread bundle rows, and PnL ledgers. | `E46D12D2DE03B9B1E5CEFDB3A4ACB1C9BE66BC2BBB430C63632905AA3E267225` |

## Implementation Boundaries

The v2 module is intentionally separate from old S27 diagnostic runners. It has
no provider client, no file parser, no runner entry point, and no backtest
entry point.

The module preserves these source-lock decisions:

- S26 scalar remains `9.3`.
- S27 scalar is book-estimated `AROUND_20` and implementation-frozen at `20.0`,
  not treated as a source-exact constant.
- Forecast replay ledger boundary is raw forecast -> sigma-price bridge ->
  risk-adjusted forecast -> EWMAC(16,64) veto -> V/Q/M multiplier -> scalar ->
  cap.
- Sigma price uses:

```text
previous_completed_daily_close_current_traded_contract * annual_percentage_sigma / 16
```

- Exact-zero trend or exact-zero mean-reversion sign cases fail closed.
- V/Q/M uses percentage sigma, ten-year rolling mean where available, expanding
  quantile history through current observation, and EWMA span 10 smoothing.
- Desired position uses capped forecast divided by `10` times base position.
- Execution planning emits adjacent-position single-lot limit orders when
  eligible and market orders when desired position is more than one contract
  from current position.
- Fill simulation requires exactly one-hour lag.
- Working-order state opens from an order plan and is transitioned one
  completed hour at a time.
- Normal session transitions carry unfilled working limits forward.
- End-of-day transitions cancel remaining working limits.
- Overnight-gap transitions cancel working limits and use market reset orders
  toward the desired rounded position.
- Roll-boundary transitions fail closed unless an explicit
  `ROLL_BOUNDARY_STATE_RESET_IMPLEMENTATION_ASSUMPTION_LOCKED` status is
  supplied; the explicit assumption cancels working limits without claiming
  book-native roll execution.
- If a one-hour OHLC bar touches both buy and sell limit sides, v2 fails closed
  because the intrabar sequence is unknown.
- Daily rows require exact prevalidated/local completed-row and level
  compatibility statuses.
- Hourly rows require exact prevalidated/local completed-row status.
- Forecast replay fails closed if the daily runtime row drifts from the daily
  input's current traded contract close or annual percentage sigma.
- Limit fills are commission-only.
- Market fills are commission plus normal bid-ask spread.
- Commission and normal spread inputs must be positive.
- Cost ledger rows are separated from fill rows.
- A one-step replay ledger bundle can be built from caller-supplied local or
  synthetic rows for exactly one decision row and the next completed hourly
  fill row.
- Source-input manifest rows bind daily source values, decision-hourly OHLC,
  next/fill-hourly OHLC, and both decision/fill provider-condition statuses.
- Daily/hourly compatibility rows bind the daily continuous close, current
  traded-contract close, hourly current price, sigma bridge price, annual
  percentage sigma, and exact compatibility status.
- The replay bundle emits source-input manifest rows, daily/hourly level
  compatibility rows, runtime replay rows, forecast rows, desired-position
  rows, order rows, fill rows, cost component rows, PnL rows, validation rows,
  and deterministic row-level SHA256 provenance rows.
- Empty artifact families receive deterministic provenance hash rows so that
  absent market, limit, fill, commission, or spread rows are explicit.
- Daily and hourly trading dates must be exact ISO calendar dates.
- Cost ledger construction rejects externally supplied malformed fills, including
  market fills without positive commission and positive normal spread.
- Multi-row replay aggregation can combine consecutive one-hour replay steps
  over caller-supplied rows only.
- Multi-row replay selects the latest strict-prior daily runtime row for each
  hourly decision and fails closed when none exists.
- Multi-row replay fails closed on unresolved carried working limits across
  normal same-session transitions; persistent working-order carry remains a
  separate source-lock problem.
- Transition labels must be supported by row facts: normal transitions require
  unchanged session/trading date, EOD and overnight resets require advanced
  session/trading date, and roll-boundary transitions require raw-symbol change
  plus the explicit roll reset assumption.
- Market-order ledger rows reflect executed transition orders; roll-boundary
  resets suppress unexecuted plan market orders.
- The replay bundle has no file reader, no provider client, no data downloader,
  no window loop, and no backtest entry point.
- PnL ledger rows require timestamp-aligned cost rows and remain unit-level
  primitives, not a backtest runner.

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

## Remaining Gates

Current local hostile audit status:

```text
S27_V2_REPLAY_STEP_LEDGER_BUNDLE_SLICE_LOCAL_HOSTILE_AUDIT_REMEDIATED_PASS
```

```text
S27_V2_MULTI_ROW_REPLAY_PLUMBING_SLICE_LOCAL_HOSTILE_AUDIT_REMEDIATED_PASS
```

Still required before any result interpretation:

- realistic row replay over a locked local ZN data contract;
- satisfaction of
  `docs/process/CARVER_S27_ZN_V2_LOCAL_DATA_CONTRACT_GATE_2026-06-05.md`;
- separate local hostile audit of any file/CSV parser, data-contract adapter,
  or window runner;
- explicit operator authorization before any provider/API access, data
  download, diagnostic, backtest, OOS, Lockbox, Forward, tuning, Git action,
  promotion, deployment, or trading.

Existing S27 results remain:

```text
DIAGNOSTIC_ONLY_FAILURE_MAP_MATERIAL
```
