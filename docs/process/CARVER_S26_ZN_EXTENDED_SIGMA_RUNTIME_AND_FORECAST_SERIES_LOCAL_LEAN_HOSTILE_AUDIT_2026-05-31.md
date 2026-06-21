# Carver S26 ZN Extended Sigma Runtime And Forecast-Series Local Lean Hostile Audit

Date: 2026-05-31

Mode: local hostile audit. No provider API access, no data download, no market-row expansion, no diagnostics, no backtests, no positions, no costs, no carry, no trend, no S27 overlay, no OOS, no Lockbox, no Forward, no deployment, no trading, no promotion, no Git operation.

Audited artifacts:

```text
docs/process/CARVER_S26_ZN_EXTENDED_SIGMA_RUNTIME_AND_FORECAST_SERIES_EXECUTION_RESULT_2026-05-31.md
docs/researchops/s26_s27_hourly_bridge/ZN_S26_WORKED_EXAMPLE/2026-04-13_2026-05-22/forecast_series_only_output/2026-05-31/
tools/databento/carver_s26_zn_extended_sigma_and_forecast_series.py
```

## Findings

Critical: none.

High: none.

Medium: none.

Low:

```text
L-1: The sigma runtime method is explicitly the short-run EWMA32 current-risk component, not the full Carver S03 long/short blended position-sizing estimate. This is source-locked in the prior S26 sigma gate and correctly labeled here, but must not be reused later as a position-sizing risk estimate.
```

## Scope Checks

The execution used only local artifacts already present in the Carver workspace:

```text
hourly input: 690-row ZN ohlcv-1h quarantine artifact
daily input: ZNM6 full-available ohlcv-1d provider CSV
daily readiness: canonical 16-symbol manifest with degraded-row exclusions
provider API access: NO
new data download: NO
```

No-lookahead behavior is explicit:

```text
each hourly forecast row consumes latest 34 normal-provider-condition daily rows strictly before that row's completed trading date
same completed trading date daily row is excluded
degraded completed daily rows are excluded
```

Output boundary is held:

```text
sigma_runtime_rows: 686
forecast_rows: 686
diagnostics_run: NO
backtests_run: NO
positions_run: NO
costs_run: NO
carry_run: NO
trend_run: NO
s27_run: NO
```

Consistency check:

```text
final row as_of: 2026-05-22T21:00:00Z
final row sigma_percent_t: 0.04472077776691995
final row capped_forecast: -0.995560007091342
matches prior G_R1B single-row bridge
```

## Verdict

```text
BLOCKING_FINDINGS: NO
AUDIT_DISPOSITION: PASS_G_R1E_S26_ZN_EXTENDED_SIGMA_RUNTIME_AND_FORECAST_SERIES_ONLY_SCOPE
NEXT_REQUIRED_GATE: S27_EWMAC16_TREND_OVERLAY_REAL_HOURLY_SOURCE_GATE_OR_S27_V_Q_M_VOL_ATTENUATION_REAL_HOURLY_SOURCE_GATE
```
