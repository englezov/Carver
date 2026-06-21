# Carver 16-Symbol Daily Intake Pilot Closeout

Date: 2026-05-30

Status:

```text
PROCESS_ONLY_CARVER_16_SYMBOL_DAILY_INTAKE_PILOT_CLOSEOUT_QUARANTINE_ONLY_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Close the 16-symbol daily intake pilot readiness and execution path at quarantine scope.

The 16-symbol set remains the NinjaTrader-supported pilot universe selected from the Appendix C/Jumbo readiness work:

```text
ZT, ZF, ZN, MES, MNQ, M2K, MYM, QM, RB, ZC, ZS, ZM, ZL, ZW, HE, LE
```

The completed execution path uses Databento Historical as the practical source-native archive path after the local NinjaTrader helper/export route failed closed for the full 16-symbol batch. This closeout does not convert the archive into strategy-facing data, diagnostics, backtests, forecasts, positions, costs, carry, trend, risk, or production readiness.

## Governing Origin

The chapter begins from the completed Appendix C to first real-data intake readiness work.

Opus-audited MES tiny intake origin:

```text
docs/process/CARVER_APPENDIX_C_TO_FIRST_REAL_DATA_INTAKE_READINESS_OPUS_AUDIT_RESULT_2026-05-30.md
AUDIT_DISPOSITION: PASS_APPENDIX_C_TO_FIRST_REAL_DATA_INTAKE_READINESS_QUARANTINE_ONLY_SCOPE
```

16-symbol next-step decision:

```text
docs/process/CARVER_16_SYMBOL_NINJATRADER_DAILY_INTAKE_PILOT_NEXT_STEP_DECISION_2026-05-30.md
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Static Dated-Contract Selection

The static dated-contract selection gate selected explicit contracts for all 16 pilot rows:

```text
docs/process/CARVER_16_SYMBOL_NINJATRADER_STATIC_DATED_CONTRACT_EVIDENCE_INTAKE_AND_SELECTION_EXECUTION_2026-05-30.md
docs/researchops/first_data_intake/CARVER_16_SYMBOL_NINJATRADER_STATIC_DATED_CONTRACT_SELECTION_2026-05-30.csv
SHA256: 4A6B975B5C4B58F422BB4695F4AD83C8166A12EED13EE86B5B1A05C4464C9F4F
```

Selected contracts:

```text
ZT  -> ZT 06-26
ZF  -> ZF 06-26
ZN  -> ZN 06-26
MES -> MES 06-26
MNQ -> MNQ 06-26
M2K -> M2K 06-26
MYM -> MYM 06-26
QM  -> QM 07-26
RB  -> RB 07-26
ZC  -> ZC 07-26
ZS  -> ZS 07-26
ZM  -> ZM 07-26
ZL  -> ZL 07-26
ZW  -> ZW 07-26
HE  -> HE 06-26
LE  -> LE 06-26
```

This was static source/process work only. It did not use market rows or historical availability as selection evidence.

## NinjaTrader Helper Path

The NinjaTrader helper/export strategy was shaped, patched, and tested through fail-closed gates.

Key records:

```text
docs/process/CARVER_16_SYMBOL_NINJATRADER_BATCH_DAILY_INTAKE_SHAPE_GATE_DRAFT_2026-05-30.md
docs/process/CARVER_16_SYMBOL_NINJATRADER_LOCKED_MANIFEST_DAILY_EXPORT_HELPER_2026-05-30.md
docs/process/CARVER_16_SYMBOL_NINJATRADER_PATCHED_PREFLIGHT_FAIL_CLOSED_EXPORT_STRATEGY_REDECISION_2026-05-30.md
docs/process/CARVER_16_SYMBOL_NINJATRADER_CHART_ADDDATASERIES_EXPORT_HELPER_2026-05-30.md
docs/process/CARVER_16_SYMBOL_NINJATRADER_CHART_SERIES_DOWNLOAD_TEST_FAIL_CLOSED_RESULT_2026-05-30.md
docs/process/CARVER_16_SYMBOL_NINJATRADER_FULL_DAILY_HISTORY_HELPER_PATCH_HANDOFF_2026-05-30.md
docs/process/CARVER_16_SYMBOL_NINJATRADER_FULL_DAILY_HISTORY_CARVEDD_SHORT_PATH_PATCH_2026-05-30.md
```

NinjaTrader conclusion:

```text
NINJATRADER_FULL_16_BATCH_PATH: FAIL_CLOSED_NOT_SELECTED_AS_COMPLETED_ARCHIVE_PATH
```

The NinjaTrader route remains useful as local provider evidence and as an operator-accessible manual/export fallback, but it did not complete the full 16-symbol quarantine archive. The failed helper paths did not authorize row dropping, symbol substitution, reweighting, diagnostics, backtests, forecasts, positions, or promotion.

## Databento Selected Path

The source-native futures daily data-source decision selected Databento as the cleanest executable quarantine archive path after Databento API authentication was remediated and Norgate remained fail-closed for public proof of exact support.

Key records:

```text
docs/process/CARVER_SOURCE_NATIVE_FUTURES_DAILY_DATA_LIBRARY_ARCHITECTURE_GATE_DRAFT_2026-05-30.md
docs/process/CARVER_16_SYMBOL_FULL_DAILY_HISTORY_QUARANTINE_ARCHIVE_SHAPE_GATE_DRAFT_2026-05-30.md
docs/process/CARVER_16_SYMBOL_FULL_DAILY_HISTORY_PROVIDER_ACCESS_DECISION_2026-05-30.md
docs/process/CARVER_DATABENTO_API_ACCESS_REMEDIATION_RESULT_2026-05-30.md
docs/process/CARVER_DATABENTO_16_SYMBOL_DAILY_FUTURES_QUARANTINE_INTAKE_SHAPE_GATE_DRAFT_2026-05-30.md
```

Databento source:

```text
provider: Databento Historical
dataset: GLBX.MDP3
schema: ohlcv-1d
```

No continuous contracts are accepted in this closeout.

## Five-Day Pipe Proof

The bounded five-day Databento quarantine intake passed for the exact locked 16 dated contracts over completed trading dates 2026-05-18 through 2026-05-22.

Records:

```text
docs/process/CARVER_DATABENTO_16_SYMBOL_DAILY_OHLCV_QUARANTINE_INTAKE_EXECUTION_PASS_2026-05-30.md
docs/process/CARVER_DATABENTO_16_SYMBOL_DAILY_OHLCV_QUARANTINE_PIPE_SMOKE_TEST_PASS_2026-05-30.md
```

Result:

```text
PASS_EXACT_16_SYMBOL_5_DAILY_ROWS_QUARANTINE_ONLY
PASS_REPRODUCIBLE_QUARANTINE_NORMALIZATION_AND_VALIDATION
```

Five-day rows:

```text
16 symbols * 5 completed trading dates = 80 accepted quarantine rows
```

The smoke test regenerated the quarantine outputs from saved raw provider output and confirmed byte-identical sanitized/validation results. It performed no new provider API access and no strategy computation.

## Full-History Dated-Contract Archive

The full-history quarantine archive completed using one exact 2026-current Databento instrument ID per locked dated contract.

Record:

```text
docs/process/CARVER_DATABENTO_16_SYMBOL_DATED_CONTRACT_FULL_HISTORY_QUARANTINE_ARCHIVE_PASS_2026-05-30.md
```

Archive root:

```text
docs/researchops/source_native_futures_daily_data_library/16_SYMBOL_FULL_DAILY_HISTORY/raw_provider_archive/DATABENTO/20260530_DATED_CONTRACT_FULL_AVAILABLE_HISTORY_PER_SYMBOL_CURRENT_IDS
```

Result:

```text
PASS_WITH_PROVIDER_CONDITION_WARNINGS_16_SYMBOL_DATED_CONTRACT_PER_SYMBOL_CURRENT_ID_FULL_HISTORY_QUARANTINE_ONLY
```

Summary:

```text
SYMBOLS_EXPECTED: 16
SYMBOLS_WITH_RAW_FILES: 16
ACCEPTED_MARKET_ROWS: 4568
DUPLICATE_DATES_TOTAL: 0
ALL_16_SYMBOLS_HAVE_ROWS: YES
PROVIDER_CONDITION_WARNINGS_OBSERVED: YES
```

Row coverage:

```text
ZTM6   142 rows  2025-11-05 through 2026-05-29
ZFM6   148 rows  2025-11-19 through 2026-05-29
ZNM6   173 rows  2025-10-21 through 2026-05-29
MESM6  232 rows  2025-04-09 through 2026-05-29
MNQM6  231 rows  2025-04-09 through 2026-05-29
M2KM6  193 rows  2025-06-03 through 2026-05-29
MYMM6  190 rows  2025-10-03 through 2026-05-29
QMN6   123 rows  2025-10-10 through 2026-05-29
RBN6   278 rows  2023-08-28 through 2026-05-29
ZCN6   560 rows  2023-05-23 through 2026-05-29
ZSN6   461 rows  2023-05-25 through 2026-05-29
ZMN6   393 rows  2024-06-07 through 2026-05-29
ZLN6   375 rows  2023-10-10 through 2026-05-29
ZWN6   409 rows  2023-07-24 through 2026-05-29
HEM6   307 rows  2025-01-30 through 2026-05-29
LEM6   353 rows  2025-01-02 through 2026-05-29
```

## Provider-Condition Overlay

The provider-condition metadata readiness gate fetched official Databento metadata for `GLBX.MDP3` over the archive date range and joined provider condition labels onto every archive row.

Records:

```text
docs/process/CARVER_DATABENTO_PROVIDER_CONDITION_METADATA_READINESS_GATE_DRAFT_2026-05-30.md
docs/process/CARVER_DATABENTO_PROVIDER_CONDITION_METADATA_READINESS_EXECUTION_PASS_2026-05-30.md
```

Provider-condition artifact root:

```text
docs/researchops/source_native_futures_daily_data_library/16_SYMBOL_FULL_DAILY_HISTORY/raw_provider_archive/DATABENTO/20260530_DATED_CONTRACT_FULL_AVAILABLE_HISTORY_PER_SYMBOL_CURRENT_IDS/provider_condition_metadata_2026-05-30
```

Result:

```text
PASS_PROVIDER_CONDITION_METADATA_JOIN_WITH_DEGRADED_ROWS_QUARANTINED
```

Verified join summary:

```text
ARCHIVE_ROWS_JOINED: 4568
DATASET_CONDITION_RECORDS: 948
ROW_READY_PROVIDER_CONDITION_NORMAL: 4483
ROW_QUARANTINED_PROVIDER_CONDITION_DEGRADED: 85
BLOCKED_OR_UNRESOLVED_PROVIDER_CONDITION_ROWS: 0
```

Degraded dates preserved:

```text
2025-09-17: 10 rows
2025-09-24: 11 rows
2025-11-28: 14 rows
2026-03-15: 9 rows
2026-03-16: 16 rows
2026-04-10: 16 rows
2026-05-24: 9 rows
```

Policy:

```text
available -> ROW_READY_PROVIDER_CONDITION_NORMAL at provider-condition scope only
degraded  -> ROW_QUARANTINED_PROVIDER_CONDITION_DEGRADED
```

No degraded row is strategy-facing ready. Normal provider-condition rows are still not strategy-facing ready until a later data-library promotion/readiness gate explicitly opens that scope.

## Closeout Decision

The 16-symbol daily intake pilot readiness and execution path is closed at quarantine scope.

Disposition:

```text
PASS_16_SYMBOL_DAILY_INTAKE_PILOT_QUARANTINE_ONLY_WITH_PROVIDER_CONDITION_LABELS
```

This means:

- the 16-symbol pilot universe is preserved without silent row dropping;
- explicit dated contracts were selected and preserved;
- the local NinjaTrader helper path was attempted and failed closed without substitution;
- Databento was selected and executed as the practical source-native quarantine archive path;
- the five-day 16-symbol pipe proof passed;
- the pipe smoke test proved reproducible quarantine normalization from saved raw provider output;
- the full-history dated-contract archive exists for all 16 rows;
- provider-condition metadata is joined row/date-wise;
- degraded provider-condition rows are quarantined and blocked for strategy use.

## What Remains Closed

This closeout does not authorize:

```text
strategy-facing promotion
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
Git staging
commit
push
PR update/opening
remote repository operations
```

## Next Clean Chapter

The next clean chapter should be one of:

```text
CARVER_SOURCE_NATIVE_DAILY_DATA_LIBRARY_STRATEGY_FACING_PROMOTION_SHAPE_GATE
CARVER_16_SYMBOL_DATA_LIBRARY_OPUS_AUDIT_PACKET
CARVER_DATABENTO_PROVIDER_CONDITION_SCHEMA_SCOPE_SUPPORT_PACKET
```

The recommended next step is the strategy-facing promotion shape gate only if the operator wants to decide how quarantined daily data may become Development/Reconciliation input. That future gate must decide whether to exclude all degraded rows, require Databento support clarification, or keep the archive quarantined until a broader source-quality policy exists.

## Non-Authorization

This artifact authorizes no provider API access, no new market-data request, no market-row parsing, no diagnostics, no backtests, no forecasts, no positions, no costs, no carry, no trend, no volatility/risk calculations, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.
