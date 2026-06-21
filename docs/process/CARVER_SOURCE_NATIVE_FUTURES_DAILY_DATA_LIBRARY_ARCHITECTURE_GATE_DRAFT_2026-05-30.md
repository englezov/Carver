# Carver Source-Native Futures Daily Data Library Architecture Gate Draft

Date: 2026-05-30

Status:

```text
PROCESS_ONLY_CARVER_SOURCE_NATIVE_FUTURES_DAILY_DATA_LIBRARY_ARCHITECTURE_GATE_DRAFT_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Define a central Carver source-native futures daily data library architecture for the full book strategy and portfolio program.

This gate replaces the one-off-download mindset with a single governed local data foundation:

```text
SOURCE_NATIVE_FUTURES_DAILY_DATA_LIBRARY
```

The library is intended to support future Carver strategy and portfolio chapters by storing provider-sourced daily futures data once, preserving raw provenance, creating normalized Carver tables, and promoting data from quarantine to strategy-readiness only through separate audited gates.

This artifact is process-only. It authorizes no provider purchase, no provider login, no installer download, no provider client execution, no data download, no market-row parsing, no diagnostics, no backtests, no forecasts, no positions, no costs, no carry, no trend, no OOS/Lockbox/Forward access, no CFD adapter work, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote repository operations.

## Background

Current state:

```text
APPENDIX_C_SOURCE_UNIVERSE_LOCKED_AS_102_ROW_BOOK_FRAME
P05_P06_P07_SYNTHETIC_PORTFOLIO_SURFACES_COMPLETE_AND_OPUS_AUDITED
MES_06_26_TINY_NINJATRADER_QUARANTINE_INTAKE_COMPLETE_AND_OPUS_AUDITED
16_SYMBOL_NINJATRADER_BATCH_PATH_FAIL_CLOSED
DATABENTO_AUTHENTICATION_BLOCKED_ON_METADATA_ONLY_ENDPOINTS
NORGATE_PUBLIC_SUPPORT_PROOF_FAIL_CLOSED_FOR_EXACT_16_SYMBOL_QM_UNRESOLVED
```

The conclusion is architectural:

```text
DATA_SHOULD_BE_A_SHARED_LIBRARY_NOT_A_PER_STRATEGY_CHORE
```

The Carver program may eventually test many standalone strategies, source-native portfolio sleeves, complete book portfolios, and readiness branches. Daily futures data should therefore be acquired, archived, normalized, validated, and promoted centrally.

## Public Provider Documentation Basis

Public documentation inspected for this architecture:

```text
Databento Historical / examples / schemas / symbology / GLBX.MDP3 documentation:
https://databento.com/docs/examples/basics-historical/eod
https://databento.com/docs/schemas-and-data-formats
https://databento.com/docs/standards-and-conventions/symbology
https://databento.com/datasets/GLBX.MDP3

Norgate Futures Package / content / pricing / Python package:
https://norgatedata.com/futurespackage.php
https://norgatedata.com/data-content-tables.php
https://norgatedata.com/prices.php
https://pypi.org/project/norgatedata/

CME DataMine:
https://www.cmegroup.com/datamine.html
```

No provider login, provider API call, installer download, data download, or market-row inspection was performed.

## Library Scope

The library lane is:

```text
SOURCE_NATIVE_FUTURES
```

Primary intended data class:

```text
DAILY_FUTURES
```

Initial supported research needs:

- Appendix C / Jumbo portfolio source universe readiness.
- The 16-symbol CME Group pilot branch.
- P05 complete trend portfolio data-readiness.
- P06 complete carry portfolio data-readiness.
- P07 complete combined trend/carry portfolio data-readiness.
- Later standalone strategy candidates from the book.
- Later complete book portfolios.

The library is not a strategy engine, not a backtester, not a diagnostic engine, not a signal engine, not a portfolio construction engine, and not a trading system.

## Provider Selection Requirements

Any provider selected for the library must satisfy or explicitly fail-close the following before market-row access:

1. Supports source-native futures, not CFD translations.
2. Provides individual dated futures contracts, not only continuous contracts.
3. Provides daily OHLCV or daily settlement-close records with clear semantics.
4. Provides instrument metadata or symbol-resolution evidence sufficient to distinguish product code, exchange, contract month, contract variant, currency, multiplier semantics, point value, tick size, tick value, first notice/last trade/expiration/delivery or cash-settlement rules where applicable.
5. Provides a reproducible batch or local database access path.
6. Allows raw provider output preservation or exact export snapshots.
7. Allows local hash-bound archival and provenance.
8. Allows update/reconciliation without silently rewriting historical raw archives.
9. Has licensing terms compatible with local research use and internal archival.
10. Can scale beyond a tiny pilot toward the full book program.

Provider classes:

| Provider path | Current architecture status | Role |
|---|---|---|
| `Databento Historical` | `PREFERRED_PROGRAMMATIC_PATH_BUT_AUTH_BLOCKED` | Best cloud/API architecture if account auth is fixed. |
| `Norgate Futures Package` | `BEST_LOCAL_DAILY_HISTORY_BACKUP_BUT_EXACT_16_QM_UNRESOLVED` | Strong local daily-history candidate; requires support confirmation or install/static metadata gate. |
| `CME DataMine` | `OFFICIAL_SOURCE_AUTHORITY_CANDIDATE_HEAVIER_WORKFLOW` | Strong official settlement/source path; likely heavier and narrower operationally. |
| `Barchart OnDemand` | `COMMERCIAL_API_CANDIDATE_PRICING_ACCESS_UNRESOLVED` | Credible if access/pricing is acceptable. |
| `NinjaTrader Desktop` | `SECONDARY_LOCAL_SANITY_AND_STATIC_IDENTITY_SOURCE` | Not primary batch library due cache/UI/provider-state dependence. |
| `Interactive Brokers` | `BROKER_RECONCILIATION_CANDIDATE_NOT_PRIMARY_LIBRARY` | Broker/TWS oriented, not clean primary research archive. |
| `Local CSV only` | `ARCHIVE_FORMAT_NOT_SOURCE_AUTHORITY` | Acceptable only when tied to source/provider provenance. |

## Supported Universe Policy

Canonical book universe:

```text
APPENDIX_C_102_ROW_SOURCE_UNIVERSE_REMAINS_CANONICAL
```

Provider-supported universe:

```text
PROVIDER_SUPPORTED_SUBSET_OR_PROVIDER_SUPPORTED_SUPERSET_MUST_BE_EXPLICITLY_LEDGERED
```

Rules:

- The Appendix C source universe must not be rewritten to fit a provider.
- Provider coverage gaps are recorded as blocked or unresolved.
- No silent drop, substitution, alias, full-size/micro/mini replacement, continuous-contract fallback, or reweighting is allowed.
- A provider-supported subset may be used for a pilot only after a separate redecision states that the subset is a pilot and not the full book portfolio.
- Alias rows require explicit alias-readiness gates.
- Variant mismatches remain fail-closed unless a later source/provider gate resolves them.

Required universe ledgers:

```text
source_universe_lock.csv
provider_universe_coverage.csv
provider_symbol_mapping.csv
contract_identity_status.csv
data_availability_status.csv
library_promotion_status.csv
```

## Dated-Contract And Continuous-Contract Policy

Primary archive class:

```text
INDIVIDUAL_DATED_FUTURES_CONTRACTS_FIRST
```

Dated contracts must carry:

```text
row_id
source_market_code
provider_symbol
provider_contract_symbol
exchange
currency
contract_month
contract_year
contract_month_code
first_notice_date
last_trade_date
expiration_date
delivery_or_cash_settlement_flag
contract_family
contract_variant
```

Continuous contracts may be stored only as explicitly labeled provider/reference artifacts:

```text
CONTINUOUS_CONTRACT_REFERENCE_ONLY_NOT_SOURCE_SUBSTITUTE
```

Continuous contracts must never silently replace dated contracts in source-native strategy work. Any continuous-contract use requires a separate policy gate that defines roll rule, adjustment method, data lineage, source faithfulness, and strategy-readiness implications.

## Raw Archive Layout

Recommended root:

```text
docs/researchops/source_native_futures_daily_data_library/
```

Provider raw archives:

```text
raw_provider_archive/<PROVIDER>/<DATASET_OR_PACKAGE>/<YYYYMMDD_RUN_ID>/
```

Required raw subdirectories:

```text
request_or_export_manifest/
provider_metadata/
raw_market_files/
raw_hashes/
provider_logs_redacted/
```

Sanitized Carver tables:

```text
sanitized/contract_daily_ohlcv/
sanitized/contract_daily_settlement/
sanitized/instrument_metadata/
sanitized/contract_lifecycle/
sanitized/provider_symbol_map/
sanitized/validation_ledgers/
sanitized/promotion_ledgers/
```

All files must be append-only or versioned by run ID. Raw provider files must not be silently overwritten. Corrections require a new run ID and a supersession ledger.

## Sanitized Daily OHLCV Schema

Minimum contract daily OHLCV schema:

```text
library_run_id
provider
provider_dataset_or_package
provider_schema_or_export_type
row_id
source_market_code
provider_symbol
provider_contract_symbol
exchange
currency
contract_month
contract_year
provider_bar_date
provider_timestamp_utc
carver_completed_trading_date_candidate
date_policy_status
price_semantics
open
high
low
close
volume
open_interest
source_file
source_file_sha256
source_row_number
validation_status
promotion_status
```

Allowed normalization:

- provider numeric scale decoding;
- date/time string normalization;
- joining static instrument and contract metadata;
- adding provenance and validation fields;
- converting provider export format to a stable Carver CSV/Parquet form.

Forbidden transformations at library-ingest stage:

- returns;
- PnL;
- forecasts;
- positions;
- costs;
- carry;
- trend;
- volatility/risk calculations;
- rolling continuous series construction unless separately authorized;
- back-adjustment unless separately authorized;
- settlement substitution unless explicitly source-labeled;
- imputation;
- forward fill;
- row dropping;
- symbol substitution;
- reweighting.

## Price And Date Semantics

Every daily row must declare one of:

```text
PROVIDER_UTC_DAILY_OHLCV
PROVIDER_EXCHANGE_SESSION_DAILY_OHLCV
PROVIDER_OFFICIAL_SETTLEMENT_DAILY
LOCAL_NINJATRADER_TEMPLATE_TRADINGDAY_LAST_BAR
UNRESOLVED_DAILY_SEMANTICS_FAIL_CLOSED
```

Every daily row must also declare:

```text
DATE_POLICY_STATUS
PRICE_SEMANTICS
SESSION_POLICY_STATUS
SETTLEMENT_POLICY_STATUS
```

The library may ingest quarantine data with unresolved strategy semantics, but strategy-readiness promotion requires the relevant date/session/close policy to be explicitly accepted for that strategy or portfolio gate.

## Metadata, Provenance, And Hash Requirements

Every library run must record:

- provider name;
- provider account/API surface used, without secrets;
- package/client/downloader version where applicable;
- dataset/package/schema/export type;
- request/export parameters;
- symbol list;
- date range;
- raw file paths;
- raw file SHA256 values;
- sanitized file paths;
- sanitized file SHA256 values;
- run timestamp in UTC;
- operator authorization artifact;
- row counts requested;
- row counts returned;
- row counts accepted;
- row counts rejected;
- rejection reason counts;
- no-diagnostics/no-backtest/no-forecast/no-position flags.

Secrets, API keys, account tokens, cookies, and credentials must not be written into the library.

## Update Policy

The library should support two update modes:

```text
FULL_HISTORY_SNAPSHOT
INCREMENTAL_DAILY_UPDATE
```

Full-history snapshots:

- create a new run ID;
- preserve raw provider output;
- create hash-bound sanitized tables;
- compare to prior snapshots;
- record revisions or provider backfills without overwriting prior raw files.

Incremental updates:

- append only after a completed-bar rule is locked;
- reject partial current-day bars unless a gate explicitly permits a different class;
- reconcile against provider calendar/session expectations;
- preserve missing/stale/duplicate ledgers;
- never auto-fill missing daily records.

No update may trigger diagnostics, strategy calculations, forecasts, positions, costs, carry, trend, backtests, OOS/Lockbox/Forward, deployment, trading, or promotion.

## Validation Policy

Initial quarantine validation:

- row shape;
- required fields present;
- numeric OHLC values;
- positive OHLC values;
- `high >= low`;
- non-negative volume if supplied;
- date range in request/export manifest;
- no duplicate provider contract/date rows;
- no unapproved continuous contracts;
- no unapproved symbol substitutions;
- source file hash present;
- provenance present.

Contract-readiness validation:

- symbol maps to intended source row;
- dated contract identity resolved;
- contract lifecycle does not conflict with the requested date range;
- first notice / last trade / expiration / delivery or cash-settlement constraints are recorded;
- exchange/currency/multiplier/tick/point semantics are locked or fail-closed.

Strategy-readiness validation:

- only opened by later strategy or portfolio gates;
- requires accepted session/date/price semantics;
- requires approved universe/subset;
- requires completed-bar policy;
- requires missing/stale/duplicate policy;
- requires data lineage from raw provider archive to sanitized table.

## Promotion Rules

Library states:

```text
RAW_ARCHIVED
QUARANTINE_SANITIZED
CONTRACT_IDENTITY_READY
SESSION_DATE_POLICY_READY
STRATEGY_INPUT_READY_FOR_NAMED_GATE
DIAGNOSTIC_OR_BACKTEST_AUTHORIZED_BY_SEPARATE_GATE
```

Default after ingest:

```text
QUARANTINE_SANITIZED_NOT_STRATEGY_INPUT
```

Data may not become strategy input merely because it is downloaded, parsed, or validated for row shape. Strategy-readiness must name:

- strategy or portfolio gate;
- exact instruments or universe;
- exact date window;
- exact price/date/session semantics;
- exact missing-data behavior;
- exact source lineage;
- explicit diagnostic/backtest boundary.

## Data Lineage

Every strategy or portfolio using the library must be able to trace each row:

```text
strategy_or_portfolio_artifact
-> library_promotion_ledger
-> sanitized_table_row
-> raw_provider_file_sha256
-> provider_request_or_export_manifest
-> provider/source documentation basis
```

No strategy may read files directly from raw provider archive. Strategy code, if later authorized, must read only from promoted Carver library tables for the named gate.

## Provider-Specific Architecture Notes

### Databento

Desired role:

```text
PRIMARY_PROGRAMMATIC_PROVIDER_IF_AUTH_REMEDIATED
```

Fit:

- programmatic historical API;
- documented futures dataset and schemas;
- raw DBN and conversion workflows;
- symbology and definition/reference paths;
- batch-compatible request model.

Current blocker:

```text
ACCOUNT_OR_API_KEY_AUTHENTICATION_BLOCKED_ON_METADATA_ONLY_ENDPOINTS
```

No Databento data download may proceed until metadata authentication succeeds and a later execution gate authorizes the exact request.

### Norgate

Desired role:

```text
PRIMARY_LOCAL_DAILY_HISTORY_BACKUP_CANDIDATE
```

Fit:

- local Windows daily data package;
- individual futures contracts;
- continuous futures as separately labeled reference;
- settlement-close oriented daily records;
- Python interface to local data updater.

Current blocker:

```text
EXACT_16_SYMBOL_PUBLIC_SUPPORT_PROOF_FAIL_CLOSED_QM_UNRESOLVED
```

No Norgate purchase, login, install, client execution, or data access may proceed without a later authorization gate.

### NinjaTrader

Desired role:

```text
SECONDARY_LOCAL_SANITY_AND_STATIC_IDENTITY_SOURCE
```

Fit:

- local static instrument definitions;
- exact small manual/cache-proven quarantine checks;
- potential broker/platform reconciliation.

Current blocker:

```text
NOT_PRIMARY_BATCH_DATA_LIBRARY
```

NinjaTrader UI/cache/provider state made 16-symbol batch loading unreliable. It should not be the central library source unless a later gate proves a robust non-manual batch path.

### CME DataMine

Desired role:

```text
OFFICIAL_SOURCE_AUTHORITY_OR_SETTLEMENT_DATA_CANDIDATE
```

Fit:

- official CME Group source path;
- potentially useful for settlement or rulebook-aligned source authority.

Current blocker:

```text
HEAVIER_ORDERING_LICENSING_AND_DELIVERY_WORKFLOW
```

DataMine may be opened later if Databento/Norgate remain blocked or if official settlement authority is required.

## Required Next Gate

Selected next gate:

```text
CARVER_SOURCE_NATIVE_DAILY_FUTURES_DATA_LIBRARY_PROVIDER_SELECTION_DECISION_GATE
```

That gate should decide whether to:

- wait for Databento support and retry metadata auth;
- ask Norgate pre-sales to confirm `QM` and exact contract support;
- open a Norgate purchase/trial/install static-metadata gate;
- open a CME DataMine feasibility/order-shape gate;
- use a smaller NinjaTrader cache-proven branch only as a temporary library mechanics test.

The next gate must remain process-only unless separately authorized.

## Audit Requirements

This architecture draft should receive an automatic lean hostile audit before any provider purchase/login/install/download gate.

Any later provider execution gate that creates market-row archives must receive a lean hostile audit covering:

- raw provenance;
- hash preservation;
- sanitized schema;
- validation ledgers;
- non-substitution;
- strategy-readiness boundaries;
- no diagnostics/backtests/forecasts/positions/costs/carry/trend.

An Opus audit should be considered before promoting a provider-backed library beyond quarantine into a reusable Part One portfolio or multi-strategy Development/Reconciliation data foundation.

## Decision

Decision:

```text
CENTRAL_DAILY_FUTURES_DATA_LIBRARY_ARCHITECTURE_SELECTED
PER_STRATEGY_MANUAL_DOWNLOADS_REJECTED_AS_PRIMARY_WORKFLOW
MARKET_ROW_ACCESS_REMAINS_CLOSED
```

Reason:

The Carver book program needs one source-native daily futures data foundation. A central library reduces duplicated downloads, prevents silent provider-specific drift, and gives every later strategy and portfolio gate a common lineage from provider raw output to promoted Carver tables.

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

This architecture gate authorizes no subscription purchase, no provider login, no free-trial registration, no installer download, no provider API/client execution, no data download, no market-row parsing, no diagnostics, no backtests, no forecasts, no positions, no costs, no carry, no trend, no OOS, no Lockbox, no Forward, no CFD adapter work, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no GitHub staging, no commit, no push, no PR update/opening, and no remote repository operations.
