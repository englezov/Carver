# Carver 16-Symbol NinjaTrader Batch Daily Intake Shape Gate Draft

Date: 2026-05-30

Status:

```text
PROCESS_ONLY_CARVER_16_SYMBOL_NINJATRADER_BATCH_DAILY_INTAKE_SHAPE_GATE_DRAFT_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Define the process boundary for a later separately authorized 16-symbol NinjaTrader daily historical-bar intake pilot.

This draft follows the completed 16-symbol static dated-contract selection execution:

```text
docs/process/CARVER_16_SYMBOL_NINJATRADER_STATIC_DATED_CONTRACT_EVIDENCE_INTAKE_AND_SELECTION_EXECUTION_2026-05-30.md
```

It does not export NinjaTrader data, access provider APIs, parse market rows, create helper code, run diagnostics, run backtests, compute forecasts, compute positions, compute costs, compute carry, compute trend, deploy, trade, promote, stage Git changes, commit, push, or update a PR.

## Exact Batch Manifest

The later intake gate, if separately authorized, must use exactly these 16 source-native futures rows and dated contracts:

| Row ID | Symbol | Dated contract | Trading Hours template |
|---|---:|---|---|
| `APPENDIX_C_172_001` | `ZT` | `ZT 06-26` | `CBOT Interest Rate ETH` |
| `APPENDIX_C_172_003` | `ZF` | `ZF 06-26` | `CBOT Interest Rate ETH` |
| `APPENDIX_C_172_004` | `ZN` | `ZN 06-26` | `CBOT Interest Rate ETH` |
| `APPENDIX_C_174_006` | `MES` | `MES 06-26` | `CME US Index Futures ETH` |
| `APPENDIX_C_174_002` | `MNQ` | `MNQ 06-26` | `CME US Index Futures ETH` |
| `APPENDIX_C_174_004` | `M2K` | `M2K 06-26` | `CME US Index Futures ETH` |
| `APPENDIX_C_174_001` | `MYM` | `MYM 06-26` | `CME US Index Futures ETH` |
| `APPENDIX_C_182_002` | `QM` | `QM 07-26` | `Nymex Metals - Energy ETH` |
| `APPENDIX_C_182_004` | `RB` | `RB 07-26` | `Nymex Metals - Energy ETH` |
| `APPENDIX_C_183_003` | `ZC` | `ZC 07-26` | `CBOT Agriculturals ETH` |
| `APPENDIX_C_183_010` | `ZS` | `ZS 07-26` | `CBOT Agriculturals ETH` |
| `APPENDIX_C_183_011` | `ZM` | `ZM 07-26` | `CBOT Agriculturals ETH` |
| `APPENDIX_C_183_012` | `ZL` | `ZL 07-26` | `CBOT Agriculturals ETH` |
| `APPENDIX_C_183_013` | `ZW` | `ZW 07-26` | `CBOT Agriculturals ETH` |
| `APPENDIX_C_183_005` | `HE` | `HE 06-26` | `CME Commodities ETH` |
| `APPENDIX_C_183_006` | `LE` | `LE 06-26` | `CME Commodities ETH` |

The manifest source is:

```text
docs/researchops/first_data_intake/CARVER_16_SYMBOL_NINJATRADER_STATIC_DATED_CONTRACT_SELECTION_2026-05-30.csv
SHA256: 4A6B975B5C4B58F422BB4695F4AD83C8166A12EED13EE86B5B1A05C4464C9F4F
```

No other Appendix C row, alias-required row, unavailable row, adjacent product, CFD symbol, continuous contract, substitute contract, or reweighted universe may enter this batch pilot.

## Exact Bar Surface

The later intake gate must be locked to:

```text
bar_type: Last
timeframe: 1 Day
completed_trading_date_start: 2026-05-18
completed_trading_date_end: 2026-05-22
expected_completed_trading_dates_per_row: 5
expected_manifest_rows: 16
expected_total_rows: 80
```

Any different timeframe, bar type, price type, date window, contract month, or symbol must fail closed before rows are admitted.

## Locked Helper / Export Strategy

A later helper/export gate must create or approve one manifest-driven local NinjaTrader helper or equivalent locked local procedure before execution.

The helper strategy must:

- be disarmed by default;
- require explicit arming inside the helper or handoff artifact;
- load or embed the exact 16-row manifest above;
- reject symbols not in the manifest;
- reject contracts not in the manifest;
- reject continuous contracts;
- reject non-`1 Day` bars;
- reject non-`Last` bars;
- reject completed trading dates outside `2026-05-18` through `2026-05-22`;
- write only under the locked batch quarantine root;
- produce one row-bound output per manifest row, or one manifest-bound combined output with row-level contract binding;
- write template-derived UTC session-end timestamps according to the locked row template policy;
- clearly label helper raw output as helper output, not provider-verbatim NinjaTrader `Time[0]`;
- emit no diagnostics, returns, forecasts, positions, costs, carry, trend, strategy values, or performance fields.

The helper gate must explicitly preserve the MES lesson:

```text
HELPER_RAW_OUTPUT_WITH_TEMPLATE_DERIVED_UTC_SESSION_END_TIMESTAMPS_NOT_PROVIDER_VERBATIM_TIME0
```

Provider-verbatim `Time[0]` output, if ever captured for comparison, must be quarantined separately and may not be used as the canonical sanitized timestamp unless a later process/source decision changes the timestamp policy.

## Quarantine Layout

The later intake gate must write only under:

```text
docs/researchops/first_data_intake/quarantine/16_SYMBOL_DAILY_LAST_2026-05-18_2026-05-22/
```

Required subdirectories:

```text
helper_raw_output/
sanitized_bars/
provenance/
row_validation/
```

Required raw helper-output convention:

```text
helper_raw_output/<SYMBOL>_<MM-YY>_Daily_Last_2026-05-18_2026-05-22_TEMPLATE_SESSION_END_UTC.csv
```

Required sanitized per-row convention:

```text
sanitized_bars/<SYMBOL>_<MM_YY>_DAILY_2026-05-18_2026-05-22.csv
```

Required manifest-level outputs:

```text
sanitized_bars/16_SYMBOL_DAILY_LAST_2026-05-18_2026-05-22_COMBINED_QUARANTINE_ONLY.csv
row_validation/16_SYMBOL_DAILY_LAST_2026-05-18_2026-05-22_ROW_VALIDATION.csv
provenance/16_SYMBOL_DAILY_LAST_2026-05-18_2026-05-22_PROVENANCE.md
provenance/16_SYMBOL_DAILY_LAST_2026-05-18_2026-05-22_INTAKE_EXECUTION_STATUS.csv
```

The combined sanitized file is quarantine-only. It is not a strategy dataset, not a diagnostic dataset, not a backtest dataset, not a forecast input authorization, not a position-sizing input, and not promotion evidence.

## Accepted Raw Helper Fields

The later intake gate may accept only these raw helper-output fields:

```text
provider_symbol
local_contract
timestamp_utc
completed_trading_date
open
high
low
close
volume
```

Optional helper metadata fields may be accepted only for provenance:

```text
row_id
local_canonical_instrument_id
trading_hours_template
source_helper
helper_version_or_sha256
source_file
source_file_sha256
row_number
exported_at_utc
```

The later intake gate must reject raw helper outputs that contain strategy, diagnostic, performance, forecast, position, return, cost, carry, trend, or tuning fields.

## Sanitized OHLCV Schema

Each accepted sanitized row must use exactly:

```text
row_id
author_market_code
local_contract
timestamp_utc
completed_trading_date
open
high
low
close
volume
source_file
source_file_sha256
source_row_number
```

All timestamps must be timezone-aware UTC strings. Completed trading dates must be ISO dates. OHLCV values must be copied from the helper raw output except for formatting normalization. No price adjustment, settlement replacement, return calculation, imputation, forward fill, merge, roll, or back-adjustment may occur.

## Timestamp And Completed Trading-Date Policy

Canonical completed trading date:

```text
LOCAL_NINJATRADER_TEMPLATE_TRADINGDAY
```

Canonical timestamp:

```text
UTC_TEMPLATE_SESSION_END_TIMESTAMP
```

The later intake gate must map each accepted row through the row's locked Trading Hours template:

```text
CBOT Interest Rate ETH
CME US Index Futures ETH
Nymex Metals - Energy ETH
CBOT Agriculturals ETH
CME Commodities ETH
```

The row is accepted only if:

- `timestamp_utc` is the locked template-derived UTC session-end timestamp for the completed trading date;
- `completed_trading_date` maps to exactly one local NinjaTrader template TradingDay;
- the date is inside `2026-05-18` through `2026-05-22`;
- local NinjaTrader Trading Hours evidence and CME static holiday/trading-hours conflict policy do not contradict the row/date.

If local NinjaTrader template evidence and CME holiday/early-close evidence conflict for a row/date, the affected row/date must fail closed.

## Row-Shape Checks

For every manifest row/date, the later intake gate must check:

- exact row ID and symbol match;
- exact local contract match;
- exact `1 Day` / `Last` surface match;
- required fields present;
- numeric OHLCV values;
- positive OHLC values;
- `high >= low`;
- `open`, `high`, `low`, and `close` within the basic positive-price sanity boundary;
- non-negative volume;
- one and only one row per completed trading date;
- five completed trading dates per manifest row;
- eighty total rows for a full 16-symbol pass.

## Strict Fail-Closed Rules

The later intake gate must fail closed on:

- missing symbol;
- missing row ID;
- missing contract;
- wrong contract month;
- continuous contract;
- substituted symbol;
- adjacent market;
- CFD symbol;
- wrong timeframe;
- wrong bar type;
- missing expected completed trading date;
- extra completed trading date;
- duplicate completed trading date;
- stale row;
- future row;
- non-monotonic row order within a symbol;
- non-UTC timestamp;
- non-template-session-end timestamp;
- timestamp outside the extracted local template session;
- timestamp mapping to zero or multiple local template sessions;
- local/CME holiday or early-close conflict;
- partial-holiday ambiguity;
- missing OHLCV field;
- non-numeric OHLCV value;
- `high < low`;
- non-positive OHLC value;
- repaired row;
- imputed row;
- forward-filled row;
- settlement replacement;
- price adjustment;
- merge/back-adjustment;
- row dropping;
- reweighting;
- any need to inspect results, diagnostics, returns, or strategy values to decide acceptance.

## All-16 Pass / Fail Semantics

The batch pilot may pass only if:

```text
MANIFEST_ROWS_EXPECTED: 16
MANIFEST_ROWS_ACCEPTED: 16
EXPECTED_COMPLETED_TRADING_DATES_PER_ROW: 5
EXPECTED_TOTAL_ROWS: 80
ACCEPTED_TOTAL_ROWS: 80
INTAKE_STATUS: PASS_16_SYMBOL_DAILY_INTAKE_QUARANTINE_ONLY
```

If any symbol/date fails, the batch pilot must use:

```text
FAIL_CLOSED_16_SYMBOL_DAILY_INTAKE_INCOMPLETE_NO_PARTIAL_PASS
```

Partial sanitized outputs may be preserved only as failed quarantine evidence. They must not be interpreted as a narrower successful pilot unless a separate process-only redecision explicitly narrows the row set before any further export or parsing.

## Provenance Requirements

The later intake execution must record:

- exact manifest file path and SHA256;
- helper source path and SHA256;
- helper arming status;
- NinjaTrader local helper placement path, if any;
- raw helper-output file paths and SHA256;
- sanitized output file paths and SHA256;
- row-validation ledger path and SHA256;
- execution status ledger path and SHA256;
- total rows seen;
- total rows accepted;
- total rows rejected;
- rejection reason counts;
- explicit `NO` flags for diagnostics, backtests, provider API access, old QuantLab pipeline use, and remote operations.

## Audit Requirements

After any later execution, run a lean hostile audit over:

- the batch shape gate;
- the helper/export gate;
- the raw helper-output policy;
- the sanitized OHLCV files;
- the provenance and row-validation ledgers;
- the all-16 pass/fail disposition.

The lean audit result should be preserved automatically as process documentation. A separate Opus audit may be requested before broader portfolio/readiness promotion, but this batch intake shape does not itself require Opus execution.

## Next Clean Gate

Selected next gate:

```text
CARVER_16_SYMBOL_NINJATRADER_LOCKED_MANIFEST_DAILY_EXPORT_HELPER_GATE
```

That gate should define or create the locked manifest-driven helper/export strategy. It must remain disarmed by default and must not itself export or parse historical bars unless separately authorized.

## Non-Authorization

This shape draft authorizes no new data export, no provider API access, no market-row parsing, no NinjaTrader historical export, no diagnostics, no backtests, no forecasts, no positions, no costs, no carry, no trend, no OOS, no Lockbox, no Forward, no CFD adapter work, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no GitHub staging, no commit, no push, no PR update/opening, and no remote operations.
