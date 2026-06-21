# Carver S26 ZN Hourly Databento Tiny Intake Execution Gate Draft

Date: 2026-05-30

Status:

```text
PROCESS_ONLY_EXECUTION_GATE_DRAFT_CARVER_S26_ZN_HOURLY_DATABENTO_TINY_INTAKE_NOT_AUTHORIZATION
```

## Purpose

Define the exact future operator-authorized Databento intake gate needed to move the S26 ZN hourly bridge from process shape to a quarantined hourly bar set.

This draft is not the execution. It exists so the later data gate can be short, bounded, and unambiguous.

## Gate Name

```text
G_R1A_ZN_S26_WORKED_EXAMPLE_DATABENTO_OHLCV_1H_TINY_QUARANTINE_INTAKE
```

## Source Anchor

```text
strategy: S26 fast mean reversion
book anchor: US 10-year future, Fig. 81, p. 480
appendix_c_row: APPENDIX_C_172_004
author_market_code: ZN
provider: Databento Historical
dataset: GLBX.MDP3
schema: ohlcv-1h
stype_in: instrument_id
instrument_id: 42000661
expected_raw_symbol: ZNM6
continuous_contracts: CLOSED
```

## Exact Future Request

The future execution must first validate the machine-readable request manifest:

```text
docs/researchops/s26_s27_hourly_bridge/ZN_S26_WORKED_EXAMPLE/2026-05-18_2026-05-22/request_manifest/CARVER_S26_ZN_DATABENTO_OHLCV_1H_REQUEST_MANIFEST_2026-05-30.json
```

Manifest status:

```text
PROCESS_ONLY_REQUEST_MANIFEST_NOT_AUTHORIZATION
```

The future execution gate may request only:

```text
dataset: GLBX.MDP3
schema: ohlcv-1h
symbols: 42000661
stype_in: instrument_id
start: 2026-05-17T00:00:00Z
end: 2026-05-23T00:00:00Z
```

Target completed trading dates:

```text
2026-05-18
2026-05-19
2026-05-20
2026-05-21
2026-05-22
```

The request envelope is wider than the target completed-date window only to capture overnight hours. The execution must preserve all provider rows in the envelope and label row disposition.

## Output Root

```text
docs/researchops/s26_s27_hourly_bridge/ZN_S26_WORKED_EXAMPLE/2026-05-18_2026-05-22/databento_ohlcv_1h_quarantine/
```

Required subfolders:

```text
raw_provider_output/
raw_provider_metadata/
sanitized_bars/
validation/
provenance/
status/
hashes/
```

## Required Raw Preservation

The future execution must preserve:

- raw Databento provider output in a provider-native or lossless local form;
- provider CSV/dataframe snapshot used by the local parser;
- request manifest with API key redacted;
- symbology resolution for `42000661` and `ZNM6`;
- definition metadata for instrument `42000661`;
- provider-condition metadata for the request interval if Databento exposes it for the interval;
- SHA256 for every raw, sanitized, metadata, validation, provenance, and status artifact.

## Sanitized Hourly OHLCV Schema

Minimum schema:

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
target_window_disposition
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

Allowed strategy-use status for this gate:

```text
QUARANTINE_ONLY_NOT_FORECAST_READY
```

## Validation Rules

The execution must fail closed if any of the following occurs:

- any symbol other than instrument `42000661` appears;
- raw symbol roundtrip is not `ZNM6`;
- dataset is not `GLBX.MDP3`;
- schema is not `ohlcv-1h`;
- a continuous, parent, or raw-symbol selector is used instead of the locked instrument ID;
- any row has non-finite or non-positive OHLC values;
- any row has negative volume;
- any duplicate `(instrument_id, provider_ts_event_start_utc)` appears;
- any provider timestamp is not UTC hour-aligned;
- any row lacks a derived completed-bar end timestamp equal to `ts_event + 1 hour`;
- any row cannot be mapped to target completed trading date, envelope-only, or fail-closed status;
- any expected target-window hourly interval is unresolved after the locked session template is applied.

No no-trade interval may be filled. A no-trade/no-print interval must be recorded as an observed provider absence under the session policy.

## Pass Condition

The gate can pass only as:

```text
PASS_ZN_S26_HOURLY_OHLCV_1H_QUARANTINE_ONLY_NOT_FORECAST_READY
```

Passing this gate means only that a quarantined ZN hourly bar set exists with source identity, timestamps, row shape, and provenance preserved. It does not mean the rows are ready for S26 forecast output.

## Next Gate After Pass

If this gate passes, the next gate is:

```text
G_R1B_ZN_S26_HOURLY_SIGMA_PERCENT_AND_FORECAST_ONLY_HANDOFF
```

That later gate must lock or fail-close the real-data `sigma_percent_t` estimation method before computing any S26 forecast output.

## Non-Authorization

This draft authorizes no Databento access, no data download, no market-row parsing, no real-data forecast computation, no diagnostics, no backtests, no positions, no costs, no carry, no trend computation, no S27 overlay, no volatility/risk calculations, no OOS, no Lockbox, no Forward, no CFD adapters, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.
