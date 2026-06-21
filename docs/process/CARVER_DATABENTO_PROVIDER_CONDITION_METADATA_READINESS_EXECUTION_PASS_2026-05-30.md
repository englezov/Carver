# Carver Databento Provider-Condition Metadata Readiness Execution Pass

Date: 2026-05-30

Status:

```text
LOCAL_PROCESS_CARVER_DATABENTO_PROVIDER_CONDITION_METADATA_READINESS_EXECUTION_PASS_DEGRADED_ROWS_QUARANTINED_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Record the bounded Databento provider-condition metadata readiness execution for the existing 16-symbol dated-contract full-history daily OHLCV quarantine archive.

This follows:

```text
docs/process/CARVER_DATABENTO_PROVIDER_CONDITION_METADATA_READINESS_GATE_DRAFT_2026-05-30.md
```

## Upstream Archive

Archive root:

```text
docs/researchops/source_native_futures_daily_data_library/16_SYMBOL_FULL_DAILY_HISTORY/raw_provider_archive/DATABENTO/20260530_DATED_CONTRACT_FULL_AVAILABLE_HISTORY_PER_SYMBOL_CURRENT_IDS
```

Archive status:

```text
PASS_WITH_PROVIDER_CONDITION_WARNINGS_16_SYMBOL_DATED_CONTRACT_PER_SYMBOL_CURRENT_ID_FULL_HISTORY_QUARANTINE_ONLY
```

Input archive rows:

```text
4568
```

## Metadata Request

Databento official metadata method:

```text
Historical.metadata.get_dataset_condition
```

Request:

```text
dataset: GLBX.MDP3
condition_start_date: 2023-05-23
condition_end_date_exclusive: 2026-05-30
```

This was metadata-only access. No new OHLCV request and no new market-data download was performed.

## Execution Result

Result:

```text
PASS_PROVIDER_CONDITION_METADATA_JOIN_WITH_DEGRADED_ROWS_QUARANTINED
```

Summary:

```text
CONDITION_RECORDS_RETURNED: 948
RAW_CONDITION_AVAILABLE_RECORDS: 941
RAW_CONDITION_DEGRADED_RECORDS: 7
ROWS_JOINED: 4568
ROW_READY_PROVIDER_CONDITION_NORMAL: 4483
ROW_QUARANTINED_PROVIDER_CONDITION_DEGRADED: 85
ROW_BLOCKED_PROVIDER_CONDITION_UNRESOLVED_OR_UNUSABLE: 0
DIAGNOSTICS_RUN: NO
BACKTESTS_RUN: NO
FORECASTS_COMPUTED: NO
POSITIONS_COMPUTED: NO
```

## Degraded Dates

The official provider-condition metadata marked the following dates as degraded within the archive date range:

```text
2025-09-17  -> 10 archive rows quarantined
2025-09-24  -> 11 archive rows quarantined
2025-11-28  -> 14 archive rows quarantined
2026-03-15  -> 9 archive rows quarantined
2026-03-16  -> 16 archive rows quarantined
2026-04-10  -> 16 archive rows quarantined
2026-05-24  -> 9 archive rows quarantined
```

These rows are not strategy-facing ready. They remain available only as quarantined archive rows with provider-condition labels preserved.

## Readiness Policy Applied

```text
available -> ROW_READY_PROVIDER_CONDITION_NORMAL
degraded  -> ROW_QUARANTINED_PROVIDER_CONDITION_DEGRADED
missing/ambiguous/unmatched -> ROW_BLOCKED_PROVIDER_CONDITION_UNRESOLVED
```

No degraded row was silently accepted as strategy-facing ready.

## Created Artifacts

Root:

```text
docs/researchops/source_native_futures_daily_data_library/16_SYMBOL_FULL_DAILY_HISTORY/raw_provider_archive/DATABENTO/20260530_DATED_CONTRACT_FULL_AVAILABLE_HISTORY_PER_SYMBOL_CURRENT_IDS/provider_condition_metadata_2026-05-30
```

Artifacts:

```text
raw_provider_metadata/DATABENTO_PROVIDER_CONDITION_REQUEST_MANIFEST_2026-05-30.json
raw_provider_metadata/DATABENTO_GLBX_MDP3_DATASET_CONDITION_RAW_2026-05-30.json
raw_provider_metadata/DATABENTO_GLBX_MDP3_DATASET_CONDITION_FIELD_INVENTORY.csv
provider_condition_ledger/DATABENTO_16_SYMBOL_DATED_CONTRACT_PROVIDER_CONDITION_LEDGER.csv
provider_condition_ledger/DATABENTO_16_SYMBOL_DATED_CONTRACT_PROVIDER_CONDITION_ROW_JOIN.csv
validation/DATABENTO_PROVIDER_CONDITION_READINESS_VALIDATION.csv
provenance/DATABENTO_PROVIDER_CONDITION_METADATA_STATUS.csv
provenance/DATABENTO_PROVIDER_CONDITION_METADATA_PROVENANCE.md
provenance/DATABENTO_PROVIDER_CONDITION_METADATA_SHA256SUMS.txt
```

## Interpretation

This pass upgrades the archive from "provider condition warnings observed" to explicit row/date condition labeling.

It does not authorize strategy use. It only proves that provider-condition metadata has been fetched, preserved, joined, and used to quarantine degraded rows.

The 16-symbol daily intake pilot remains quarantine-only until later gates explicitly decide how strategy-facing data views handle quarantined dates.

## Non-Authorization

Still closed:

```text
new OHLCV data download
new market-data request
symbols outside the locked 16
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
