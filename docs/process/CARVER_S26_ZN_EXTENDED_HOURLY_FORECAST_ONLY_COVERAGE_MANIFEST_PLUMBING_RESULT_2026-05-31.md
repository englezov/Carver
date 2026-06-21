# Carver S26 ZN Extended Hourly Forecast-Only Coverage Manifest Plumbing Result

Date: 2026-05-31

Status:

```text
PROCESS_AND_CODE_S26_ZN_EXTENDED_HOURLY_FORECAST_ONLY_COVERAGE_MANIFEST_PLUMBING_COMPLETE_NOT_DATA_AUTHORIZATION
```

## Scope

This result preserves machine-readable manifest plumbing for a later S26 ZN extended hourly forecast-only coverage gate.

Implemented code:

```text
src/carver/spine/s26_s27.py
src/carver/spine/__init__.py
tests/test_s26_s27_fast_mean_reversion_synthetic.py
```

New public objects:

```text
S26_ZN_EXTENDED_HOURLY_REQUEST_MANIFEST_STATUS
S26_ZN_EXTENDED_HOURLY_REQUEST_START_UTC
S26_ZN_EXTENDED_HOURLY_REQUEST_END_UTC
S26_ZN_EXTENDED_TARGET_COMPLETED_TRADING_DATES
S26_ZN_EXTENDED_HOURLY_REQUEST_OUTPUT_ROOT
S26ExtendedHourlyForecastOnlyCoverageManifest
build_s26_zn_extended_hourly_forecast_only_coverage_manifest
validate_s26_zn_extended_hourly_forecast_only_coverage_manifest
```

## Locked Manifest Shape

The manifest locks:

```text
provider: DATABENTO_HISTORICAL
dataset: GLBX.MDP3
schema: ohlcv-1h
stype_in: instrument_id
symbols: 42000661 only
row_id: APPENDIX_C_172_004
author_market_code: ZN
expected_raw_symbol: ZNM6
request_start_utc: 2026-04-12T00:00:00Z
request_end_utc: 2026-05-23T00:00:00Z
target_completed_trading_dates: 30 weekdays from 2026-04-13 through 2026-05-22
continuous_contracts_status: CLOSED
parent_symbols_status: CLOSED
raw_symbol_selector_status: CLOSED_CROSS_CHECK_ONLY
```

Purpose:

```text
EXPAND_S26_FORECAST_ONLY_COVERAGE_BEFORE_S27_TEST_GATE
```

Output boundary:

```text
FORECAST_ONLY_NO_DIAGNOSTIC_NO_BACKTEST_NO_POSITION
```

Sigma requirement:

```text
ONE_PREVALIDATED_NO_LOOKAHEAD_SIGMA_RUNTIME_PER_FORECAST_ROW_REQUIRED
```

## Fail-Closed Rules

The manifest validator fail-closes on:

```text
status drift
provider/dataset/schema/selector drift
symbol or raw-symbol drift
dated-contract identity drift
request start/end drift
target completed-trading-date drift
loss of original G_R1A target dates
purpose drift
sigma runtime requirement drift
output boundary drift
continuous/parent/raw-symbol selector opening
output-root drift
missing no-authorization atoms
```

## Current Dependency Status

```text
S26 extended coverage/window manifest plumbing: COMPLETE_PROCESS_ONLY
extended Databento request execution: NOT_OPEN
extended market-row parsing: NOT_OPEN
extended S26 forecast-series artifact execution: NOT_OPEN
S27 strategy test: NOT_OPEN
```

## Verification

Focused verification:

```text
python -m unittest tests.test_s26_s27_fast_mean_reversion_synthetic -v
```

Result:

```text
34 focused S26/S27 tests passed
```

Full repository verification:

```text
python -m unittest discover -s tests
```

Result:

```text
190 tests passed
```

Secret scan:

```text
rg -n "db-[A-Za-z0-9]{20,}" docs\process docs\researchops src tests
```

Result:

```text
NO_MATCHES
```

## Non-Authorization

This result authorizes no provider API access, no new data download, no market-row parsing, no real forecast-series execution, no diagnostics, no backtests, no returns, no PnL, no positions, no orders, no fills, no costs, no carry, no trend computation, no S27 real-data computation, no testing, no OOS, no Lockbox, no Forward, no CFD adapters, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.
