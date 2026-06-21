# Carver S27 ZN 2022-2023 Hourly Databento Intake Result

Date: 2026-05-31

Status:

```text
FAIL_CLOSED_PROVIDER_CONDITION_BLOCKERS_PRESENT_NOT_BACKTEST_READY
```

## Scope Executed

Operator-authorized Databento intake was limited to the locked S27 ZN single-instrument Development/Reconciliation archive surface:

```text
lane: SOURCE_NATIVE_FUTURES
provider: DATABENTO_HISTORICAL
dataset: GLBX.MDP3
schema: ohlcv-1h
stype_in: raw_symbol
row_id: APPENDIX_C_172_004
author_market_code: ZN
request_start_utc: 2021-12-31T00:00:00Z
request_end_utc: 2024-01-01T00:00:00Z
target_completed_trading_date_start: 2022-01-01
target_completed_trading_date_end: 2023-12-31
raw_symbols: ZNH2, ZNM2, ZNU2, ZNZ2, ZNH3, ZNM3, ZNU3, ZNZ3, ZNH4
```

## Artifacts

Root:

```text
docs/researchops/s26_s27_backtest_readiness/ZN_S27_SINGLE_INSTRUMENT/2022-01-01_2023-12-31/hourly_archive_quarantine/
```

Key files:

```text
manifest/20260531_S27_ZN_2022_2023_OHLCV_1H_ARCHIVE_request_manifest.json
raw_provider_output/20260531_S27_ZN_2022_2023_OHLCV_1H_ARCHIVE_<raw_symbol>.dbn
raw_provider_output/20260531_S27_ZN_2022_2023_OHLCV_1H_ARCHIVE_<raw_symbol>_provider.csv
raw_provider_metadata/20260531_S27_ZN_2022_2023_OHLCV_1H_ARCHIVE_dataset_condition.json
raw_provider_metadata/20260531_S27_ZN_2022_2023_OHLCV_1H_ARCHIVE_<raw_symbol>_definition.*
raw_provider_metadata/20260531_S27_ZN_2022_2023_OHLCV_1H_ARCHIVE_<raw_symbol>_symbology_raw_symbol_to_instrument_id.json
sanitized_hourly_bars/20260531_S27_ZN_2022_2023_OHLCV_1H_ARCHIVE_sanitized_quarantine_ohlcv_1h.csv
validation/20260531_S27_ZN_2022_2023_OHLCV_1H_ARCHIVE_row_validation.json
status/20260531_S27_ZN_2022_2023_OHLCV_1H_ARCHIVE_quarantine_intake_status.json
provenance/20260531_S27_ZN_2022_2023_OHLCV_1H_ARCHIVE_provenance.json
hashes/20260531_S27_ZN_2022_2023_OHLCV_1H_ARCHIVE_sha256.json
```

## Row Counts

```text
accepted_quarantine_rows: 20900
ZNH2: 1210
ZNM2: 2504
ZNU2: 2749
ZNZ2: 2640
ZNH3: 2578
ZNM3: 2540
ZNU3: 2650
ZNZ3: 2570
ZNH4: 1459
```

## Provider Condition Blocker

Databento metadata reported one degraded provider-condition date:

```text
2022-01-02: degraded
```

The sanitized archive preserves the affected row, but marks it:

```text
QUARANTINE_PRESERVED_PROVIDER_CONDITION_BLOCKED_NOT_BACKTEST_READY
```

Provider-condition counts:

```text
PROVIDER_CONDITION_AVAILABLE: 20899
PROVIDER_CONDITION_DEGRADED: 1
```

Therefore the archive is preserved as source-native quarantine evidence, but it is not backtest-ready. A separate provider-condition blocker decision must either fail closed the affected completed trading date/window or explicitly authorize a narrowly documented exclusion policy before any backtest execution.

## Boundary

No diagnostics, backtests, forecasts, positions, costs, carry, OOS, Lockbox, Forward, deployment, trading, promotion, Git operations, or remote repository operations were run.

## Next Gate

```text
S27_ZN_PROVIDER_CONDITION_BLOCKER_DECISION_BEFORE_BACKTEST_EXECUTION
```

