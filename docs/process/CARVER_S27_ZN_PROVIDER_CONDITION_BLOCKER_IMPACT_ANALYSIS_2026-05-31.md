# Carver S27 ZN Provider-Condition Blocker Impact Analysis

Date: 2026-05-31

Status:

```text
PROCESS_ONLY_IMPACT_ANALYSIS_NOT_BACKTEST_AUTHORIZATION
```

## Purpose

Record the exact impact of the Databento provider-condition blocker discovered in the S27 ZN 2022-2023 hourly quarantine archive, before any backtest execution or policy decision.

## Source Artifact

```text
docs/researchops/s26_s27_backtest_readiness/ZN_S27_SINGLE_INSTRUMENT/2022-01-01_2023-12-31/hourly_archive_quarantine/sanitized_hourly_bars/20260531_S27_ZN_2022_2023_OHLCV_1H_ARCHIVE_sanitized_quarantine_ohlcv_1h.csv
```

## Exact Blocked Row

```text
row_id: APPENDIX_C_172_004
author_market_code: ZN
raw_symbol: ZNH2
instrument_id: 768155
provider_ts_event_start_utc: 2022-01-02T23:00:00Z
derived_completed_bar_end_utc: 2022-01-03T00:00:00Z
completed_trading_date: 2022-01-03
provider_condition_status: PROVIDER_CONDITION_DEGRADED
strategy_use_status: QUARANTINE_PRESERVED_PROVIDER_CONDITION_BLOCKED_NOT_BACKTEST_READY
```

OHLCV values are preserved in quarantine but not strategy-ready:

```text
open: 130.328125
high: 130.34375
low: 130.234375
close: 130.34375
volume: 15862.0
```

## Impact

The blocker is at the very beginning of the target window:

```text
target window: 2022-01-01 through 2023-12-31
first affected completed trading date: 2022-01-03
affected rows: 1
available rows: 20899
degraded rows: 1
```

Because the row is the first observed Sunday-evening ZNH2 row for the first active completed trading date, using it silently would violate the provider-condition fail-closed rule. Dropping it silently would also violate the zero-silent-row-skip rule.

## Clean Decision Options

Recommended cleanest path:

```text
OPTION_C_REDUCE_BACKTEST_START_AFTER_BLOCKER
```

Retarget the effective strategy-facing backtest window to begin after the degraded row has no role in warmup, lineage, forecast, position, or return calculations. This preserves the original 2022-2023 archive as quarantine evidence, avoids silent row skipping, and avoids normalizing degraded provider evidence.

Other valid paths:

```text
OPTION_A_FAIL_CLOSED_FULL_BACKTEST_BLOCKED
```

Do not run the 2022-2023 backtest until a fully provider-condition-available archive exists.

```text
OPTION_B_EXCLUDE_DEGRADED_ROW_AND_RECORD_GAP
```

Preserve the degraded row in quarantine, exclude it from strategy-facing lineage with an explicit one-row exclusion ledger, and fail closed if that exclusion creates a completed-bar, warmup, lineage, forecast, or return gap.

## Recommendation Rationale

`OPTION_C` is preferred because the degraded row sits at the start boundary rather than inside the mature forecast period. A retargeted effective backtest start is cleaner than an in-window exclusion, provided the later execution gate proves the degraded row is not used for:

```text
EWMA(5) S26 warmup
S27 EWMAC(16,64) daily trend warmup
S27 V/Q/M volatility warmup
local roll/back-adjustment lineage
position sizing
returns/PnL
costs
```

## Non-Authorization

This analysis authorizes no provider API access, no data download, no market-row parsing beyond read-only inspection of the existing quarantine artifact, no diagnostics, no backtests, no forecasts, no positions, no costs, no carry, no OOS, no Lockbox, no Forward, no CFD adapters, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.
