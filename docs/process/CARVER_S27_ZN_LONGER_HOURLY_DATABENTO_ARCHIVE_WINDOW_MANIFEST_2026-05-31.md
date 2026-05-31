# Carver S27 ZN Longer Hourly Databento Archive Window Manifest

Date: 2026-05-31

Status:

```text
PROCESS_ONLY_S27_ZN_BACKTEST_HOURLY_ARCHIVE_WINDOW_MANIFEST_NOT_DATA_AUTHORIZATION
```

## Purpose

Define the exact ZN hourly archive window required before a later separately authorized S27 ZN Development/Reconciliation backtest over 2022-2023.

This manifest is not data authorization.

## Provider Surface

```text
provider: DATABENTO_HISTORICAL
dataset: GLBX.MDP3
schema: ohlcv-1h
stype_in: raw_symbol
author_market_code: ZN
row_id: APPENDIX_C_172_004
```

## Target Completed Trading-Date Window

```text
target_completed_trading_date_start: 2022-01-01
target_completed_trading_date_end: 2023-12-31
```

Request envelope:

```text
request_start_utc: 2021-12-31T00:00:00Z
request_end_utc: 2024-01-01T00:00:00Z
```

Rationale:

```text
bounded to the operator-selected 2022-2023 Development/Reconciliation period
longer than the existing 2026-04-13 through 2026-05-22 forecast-only bridge
captures the ZN quarterly contracts needed for a local dated-contract chain across 2022-2023
large enough to expose roll, stale/missing, position, and turnover mechanics
still Development/Reconciliation only
```

## Required Dated-Contract Chain

```text
ZNH2
ZNM2
ZNU2
ZNZ2
ZNH3
ZNM3
ZNU3
ZNZ3
ZNH4
```

The chain is deliberately dated-contract based. Provider-built continuous contracts remain closed as source authority.

## Local Continuous Policy

```text
LOCAL_DATED_CONTRACT_CHAIN_REQUIRED_NO_PROVIDER_CONTINUOUS_FALLBACK
```

Before any later backtest, the execution gate must build or verify a local hourly lineage:

```text
source row -> dated contract -> roll plan -> local continuous row -> forecast row -> position row
```

## Provider Condition Policy

```text
PROVIDER_CONDITION_AVAILABLE_ONLY_ZERO_SILENT_ROW_SKIP
```

Every missing, degraded, or unresolved row/date must be preserved in validation artifacts and fail closed unless a separately audited rule allows exclusion.

## Output Root

```text
docs/researchops/s26_s27_backtest_readiness/ZN_S27_SINGLE_INSTRUMENT/2022-01-01_2023-12-31/hourly_archive_quarantine/
```

## Non-Authorization

This manifest authorizes no provider API access, no data download, no market-row parsing, no diagnostics, no backtests, no returns, no PnL, no forecasts, no positions, no orders, no fills, no costs, no carry, no OOS, no Lockbox, no Forward, no CFD adapters, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.
