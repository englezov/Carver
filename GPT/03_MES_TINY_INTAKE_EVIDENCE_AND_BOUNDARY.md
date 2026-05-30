# MES Tiny Intake Evidence And Boundary

Date: 2026-05-30

Status:

```text
OPUS_INPUT_PACKET_MES_TINY_INTAKE_EVIDENCE_AND_BOUNDARY_NOT_EXECUTION
```

## Why MES Only

The 16-row NinjaTrader-supported pilot remained fail-closed for broad intake. A later dated-contract selection path selected a single tiny row:

```text
row_id: APPENDIX_C_174_006
author_market_code: MES
selected_source_native_dated_contract: MES 06-26
bar_type: Last
timeframe: 1 Day
completed trading dates: 2026-05-18 through 2026-05-22
```

The MES path is a tiny proof that Carver can touch one source-native futures historical-bar slice under quarantine. It is not a portfolio data opening.

## Static MES Lock

MES static dated-contract lock:

```text
docs/researchops/first_data_intake/CARVER_NINJATRADER_SUPPORTED_PILOT_MES_STATIC_DATED_CONTRACT_LOCK_2026-05-30.csv
rows: 1
sha256: 65E3F7C5E4E6D0B71DA78F6BDE742DFC2EA08263438A84F9D5ACD219FD6C1A7F
```

Selected fields:

```text
row_id: APPENDIX_C_174_006
author_market_code: MES
descriptive_name: S&P 500 (micro)
lane_class: SOURCE_NATIVE_FUTURES
official_product_name: Micro E-mini S&P 500 Futures
official_product_code: MES
selected_source_native_dated_contract: MES 06-26
selected_ninjatrader_local_contract: MES 06-26
target_completed_trading_date_start: 2026-05-18
target_completed_trading_date_end: 2026-05-22
final_static_readiness_for_later_tiny_historical_bar_intake: YES
final_static_readiness_status: STATIC_READY_FOR_LATER_TINY_HISTORICAL_BAR_INTAKE_NOT_DATA_AUTHORIZATION
```

## Shape Gate Boundary

Shape gate:

```text
docs/process/CARVER_NINJATRADER_SUPPORTED_PILOT_MES_TINY_HISTORICAL_BAR_INTAKE_SHAPE_GATE_DRAFT_2026-05-30.md
```

Allowed row set:

```text
APPENDIX_C_174_006 / MES / MES 06-26 only
```

Allowed completed trading-date window:

```text
2026-05-18 through 2026-05-22 inclusive
```

Allowed fields:

```text
provider_symbol
local_contract
timestamp_utc
open
high
low
close
volume
```

Timestamp requirement:

```text
UTC_END_OF_BAR_TIMESTAMP_ONLY
```

Canonical completed trading-date mapping:

```text
LOCAL_NINJATRADER_TEMPLATE_TRADINGDAY
Trading Hours template: CME US Index Futures ETH
Template timezone: Central Standard Time
```

## Helper Boundary

Repo helper files:

```text
tools/nt8/CarverMesTinyDailyExporter.cs
tools/nt8/CarverMesTinyDailyExporterSessionEndUtc.cs
```

Boundary claimed by the process:

- helper is MES-only;
- helper is 1 Day Last-only;
- helper is disarmed by default in repo;
- helper writes only to the locked MES quarantine raw-source path;
- v2 helper writes template-derived UTC session-end timestamps rather than observed NinjaTrader daily `Time[0]` when that does not match the locked policy;
- v2 corrected output is helper raw output with template-derived UTC session-end timestamps, not provider-verbatim NinjaTrader `Time[0]` output;
- no diagnostics, forecasts, backtests, positions, or trading functions are part of the helper.

The reviewer should inspect whether the helper or process docs accidentally allow wider symbols, dates, series types, bar periods, or output paths.

## Initial Fail-Closed Raw File

First raw file:

```text
docs/researchops/first_data_intake/quarantine/MES_06_26_2026-05-18_2026-05-22/raw_source_copy/MES_06-26_Daily_Last_2026-05-18_2026-05-22.csv
sha256: 9313F3A3128DF0A989F7DEE09C007C81246D968AE5FE690ECE47143199F91FF1
```

Disposition:

```text
FAIL_CLOSED_UTC_END_OF_BAR_TEMPLATE_SESSION_ALIGNMENT_FAILED_NO_SANITIZED_BARS_CREATED
```

Reason:

```text
raw timestamps: 23:00:00Z
mapped central wall time in May 2026: 18:00 Central
locked template session end: 16:00 Central
```

The initial file was preserved and fail-closed. It was not silently repaired in place.

## Corrected V2 Raw File

Corrected raw file:

```text
docs/researchops/first_data_intake/quarantine/MES_06_26_2026-05-18_2026-05-22/raw_source_copy/MES_06-26_Daily_Last_2026-05-18_2026-05-22_TEMPLATE_SESSION_END_UTC.csv
sha256: 39C9572844D184523CBC47E394BEDAB8BAC246F7CDB9134FEF2535F68325984E
```

Clarification:

```text
HELPER_RAW_OUTPUT_WITH_TEMPLATE_DERIVED_UTC_SESSION_END_TIMESTAMPS_NOT_PROVIDER_VERBATIM_TIME0
```

Corrected timestamps:

```text
2026-05-18T21:00:00Z
2026-05-19T21:00:00Z
2026-05-20T21:00:00Z
2026-05-21T21:00:00Z
2026-05-22T21:00:00Z
```

Row validation:

```text
docs/researchops/first_data_intake/quarantine/MES_06_26_2026-05-18_2026-05-22/provenance/MES_06_26_DAILY_2026-05-18_2026-05-22_TEMPLATE_SESSION_END_ROW_VALIDATION.csv
rows: 5
row_status PASS: 5
sha256: 2356D272E20782CFBE710364020EFFDB5DFE13A065DA0E7D091C67879DAEF33E
```

Sanitized bars:

```text
docs/researchops/first_data_intake/quarantine/MES_06_26_2026-05-18_2026-05-22/sanitized_bars/MES_06_26_DAILY_2026-05-18_2026-05-22.csv
rows: 5
sha256: 0FE54EA66726F26B0C2A984D3B75465AC373B234F516391472F1E61D2AF6B383
```

Status ledger:

```text
docs/researchops/first_data_intake/quarantine/MES_06_26_2026-05-18_2026-05-22/provenance/MES_06_26_DAILY_2026-05-18_2026-05-22_INTAKE_EXECUTION_STATUS.csv
sha256: 99653E84A3F2EB0EB5A4777C06B3249591D8F0668D465DFB03E1FF9211D6D557
intake_status: PASS_TINY_HISTORICAL_BAR_INTAKE_QUARANTINE_ONLY
accepted_market_rows: 5
diagnostics_run: NO
backtests_run: NO
provider_api_access: NO
old_quantlab_pipeline_use: NO
remote_operations: NO
```

## Audit Risk Points

The reviewer should attack these points:

- Is MES 06-26 correctly separated from continuous MES or broader MES data?
- Does the timestamp correction create source-faithfulness risk by replacing NinjaTrader observed daily bar time with template-derived session end?
- Is that correction adequately disclosed as a quarantine parser policy rather than a price-data transformation?
- Are the raw source copies preserved separately?
- Does the sanitized file remain quarantine-only?
- Does any wording imply the 5 rows can be used for diagnostics, forecasts, position sizing, or backtests?
- Does any helper or process file allow a wider symbol/date/timeframe than MES 06-26, 1 Day Last, 2026-05-18 to 2026-05-22?
