# Carver Appendix C Contract Identity Readiness Shape Gate Draft

Date: 2026-05-29

Status:

```text
PROCESS_ONLY_CARVER_APPENDIX_C_CONTRACT_IDENTITY_READINESS_SHAPE_GATE_DRAFT_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Define the process-only boundary for resolving contract identity after the audited Appendix C NinjaTrader provider mapping execution artifact.

This draft does not resolve contract identity. It defines the evidence, fields, statuses, review rules, and fail-closed behavior required before any future contract identity execution gate may lock Appendix C rows for downstream readiness work.

## Current Inputs

Audited Appendix C source universe:

```text
docs/researchops/portfolios/CARVER_APPENDIX_C_JUMBO_UNIVERSE_LOCK_2026-05-29.csv
```

Static NinjaTrader instrument evidence:

```text
docs/researchops/provider_specs/NINJATRADER_STATIC_INSTRUMENT_MASTER_EXTRACT_2026-05-29.csv
```

Provider mapping artifact:

```text
docs/researchops/provider_mappings/CARVER_APPENDIX_C_NINJATRADER_SOURCE_NATIVE_PROVIDER_MAPPING_2026-05-29.csv
```

Provider mapping SHA-256:

```text
80c7f52fe599318fe6e095c7f6105b6b9646fc2f35dc1ccf821bcc2afe3586ce
```

Provider mapping hostile audit disposition:

```text
NO BLOCKING FINDINGS
AUDIT_DISPOSITION: PASS_PROCESS_SOURCE_PROVIDER_MAPPING_EXECUTION_SCOPE
```

## Current Provider Mapping State

The contract identity chapter starts from exactly 102 Appendix C rows:

```text
MAPPED_SOURCE_NATIVE_REQUIRES_REVIEW: 41
BLOCKED_UNAVAILABLE: 59
BLOCKED_CONTRACT_VARIANT_MISMATCH: 2
MAPPED_SOURCE_NATIVE_EXACT: 0
```

The 41 review-required rows are candidates only. They are not contract identity locks.

The 59 unavailable rows remain blocked unless a later gate introduces new static source-native evidence.

The 2 variant-mismatch rows remain blocked unless a later gate introduces exact source-native evidence that resolves the contradiction without substitution.

## What This Gate Draft Locks

This draft locks the shape of the contract identity readiness question:

- contract identity is separate from provider mapping;
- `MAPPED_SOURCE_NATIVE_REQUIRES_REVIEW` is not production readiness;
- every Appendix C source row remains represented;
- missing, blocked, unavailable, variant-mismatched, ambiguous, inactive, or insufficiently evidenced rows fail closed;
- local canonical IDs must be Carver-local and tied to Appendix C `row_id`;
- source-native futures identity must be resolved before sessions, rolls, completed-bar rules, risk, FX, costs, carry legs, diagnostics, backtests, deployment, trading, or promotion.

## What This Gate Draft Does Not Lock

This draft does not lock:

- production contract identity for any row;
- exchange equivalence;
- currency equivalence;
- multiplier semantics;
- tick value;
- point value;
- active tradability;
- delivery months or contract cycle;
- roll rules;
- back-adjustment rules;
- session calendars;
- completed-bar timestamps;
- FX sources;
- risk sources;
- costs;
- carry curve-leg availability;
- market data readiness.

## Future Contract Identity Artifact Fields

A future contract identity execution artifact must be machine-readable and preserve all source and provider mapping fields.

Minimum required fields:

- `row_id`;
- `appendix_table`;
- `source_group`;
- `descriptive_name`;
- `author_market_code`;
- `source_exchange`;
- `source_currency`;
- `source_multiplier`;
- `first_source_year`;
- `provider_name`;
- `provider_symbol`;
- `provider_exchange`;
- `provider_currency`;
- `provider_multiplier`;
- `provider_contract_family`;
- `provider_instrument_status`;
- `provider_mapping_status`;
- `provider_mapping_review_status`;
- `local_canonical_instrument_id`;
- `contract_identity_status`;
- `contract_identity_review_status`;
- `normalized_exchange`;
- `exchange_evidence_reference`;
- `normalized_currency`;
- `currency_evidence_reference`;
- `contract_family`;
- `contract_family_evidence_reference`;
- `contract_variant`;
- `variant_evidence_reference`;
- `multiplier_semantics`;
- `multiplier_value`;
- `multiplier_evidence_reference`;
- `point_value`;
- `tick_size`;
- `tick_value`;
- `tick_value_evidence_reference`;
- `active_status`;
- `active_status_evidence_reference`;
- `delivery_cycle_status`;
- `delivery_cycle_summary`;
- `delivery_cycle_evidence_reference`;
- `local_identity_block_reason`;
- `substitution_status`;
- `notes`.

## Allowed Contract Identity Status Values

Future rows must use one of:

```text
CONTRACT_IDENTITY_LOCKED_SOURCE_NATIVE
CONTRACT_IDENTITY_REQUIRES_REVIEW
CONTRACT_IDENTITY_BLOCKED_UNAVAILABLE
CONTRACT_IDENTITY_BLOCKED_AMBIGUOUS
CONTRACT_IDENTITY_BLOCKED_EXCHANGE_MISMATCH
CONTRACT_IDENTITY_BLOCKED_CURRENCY_MISMATCH
CONTRACT_IDENTITY_BLOCKED_MULTIPLIER_MISMATCH
CONTRACT_IDENTITY_BLOCKED_VARIANT_MISMATCH
CONTRACT_IDENTITY_BLOCKED_INACTIVE_OR_DELISTED
CONTRACT_IDENTITY_BLOCKED_PROVIDER_UNSUPPORTED
CONTRACT_IDENTITY_BLOCKED_INSUFFICIENT_EVIDENCE
```

Default before execution:

```text
CONTRACT_IDENTITY_REQUIRES_REVIEW
```

for mapped candidates, and the corresponding blocked status for rows already blocked by provider mapping.

## Evidence Requirements

Acceptable evidence for a future contract identity execution gate:

- audited Appendix C source universe row;
- clean Carver provider mapping artifact;
- clean NinjaTrader static instrument evidence extract;
- provider static contract specification page;
- exchange static contract specification page;
- manually reviewed source-native futures specification artifact;
- hash-bound static provider instrument master with relevant fields.

Forbidden as standalone authority:

- market rows;
- NinjaTrader historical export;
- chart labels;
- old QuantLab mapping files;
- old CFD adapter symbols;
- broker CFD symbol lists;
- copied market data folders;
- performance results;
- backtest outputs;
- informal memory;
- ticker guesses;
- provider API calls not separately authorized as static evidence access.

## Exchange Normalization Rules

A future execution gate must define a deterministic exchange-normalization table.

Examples requiring explicit treatment:

```text
ECBOT
CBOT
CME_CBT
GLOBEX
CME
NYMEX
COMEX
MONEP
SGX
DTB
```

Rules:

- source exchange and provider exchange may not be treated as equivalent by string similarity alone;
- exchange aliases require explicit evidence and a recorded equivalence rule;
- exchange mismatch fails closed unless an equivalence rule is locked;
- empty provider exchange fails to `CONTRACT_IDENTITY_REQUIRES_REVIEW` or blocked, depending on available evidence;
- exchange normalization does not open session or roll readiness.

## Currency Normalization Rules

The NinjaTrader static extract currently records raw currency codes such as:

```text
NINJATRADER_RAW_CURRENCY_CODE_7
```

A future execution gate must map raw provider currency codes to ISO-style currency labels only from static evidence.

Rules:

- raw currency code may not be guessed;
- source currency and provider currency must be explicitly normalized before a row can be locked;
- currency mismatch fails closed;
- FX source readiness remains a later gate.

## Multiplier And Value Semantics

Appendix C `source_multiplier`, NinjaTrader `point_value`, `tick_size`, and any provider or exchange `contract multiplier` may not be assumed to be the same field.

A future execution gate must define:

- source multiplier semantics;
- provider point-value semantics;
- contract unit size;
- tick size;
- tick value;
- whether source and provider units are compatible;
- whether apparent differences are true mismatches or unit-definition differences.

Rows with unresolved or contradictory value semantics must remain:

```text
CONTRACT_IDENTITY_REQUIRES_REVIEW
```

or fail closed as:

```text
CONTRACT_IDENTITY_BLOCKED_MULTIPLIER_MISMATCH
```

No row may be locked only because the provider symbol text matches the Appendix C code.

## Active Status And Availability

Future contract identity execution must distinguish:

- present in static provider master;
- server-supported in static provider master;
- active for current provider use;
- delisted;
- unavailable;
- unsupported;
- ambiguous.

`SERVER_SUPPORTED` in the provider mapping artifact is not enough by itself to declare production readiness.

Rows marked `BLOCKED_UNAVAILABLE` in provider mapping remain blocked unless new static source-native evidence is explicitly introduced.

Rows marked `BLOCKED_CONTRACT_VARIANT_MISMATCH` remain blocked unless new exact source-native evidence resolves the mismatch.

## Variant Rules

The following must remain distinct:

- micro;
- mini;
- e-mini;
- full-size;
- ultra;
- sector;
- swap;
- last-day;
- physical;
- financial;
- cross-currency;
- crypto;
- index future;
- option;
- spread;
- cash index;
- ETF;
- CFD.

The future gate must not substitute:

- full-size for micro;
- micro for full-size;
- mini for standard;
- different exchange contract for source contract;
- cash index for futures;
- ETF for futures;
- CFD for futures;
- option or spread for outright futures;
- nearby market because the Appendix C member is unavailable.

## Local Canonical ID Rules

Local canonical IDs must:

- be Carver-local;
- be tied to `row_id`;
- be deterministic;
- not be raw provider symbols;
- not be old QuantLab names;
- preserve source identity even when provider mapping is blocked;
- carry blocked status rather than disappearing.

Recommended shape:

```text
CARVER_APPENDIX_C_<table>_<row>_<author_market_code>
```

The existing provider mapping artifact already carries this style. A future contract identity execution gate may keep it if hostile audit confirms that it is stable and row-tied.

## Missing Or Blocked Member Policy

Default behavior remains:

```text
FAIL_CLOSED_NO_DROP_NO_SUBSTITUTE_NO_REWEIGHT
```

No Appendix C member may be dropped, substituted, or reweighted because it is unavailable, ambiguous, inactive, unsupported, or blocked.

If any member is blocked, the complete 102-member production universe remains incomplete for real-data portfolio work.

## Relationship To Later Gates

Contract identity/readiness must precede:

- session/roll/completed-bar readiness;
- risk, FX, cost, and carry-leg readiness;
- real-data Development/Reconciliation;
- diagnostics;
- backtests;
- OOS;
- Lockbox;
- Forward;
- deployment;
- trading;
- promotion.

This draft does not authorize any later gate.

## Audit Requirements

This draft should receive a lean regular hostile audit before being treated as locked.

Audit focus:

- the draft does not resolve contract identities;
- the draft does not mark rows production-ready;
- every Appendix C row remains in scope;
- provider mapping statuses are represented accurately;
- exchange, currency, multiplier, active status, variant, delivery cycle, and local ID requirements are fail-closed;
- blocked/unavailable rows are not dropped;
- market rows, NinjaTrader export, provider API access, diagnostics, backtests, CFD adapters, old QuantLab active-pipeline use, deployment, trading, promotion, Opus/GPT execution, and remote operations remain closed.

Regular hostile audit results should be preserved automatically as separate process-only audit-result records.

## Next Proposed Authorization

```text
Operator authorizes one process-only Carver Appendix C contract identity
execution/readiness gate using static source-native contract specification
evidence.

Scope:
Create a process/source contract identity artifact for the Appendix C rows
using only the audited provider mapping artifact and explicitly named static
contract specification evidence. Resolve or fail-close exchange normalization,
currency normalization, multiplier semantics, active status, contract family,
delivery cycle, local canonical IDs, and variant status before any market-row
access.

Allowed:
Read-only inspection of current Carver process artifacts, the Appendix C
universe lock, the NinjaTrader static instrument extract, the provider mapping
artifact, and explicitly named static contract specification evidence, plus
creation of contract identity process/source documentation or a machine-readable
contract identity artifact.

Forbidden:
No code edits, no tests, no real market data, no market-row parsing, no
NinjaTrader export, no provider API access unless separately specified as
static evidence access, no diagnostics, no backtests, no OOS, no Lockbox, no
Forward, no CFD adapters, no old QuantLab pipeline use, no tuning, no
deployment, no trading, no promotion, no silent substitution/drop/reweight, no
Opus/GPT execution, no remote operations.
```

## Non-Authorization

This shape gate draft authorizes no code edits, no tests, no real market data, no market-row parsing, no NinjaTrader historical export, no provider API access, no diagnostics, no backtests, no returns, no PnL, no Sharpe, no drawdown, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old QuantLab pipeline use, no tuning, no deployment, no trading, no promotion, no silent substitution/drop/reweight, no production contract identity lock, no market data readiness claim, no Opus/GPT execution, no remote push, and no GitHub action.
