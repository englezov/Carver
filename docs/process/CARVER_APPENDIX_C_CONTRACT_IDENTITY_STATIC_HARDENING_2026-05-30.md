# Carver Appendix C Contract Identity Static Hardening

Date: 2026-05-30

Status:

```text
PROCESS_SOURCE_CARVER_APPENDIX_C_CONTRACT_IDENTITY_STATIC_HARDENING_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Record the contract-identity hardening result for the 41 Appendix C rows currently marked:

```text
CONTRACT_IDENTITY_REQUIRES_REVIEW
```

This gate uses only current Carver static artifacts because no external static source/provider/exchange contract specification files or pages were named in the authorization.

## Inputs

Current contract identity artifact:

```text
docs/researchops/contract_identity/CARVER_APPENDIX_C_CONTRACT_IDENTITY_STATUS_2026-05-29.csv
```

Static contract-spec evidence intake:

```text
docs/researchops/contract_specs/CARVER_APPENDIX_C_STATIC_CONTRACT_SPEC_EVIDENCE_INTAKE_2026-05-29.csv
```

NinjaTrader static instrument master extract:

```text
docs/researchops/provider_specs/NINJATRADER_STATIC_INSTRUMENT_MASTER_EXTRACT_2026-05-29.csv
```

No market rows, NinjaTrader historical exports, provider APIs, old QuantLab artifacts, diagnostics, or backtests were used.

## Output

Machine-readable hardening artifact:

```text
docs/researchops/contract_identity/CARVER_APPENDIX_C_CONTRACT_IDENTITY_STATIC_HARDENING_2026-05-30.csv
Rows: 41
SHA256: FC276F29599C27084F80E4EAFAD0E91BA7D138BEEA74E2C4C1F9FC0FED30708E
```

## Result

Hardening status:

```text
CONTRACT_IDENTITY_HARDENING_FAIL_CLOSED_EXTERNAL_SPEC_REQUIRED: 41
```

Multiplier numeric comparison:

```text
YES_SOURCE_MULTIPLIER_EQUALS_PROVIDER_POINT_VALUE: 30
NO_SOURCE_MULTIPLIER_DIFFERS_FROM_PROVIDER_POINT_VALUE: 11
```

Provider exchange-token status:

```text
PROVIDER_EXCHANGE_TOKENS_PRESENT_NOT_NORMALIZED: 37
PROVIDER_EXCHANGE_TOKENS_MISSING_REQUIRES_EXTERNAL_SPEC: 4
```

Boundary checks:

```text
NO_MARKET_ROW_ACCESS: 41
provider_api_accessed NO: 41
ninjatrader_export_used NO: 41
production_contract_identity_lock_status NOT_LOCKED: 41
```

## Interpretation

The current Carver static artifacts preserve useful candidate evidence:

- source descriptive name and author market code;
- source exchange, currency, and multiplier;
- NinjaTrader candidate symbol;
- provider exchange tokens where available;
- raw provider currency code;
- provider point value, tick size, and tick value where available;
- provider contract-family text;
- provider server-supported/static-master flag where available.

However, this evidence is not enough to lock production contract identity.

The hardening gate therefore fails closed for all 41 review-required rows because the following atoms remain unresolved:

- exchange normalization;
- provider raw currency-code mapping;
- source multiplier versus provider point-value semantics;
- active tradability status;
- delivery cycle;
- external source/provider/exchange contract-spec evidence.

The 11 rows where source multiplier differs numerically from provider point value are not classified as production mismatches by this gate. They are marked as unresolved because some futures quote units require source-specific multiplier semantics. They require external contract specification evidence before they can be locked or rejected.

## Required Next Evidence

A future hardening pass needs explicit static contract specification evidence for each candidate family, preferably from official exchange or provider contract specification pages/PDFs.

Minimum required static evidence:

- exchange and venue identity;
- currency;
- point value or contract unit;
- tick size;
- tick value;
- contract family;
- micro/mini/full/last-day/financial/physical variant;
- delivery cycle or listed contract months;
- active/listed status;
- official symbol or product code;
- source date or retrieval/provenance marker.

## Relationship To First Data Intake

No row is ready for session/roll/completed-bar hardening, risk/FX/cost/carry-leg hardening, or NinjaTrader historical-bar intake based on this pass.

The next clean step is to supply explicit static contract specification evidence for the 41 candidates, then rerun a contract identity hardening pass that can lock or reject rows without touching market data.

## Non-Authorization

This record authorizes no code edits, no tests, no real market data, no market-row parsing, no NinjaTrader historical export, no provider API access, no diagnostics, no backtests, no returns, no PnL, no Sharpe, no drawdown, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old QuantLab pipeline use, no tuning, no deployment, no trading, no promotion, no remote push, and no GitHub action.
