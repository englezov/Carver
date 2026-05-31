# Carver S26/S27 Source Atoms And Machine Path

Status:

```text
SOURCE_NATIVE_FUTURES_S26_S27_MACHINE_PATH_AUDIT_PACKET
```

## Book-Source Atoms To Verify

### Part Four Frequency Boundary

Carver Part Four controls both S26 and S27. The relevant source atom is that Part Four strategies use a modified Part One position-management framework, but forecasts are generated more frequently and backtested on hourly data.

Audit page reference:

```text
00_Carver.pdf p.475
```

Required interpretation:

```text
S26/S27 require hourly source-native futures bars for real-data forecast/backtest work.
Daily Appendix C data alone is not source-frequency-compatible with S26/S27.
```

### S26 - Fast Mean Reversion

Book source atoms to verify:

```text
Strategy title: Strategy twenty-six: Fast mean reversion
Equilibrium: EWMA span 5 of prices
Raw forecast: Equilibrium - p_t
Risk adjustment: raw forecast divided by sigma_price_i_t
Forecast scalar: 9.3
Forecast cap: +/-20
No FDM: single rule
No buffering: fast mean reversion execution differs from daily strategy machinery
Execution note: limit-order style execution is source-relevant
```

Audit page references:

```text
00_Carver.pdf pp.476-481
```

### S27 - Safer Fast Mean Reversion

Book source atoms to verify:

```text
Strategy title: Strategy twenty-seven: Safer fast mean reversion
S27 inherits S26 stages unless explicitly changed
Trend overlay: EWMAC16, spans 16 and 64 days
Mean-reversion forecast must not oppose trend forecast
Volatility attenuation: S13-style V/Q/M dependency
Forecast scalar: inherited 9.3
Forecast cap: inherited +/-20
No forecast-combination block with trend/carry daily sleeves
```

Audit page references:

```text
00_Carver.pdf pp.499-509
```

## Machine Path Summary

The current machine path is:

```text
source atoms -> synthetic conformance -> ZN hourly intake/readiness -> daily sigma/trend/V/Q/M runtime -> S27 forecast rows -> M1-style position ladder -> Development/Reconciliation backtest rows
```

Key implementation files:

```text
src/carver/spine/s26_s27.py
tests/test_s26_s27_fast_mean_reversion_synthetic.py
tools/databento/carver_s27_zn_local_extended_daily_runtime_2022_2023.py
tools/databento/carver_s27_zn_2022_2023_retargeted_dev_recon_backtest.py
tools/databento/carver_s27_zn_m1_ladder_dev_recon_backtest.py
```

Key process records:

```text
docs/process/CARVER_S26_S27_MEAN_REVERSION_OPUS_AUDIT_RESULT_2026-05-30.md
docs/process/CARVER_S26_S27_SOURCE_ATOM_SHEET_2026-05-30.md
docs/process/CARVER_S26_S27_SYNTHETIC_CONFORMANCE_IMPLEMENTATION_RESULT_2026-05-30.md
docs/process/CARVER_S26_S27_COMPLETED_FORECAST_MACHINERY_LOCAL_HOSTILE_AUDIT_2026-05-31.md
docs/process/CARVER_S27_ZN_2022_2023_LOCAL_EXTENDED_DAILY_RUNTIME_RESULT_2026-05-31.md
docs/process/CARVER_S27_ZN_2022_2023_RETARGETED_DEV_RECON_BACKTEST_EXECUTION_RESULT_2026-05-31.md
docs/process/CARVER_S27_ZN_M1_LADDER_DEV_RECON_BACKTEST_RESULT_2026-05-31.md
docs/process/CARVER_S27_ZN_M1_LADDER_DEV_RECON_BACKTEST_LOCAL_LEAN_HOSTILE_AUDIT_2026-05-31.md
```

## Important Machine Corrections Since Earlier Work

The previous R2 comparison-fed M1 ladder result was rejected because the S27 forecast rows used stale daily runtime:

```text
source_vqm_completed_trading_date = 2020-12-21
first observed 2022 row = 2022-01-03T05:00:00Z
runtime lag = 378 days
disposition = SUPERSEDED_FAIL_CLOSED_STALE_DAILY_RUNTIME_DEPENDENCY
```

Corrective machine guards:

```text
MAX_SOURCE_RUNTIME_LAG_DAYS = 10
runtime_lag_days must be > 0
runtime_lag_days must be <= 10
accepted rows observed max lag = 1 day
```

Patched scripts containing stale-runtime guard:

```text
tools/databento/carver_s27_candidate_comparison_2022_2023.py
tools/databento/carver_s27_zn_2022_2023_retargeted_dev_recon_backtest.py
tools/databento/carver_s27_zn_m1_ladder_dev_recon_backtest.py
```

## Local Extended Daily Runtime

A local extended daily runtime was built to support strict prior S13-style V/Q/M across the 2022-2023 hourly backtest window without new provider access.

Artifact root:

```text
docs/researchops/s26_s27_backtest_readiness/ZN_S27_SINGLE_INSTRUMENT/2022-01-01_2023-12-31/local_extended_daily_runtime
```

Status:

```text
PASS_LOCAL_EXTENDED_DAILY_RUNTIME_DEV_RECON_ONLY
```

Critical caveat:

```text
This local extended daily runtime is Development/Reconciliation-only.
It is not production continuous-contract authority.
```

Construction summary:

```text
pre-2015 support history: R2 deduped local continuous daily ZN history
2015+ source: existing V/Q/M local continuous daily risk history
bridge day: 2015-01-01
constant bridge offset applied to pre-2015 support segment: -0.28125
extended daily rows: 4750
extended daily window: 2011-01-02 through 2026-05-22
V/Q/M rows: 2157
V/Q/M window: 2019-06-06 through 2026-05-22
```

Audit question:

```text
Is this support-history stitch clearly labeled as Dev/Reconciliation-only and not over-promoted?
```

