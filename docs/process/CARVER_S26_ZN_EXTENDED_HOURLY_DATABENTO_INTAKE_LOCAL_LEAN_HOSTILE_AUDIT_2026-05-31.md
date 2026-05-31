# Carver S26 ZN Extended Hourly Databento Intake Local Lean Hostile Audit

Date: 2026-05-31

Mode: local hostile audit. No new provider request, no market-row expansion beyond the already generated quarantine artifacts, no diagnostics, no backtests, no forecasts, no positions, no costs, no carry, no trend, no S27 overlay, no OOS, no Lockbox, no Forward, no deployment, no trading, no promotion, no Git operation.

Audited artifacts:

```text
docs/process/CARVER_S26_ZN_EXTENDED_HOURLY_FORECAST_ONLY_COVERAGE_SHAPE_GATE_DRAFT_2026-05-31.md
docs/process/CARVER_S26_ZN_EXTENDED_HOURLY_FORECAST_ONLY_COVERAGE_MANIFEST_PLUMBING_RESULT_2026-05-31.md
docs/process/CARVER_S26_ZN_EXTENDED_HOURLY_DATABENTO_INTAKE_RESULT_2026-05-31.md
docs/researchops/s26_s27_hourly_bridge/ZN_S26_WORKED_EXAMPLE/2026-04-13_2026-05-22/databento_ohlcv_1h_extended_forecast_only_quarantine/
tools/databento/carver_s26_zn_extended_hourly_intake.py
```

## Findings

Critical: none.

High: none.

Medium: none.

Low:

```text
L-1: The completed-trading-date mapping remains the same locked observed ZN hourly convention used in G_R1A: UTC hour >= 22 maps to the next completed trading date. This is acceptable for the current ZN extended bridge because the result remains quarantine-only and not forecast-ready. A later production-grade hourly session policy still requires a separate source lock before broader instruments or strategy tests.
```

## Scope Checks

The executed request stayed inside the locked manifest:

```text
dataset: GLBX.MDP3
schema: ohlcv-1h
stype_in: instrument_id
symbol: 42000661 only
raw symbol cross-check: ZNM6
request window: 2026-04-12T00:00:00Z through 2026-05-23T00:00:00Z
continuous contracts: closed
parent symbols: closed
```

The quarantine ledgers report:

```text
raw_provider_dataframe_rows: 690
accepted_quarantine_rows: 690
completed_trading_date_counts: 30 dates x 23 rows
provider_condition_status_counts: PROVIDER_CONDITION_AVAILABLE = 690
duplicate_ts_event_status: PASS_NO_DUPLICATES
strategy_use_status: QUARANTINE_ONLY_NOT_FORECAST_READY
```

The boundary is held:

```text
diagnostics_run: NO
backtests_run: NO
forecasts_run: NO
positions_run: NO
```

## Verdict

```text
BLOCKING_FINDINGS: NO
AUDIT_DISPOSITION: PASS_G_R1D_ZN_S26_EXTENDED_HOURLY_QUARANTINE_INTAKE_SCOPE
NEXT_REQUIRED_GATE: ONE_PREVALIDATED_NO_LOOKAHEAD_SIGMA_RUNTIME_PER_FORECAST_ROW_REQUIRED
```
