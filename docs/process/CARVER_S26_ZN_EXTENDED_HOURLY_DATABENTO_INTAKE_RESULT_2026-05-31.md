# Carver S26 ZN Extended Hourly Databento Intake Result

Date: 2026-05-31

Status:

```text
PASS_ZN_S26_EXTENDED_HOURLY_OHLCV_1H_QUARANTINE_ONLY_NOT_FORECAST_READY
```

## Gate

```text
G_R1D_ZN_S26_EXTENDED_DATABENTO_OHLCV_1H_FORECAST_ONLY_COVERAGE_QUARANTINE_INTAKE
```

## Executed Request

Operator authorized bounded Databento access for the locked S26 ZN extended hourly manifest only.

```text
provider: Databento Historical
dataset: GLBX.MDP3
schema: ohlcv-1h
stype_in: instrument_id
symbol: 42000661 only
expected_raw_symbol: ZNM6
request_start_utc: 2026-04-12T00:00:00Z
request_end_utc: 2026-05-23T00:00:00Z
target_completed_trading_dates: 2026-04-13 through 2026-05-22, weekdays only
```

No continuous contract, parent symbol, substitute symbol, alternate dataset, alternate schema, wider symbol set, or wider request window was used.

## Result

```text
raw_provider_dataframe_rows: 690
definition_metadata_rows: 37
accepted_quarantine_rows: 690
completed_trading_dates: 30
rows_per_completed_trading_date: 23
provider_condition_status_counts:
  PROVIDER_CONDITION_AVAILABLE: 690
validation_status: PASS_ROW_SHAPE_COMPLETED_BAR_MAPPING_EXTENDED_QUARANTINE_ONLY_NOT_FORECAST_READY
```

Completed-bar policy:

```text
provider ts_event interval start preserved
derived_completed_bar_end_utc = provider_ts_event_start_utc + 1 hour
```

Completed trading-date policy:

```text
UTC hour >= 22 maps to the next completed trading date.
UTC hour < 22 maps to the same UTC date.
All accepted rows map into the 30 locked extended target weekdays.
```

## Artifact Root

```text
docs/researchops/s26_s27_hourly_bridge/ZN_S26_WORKED_EXAMPLE/2026-04-13_2026-05-22/databento_ohlcv_1h_extended_forecast_only_quarantine/
```

Key artifacts:

```text
raw_provider_output/20260531_G_R1D_ZN_S26_OHLCV_1H_EXTENDED.dbn
raw_provider_output/20260531_G_R1D_ZN_S26_OHLCV_1H_EXTENDED_provider_dataframe.csv
raw_provider_output/20260531_G_R1D_ZN_S26_OHLCV_1H_EXTENDED_parser_snapshot.csv
raw_provider_metadata/20260531_G_R1D_ZN_S26_OHLCV_1H_EXTENDED_definition.dbn
raw_provider_metadata/20260531_G_R1D_ZN_S26_OHLCV_1H_EXTENDED_definition_dataframe.csv
raw_provider_metadata/20260531_G_R1D_ZN_S26_OHLCV_1H_EXTENDED_symbology_instrument_id_to_raw_symbol.json
raw_provider_metadata/20260531_G_R1D_ZN_S26_OHLCV_1H_EXTENDED_dataset_condition.json
sanitized_bars/20260531_G_R1D_ZN_S26_OHLCV_1H_EXTENDED_sanitized_quarantine_ohlcv_1h.csv
validation/20260531_G_R1D_ZN_S26_OHLCV_1H_EXTENDED_row_validation.json
status/20260531_G_R1D_ZN_S26_OHLCV_1H_EXTENDED_raw_request_status.json
status/20260531_G_R1D_ZN_S26_OHLCV_1H_EXTENDED_quarantine_intake_status.json
provenance/20260531_G_R1D_ZN_S26_OHLCV_1H_EXTENDED_request_provenance.json
hashes/20260531_G_R1D_ZN_S26_OHLCV_1H_EXTENDED_sha256.json
```

## Helper

Bounded helper:

```text
tools/databento/carver_s26_zn_extended_hourly_intake.py
```

The helper reads the Databento key locally without printing or writing it, enforces the exact manifest constants, preserves raw DBN/provider CSV/metadata, writes quarantine-only sanitized OHLCV rows, and emits no forecast, diagnostic, backtest, position, order, cost, carry, trend, or S27 output.

## Boundary

The accepted rows remain:

```text
QUARANTINE_ONLY_NOT_FORECAST_READY
```

The next required blocker before any S26 forecast-series artifact remains:

```text
ONE_PREVALIDATED_NO_LOOKAHEAD_SIGMA_RUNTIME_PER_FORECAST_ROW_REQUIRED
```

## Non-Authorization

This result authorizes no additional provider API access, no additional data download, no wider market-row parsing, no real forecast-series execution, no diagnostics, no backtests, no returns, no PnL, no Sharpe, no drawdown, no positions, no orders, no fills, no costs, no carry, no trend computation, no S27 overlay, no volatility/risk use beyond later separately authorized sigma-runtime work, no OOS, no Lockbox, no Forward, no CFD adapters, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.
