# Carver Daily Data Foundation Completion Criteria And Evidence Matrix

Date: 2026-05-30

Status:

```text
PROCESS_ONLY_CARVER_DAILY_DATA_FOUNDATION_COMPLETION_CRITERIA_AND_EVIDENCE_MATRIX_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Define the concrete evidence required before the active Carver source-native daily data foundation goal can be marked complete.

This artifact does not execute any gate. It does not parse market rows, create the dated-contract fragment table, inspect provider accounts, download data, build continuous series, create strategy input, run diagnostics, run backtests, compute forecasts, compute positions, compute costs, compute carry, compute trend, compute volatility/risk, access OOS/Lockbox/Forward, deploy, trade, promote, stage Git changes, commit, push, update a PR, or perform remote operations.

## Active Goal Boundary

The active goal is:

```text
Build the Carver source-native daily data foundation for first strategy machinery, starting with a tightly fenced 16-symbol dated-contract fragment Development/Reconciliation table shape gate for plumbing only, then requiring a source-native continuous/roll daily data semantics shape gate before any broad Carver strategy machinery, while keeping provider access, new downloads, market-row parsing, diagnostics, backtests, forecasts, positions, costs, carry, trend, volatility/risk calculations, OOS/Lockbox/Forward, CFD adapters, old QuantLab active-pipeline use, tuning, deployment, trading, promotion, and Git operations closed unless separately authorized.
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Current Proven State

The current worktree proves the following process/readiness items exist:

| Requirement | Current evidence | Completion status |
|---|---|---|
| Source-native futures lane and clean workspace governance are established. | `README.md`; `docs/mission/CARVER_SOURCE_NATIVE_RESEARCH_CHARTER_2026-05-28.md`; `docs/process/LANE_CLASSIFICATION_AND_ADAPTER_QUARANTINE_RULES_2026-05-28.md` | PROVEN |
| Old QuantLab active-pipeline reuse remains closed. | `docs/process/CLEAN_WORKSPACE_MIGRATION_RECORD_2026-05-28.md` | PROVEN |
| The 16-symbol Databento dated-contract quarantine archive exists as prior audited state. | `docs/process/CARVER_DAILY_DATA_FOUNDATION_CURRENT_STATE_AND_AUTHORIZATION_QUEUE_2026-05-30.md` records 4,568 quarantined archive rows, 4,483 normal rows, 85 degraded rows, and non-strategy schema/date join smoke-test pass. | PROVEN AS PROCESS-CARRIED STATE |
| Dated-contract fragment table shape is defined as plumbing-only. | `docs/process/CARVER_16_SYMBOL_DATED_CONTRACT_FRAGMENT_DEV_RECON_TABLE_SHAPE_GATE_2026-05-30.md` | PROVEN |
| Continuous/roll semantics shape is defined before broad strategy machinery. | `docs/process/CARVER_SOURCE_NATIVE_CONTINUOUS_ROLL_DAILY_DATA_SEMANTICS_SHAPE_GATE_2026-05-30.md` | PROVEN |
| Continuous/roll evidence needs are identified. | `docs/process/CARVER_SOURCE_NATIVE_CONTINUOUS_ROLL_DAILY_DATA_SEMANTICS_EVIDENCE_PACKET_2026-05-30.md` | PROVEN |
| Future execution gate drafts exist for the plumbing table and continuous/roll evidence. | `docs/process/CARVER_16_SYMBOL_DATED_CONTRACT_FRAGMENT_DEV_RECON_TABLE_EXECUTION_GATE_DRAFT_2026-05-30.md`; `docs/process/CARVER_SOURCE_NATIVE_CONTINUOUS_ROLL_DAILY_DATA_SEMANTICS_EVIDENCE_EXECUTION_GATE_DRAFT_2026-05-30.md` | PROVEN |
| Automatic lean hostile audits have been preserved for the process-only shape, handoff, evidence packet, execution drafts, and queue. | `docs/process/CARVER_DAILY_DATA_FOUNDATION_SHAPE_GATES_LEAN_HOSTILE_AUDIT_RESULT_2026-05-30.md`; `docs/process/CARVER_DAILY_DATA_FOUNDATION_NEXT_STEP_HANDOFF_LEAN_HOSTILE_AUDIT_RESULT_2026-05-30.md`; `docs/process/CARVER_SOURCE_NATIVE_CONTINUOUS_ROLL_DAILY_DATA_SEMANTICS_EVIDENCE_PACKET_LEAN_HOSTILE_AUDIT_RESULT_2026-05-30.md`; `docs/process/CARVER_DAILY_DATA_FOUNDATION_EXECUTION_GATE_DRAFTS_LEAN_HOSTILE_AUDIT_RESULT_2026-05-30.md`; `docs/process/CARVER_DAILY_DATA_FOUNDATION_CURRENT_STATE_AND_AUTHORIZATION_QUEUE_LEAN_HOSTILE_AUDIT_RESULT_2026-05-30.md` | PROVEN |

## Missing Evidence Before Goal Completion

The broad goal is not complete. The following evidence is still missing:

| Missing item | Required evidence to prove completion | Current status |
|---|---|---|
| Dated-contract fragment Development/Reconciliation table execution. | Four output artifacts under `docs/researchops/source_native_futures_daily_data_library/16_SYMBOL_DATED_CONTRACT_FRAGMENT_DEV_RECON_TABLE/2026-05-30/`: table CSV, status CSV, provenance MD, SHA256SUMS. | MISSING; separate execution gate required |
| Admission of exactly 4,483 normal provider-condition rows and exclusion of exactly 85 degraded rows. | Executed table/status artifacts proving counts, hash lineage, no non-manifest rows, no continuous rows, no duplicate `(provider_symbol, completed_trading_date)` keys, and `NOT_STRATEGY_INPUT_NOT_BACKTEST_READY` labels. | MISSING; separate execution gate required |
| Automatic lean hostile audit of the executed dated-contract fragment table. | Audit record covering row counts, hash lineage, dated-contract-only labeling, no strategy input, no diagnostics/backtests/forecasts/positions/costs/carry/trend/risk, no provider access, no new download, and no Git/remote operations. | MISSING; requires table execution first |
| Continuous/roll daily data semantics evidence execution. | Evidence source index, 16-symbol evidence requirement ledger, provider capability status ledger, lifecycle evidence needs ledger, and SHA256SUMS under `docs/researchops/source_native_futures_daily_data_library/continuous_roll_semantics_evidence/2026-05-30/`. | MISSING; separate process/source execution gate required |
| Automatic lean hostile audit of the continuous/roll evidence execution. | Audit record proving static source boundaries, no provider API/login, no market data download, no market-row parsing, no continuous-series construction, and no strategy input. | MISSING; requires evidence execution first |
| Continuous/roll daily data policy decision. | A later decision artifact choosing whether provider-built continuous series are reference-only, source authority after lineage proof, locally built from dated contracts, blocked pending settlement/close evidence, or blocked entirely. | MISSING; requires evidence execution first |
| Strategy-facing daily data readiness. | A later separately authorized gate after continuous/roll policy decision. | BLOCKED |

## Completion Evidence Matrix

The active goal can be marked complete only when each row below is proven by current artifacts.

| Completion criterion | Required proof | Accepted status |
|---|---|---|
| The 16-symbol dated-contract fragment table exists for plumbing only. | Executed table, status, provenance, and SHA artifacts at the locked output root. | REQUIRED |
| The fragment table excludes degraded provider-condition rows. | Status/provenance records exactly 4,483 admitted normal rows and exactly 85 excluded degraded rows, or fails closed with a replacement hash-bound count authority separately authorized before execution. | REQUIRED |
| The fragment table cannot be mistaken for strategy input. | Every row or status artifact includes `DATED_CONTRACT_FRAGMENT_TABLE_FOR_PLUMBING_ONLY` and `NOT_STRATEGY_INPUT_NOT_BACKTEST_READY`. | REQUIRED |
| No provider access or new data request occurred during fragment table execution. | Status and audit record `provider_api_access: NO` and `new_data_download: NO`. | REQUIRED |
| Continuous/roll source and provider semantics evidence has been executed. | Evidence source index and 16-symbol ledgers exist at the locked continuous/roll evidence root. | REQUIRED |
| Continuous/roll evidence does not construct strategy input. | Ledgers default every symbol/family to `STRATEGY_USE_STATUS: BLOCKED_PENDING_CONTINUOUS_ROLL_POLICY` or stricter. | REQUIRED |
| The next policy decision is explicit. | A source-native continuous/roll daily data policy decision artifact exists after evidence execution. | REQUIRED |
| Audits are preserved automatically. | Lean hostile audit records exist for the executed fragment table and continuous/roll evidence execution. | REQUIRED |
| Prohibited work remains closed. | Current status/audit records preserve no diagnostics, no backtests, no forecasts, no positions, no costs, no carry, no trend, no volatility/risk calculations, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git operations, and no remote operations. Future gates must carry their own separate authorization and non-authorization boundary. | REQUIRED |

## Current Completion Decision

Current broad-goal completion state:

```text
NOT_COMPLETE
```

Reason:

```text
The table shape, continuous/roll shape, evidence packet, gate drafts, authorization queue, and automatic audits are present, but the dated-contract fragment table execution and continuous/roll evidence execution have not been separately authorized or performed.
```

Next required gate:

```text
CARVER_16_SYMBOL_DATED_CONTRACT_FRAGMENT_DEV_RECON_TABLE_EXECUTION_GATE
```

Next required semantic gate:

```text
CARVER_SOURCE_NATIVE_CONTINUOUS_ROLL_DAILY_DATA_SEMANTICS_EVIDENCE_EXECUTION_GATE
```

## Non-Authorization

This matrix authorizes no provider API access, no provider login, no new market-data request, no data download, no market-row parsing, no table execution, no raw or sanitized archive modification, no continuous-contract download, no continuous-series construction, no diagnostics, no backtests, no forecasts, no positions, no costs, no carry, no trend, no volatility/risk calculations, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.
