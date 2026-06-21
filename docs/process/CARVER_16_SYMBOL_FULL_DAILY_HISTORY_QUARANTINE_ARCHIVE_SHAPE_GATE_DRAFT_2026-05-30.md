# Carver 16-Symbol Full Daily History Quarantine Archive Shape Gate Draft

Date: 2026-05-30

Status:

```text
PROCESS_ONLY_CARVER_16_SYMBOL_FULL_DAILY_HISTORY_QUARANTINE_ARCHIVE_SHAPE_GATE_DRAFT_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Define the process boundary for a later separately authorized full-history daily futures archive intake for the locked 16-symbol pilot universe.

This gate follows:

```text
docs/process/CARVER_SOURCE_NATIVE_FUTURES_DAILY_DATA_LIBRARY_ARCHITECTURE_GATE_DRAFT_2026-05-30.md
docs/researchops/first_data_intake/CARVER_16_SYMBOL_NINJATRADER_STATIC_DATED_CONTRACT_SELECTION_2026-05-30.csv
```

This artifact is process-only. It defines the archive shape before provider purchase, provider login, installer download, provider API/client execution, data download, market-row parsing, diagnostics, backtests, forecasts, positions, costs, carry, trend, OOS/Lockbox/Forward access, CFD adapter work, old QuantLab active-pipeline use, tuning, deployment, trading, promotion, Git staging, commit, push, PR update/opening, or remote repository operations.

## Locked Universe

Lane:

```text
SOURCE_NATIVE_FUTURES
```

Locked 16-symbol pilot universe:

| Row ID | Code | Descriptive name | Static selected dated contract used for prior five-day pilot |
|---|---:|---|---|
| `APPENDIX_C_172_001` | `ZT` | `2-year US` | `ZT JUN 2026` |
| `APPENDIX_C_172_003` | `ZF` | `5-year US` | `ZF JUN 2026` |
| `APPENDIX_C_172_004` | `ZN` | `10-year US` | `ZN JUN 2026` |
| `APPENDIX_C_174_006` | `MES` | `S&P 500 (micro)` | `MES JUN 2026` |
| `APPENDIX_C_174_002` | `MNQ` | `Nasdaq (micro)` | `MNQ JUN 2026` |
| `APPENDIX_C_174_004` | `M2K` | `Russell 2000 smallcap (micro)` | `M2K JUN 2026` |
| `APPENDIX_C_174_001` | `MYM` | `Dow Jones industrial (micro)` | `MYM JUN 2026` |
| `APPENDIX_C_182_002` | `QM` | `WTI Crude (mini)` | `QM JUL 2026` |
| `APPENDIX_C_182_004` | `RB` | `Gasoline` | `RB JUL 2026` |
| `APPENDIX_C_183_003` | `ZC` | `Corn` | `ZC JUL 2026` |
| `APPENDIX_C_183_010` | `ZS` | `Soybeans` | `ZS JUL 2026` |
| `APPENDIX_C_183_011` | `ZM` | `Soybean Meal` | `ZM JUL 2026` |
| `APPENDIX_C_183_012` | `ZL` | `Soybean Oil` | `ZL JUL 2026` |
| `APPENDIX_C_183_013` | `ZW` | `Wheat` | `ZW JUL 2026` |
| `APPENDIX_C_183_005` | `HE` | `Lean Hogs` | `HE JUN 2026` |
| `APPENDIX_C_183_006` | `LE` | `Live Cattle` | `LE JUN 2026` |

The prior static selected dated contracts prove contract-selection shape for the five-day pilot. They do not limit full-history archive scope to one expiry month. A full-history archive must cover the available individual dated contracts for each root market, subject to provider support and lifecycle metadata.

## Provider/Data-Access Decision Boundary

This shape gate does not select or access a provider. It defines the required shape for the later data-access gate.

The next execution provider must be chosen by a separate decision that resolves one of:

```text
DATABENTO_AUTH_REMEDIATED_AND_SELECTED_FOR_FULL_HISTORY
NORGATE_PURCHASE_TRIAL_INSTALL_STATIC_METADATA_SELECTED
CME_DATAMINE_FEASIBILITY_ORDER_SELECTED
BARCHART_OR_OTHER_PROVIDER_SELECTED
NINJATRADER_SELECTED_ONLY_IF_NON_MANUAL_FULL_HISTORY_BATCH_PATH_IS_PROVEN
```

Provider data-access authorization must separately name:

- provider;
- account/API/client surface;
- exact symbol universe;
- exact historical range policy;
- raw-output path;
- permitted schemas or export types;
- whether individual dated contracts, continuous reference series, or both are requested;
- whether official settlement, last trade, UTC OHLCV, or exchange-session OHLCV semantics are expected.

This gate keeps all data access closed.

## Full-History Meaning

For this chapter, full history means:

```text
ALL_AVAILABLE_DAILY_HISTORY_FROM_THE_SELECTED_PROVIDER_FOR_THE_LOCKED_16_ROOT_MARKETS
```

Primary archive:

```text
INDIVIDUAL_DATED_CONTRACT_DAILY_HISTORY
```

Optional reference archive:

```text
CONTINUOUS_CONTRACT_DAILY_HISTORY_REFERENCE_ONLY
```

The execution gate must not silently impose a short fixed date window. It must either:

1. request the provider's complete available history for the selected 16 root markets; or
2. use a provider-supported full-history export package; or
3. fail closed if the provider cannot express full available daily history in a reproducible way.

If the provider requires a start date, the execution gate must record the earliest provider-supported date per root market or contract family before row parsing. It must not choose a performance-looking or result-looking date window.

## Individual Dated-Contract Archive Policy

Individual dated contracts are the primary source-native archive.

Required per contract:

```text
row_id
source_market_code
root_symbol
provider_symbol
provider_contract_symbol
exchange
currency
contract_month_code
contract_month
contract_year
first_notice_date
last_trade_date
expiration_date
delivery_or_cash_settlement_flag
contract_family
contract_variant
provider_available_start_date
provider_available_end_date
```

Provider metadata must distinguish:

- outright futures from options;
- outright futures from spreads;
- individual dated contracts from continuous contracts;
- micro/mini/full-size variants;
- local aliases from source-native symbols.

No continuous contract may be used to fill missing individual contract rows.

## Continuous-Contract Reference Policy

Continuous contracts are optional and reference-only.

Status if stored:

```text
CONTINUOUS_CONTRACT_REFERENCE_ONLY_NOT_SOURCE_SUBSTITUTE_NOT_STRATEGY_INPUT
```

Continuous reference series must carry:

```text
roll_rule
adjustment_method
provider_continuous_symbol
provider_documentation_basis
raw_file_sha256
not_a_replacement_for_dated_contract_history
```

No continuous series may enter strategy-readiness unless a later strategy-specific or portfolio-specific gate opens and source-locks the roll/adjustment policy.

## Zero-Silent-Row-Skip Validation

The full-history archive may contain provider gaps, non-trading days, contract lifecycle gaps, discontinued contracts, or unavailable roots. Those are not automatic failures. The failure is silent omission.

Required principle:

```text
ZERO_SILENT_ROW_SKIP
```

Required ledgers:

```text
expected_contracts_by_root.csv
provider_returned_contracts_by_root.csv
missing_contracts_or_unresolved_contracts.csv
daily_row_counts_by_contract.csv
missing_or_duplicate_dates_by_contract.csv
rejected_rows.csv
accepted_rows_summary.csv
```

Every expected provider contract and every parsed row must end in one of:

```text
ACCEPTED_QUARANTINE
REJECTED_SHAPE_INVALID
REJECTED_IDENTITY_UNRESOLVED
REJECTED_DATE_POLICY_UNRESOLVED
REJECTED_DUPLICATE
REJECTED_PROVIDER_GAP_RECORDED
BLOCKED_PROVIDER_UNAVAILABLE
BLOCKED_PROVIDER_SYMBOL_UNRESOLVED
```

No row may be dropped merely because it is inconvenient. No missing provider date may be forward-filled, backfilled, imputed, or repaired.

## Raw Provider Archive Layout

Required root:

```text
docs/researchops/source_native_futures_daily_data_library/16_SYMBOL_FULL_DAILY_HISTORY/
```

Provider-specific run root:

```text
raw_provider_archive/<PROVIDER>/<YYYYMMDD_RUN_ID>/
```

Required subdirectories:

```text
request_or_export_manifest/
provider_metadata/
raw_market_files/
raw_hashes/
provider_logs_redacted/
license_or_terms_snapshot/
```

Required raw records:

- exact request/export manifest;
- provider package/client/downloader version if applicable;
- raw market files exactly as delivered or exported;
- raw file SHA256 ledger;
- provider symbol-resolution output;
- provider contract metadata output;
- provider data-availability output if available;
- redacted logs that prove the provider path and run status without exposing secrets.

Raw files are append-only by run ID. No raw file may be overwritten in place. A corrected run must create a new run ID and supersession ledger.

## Sanitized Quarantine Schema

Primary sanitized contract daily table:

```text
library_run_id
provider
provider_dataset_or_package
provider_schema_or_export_type
row_id
source_market_code
root_symbol
provider_symbol
provider_contract_symbol
exchange
currency
contract_month_code
contract_month
contract_year
provider_bar_date
provider_timestamp_utc
carver_completed_trading_date_candidate
date_policy_status
price_semantics
session_policy_status
settlement_policy_status
open
high
low
close
volume
open_interest
source_file
source_file_sha256
source_row_number
row_validation_status
promotion_status
```

Allowed formatting/normalization:

- provider numeric scale decoding;
- date/time string normalization;
- attaching row ID and static source identity;
- attaching provider contract metadata;
- converting provider export format into Carver CSV or Parquet.

Forbidden transformations:

- returns;
- PnL;
- forecasts;
- positions;
- costs;
- carry;
- trend;
- volatility or risk calculations;
- continuous rolling;
- back-adjustment;
- settlement replacement unless the provider row itself is explicitly settlement data;
- imputation;
- forward fill;
- synthetic row creation;
- row dropping;
- symbol substitution;
- reweighting.

Default promotion status:

```text
QUARANTINE_SANITIZED_NOT_STRATEGY_INPUT
```

## Price And Date Semantics

Every accepted daily row must declare one of:

```text
PROVIDER_UTC_DAILY_OHLCV
PROVIDER_EXCHANGE_SESSION_DAILY_OHLCV
PROVIDER_OFFICIAL_SETTLEMENT_DAILY
LOCAL_NINJATRADER_TEMPLATE_TRADINGDAY_LAST_BAR
UNRESOLVED_DAILY_SEMANTICS_FAIL_CLOSED
```

Every row must also carry:

```text
date_policy_status
price_semantics
session_policy_status
settlement_policy_status
```

If the provider supplies settlement-close daily data, it must not be relabeled as last-trade close. If the provider supplies UTC daily bars, it must not be relabeled as exchange-session completed TradingDay bars. Strategy-readiness requires a later policy gate that accepts the provider semantics for a named strategy or portfolio.

## Metadata, Provenance, And Hash Requirements

The later execution gate must create:

```text
provenance/<PROVIDER>_16_SYMBOL_FULL_DAILY_HISTORY_PROVENANCE.md
provenance/<PROVIDER>_16_SYMBOL_FULL_DAILY_HISTORY_INTAKE_STATUS.csv
validation/<PROVIDER>_16_SYMBOL_FULL_DAILY_HISTORY_ROW_VALIDATION.csv
validation/<PROVIDER>_16_SYMBOL_FULL_DAILY_HISTORY_CONTRACT_COVERAGE.csv
validation/<PROVIDER>_16_SYMBOL_FULL_DAILY_HISTORY_MISSING_DUPLICATE_LEDGER.csv
hashes/<PROVIDER>_16_SYMBOL_FULL_DAILY_HISTORY_SHA256SUMS.txt
```

Provenance must include:

- provider name;
- provider account/API/client surface used, without secrets;
- provider package/client/downloader version;
- run ID;
- UTC run timestamp;
- operator authorization artifact;
- exact universe requested;
- exact history range policy;
- raw file paths and SHA256;
- sanitized file paths and SHA256;
- total roots requested;
- total provider roots resolved;
- total contracts returned;
- total daily rows parsed;
- total rows accepted;
- total rows rejected;
- rejection reason counts;
- explicit `NO` flags for diagnostics, backtests, forecasts, positions, costs, carry, trend, old QuantLab active-pipeline use, remote operations, deployment, trading, and promotion.

Secrets, API keys, tokens, cookies, account IDs beyond non-secret provider labels, and credentials must not be recorded.

## Update Policy

The first execution is a full-history snapshot:

```text
FULL_HISTORY_SNAPSHOT_RUN
```

Future updates require a separate update gate and must use:

```text
INCREMENTAL_DAILY_UPDATE_RUN
```

Update rules:

- append under a new run ID;
- never overwrite the original raw snapshot;
- record provider revisions/backfills;
- reject partial current-day records unless a later gate explicitly opens them;
- keep missing/stale/duplicate ledgers;
- never auto-fill gaps.

## Fail-Closed Rules

The later execution gate must fail closed on:

- provider not selected by a prior decision;
- provider authentication unavailable;
- provider terms/license not compatible with local archive;
- root symbol unresolved;
- individual contract identity unresolved;
- `QM` replaced by `CL`;
- micro/mini/full-size substitution;
- continuous-only output when individual contracts are required;
- option/spread output mixed into outright futures table;
- raw provider file not hash-bound;
- missing request/export manifest;
- missing contract metadata;
- missing row provenance;
- malformed OHLC values;
- `high < low`;
- non-positive OHLC where positive prices are required;
- duplicate contract/date row not explicitly rejected;
- missing provider rows silently skipped;
- imputation, fill, repair, back-adjustment, rolling, or settlement substitution outside declared policy;
- any need to inspect diagnostics, returns, forecasts, positions, costs, carry, trend, or performance to decide acceptance.

## Promotion Boundaries

This archive may only reach:

```text
RAW_ARCHIVED
QUARANTINE_SANITIZED
```

It does not create:

```text
CONTRACT_IDENTITY_READY_FOR_ALL_ROWS
SESSION_DATE_POLICY_READY_FOR_STRATEGY
STRATEGY_INPUT_READY
DIAGNOSTIC_READY
BACKTEST_READY
PORTFOLIO_READY
TRADING_READY
PROMOTION_READY
```

Any later strategy or portfolio use must open a named gate that promotes a named subset from quarantine to strategy-input readiness with explicit date/session/price semantics and source lineage.

## Audit Requirements

Before any provider data-access/download execution gate, this shape draft should receive an automatic lean hostile audit.

After any future full-history archive execution, run an automatic lean hostile audit over:

- provider/data-access boundary;
- raw archive preservation;
- hash ledgers;
- contract coverage ledgers;
- zero-silent-row-skip ledgers;
- sanitized schema;
- price/date semantics labels;
- non-substitution;
- no diagnostics/backtests/forecasts/positions/costs/carry/trend;
- promotion boundaries.

An Opus audit should be considered before the full-history archive is promoted beyond quarantine into reusable multi-strategy or Part One portfolio Development/Reconciliation input.

## Required Next Gate

Selected next gate:

```text
CARVER_16_SYMBOL_FULL_DAILY_HISTORY_PROVIDER_ACCESS_DECISION_GATE
```

That gate should decide whether the first full-history archive execution path is:

- Databento, if authentication is fixed;
- Norgate, if `QM` and exact contract support are confirmed or a trial/install static-metadata gate is authorized;
- CME DataMine, if official-source ordering is selected;
- another provider with explicit dated futures history;
- blocked until a provider can support the exact 16-symbol full-history archive.

## Decision

Decision:

```text
16_SYMBOL_FULL_DAILY_HISTORY_QUARANTINE_ARCHIVE_SHAPE_DEFINED
FIVE_DAY_TEST_WINDOW_RETIRED_AS_PRIMARY_DATA_UNIT
FULL_HISTORY_ARCHIVE_REQUIRES_SEPARATE_PROVIDER_ACCESS_GATE
```

Reason:

The central Carver data library should ingest useful full daily histories once, not repeat manual or per-strategy downloads. The five-day window remains useful as plumbing history, but the book program needs a governed full-history archive with raw provenance, zero silent skipping, and strict quarantine boundaries before any strategy use.

## Closed Boundaries

Still closed:

```text
subscription purchase
provider login
free-trial registration
installer download
provider API/client execution
data download
market-row parsing
diagnostics
backtests
forecasts
positions
costs
carry
trend
OOS
Lockbox
Forward
CFD adapters
old QuantLab active-pipeline use
tuning
deployment
trading
promotion
Git staging
commit
push
PR update/opening
remote repository operations
```

## Non-Authorization

This shape gate authorizes no subscription purchase, no provider login, no free-trial registration, no installer download, no provider API/client execution, no data download, no market-row parsing, no diagnostics, no backtests, no forecasts, no positions, no costs, no carry, no trend, no OOS, no Lockbox, no Forward, no CFD adapter work, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no GitHub staging, no commit, no push, no PR update/opening, and no remote repository operations.
