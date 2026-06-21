# S27 ZN V2 Replay Scaffold GPT P1 Fail-Closed Schema Patch Record

Date: 2026-06-06

Status:

```text
PROCESS_ONLY_S27_ZN_V2_REPLAY_SCAFFOLD_GPT_P1_FAIL_CLOSED_SCHEMA_PATCH_RECORD_NOT_REPLAY_OR_BACKTEST_AUTHORIZATION
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Authorization Boundary

Operator authorization received:

```text
Operator authorizes S27_V2 replay scaffold GPT P1 fail-closed schema patch only, covering source-row/forecast positivity, trend-veto/zero/cap invariants, and exact next-completed fill-row or session-gap proof scaffolding, no provider/API, no downloads, no parser/file replay execution, no diagnostics, no backtests, no OOS/Lockbox/Forward, no git actions, no adapter work, no deployment, no trading, no promotion.
```

This record documents a narrow scaffold patch only. It authorizes and performed no provider/API calls, no downloads, no parser/file replay execution, no diagnostics, no tests/backtests, no OOS, no Lockbox, no Forward, no Git actions, no adapter work, no deployment, no trading, no promotion, and no result interpretation.

## Source Finding

GPT external hostile-audit synthesis:

```text
docs/process/CARVER_S27_ZN_V2_GPT_LOCALLY_REAUDITED_REPLAY_SCAFFOLD_EXTERNAL_AUDIT_SYNTHESIS_2026-06-06.md
```

Open P1 findings patched:

```text
P1_SOURCE_ROW_AND_FORECAST_POSITIVITY
P1_TREND_ZERO_VETO_AND_CAP_INVARIANTS
P1_EXACT_NEXT_COMPLETED_FILL_ROW_OR_SESSION_GAP_PROOF
```

## Patched Files

```text
src/carver/spine/s27_v2_replay/source_rows.py
src/carver/spine/s27_v2_replay/forecast.py
src/carver/spine/s27_v2_replay/transitions.py
src/carver/spine/s27_v2_replay/fills.py
```

## Patch Summary

Source-row and forecast positivity:

- `LocalDailySourceRow.close_price` now requires a positive value.
- `LocalDailySourceRow.annual_percentage_sigma` now requires a positive value.
- `LocalHourlySourceRow.close_price` now requires a positive value.
- `ForecastReplayLedgerRow.sigma_bridge_price_value` now requires a positive value.
- `ForecastReplayLedgerRow.annual_percentage_sigma_value` now requires a positive value.
- `ForecastReplayLedgerRow.sigma_price_value` now requires a positive value.
- `ForecastReplayLedgerRow.relative_volatility_v_value`, `raw_volatility_multiplier_value`, and `ewma10_multiplier_m_value` now require positive values.

Trend-veto, zero-state, and cap fail-closed guards:

- Added a nonzero sign helper for source-locked nonzero forecast/trend signs.
- `EWMAC16/64` trend value must be nonzero and its explicit sign must match the value.
- `EWMAC16/64` trend sign no longer accepts unresolved `ZERO`.
- Pre-veto risk-adjusted forecast must be nonzero until a zero-policy is separately source-locked.
- Agreeing trend/mean-reversion signs require `PERMIT_MEAN_REVERSION` and preservation of the pre-veto forecast.
- Opposing trend/mean-reversion signs require `ZERO_FORECAST_BY_TREND_VETO` and zero post-veto forecast.
- `capped_forecast_value` must be in `[-20, 20]`.

Exact next-completed fill-row or session-gap proof scaffolding:

- `WorkingOrderTransitionLedgerRow` now carries `next_completed_hourly_fill_row_hash`, `fill_lag_reason_code`, and optional `session_gap_proof_hash`.
- `NORMAL_ONE_HOUR_LAG` requires `EXACT_NEXT_COMPLETED_HOURLY_ROW`, exactly one hour between decision and fill timestamps, and no session-gap proof.
- `EOD_OVERNIGHT_RECOMPUTE` requires `SESSION_GAP_OVERNIGHT_NEXT_COMPLETED_HOURLY_ROW` and a session-gap proof hash.
- `ROLL_BOUNDARY` requires `ROLL_SESSION_GAP_NEXT_COMPLETED_HOURLY_ROW` and a session-gap proof hash.
- `FillLedgerRow` now carries `next_completed_hourly_fill_row_hash` and requires `fill_decision_source_row_hash` to equal that next completed hourly fill-row hash.

## Static Inspection Result

Static inspection performed:

```text
STATIC_TEXT_AND_FILE_INVENTORY_ONLY
```

Inspection found:

```text
SOURCE_ROW_POSITIVITY_MARKERS_PRESENT
FORECAST_POSITIVITY_MARKERS_PRESENT
TREND_ZERO_VETO_CAP_FAIL_CLOSED_MARKERS_PRESENT
NEXT_COMPLETED_HOURLY_FILL_ROW_MARKERS_PRESENT
SESSION_GAP_PROOF_MARKERS_PRESENT
NO_PROVIDER_API_DOWNLOAD_BACKTEST_DIAGNOSTIC_SUBPROCESS_CLI_FILE_OPEN_SURFACE_FOUND_BY_TEXT_SCAN
```

Package file count remained:

```text
19
```

Python import, compile, unit tests, parser execution, file replay, diagnostics, and backtests were intentionally not run under this authorization.

## Next Gate

The standing local hostile-audit pre-approval rule permits a local hostile re-audit of this narrow patch. Any external audit handoff, parser/file replay work, diagnostics, backtests, data access, Git actions, adapter work, deployment, trading, promotion, or result interpretation still requires its own proper gate.
