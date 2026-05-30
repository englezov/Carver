# Carver Databento Appendix C Session Roll Provider Condition Data Intake Shape Gate

Date: 2026-05-30

Status:

```text
PROCESS_ONLY_DATABENTO_APPENDIX_C_66_ROW_INTAKE_SHAPE_GATE_NOT_DATA_AUTHORIZATION
```

## Purpose

Define the next clean shape for a future Databento Appendix C OHLCV intake after contract identity hardening.

This gate is process-only. It does not authorize a Databento request, OHLCV download, market-row parsing, diagnostics, backtests, forecasts, positions, costs, carry, trend, risk calculations, or strategy use.

## Eligible Static Row Set

Input ledger:

```text
docs/researchops/contract_identity/databento_appendix_c_contract_identity_hardening_2026-05-30/ledger/CARVER_DATABENTO_APPENDIX_C_CONTRACT_IDENTITY_HARDENED_LEDGER_2026-05-30.csv
```

Eligible rows:

```text
eligible_for_session_roll_provider_condition_data_intake_shape_gate == YES
```

Count:

```text
66
```

Closed rows:

```text
PRESERVED_NON_CANDIDATE_FAIL_CLOSED_ROWS: 33
HARDENING_FAIL_CLOSED_ROWS: 3
```

Closed rows may not be silently dropped, substituted, or reweighted. They remain excluded from any future request unless a separate static provider evidence gate resolves them.

## Future Intake Manifest Requirements

A later execution gate must create a request manifest with one row per eligible static contract:

- Appendix C `row_id`.
- Appendix C descriptive name.
- author market code.
- Databento dataset.
- Databento continuous symbol used for selection.
- Databento selected dated raw symbol.
- Databento selected instrument ID.
- provider exchange.
- currency.
- maturity year/month/day.
- activation and expiration where available.
- source of any hardening correction.
- fail-closed exclusion reason for all non-eligible rows.

## Session And Timestamp Requirements

Before OHLCV intake, the future gate must define:

- daily `ohlcv-1d` timestamp interpretation;
- completed trading-date derivation;
- timezone policy;
- holiday and partial-holiday handling;
- stale/missing/duplicate row behavior;
- provider condition metadata join policy;
- conflict handling between provider timestamps and exchange/session rules.

No row may be promoted if completed-date mapping is ambiguous.

## Roll And Lifecycle Requirements

For dated-contract archive intake:

- individual dated contracts are source lineage authority;
- Databento continuous symbols are only selection evidence;
- provider-built continuous series are not source authority;
- any local continuous construction must be separately gated;
- roll-boundary rows must be labeled and quarantined if provider metadata indicates ambiguity;
- expiration, delivery, cash-settlement, first-notice, and lifecycle blockers must be preserved as explicit fields where available.

## Provider Condition Requirements

A future OHLCV execution gate must also request or load Databento provider-condition metadata for the exact request window and join condition labels row/date-wise.

Rows with normal provider condition may proceed only at quarantine scope. Rows with degraded, warning, missing, ambiguous, partial, or unusable condition metadata must be quarantined or fail-closed under explicit labels.

## Quarantine Layout

The future execution gate should write under a new locked root, for example:

```text
docs/researchops/source_native_futures_daily_data_library/APPENDIX_C_DATABENTO_66_ROW_DATED_CONTRACT_DAILY_ARCHIVE/
```

Expected subfolders:

```text
request_manifest/
raw_provider_metadata/
raw_provider_output/
definition_metadata/
provider_condition_metadata/
sanitized_bars/
validation/
provenance/
```

## Sanitized Schema

Any future sanitized OHLCV file must include:

- `row_id`
- `author_market_code`
- `descriptive_name`
- `provider`
- `dataset`
- `schema`
- `source_contract_identity`
- `databento_continuous_symbol`
- `databento_raw_symbol`
- `databento_instrument_id`
- `completed_trading_date`
- `provider_timestamp_utc`
- `open`
- `high`
- `low`
- `close`
- `volume`
- `provider_condition_readiness_status`
- `validation_status`
- `strategy_use_status`

`strategy_use_status` must remain:

```text
NOT_STRATEGY_INPUT_NOT_BACKTEST_READY
```

until a separate promotion gate authorizes otherwise.

## Future Execution Boundary

A later execution gate may request OHLCV only if it explicitly names:

- exact eligible row set;
- exact dataset list;
- exact schema;
- exact dated raw symbols or instrument IDs;
- exact date window;
- exact output root;
- exact provider condition metadata policy;
- exact fail-closed behavior.

## Non-Authorization

This shape gate authorizes no provider API call, no OHLCV download, no market-row parsing, no diagnostics, no backtests, no forecasts, no positions, no costs, no carry, no trend, no risk calculations, no OOS, no Lockbox, no Forward, no CFD adapters, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git operations, and no remote repository operations.
