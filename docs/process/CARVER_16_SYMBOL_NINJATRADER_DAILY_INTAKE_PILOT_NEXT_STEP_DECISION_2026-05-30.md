# Carver 16-Symbol NinjaTrader Daily Intake Pilot Next-Step Decision

Date: 2026-05-30

Status:

```text
PROCESS_ONLY_CARVER_16_SYMBOL_NINJATRADER_DAILY_INTAKE_PILOT_NEXT_STEP_DECISION_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Decide the next clean sequence after the completed and Opus-audited MES 06-26 tiny quarantine intake chapter.

This decision opens no data export, no provider API access, no market-row parsing, no diagnostics, no backtests, no forecasts, no positions, no costs, no carry, no trend, no deployment, no trading, and no promotion.

It defines the process path for completing the 16-symbol NinjaTrader-supported daily intake pilot.

## Inputs

Completed Appendix C to first real-data intake readiness closeout:

```text
docs/process/CARVER_APPENDIX_C_TO_FIRST_REAL_DATA_INTAKE_READINESS_CHAPTER_CLOSEOUT_2026-05-30.md
```

Opus audit result:

```text
docs/process/CARVER_APPENDIX_C_TO_FIRST_REAL_DATA_INTAKE_READINESS_OPUS_AUDIT_RESULT_2026-05-30.md
BLOCKING_FINDINGS: NO
AUDIT_DISPOSITION: PASS_APPENDIX_C_TO_FIRST_REAL_DATA_INTAKE_READINESS_QUARANTINE_ONLY_SCOPE
```

Existing 16-symbol static readiness ledgers:

```text
docs/researchops/first_data_intake/CARVER_NINJATRADER_SUPPORTED_PILOT_STATIC_READINESS_STATUS_2026-05-30.csv
docs/researchops/first_data_intake/CARVER_NINJATRADER_SUPPORTED_PILOT_STATIC_POLICY_READINESS_REFRESH_2026-05-30.csv
docs/researchops/first_data_intake/CARVER_NINJATRADER_SUPPORTED_PILOT_EXPLICIT_CONTRACT_MONTH_CONTRACT_IDENTITY_FINAL_STATIC_LOCK_2026-05-30.csv
```

MES tiny intake execution:

```text
docs/process/CARVER_NINJATRADER_SUPPORTED_PILOT_MES_TINY_HISTORICAL_BAR_INTAKE_EXECUTION_2026-05-30.md
PASS_TINY_HISTORICAL_BAR_INTAKE_QUARANTINE_ONLY
```

No new market rows, historical bars, NinjaTrader exports, provider APIs, diagnostics, or backtests were used for this decision.

## Target 16-Symbol Pilot

The target pilot remains exactly:

```text
ZT, ZF, ZN, MES, MNQ, M2K, MYM, QM, RB, ZC, ZS, ZM, ZL, ZW, HE, LE
```

Interpretation:

```text
SOURCE_NATIVE_FUTURES
NINJATRADER_SUPPORTED_DAILY_INTAKE_PILOT_CANDIDATES
```

This is not the full Appendix C 102-row Jumbo universe. It is a practical NinjaTrader-supported pilot subset selected for daily bar intake readiness work.

## Current State

The prior 16-row pilot was correctly fail-closed before the MES-only reduction:

```text
STATIC_READINESS_FAIL_CLOSED_NOT_READY_FOR_TINY_HISTORICAL_BAR_INTAKE: 16
CONTRACT_IDENTITY_FAIL_CLOSED_NOT_LOCKED: 16
SESSION_ROLL_COMPLETED_BAR_FAIL_CLOSED_NOT_LOCKED: 16
RISK_FX_COST_CARRY_LEG_FAIL_CLOSED_NOT_LOCKED: 16
ready_for_tiny_historical_bar_intake NO: 16
```

The explicit contract-month ledger likewise kept all 16 rows blocked:

```text
FAIL_CLOSED_EXPLICIT_DATED_CONTRACT_MONTH_NOT_SELECTED_NO_AS_OF_DATE_OR_TARGET_WINDOW: 16
final_static_readiness_for_tiny_historical_bar_intake NO: 16
```

The MES-only chapter then proved a narrower path:

```text
MES 06-26
1 Day Last
2026-05-18 through 2026-05-22
accepted_market_rows: 5
PASS_TINY_HISTORICAL_BAR_INTAKE_QUARANTINE_ONLY
```

The MES proof does not make the other 15 rows data-ready and does not authorize a 16-symbol export.

## Decision

Decision:

```text
OPEN_16_SYMBOL_NINJATRADER_DAILY_INTAKE_PILOT_READINESS_PATH
```

The path should aim to complete all 16 symbols under one manifest-driven daily intake pilot, but only after each row has explicit static readiness for the selected date window.

The target completed trading-date window for the 16-symbol pilot should remain:

```text
2026-05-18 through 2026-05-22 inclusive
```

Reason:

- MES already proved the quarantine/session policy for this fixed window;
- reusing the same completed trading-date window avoids choosing a new window after seeing data;
- a five-trading-day daily pilot is enough to test multi-symbol row-shape, timestamp, completeness, and provenance mechanics without opening diagnostics or backtests.

## Required Sequence

### 1. 16-Symbol Static Dated-Contract Selection Shape Gate

Create a process-only gate that defines:

- as-of date for static contract availability;
- fixed target completed trading-date window `2026-05-18` through `2026-05-22`;
- official/static evidence sources for active/listed status and listed contract months;
- dated-contract selection rule per product family;
- first notice, last trade, delivery, expiration, and cash-settlement blockers;
- NinjaTrader local dated-contract syntax requirements;
- fail-closed behavior for any row that cannot be statically selected.

No market rows or NinjaTrader historical export.

### 2. 16-Symbol Static Contract Evidence Intake

Create a process/source evidence artifact that attempts to lock, for all 16 rows:

- official active/listed status as of the chosen as-of date;
- official listed contract months covering the target window;
- last-trade/first-notice/expiration/delivery/cash-settlement constraints;
- local NinjaTrader static expiry row;
- NinjaTrader local contract syntax;
- selected source-native dated contract candidate.

Expected candidate families:

```text
Rates: ZT, ZF, ZN
Equity index: MES, MNQ, M2K, MYM
Energy: QM, RB
Grains/oilseeds: ZC, ZS, ZM, ZL, ZW
Livestock: HE, LE
```

Rows that cannot be statically locked must remain fail-closed. They must not be substituted, dropped, or reweighted inside a 16-symbol pilot claim.

### 3. 16-Symbol Static Readiness Hardening Execution

Create a machine-readable readiness ledger that records, row by row:

- selected dated contract;
- local NinjaTrader contract syntax;
- venue, currency, multiplier, point value, tick size, tick value;
- product family and variant;
- active/listed status;
- delivery cycle and expiration/first-notice/last-trade safety for the target window;
- trading-hours template;
- completed trading-date authority;
- UTC end-of-bar policy;
- local template/CME conflict policy;
- stale/missing/duplicate policy;
- daily close policy;
- risk/FX/cost/carry-leg classification status.

Required readiness target before batch export:

```text
STATIC_READY_FOR_16_SYMBOL_DAILY_INTAKE: 16
```

If fewer than 16 rows are ready, a separate process-only redecision must choose whether to fix the blockers, keep the pilot blocked, or narrow scope. Narrowing may not happen silently.

### 4. 16-Symbol Batch Intake Shape Gate

Create a process-only shape gate defining:

- exact manifest rows and dated contracts;
- bar type `Last`;
- timeframe `1 Day`;
- completed trading-date window `2026-05-18` through `2026-05-22`;
- accepted fields;
- quarantine directory layout;
- raw helper-output policy;
- sanitized OHLCV output schema;
- row validation outputs;
- provenance outputs;
- strict fail-closed rules;
- no-diagnostics/no-backtest/no-forecast boundary.

The shape gate must explicitly say whether batch success requires all 16 rows to pass. Default decision:

```text
ALL_16_ROWS_REQUIRED_FOR_16_SYMBOL_PILOT_PASS
```

### 5. Locked Manifest-Driven NinjaTrader Helper Gate

Create a locked helper/export strategy before any execution:

- one manifest-driven helper or equivalent local procedure;
- disarmed by default;
- refuses symbols not in the manifest;
- refuses contracts not in the manifest;
- refuses non-`1 Day` bars;
- refuses non-`Last` bars;
- refuses dates outside `2026-05-18` through `2026-05-22`;
- writes only under the locked 16-symbol quarantine root;
- records helper raw output vs provider-verbatim timestamp semantics;
- preserves raw outputs separately from sanitized outputs;
- does not compute diagnostics, forecasts, positions, or returns.

The helper should be allowed to export all 16 manifest rows in one controlled run only after the manifest and static readiness ledger are complete.

### 6. 16-Symbol Batch Intake Execution Gate

Only after the prior gates pass, a later execution gate may:

- run the locked local NinjaTrader helper for the 16-symbol manifest;
- preserve raw helper outputs;
- create sanitized OHLCV CSVs;
- create row-level validation ledgers;
- create provenance records;
- apply only row-shape, UTC end-of-bar, TradingDay mapping, template/CME conflict, stale/missing/duplicate, and session-alignment checks.

It must not compute diagnostics, returns, forecasts, positions, costs, carry, trend, PnL, Sharpe, drawdown, OOS, Lockbox, Forward, or promotion evidence.

### 7. Audit And Checkpoint

After batch intake execution:

- run a lean hostile audit over the 16-symbol static readiness and quarantine-only intake artifacts;
- preserve the audit result automatically as process documentation;
- decide separately whether an Opus audit is needed before any broader portfolio/readiness chapter;
- checkpoint to GitHub only under a separately authorized publication gate.

## What Remains Closed

The following remain closed after this decision:

```text
NinjaTrader historical export
provider API access
market-row parsing
diagnostics
backtests
returns
PnL
Sharpe
drawdown
forecast computation
position sizing
cost computation
carry computation
trend computation
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
remote operations
```

## Next Clean Gate

Selected next gate:

```text
CARVER_16_SYMBOL_NINJATRADER_STATIC_DATED_CONTRACT_SELECTION_SHAPE_GATE
```

That gate should define the exact as-of date, target window, static evidence sources, product-family selection rules, fail-closed row behavior, and machine-readable output expectations for selecting dated contracts across all 16 pilot symbols.

## Non-Authorization

This decision authorizes no code edits beyond this process document, no tests, no new data export, no provider API access, no market-row parsing, no diagnostics, no backtests, no forecasts, no positions, no costs, no carry, no trend, no OOS, no Lockbox, no Forward, no CFD adapter work, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no GitHub staging, no commit, no push, no PR update/opening, and no remote operations.
