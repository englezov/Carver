# Carver Source-Native Futures Historical Data-Source Selection Decision

Date: 2026-05-30

Status:

```text
PROCESS_ONLY_CARVER_SOURCE_NATIVE_FUTURES_HISTORICAL_DATA_SOURCE_SELECTION_DECISION_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Evaluate practical source-native futures historical data-source paths for the locked 16-symbol daily intake pilot and select the cleanest next path.

This decision follows:

```text
docs/process/CARVER_16_SYMBOL_NINJATRADER_CHART_SERIES_DOWNLOAD_TEST_FAIL_CLOSED_RESULT_2026-05-30.md
```

This artifact is process-only. It uses read-only inspection of current Carver artifacts and public provider documentation/pricing/API capability pages. It does not download data, access a provider API, parse market rows, run diagnostics, run backtests, compute forecasts, compute positions, compute costs, compute carry, compute trend, access OOS/Lockbox/Forward, use CFD adapters, use old QuantLab active pipelines, tune, deploy, trade, promote, stage Git changes, commit, push, update a PR, or perform remote repository operations.

## Locked Pilot Need

Pilot lane:

```text
SOURCE_NATIVE_FUTURES
```

Locked row set:

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

Locked bar surface:

```text
1 Day
Last or exchange/vendor daily OHLCV equivalent, explicitly labeled
completed trading dates 2026-05-18 through 2026-05-22
dated contracts only
no continuous contracts
no substitutions
no row dropping
no reweighting
quarantine-only output
```

Existing local result:

```text
NINJATRADER_CHART_SERIES_PATH_AVAILABLE_BY_OBSERVATION_FOR_MES_AND_ZN_ONLY
NINJATRADER_CHART_SERIES_PATH_FAIL_CLOSED_FOR_14_OF_16_MANIFEST_ROWS
NO_HELPER_RAW_OUTPUT_FILES_WRITTEN
```

## Public Capability Sources Inspected

Static provider pages inspected:

```text
NinjaTrader Historical Data Manager:
https://ninjatrader.com/support/helpguides/nt7/historical_data_manager.htm

NinjaTrader historical data download:
https://ninjatrader.com/support/helpguides/nt7/download.htm

CME DataMine:
https://www.cmegroup.com/market-data/datamine-historical-data.html

Databento main product page:
https://databento.com/

Databento historical getting-started docs:
https://databento.com/docs/examples/basics-historical/historical-introduction

Databento futures examples:
https://databento.com/docs/examples/futures/futures-introduction/special-conventions-for-futures-on-databento

Databento pricing and credits:
https://databento.com/pricing/
https://databento.com/docs/faqs

Barchart OnDemand getHistory:
https://www.barchart.com/ondemand/api/getHistory

Barchart OnDemand pricing support page:
https://help.barchart.com/support/solutions/articles/252001-api-inquiry-response

Norgate futures package:
https://norgatedata.com/futurespackage.php

Interactive Brokers TWS historical data:
https://interactivebrokers.github.io/tws-api/historical_data.html
https://interactivebrokers.github.io/tws-api/historical_bars.html

Polygon futures:
https://polygon.io/futures
https://polygon.io/docs/rest/futures/overview/
```

No provider login, provider API call, data download, or market-row inspection was performed.

## Options

### Option A: Keep NinjaTrader Desktop As Primary Batch Loader

Disposition:

```text
NOT_SELECTED_AS_PRIMARY
```

Reason:

NinjaTrader remains useful as local source-native evidence and as a small quarantine proof path. The Historical Data Manager and chart/AddDataSeries routes can load historical data supplied by the configured provider or local cache. However, the current 16-symbol batch attempt failed closed with no helper raw output and only `MES` / `ZN` absent from the missing-date failure list.

NinjaTrader Desktop is therefore too UI/cache/provider-state dependent to be the primary manifest-scale research loader. It remains useful as:

```text
SECONDARY_LOCAL_SANITY_SOURCE
STATIC_INSTRUMENT_IDENTITY_SOURCE
MES_ZN_CACHE_PROVEN_QUARANTINE_PATH
```

### Option B: CME DataMine

Disposition:

```text
NOT_SELECTED_FOR_TINY_NEXT_GATE
```

Reason:

CME DataMine is the most official CME Group historical data source and supports historical futures and options datasets, including settlements, with delivery options such as Data API, SFTP, S3, file browser, and custom select. It is excellent as long-term source authority or official settlement source.

It is not selected for the immediate tiny 16-symbol pilot because the ordering/licensing workflow is heavier than needed for a five-day quarantine mechanics test.

### Option C: Barchart OnDemand

Disposition:

```text
NOT_SELECTED_FOR_TINY_NEXT_GATE
```

Reason:

Barchart OnDemand `getHistory` supports historical time-series data, including futures, and supports end-of-day data. It is a credible commercial API path. Public support material indicates API pricing starts at a high monthly commercial tier, which is too heavy for this immediate pilot unless the operator already has access.

### Option D: Databento Historical

Disposition:

```text
SELECTED_PRIMARY_NEXT_CANDIDATE
```

Reason:

Databento is the cleanest next candidate for this specific problem:

- public docs show historical and live services separated;
- futures coverage includes CME, CBOT, NYMEX, and COMEX;
- the CME Globex MDP 3.0 dataset is documented as `GLBX.MDP3`;
- daily futures OHLCV is available through the `ohlcv-1d` schema in public examples;
- `statistics` is documented as a way to get official daily settlement prices and trade volumes;
- instrument definitions/reference data are available, which can help keep dated-contract identity explicit;
- historical access can be through API or batch/file delivery;
- public pricing is usage-based and new accounts receive historical data credits, which is proportionate to a tiny 16-contract, five-day pilot.

This option best separates:

```text
DATA_SOURCE_RETRIEVAL
CARVER_QUARANTINE_PARSER
GOVERNANCE_BOUNDARY
```

It also avoids relying on NinjaTrader chart cache state as the proof of whether a row exists.

### Option E: Norgate Data Futures Package

Disposition:

```text
NOT_SELECTED_FOR_TINY_NEXT_GATE_BUT_KEEP_AS_LONG_HISTORY_CANDIDATE
```

Reason:

Norgate offers a futures package with long-history daily data, individual futures contracts, continuous contracts, and explicit settlement-close notes. It may be attractive later for broad daily research and complete portfolio reconstruction.

It is not selected for this immediate pilot because the next gate needs a narrow API/file request for exact dated contracts and a five-day quarantine surface. Norgate should remain a candidate for a later long-history daily futures data chapter.

### Option F: Interactive Brokers Historical API

Disposition:

```text
NOT_SELECTED_AS_PRIMARY_RESEARCH_DATA_SOURCE
```

Reason:

Interactive Brokers provides historical bar data through TWS/API, but official documentation states that API historical data has market-data subscription requirements and shares availability behavior with TWS charts. Official docs also note futures daily bars may use settlement prices when available. This keeps IBKR closer to a broker/TWS operational path than a clean batch research data source.

IBKR may be useful later for broker reconciliation, but it should not be the first primary historical data source for this Carver research workspace.

### Option G: Polygon Futures

Disposition:

```text
NOT_SELECTED_BETA_COMING_SOON
```

Reason:

Polygon's futures page advertises futures historical and reference capabilities, but the REST futures overview states futures REST access is in beta and coming soon. That makes it unsuitable as the immediate next path.

### Option H: Local Reproducible CSV Intake

Disposition:

```text
SELECTED_AS_COMMON_QUARANTINE_FORMAT_NOT_AS_SOURCE_BY_ITSELF
```

Reason:

Local CSV is the right Carver intake surface after provider retrieval. It is not a source authority by itself. The next data gate should require provider provenance plus hash-bound raw provider output, then normalize into the existing quarantine OHLCV schema.

## Decision

Selected next path:

```text
DATABENTO_HISTORICAL_DAILY_FUTURES_OHLCV_CANDIDATE_FOR_16_SYMBOL_QUARANTINE_PILOT
```

Supporting path:

```text
LOCAL_REPRODUCIBLE_CSV_QUARANTINE_INTAKE_FORMAT
```

Preserved secondary path:

```text
NINJATRADER_DESKTOP_SECONDARY_SANITY_AND_STATIC_IDENTITY_SOURCE
```

Not selected as primary next path:

```text
NINJATRADER_DESKTOP_BATCH_LOADER
CME_DATAMINE_FOR_TINY_MECHANICS_TEST
BARCHART_ONDEMAND_FOR_TINY_MECHANICS_TEST
IBKR_TWS_API_FOR_PRIMARY_RESEARCH_DATA
POLYGON_FUTURES_BETA_COMING_SOON
NORGATE_FOR_TINY_EXACT_DATED_CONTRACT_TEST
```

## Required Next Gate

Next clean gate:

```text
CARVER_DATABENTO_16_SYMBOL_DAILY_FUTURES_QUARANTINE_INTAKE_SHAPE_GATE
```

That gate should define, before any provider API access or data download:

- exact Databento dataset candidate, expected initially `GLBX.MDP3`;
- exact schema candidate, expected initially `ohlcv-1d`;
- whether `statistics` is needed separately for settlement comparison or official settlement close labeling;
- exact symbol mapping from the Carver locked dated contracts to Databento symbology or instrument IDs;
- exact date/time request window needed to cover completed trading dates `2026-05-18` through `2026-05-22`;
- exact raw-output quarantine path;
- raw provider-output preservation policy;
- sanitized OHLCV schema;
- provider timestamp interpretation;
- completed trading-date derivation;
- all-or-nothing versus row-level fail-closed semantics;
- no continuous-contract fallback;
- no NinjaTrader substitution;
- no diagnostics, backtests, forecasts, positions, costs, carry, trend, OOS/Lockbox/Forward, deployment, trading, or promotion.

The shape gate should still not access Databento, create an account token, call an API, download data, or parse market rows. A later separately authorized execution gate must do that.

## Closed Boundaries

Still closed:

```text
data download
provider API access
provider credentials
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
GitHub staging
commit
push
PR update/opening
remote repository operations
```

## Non-Authorization

This decision authorizes no provider account creation, no provider login, no provider API key use, no provider API call, no data download, no market-row parsing, no diagnostics, no backtests, no forecasts, no positions, no costs, no carry, no trend, no OOS, no Lockbox, no Forward, no CFD adapter work, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no GitHub staging, no commit, no push, no PR update/opening, and no remote repository operations.
