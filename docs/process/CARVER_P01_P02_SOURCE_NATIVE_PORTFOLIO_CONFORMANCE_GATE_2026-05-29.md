# Carver P01/P02 Source-Native Portfolio Conformance Gate

Date: 2026-05-29

Status:

```text
PROCESS_ONLY_AND_SYNTHETIC_CODE_CARVER_P01_P02_PORTFOLIO_CONFORMANCE_GATE_NOT_BACKTEST_NOT_DATA_DOWNLOAD
```

## Purpose

Wire the first place where the Carver spine clicks together:

```text
locked source-native contract identity
-> quarantined normalized chart/minute bars
-> completed daily market bars
-> prevalidated annual risk and FX inputs
-> M1/M3 sizing
-> P01/P02 exact-portfolio conformance
```

This gate is still synthetic-only. It proves the shape of the intake and portfolio conformance path without executing a real NinjaTrader/Tradovate API call, reading live browser storage, downloading market history, running a diagnostic, or running a backtest.

## Implemented Surface

The code surface added by this gate is deliberately small:

- `daily_bars.py` derives a completed daily OHLCV bar from a full contiguous one-minute synthetic session.
- `daily_bars.py` also normalizes direct daily Web Chart bars as the primary intake path when the provider supplies completed daily candles.
- `web_chart_api.py` can read a JSON chart response only from a Git-ignored quarantine directory and normalize it through the existing synthetic chart validator. The response envelope must echo the exact locked request payload and provider identity before any bars are admitted. Normalized bars remain request-bound and cannot be replayed under a different request.
- `continuous.py` defines a continuous-contract rule set but refuses to build a continuous/back-adjusted series until session, roll, back-adjustment, and cost-source rules are locked separately.
- `portfolio_conformance.py` sizes P01/P02 from exact completed daily bars, prevalidated annual risk estimates, and aligned FX rates.
- `portfolio_conformance.py` defines exact provider mapping sets that must match the portfolio legs and the locked provider registry before a real-data route can be considered mapped.
- Provider-symbol mapping status is explicit and fail-closed. The currently locked observed mappings are only `ES 06-26 -> 3570919` and `ZN 06-26 -> 4470301`. P01 uses `MES` and `ZN`; P02 uses `MES`, `ZN`, `ZF`, `QM`, `ZC`, and `MGC`. Therefore real P01/P02 Web Chart conformance remains blocked until exact book-contract provider IDs are locked.

## Required Next Data-Surface Locks

Before any real P01/P02 data pull or conformance run:

- Lock exact NinjaTrader/Tradovate provider IDs for `MES`, `ZN`, `ZF`, `QM`, `ZC`, and `MGC` contract months.
- Lock the daily-session convention for each instrument.
- Lock whether the first data intake uses direct daily bars or one-minute-to-daily derivation.
- Lock roll and back-adjustment rules for continuous series use.
- Lock annual risk estimates and FX inputs as prevalidated upstream facts, not post-result tuned values.
- Pass the real-data conformance preflight before any future real-data sizing call.
- Keep any raw API response under quarantine and parse only expected JSON chart envelopes.

## Explicit Non-Authorization

This gate authorizes no real WebSocket call, no token/cookie/storage extraction, no NinjaTrader export, no `.ncd` decoding, no bulk download, no data diagnostic, no backtest, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old QuantLab import, no tuning, no deployment, no trading, no promotion, and no remote push.

## Test Posture

Synthetic tests cover:

- quarantined JSON chart response normalization;
- full-session one-minute-to-completed-daily derivation;
- rejection of missing, gapped, incomplete, or misaligned bars;
- fail-closed continuous/roll/back-adjustment placeholders;
- exact P01/P02 portfolio conformance from completed daily closes;
- unresolved provider mappings for P01/P02 instruments.

The test suite does not use real market data and does not claim strategy performance.
