# Carver S26 ZN Hourly Sigma-Percent Source Gate

Date: 2026-05-30

Status:

```text
PROCESS_ONLY_CARVER_S26_ZN_HOURLY_SIGMA_PERCENT_SOURCE_GATE_NOT_DATA_NOT_FORECAST
```

## Purpose

Lock the source method for the `sigma_percent_t` input required by the S26 ZN hourly forecast-only bridge.

This source gate does not compute a real risk estimate, ingest Databento data, parse market rows, run diagnostics, run backtests, compute positions, compute costs, compute carry, compute trend, run S27, deploy, trade, promote, or open Git operations.

## Source Anchors

S26 risk adjustment:

```text
00_Carver.pdf p. 480
```

Locked atoms:

- S26 divides the raw mean-reversion forecast by daily standard deviation of price returns.
- That daily price-risk value can be calculated directly from price differences or derived from annual percentage volatility `sigma_percent_t`.
- The derivation from annual percentage volatility is:

```text
sigma_price_t = price_t * sigma_percent_t / 16
```

Shared Part One price-risk conversion:

```text
00_Carver.pdf p. 72
```

Locked atom:

```text
daily price risk in points = current price * annual percentage risk / 16
```

Shared Part One variable-risk estimate family:

```text
00_Carver.pdf pp. 95-97
docs/process/CARVER_S09_DAILY_PRICE_RISK_SOURCE_GATE_2026-05-29.md
```

Locked atoms:

- Annual percentage risk `sigma_percent_t` is an annualized standard deviation of percentage returns.
- If estimating `sigma_percent_t`, use percentage returns and annualize by multiplying the daily estimate by 16.
- The current-risk estimate uses an exponentially weighted standard deviation.
- The short-run EWMA standard-deviation span is 32 days, equivalent to lambda about 0.06061.
- Carver's future reference estimate blends long-run and short-run volatility with weights 0.3 and 0.7 respectively.

## Locked S26 Bridge Policy

For the first S26 ZN hourly bridge:

```text
S26_SIGMA_PERCENT_SOURCE_METHOD: LOCKED_TO_PART_ONE_S03_VARIABLE_RISK_FAMILY
S26_SIGMA_PRICE_CONVERSION: LOCKED_TO_PRICE_TIMES_SIGMA_PERCENT_DIVIDED_BY_16
S26_SIGMA_VALUE_SOURCE: PREVALIDATED_INPUT_REQUIRED
```

The tiny hourly intake gate must not estimate `sigma_percent_t` from the five-day hourly window.

The forecast-only handoff may consume `sigma_percent_t` only if a separate prevalidated risk artifact proves:

- `SOURCE_NATIVE_FUTURES` lane;
- ZN / `APPENDIX_C_172_004` / `42000661` / `ZNM6` identity alignment;
- completed-bar-only source data;
- no lookahead beyond the forecast timestamp;
- annualized percentage-return volatility, not daily OHLCV row count or intraday noise proxy;
- Part One S03 EWMA/blended volatility family or a separately source-justified equivalent;
- timestamp alignment to the S26 forecast output row;
- finite positive value;
- no tuning after seeing S26 forecast output.

## Direct Daily Price-Risk Alternative

S26 p. 480 permits daily standard deviation of price returns to be calculated directly.

That alternative remains closed for this first bridge because the active goal is to feed quarantined hourly ZN bars into a forecast-only surface. A direct daily price-difference risk estimate requires a separate daily/continuous ZN risk-source artifact and cannot be inferred from the five-day hourly intake.

## Current Readiness

```text
SIGMA_PERCENT_METHOD_LOCK: PASS_SOURCE_METHOD_LOCKED
SIGMA_PERCENT_RUNTIME_VALUE: NOT_AVAILABLE_REQUIRES_PREVALIDATED_RISK_ARTIFACT
FORECAST_ONLY_EXECUTION: BLOCKED_UNTIL_HOURLY_INTAKE_AND_PREVALIDATED_SIGMA_VALUE_EXIST
```

## Non-Authorization

This gate authorizes no Databento access, no data download, no market-row parsing, no real-data risk estimation, no real-data forecast computation, no diagnostics, no backtests, no positions, no costs, no carry, no trend computation, no S27 overlay, no volatility/risk calculations on live/provider data, no OOS, no Lockbox, no Forward, no CFD adapters, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.
