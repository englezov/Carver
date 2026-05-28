# Carver P05 Jumbo Multiple Trend Portfolio Shape Gate

Date: 2026-05-29

Status:

```text
PROCESS_ONLY_CARVER_P05_JUMBO_MULTIPLE_TREND_PORTFOLIO_SHAPE_NOT_DATA_NOT_BACKTEST
```

## Purpose

Record the future P05 portfolio boundary without opening implementation or data work.

P05 is the complete book portfolio that applies S09 multiple trend following across the Jumbo futures universe after S09 and all source-native machinery are locked.

Summary shape:

```text
S09 over a source-locked Jumbo futures universe with per-instrument eligible EWMAC speed sets.
```

## Required Dependencies

- M0 source-native futures foundation.
- M1 position sizing and risk scaling.
- M2 forecast-block architecture.
- M3 multi-instrument portfolio construction.
- S03 variable-risk estimate source.
- S09 multiple trend following source and synthetic code gate.
- Source-native contract identity, session, roll, back-adjustment, cost, FX, and daily price-point risk artifacts for every admitted instrument.

## Shape

```text
For each eligible Jumbo instrument:
  construct S09 EWMAC forecasts from completed daily closes,
  use the locked eligible EWMAC speed set for that instrument,
  combine forecasts through M2,
  pass the final capped forecast into inherited position sizing,
  aggregate through a separately locked M3 Jumbo portfolio construction.
```

## Blocked Before Any P05 Data Work

- Appendix C/Jumbo universe mapping.
- Per-instrument source-native provider IDs.
- Completed daily session/cut for every instrument.
- Roll/back-adjustment and current held-contract price source.
- Per-instrument cost source and speed/cost eligibility artifact.
- Instrument weights, IDM, target risk, capital base, and minimum-capital rule.
- Evidence-window budget.

## Non-Authorization

This shape gate authorizes no data access, no market-row parsing, no implementation beyond the S09/M2 synthetic gate, no diagnostics, no backtests, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old QuantLab import, no tuning, no deployment, no trading, and no promotion.
