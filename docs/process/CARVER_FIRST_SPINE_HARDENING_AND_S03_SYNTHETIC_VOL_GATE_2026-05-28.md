# Carver First Spine Hardening And S03 Synthetic Volatility Gate

Date: 2026-05-28

Status:

```text
PROCESS_ONLY_CARVER_FIRST_SPINE_HARDENING_AND_S03_SYNTHETIC_VOL_NOT_DATA_NOT_BACKTEST
```

## Purpose

Harden the first daily source-native futures implementation spine without opening market data, diagnostics, historical backtests, OOS, Lockbox, Forward, CFD adapters, deployment, trading, or promotion.

This chapter extends the prior synthetic gate only:

```text
M0 contract/rule guardrails -> M1 sizing -> M3 exact portfolio validation -> S03 synthetic volatility estimate -> S01/S02/S03/S04/P01/P02 synthetic conformance
```

## Authorized Implementation Surface

Authorized code may include only:

- Source-native contract identity containers with exact code, name, exchange, currency, multiplier, and lane class.
- Fail-closed placeholders for session calendar, roll rule, back-adjustment rule, and `config/costs.json` cost source.
- Stronger P01/P02 portfolio validation, including exact contract identity and exact synthetic market-input membership.
- S03 synthetic-only EWMA/blended annual risk estimation from hand-built completed daily observations.
- Focused synthetic tests proving fail-closed behavior and deterministic S03 estimator behavior.

## Explicit Non-Authorization

This gate does not authorize:

- Real market data access.
- NinjaTrader export or parsing.
- CSV, database, cache, API, brokerage, account, credential, or order-routing file access.
- Diagnostics, historical backtests, OOS, Lockbox, Forward, CFD adapter work, old QuantLab imports, tuning, deployment, trading, or promotion.
- Forecast M2 logic, carry M5 logic, S09, S10, or S11 implementation.

## S03 Synthetic Volatility Notes

The S03 estimator is a synthetic conformance implementation only. It validates completed daily synthetic observations, computes daily percentage returns, applies a deterministic EWMA variance with span 32, annualizes with 256 days, and blends the resulting short-run annual risk with an operator-supplied long-run annual risk using 30/70 long/short weights.

Production warm-up, vendor session calendars, roll-adjusted input construction, price-point sizing for negative prices, and source-data availability remain unresolved gates.

## Standing Non-Authorization

This file authorizes no data access, no market-row parsing, no NinjaTrader export, no diagnostics, no historical backtests, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old-adapter import, no tuning, no deployment, no trading, and no promotion.
