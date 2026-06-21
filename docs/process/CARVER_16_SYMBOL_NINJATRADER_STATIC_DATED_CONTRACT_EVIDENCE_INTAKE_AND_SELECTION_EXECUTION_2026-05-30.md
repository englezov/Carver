# Carver 16-Symbol NinjaTrader Static Dated-Contract Evidence Intake And Selection Execution

Date: 2026-05-30

Status:

```text
PROCESS_SOURCE_CARVER_16_SYMBOL_NINJATRADER_STATIC_DATED_CONTRACT_SELECTION_EXECUTION_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Execute the static dated-contract selection gate for the 16-symbol NinjaTrader-supported daily intake pilot:

```text
ZT, ZF, ZN, MES, MNQ, M2K, MYM, QM, RB, ZC, ZS, ZM, ZL, ZW, HE, LE
```

This artifact selects explicit source-native dated contracts using static evidence only. It does not authorize NinjaTrader historical export, provider API access, market-row parsing, diagnostics, backtests, forecasts, positions, costs, carry, trend, deployment, trading, promotion, GitHub publication, or any old QuantLab active-pipeline use.

## Input Gate

Shape gate:

```text
docs/process/CARVER_16_SYMBOL_NINJATRADER_STATIC_DATED_CONTRACT_SELECTION_SHAPE_GATE_DRAFT_2026-05-30.md
```

Selection as-of date:

```text
2026-05-30
```

Target completed trading-date window:

```text
2026-05-18 through 2026-05-22 inclusive
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Static Evidence Used

Current Carver static artifacts:

- `docs/researchops/portfolios/CARVER_APPENDIX_C_JUMBO_UNIVERSE_LOCK_2026-05-29.csv`
- `docs/researchops/provider_mappings/CARVER_APPENDIX_C_NINJATRADER_SOURCE_NATIVE_PROVIDER_MAPPING_2026-05-29.csv`
- `docs/researchops/contract_identity/CARVER_APPENDIX_C_CONTRACT_IDENTITY_STATIC_HARDENING_UPDATE_2026-05-30.csv`
- `docs/researchops/contract_specs/CARVER_APPENDIX_C_STATIC_CONTRACT_SPEC_EVIDENCE_INTAKE_2026-05-30.csv`
- `docs/researchops/first_data_intake/CARVER_NINJATRADER_SUPPORTED_PILOT_EXPLICIT_CONTRACT_MONTH_CONTRACT_IDENTITY_FINAL_STATIC_LOCK_2026-05-30.csv`
- `docs/researchops/first_data_intake/CARVER_NINJATRADER_SUPPORTED_PILOT_STATIC_POLICY_READINESS_REFRESH_2026-05-30.csv`
- `docs/researchops/first_data_intake/CARVER_NINJATRADER_SUPPORTED_PILOT_TRADING_HOURS_ROW_POLICY_LEDGER_2026-05-30.csv`

Local static NinjaTrader evidence:

```text
C:\Users\openclaw\Documents\NinjaTrader 8\db\NinjaTrader.sqlite
```

Only the static `MasterInstruments` and `Instruments` tables were inspected. Account, order, execution, position, strategy, log, and market-row data tables were not used as evidence.

Official static source URLs are recorded per row in the output ledger. They are CME Group contract specification pages, CME Group fact cards, CME Group educational PDFs, and CME Group Treasury futures education material already named by the existing contract-spec evidence ledgers. No provider API, historical availability check, market data page, or bar endpoint was used.

## Output Ledger

Machine-readable output:

```text
docs/researchops/first_data_intake/CARVER_16_SYMBOL_NINJATRADER_STATIC_DATED_CONTRACT_SELECTION_2026-05-30.csv
```

SHA256:

```text
4A6B975B5C4B58F422BB4695F4AD83C8166A12EED13EE86B5B1A05C4464C9F4F
```

## Selection Result

Global checks:

```text
ROWS_EXPECTED: 16
ROWS_PRESERVED: 16
UNIQUE_ROW_IDS: 16
STATIC_DATED_CONTRACT_SELECTED_FOR_16_SYMBOL_DAILY_INTAKE: 16
MARKET_ROW_ACCESS_STATUS: NO_MARKET_ROW_ACCESS
PROVIDER_API_ACCESSED: NO
NINJATRADER_HISTORICAL_EXPORT_USED: NO
DIAGNOSTICS_OR_BACKTESTS_RUN: NO
SUBSTITUTION_STATUS: FAIL_CLOSED_NO_DROP_NO_SUBSTITUTE_NO_REWEIGHT
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

## Family Decisions

### Rates

`ZT`, `ZF`, and `ZN` select June 2026. Static support:

- official Treasury product identity and quarterly Treasury contract cycle sources are recorded in the row evidence;
- local NinjaTrader static 2026-06 expiry rows exist;
- the full target window is before the June delivery-month conflict interval;
- no historical availability check was used.

### Equity Index Micros

`MES`, `MNQ`, `M2K`, and `MYM` select June 2026. Static support:

- official product identity and quarterly equity-index contract cycle sources are recorded in the row evidence;
- local NinjaTrader static 2026-06 expiry rows exist;
- the target window precedes the June 2026 cash-settled termination period;
- `MES 06-26` is consistent with the earlier MES-only static lock.

### Energy

`QM` and `RB` select July 2026. Static reasoning:

- monthly local NinjaTrader expiry rows exist for July 2026;
- the June nearby contracts are deliberately not selected because the target/as-of combination is lifecycle-sensitive around May 2026;
- July 2026 is the nearest static monthly candidate recorded as active/listed in the local static evidence and covering the full target window without the June nearby conflict.

This is a conservative source-native selection rule, not a data-availability decision.

### Grains And Oilseeds

`ZC`, `ZS`, `ZM`, `ZL`, and `ZW` select July 2026. Static reasoning:

- local NinjaTrader static July 2026 expiry rows exist for all five rows;
- May 2026 nearby contracts are not selected because grain/oilseed first-notice, delivery, and last-trade risk is too close to or inside the target/as-of boundary;
- July 2026 is the nearest static source-native candidate that covers the full target window without requiring a market-row look.

### Livestock

`HE` and `LE` select June 2026. Static support:

- official livestock product identity and delivery-cycle sources are recorded in the row evidence;
- local NinjaTrader static 2026-06 expiry rows exist;
- June 2026 remains the nearest static listed candidate covering the target window and active as of the static cutoff.

## What This Removes

This execution removes only the prior blocker:

```text
FAIL_CLOSED_EXPLICIT_DATED_CONTRACT_MONTH_NOT_SELECTED_NO_AS_OF_DATE_OR_TARGET_WINDOW
```

for the 16-symbol pilot.

## What Remains Closed

The following remain closed:

- 16-symbol NinjaTrader historical export;
- provider API access;
- market-row parsing;
- continuous contracts;
- merge/back-adjusted series construction;
- diagnostics;
- backtests;
- forecasts;
- positions;
- costs;
- carry;
- trend;
- OOS, Lockbox, Forward;
- CFD adapters;
- old QuantLab active-pipeline use;
- tuning;
- deployment;
- trading;
- promotion;
- GitHub staging, commit, push, or PR update.

## Next Clean Gate

Selected next gate:

```text
CARVER_16_SYMBOL_NINJATRADER_BATCH_DAILY_INTAKE_SHAPE_GATE_DRAFT
```

That future gate should define, before any export or parsing:

- exact 16-row manifest and selected dated contracts;
- `1 Day` timeframe and `Last` bars;
- fixed completed trading-date window `2026-05-18` through `2026-05-22`;
- locked helper/export strategy;
- quarantine folder layout;
- raw helper-output provenance;
- sanitized OHLCV schema;
- row-shape, timestamp, duplicate, stale/missing, and session-alignment checks;
- all-16 pass/fail semantics;
- no-diagnostics/no-backtest boundary.

## Non-Authorization

This execution authorizes no new data export, no provider API access, no market-row parsing, no NinjaTrader historical export, no diagnostics, no backtests, no forecasts, no positions, no costs, no carry, no trend, no OOS, no Lockbox, no Forward, no CFD adapter work, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no GitHub staging, no commit, no push, no PR update/opening, and no remote operations.
