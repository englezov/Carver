# Carver Appendix C Static Contract Specification Evidence Intake

Date: 2026-05-30

Status:

```text
PROCESS_SOURCE_CARVER_APPENDIX_C_STATIC_CONTRACT_SPECIFICATION_EVIDENCE_INTAKE_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Record a static official-source contract specification evidence intake for the 41 Appendix C rows currently marked:

```text
CONTRACT_IDENTITY_HARDENING_FAIL_CLOSED_EXTERNAL_SPEC_REQUIRED
```

This gate converts the prior contract specification source packet into a machine-readable evidence intake ledger. It extracts official static contract-spec fields where source material is sufficient and fails closed where venue, variant, active/retired status, delivery cycle, product-code, or quote-unit semantics still need a later source-hashed hardening pass.

This is not a production contract identity lock and not a real-data intake.

## Inputs

Contract specification source packet:

```text
docs/process/CARVER_APPENDIX_C_CONTRACT_SPECIFICATION_SOURCE_PACKET_2026-05-30.md
```

Contract identity static hardening artifact:

```text
docs/researchops/contract_identity/CARVER_APPENDIX_C_CONTRACT_IDENTITY_STATIC_HARDENING_2026-05-30.csv
SHA256: FC276F29599C27084F80E4EAFAD0E91BA7D138BEEA74E2C4C1F9FC0FED30708E
```

Official static source families inspected or identified:

- CME Group official contract specification pages;
- CME Group official static fact cards and PDFs;
- CME Group rulebook chapters or rulebook-linked PDFs where live product pages are insufficient;
- Euronext official CAC 40 Index Future contract specification page;
- SGX official GIFT Connect Nifty source page, with NSE IX source still required for final NIFTY lock;
- NinjaTrader static master as provider-side corroboration only, not official exchange authority.

No market rows, historical bars, NinjaTrader historical exports, provider APIs, old QuantLab artifacts, diagnostics, or backtests were used.

## Output

Machine-readable static evidence intake ledger:

```text
docs/researchops/contract_specs/CARVER_APPENDIX_C_STATIC_CONTRACT_SPEC_EVIDENCE_INTAKE_2026-05-30.csv
Rows: 41
SHA256: 908D9C147BABF839FF4475F4286BF9E7828921F274F2D1A4A7A4CB5C2B7EAD1D
```

## Evidence Status Counts

```text
STATIC_FIELDS_EXTRACTED_CONTRACT_IDENTITY_NOT_LOCKED: 12
STATIC_FIELDS_EXTRACTED_FAIL_CLOSED_QUOTE_UNIT_RECONCILIATION_REQUIRED: 8
STATIC_FIELDS_PARTIAL_EXTRACTED_FAIL_CLOSED_DELIVERY_CYCLE_REVIEW_REQUIRED: 6
STATIC_FIELDS_EXTRACTED_FAIL_CLOSED_PROVIDER_TICK_MISMATCH_REVIEW_REQUIRED: 3
STATIC_FIELDS_EXTRACTED_FAIL_CLOSED_EXCHANGE_LABEL_RECONCILIATION_REQUIRED: 3
STATIC_FIELDS_EXTRACTED_FAIL_CLOSED_SOURCE_NAME_RECONCILIATION_REQUIRED: 2
STATIC_FIELDS_EXTRACTED_FAIL_CLOSED_PRODUCT_CODE_RECONCILIATION_REQUIRED: 1
STATIC_FIELDS_EXTRACTED_FAIL_CLOSED_PROVIDER_EXCHANGE_TOKEN_MISSING: 1
STATIC_FIELDS_EXTRACTED_FAIL_CLOSED_PRODUCT_FAMILY_AND_QUOTE_UNIT_RECONCILIATION_REQUIRED: 1
STATIC_FIELDS_EXTRACTED_FAIL_CLOSED_RETIREMENT_TRANSITION_REVIEW_REQUIRED: 1
STATIC_FIELDS_EXTRACTED_FAIL_CLOSED_SOURCE_PROVIDER_VARIANT_RECONCILIATION_REQUIRED: 1
STATIC_FIELDS_EXTRACTED_FAIL_CLOSED_MULTIPLIER_AND_EXCHANGE_RECONCILIATION_REQUIRED: 1
STATIC_FIELDS_EXTRACTED_FAIL_CLOSED_ACTIVE_RETIREMENT_AND_RULEBOOK_REVIEW_REQUIRED: 1
```

Boundary status:

```text
NO_MARKET_ROW_ACCESS: 41
provider_api_accessed NO: 41
ninjatrader_historical_export_used NO: 41
production_contract_identity_lock_status NOT_LOCKED: 41
```

## Interpretation

The evidence intake materially improves the 41-row contract identity hardening surface:

- it names official static source targets for all 41 rows;
- it extracts official static contract unit, quote-unit, tick, venue, and product-family evidence where the official source material is clear enough for this process/source stage;
- it identifies rows where current NinjaTrader static fields are corroborated but not production locks;
- it identifies rows where the official source and the provider static extract conflict or require special interpretation;
- it keeps every row fail-closed for production contract identity until a later hardening gate explicitly locks or rejects the row.

The important blockers after this intake are:

```text
N1U: active/retired and rulebook review required.
GE: Eurodollar retirement/transition review required.
Z3N, NOK, SEK: official static tick value conflicts with the current NinjaTrader static extract.
NIFTY: SGX/GIFT/NSE IX/local provider variant reconciliation required.
SI: Appendix C multiplier conflicts with full Silver futures official/provider semantics.
HG, MGC, CAC40: source exchange label needs official venue normalization.
ZB, HO: source descriptive name needs current official product-name reconciliation.
HH: product-code/rulebook chapter ambiguity remains.
QG: provider exchange token is missing.
Agriculture and livestock quote-unit rows: source multiplier and provider point value reconcile only through official quote-unit semantics and still need final source-hashed lock.
Rows with partial delivery-cycle extraction: delivery cycle remains fail-closed until the exact static source section is locked.
```

## Relationship To Contract Identity Hardening

This intake is an upstream evidence artifact for a later contract identity hardening pass. It does not itself change the current contract identity status ledger:

```text
CONTRACT_IDENTITY_BLOCKED_UNAVAILABLE: 59
CONTRACT_IDENTITY_REQUIRES_REVIEW: 41
CONTRACT_IDENTITY_BLOCKED_VARIANT_MISMATCH: 2
CONTRACT_IDENTITY_LOCKED_SOURCE_NATIVE: 0
```

The next clean gate is a static contract identity hardening pass using:

```text
docs/researchops/contract_identity/CARVER_APPENDIX_C_CONTRACT_IDENTITY_STATIC_HARDENING_2026-05-30.csv
docs/researchops/contract_specs/CARVER_APPENDIX_C_STATIC_CONTRACT_SPEC_EVIDENCE_INTAKE_2026-05-30.csv
```

That next pass should resolve or fail-close the 41 rows without touching market data. Only after that pass can session/roll/completed-bar readiness be revisited.

## Not Ready For Data Intake

This gate does not make any row ready for NinjaTrader historical-bar intake because:

- no production contract identity lock was issued;
- delivery cycles remain unlocked or source-hash pending for many rows;
- completed-bar policy remains blocked;
- roll and back-adjustment policy remain blocked;
- risk, FX, costs, trend/carry eligibility, and carry curve-leg evidence remain blocked downstream;
- no real market rows were inspected.

## Non-Authorization

This record authorizes no code edits, no tests, no real market data, no market-row parsing, no NinjaTrader historical export, no provider API access, no diagnostics, no backtests, no returns, no PnL, no Sharpe, no drawdown, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old QuantLab pipeline use, no tuning, no deployment, no trading, no promotion, no remote push, and no GitHub action.
