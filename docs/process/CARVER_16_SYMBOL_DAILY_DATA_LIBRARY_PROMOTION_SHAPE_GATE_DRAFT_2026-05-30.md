# Carver 16-Symbol Daily Data Library Promotion Shape Gate Draft

Date: 2026-05-30

Status:

```text
PROCESS_ONLY_CARVER_16_SYMBOL_DAILY_DATA_LIBRARY_PROMOTION_SHAPE_GATE_DRAFT_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Define the shape for moving the completed 16-symbol Databento daily archive from quarantine toward a source-native Development/Reconciliation data library candidate.

This draft does not perform the promotion. It defines the future admissibility contract and keeps diagnostics, backtests, forecasts, positions, costs, carry, trend, volatility/risk calculations, OOS, Lockbox, Forward, deployment, trading, and production promotion closed.

## Scope

Universe:

```text
ZT, ZF, ZN, MES, MNQ, M2K, MYM, QM, RB, ZC, ZS, ZM, ZL, ZW, HE, LE
```

Archive provider:

```text
provider: Databento Historical
dataset: GLBX.MDP3
schema: ohlcv-1d
request identity: exact 2026-current instrument_id per dated contract
continuous contracts: CLOSED
```

Canonical manifest:

```text
docs/researchops/source_native_futures_daily_data_library/16_SYMBOL_DAILY_LIBRARY_PROMOTION_READINESS/manifest/CARVER_16_SYMBOL_DATABENTO_DAILY_LIBRARY_CANONICAL_MANIFEST_2026-05-30.csv
SHA256: 0D1F86071A536227BB120163E8166BA13DE7F4C47345AE3CA1DF99F1B3DF0E88
```

## Promotion-Readiness Inputs

The future promotion execution gate must use only these already-created artifact classes unless separately authorized:

- static dated-contract selection ledger;
- Databento full-history raw provider archive;
- Databento definition metadata files;
- sanitized quarantine OHLCV file;
- full-history validation ledger;
- provider-condition metadata row join;
- canonical promotion-readiness manifest;
- provenance and SHA256 records.

No provider API call, new OHLCV request, continuous-contract request, or symbol/date expansion is opened by this draft.

## Admissible Row Rule

The future strategy-facing candidate table may include only archive rows satisfying all of:

```text
provider == DATABENTO
dataset == GLBX.MDP3
schema == ohlcv-1d
stype_in == instrument_id
quarantine_status == QUARANTINE_ONLY_NOT_DIAGNOSTIC_NOT_BACKTEST
provider_condition_readiness_status == ROW_READY_PROVIDER_CONDITION_NORMAL
validation_status == PASS_PER_SYMBOL_CURRENT_ID_FULL_AVAILABLE_ROWS_PRESENT_NO_DUPLICATES
timestamp_policy == PASS_ALL_UTC_MIDNIGHT
symbol_roundtrip == PASS_RAW_SYMBOL_AND_INSTRUMENT_ID_MATCH
```

Rows with any of the following are excluded:

```text
ROW_QUARANTINED_PROVIDER_CONDITION_DEGRADED
missing provider-condition metadata
blocked provider-condition metadata
unresolved provider-condition metadata
duplicate symbol/date
timestamp policy failure
symbol/instrument mismatch
continuous-contract identity
non-manifest symbol
non-ohlcv-1d schema
```

## Current Candidate Counts

Current manifest totals:

```text
MANIFEST_ROWS: 16
ARCHIVE_ROWS: 4568
NORMAL_PROVIDER_CONDITION_CANDIDATE_ROWS: 4483
DEGRADED_QUARANTINED_ROWS: 85
OTHER_BLOCKED_OR_UNRESOLVED_ROWS: 0
```

The 4,483 normal rows are promotion-readiness candidates only. They are not evidence of performance, alpha, tradability, costs, risk, strategy quality, or production readiness.

## Strategy-Facing Table Contract

A later promotion execution may create a strategy-facing Development/Reconciliation candidate table only if it:

- uses the canonical manifest as the source of allowed rows;
- excludes all degraded rows by completed trading date and symbol;
- preserves the raw Databento timestamp and completed trading date;
- preserves `provider_symbol`, `locked_raw_symbol`, and `instrument_id`;
- preserves provenance hashes back to raw provider output;
- preserves the exact policy label that degraded rows were excluded;
- names the output as Development/Reconciliation candidate data only;
- records that diagnostics/backtests/forecasts/positions/costs/carry/trend/risk remain closed.

Minimum allowed schema:

```text
provider
dataset
schema
provider_symbol
locked_raw_symbol
instrument_id
timestamp_utc
completed_trading_date
open
high
low
close
volume
provider_condition_readiness_status
source_archive_sha256
condition_join_sha256
promotion_policy_status
```

## Required Validation Before Any Future Promotion Execution

A later promotion execution must prove:

- all 16 manifest rows are present;
- no non-manifest symbols are included;
- all degraded rows are excluded;
- row counts match the canonical manifest normal-row counts;
- per-symbol dates are strictly increasing;
- no duplicate `(provider_symbol, completed_trading_date)` pairs exist;
- every row has a matching condition row;
- every row has a hash lineage to the raw archive and provider-condition join;
- no diagnostics/backtests/forecasts/positions/costs/carry/trend/risk are computed.

## Audit Requirements

Lean hostile audit is automatic for the promotion-shape chapter.

Opus audit is recommended before any broader use of this library as multi-strategy or portfolio Development/Reconciliation input, especially if the operator considers admitting degraded provider-condition rows or broadening beyond the 16 dated-contract pilot.

## Non-Authorization

This draft authorizes no provider API access, no new market-data request, no market-row parsing, no diagnostics, no backtests, no forecasts, no positions, no costs, no carry, no trend, no volatility/risk calculations, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.
