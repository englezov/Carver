# Carver NinjaTrader-Supported Pilot Static Dated-Contract Evidence Intake

Date: 2026-05-30

Status:

```text
PROCESS_SOURCE_CARVER_NINJATRADER_SUPPORTED_PILOT_STATIC_DATED_CONTRACT_EVIDENCE_INTAKE_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Ingest static dated-contract evidence for the first tiny NinjaTrader-supported pilot candidate set:

```text
ZN, MES, QM, ZC
```

This gate attempts to lock active/listed status, official listed contract months, lifecycle constraints, and NinjaTrader local dated-contract syntax before any historical-bar intake.

It does not export NinjaTrader historical data, parse market rows, access provider APIs, run diagnostics, run backtests, trade, deploy, or promote anything.

## Inputs

Current Carver artifacts:

```text
docs/process/CARVER_NINJATRADER_SUPPORTED_PILOT_STATIC_DATED_CONTRACT_SELECTION_SHAPE_GATE_DRAFT_2026-05-30.md
docs/process/CARVER_NINJATRADER_SUPPORTED_PILOT_STATIC_DATED_CONTRACT_SELECTION_EXECUTION_2026-05-30.md
docs/researchops/first_data_intake/CARVER_NINJATRADER_SUPPORTED_PILOT_STATIC_DATED_CONTRACT_SELECTION_EXECUTION_2026-05-30.csv
```

Local static NinjaTrader evidence:

```text
C:\Users\openclaw\Documents\NinjaTrader 8\db\NinjaTrader.sqlite
```

The SQLite database was queried read-only. A direct file hash was not available because the file was locked by a running NinjaTrader process.

Official/static evidence references used:

```text
https://www.cmegroup.com/markets/interest-rates/us-treasury/10-year-us-treasury-note.contractSpecs.html
https://ninjatrader.com/futures/futures-contracts/us-treasury-bonds/10-year-notes/
https://www.cmegroup.com/content/dam/cmegroup/trading/interest-rates/files/us-treasury-futures-delivery-process.pdf
https://www.cmegroup.com/markets/equities/sp/micro-e-mini-sandp-500.contractSpecs.html
https://www.cmegroup.com/trading/equity-index/files/cme-micro-e-mini-futures-fact-card.pdf
https://www.cmegroup.com/markets/energy/crude-oil/e-mini-crude-oil.contractSpecs.html
https://www.cmegroup.com/trading/energy/files/micro-wti-crude-oil-futures-fact-card.pdf
https://www.cmegroup.com/markets/agriculture/grains/corn.contractSpecs.html
https://www.cmegroup.com/trading/agricultural/files/CornContractSpecs.pdf
https://ninjatrader.com/support/helpguides/nt8/rolling_over_a_futures_contrac.htm
```

No market rows, historical-bar availability checks, NinjaTrader exports, provider APIs, diagnostics, or backtests were used.

## Output

Machine-readable evidence ledger:

```text
docs/researchops/first_data_intake/CARVER_NINJATRADER_SUPPORTED_PILOT_STATIC_DATED_CONTRACT_EVIDENCE_INTAKE_2026-05-30.csv
```

SHA256:

```text
FF4E4B1C69A09C3A83FB70F12ECF7CAFBE1A29B698CA28A963C4A5327963E8BF
```

## Evidence Results

Rows preserved:

```text
CANDIDATE_ROWS_EXPECTED: 4
CANDIDATE_ROWS_PRESERVED: 4
```

Local static NinjaTrader expiry rows:

```text
LOCAL_NINJATRADER_STATIC_EXPIRY_ROW_FOUND: 4
```

Candidate local contracts recorded:

```text
ZN: ZN 06-26
MES: MES 06-26
QM: QM 06-26
ZC: ZC 07-26
```

These are evidence candidates, not selected contracts for historical-bar intake.

## Readiness Result

```text
STATIC_READY_FOR_DATED_CONTRACT_SELECTION_REEXECUTION: 0
STATIC_DATED_CONTRACT_EVIDENCE_PARTIAL_FAIL_CLOSED_NOT_READY_FOR_SELECTION_REEXECUTION: 4
```

The evidence intake improved local static dated-contract evidence but did not unlock re-selection.

Remaining blockers:

- official active/listed status as of `2026-05-30` is not fully locked;
- official listed-month evidence remains partial or not hash-bound;
- last-trade, first-notice, expiration, delivery, and cash-settlement constraints remain incomplete for at least one row;
- target-window coverage is not final-locked;
- `QM` remains especially blocked because energy expiration timing may conflict with the `2026-05-18` through `2026-05-22` target window.

## Interpretation

This is not a NinjaTrader data failure and not a market-data result.

The local static database proves that NinjaTrader has static expiry rows for candidate contracts. It does not prove that those contracts are safe for historical-bar intake under the Carver completed-bar, contract-lifecycle, and fail-closed rules.

## Next Clean Gate

Selected next gate:

```text
NINJATRADER_SUPPORTED_PILOT_STATIC_DATED_CONTRACT_SELECTION_REDECISION_GATE
```

That gate should decide whether to:

- keep all four rows blocked;
- narrow to the rows with strongest static evidence, likely `MES` first;
- select a different target window that avoids energy/grain expiry ambiguity;
- or require hash-bound official rulebook/spec extracts before trying dated-contract selection again.

It must not export historical bars, parse market rows, access provider APIs, run diagnostics, or run backtests.

## Non-Authorization

This evidence intake authorizes no code edits, no tests, no real market data, no market-row parsing, no NinjaTrader historical export, no provider API access, no diagnostics, no backtests, no returns, no PnL, no Sharpe, no drawdown, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old QuantLab pipeline use, no tuning, no deployment, no trading, no promotion, no remote push, and no GitHub action.
