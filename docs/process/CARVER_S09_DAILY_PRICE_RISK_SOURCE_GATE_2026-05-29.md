# Carver S09 Daily Price-Risk Source Gate

Date: 2026-05-29

Status:

```text
PROCESS_AND_SYNTHETIC_CODE_CARVER_S09_DAILY_PRICE_RISK_SOURCE_GATE_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Lock the S09 daily price-point risk conversion used to normalize EWMAC crossover forecasts.

This gate solves only the S09 conversion from a prevalidated annual percentage risk estimate into daily price units. It does not independently solve the upstream annual-risk estimate, long-run volatility source, cost/speed eligibility, buffering, position sizing, returns, diagnostics, or backtests.

## Source Anchors

S03 locks the shared volatility-estimation framing:

- EWMA span 32 days, lambda about 0.06061.
- Long-run/short-run volatility blend with weights 0.3 and 0.7.
- The blended estimate is the future reference standard-deviation estimate after S03.

Source: `Carver.pdf`, PDF page 97.

S07/S09 lock the EWMAC forecast normalization:

- EWMAC raw forecast divides the crossover by standard deviation in daily price units, not annualized percentage points.
- Daily price-point risk equals current price times annualized percentage risk divided by 16.

Source: `Carver.pdf`, PDF page 180.

S09 keeps the same risk-estimation family across trend speeds rather than using separate volatility spans per EWMAC speed.

Source: `Carver.pdf`, PDF pages 204-205.

## Locked Conversion

For S09 EWMAC forecast construction:

```text
daily_price_risk = current_price * annual_percentage_risk / 16
```

The code implements the same as:

```text
daily_price_risk = current_price * annual_percentage_risk / sqrt(256)
```

The annualization convention is locked to 256 trading days in this gate because the book's daily price-risk conversion uses division by 16.

## Implemented Surface

Code:

```text
src/carver/spine/s09.py
```

Public objects:

```text
S09DailyPriceRiskRequest
s09_daily_price_risk
```

The conversion fails closed if:

- lane class is not `SOURCE_NATIVE_FUTURES`;
- the completed bar is not a completed daily bar;
- the conversion source status is not `LOCKED`;
- annualization days differ from `256`;
- current price timestamp is not aligned to the completed bar;
- annual percentage risk timestamp is not aligned to the completed bar;
- current price is not finite and positive;
- annual percentage risk is not finite and positive.

## Remaining Upstream Block

This gate does not lock the actual annual percentage risk value for any instrument.

Future real-data S09 conformance must still supply a prevalidated annual percentage risk estimate whose own source gate proves:

- completed-bar-only inputs;
- no lookahead beyond the forecast timestamp;
- S03 EWMA/blend convention;
- long-run annual volatility source;
- missing/gap/invalid-price handling;
- first usable date after warm-up.

## Verification

```text
python -m unittest tests.test_s09_m2_synthetic -v
9 passed
```

Additional full-suite verification belongs to the broader portfolio-construction bridge goal.

## Non-Authorization

This artifact authorizes no data export, no market-row parsing, no new real-data run, no returns, no PnL, no Sharpe, no drawdown, no hit rate, no costs, no turnover, no diagnostics, no backtests, no OOS, no Lockbox, no Forward, no CFD adapter, no old QuantLab import, no tuning, no deployment, no trading, no promotion, and no remote push by inference.
