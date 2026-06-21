# Carver 16-Symbol NinjaTrader Chart/AddDataSeries Export Helper Hostile Audit Result

Date: 2026-05-30

Status:

```text
PROCESS_ONLY_LEAN_HOSTILE_AUDIT_RESULT_CARVER_16_SYMBOL_NINJATRADER_CHART_ADDDATASERIES_HELPER_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Scope

Lean hostile re-audit of:

```text
tools/nt8/Carver16SymbolDailyChartSeriesExporterSessionEndUtc.cs
docs/process/CARVER_16_SYMBOL_NINJATRADER_CHART_ADDDATASERIES_EXPORT_HELPER_2026-05-30.md
```

The audit was performed by subagent.

## Result

```text
BLOCKING_FINDINGS: NO
AUDIT_DISPOSITION: PASS_READ_ONLY_HOSTILE_REAUDIT
```

## Later Correction

After the bounded NinjaTrader GUI test, runtime evidence showed NinjaTrader chart `Instrument.FullName` uses `SYMBOL MONYY` syntax such as `MES JUN26`, while the Carver ledger/output contract remains `SYMBOL MM-YY` such as `MES 06-26`.

The helper was corrected after this audit to restore the runtime/provenance split:

```text
NINJATRADER_RUNTIME_CONTRACT_SYNTAX: SYMBOL_MONYY
CARVER_LEDGER_OUTPUT_CONTRACT_SYNTAX: SYMBOL_MM_DASH_YY
```

This audit result is retained as the pre-correction audit record. The corrected helper hash is:

```text
CABC79C9CE7FCDA13C83CCEC9326CA44DDF4A9D60CB0203F32ED8B36CABB34C8
```

## Checked Items

- `SYMBOL MM-YY` ledger-native contract syntax is used for manifest contracts, `AddDataSeries`, and primary validation.
- No `SYMBOL MONYY` loading or primary-validation path remains.
- Trading-hours template mismatch fails closed before row collection or helper raw-output write.
- Temp files and moved outputs are cleaned up on batch write/move failure.
- `ExecutionArmed = false` by default, and `State.Configure` returns before `AddDataSeries`.
- The exact 16 manifest rows, locked dates `2026-05-18` through `2026-05-22`, locked output root, `1 Day` / `Last` surface, no `BarsRequest`, and no substitution/drop/reweight path are preserved.
- Handoff SHA matches helper:

```text
C2AD47BC6BE35CF28EE385E00B8A88DEAFFA90D1AC8A86C18ADD603B1B126878
```

## Non-Blocking Note

The repo-disarmed helper does not add secondary series because `State.Configure` returns before `AddDataSeries`. It still runs validation during `State.DataLoaded`, so applying the disarmed helper to a non-locked chart may throw. This does not create data/export risk. The handoff meaning is:

```text
DISARMED_MEANS_NO_SECONDARY_SERIES_ADDED_NOT_FULLY_INERT_ON_ANY_CHART
```

## Non-Authorization

This record authorizes no new data export, no provider API access, no market-row parsing, no NinjaTrader execution, no diagnostics, no backtests, no forecasts, no positions, no costs, no carry, no trend, no OOS, no Lockbox, no Forward, no CFD adapter work, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no GitHub staging, no commit, no push, no PR update/opening, and no remote operations.
