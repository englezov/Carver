# Carver S26 ZN Hourly Request Manifest Plumbing Result

Date: 2026-05-30

Status:

```text
PROCESS_ONLY_REQUEST_MANIFEST_VALIDATION_PLUMBING_COMPLETE_NOT_DATA_AUTHORIZATION
```

## Purpose

Record the non-data plumbing added for the next S26 real-hourly bridge gate.

The purpose is to make the later Databento request fail closed before any provider call if it drifts away from Carver's Strategy 26 worked-example instrument:

```text
book anchor: US 10-year future, Fig. 81, p. 480
appendix_c_row: APPENDIX_C_172_004
author_market_code: ZN
provider: Databento Historical
dataset: GLBX.MDP3
schema: ohlcv-1h
stype_in: instrument_id
instrument_id: 42000661
expected_raw_symbol: ZNM6
```

## Machine-Readable Manifest

```text
docs/researchops/s26_s27_hourly_bridge/ZN_S26_WORKED_EXAMPLE/2026-05-18_2026-05-22/request_manifest/CARVER_S26_ZN_DATABENTO_OHLCV_1H_REQUEST_MANIFEST_2026-05-30.json
```

Manifest status:

```text
PROCESS_ONLY_REQUEST_MANIFEST_NOT_AUTHORIZATION
```

The manifest locks the future request to:

```text
dataset: GLBX.MDP3
schema: ohlcv-1h
stype_in: instrument_id
symbols: [42000661]
row_id: APPENDIX_C_172_004
author_market_code: ZN
expected_raw_symbol: ZNM6
start: 2026-05-17T00:00:00Z
end: 2026-05-23T00:00:00Z
target_completed_trading_dates: 2026-05-18 through 2026-05-22
continuous_contracts_status: CLOSED
parent_symbols_status: CLOSED
raw_symbol_selector_status: CLOSED_CROSS_CHECK_ONLY
```

## Local Validation Plumbing

Added local validation objects:

```text
S26DatabentoHourlyIntakeRequestManifest
validate_s26_zn_hourly_databento_request_manifest
```

The validator fails closed on:

- any dataset other than `GLBX.MDP3`;
- any schema other than `ohlcv-1h`;
- any selector other than `instrument_id`;
- any symbol set other than `[42000661]`;
- any raw-symbol expectation other than `ZNM6`;
- any continuous, parent-symbol, or raw-symbol selector opening;
- any target-window drift;
- any output-root drift;
- missing no-authorization guards.

Required no-authorization guard tokens include:

```text
NO_PROVIDER_API_ACCESS
NO_DATA_DOWNLOAD
NO_MARKET_ROW_PARSING
NO_DIAGNOSTICS
NO_BACKTESTS
NO_FORECAST_COMPUTATION
NO_POSITIONS
NO_GIT_OPERATIONS
```

## Test Result

Local tests were expanded to cover the manifest and scope-drift failures:

```text
python -m unittest tests.test_s26_s27_fast_mean_reversion_synthetic
Ran 16 tests
OK

python -m unittest discover -s tests
Ran 171 tests
OK
```

## Remaining Blockers

The active chapter is still not complete.

Remaining gates:

```text
G_R1A_ZN_S26_WORKED_EXAMPLE_DATABENTO_OHLCV_1H_TINY_QUARANTINE_INTAKE
PREVALIDATED_S26_ZN_SIGMA_PERCENT_RUNTIME_VALUE
G_R1B_ZN_S26_HOURLY_SIGMA_PERCENT_AND_FORECAST_ONLY_HANDOFF
```

## Non-Authorization

This record authorizes no provider API access, no data download, no market-row parsing, no real-data forecast computation, no diagnostics, no backtests, no positions, no costs, no carry, no trend computation, no S27 overlay, no volatility/risk calculations, no OOS, no Lockbox, no Forward, no CFD adapters, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.
