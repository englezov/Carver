# Carver NinjaTrader-Supported Pilot MES Tiny Historical-Bar Intake Shape Gate Draft

Date: 2026-05-30

Status:

```text
PROCESS_ONLY_CARVER_NINJATRADER_SUPPORTED_PILOT_MES_TINY_HISTORICAL_BAR_INTAKE_SHAPE_GATE_DRAFT_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Define the process boundary for a later tiny historical-bar intake gate using the statically locked MES dated contract.

This draft does not export NinjaTrader historical data, parse market rows, run diagnostics, run backtests, or authorize any trading lane.

## Inputs

Static MES lock:

```text
docs/process/CARVER_NINJATRADER_SUPPORTED_PILOT_MES_STATIC_DATED_CONTRACT_LOCK_2026-05-30.md
docs/researchops/first_data_intake/CARVER_NINJATRADER_SUPPORTED_PILOT_MES_STATIC_DATED_CONTRACT_LOCK_2026-05-30.csv
```

Completed-bar and holiday-precedence policy:

```text
docs/process/CARVER_NINJATRADER_SUPPORTED_PILOT_COMPLETED_BAR_HOLIDAY_PRECEDENCE_POLICY_DECISION_2026-05-30.md
docs/researchops/first_data_intake/CARVER_NINJATRADER_SUPPORTED_PILOT_TRADING_HOURS_ROW_POLICY_LEDGER_2026-05-30.csv
```

## Exact Row Set

The later intake gate, if separately authorized, must be limited to exactly one row:

```text
row_id: APPENDIX_C_174_006
author_market_code: MES
contract: MES 06-26
local_canonical_instrument_id: CARVER_APPENDIX_C_174_006_MES
lane_class: SOURCE_NATIVE_FUTURES
```

No other Appendix C row, adjacent symbol, continuous contract, CFD symbol, or substituted instrument may be included.

## Exact Completed Trading-Date Window

The only permitted completed trading-date window is:

```text
2026-05-18 through 2026-05-22 inclusive
```

The later intake gate must reject any row outside this completed trading-date window.

## Accepted Daily Bar Fields

The later intake gate may accept only the following source fields:

```text
provider_symbol
local_contract
timestamp_utc
open
high
low
close
volume
```

Optional metadata fields may be added only for provenance:

```text
source_file
source_file_sha256
imported_at_utc
row_number
```

The later intake gate must not compute returns, PnL, Sharpe, drawdown, volatility, diagnostics, forecast inputs, positions, or strategy signals.

## Timestamp Requirement

The later intake gate must require:

```text
UTC_END_OF_BAR_TIMESTAMP_ONLY
```

Every accepted row must have a timezone-aware UTC timestamp. Naive timestamps, local-only timestamps, intraday-incomplete timestamps, future-session timestamps, duplicate timestamps, and non-end-of-bar timestamps must fail closed.

## Completed Trading-Date Mapping

Canonical completed trading date:

```text
LOCAL_NINJATRADER_TEMPLATE_TRADINGDAY
```

The later intake gate must map each UTC end-of-bar timestamp through:

```text
Trading Hours template: CME US Index Futures ETH
Template timezone: Central Standard Time
Template evidence SHA256: 370B17F23EEEA694E686394B5FDB9B55681089C22D5232D5E6A354A314325620
```

The row is accepted only if the timestamp maps to exactly one extracted local template session and one local NinjaTrader `TradingDay`.

## Trading Hours And CME Conflict Policy

Operational filter:

```text
LOCAL_NINJATRADER_TEMPLATE_IS_OPERATIONAL_FILTER
```

Conflict check:

```text
CME_HOLIDAY_TRADING_HOURS_PAGE_IS_CONFLICT_CHECK
```

If local NinjaTrader Trading Hours evidence and CME static holiday/trading-hours evidence conflict for the selected row/date, the affected row/date must fail closed.

The later intake gate may not choose whichever source is more convenient after seeing data.

## Daily Close Policy

The close field is interpreted only as:

```text
NINJATRADER_PROVIDER_RECORDED_DAILY_BAR_CLOSE
```

Official CME settlement validation, correction, replacement, or reconciliation remains closed. If settlement reconciliation is ever desired, it requires a separate gate.

## Strict Fail-Closed Rules

The later intake gate must fail closed on:

- missing expected completed trading date;
- duplicate row for the same completed trading date;
- stale row;
- future row;
- non-monotonic row order;
- non-UTC timestamp;
- non-end-of-bar timestamp;
- timestamp outside the extracted local template session;
- timestamp mapping to zero or multiple local template sessions;
- CME/local holiday or early-close conflict;
- partial-holiday ambiguity;
- missing required OHLCV field;
- non-numeric OHLCV value;
- `high < low`;
- `open`, `high`, `low`, or `close` outside basic positive-price sanity;
- substituted symbol, substituted contract, continuous contract, merge/back-adjusted series, repaired row, imputation, forward-fill, or reweighting.

## Output Quarantine Path

Any later authorized intake output must be quarantined under:

```text
docs/researchops/first_data_intake/quarantine/MES_06_26_2026-05-18_2026-05-22/
```

Required quarantine outputs:

```text
raw_source_copy/
sanitized_bars/MES_06_26_DAILY_2026-05-18_2026-05-22.csv
provenance/MES_06_26_DAILY_2026-05-18_2026-05-22_PROVENANCE.md
```

The quarantine output is not a strategy dataset, not a diagnostic dataset, not a backtest dataset, and not promotion evidence.

## No-Diagnostics / No-Backtest Boundary

The later intake gate may only preserve and validate row shape, timestamps, provenance, and fail-closed completeness.

It must not compute:

- returns;
- PnL;
- volatility;
- Sharpe;
- drawdown;
- forecasts;
- positions;
- costs;
- carry;
- trend;
- diagnostics;
- backtests;
- OOS, Lockbox, or Forward evidence.

## Next Clean Gate

Selected next gate:

```text
NINJATRADER_SUPPORTED_PILOT_MES_TINY_HISTORICAL_BAR_INTAKE_EXECUTION_GATE
```

That gate would be the first gate allowed to export or ingest the tiny MES historical daily-bar rows, but only if separately authorized by the operator.

## Non-Authorization

This shape draft authorizes no code edits, no tests, no real market data, no market-row parsing, no NinjaTrader historical export, no provider API access, no diagnostics, no backtests, no returns, no PnL, no Sharpe, no drawdown, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old QuantLab pipeline use, no tuning, no deployment, no trading, no promotion, no remote push, and no GitHub action.
