# Carver 16-Symbol Full Daily History Provider-Access Decision

Date: 2026-05-30

Status:

```text
PROCESS_ONLY_CARVER_16_SYMBOL_FULL_DAILY_HISTORY_PROVIDER_ACCESS_DECISION_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Select the next provider-access path for the first full-history daily futures quarantine archive execution for the locked 16-symbol pilot universe.

This decision follows:

```text
docs/process/CARVER_16_SYMBOL_FULL_DAILY_HISTORY_QUARANTINE_ARCHIVE_SHAPE_GATE_DRAFT_2026-05-30.md
docs/process/CARVER_SOURCE_NATIVE_FUTURES_DAILY_DATA_LIBRARY_ARCHITECTURE_GATE_DRAFT_2026-05-30.md
```

This artifact is process-only. It authorizes no subscription purchase, provider login, free-trial registration, installer download, provider API/client execution, data download, market-row parsing, diagnostics, backtests, forecasts, positions, costs, carry, trend, OOS/Lockbox/Forward, CFD adapters, old QuantLab active-pipeline use, tuning, deployment, trading, promotion, Git staging, commit, push, PR update/opening, or remote repository operations.

## Locked Archive Target

Lane:

```text
SOURCE_NATIVE_FUTURES
```

Root universe:

```text
ZT, ZF, ZN, MES, MNQ, M2K, MYM, QM, RB, ZC, ZS, ZM, ZL, ZW, HE, LE
```

Archive target:

```text
ALL_AVAILABLE_DAILY_HISTORY_FROM_SELECTED_PROVIDER_FOR_LOCKED_16_ROOT_MARKETS
INDIVIDUAL_DATED_CONTRACT_DAILY_HISTORY_PRIMARY
CONTINUOUS_CONTRACT_DAILY_HISTORY_REFERENCE_ONLY_OPTIONAL
ZERO_SILENT_ROW_SKIP
QUARANTINE_ONLY_NOT_STRATEGY_INPUT
```

## Public Documentation Checked

Static public sources checked for the provider decision:

```text
Databento historical futures / OHLCV / symbology documentation:
https://databento.com/docs/examples/futures/futures-introduction/special-conventions-for-futures-on-databento
https://databento.com/docs/api-reference-historical/helpers/pit-symbol-map
https://databento.com/docs/standards-and-conventions

Norgate futures package:
https://norgatedata.com/futurespackage.php

CME DataMine:
https://www.cmegroup.com/market-data/datamine-historical-data/index.html

Barchart OnDemand getHistory:
https://www.barchart.com/ondemand/api/getHistory
```

No provider login, API key use, client execution, installer download, data download, or market-row parsing was performed.

## Provider Candidates

### Databento Historical

Decision:

```text
PRIMARY_PROVIDER_ACCESS_PATH_IF_AUTHENTICATION_IS_REMEDIATED
```

Why:

- Programmatic historical access fits full-history archive automation.
- `GLBX.MDP3` is the CME Group futures dataset already shaped for the 16-symbol pilot.
- Databento supports raw futures symbology and multiple historical schemas, including daily OHLCV and metadata/reference paths.
- It can preserve request manifests, raw provider outputs, and symbol-resolution evidence in a clean quarantine archive.
- It avoids manual NinjaTrader cache/UI dependence.

Current blocker:

```text
DATABENTO_METADATA_AUTHENTICATION_401_BLOCK
```

Evidence required before any Databento data-access gate:

```text
OFFICIAL_CLIENT_METADATA_CALL_SUCCEEDS
OR
DATABENTO_SUPPORT_CONFIRMS_ACCOUNT_API_KEY_ACTIVE_AND_METADATA_ACCESS_WORKING
```

Minimum metadata-only proof before market-row request:

```text
client.metadata.list_schemas(dataset="GLBX.MDP3") succeeds
client.metadata.list_datasets() succeeds
no key value printed or recorded
```

Only after that proof may a separate Databento execution gate authorize:

- API key use without exposing the key;
- full-history daily request shape;
- raw DBN/provider output preservation;
- symbology/definition metadata retrieval;
- quarantine-only parsing and validation.

### Norgate Futures Package

Decision:

```text
BACKUP_LOCAL_DAILY_HISTORY_PATH_IF_QM_AND_EXACT_CONTRACT_SUPPORT_ARE_CONFIRMED
```

Why:

- Strong local Windows daily-history architecture.
- Public docs describe individual futures contracts and daily end-of-day updates.
- Public docs state close is official settlement unless otherwise specified.
- Python access to the local Norgate Data Updater could support repeatable local archive construction.

Current blocker:

```text
PUBLIC_NORGATE_SUPPORT_PROOF_FAIL_CLOSED_FOR_EXACT_16_QM_UNRESOLVED
```

Evidence required before any Norgate purchase/trial/install gate:

```text
NORGATE_CONFIRMS_QM_E_MINI_CRUDE_INDIVIDUAL_CONTRACTS_SUPPORTED
NORGATE_CONFIRMS_EXACT_16_ROOT_MARKETS_SUPPORTED
NORGATE_CONFIRMS_INDIVIDUAL_CONTRACT_SYMBOL_SYNTAX_DISCOVERABLE
NORGATE_CONFIRMS_DAILY_CLOSE_SEMANTICS_FOR_THESE_MARKETS
NORGATE_LICENSE_COMPATIBLE_WITH_LOCAL_RESEARCH_ARCHIVE
```

Evidence may come from public Norgate documentation or non-secret vendor pre-sales text supplied by the operator. No market data is needed for this proof.

Only after that proof may a separate Norgate gate authorize trial/purchase/install and static metadata inspection. Market-row archive execution would still require another later gate.

### CME DataMine

Decision:

```text
OFFICIAL_SOURCE_BACKUP_IF_DATABENTO_AND_NORGATE_REMAIN_BLOCKED
```

Why:

- Official CME Group source path for historical futures/options and settlements.
- Strong candidate when official settlement authority matters more than ease of setup.

Current blocker:

```text
HEAVY_ORDERING_LICENSING_DELIVERY_WORKFLOW_NOT_SELECTED_FOR_FIRST_EXECUTION
```

Evidence required before any CME DataMine order/access gate:

- exact product/dataset list covering all 16 roots;
- whether individual dated contracts and full daily history are available;
- delivery method and raw-file preservation path;
- pricing/licensing compatibility with local research archive;
- settlement/OHLCV field semantics.

### Barchart OnDemand Or Other Vendor

Decision:

```text
TERTIARY_COMMERCIAL_API_BACKUP
```

Why:

- Barchart `getHistory` publicly supports historical time-series requests for futures, including daily and continuous-style intervals.

Current blocker:

```text
ACCESS_PRICING_CONTRACT_IDENTITY_AND_FULL_HISTORY_SCOPE_UNRESOLVED
```

Evidence required before any vendor access gate:

- exact support for the 16 root markets and individual dated contracts;
- full-history availability;
- pricing/access level;
- raw export/API provenance;
- date/settlement/last semantics;
- local archive license compatibility.

### NinjaTrader Desktop

Decision:

```text
NOT_SELECTED_FOR_FULL_HISTORY_PROVIDER_ACCESS
```

Why:

NinjaTrader remains useful for static instrument identity and small local sanity checks, but the 16-symbol chart/AddDataSeries helper failed closed due to local availability/cache behavior. It is not a clean full-history archive provider unless a later gate proves a robust, non-manual, provider-backed batch path.

## Decision

Selected provider-access path for the first full-history archive:

```text
DATABENTO_PRIMARY_CONDITIONAL_ON_AUTH_REMEDIATION
```

Selected backup path:

```text
NORGATE_BACKUP_CONDITIONAL_ON_QM_AND_EXACT_16_SUPPORT_CONFIRMATION
```

Not selected for first execution:

```text
NINJATRADER_FULL_HISTORY_BATCH
CME_DATAMINE_FIRST_EXECUTION
BARCHART_OR_OTHER_VENDOR_FIRST_EXECUTION
```

Current execution state:

```text
FULL_HISTORY_MARKET_ROW_ACCESS_BLOCKED_PENDING_PROVIDER_ACCESS_EVIDENCE
```

This is not a retreat to five-day tests. The selected archive unit remains full available daily history. The block is provider access evidence, not archive design.

## Required Next Gate

Selected next clean gate:

```text
CARVER_DATABENTO_AUTH_REMEDIATION_RETRY_OR_PROVIDER_SWITCH_DECISION_GATE
```

That gate should use only metadata/auth checks or operator-provided support response to decide:

- whether Databento auth is fixed and can proceed to a full-history data-access execution gate;
- whether Databento remains blocked and the project should open the Norgate vendor confirmation gate;
- whether to skip both and open CME DataMine/Barchart feasibility.

If the operator wants to avoid waiting for Databento support, the alternative immediate gate is:

```text
CARVER_NORGATE_VENDOR_PRE_SALES_CONFIRMATION_GATE
```

## Evidence Required Before Any Provider Purchase/Login/Install/API/Data Gate

Mandatory evidence:

```text
PROVIDER_SELECTED_BY_PROCESS_DECISION
EXACT_16_ROOT_SUPPORT_EVIDENCE
INDIVIDUAL_DATED_CONTRACT_SUPPORT_EVIDENCE
FULL_HISTORY_DAILY_AVAILABILITY_EVIDENCE
RAW_ARCHIVE_ALLOWED_BY_PROVIDER_TERMS
DATE_AND_PRICE_SEMANTICS_DISCLOSED
ZERO_SILENT_ROW_SKIP_VALIDATION_PLAN_ACCEPTED
SECRETS_HANDLING_PLAN_ACCEPTED
QUARANTINE_ONLY_BOUNDARY_ACCEPTED
```

Without this evidence, provider data access remains fail-closed.

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

This decision authorizes no subscription purchase, no provider login, no free-trial registration, no installer download, no provider API/client execution, no data download, no market-row parsing, no diagnostics, no backtests, no forecasts, no positions, no costs, no carry, no trend, no OOS, no Lockbox, no Forward, no CFD adapter work, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no GitHub staging, no commit, no push, no PR update/opening, and no remote repository operations.
