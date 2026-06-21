# Carver 16-Symbol Provider-Condition Policy Decision

Date: 2026-05-30

Status:

```text
PROCESS_ONLY_CARVER_16_SYMBOL_PROVIDER_CONDITION_POLICY_DECISION_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Decide how Databento `GLBX.MDP3` provider-condition metadata affects the 16-symbol source-native daily data library promotion-readiness chapter.

This is a process-only policy decision over already downloaded quarantine artifacts and already fetched provider-condition metadata. It does not request new data, run diagnostics, run backtests, compute forecasts, compute positions, compute costs, compute carry, compute trend, compute volatility/risk, deploy, trade, or promote.

## Inputs

Full-history archive pass:

```text
docs/process/CARVER_DATABENTO_16_SYMBOL_DATED_CONTRACT_FULL_HISTORY_QUARANTINE_ARCHIVE_PASS_2026-05-30.md
```

Provider-condition metadata execution:

```text
docs/process/CARVER_DATABENTO_PROVIDER_CONDITION_METADATA_READINESS_EXECUTION_PASS_2026-05-30.md
```

Provider-condition row join:

```text
docs/researchops/source_native_futures_daily_data_library/16_SYMBOL_FULL_DAILY_HISTORY/raw_provider_archive/DATABENTO/20260530_DATED_CONTRACT_FULL_AVAILABLE_HISTORY_PER_SYMBOL_CURRENT_IDS/provider_condition_metadata_2026-05-30/provider_condition_ledger/DATABENTO_16_SYMBOL_DATED_CONTRACT_PROVIDER_CONDITION_ROW_JOIN.csv
```

## Evidence Summary

The archive contains:

```text
ARCHIVE_ROWS: 4568
SYMBOLS: 16
DATASET: GLBX.MDP3
SCHEMA: ohlcv-1d
```

The provider-condition overlay joined every archive row:

```text
ROWS_JOINED: 4568
ROW_READY_PROVIDER_CONDITION_NORMAL: 4483
ROW_QUARANTINED_PROVIDER_CONDITION_DEGRADED: 85
ROW_BLOCKED_OR_UNRESOLVED_PROVIDER_CONDITION: 0
```

Degraded dates:

```text
2025-09-17
2025-09-24
2025-11-28
2026-03-15
2026-03-16
2026-04-10
2026-05-24
```

## Decision

Provider-condition policy:

```text
NORMAL_PROVIDER_CONDITION_ROWS: ELIGIBLE_FOR_PROMOTION_READINESS_CANDIDATE_SET
DEGRADED_PROVIDER_CONDITION_ROWS: EXCLUDE_FROM_STRATEGY_FACING_CANDIDATE_SET_KEEP_QUARANTINED
BLOCKED_OR_UNRESOLVED_PROVIDER_CONDITION_ROWS: EXCLUDE_FAIL_CLOSED
```

The 85 degraded rows remain preserved in the raw and sanitized quarantine archive with their labels. They are not deleted, repaired, imputed, overwritten, smoothed, substituted, or silently accepted.

The 4,483 normal provider-condition rows may be listed in the canonical manifest as promotion-readiness candidates only. They are not yet strategy data and may not be consumed by diagnostics, backtests, forecasts, positions, costs, carry, trend, volatility/risk calculations, OOS, Lockbox, Forward, deployment, trading, or promotion.

## Rationale

The Databento condition metadata is dataset-level evidence and does not prove row-specific OHLCV corruption. But without official schema-specific proof that the degraded condition is irrelevant to `ohlcv-1d`, the conservative source-native policy is to exclude degraded dates from the strategy-facing candidate set and preserve the labels for audit.

This chooses data-label fidelity over convenience. The library can later loosen this policy only through a separate evidence gate, such as a Databento support clarification or official metadata documentation proving the condition does not affect daily OHLCV.

## Promotion-Readiness Consequence

The canonical manifest must encode:

```text
archive row count
normal candidate row count
degraded quarantined row count
excluded completed trading dates
raw/provider/definition/condition hashes
no diagnostics/backtests/forecasts/positions status
```

The future promotion shape may admit only rows whose provider-condition readiness status is:

```text
ROW_READY_PROVIDER_CONDITION_NORMAL
```

Rows whose provider-condition readiness status is:

```text
ROW_QUARANTINED_PROVIDER_CONDITION_DEGRADED
```

must remain excluded until a separate provider-condition relaxation gate is authorized and passes.

## Non-Authorization

This decision authorizes no provider API access, no new market-data request, no market-row parsing, no diagnostics, no backtests, no forecasts, no positions, no costs, no carry, no trend, no volatility/risk calculations, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.
