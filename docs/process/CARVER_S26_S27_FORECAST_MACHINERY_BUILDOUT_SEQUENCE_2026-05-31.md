# Carver S26/S27 Forecast Machinery Buildout Sequence

Date: 2026-05-31

Status:

```text
PROCESS_ONLY_BUILDOUT_SEQUENCE_S27_TEST_FIRST_LATER_NOT_TEST_AUTHORIZATION
```

## Objective

Build S26 and S27 source-faithful forecast machinery before strategy testing. The later first strategy test target is S27, not S26.

## Five-Step Buildout

1. Close the ZN S26 bridge cleanly.

Status:

```text
G_R1A hourly ZN quarantine: PASS
G_R1B single S26 forecast-only row: PASS
hostile audit: PASS_WITH_NON_BLOCKING_CAUTIONS
```

2. Build S26 hourly forecast-series-only machinery.

Status:

```text
G_R1C forecast-series plumbing: COMPLETE
real extended G_R1E sigma-runtime ledger: PASS
real extended S26 forecast-series-only artifact execution: PASS
input_hourly_rows: 690
sigma_runtime_rows: 686
forecast_rows: 686
```

3. Expand S26 forecast-only coverage/window.

Status:

```text
S26 extended forecast-only coverage/window manifest plumbing: COMPLETE_PROCESS_ONLY
extended data intake/execution: PASS_QUARANTINE_ONLY_NOT_FORECAST_READY
accepted extended hourly rows: 690
completed trading dates: 30
rows per completed trading date: 23
provider condition: PROVIDER_CONDITION_AVAILABLE
forecast-series execution: PASS_AFTER_G_R1E_SIGMA_RUNTIME_LEDGER
```

Boundary:

```text
forecast fields only
no diagnostics/backtests/positions/costs/carry/trend/S27
```

Forecast-series artifacts:

```text
docs/process/CARVER_S26_ZN_EXTENDED_SIGMA_RUNTIME_AND_FORECAST_SERIES_EXECUTION_RESULT_2026-05-31.md
docs/process/CARVER_S26_ZN_EXTENDED_SIGMA_RUNTIME_AND_FORECAST_SERIES_LOCAL_LEAN_HOSTILE_AUDIT_2026-05-31.md
docs/researchops/s26_s27_hourly_bridge/ZN_S26_WORKED_EXAMPLE/2026-04-13_2026-05-22/forecast_series_only_output/2026-05-31/
```

Coverage/intake artifacts:

```text
docs/process/CARVER_S26_ZN_EXTENDED_HOURLY_FORECAST_ONLY_COVERAGE_SHAPE_GATE_DRAFT_2026-05-31.md
docs/process/CARVER_S26_ZN_EXTENDED_HOURLY_FORECAST_ONLY_COVERAGE_MANIFEST_PLUMBING_RESULT_2026-05-31.md
docs/process/CARVER_S26_ZN_EXTENDED_HOURLY_FORECAST_ONLY_COVERAGE_MANIFEST_LOCAL_LEAN_HOSTILE_AUDIT_2026-05-31.md
docs/process/CARVER_S26_ZN_EXTENDED_HOURLY_DATABENTO_INTAKE_RESULT_2026-05-31.md
docs/process/CARVER_S26_ZN_EXTENDED_HOURLY_DATABENTO_INTAKE_LOCAL_LEAN_HOSTILE_AUDIT_2026-05-31.md
docs/researchops/s26_s27_hourly_bridge/ZN_S26_WORKED_EXAMPLE/2026-04-13_2026-05-22/databento_ohlcv_1h_extended_forecast_only_quarantine/
```

4. Lock S26 execution semantics as design only.

Status:

```text
S26 execution semantics source lock: COMPLETE_DESIGN_ONLY
```

Artifacts:

```text
docs/process/CARVER_S26_FAST_MEAN_REVERSION_EXECUTION_SEMANTICS_SOURCE_GATE_DRAFT_2026-05-31.md
docs/process/CARVER_S26_EXECUTION_SEMANTICS_SOURCE_LOCK_RESULT_2026-05-31.md
docs/process/CARVER_S26_EXECUTION_SEMANTICS_SOURCE_LOCK_LOCAL_LEAN_HOSTILE_AUDIT_2026-05-31.md
```

It must lock:

```text
no buffering
limit-order treatment
forecast cadence versus execution cadence
completed-hourly-bar availability
no market-order cost assumption
no performance test
```

5. Build S27 dependencies and forecast-only machinery, then test S27 first later.

Required future gates:

```text
S27_EWMAC16_TREND_OVERLAY_REAL_HOURLY_SOURCE_GATE
S27_V_Q_M_VOL_ATTENUATION_REAL_HOURLY_SOURCE_GATE
S27_ZN_FORECAST_ONLY_SERIES_GATE
S27_FIRST_STRATEGY_TEST_GATE_LATER
```

Shape artifact:

```text
docs/process/CARVER_S27_REAL_HOURLY_FORECAST_ONLY_MACHINERY_SHAPE_GATE_DRAFT_2026-05-31.md
```

Plumbing artifact:

```text
docs/process/CARVER_S27_REAL_HOURLY_FORECAST_ONLY_HANDOFF_PLUMBING_RESULT_2026-05-31.md
docs/process/CARVER_S27_REAL_HOURLY_FORECAST_SERIES_ONLY_HANDOFF_PLUMBING_RESULT_2026-05-31.md
docs/process/CARVER_S27_EWMAC16_TREND_RUNTIME_LEDGER_PLUMBING_RESULT_2026-05-31.md
docs/process/CARVER_S27_V_Q_M_VOL_ATTENUATION_RUNTIME_LEDGER_PLUMBING_RESULT_2026-05-31.md
docs/process/CARVER_S27_V_Q_M_VOL_ATTENUATION_RUNTIME_LEDGER_LOCAL_LEAN_HOSTILE_AUDIT_2026-05-31.md
```

S27 remains dependent on S26 forecast machinery, EWMAC(16,64), and the S13-style volatility attenuation mechanism. S27 must not be tested until these dependencies have source-faithful real-hourly forecast-only artifacts and a separate test gate.

S27 scalar correction:

```text
S26 scalar: 9.3
S27 scalar: 20.0 per the Chapter 27 p. 502 scalar paragraph
correction artifacts:
docs/process/CARVER_S27_SCALAR_SOURCE_CORRECTION_2026-05-31.md
docs/process/CARVER_S27_SCALAR_SOURCE_CORRECTION_LOCAL_LEAN_HOSTILE_AUDIT_2026-05-31.md
```

Current S27 handoff status:

```text
forecast-only row handoff plumbing: COMPLETE
forecast-series handoff plumbing: COMPLETE
EWMAC16 trend runtime ledger plumbing: COMPLETE_PREVALIDATED_ONLY
V/Q/M volatility runtime ledger plumbing: COMPLETE_PREVALIDATED_ONLY
real EWMAC16 trend computation: PASS_DEV_RECON_RUNTIME_LEDGER_ONLY
S27 scalar source correction: PASS
real S13-style V/Q/M volatility computation: PASS_DEV_RECON_RUNTIME_LEDGER_ONLY
S27 forecast-series-only execution: PASS_NOT_TEST
S27 strategy test: NOT_OPEN
```

S27 ZN backtest-readiness chapter status:

```text
completed forecast machinery hostile audit: PASS_LOCAL_HOSTILE_AUDIT_NO_BLOCKING_FINDINGS
S27 ZN position/execution/cost semantics lock: PASS_NOT_BACKTEST
S27 ZN longer hourly archive window manifest: PROCESS_ONLY_NOT_DATA_AUTHORIZATION
S27 ZN quarantined Development/Reconciliation backtest path prep: PROCESS_ONLY_NOT_BACKTEST_AUTHORIZATION
readiness local hostile audit: PASS_S27_ZN_BACKTEST_READINESS_PATH_NOT_BACKTEST
```

Readiness artifacts:

```text
docs/process/CARVER_S26_S27_COMPLETED_FORECAST_MACHINERY_LOCAL_HOSTILE_AUDIT_2026-05-31.md
docs/process/CARVER_S27_ZN_SINGLE_INSTRUMENT_BACKTEST_READINESS_GATE_DRAFT_2026-05-31.md
docs/process/CARVER_S27_ZN_POSITION_EXECUTION_COST_SEMANTICS_LOCK_2026-05-31.md
docs/process/CARVER_S27_ZN_LONGER_HOURLY_DATABENTO_ARCHIVE_WINDOW_MANIFEST_2026-05-31.md
docs/process/CARVER_S27_ZN_QUARANTINED_DEV_BACKTEST_PATH_PREP_2026-05-31.md
docs/process/CARVER_S27_ZN_BACKTEST_READINESS_LOCAL_LEAN_HOSTILE_AUDIT_2026-05-31.md
```

S27 EWMAC16 source-gate artifacts:

```text
docs/process/CARVER_S27_EWMAC16_TREND_SOURCE_GATE_RESULT_2026-05-31.md
docs/process/CARVER_S27_EWMAC16_TREND_SOURCE_GATE_LOCAL_LEAN_HOSTILE_AUDIT_2026-05-31.md
```

ZN lifecycle/lineage repair probe artifacts:

```text
docs/process/CARVER_ZN_LOCAL_CONTINUOUS_DAILY_LIFECYCLE_EVIDENCE_AND_LINEAGE_REPAIR_GATE_DRAFT_2026-05-31.md
docs/process/CARVER_ZN_LOCAL_CONTINUOUS_DAILY_LIFECYCLE_EVIDENCE_AND_LINEAGE_REPAIR_GATE_DRAFT_LOCAL_LEAN_HOSTILE_AUDIT_2026-05-31.md
docs/process/CARVER_ZN_LOCAL_CONTINUOUS_DAILY_DATABENTO_DEFINITION_LIFECYCLE_PROBE_RESULT_2026-05-31.md
docs/process/CARVER_ZN_LOCAL_CONTINUOUS_DAILY_DATABENTO_DEFINITION_LIFECYCLE_PROBE_LOCAL_LEAN_HOSTILE_AUDIT_2026-05-31.md
docs/process/CARVER_ZN_LOCAL_CONTINUOUS_DAILY_LIFECYCLE_REPAIR_RESULT_2026-05-31.md
docs/process/CARVER_S27_ZN_EWMAC16_TREND_RUNTIME_EXECUTION_RESULT_2026-05-31.md
docs/process/CARVER_S27_ZN_EWMAC16_TREND_RUNTIME_LOCAL_LEAN_HOSTILE_AUDIT_2026-05-31.md
docs/researchops/s26_s27_hourly_bridge/ZN_S27_EWMAC16_TREND_DEPENDENCY/zn_lifecycle_databento_definition_probe_2026-05-31/
docs/researchops/s26_s27_hourly_bridge/ZN_S27_EWMAC16_TREND_DEPENDENCY/local_continuous_daily_lineage_2026-05-31/
docs/researchops/s26_s27_hourly_bridge/ZN_S27_EWMAC16_TREND_DEPENDENCY/ewmac16_trend_runtime_ledger_2026-05-31/
```

S27 V/Q/M real source gate artifacts:

```text
docs/process/CARVER_S27_V_Q_M_VOL_ATTENUATION_REAL_SOURCE_GATE_RESULT_2026-05-31.md
docs/process/CARVER_S27_V_Q_M_VOL_ATTENUATION_REAL_SOURCE_GATE_LOCAL_LEAN_HOSTILE_AUDIT_2026-05-31.md
docs/process/CARVER_S27_ZN_V_Q_M_TEN_YEAR_VOL_HISTORY_AND_RUNTIME_SHAPE_GATE_DRAFT_2026-05-31.md
docs/process/CARVER_S27_ZN_V_Q_M_TEN_YEAR_VOL_RUNTIME_EXECUTION_RESULT_2026-05-31.md
docs/process/CARVER_S27_ZN_V_Q_M_TEN_YEAR_VOL_RUNTIME_LOCAL_LEAN_HOSTILE_AUDIT_2026-05-31.md
docs/researchops/s26_s27_hourly_bridge/ZN_S27_V_Q_M_VOL_ATTENUATION/ten_year_vol_history_runtime_2026-05-31/
```

S27 forecast-series-only artifacts:

```text
docs/process/CARVER_S27_ZN_FORECAST_SERIES_ONLY_EXECUTION_RESULT_2026-05-31.md
docs/process/CARVER_S27_ZN_FORECAST_SERIES_ONLY_LOCAL_LEAN_HOSTILE_AUDIT_2026-05-31.md
docs/researchops/s26_s27_hourly_bridge/ZN_S27_FORECAST_SERIES_ONLY/2026-05-31/
```

Databento definition metadata locked ZNH6/ZNM6/ZNU6 activation, expiration, maturity, currency, exchange, asset, group, and instrument IDs. Official CME/CBOT static rule evidence then locked ZNH6/ZNM6 lifecycle blockers for the local Development/Reconciliation roll decision. The repaired ZN local continuous daily lineage emitted 175 rows, and the S27 EWMAC16 trend runtime ledger emitted 686 rows aligned one-for-one with the S26 forecast-series-only rows.

## Current Next Best Gate

```text
S27_ZN_LONGER_HOURLY_ARCHIVE_AND_DEV_RECON_BACKTEST_EXECUTION_GATE_LATER
```

The S26 extended forecast-series-only bridge exists. The S27 EWMAC16 source dependency is satisfied at Development/Reconciliation runtime-ledger-only scope. The S27 scalar has been corrected to use the Chapter 27 scalar around 20. The S27 V/Q/M runtime ledger has been emitted from a Databento ZN dated-contract ten-year daily risk-history path, and the S27 ZN forecast-series-only artifact now exists. The S27 ZN strategy-test/readiness path is now documented, with position/execution/cost semantics and the longer hourly archive manifest locked as process/readiness artifacts. The next aligned move is a separately authorized S27 ZN archive/backtest execution gate.

## Non-Authorization

This sequence records bounded Databento provider access for the locked ZN hourly S26 bridge and the locked ZN dated-contract daily S27 V/Q/M runtime dependency. It also records local S26 forecast-series-only, S27 EWMAC16 runtime, S27 V/Q/M runtime, and S27 forecast-series-only execution. It authorizes no additional provider API access, no additional data download, no wider market-row expansion, no diagnostics, no backtests, no returns, no PnL, no positions, no costs, no carry, no strategy testing, no OOS, no Lockbox, no Forward, no CFD adapters, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.
