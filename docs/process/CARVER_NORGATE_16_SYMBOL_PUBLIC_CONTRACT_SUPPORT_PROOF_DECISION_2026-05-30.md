# Carver Norgate 16-Symbol Public Contract Support Proof Decision

Date: 2026-05-30

Status:

```text
PROCESS_ONLY_CARVER_NORGATE_16_SYMBOL_PUBLIC_CONTRACT_SUPPORT_PROOF_DECISION_FAIL_CLOSED_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Decide whether public/static Norgate documentation is sufficient to treat Norgate Data Futures Package as supporting the exact locked Carver 16-symbol dated futures daily intake pilot.

This decision follows:

```text
docs/process/CARVER_NORGATE_FUTURES_DATA_SOURCE_FEASIBILITY_INTAKE_SHAPE_GATE_DRAFT_2026-05-30.md
```

This artifact is process-only. It uses read-only inspection of current Carver artifacts and public Norgate / PyPI documentation only. No subscription was purchased, no login was used, no installer was downloaded, no provider client was executed, no data was downloaded, no market rows were parsed, no diagnostics or backtests were run, no forecasts, positions, costs, carry, or trend were computed, no OOS/Lockbox/Forward was accessed, no CFD adapters or old QuantLab active pipelines were used, no tuning/deployment/trading/promotion occurred, and no Git staging/commit/push/PR or remote repository operation was performed.

## Locked Pilot Under Review

Lane:

```text
SOURCE_NATIVE_FUTURES
```

Locked pilot:

| Row ID | Code | Locked dated contract |
|---|---:|---|
| `APPENDIX_C_172_001` | `ZT` | `ZT JUN26` |
| `APPENDIX_C_172_003` | `ZF` | `ZF JUN26` |
| `APPENDIX_C_172_004` | `ZN` | `ZN JUN26` |
| `APPENDIX_C_174_006` | `MES` | `MES JUN26` |
| `APPENDIX_C_174_002` | `MNQ` | `MNQ JUN26` |
| `APPENDIX_C_174_004` | `M2K` | `M2K JUN26` |
| `APPENDIX_C_174_001` | `MYM` | `MYM JUN26` |
| `APPENDIX_C_182_002` | `QM` | `QM JUL26` |
| `APPENDIX_C_182_004` | `RB` | `RB JUL26` |
| `APPENDIX_C_183_003` | `ZC` | `ZC JUL26` |
| `APPENDIX_C_183_010` | `ZS` | `ZS JUL26` |
| `APPENDIX_C_183_011` | `ZM` | `ZM JUL26` |
| `APPENDIX_C_183_012` | `ZL` | `ZL JUL26` |
| `APPENDIX_C_183_013` | `ZW` | `ZW JUL26` |
| `APPENDIX_C_183_005` | `HE` | `HE JUN26` |
| `APPENDIX_C_183_006` | `LE` | `LE JUN26` |

Target date window:

```text
2026-05-18 through 2026-05-22 inclusive
```

Required proof threshold:

```text
EXACT_16_SYMBOL_DATED_CONTRACT_SUPPORT_OR_FAIL_CLOSED
```

No full-size, E-mini, micro, adjacent product, continuous contract, local alias, CFD symbol, or alternate source row may substitute for a locked manifest row.

## Static Public Sources Inspected

Public/static sources:

```text
Norgate Futures Package:
https://norgatedata.com/futurespackage.php

Norgate Data Content Tables:
https://norgatedata.com/data-content-tables.php

Norgate subscription price page:
https://norgatedata.com/prices.php

Norgate Python package:
https://pypi.org/project/norgatedata/

Premium Data / DataTools public support pages discovered while looking for the contract-detail spreadsheet:
https://www.premiumdata.net/support/downloads.php
https://www.premiumdata.net/support/understandingfuturesdata.php
```

No vendor pre-sales support confirmation was supplied in the current context.

No subscriber/trial-only Norgate download area was accessed.

## Public Documentation Atoms

Verified public atoms:

- Norgate Futures Package covers around 100 futures markets across 11 exchanges or exchange groups.
- Norgate states that coverage is selective rather than exhaustive.
- The futures coverage table states that shown symbols are for individual contracts and that continuous contracts are also provided for each market.
- Norgate advertises individual contract daily price history, end-of-day updates, and pre-built continuous contracts for the Futures Data package.
- Norgate states that, unless otherwise specified, close price is the official settlement price, not last-traded price.
- Norgate public pricing lists Futures Data with 30+ year individual contract daily price history, end-of-day updates, and pre-built continuous contracts.
- The `norgatedata` Python package is a Python interface to Norgate Data.
- The Python package requires the Windows-only Norgate Data Updater to be running.
- The Python package documents daily price time series access and futures metadata functions, including tick size, point value, first notice date, session type, market/session symbols, and all contracts for a futures session symbol.
- Public Premium Data / DataTools pages indicate a Futures Contract Detail spreadsheet exists, but downloads are behind current subscriber or free-trial login.
- Public Premium Data / DataTools documentation states futures markets consist of individual contract months that trade side by side, each with a unique expiry date.

## Public Coverage Result

Coverage visible in Norgate public data-content table:

| Code | Public table result | Status |
|---|---|---|
| `ZT` | `2-Year U.S. T-Note ... ZT` | `PUBLIC_ROOT_SYMBOL_MATCH` |
| `ZF` | `5-Year U.S. T-Note ... ZF` | `PUBLIC_ROOT_SYMBOL_MATCH` |
| `ZN` | `10-Year U.S. T-Note ... ZN` | `PUBLIC_ROOT_SYMBOL_MATCH` |
| `MES` | `Micro E-mini S&P 500 ... MES` | `PUBLIC_ROOT_SYMBOL_MATCH` |
| `MNQ` | `Micro E-mini Nasdaq 100 ... MNQ` | `PUBLIC_ROOT_SYMBOL_MATCH` |
| `M2K` | `Micro E-mini Russell 2000 ... M2K` | `PUBLIC_ROOT_SYMBOL_MATCH` |
| `MYM` | `Micro E-mini Dow ... MYM` | `PUBLIC_ROOT_SYMBOL_MATCH` |
| `QM` | no public table row found for `QM` / E-mini Crude; `CL` is listed | `PUBLIC_ROOT_SYMBOL_UNRESOLVED_FAIL_CLOSED` |
| `RB` | `RBOB Gasoline ... RB` | `PUBLIC_ROOT_SYMBOL_MATCH` |
| `ZC` | `Corn ... ZC` | `PUBLIC_ROOT_SYMBOL_MATCH` |
| `ZS` | `Soybean ... ZS` | `PUBLIC_ROOT_SYMBOL_MATCH` |
| `ZM` | `Soybean Meal ... ZM` | `PUBLIC_ROOT_SYMBOL_MATCH` |
| `ZL` | `Soybean Oil ... ZL` | `PUBLIC_ROOT_SYMBOL_MATCH` |
| `ZW` | `Chicago SRW Wheat ... ZW` | `PUBLIC_ROOT_SYMBOL_MATCH` |
| `HE` | `Lean Hogs ... HE` | `PUBLIC_ROOT_SYMBOL_MATCH` |
| `LE` | `Live Cattle ... LE` | `PUBLIC_ROOT_SYMBOL_MATCH` |

Summary:

```text
PUBLIC_ROOT_SYMBOL_MATCH_COUNT: 15
PUBLIC_ROOT_SYMBOL_UNRESOLVED_FAIL_CLOSED_COUNT: 1
UNRESOLVED_CODE: QM
```

The public coverage table is enough to keep Norgate as a strong backup candidate. It is not enough to prove exact 16-symbol support.

## Exact Dated-Contract Syntax Proof

Public documentation does not lock the exact Norgate individual contract symbol syntax for the target rows:

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

The Python package examples show individual futures contracts using a `market-year-monthcode` style, for example `CL-2017X`, and show functions for discovering all contracts for a futures session symbol. However, no local Norgate client was executed and no subscription/trial area was accessed. Therefore the exact symbol syntax for the locked 2026 contracts remains:

```text
NOT_PUBLICLY_MACHINE_LOCKED
```

This is acceptable for a candidate provider evaluation. It is not enough for a market-row intake gate.

## Daily Close Semantics Proof

Public Norgate docs do lock one useful semantic:

```text
CLOSE_IS_OFFICIAL_SETTLEMENT_UNLESS_OTHERWISE_SPECIFIED
```

This is source-useful, but it differs from the previous NinjaTrader pilot's `Last` bar surface. Therefore any future Norgate path must be labeled as:

```text
NORGATE_DAILY_SETTLEMENT_CLOSE_PATH
NOT_NINJATRADER_LAST_BAR_PATH
NOT_EXCHANGE_SESSION_TIMESTAMP_LOCK
```

This supports a daily futures research path, but it does not directly continue the exact NinjaTrader `1 Day Last` semantics without a separate date/close policy decision.

## Decision

Decision:

```text
NORGATE_EXACT_16_SYMBOL_PUBLIC_SUPPORT_PROOF_FAIL_CLOSED
```

Reasons:

1. Public Norgate documentation visibly supports 15 of the 16 locked root symbols.
2. `QM` is not publicly proven; `CL` appears, but `CL` may not substitute for `QM`.
3. Exact individual dated-contract syntax for all 16 target contracts is not publicly machine-locked.
4. The contract-detail spreadsheet appears to require subscriber/free-trial login, which is outside this process-only public proof gate.
5. Norgate daily close semantics are settlement-close oriented and must be separately labeled before any Carver market-row use.

Norgate remains:

```text
STRONG_BACKUP_PROVIDER_CANDIDATE_FOR_LOCAL_PROGRAMMATIC_DAILY_FUTURES_HISTORY
```

Norgate does not yet become:

```text
AUTHORIZED_16_SYMBOL_INTAKE_SOURCE
AUTHORIZED_PURCHASE_OR_INSTALLATION_TARGET
AUTHORIZED_MARKET_ROW_SOURCE
```

## Next Clean Options

Option A:

```text
NORGATE_VENDOR_PRE_SALES_CONFIRMATION_GATE
```

Ask Norgate support, without sending or requesting market data, to confirm:

- whether `QM` / E-mini Crude Oil individual contracts are included;
- exact individual contract symbol syntax for all 16 target contracts;
- whether `JUN26` / `JUL26` target contracts would be available after subscription/trial;
- whether daily close is official settlement for all 16 rows unless otherwise specified;
- whether Python access can query individual contract rows and metadata locally on Windows.

Option B:

```text
NORGATE_FREE_TRIAL_OR_PURCHASE_INSTALLATION_GATE
```

Only after operator authorization. This would allow login/installer/client access and static metadata inspection first, then still require a later market-row intake gate.

This option is not recommended until `QM` is confirmed, because a purchase/trial could still fail the exact 16-row pilot.

Option C:

```text
BACKUP_PROVIDER_DECISION_GATE
```

Reopen provider selection toward a provider with explicit dated futures API coverage and less ambiguity around `QM`, such as CME DataMine or Barchart OnDemand, while keeping Databento blocked pending auth repair.

## Selected Next Gate

Selected next gate:

```text
CARVER_NORGATE_VENDOR_PRE_SALES_CONFIRMATION_GATE
```

Reason:

The cheapest clean move is not another data-provider implementation. It is one non-data confirmation step that answers the only question that matters before buying or installing anything:

```text
DOES_NORGATE_SUPPORT_THE_EXACT_16_ROW_DATED_CONTRACT_SURFACE_OR_NOT
```

If Norgate confirms `QM` and exact contract syntax, then a later purchase/trial/install static-metadata gate can be opened. If Norgate cannot confirm `QM`, the exact 16-row Norgate path remains fail-closed and the project should use a different provider or separately redecide a smaller pilot.

## Closed Boundaries

Still closed:

```text
subscription purchase
provider login
free-trial registration
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

This decision authorizes no Norgate subscription purchase, no Norgate login, no free-trial registration, no installer download, no provider client execution, no data download, no market-row parsing, no diagnostics, no backtests, no forecasts, no positions, no costs, no carry, no trend, no OOS, no Lockbox, no Forward, no CFD adapter work, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no GitHub staging, no commit, no push, no PR update/opening, and no remote repository operations.
