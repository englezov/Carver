# Carver S27 ZN Provider-Condition Blocker Option C Resolution

Date: 2026-05-31

Status:

```text
PASS_OPTION_C_EFFECTIVE_WINDOW_PROVIDER_CONDITION_AVAILABLE_NOT_BACKTEST_AUTHORIZATION
```

## Purpose

Resolve the Databento provider-condition blocker in the already downloaded S27 ZN 2022-2023 hourly quarantine archive without treating degraded provider evidence as normal and without silently dropping rows.

This is a local/process resolution only. It does not authorize a backtest.

## Decision

Selected path:

```text
OPTION_C_REDUCE_BACKTEST_START_AFTER_PROVIDER_CONDITION_BLOCKER
```

The full archive remains preserved:

```text
source archive window: 2022-01-01 through 2023-12-31
```

The strategy-facing effective window is retargeted to:

```text
effective strategy window: 2022-01-04 through 2023-12-31
```

The early excluded block is explicit and ledgered. It is not a silent row skip.

## Source Archive

```text
docs/researchops/s26_s27_backtest_readiness/ZN_S27_SINGLE_INSTRUMENT/2022-01-01_2023-12-31/hourly_archive_quarantine/sanitized_hourly_bars/20260531_S27_ZN_2022_2023_OHLCV_1H_ARCHIVE_sanitized_quarantine_ohlcv_1h.csv
```

Source archive status before this resolution:

```text
FAIL_CLOSED_PROVIDER_CONDITION_BLOCKERS_PRESENT_NOT_BACKTEST_READY
```

Provider-condition counts:

```text
PROVIDER_CONDITION_AVAILABLE: 20899
PROVIDER_CONDITION_DEGRADED: 1
```

## Exclusion Result

Generated strategy-facing artifacts:

```text
docs/researchops/s26_s27_backtest_readiness/ZN_S27_SINGLE_INSTRUMENT/2022-01-01_2023-12-31/hourly_archive_quarantine/provider_condition_resolution/strategy_facing_hourly_bars/20260531_S27_ZN_2022_2023_PROVIDER_CONDITION_OPTION_C_strategy_facing_available_ohlcv_1h.csv

docs/researchops/s26_s27_backtest_readiness/ZN_S27_SINGLE_INSTRUMENT/2022-01-01_2023-12-31/hourly_archive_quarantine/provider_condition_resolution/exclusion_ledger/20260531_S27_ZN_2022_2023_PROVIDER_CONDITION_OPTION_C_exclusion_ledger.csv

docs/researchops/s26_s27_backtest_readiness/ZN_S27_SINGLE_INSTRUMENT/2022-01-01_2023-12-31/hourly_archive_quarantine/provider_condition_resolution/status/20260531_S27_ZN_2022_2023_PROVIDER_CONDITION_OPTION_C_status.json
```

Counts:

```text
source quarantine rows: 20900
strategy-facing provider-condition-available rows: 20870
excluded rows: 30
excluded degraded rows: 1
```

Excluded rows by source symbol/date:

```text
ZNH2 2022-01-03 PROVIDER_CONDITION_DEGRADED: 1
ZNH2 2022-01-03 PROVIDER_CONDITION_AVAILABLE: 22
ZNM2 2022-01-03 PROVIDER_CONDITION_AVAILABLE: 7
```

The additional available rows on the excluded completed trading date are excluded because the effective strategy-facing window starts after the blocker. This avoids admitting a partial first completed trading date into warmup, lineage, forecast, position, return, or cost calculations.

## Boundary

The strategy-facing file is still not a backtest artifact. It is a provider-condition-available input layer for a later separately authorized retargeted backtest gate.

No provider API access, new data download, diagnostics, backtests, forecasts, positions, costs, OOS, Lockbox, Forward, deployment, trading, promotion, Git operations, or remote operations occurred in this resolution.

## Next Gate

```text
S27_ZN_2022_2023_DEV_RECON_BACKTEST_EXECUTION_GATE_RETARGETED_EFFECTIVE_WINDOW
```

That later gate must prove that no excluded row participates in:

```text
S26 EWMA(5) equilibrium warmup
S27 EWMAC(16,64) trend runtime
S27 V/Q/M volatility attenuation runtime
local roll/back-adjustment lineage
position sizing
returns/PnL
costs
```

## Non-Authorization

This artifact authorizes no provider API access, no new data download, no diagnostics, no backtests, no forecasts, no positions, no costs, no carry, no trend sleeve integration, no OOS, no Lockbox, no Forward, no CFD adapters, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.
