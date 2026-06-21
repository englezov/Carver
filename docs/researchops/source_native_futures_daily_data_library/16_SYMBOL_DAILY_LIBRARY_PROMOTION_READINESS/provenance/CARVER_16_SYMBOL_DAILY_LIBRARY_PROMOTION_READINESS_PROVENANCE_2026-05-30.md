# Carver 16-Symbol Daily Library Promotion Readiness Provenance

Date: 2026-05-30

Status:

```text
PASS_CANONICAL_MANIFEST_PROMOTION_READINESS_NORMAL_ROWS_ONLY_DEGRADED_ROWS_QUARANTINED
```

This provenance record covers the canonical manifest created for the 16-symbol source-native daily data library promotion readiness chapter.

Inputs inspected:

```text
docs\researchops\first_data_intake\CARVER_16_SYMBOL_NINJATRADER_STATIC_DATED_CONTRACT_SELECTION_2026-05-30.csv
docs\researchops\source_native_futures_daily_data_library\16_SYMBOL_FULL_DAILY_HISTORY\raw_provider_archive\DATABENTO\20260530_DATED_CONTRACT_FULL_AVAILABLE_HISTORY_PER_SYMBOL_CURRENT_IDS\validation\DATABENTO_16_SYMBOL_DATED_CONTRACT_FULL_HISTORY_PER_SYMBOL_CURRENT_ID_VALIDATION.csv
docs\researchops\source_native_futures_daily_data_library\16_SYMBOL_FULL_DAILY_HISTORY\raw_provider_archive\DATABENTO\20260530_DATED_CONTRACT_FULL_AVAILABLE_HISTORY_PER_SYMBOL_CURRENT_IDS\sanitized_bars\DATABENTO_16_SYMBOL_DATED_CONTRACT_FULL_HISTORY_PER_SYMBOL_CURRENT_IDS_SANITIZED.csv
docs\researchops\source_native_futures_daily_data_library\16_SYMBOL_FULL_DAILY_HISTORY\raw_provider_archive\DATABENTO\20260530_DATED_CONTRACT_FULL_AVAILABLE_HISTORY_PER_SYMBOL_CURRENT_IDS\provider_condition_metadata_2026-05-30\provider_condition_ledger\DATABENTO_16_SYMBOL_DATED_CONTRACT_PROVIDER_CONDITION_ROW_JOIN.csv
docs\researchops\source_native_futures_daily_data_library\16_SYMBOL_FULL_DAILY_HISTORY\raw_provider_archive\DATABENTO\20260530_DATED_CONTRACT_FULL_AVAILABLE_HISTORY_PER_SYMBOL_CURRENT_IDS\provider_condition_metadata_2026-05-30\provider_condition_ledger\DATABENTO_16_SYMBOL_DATED_CONTRACT_PROVIDER_CONDITION_LEDGER.csv
docs\researchops\source_native_futures_daily_data_library\16_SYMBOL_FULL_DAILY_HISTORY\raw_provider_archive\DATABENTO\20260530_DATED_CONTRACT_FULL_AVAILABLE_HISTORY_PER_SYMBOL_CURRENT_IDS\provider_condition_metadata_2026-05-30\provenance\DATABENTO_PROVIDER_CONDITION_METADATA_STATUS.csv
```

Outputs created:

```text
docs\researchops\source_native_futures_daily_data_library\16_SYMBOL_DAILY_LIBRARY_PROMOTION_READINESS\manifest\CARVER_16_SYMBOL_DATABENTO_DAILY_LIBRARY_CANONICAL_MANIFEST_2026-05-30.csv
docs\researchops\source_native_futures_daily_data_library\16_SYMBOL_DAILY_LIBRARY_PROMOTION_READINESS\provenance\CARVER_16_SYMBOL_DAILY_LIBRARY_PROMOTION_READINESS_STATUS_2026-05-30.csv
docs\researchops\source_native_futures_daily_data_library\16_SYMBOL_DAILY_LIBRARY_PROMOTION_READINESS\provenance\CARVER_16_SYMBOL_DAILY_LIBRARY_PROMOTION_READINESS_SHA256SUMS_2026-05-30.txt
```

Policy encoded:

```text
available provider condition -> candidate row for later Development/Reconciliation promotion shape
Databento degraded provider condition -> excluded from strategy-facing candidate set and retained only as quarantined archive row
blocked/unresolved provider condition -> excluded/fail-closed
```

Counts:

```text
MANIFEST_ROWS: 16
ARCHIVE_ROWS: 4568
NORMAL_CANDIDATE_ROWS: 4483
DEGRADED_QUARANTINED_ROWS: 85
OTHER_BLOCKED_OR_UNRESOLVED_ROWS: 0
```

This provenance record authorizes no new provider API access, no new market-data request, no diagnostics, no backtests, no forecasts, no positions, no costs, no carry, no trend, no volatility/risk calculations, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.
