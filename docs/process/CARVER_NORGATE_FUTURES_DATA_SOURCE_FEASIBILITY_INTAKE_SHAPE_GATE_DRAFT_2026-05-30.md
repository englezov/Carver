# Carver Norgate Futures Data-Source Feasibility And Intake Shape Gate Draft

Date: 2026-05-30

Status:

```text
PROCESS_ONLY_CARVER_NORGATE_FUTURES_DATA_SOURCE_FEASIBILITY_INTAKE_SHAPE_GATE_DRAFT_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Evaluate Norgate Data Futures Package as a backup programmatic/local daily futures data-source candidate for the Carver 16-symbol source-native futures intake pilot and eventual Appendix C path.

This draft follows:

```text
docs/process/CARVER_DATABENTO_API_ACCESS_REMEDIATION_RESULT_2026-05-30.md
docs/process/CARVER_SOURCE_NATIVE_FUTURES_HISTORICAL_DATA_SOURCE_SELECTION_DECISION_2026-05-30.md
docs/process/CARVER_16_SYMBOL_NINJATRADER_CHART_SERIES_DOWNLOAD_TEST_FAIL_CLOSED_RESULT_2026-05-30.md
```

This artifact is process-only. It uses read-only inspection of current Carver artifacts and public Norgate / PyPI documentation only. It does not purchase a subscription, log in to Norgate, download an installer, run a provider client, download data, parse market rows, run diagnostics, run backtests, compute forecasts, compute positions, compute costs, compute carry, compute trend, access OOS/Lockbox/Forward, use CFD adapters, use old QuantLab active pipelines, tune, deploy, trade, promote, stage Git changes, commit, push, update a PR, or perform remote repository operations.

## Locked Carver Need

Lane:

```text
SOURCE_NATIVE_FUTURES
```

Locked 16-row pilot manifest:

```text
ZT JUN26
ZF JUN26
ZN JUN26
MES JUN26
MNQ JUN26
M2K JUN26
MYM JUN26
QM JUL26
RB JUL26
ZC JUL26
ZS JUL26
ZM JUL26
ZL JUL26
ZW JUL26
HE JUN26
LE JUN26
```

Target completed trading dates:

```text
2026-05-18 through 2026-05-22 inclusive
```

Current blockers:

```text
NINJATRADER_CHART_SERIES_PATH_FAIL_CLOSED_FOR_14_OF_16_MANIFEST_ROWS
DATABENTO_METADATA_AUTHENTICATION_BLOCKED_HTTP_401
NO_16_SYMBOL_RAW_OR_SANITIZED_MARKET_FILES_EXIST
```

The backup path must preserve exact dated-contract identity. It must not use continuous contracts, substitute `CL` for `QM`, substitute E-mini/full-size products for micro products, drop rows, reweight, or silently alter the pilot.

## Public Norgate Documentation Basis

Static public sources inspected:

```text
Norgate Futures Package:
https://norgatedata.com/futurespackage.php

Norgate Data Content Tables:
https://norgatedata.com/data-content-tables.php

Norgate subscription price page:
https://norgatedata.com/prices.php

Norgate Python package:
https://pypi.org/project/norgatedata/
```

Relevant public documentation atoms:

- Norgate Futures Package covers around 100 futures markets across 11 exchanges or exchange groups.
- Coverage is selective rather than exhaustive.
- The public futures coverage table says the shown symbols are for individual contracts, and that continuous contracts are also provided for each market.
- The futures package advertises 30+ years of individual contract daily price history, end-of-day updates, and pre-built continuous contracts.
- Norgate states that, unless otherwise specified, the close price is the official settlement price rather than the last-traded price.
- Norgate provides spot-month continuous contracts in unadjusted and back-adjusted forms, but those remain closed for this Carver pilot because the pilot is dated-contract only.
- The Python package is a Python interface to Norgate Data, but the Norgate Data Updater is Windows-only and must be running for the package to work.
- The Python package documents `price_timeseries`, daily interval support, futures metadata functions, and futures contract/session/market symbol discovery.
- The Python package documents futures metadata fields such as tick size, point value, first notice date, session type, futures market/session symbols, and all contracts for a session symbol.

## Public Coverage Check Against The Locked 16

Public Norgate coverage table visibility:

| Carver code | Locked contract | Public Norgate table evidence | Feasibility status before subscription |
|---|---|---|---|
| `ZT` | `ZT JUN26` | `2-Year U.S. T-Note ... ZT` | `PUBLIC_TABLE_MATCH` |
| `ZF` | `ZF JUN26` | `5-Year U.S. T-Note ... ZF` | `PUBLIC_TABLE_MATCH` |
| `ZN` | `ZN JUN26` | `10-Year U.S. T-Note ... ZN` | `PUBLIC_TABLE_MATCH` |
| `MES` | `MES JUN26` | `Micro E-mini S&P 500 ... MES` | `PUBLIC_TABLE_MATCH` |
| `MNQ` | `MNQ JUN26` | `Micro E-mini Nasdaq 100 ... MNQ` | `PUBLIC_TABLE_MATCH` |
| `M2K` | `M2K JUN26` | `Micro E-mini Russell 2000 ... M2K` | `PUBLIC_TABLE_MATCH` |
| `MYM` | `MYM JUN26` | `Micro E-mini Dow ... MYM` | `PUBLIC_TABLE_MATCH` |
| `QM` | `QM JUL26` | no `QM` / E-mini Crude Oil row visible in the public table; `CL` appears | `PUBLIC_TABLE_UNRESOLVED_FAIL_CLOSED` |
| `RB` | `RB JUL26` | `RBOB Gasoline ... RB` | `PUBLIC_TABLE_MATCH` |
| `ZC` | `ZC JUL26` | `Corn ... ZC` | `PUBLIC_TABLE_MATCH` |
| `ZS` | `ZS JUL26` | `Soybean ... ZS` | `PUBLIC_TABLE_MATCH` |
| `ZM` | `ZM JUL26` | `Soybean Meal ... ZM` | `PUBLIC_TABLE_MATCH` |
| `ZL` | `ZL JUL26` | `Soybean Oil ... ZL` | `PUBLIC_TABLE_MATCH` |
| `ZW` | `ZW JUL26` | `Chicago SRW Wheat ... ZW` | `PUBLIC_TABLE_MATCH` |
| `HE` | `HE JUN26` | `Lean Hogs ... HE` | `PUBLIC_TABLE_MATCH` |
| `LE` | `LE JUN26` | `Live Cattle ... LE` | `PUBLIC_TABLE_MATCH` |

Interpretation:

```text
NORGATE_PUBLIC_TABLE_SUPPORTS_15_OF_16_LOCKED_CODES
NORGATE_PUBLIC_TABLE_DOES_NOT_LOCK_QM
NORGATE_AS_EXACT_16_SYMBOL_SOURCE_REMAINS_UNRESOLVED_BEFORE_SUBSCRIPTION_OR_VENDOR_CONFIRMATION
```

`CL` must not be treated as a substitute for `QM`. If Norgate does not support `QM` individual contracts, then the exact 16-row Carver pilot cannot pass on Norgate without a separate operator-authorized redecision that either narrows the pilot or changes the source universe. This draft authorizes neither.

## Feasibility Assessment

### Strengths

Disposition:

```text
STRONG_BACKUP_CANDIDATE_FOR_SCALABLE_DAILY_FUTURES_RESEARCH
```

Reasons:

- Local Windows database plus Python access fits the Carver local reproducibility preference better than manual web downloads.
- Individual futures contracts are explicitly part of the package.
- Daily historical depth is broad enough for later Development/Reconciliation work after separate authorization.
- Official settlement-close default is useful for Carver daily futures research, as long as it is explicitly labeled and not confused with last-trade close.
- Futures metadata functions may help harden contract identity, first notice handling, point value, tick size, session type, and symbol/session mapping.
- ASCII export is also available as a fallback raw quarantine format if Python access is blocked, but this would need a separate gate.

### Weaknesses

Disposition:

```text
NOT_READY_FOR_EXACT_16_SYMBOL_EXECUTION_GATE
```

Reasons:

- The public table does not visibly lock `QM`; exact mini crude support must be confirmed before any 16-row all-or-nothing intake.
- Norgate is subscription/local-install based. It is not a cloud HTTP request that can be tested without purchase/login/install.
- Public docs do not by themselves prove the exact individual contract symbol syntax for `JUN26` / `JUL26` rows, such as whether the local symbol form is `MES-2026M`, `MES-2026M` equivalent, or another local canonical representation.
- Public docs do not by themselves prove the exact row-level daily bar date semantics for Carver's completed trading-date policy.
- Public docs say close is official settlement unless otherwise specified, while the NinjaTrader pilot was `Last` bars. This is acceptable only if the Norgate path is explicitly relabeled as settlement-close daily data and not merged with prior Last-bar semantics.
- Eventual Appendix C coverage remains unresolved because Norgate coverage is selective rather than exhaustive and around 100 markets, while Appendix C is a 102-row source universe with some micro/mini/product-variant sensitivity.

## Required Pre-Purchase / Pre-Install Proofs

Before any Norgate purchase, login, installation, client execution, or data access, a follow-up process-only proof packet should require:

```text
NORGATE_QM_SUPPORT_PROOF_OR_FAIL_CLOSED
NORGATE_16_SYMBOL_INDIVIDUAL_CONTRACT_SYMBOL_SYNTAX_PROOF
NORGATE_DAILY_DATE_AND_CLOSE_SEMANTICS_PROOF
NORGATE_PYTHON_ACCESS_LOCAL_PROVENANCE_LAYOUT_PROOF
NORGATE_LICENSE_AND_EXPORT_RESTRICTION_REVIEW
```

Accepted proof sources:

- public Norgate contract-details spreadsheet, if accessible without login and treated as static documentation;
- Norgate public docs that explicitly list individual contract symbol syntax;
- vendor pre-sales support reply confirming exact support for `QM` and all 16 locked codes, without sending or receiving market data;
- local operator screenshot or exported documentation from a trial/purchase only if a later gate separately authorizes login/install.

Unaccepted proofs:

- assuming `CL` can substitute for `QM`;
- assuming Norgate continuous contracts prove individual dated-contract support;
- assuming public root-symbol coverage proves a specific `JUN26` / `JUL26` contract row exists;
- using market rows as proof before an intake execution gate.

## Candidate Norgate Intake Shape

If a later gate proves exact support and authorizes installation/access, the Norgate quarantine path should use:

```text
docs/researchops/first_data_intake/quarantine/NORGATE_16_SYMBOL_DAILY_2026-05-18_2026-05-22/
```

Required subdirectories:

```text
raw_provider_output/
raw_provider_metadata/
sanitized_bars/
row_validation/
provenance/
```

Required pre-market-row metadata checks before accepting price rows:

- provider package/version;
- local Norgate Data Updater version if available;
- exact Norgate database/update timestamp;
- exact Norgate symbol/session/contract syntax for every locked row;
- futures market symbol;
- futures market session symbol;
- all available individual contracts for each session symbol, limited to metadata only until data access is separately authorized;
- first notice date where applicable;
- point value;
- tick size;
- session type;
- close-price semantic label, especially `OFFICIAL_SETTLEMENT_CLOSE_UNLESS_OTHERWISE_SPECIFIED`.

The first Norgate market-row gate, if ever opened, should request or export only the exact locked dated contracts and date window. It must preserve raw provider output or raw exported ASCII, record SHA256 hashes, then create a sanitized quarantine CSV only if all expected rows pass validation.

## Candidate Sanitized Schema

The sanitized combined quarantine CSV should use:

```text
row_id
author_market_code
selected_source_native_dated_contract
norgate_market_symbol
norgate_session_symbol
norgate_individual_contract_symbol
norgate_session_type
norgate_close_semantics
provider_bar_date
carver_completed_trading_date_candidate
completed_trading_date_policy_status
open
high
low
close
volume
open_interest
source_file
source_file_sha256
source_row_number
```

Required row status:

```text
NORGATE_DAILY_SETTLEMENT_CLOSE_QUARANTINE_ONLY_NOT_NINJATRADER_LAST_BAR_NOT_STRATEGY_INPUT_AUTHORIZATION
```

If Norgate provides no volume or open interest for a row, the field must be explicit and row-statused. Missing optional fields must not be silently fabricated.

## Timestamp And Date Policy

Norgate daily records should be treated as date-labeled end-of-day futures records unless later documentation proves a finer timestamp policy.

Initial policy:

```text
provider_bar_date = Norgate Date field
carver_completed_trading_date_candidate = provider_bar_date
completed_trading_date_policy_status = NORGATE_DAILY_DATE_LABEL_QUARANTINE_ONLY_NOT_EXCHANGE_SESSION_TIMESTAMP_LOCK
```

This is sufficient for quarantine mechanics, symbol identity checks, and provider path evaluation. It is not sufficient for strategy computation until a later session/date semantics gate decides whether Norgate's date and settlement semantics are acceptable for the Carver book machinery.

## Row Validation Semantics

Expected count for exact 16-row pass:

```text
16 symbols * 5 daily rows = 80 rows
```

The later execution gate must validate:

- all 16 manifest rows preserved;
- no continuous contracts;
- no parent-symbol or session aggregate substituted for the individual dated contract;
- no `CL` in place of `QM`;
- no full-size/E-mini product in place of a micro product;
- exact `JUN26` / `JUL26` dated contract identity;
- provider date in `2026-05-18` through `2026-05-22`;
- exactly five daily rows per symbol;
- no duplicate symbol/date;
- no missing symbol/date;
- required OHLC fields present;
- numeric OHLC values;
- positive OHLC values;
- `high >= low`;
- non-negative volume if volume is supplied;
- raw output hash present;
- provenance present.

All-or-nothing disposition:

```text
ALL_16_SYMBOLS_PASS_OR_BATCH_FAILS_CLOSED
```

If `QM` remains unsupported or unresolved, the exact 16-symbol Norgate pilot must fail closed. A smaller Norgate pilot may only be opened by a separate process-only redecision before any data access.

## Audit Requirements

After any future Norgate access or execution gate, run an automatic lean hostile audit over:

- proof of exact symbol coverage;
- individual contract identity;
- close/date semantics;
- raw provider preservation;
- sanitized schema;
- row-validation ledger;
- all-or-nothing pass/fail disposition;
- non-authorization boundaries.

An Opus audit is not required for this feasibility draft. A later Opus audit may be appropriate before treating Norgate as the broader Appendix C production research source.

## Decision

Decision:

```text
KEEP_NORGATE_AS_BACKUP_DAILY_FUTURES_PROVIDER_CANDIDATE
DO_NOT_OPEN_NORGATE_MARKET_ROW_INTAKE_YET
REQUIRE_QM_AND_EXACT_16_SYMBOL_CONTRACT_SYNTAX_PROOF_BEFORE_PURCHASE_OR_INSTALLATION_GATE
```

Updated provider ordering:

```text
DATABENTO_REMAINS_PRIMARY_IF_AUTH_FIXES_PROMPTLY
NORGATE_IS_BEST_BACKUP_FOR_LOCAL_PROGRAMMATIC_DAILY_HISTORY
NORGATE_EXACT_16_SYMBOL_PATH_BLOCKED_UNTIL_QM_AND_SYMBOL_SYNTAX_ARE_PROVEN
NINJATRADER_REMAINS_SECONDARY_LOCAL_SANITY_AND_STATIC_IDENTITY_SOURCE
```

## Required Next Gate

Recommended next clean gate:

```text
CARVER_NORGATE_16_SYMBOL_PUBLIC_CONTRACT_SUPPORT_PROOF_OR_FAIL_CLOSED_DECISION_GATE
```

That gate should use only public/static Norgate documentation or vendor pre-sales confirmation to decide:

- whether `QM` individual contracts are supported;
- exact Norgate individual contract symbol syntax for all 16 selected contracts;
- whether the 16-row pilot can remain exact under Norgate;
- whether to authorize purchase/trial/install later, keep Norgate blocked, or narrow to a smaller Norgate-supported pilot.

## Closed Boundaries

Still closed:

```text
subscription purchase
provider login
installer download
provider client execution
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

This draft authorizes no Norgate subscription purchase, no Norgate login, no installer download, no provider API/client execution, no data download, no market-row parsing, no diagnostics, no backtests, no forecasts, no positions, no costs, no carry, no trend, no OOS, no Lockbox, no Forward, no CFD adapter work, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no GitHub staging, no commit, no push, no PR update/opening, and no remote repository operations.
