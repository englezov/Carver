# Carver Databento 16-Symbol Daily Futures Quarantine Intake Shape Gate Draft

Date: 2026-05-30

Status:

```text
PROCESS_ONLY_CARVER_DATABENTO_16_SYMBOL_DAILY_FUTURES_QUARANTINE_INTAKE_SHAPE_GATE_DRAFT_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Define the process boundary for a later separately authorized Databento Historical quarantine intake for the locked 16-symbol source-native futures daily pilot.

This draft follows:

```text
docs/process/CARVER_SOURCE_NATIVE_FUTURES_HISTORICAL_DATA_SOURCE_SELECTION_DECISION_2026-05-30.md
```

This draft uses current Carver artifacts and Databento public documentation only. It does not log in to Databento, use an API key, call a provider API, download data, parse market rows, run diagnostics, run backtests, compute forecasts, compute positions, compute costs, compute carry, compute trend, access OOS/Lockbox/Forward, use CFD adapters, use old QuantLab active pipelines, tune, deploy, trade, promote, stage Git changes, commit, push, update a PR, or perform remote repository operations.

## Public Databento Documentation Basis

Static public Databento documentation inspected:

```text
Databento historical API:
https://databento.com/docs/api-reference-historical?historical=http

Databento schemas and data formats:
https://databento.com/docs/schemas-and-data-formats

Databento end-of-day OHLCV example:
https://databento.com/docs/examples/basics-historical/eod

Databento request-many-symbols example:
https://databento.com/docs/examples/basics-historical/requesting

Databento symbology conventions:
https://databento.com/docs/standards-and-conventions/symbology

Databento CME Globex MDP 3.0 dataset page:
https://databento.com/datasets/GLBX.MDP3

Databento CME Globex MDP 3.0 technical page:
https://databento.com/docs/venues-and-datasets/glbx-mdp3
```

Relevant static documentation atoms:

- `GLBX.MDP3` covers CME Globex futures/options for CME, CBOT, NYMEX, and COMEX.
- Historical `timeseries.get_range` supports `dataset`, `start`, `end`, `symbols`, `schema`, `stype_in`, `stype_out`, and `path`.
- Historical requests can use raw symbology, instrument ID symbology, parent symbology, or continuous symbology, subject to dataset support.
- Databento supports multiple specific symbols in one request, with a documented maximum of 2,000 symbols per request.
- `ohlcv-1d` is a documented OHLCV aggregate-bar schema.
- Databento documents that `ohlcv-1d` is based on UTC dates and may differ from exchange-session daily data or official settlement data.
- The `statistics` schema is documented as the official-settlement/daily-statistics path, not a replacement for full OHLC bars.
- Continuous symbology exists but must remain forbidden for this Carver pilot because this pilot is explicitly dated-contract only.

## Locked Carver Pilot

Lane:

```text
SOURCE_NATIVE_FUTURES
```

Carver manifest source:

```text
docs/researchops/first_data_intake/CARVER_16_SYMBOL_NINJATRADER_STATIC_DATED_CONTRACT_SELECTION_2026-05-30.csv
SHA256: 4A6B975B5C4B58F422BB4695F4AD83C8166A12EED13EE86B5B1A05C4464C9F4F
```

Locked target completed trading dates:

```text
2026-05-18 through 2026-05-22 inclusive
```

Locked row set:

| Row ID | Carver code | Carver selected dated contract | Candidate Databento raw symbol | Venue |
|---|---:|---|---|---|
| `APPENDIX_C_172_001` | `ZT` | `ZT JUN 2026` | `ZTM6` | `CBOT` |
| `APPENDIX_C_172_003` | `ZF` | `ZF JUN 2026` | `ZFM6` | `CBOT` |
| `APPENDIX_C_172_004` | `ZN` | `ZN JUN 2026` | `ZNM6` | `CBOT` |
| `APPENDIX_C_174_006` | `MES` | `MES JUN 2026` | `MESM6` | `CME` |
| `APPENDIX_C_174_002` | `MNQ` | `MNQ JUN 2026` | `MNQM6` | `CME` |
| `APPENDIX_C_174_004` | `M2K` | `M2K JUN 2026` | `M2KM6` | `CME` |
| `APPENDIX_C_174_001` | `MYM` | `MYM JUN 2026` | `MYMM6` | `CBOT` |
| `APPENDIX_C_182_002` | `QM` | `QM JUL 2026` | `QMN6` | `NYMEX` |
| `APPENDIX_C_182_004` | `RB` | `RB JUL 2026` | `RBN6` | `NYMEX` |
| `APPENDIX_C_183_003` | `ZC` | `ZC JUL 2026` | `ZCN6` | `CBOT` |
| `APPENDIX_C_183_010` | `ZS` | `ZS JUL 2026` | `ZSN6` | `CBOT` |
| `APPENDIX_C_183_011` | `ZM` | `ZM JUL 2026` | `ZMN6` | `CBOT` |
| `APPENDIX_C_183_012` | `ZL` | `ZL JUL 2026` | `ZLN6` | `CBOT` |
| `APPENDIX_C_183_013` | `ZW` | `ZW JUL 2026` | `ZWN6` | `CBOT` |
| `APPENDIX_C_183_005` | `HE` | `HE JUN 2026` | `HEM6` | `CME` |
| `APPENDIX_C_183_006` | `LE` | `LE JUN 2026` | `LEM6` | `CME` |

The Databento raw-symbol column is a candidate mapping only. A later execution gate must resolve it through Databento symbology and/or `definition` records before any market-row output is accepted.

No parent symbols, continuous symbols, alternate contracts, adjacent tickers, Mini/Micro substitutions, NinjaTrader aliases, CFD symbols, or row drops may enter the pilot.

## Dataset And Schema Shape

Selected dataset candidate:

```text
GLBX.MDP3
```

Reason:

`GLBX.MDP3` is the Databento CME Globex MDP 3.0 dataset covering CME Group futures venues needed by the locked manifest:

```text
CME
CBOT
NYMEX
```

Primary schema candidate:

```text
ohlcv-1d
```

Interpretation:

```text
DATABENTO_UTC_DAILY_TRADE_AGGREGATE
```

Important boundary:

`ohlcv-1d` must not be silently treated as the same thing as the local NinjaTrader exchange-session completed TradingDay policy. Public Databento documentation states that `ohlcv-1d` is based on UTC dates and may differ from exchange-session daily bars and official settlement data.

Therefore the later execution gate must label any accepted `ohlcv-1d` rows as:

```text
PROVIDER_UTC_DAILY_OHLCV_QUARANTINE_ONLY
NOT_EXCHANGE_SESSION_DAILY_BAR_LOCK
NOT_OFFICIAL_SETTLEMENT_LOCK
NOT_STRATEGY_INPUT_AUTHORIZATION
```

Supplemental schema candidate:

```text
statistics
```

Purpose:

The `statistics` schema may be separately gated later for official settlement or exchange-published daily statistics comparison. It is not required for this first Databento OHLCV quarantine mechanics gate and must not be mixed into OHLCV rows without a separate source decision.

Definition/reference schema candidate:

```text
definition
```

Purpose:

Before accepting market rows, a later execution gate should use `definition` and/or Databento symbology resolution to verify that every candidate raw symbol maps to the intended dated futures outright and not to an option, spread, continuous contract, or adjacent product.

## Request Window Shape

Candidate request window for `ohlcv-1d`:

```text
dataset: GLBX.MDP3
schema: ohlcv-1d
stype_in: raw_symbol
stype_out: raw_symbol or instrument_id plus resolved symbol map
symbols:
  ZTM6, ZFM6, ZNM6, MESM6, MNQM6, M2KM6, MYMM6,
  QMN6, RBN6, ZCN6, ZSN6, ZMN6, ZLN6, ZWN6, HEM6, LEM6
start: 2026-05-18T00:00:00Z
end: 2026-05-23T00:00:00Z
```

Rationale:

The `end` timestamp is exclusive. The UTC-day window from `2026-05-18T00:00:00Z` to `2026-05-23T00:00:00Z` is the candidate provider window for five UTC daily bars labeled `2026-05-18` through `2026-05-22`.

Fail-closed caveat:

If this request shape does not produce exactly five UTC daily OHLCV rows per locked symbol, or if a provider row cannot be reconciled to the target date label without ambiguity, the affected row must fail closed. No row may be imputed, shifted, forward-filled, replaced with another contract, or rescued through continuous symbology.

## Quarantine Layout

The later execution gate must write only under:

```text
docs/researchops/first_data_intake/quarantine/DATABENTO_16_SYMBOL_DAILY_OHLCV_2026-05-18_2026-05-22/
```

Required subdirectories:

```text
raw_provider_output/
raw_provider_metadata/
sanitized_bars/
row_validation/
provenance/
```

Required raw provider artifacts:

```text
raw_provider_metadata/databento_request_manifest_2026-05-18_2026-05-22.json
raw_provider_metadata/databento_symbology_resolution_2026-05-18_2026-05-22.csv
raw_provider_metadata/databento_definition_check_2026-05-18_2026-05-22.csv
raw_provider_output/databento_GLBX_MDP3_ohlcv-1d_16_SYMBOL_2026-05-18_2026-05-22_RAW.<provider-extension>
```

The raw provider artifact should prefer a Databento-native raw form such as DBN/Zstandard when available, with a separately generated CSV only if the future execution gate explicitly permits conversion for inspection.

Required sanitized artifacts:

```text
sanitized_bars/DATABENTO_16_SYMBOL_DAILY_OHLCV_2026-05-18_2026-05-22_COMBINED_QUARANTINE_ONLY.csv
row_validation/DATABENTO_16_SYMBOL_DAILY_OHLCV_2026-05-18_2026-05-22_ROW_VALIDATION.csv
provenance/DATABENTO_16_SYMBOL_DAILY_OHLCV_2026-05-18_2026-05-22_PROVENANCE.md
provenance/DATABENTO_16_SYMBOL_DAILY_OHLCV_2026-05-18_2026-05-22_INTAKE_STATUS.csv
```

## Raw Provider Preservation

The later execution gate must preserve:

- exact request parameters;
- provider account/API surface used, without recording secrets;
- Databento client/package version if a client library is used;
- raw provider file path;
- raw provider file SHA256;
- export/download timestamp in UTC;
- schema;
- dataset;
- symbology input type;
- symbology output type;
- source symbols requested;
- symbols returned;
- record counts per symbol;
- whether the file is DBN, CSV, JSON, or another Databento-supported encoding.

Secrets and API keys must not be written into any artifact.

## Sanitized OHLCV Schema

The sanitized combined quarantine CSV must use exactly:

```text
row_id
author_market_code
selected_source_native_dated_contract
databento_dataset
databento_schema
databento_raw_symbol
databento_instrument_id
provider_ts_event_utc
provider_utc_bar_date
carver_completed_trading_date_candidate
completed_trading_date_policy_status
open
high
low
close
volume
source_file
source_file_sha256
source_row_number
```

Allowed transformations:

- integer/numeric price scale decoding required by Databento format;
- string/date formatting normalization;
- joining resolved symbol/instrument metadata for row identity;
- copying OHLCV values into the sanitized schema.

Forbidden transformations:

- returns;
- PnL;
- forecasts;
- positions;
- costs;
- carry;
- trend;
- volatility;
- risk;
- settlement substitution;
- continuous-contract rolling;
- back-adjustment;
- price adjustment;
- imputation;
- forward fill;
- missing-row repair;
- resampling from a different schema unless separately authorized;
- row dropping;
- substitution;
- reweighting.

## Timestamp And Completed-Date Policy

Provider timestamp:

```text
provider_ts_event_utc = Databento ts_event for the ohlcv-1d row
```

Provider UTC bar date:

```text
provider_utc_bar_date = date(provider_ts_event_utc)
```

Carver completed trading-date candidate:

```text
carver_completed_trading_date_candidate = provider_utc_bar_date
```

Policy status required on every accepted row:

```text
DATABENTO_UTC_DATE_DAILY_BAR_QUARANTINE_LABEL_ONLY_NOT_EXCHANGE_SESSION_TRADINGDAY_LOCK
```

This policy intentionally prevents the first Databento OHLCV quarantine intake from being misread as an exchange-session daily bar lock. It is enough to test provider retrieval, source-native dated-contract symbology, raw-output preservation, row-shape, and quarantine mechanics. It is not enough to feed strategy calculations.

If a later Carver chapter requires true exchange-session completed bars from Databento, it must open a separate aggregation policy gate, likely using a more granular schema such as `trades`, `ohlcv-1m`, or `ohlcv-1h` and a source-locked session calendar.

## Row Validation Semantics

Expected count:

```text
16 symbols * 5 UTC daily rows = 80 rows
```

The later execution gate must validate:

- all 16 manifest rows preserved;
- candidate raw symbol resolved to the intended dated futures outright;
- no options;
- no spreads;
- no continuous contracts;
- no parent-symbol aggregate output;
- no duplicate row ID/date;
- no missing row ID/date;
- exactly five UTC daily rows per symbol;
- `provider_utc_bar_date` in `2026-05-18` through `2026-05-22`;
- required OHLCV fields present;
- numeric OHLCV values;
- positive OHLC values;
- `high >= low`;
- non-negative volume;
- source file hash present;
- row provenance present.

All-or-nothing disposition:

```text
ALL_16_SYMBOLS_PASS_OR_BATCH_FAILS_CLOSED
```

If any row fails validation, the execution gate must preserve raw provider output and write a fail-closed status, but it must not publish a combined sanitized file as ready for downstream use. A separately authorized redecision may later choose a smaller row set.

## Output Status Values

Successful quarantine-only status:

```text
PASS_DATABENTO_16_SYMBOL_DAILY_OHLCV_QUARANTINE_ONLY_NOT_EXCHANGE_SESSION_LOCK_NOT_DIAGNOSTIC_NOT_BACKTEST
```

Fail-closed statuses:

```text
FAIL_CLOSED_DATABENTO_SYMBOLOGY_UNRESOLVED
FAIL_CLOSED_DATABENTO_DATED_CONTRACT_MISMATCH
FAIL_CLOSED_DATABENTO_CONTINUOUS_OR_PARENT_SYMBOL_OUTPUT
FAIL_CLOSED_DATABENTO_MISSING_UTC_DAILY_ROW
FAIL_CLOSED_DATABENTO_DUPLICATE_UTC_DAILY_ROW
FAIL_CLOSED_DATABENTO_OHLCV_SHAPE_INVALID
FAIL_CLOSED_DATABENTO_COMPLETED_DATE_POLICY_UNRESOLVED
FAIL_CLOSED_DATABENTO_RAW_OUTPUT_NOT_HASH_BOUND
```

## What This Gate Does Not Open

This draft does not make the 16-symbol pilot:

```text
exchange-session daily-bar ready
strategy-input ready
diagnostic ready
backtest ready
forecast ready
position-sizing ready
cost ready
carry ready
trend ready
portfolio ready
OOS ready
Lockbox ready
Forward ready
deployment ready
trading ready
promotion ready
```

## Required Next Gate

Next gate, if the operator chooses to proceed:

```text
CARVER_DATABENTO_16_SYMBOL_DAILY_OHLCV_QUARANTINE_INTAKE_EXECUTION_GATE
```

That later gate must separately authorize:

- Databento API key use without exposing the key;
- Databento historical API access;
- the exact `GLBX.MDP3` / `ohlcv-1d` request;
- raw provider output preservation;
- quarantine-only parsing of the raw provider output;
- validation limited to row-shape, symbology, timestamp/date labeling, duplicate/missing checks, and provenance.

It must still forbid diagnostics, backtests, forecasts, positions, costs, carry, trend, OOS, Lockbox, Forward, CFD adapters, old QuantLab active-pipeline use, tuning, deployment, trading, promotion, GitHub staging, commit, push, PR update/opening, and remote repository operations.

## Non-Authorization

This draft authorizes no Databento login, no API key use, no provider API call, no data download, no market-row parsing, no diagnostics, no backtests, no forecasts, no positions, no costs, no carry, no trend, no OOS, no Lockbox, no Forward, no CFD adapter work, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no GitHub staging, no commit, no push, no PR update/opening, and no remote repository operations.
