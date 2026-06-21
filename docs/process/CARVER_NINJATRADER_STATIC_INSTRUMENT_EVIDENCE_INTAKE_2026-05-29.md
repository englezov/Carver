# Carver NinjaTrader Static Instrument Evidence Intake

Date: 2026-05-29

Status:

```text
PROCESS_ONLY_CARVER_NINJATRADER_STATIC_INSTRUMENT_EVIDENCE_INTAKE_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Record a process-only intake of NinjaTrader static instrument-definition evidence for future Appendix C source-native provider mapping.

This artifact does not perform Appendix C provider mapping. It records the evidence source and the sanitized extract created from it.

## Authorized Static Evidence Source

```text
C:\Users\openclaw\Documents\NinjaTrader 8\db\NinjaTrader.sqlite
```

The database was inspected read-only as static instrument-definition evidence only.

## Sanitized Extract

Output artifact:

```text
docs/researchops/provider_specs/NINJATRADER_STATIC_INSTRUMENT_MASTER_EXTRACT_2026-05-29.csv
```

SHA-256:

```text
e297cb93a876e1643cab7b54c9619dca1c9ff02654c19a791a91cb800dda9af8
```

Row count:

```text
264
```

The extract contains only NinjaTrader `MasterInstruments` rows with:

```text
InstrumentType = 0
```

The local intake labels these rows as:

```text
FUTURE
```

## Extracted Fields

The sanitized CSV records:

- static extract status;
- static source database path;
- NinjaTrader master instrument id;
- NinjaTrader master instrument name;
- NinjaTrader description;
- raw instrument type code;
- local extract label for the instrument type;
- raw NinjaTrader currency code;
- point value;
- tick size;
- trading-hours template name;
- server-supported flag;
- size of the static instrument user-data blob;
- sanitized symbol-mapping-style tokens extracted from the static instrument user-data blob;
- explicit flags that no market rows, account/order/execution fields, or provider API access were included.

## Schema Discovery Boundary

SQLite schema discovery found relevant static instrument tables:

```text
MasterInstruments
Instruments
InstrumentLists
Instrument2InstrumentList
```

The extract used only `MasterInstruments` for this intake.

The following tables were not read for extract rows and are not part of this evidence artifact:

```text
Accounts
AccountItems
Executions
JournalEntries
Logs
OrderUpdates
Orders
Positions
Strategies
Strategy2Account
Strategy2Execution
Strategy2Instrument
Strategy2Order
User2Account
User2MarketDataEntitlement
Users
Versions
```

## Mapping Boundary

This evidence intake does not classify any Appendix C row as mapped.

Every future Appendix C mapping decision must still be made in a separate provider mapping execution gate using the audited Appendix C universe lock and this static evidence extract.

Allowed future statuses remain:

```text
UNRESOLVED
MAPPED_SOURCE_NATIVE_EXACT
MAPPED_SOURCE_NATIVE_REQUIRES_REVIEW
BLOCKED_UNAVAILABLE
BLOCKED_AMBIGUOUS
BLOCKED_MULTIPLIER_MISMATCH
BLOCKED_EXCHANGE_MISMATCH
BLOCKED_CURRENCY_MISMATCH
BLOCKED_CONTRACT_VARIANT_MISMATCH
BLOCKED_INACTIVE_OR_DELISTED
BLOCKED_PROVIDER_UNSUPPORTED
```

## Non-Authorization

This evidence intake authorizes no code edits, no tests, no real market data, no market-row parsing, no NinjaTrader historical export, no provider API access, no diagnostics, no backtests, no returns, no PnL, no Sharpe, no drawdown, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old QuantLab pipeline use, no tuning, no deployment, no trading, no promotion, no Appendix C provider mapping execution, no production data readiness claim, no Opus/GPT execution, no remote push, and no GitHub action.

## Next Clean Gate

The next clean gate may be:

```text
APPENDIX_C_SOURCE_NATIVE_PROVIDER_MAPPING_EXECUTION_GATE
```

That gate should consume:

```text
docs/researchops/portfolios/CARVER_APPENDIX_C_JUMBO_UNIVERSE_LOCK_2026-05-29.csv
docs/researchops/provider_specs/NINJATRADER_STATIC_INSTRUMENT_MASTER_EXTRACT_2026-05-29.csv
```

It must not touch market rows.
