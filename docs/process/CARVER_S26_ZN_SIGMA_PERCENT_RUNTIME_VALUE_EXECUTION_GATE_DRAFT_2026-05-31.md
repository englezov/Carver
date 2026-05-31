# Carver S26 ZN Sigma-Percent Runtime Value Execution Gate Draft

Date: 2026-05-31

Status:

```text
PROCESS_ONLY_EXECUTION_GATE_DRAFT_PREVALIDATED_S26_ZN_SIGMA_PERCENT_RUNTIME_VALUE_NOT_AUTHORIZATION
```

## Purpose

Define the exact next gate needed before G_R1B can emit S26 forecast output from the quarantined ZN hourly bars.

G_R1A produced valid hourly prices. S26 still requires:

```text
sigma_price_t = price_t * sigma_percent_t / 16
```

The `sigma_percent_t` runtime value must be prevalidated before the S26 forecast-only handoff.

## Gate Name

```text
PREVALIDATED_S26_ZN_SIGMA_PERCENT_RUNTIME_VALUE
```

## Source Method

Locked source method:

```text
LOCKED_TO_PART_ONE_S03_VARIABLE_RISK_FAMILY
```

Source anchors:

```text
00_Carver.pdf p. 480: S26 risk-adjusts raw forecast by daily standard deviation of price returns.
00_Carver.pdf p. 72: daily price risk in points = current price * annual percentage risk / 16.
00_Carver.pdf pp. 95-97: annual percentage risk is annualized standard deviation of percentage returns; variable risk uses EWMA/current risk and long/short blend.
docs/process/CARVER_S26_ZN_HOURLY_SIGMA_PERCENT_SOURCE_GATE_2026-05-30.md
```

## Required Runtime Artifact

The execution must create one machine-readable runtime record for the final G_R1A completed hourly bar:

```text
as_of: 2026-05-22T21:00:00Z
row_id: APPENDIX_C_172_004
author_market_code: ZN
instrument_id: 42000661
raw_symbol: ZNM6
value_field: sigma_percent_t
runtime_status: PREVALIDATED_S26_ZN_SIGMA_PERCENT_RUNTIME_VALUE
method_status: LOCKED_TO_PART_ONE_S03_VARIABLE_RISK_FAMILY
no_lookahead_status: PASS_NO_LOOKAHEAD
source_window_status: PASS_SOURCE_WINDOW_PREVALIDATED
```

The timestamp is the last completed hourly bar in the G_R1A quarantine slice:

```text
provider_ts_event_start_utc: 2026-05-22T20:00:00Z
derived_completed_bar_end_utc: 2026-05-22T21:00:00Z
```

## Allowed Source Evidence For A Future Execution

A future execution may use one of:

1. A current Carver source-native completed-daily ZN/ZNM6 risk artifact that already proves no-lookahead and source identity.
2. A separately authorized source-native daily ZN/ZNM6 data/risk gate that computes only `sigma_percent_t` and no forecast/diagnostic/backtest/position output.

The five-day G_R1A hourly intake may be used only as the forecast price input, not as the volatility-estimation sample.

## Fail-Closed Rules

Fail closed if:

- source identity is not `APPENDIX_C_172_004 / ZN / 42000661 / ZNM6`;
- the value is missing, non-finite, zero, or negative;
- the value is estimated from the five-day hourly G_R1A sample;
- the value uses future rows after `2026-05-22T21:00:00Z`;
- completed-bar-only evidence is not proven;
- the method is not the Part One S03 variable-risk family or separately source-locked equivalent;
- the source artifact SHA is missing;
- the output is used for diagnostics, backtests, positions, costs, carry, trend, S27, OOS, Lockbox, Forward, deployment, trading, or promotion.

## Next Gate After Pass

If this runtime value passes, the next gate is:

```text
G_R1B_ZN_S26_HOURLY_SIGMA_PERCENT_AND_FORECAST_ONLY_HANDOFF
```

That gate may consume:

- G_R1A quarantined hourly ZN bars;
- this prevalidated runtime sigma record;
- the already implemented forecast-only handoff function.

It may emit only S26 forecast fields and no diagnostics/backtests/positions.

## Non-Authorization

This draft authorizes no provider API access, no data download, no market-row parsing, no real-data volatility/risk calculation, no real-data forecast computation, no diagnostics, no backtests, no positions, no costs, no carry, no trend computation, no S27 overlay, no OOS, no Lockbox, no Forward, no CFD adapters, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.
