# Carver S26 ZN Hourly Databento Bridge Shape Gate

Date: 2026-05-30

Status:

```text
PROCESS_ONLY_CARVER_S26_ZN_HOURLY_DATABENTO_BRIDGE_SHAPE_GATE_NOT_DATA_NOT_FORECAST
```

## Purpose

Define the next five-step bridge from completed S26/S27 synthetic conformance toward the first source-faithful hourly real-data gate.

This is a shape gate only. It does not call Databento, download data, parse market rows, compute real forecasts, run diagnostics, run backtests, compute positions, compute costs, compute carry, compute trend sleeves, promote data, trade, deploy, or open Git operations.

## Five-Step Goal

```text
1. SOURCE_ANCHOR_ZN_FROM_BOOK
2. DEFINE_HOURLY_DATABENTO_REQUEST_SHAPE
3. LOCK_HOURLY_COMPLETED_BAR_SEMANTICS
4. PREPARE_TINY_AUTHORIZED_INTAKE_PATH
5. LATER_FEED_QUARANTINED_ZN_HOURLY_BARS_INTO_S26_FORECAST_OUTPUT_ONLY
```

The fifth step remains blocked until the hourly intake passes and the S26 real-data sigma-percent estimation atom is locked.

## Step 1: Source Anchor

Controlling book strategy:

```text
S26: Strategy twenty-six: Fast mean reversion
```

Source anchor:

```text
BOOK_WORKED_EXAMPLE: US 10-year future
BOOK_LOCATION: Fig. 81, p. 480, 00_Carver.pdf
LOCAL_APPENDIX_C_PATH: APPENDIX_C_172_004 / 10-year US / ZN
LANE_CLASS: SOURCE_NATIVE_FUTURES
```

Local Databento static locks currently available:

```text
coverage ledger: docs/researchops/provider_mappings/CARVER_APPENDIX_C_DATABENTO_PROVIDER_COVERAGE_AFTER_ALIAS_PATCH_2026-05-30.csv
row_id: APPENDIX_C_172_004
author_market_code: ZN
descriptive_name: 10-year US
dataset candidate: GLBX.MDP3
continuous coverage candidate: ZN.c.0
coverage classification: DATABENTO_EXACT_METADATA_MATCH
```

Current dated-contract static selection available from the daily foundation:

```text
ledger: docs/researchops/contract_identity/databento_appendix_c_contract_identity_static_lock_2026-05-30/ledger/CARVER_DATABENTO_APPENDIX_C_CONTRACT_IDENTITY_STATIC_LOCK_AND_DATED_SELECTION_LEDGER_2026-05-30.csv
selected_dated_raw_symbol: ZNM6
selected_instrument_id: 42000661
provider_exchange: XCBT
provider_currency: USD
active/listed status: PASS_ACTIVE_LISTED_AT_PROVIDER_METADATA_ASOF_FROM_DATABENTO_DEFINITION
contract identity status: STATIC_DATED_CONTRACT_SELECTED_BUT_CONTRACT_IDENTITY_REQUIRES_REVIEW_OR_FAIL_CLOSED
```

Guardrail:

```text
ZN IS THE ONLY FIRST REAL-DATA S26 WORKED-EXAMPLE CANDIDATE IN THIS GATE.
ZT, T-bills, 2-year Treasury notes, MES/SP500, and the 16-symbol daily pilot are not substitutes for this S26 worked-example gate.
```

## Step 2: Hourly Databento Request Shape

Official Databento documentation supports the following static request facts:

- Dataset identifiers use the `PUBLISHER.DATASET` form, including `GLBX.MDP3`.
- Historical time series requests support raw symbols, instrument IDs, parent symbols, and continuous symbols.
- OHLCV schemas include `ohlcv-1h`.
- For OHLCV bars, `ts_event` marks the inclusive start of the aggregation interval.
- If no trade occurs in an interval, Databento does not print a record.

Official docs:

```text
https://databento.com/docs/api-reference-historical/basics/datasets
https://databento.com/docs/schemas-and-data-formats/ohlcv
```

Future request shape, if separately authorized:

```text
provider: DATABENTO_HISTORICAL
dataset: GLBX.MDP3
schema: ohlcv-1h
stype_in: instrument_id
symbols: 42000661
expected_raw_symbol_roundtrip: ZNM6
continuous_contracts: CLOSED
parent_symbols: CLOSED
other_symbols: CLOSED
```

Target completed trading dates:

```text
2026-05-18 through 2026-05-22 inclusive
```

Provider request envelope for the future execution gate:

```text
request_start_utc: 2026-05-17T00:00:00Z
request_end_utc: 2026-05-23T00:00:00Z
```

The wider UTC envelope exists only to capture overnight session hours that may belong to the target completed trading dates. A later execution gate must preserve the raw envelope, explicitly map each row to a completed trading date, and label any non-target envelope row as `ENVELOPE_ONLY_NOT_TARGET_TRADING_DATE`. No row may be silently dropped.

## Step 3: Hourly Completed-Bar Semantics

Canonical timestamp policy for this bridge:

```text
provider_interval_start_utc = Databento ts_event
derived_completed_bar_end_utc = ts_event + 1 hour
forecast_input_close_timestamp = derived_completed_bar_end_utc
provider_ts_event_start_preserved = YES
```

Completed-bar policy:

```text
ACCEPT_ONLY_COMPLETED_HOURLY_INTERVALS
NO_PARTIAL_HOUR
NO_SYNTHETIC_FILL_FOR_NO_TRADE_HOURS
NO_INTERPOLATION
NO_DROP
NO_SUBSTITUTE
NO_REWEIGHT
```

Session/trading-date policy for a later execution gate:

```text
ROW_LEVEL_TRADING_DATE_AUTHORITY: must be explicitly derived from locked ZN/CME Treasury session evidence before strategy use
HOLIDAY_EARLY_CLOSE_POLICY: must be locked before strategy use
EXPECTED_HOUR_COUNT: must be derived before validation can pass
NO_TRADE_INTERVALS: must be recorded as missing/no-print intervals, not filled
```

S26 uses hourly closes for the first real-data bridge. It must not use daily `ohlcv-1d` rows, daily settlement rows, or the already-certified daily Appendix C archive as a substitute for hourly data.

## Step 4: Tiny Intake Path

Future quarantine root:

```text
docs/researchops/s26_s27_hourly_bridge/ZN_S26_WORKED_EXAMPLE/2026-05-18_2026-05-22/databento_ohlcv_1h_quarantine/
```

Required future layout:

```text
raw_provider_output/
raw_provider_metadata/
sanitized_bars/
validation/
provenance/
status/
hashes/
```

Required raw artifacts:

```text
Databento raw DBN or provider-native file
Databento provider CSV export or dataframe snapshot
symbology resolution metadata for 42000661 <-> ZNM6
definition metadata for instrument 42000661
request manifest
provider condition metadata if available for the request interval
```

Minimum sanitized schema:

```text
lane_class
strategy_context
provider
dataset
schema
stype_in
row_id
author_market_code
descriptive_name
instrument_id
raw_symbol
provider_ts_event_start_utc
derived_completed_bar_end_utc
completed_trading_date
open
high
low
close
volume
provider_condition_status
session_mapping_status
row_shape_status
duplicate_status
missing_hour_status
source_raw_sha256
source_definition_sha256
strategy_use_status
```

The future execution gate must fail closed unless:

- the request uses only `GLBX.MDP3`, `ohlcv-1h`, `instrument_id`, and `42000661`;
- raw symbol roundtrip proves `ZNM6`;
- every accepted row maps to the target completed trading-date window;
- every required hourly interval is accounted for as observed or explicitly no-print/missing according to the locked session policy;
- no duplicate `(instrument_id, provider_ts_event_start_utc)` rows exist;
- no non-ZN symbol or continuous contract appears;
- all rows preserve raw/source hashes and provenance.

## Step 5: Later S26 Forecast-Output Bridge

This shape gate does not authorize real-data S26 forecast computation.

A later explicit execution gate may create S26 forecast output only if all prerequisites pass:

```text
ZN hourly intake quarantine passes
ZN session/trading-date mapping passes
ZN provider-condition policy passes
S26 sigma_percent_t estimation atom is locked from the book/source
S26 forecast-only output boundary is explicitly authorized
```

Maximum allowed future output:

```text
provider_ts_event_start_utc
derived_completed_bar_end_utc
completed_trading_date
price_close
equilibrium_ewma_5
raw_forecast
sigma_price
risk_adjusted_forecast
scaled_forecast
capped_forecast
source_locks_status
```

Still forbidden in that later forecast-output gate:

```text
diagnostics
backtests
returns
PnL
Sharpe
drawdown
positions
orders
costs
carry
trend sleeve
S27 overlay
portfolio integration
OOS
Lockbox
Forward
deployment
trading
promotion
```

## Immediate Decision

The next executable gate, if the operator chooses to touch data later, is:

```text
G_R1A_ZN_S26_WORKED_EXAMPLE_DATABENTO_OHLCV_1H_TINY_QUARANTINE_INTAKE
```

That future gate requires explicit operator authorization because it uses Databento Historical and parses market rows.

## Non-Authorization

This file authorizes no provider API access, no data download, no market-row parsing, no real-data forecast computation, no diagnostics, no backtests, no positions, no costs, no carry, no trend computation, no S27 overlay, no volatility/risk calculations, no OOS, no Lockbox, no Forward, no CFD adapters, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.
