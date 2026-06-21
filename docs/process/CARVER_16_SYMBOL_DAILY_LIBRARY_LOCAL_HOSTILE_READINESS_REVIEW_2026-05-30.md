# Carver 16-Symbol Daily Library Local Hostile Readiness Review

Date: 2026-05-30

Status:

```text
PROCESS_ONLY_CARVER_16_SYMBOL_DAILY_LIBRARY_LOCAL_HOSTILE_READINESS_REVIEW_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Perform a local hostile readiness review after the completed 16-symbol Databento quarantine archive, provider-condition overlay, promotion-readiness manifest, and non-strategy schema/date join smoke test.

This review decides whether the current 16-symbol daily data library is ready to become Development/Reconciliation input, or whether continuous/roll semantics must be shaped first.

## Reviewed Evidence

Primary process records:

```text
docs/process/CARVER_16_SYMBOL_DAILY_INTAKE_PILOT_CLOSEOUT_2026-05-30.md
docs/process/CARVER_16_SYMBOL_DAILY_DATA_LIBRARY_PROMOTION_READINESS_CHAPTER_CLOSEOUT_2026-05-30.md
docs/process/CARVER_16_SYMBOL_DAILY_DATA_LIBRARY_PROMOTION_SHAPE_GATE_DRAFT_2026-05-30.md
docs/process/CARVER_16_SYMBOL_DAILY_DATA_LIBRARY_NON_STRATEGY_SMOKE_TEST_EXECUTION_PASS_2026-05-30.md
```

Primary machine-readable records:

```text
docs/researchops/source_native_futures_daily_data_library/16_SYMBOL_DAILY_LIBRARY_PROMOTION_READINESS/manifest/CARVER_16_SYMBOL_DATABENTO_DAILY_LIBRARY_CANONICAL_MANIFEST_2026-05-30.csv
docs/researchops/source_native_futures_daily_data_library/16_SYMBOL_DAILY_LIBRARY_PROMOTION_READINESS/smoke_tests/2026-05-30_schema_date_join/
```

Observed library counts:

```text
MANIFEST_ROWS: 16
ARCHIVE_ROWS: 4568
NORMAL_PROVIDER_CONDITION_CANDIDATE_ROWS: 4483
DEGRADED_QUARANTINED_ROWS: 85
OTHER_BLOCKED_OR_UNRESOLVED_ROWS: 0
SMOKE_TEST_RESULT: PASS_NON_STRATEGY_SCHEMA_DATE_JOIN_SMOKE_TEST
```

## Findings

### Finding 1 - Dated-contract bars are not a general Carver strategy input

Severity:

```text
HIGH
```

The archive contains explicit 2026-current dated contracts, not continuous contracts and not a rolled futures history.

Examples:

```text
ZTM6, ZFM6, ZNM6, MESM6, MNQM6, M2KM6, MYMM6, QMN6, RBN6, ZCN6, ZSN6, ZMN6, ZLN6, ZWN6, HEM6, LEM6
```

The current archive proves the Databento pipe, source-native instrument identity, raw/sanitized preservation, provider-condition joining, and non-strategy date/schema plumbing. It does not yet provide the continuous economic series needed for Carver strategy computation.

Decision impact:

```text
BLOCK_GENERAL_STRATEGY_FACING_PROMOTION
REQUIRE_CONTINUOUS_OR_ROLLED_SERIES_SEMANTICS_BEFORE_CARVER_STRATEGY_MACHINERY
```

### Finding 2 - Per-contract history is too short and uneven for strategy interpretation

Severity:

```text
HIGH
```

The full-history archive is full available history for each current dated contract, not full economic market history.

Recorded row coverage includes:

```text
ZTM6   142 rows  2025-11-05 through 2026-05-29
MESM6  232 rows  2025-04-09 through 2026-05-29
ZCN6   560 rows  2023-05-23 through 2026-05-29
LEM6   353 rows  2025-01-02 through 2026-05-29
```

These windows are useful for pipeline proof and reconciliation, but they are not a uniform historical panel for strategy tests, volatility estimation, trend/carry inputs, or portfolio machinery.

Decision impact:

```text
ALLOW_ONLY_NARROW_PLUMBING_OR_RECONCILIATION_SHAPING
BLOCK_PERFORMANCE_OR_STRATEGY_READINESS_INTERPRETATION
```

### Finding 3 - Provider-condition degraded rows create real holes

Severity:

```text
MEDIUM
```

The provider-condition overlay found:

```text
ROW_READY_PROVIDER_CONDITION_NORMAL: 4483
ROW_QUARANTINED_PROVIDER_CONDITION_DEGRADED: 85
BLOCKED_OR_UNRESOLVED_PROVIDER_CONDITION_ROWS: 0
```

The current policy correctly excludes degraded rows from the candidate set. That exclusion creates explicit date/symbol holes. The holes are acceptable for a quarantine/data-quality chapter and for plumbing checks that preserve the exclusion label. They are not acceptable as silent gaps in any strategy-facing time series.

Decision impact:

```text
PRESERVE_DEGRADED_ROW_EXCLUSION
REQUIRE_GAP_POLICY_BEFORE_STRATEGY_FACING_TABLE
```

### Finding 4 - Timestamp semantics remain provider-daily, not strategy session authority

Severity:

```text
MEDIUM
```

The Databento archive uses `ohlcv-1d` rows with UTC daily timestamps. The smoke test verified schema/date joining and duplicate/missing behavior at the archive level. It did not lock a complete Carver session authority for strategy computation.

For a future strategy-facing table, `completed_trading_date` must remain the primary daily key, and UTC timestamps must be carried as provider timestamps rather than silently interpreted as exchange session-end timestamps.

Decision impact:

```text
REQUIRE_COMPLETED_TRADING_DATE_POLICY_IN_STRATEGY_TABLE_SHAPE
REQUIRE_SESSION_ALIGNMENT_POLICY_BEFORE_STRATEGY_COMPUTATION
```

### Finding 5 - Roll, back-adjustment, settlement, carry-leg, cost, and risk semantics are still closed

Severity:

```text
HIGH
```

The current chapter did not open:

```text
continuous contracts
roll rules
back-adjustment policy
settlement versus close policy
carry curve-leg availability
costs
FX
annual risk
price risk
volatility/risk calculations
trend or carry computation
```

This is correct governance. It also means the archive cannot be treated as ready for the book strategies.

Decision impact:

```text
BLOCK_CARVER_STRATEGY_INPUT
REQUIRE_CONTINUOUS_ROLL_SEMANTICS_AND_DATA_POLICY_GATE
```

### Finding 6 - The non-strategy smoke test passed its actual boundary

Severity:

```text
INFORMATIONAL
```

The smoke test result is clean for what it claimed:

```text
JOINED_ROWS_OBSERVED: 4568
NORMAL_PROVIDER_CONDITION_ROWS_OBSERVED: 4483
DEGRADED_ROWS_EXCLUDED_OBSERVED: 85
DUPLICATE_KEYS_AFTER_EXCLUSION: 0
NON_MANIFEST_SYMBOLS: 0
UNJOINED_ARCHIVE_ROWS: 0
```

This is a strong plumbing result. It is not performance evidence, alpha evidence, or strategy readiness.

### Finding 7 - Source-native and governance boundaries were preserved

Severity:

```text
INFORMATIONAL
```

No reviewed artifact uses CFD assumptions, old QuantLab active-pipeline state, diagnostics, backtests, forecasts, positions, costs, carry, trend, risk calculations, OOS, Lockbox, Forward, deployment, trading, promotion, or Git operations.

## Hostile Review Verdict

For general Carver strategy-facing Development/Reconciliation input:

```text
BLOCKING_FINDINGS: YES
DISPOSITION: BLOCK_GENERAL_STRATEGY_INPUT_PENDING_CONTINUOUS_ROLL_SEMANTICS
```

For narrow non-strategy plumbing or dated-contract reconciliation table shaping:

```text
BLOCKING_FINDINGS: NO
DISPOSITION: PASS_NARROW_DATED_CONTRACT_PLUMBING_RECONCILIATION_SHAPE_ONLY
```

The current library can support tightly labeled source-native dated-contract plumbing/reconciliation work. It must not be silently promoted into Carver strategy machinery.

## Required Next Gates

Immediate permissible next gate:

```text
CARVER_16_SYMBOL_DATED_CONTRACT_FRAGMENT_DEV_RECON_TABLE_SHAPE_GATE
```

That gate may shape a plumbing-only table from existing normal provider-condition rows, provided it labels the table as a dated-contract fragment and forbids strategy interpretation.

Required gate before general Carver strategy machinery:

```text
CARVER_SOURCE_NATIVE_CONTINUOUS_ROLL_DAILY_DATA_SEMANTICS_SHAPE_GATE
```

That gate must decide how Carver will represent continuous/rolled daily futures histories, dated-contract lineage, roll timing, back-adjustment, settlement/close semantics, provider-condition gaps, and completed-bar alignment before any strategy computation.

## Non-Authorization

This review authorizes no provider API access, no new market-data request, no data download, no market-row parsing, no diagnostics, no backtests, no forecasts, no positions, no costs, no carry, no trend, no volatility/risk calculations, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.
