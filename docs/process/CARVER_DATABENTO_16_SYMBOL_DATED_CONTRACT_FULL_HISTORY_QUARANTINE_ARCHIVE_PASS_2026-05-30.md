# Carver Databento 16-Symbol Dated-Contract Full-History Quarantine Archive Pass

Date: 2026-05-30

Status:

```text
LOCAL_PROCESS_CARVER_DATABENTO_16_SYMBOL_DATED_CONTRACT_FULL_HISTORY_QUARANTINE_ARCHIVE_PASS_WITH_PROVIDER_CONDITION_WARNINGS_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Record the bounded Databento Historical full available dated-contract daily OHLCV quarantine archive for the locked 16-symbol pilot universe.

This follows the successful five-day Databento pipe proof and preserves the next archive unit for the source-native daily futures data library.

## Locked Universe

```text
ZTM6, ZFM6, ZNM6, MESM6, MNQM6, M2KM6, MYMM6, QMN6,
RBN6, ZCN6, ZSN6, ZMN6, ZLN6, ZWN6, HEM6, LEM6
```

Dataset/schema:

```text
provider: Databento Historical
dataset: GLBX.MDP3
schema: ohlcv-1d
definition metadata schema: definition
```

## Identity Rule

The first wide raw-symbol full-history request failed closed after Databento ended the stream prematurely. The saved Databento symbology resolution also showed older raw-symbol intervals for some symbols.

To preserve exact dated-contract identity, the successful archive uses one exact 2026-current `instrument_id` per locked raw symbol, derived from the saved Databento symbology resolution, and requests each instrument separately.

No continuous contracts were requested.

## Execution Result

Result:

```text
PASS_WITH_PROVIDER_CONDITION_WARNINGS_16_SYMBOL_DATED_CONTRACT_PER_SYMBOL_CURRENT_ID_FULL_HISTORY_QUARANTINE_ONLY
```

Summary:

```text
SYMBOLS_EXPECTED: 16
SYMBOLS_WITH_RAW_FILES: 16
ACCEPTED_MARKET_ROWS: 4568
DUPLICATE_DATES_TOTAL: 0
ALL_16_SYMBOLS_HAVE_ROWS: YES
PROVIDER_CONDITION_WARNINGS_OBSERVED: YES_REDUCED_QUALITY_WARNINGS_PRINTED_DURING_REQUESTS
DIAGNOSTICS_RUN: NO
BACKTESTS_RUN: NO
FORECASTS_COMPUTED: NO
POSITIONS_COMPUTED: NO
```

## Row Coverage

```text
ZTM6   142 rows  2025-11-05 through 2026-05-29
ZFM6   148 rows  2025-11-19 through 2026-05-29
ZNM6   173 rows  2025-10-21 through 2026-05-29
MESM6  232 rows  2025-04-09 through 2026-05-29
MNQM6  231 rows  2025-04-09 through 2026-05-29
M2KM6  193 rows  2025-06-03 through 2026-05-29
MYMM6  190 rows  2025-10-03 through 2026-05-29
QMN6   123 rows  2025-10-10 through 2026-05-29
RBN6   278 rows  2023-08-28 through 2026-05-29
ZCN6   560 rows  2023-05-23 through 2026-05-29
ZSN6   461 rows  2023-05-25 through 2026-05-29
ZMN6   393 rows  2024-06-07 through 2026-05-29
ZLN6   375 rows  2023-10-10 through 2026-05-29
ZWN6   409 rows  2023-07-24 through 2026-05-29
HEM6   307 rows  2025-01-30 through 2026-05-29
LEM6   353 rows  2025-01-02 through 2026-05-29
```

## Created Artifact Root

```text
docs/researchops/source_native_futures_daily_data_library/16_SYMBOL_FULL_DAILY_HISTORY/raw_provider_archive/DATABENTO/20260530_DATED_CONTRACT_FULL_AVAILABLE_HISTORY_PER_SYMBOL_CURRENT_IDS
```

Key artifacts:

```text
raw_provider_output/
raw_provider_metadata/databento_per_symbol_current_id_archive_identity_lock.json
sanitized_bars/DATABENTO_16_SYMBOL_DATED_CONTRACT_FULL_HISTORY_PER_SYMBOL_CURRENT_IDS_SANITIZED.csv
validation/DATABENTO_16_SYMBOL_DATED_CONTRACT_FULL_HISTORY_PER_SYMBOL_CURRENT_ID_VALIDATION.csv
provenance/DATABENTO_16_SYMBOL_DATED_CONTRACT_FULL_HISTORY_PER_SYMBOL_CURRENT_ID_STATUS.csv
provenance/DATABENTO_16_SYMBOL_DATED_CONTRACT_FULL_HISTORY_PER_SYMBOL_CURRENT_ID_PROVENANCE.md
provenance/DATABENTO_16_SYMBOL_DATED_CONTRACT_FULL_HISTORY_PER_SYMBOL_CURRENT_ID_SHA256SUMS.txt
```

The artifact root contains 90 files, including raw DBN/CSV provider output, per-symbol definition metadata files, sanitized OHLCV, validation, provenance, and hashes.

## Provider Condition Caveat

Databento emitted reduced-quality warnings during several per-symbol requests. The archive passes quarantine row-shape validation, but these provider condition warnings remain a readiness caveat before any later strategy, diagnostic, backtest, or production use.

The next clean readiness step should decide whether to ingest Databento dataset-condition metadata and encode provider-condition status row/date-wise before any strategy-facing promotion.

## Non-Authorization

This archive does not authorize:

```text
continuous contracts
diagnostics
backtests
forecasts
positions
costs
carry
trend
volatility or risk calculations
OOS
Lockbox
Forward
CFD adapters
old QuantLab active-pipeline use
tuning
deployment
trading
promotion
GitHub staging
commit
push
PR update/opening
remote repository operations
```
