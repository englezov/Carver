# Carver S26 ZN Hourly Databento Tiny Intake Lean Hostile Audit

Date: 2026-05-31

Status:

```text
LOCAL_LEAN_HOSTILE_AUDIT_RESULT_G_R1A_PASS_QUARANTINE_ONLY_NOT_FORECAST_READY
```

Audited result:

```text
docs/process/CARVER_S26_ZN_HOURLY_DATABENTO_TINY_INTAKE_RESULT_2026-05-31.md
docs/researchops/s26_s27_hourly_bridge/ZN_S26_WORKED_EXAMPLE/2026-05-18_2026-05-22/databento_ohlcv_1h_quarantine/
```

## Findings

### Critical

None.

The Databento request was bounded to the locked manifest:

```text
GLBX.MDP3 / ohlcv-1h / stype_in=instrument_id / symbol=42000661 / 2026-05-17T00:00:00Z through 2026-05-23T00:00:00Z
```

No continuous contract, parent symbol, substitute symbol, alternate dataset, alternate schema, or wider date window was requested.

### High

None.

The quarantine validation accepted 115 rows and mapped them into exactly five completed trading dates:

```text
2026-05-18: 23
2026-05-19: 23
2026-05-20: 23
2026-05-21: 23
2026-05-22: 23
```

All accepted rows carry:

```text
PROVIDER_CONDITION_AVAILABLE
QUARANTINE_ONLY_NOT_FORECAST_READY
```

### Medium

M-1. The bridge remains intentionally incomplete for forecast output.

The current pass is quarantine-only. Forecast output remains blocked until:

```text
PREVALIDATED_S26_ZN_SIGMA_PERCENT_RUNTIME_VALUE
G_R1B_ZN_S26_HOURLY_SIGMA_PERCENT_AND_FORECAST_ONLY_HANDOFF
```

This is not a defect in G_R1A. It is the correct boundary: hourly prices are now quarantined, but S26 still requires the source-faithful sigma-percent input before any forecast can be emitted.

## Negative Evidence

The execution recorded:

```text
diagnostics_run: NO
backtests_run: NO
forecasts_run: NO
positions_run: NO
```

No costs, carry, trend computation, S27 overlay, risk calculation, OOS, Lockbox, Forward, deployment, trading, promotion, Git operation, or remote repository operation was performed.

## Disposition

```text
BLOCKING_FINDINGS: NO
AUDIT_DISPOSITION: PASS_G_R1A_ZN_S26_HOURLY_DATABENTO_TINY_INTAKE_QUARANTINE_ONLY_NOT_FORECAST_READY
GOAL_STATUS: PROGRESS_ONLY_NOT_COMPLETE
NEXT_REQUIRED_GATE: G_R1B_ZN_S26_HOURLY_SIGMA_PERCENT_AND_FORECAST_ONLY_HANDOFF
```

## Non-Authorization

This audit authorizes no additional provider API access, no additional data download, no wider market-row parsing, no real-data forecast computation, no diagnostics, no backtests, no positions, no costs, no carry, no trend computation, no S27 overlay, no volatility/risk calculations, no OOS, no Lockbox, no Forward, no CFD adapters, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.
