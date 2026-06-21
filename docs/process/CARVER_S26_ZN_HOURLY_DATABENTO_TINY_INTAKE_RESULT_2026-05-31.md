# Carver S26 ZN Hourly Databento Tiny Intake Result

Date: 2026-05-31

Status:

```text
PASS_ZN_S26_HOURLY_OHLCV_1H_QUARANTINE_ONLY_NOT_FORECAST_READY
```

## Gate

```text
G_R1A_ZN_S26_WORKED_EXAMPLE_DATABENTO_OHLCV_1H_TINY_QUARANTINE_INTAKE
```

## Executed Request

The operator opened the Databento gate. The execution used only the locked request manifest:

```text
docs/researchops/s26_s27_hourly_bridge/ZN_S26_WORKED_EXAMPLE/2026-05-18_2026-05-22/request_manifest/CARVER_S26_ZN_DATABENTO_OHLCV_1H_REQUEST_MANIFEST_2026-05-30.json
```

Request:

```text
provider: Databento Historical
dataset: GLBX.MDP3
schema: ohlcv-1h
stype_in: instrument_id
symbol: 42000661
expected_raw_symbol: ZNM6
start: 2026-05-17T00:00:00Z
end: 2026-05-23T00:00:00Z
```

No continuous contract, parent symbol, substitute symbol, wider date range, wider dataset, or alternate schema was requested.

## Result

```text
raw_provider_dataframe_rows: 115
definition_metadata_rows: 7
accepted_quarantine_rows: 115
completed_trading_date_counts:
  2026-05-18: 23
  2026-05-19: 23
  2026-05-20: 23
  2026-05-21: 23
  2026-05-22: 23
provider_condition_status_counts:
  PROVIDER_CONDITION_AVAILABLE: 115
```

Completed-bar policy:

```text
provider ts_event interval start preserved
derived_completed_bar_end_utc = provider_ts_event_start_utc + 1 hour
```

Completed trading-date policy for this locked observed ZN slice:

```text
UTC hour >= 22 maps to the next completed trading date.
UTC hour < 22 maps to the same UTC date.
No row maps outside 2026-05-18 through 2026-05-22.
```

## Artifact Root

```text
docs/researchops/s26_s27_hourly_bridge/ZN_S26_WORKED_EXAMPLE/2026-05-18_2026-05-22/databento_ohlcv_1h_quarantine/
```

Key artifacts:

```text
raw_provider_output/20260531_G_R1A_ZN_S26_OHLCV_1H_TINY.dbn
raw_provider_output/20260531_G_R1A_ZN_S26_OHLCV_1H_TINY_provider_dataframe.csv
raw_provider_output/20260531_G_R1A_ZN_S26_OHLCV_1H_TINY_parser_snapshot.csv
raw_provider_metadata/20260531_G_R1A_ZN_S26_OHLCV_1H_TINY_definition.dbn
raw_provider_metadata/20260531_G_R1A_ZN_S26_OHLCV_1H_TINY_definition_dataframe.csv
raw_provider_metadata/20260531_G_R1A_ZN_S26_OHLCV_1H_TINY_symbology_instrument_id_to_raw_symbol.json
raw_provider_metadata/20260531_G_R1A_ZN_S26_OHLCV_1H_TINY_dataset_condition.json
sanitized_bars/20260531_G_R1A_ZN_S26_OHLCV_1H_TINY_sanitized_quarantine_ohlcv_1h.csv
validation/20260531_G_R1A_ZN_S26_OHLCV_1H_TINY_row_validation.json
status/20260531_G_R1A_ZN_S26_OHLCV_1H_TINY_raw_request_status.json
status/20260531_G_R1A_ZN_S26_OHLCV_1H_TINY_quarantine_intake_status.json
provenance/20260531_G_R1A_ZN_S26_OHLCV_1H_TINY_request_provenance.json
hashes/20260531_G_R1A_ZN_S26_OHLCV_1H_TINY_sha256.json
```

## Boundary

The accepted rows remain:

```text
QUARANTINE_ONLY_NOT_FORECAST_READY
```

This gate did not compute S26 forecasts. The next required gate remains:

```text
G_R1B_ZN_S26_HOURLY_SIGMA_PERCENT_AND_FORECAST_ONLY_HANDOFF
```

Required blocker before forecast output:

```text
PREVALIDATED_S26_ZN_SIGMA_PERCENT_RUNTIME_VALUE
```

## Non-Authorization

This result authorizes no additional provider API access, no additional data download, no wider market-row parsing, no real-data forecast computation, no diagnostics, no backtests, no positions, no costs, no carry, no trend computation, no S27 overlay, no volatility/risk calculations, no OOS, no Lockbox, no Forward, no CFD adapters, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.
