# Carver Databento Provider-Condition Metadata Readiness Gate Draft

Date: 2026-05-30

Status:

```text
PROCESS_ONLY_CARVER_DATABENTO_PROVIDER_CONDITION_METADATA_READINESS_GATE_DRAFT_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Define the gate required before the Databento 16-symbol dated-contract full-history daily OHLCV quarantine archive can become strategy-facing readiness input.

The current archive passed quarantine row-shape validation, but Databento emitted reduced-quality provider-condition warnings during the full-history per-symbol requests. Those warnings must be preserved as explicit date/row readiness metadata before any diagnostics, backtests, forecasts, positions, costs, carry, trend, or strategy use.

## Current Upstream Evidence

Archive pass record:

```text
docs/process/CARVER_DATABENTO_16_SYMBOL_DATED_CONTRACT_FULL_HISTORY_QUARANTINE_ARCHIVE_PASS_2026-05-30.md
```

Archive root:

```text
docs/researchops/source_native_futures_daily_data_library/16_SYMBOL_FULL_DAILY_HISTORY/raw_provider_archive/DATABENTO/20260530_DATED_CONTRACT_FULL_AVAILABLE_HISTORY_PER_SYMBOL_CURRENT_IDS
```

Archive status:

```text
PASS_WITH_PROVIDER_CONDITION_WARNINGS_16_SYMBOL_DATED_CONTRACT_PER_SYMBOL_CURRENT_ID_FULL_HISTORY_QUARANTINE_ONLY
```

Known archive facts:

```text
SYMBOLS_EXPECTED: 16
SYMBOLS_WITH_RAW_FILES: 16
ACCEPTED_MARKET_ROWS: 4568
DUPLICATE_DATES_TOTAL: 0
ALL_16_SYMBOLS_HAVE_ROWS: YES
PROVIDER_CONDITION_WARNINGS_OBSERVED: YES_REDUCED_QUALITY_WARNINGS_PRINTED_DURING_REQUESTS
```

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
```

## Required Rule

No market row may become strategy-facing unless provider condition is known, recorded, and accepted under a documented policy.

The condition ledger must distinguish:

```text
PROVIDER_CONDITION_NORMAL
PROVIDER_CONDITION_REVIEWED_NOT_APPLICABLE_TO_OHLCV_1D
PROVIDER_CONDITION_DEGRADED_QUARANTINE
PROVIDER_CONDITION_BLOCKED_UNUSABLE
PROVIDER_CONDITION_UNRESOLVED_FAIL_CLOSED
```

## Required Evidence

A later execution gate must use Databento official metadata only to obtain dataset-condition evidence for `GLBX.MDP3` across the archive date range represented by the 4,568-row quarantine archive.

The evidence must preserve:

- provider metadata endpoint or client method used;
- dataset;
- condition date range queried;
- returned condition status per date or interval;
- whether the condition applies globally, by schema, by venue/feed, or by other provider-defined scope;
- whether `ohlcv-1d` is affected, unaffected, or unresolved;
- raw provider condition metadata preserved without silent rewriting;
- hash/provenance for all condition metadata artifacts.

## Required Join

The execution gate must join provider-condition evidence onto the existing sanitized archive by completed trading date and, where provider evidence supports it, by symbol/instrument/scope.

Expected row-level fields:

```text
provider
dataset
schema
provider_symbol
locked_raw_symbol
instrument_id
completed_trading_date
timestamp_utc
provider_condition_source
provider_condition_raw_status
provider_condition_scope
provider_condition_applies_to_ohlcv_1d
provider_condition_readiness_status
strategy_facing_readiness_status
condition_review_notes
```

The original raw provider output and accepted sanitized archive must remain unchanged. The provider-condition ledger is a new overlay/readiness artifact.

## Classification Policy

Default policy:

```text
NORMAL provider condition -> ROW_READY_PROVIDER_CONDITION_NORMAL
warning reviewed and irrelevant to ohlcv-1d -> ROW_READY_PROVIDER_CONDITION_REVIEWED_NOT_APPLICABLE
warning possibly relevant but not fatal -> ROW_QUARANTINED_PROVIDER_CONDITION_DEGRADED
warning relevant and unsafe -> ROW_BLOCKED_PROVIDER_CONDITION_UNUSABLE
missing or ambiguous condition metadata -> ROW_BLOCKED_PROVIDER_CONDITION_UNRESOLVED
```

Any unresolved provider condition must fail closed for strategy-facing use.

## Required Outputs

Expected execution artifacts:

```text
raw_provider_metadata/DATABENTO_GLBX_MDP3_DATASET_CONDITION_RAW_*.json
provider_condition_ledger/DATABENTO_16_SYMBOL_DATED_CONTRACT_PROVIDER_CONDITION_LEDGER.csv
provider_condition_ledger/DATABENTO_16_SYMBOL_DATED_CONTRACT_PROVIDER_CONDITION_ROW_JOIN.csv
validation/DATABENTO_PROVIDER_CONDITION_READINESS_VALIDATION.csv
provenance/DATABENTO_PROVIDER_CONDITION_METADATA_PROVENANCE.md
provenance/DATABENTO_PROVIDER_CONDITION_METADATA_STATUS.csv
provenance/DATABENTO_PROVIDER_CONDITION_METADATA_SHA256SUMS.txt
```

## Pass Criteria

The gate may pass only if:

- official Databento condition metadata is preserved;
- every archive row receives exactly one provider-condition readiness status;
- every degraded/warning date is either reviewed as not applicable, quarantined, blocked, or unresolved fail-closed;
- no row with unresolved provider condition is marked strategy-facing ready;
- raw archive rows are not modified;
- no diagnostics, backtests, forecasts, positions, costs, carry, trend, or risk calculations are performed.

Expected pass disposition:

```text
PASS_DATABENTO_PROVIDER_CONDITION_METADATA_ROW_READINESS_SCOPE
```

## Fail-Closed Conditions

The gate must fail closed if:

- Databento condition metadata cannot be obtained;
- condition metadata exists but cannot be mapped to archive dates;
- provider condition scope cannot be interpreted for `ohlcv-1d`;
- any archive row receives multiple conflicting condition statuses;
- any unresolved condition is silently accepted;
- any artifact mutates the raw provider output or accepted sanitized archive.

Expected fail disposition:

```text
FAIL_CLOSED_DATABENTO_PROVIDER_CONDITION_METADATA_UNRESOLVED
```

## What Remains Closed

Still closed:

```text
new OHLCV data download
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

## Non-Authorization

This draft authorizes no provider API access, no new data download, no market-row parsing beyond future explicitly authorized provider-condition joining, no diagnostics, no backtests, no forecasts, no positions, no costs, no carry, no trend, no volatility/risk calculations, no OOS, no Lockbox, no Forward, no deployment, no trading, and no promotion.
