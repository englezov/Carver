# Governance And Current State For Opus S26/S27 Design

Date: 2026-05-30

Status:

```text
PROCESS_ONLY_OPUS_PACKET_CONTEXT_NOT_EXECUTION_AUTHORIZATION
```

## Source Authority

The only book authority in this packet is:

```text
00_Carver.pdf
```

Use `00_Carver.pdf` as the source authority for Strategies 26 and 27. This packet intentionally does not pre-supply S26/S27 page ranges or rules; Opus should find and extract them directly from the book.

## Workspace Governance

Clean active workspace:

```text
C:\Users\openclaw\Desktop\Carver
```

Archived workspace:

```text
C:\Users\openclaw\Desktop\QuantLab_v3
```

`QuantLab_v3` is archived and must not be used as an active pipeline, adapter, data, or execution authority.

## Research Lane

The current Carver lane is:

```text
SOURCE_NATIVE_FUTURES
```

CFD assumptions, CFD broker-clock assumptions, CFD adapters, and old mixed futures/CFD translation scripts are out of scope.

## Current Research Position

The Appendix C/Jumbo data-foundation chapter has established that source-native futures data access is practical for a large Carver subset through Databento, but no strategy has been proven or promoted.

Current practical position:

```text
APPENDIX_C_SOURCE_ROWS: 102
DATABENTO_STATIC_IDENTITY_READY_INTAKE_ROWS: 66
DEV_RECON_DATA_READY_ROWS_AFTER_HARDENING: 65
FAIL_CLOSED_ROW_AFTER_HARDENING: 1
FAIL_CLOSED_ROW: APPENDIX_C_181_001 / ALI / Aluminium
```

The 65 ready rows are data-library/readiness material only:

```text
YES_DEV_RECON_DATA_READY_NOT_STRATEGY_READY
```

## Prior Book Atoms Already Verified In Earlier Work

Earlier Opus/GPT packet work verified the following high-level Carver atoms:

- Appendix C Tables 172-183 are the 102-instrument Jumbo source universe.
- Jumbo portfolio IDM is 2.47.
- Annual target risk example is 20%.
- P02 All Weather example uses S&P 500 micro, US 10-year, US 5-year, WTI crude oil mini, Corn, and Gold micro, with book IDM 1.81.
- Carver explicitly discusses small-account instrument selection, minimum capital, cost, liquidity, instrument-size choice, and micro/mini selection.
- Carver gives a small-account selection method and a $100,000 example with 16 instruments.

These atoms are context only. For S26/S27, Opus should re-extract the direct source atoms from `00_Carver.pdf`.

## Current Strategic Pivot

The operator has decided to stop deepening the Appendix C/Jumbo infrastructure chapter for now and pivot to:

```text
S26_S27_MEAN_REVERSION_SOURCE_NATIVE_RESEARCH_PATH
```

The purpose of this Opus packet is to design that path from the book before implementation.

## Non-Authorization

This packet authorizes no code execution, no file edits, no real-data parsing, no provider API access, no diagnostics, no backtests, no forecasts on real data, no positions, no position sizing, no costs, no carry, no trend computation, no volatility/risk calculations, no OOS, no Lockbox, no Forward, no CFD adapters, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git operations, and no remote operations.
