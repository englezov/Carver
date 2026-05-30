# Carver NinjaTrader-Supported Pilot MES Tiny Historical-Bar Intake Execution

Date: 2026-05-30

Status:

```text
PROCESS_SOURCE_CARVER_NINJATRADER_SUPPORTED_PILOT_MES_TINY_HISTORICAL_BAR_INTAKE_EXECUTION_PASS_QUARANTINE_ONLY_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Execute the separately authorized tiny historical-bar intake gate for the statically locked MES dated contract:

```text
MES 06-26
```

Target completed trading-date window:

```text
2026-05-18 through 2026-05-22 inclusive
```

This gate was allowed to ingest only a NinjaTrader historical export for the exact MES 06-26 daily-bar window above, preserve a raw quarantine copy, create a sanitized OHLCV CSV, and apply only row-shape, UTC end-of-bar, TradingDay mapping, template/CME conflict, stale/missing/duplicate, and session-alignment fail-closed checks.

## Inputs

Shape gate:

```text
docs/process/CARVER_NINJATRADER_SUPPORTED_PILOT_MES_TINY_HISTORICAL_BAR_INTAKE_SHAPE_GATE_DRAFT_2026-05-30.md
```

Static dated-contract lock:

```text
docs/process/CARVER_NINJATRADER_SUPPORTED_PILOT_MES_STATIC_DATED_CONTRACT_LOCK_2026-05-30.md
docs/researchops/first_data_intake/CARVER_NINJATRADER_SUPPORTED_PILOT_MES_STATIC_DATED_CONTRACT_LOCK_2026-05-30.csv
```

Completed-bar and holiday-precedence policy:

```text
docs/process/CARVER_NINJATRADER_SUPPORTED_PILOT_COMPLETED_BAR_HOLIDAY_PRECEDENCE_POLICY_DECISION_2026-05-30.md
docs/researchops/first_data_intake/CARVER_NINJATRADER_SUPPORTED_PILOT_TRADING_HOURS_ROW_POLICY_LEDGER_2026-05-30.csv
```

## Quarantine Path

Created quarantine folder:

```text
docs/researchops/first_data_intake/quarantine/MES_06_26_2026-05-18_2026-05-22/
```

Created child folders:

```text
raw_source_copy/
sanitized_bars/
provenance/
```

## Source Export Search

The execution searched for an already-present exact or plausible MES 06-26 NinjaTrader daily export under:

```text
docs/researchops/first_data_intake/
docs/researchops/first_data_intake/quarantine/
data/
exports/
C:\Users\openclaw\Downloads
C:\Users\openclaw\Documents\NinjaTrader 8\export
C:\Users\openclaw\Desktop (top-level files only)
```

Historical NinjaTrader cache/database folders were not used as source data. Old QuantLab pipeline files were not used.

## Result

No MES 06-26 NinjaTrader historical export file for the exact target window was present.

After the subsequent manual/local export placement and tiny intake rerun authorization, the locked raw-source placement path was inspected again:

```text
docs/researchops/first_data_intake/quarantine/MES_06_26_2026-05-18_2026-05-22/raw_source_copy/
```

No raw MES 06-26 export file was present there, and no matching MES 06-26 daily export file was found in ordinary local drop paths.

After the local NinjaTrader helper execution gate was authorized, an armed helper copy was placed at:

```text
C:\Users\openclaw\Documents\NinjaTrader 8\bin\Custom\Indicators\CarverMesTinyDailyExporter.cs
```

Armed copy SHA256:

```text
D12F953D71F4C000B150884C78AB038BEBF88BC4C4DD70F5FD38EB55F5E9EC08
```

The repo helper remains disarmed. The locked raw output file was checked after armed-copy placement and was still absent.

The locked raw output file later appeared at:

```text
docs/researchops/first_data_intake/quarantine/MES_06_26_2026-05-18_2026-05-22/raw_source_copy/MES_06-26_Daily_Last_2026-05-18_2026-05-22.csv
```

Raw file SHA256:

```text
9313F3A3128DF0A989F7DEE09C007C81246D968AE5FE690ECE47143199F91FF1
```

Execution disposition:

```text
FAIL_CLOSED_UTC_END_OF_BAR_TEMPLATE_SESSION_ALIGNMENT_FAILED_NO_SANITIZED_BARS_CREATED
```

Because the authorized raw export file failed UTC end-of-bar and template session-alignment checks:

- the raw source copy was preserved;
- market rows were parsed only for the authorized tiny row-shape/session-alignment checks;
- no sanitized OHLCV bars CSV was created;
- TradingDay mapping was applied only for the five authorized rows;
- stale/missing/duplicate/session-alignment checks were applied only for the five authorized rows.

This is a fail-closed execution result, not a partial intake.

## Row-Level Validation Result

Row-level validation report:

```text
docs/researchops/first_data_intake/quarantine/MES_06_26_2026-05-18_2026-05-22/provenance/MES_06_26_DAILY_2026-05-18_2026-05-22_ROW_VALIDATION.csv
```

SHA256:

```text
20D1E47C7DDDC884E123461848B6EF2945C0CA3C15C3F711C14B8FE98391FE1B
```

Summary:

```text
rows_seen: 5
rows_accepted_for_sanitized_output: 0
failure: UTC_TIMESTAMP_NOT_EXTRACTED_TEMPLATE_SESSION_END
additional_failure: final raw timestamp maps outside target TradingDay window
```

The raw timestamps are `23:00:00Z`. During May 2026, that maps to 18:00 Central wall time. The extracted `CME US Index Futures ETH` template weekday session end is 16:00 Central, so the rows do not satisfy the gate's UTC end-of-bar/session-alignment boundary.

## Corrected V2 Intake Result

The distinct v2 helper:

```text
CarverMesTinyDailyExporterSessionEndUtc
```

produced the corrected helper raw-output file:

```text
docs/researchops/first_data_intake/quarantine/MES_06_26_2026-05-18_2026-05-22/raw_source_copy/MES_06-26_Daily_Last_2026-05-18_2026-05-22_TEMPLATE_SESSION_END_UTC.csv
```

Clarification:

```text
HELPER_RAW_OUTPUT_WITH_TEMPLATE_DERIVED_UTC_SESSION_END_TIMESTAMPS_NOT_PROVIDER_VERBATIM_TIME0
```

The corrected v2 file preserves the helper's raw OHLCV output but writes the locked template-derived `timestamp_utc` value. It is not a provider-verbatim copy of NinjaTrader `Time[0]`.

Corrected raw SHA256:

```text
39C9572844D184523CBC47E394BEDAB8BAC246F7CDB9134FEF2535F68325984E
```

The corrected rows use template session-end UTC timestamps:

```text
2026-05-18T21:00:00Z
2026-05-19T21:00:00Z
2026-05-20T21:00:00Z
2026-05-21T21:00:00Z
2026-05-22T21:00:00Z
```

Corrected validation report:

```text
docs/researchops/first_data_intake/quarantine/MES_06_26_2026-05-18_2026-05-22/provenance/MES_06_26_DAILY_2026-05-18_2026-05-22_TEMPLATE_SESSION_END_ROW_VALIDATION.csv
```

SHA256:

```text
2356D272E20782CFBE710364020EFFDB5DFE13A065DA0E7D091C67879DAEF33E
```

Corrected intake disposition:

```text
PASS_TINY_HISTORICAL_BAR_INTAKE_QUARANTINE_ONLY
```

Sanitized quarantine CSV:

```text
docs/researchops/first_data_intake/quarantine/MES_06_26_2026-05-18_2026-05-22/sanitized_bars/MES_06_26_DAILY_2026-05-18_2026-05-22.csv
```

SHA256:

```text
0FE54EA66726F26B0C2A984D3B75465AC373B234F516391472F1E61D2AF6B383
```

Accepted rows:

```text
5
```

This pass authorizes no diagnostics, backtests, returns, PnL, Sharpe, drawdown, forecasts, positions, costs, carry, trend, OOS, Lockbox, Forward, CFD adapter work, deployment, trading, or promotion.

## Machine-Readable Status

Execution status ledger:

```text
docs/researchops/first_data_intake/quarantine/MES_06_26_2026-05-18_2026-05-22/provenance/MES_06_26_DAILY_2026-05-18_2026-05-22_INTAKE_EXECUTION_STATUS.csv
```

SHA256:

```text
26574CE0FDC2405EB47ECC7ACFAD1EE33A16168C2A4C24FD59875923B6912D3F
```

Provenance record:

```text
docs/researchops/first_data_intake/quarantine/MES_06_26_2026-05-18_2026-05-22/provenance/MES_06_26_DAILY_2026-05-18_2026-05-22_PROVENANCE.md
```

SHA256:

```text
33B697A778B867C64FEEC05E8D7616341B7F14C6D5A5EA0CF46909B5F319E2D7
```

## Boundary Preserved

No diagnostics, backtests, returns, PnL, Sharpe, drawdown, forecast computation, position sizing, costs, carry, trend, OOS, Lockbox, Forward, CFD adapter work, old QuantLab pipeline use, tuning, deployment, trading, promotion, provider API access, or remote operation occurred.

## Next Clean Gate

The timestamp-policy correction gate has been completed by the distinct v2 helper and corrected raw file recorded above.

This tiny intake is now complete only at the quarantine row-shape/session-alignment level:

```text
MES 06-26
1 Day
Last
2026-05-18 through 2026-05-22 inclusive
```

The next clean gate, if separately authorized, should be a process-only closeout or expansion decision. It must not treat the sanitized MES rows as diagnostic, backtest, forecast, position-sizing, trading, deployment, or promotion evidence.

## Non-Authorization

This execution record authorizes no further NinjaTrader export, no market-row parsing, no diagnostics, no backtests, no returns, no PnL, no Sharpe, no drawdown, no forecast computation, no position sizing, no costs, no carry, no trend, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old QuantLab pipeline use, no tuning, no deployment, no trading, no promotion, no provider API access, no remote push, and no GitHub action.
