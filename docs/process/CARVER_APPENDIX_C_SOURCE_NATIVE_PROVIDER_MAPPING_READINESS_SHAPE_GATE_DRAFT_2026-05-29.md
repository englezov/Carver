# Carver Appendix C Source-Native Provider Mapping Readiness Shape Gate Draft

Date: 2026-05-29

Status:

```text
PROCESS_ONLY_CARVER_APPENDIX_C_SOURCE_NATIVE_PROVIDER_MAPPING_READINESS_SHAPE_GATE_DRAFT_NOT_DATA_NOT_MAPPING_EXECUTION
```

## Purpose

Define the rules and evidence required before any provider mapping can be executed from the audited Appendix C machine-readable 102-row source universe.

This is a process-only readiness-shape draft. It does not perform provider mapping, access provider APIs, inspect local market rows, export NinjaTrader data, run diagnostics, run backtests, implement code, or authorize trading.

## Inputs Inspected

Required Carver guardrails:

```text
README.md
docs/mission/CARVER_SOURCE_NATIVE_RESEARCH_CHARTER_2026-05-28.md
docs/process/CLEAN_WORKSPACE_MIGRATION_RECORD_2026-05-28.md
docs/process/LANE_CLASSIFICATION_AND_ADAPTER_QUARANTINE_RULES_2026-05-28.md
```

Appendix C machine-readable universe lock:

```text
docs/researchops/portfolios/CARVER_APPENDIX_C_JUMBO_UNIVERSE_LOCK_2026-05-29.csv
docs/process/CARVER_APPENDIX_C_MACHINE_READABLE_UNIVERSE_LOCK_2026-05-29.md
docs/process/CARVER_APPENDIX_C_MACHINE_READABLE_UNIVERSE_LOCK_HOSTILE_AUDIT_RESULT_2026-05-29.md
docs/process/CARVER_POST_APPENDIX_C_MACHINE_READABLE_UNIVERSE_LOCK_NEXT_STEP_DECISION_2026-05-29.md
```

## Current Locked Source Input

The provider mapping readiness chapter must consume exactly this source input:

```text
docs/researchops/portfolios/CARVER_APPENDIX_C_JUMBO_UNIVERSE_LOCK_2026-05-29.csv
```

Current source-universe hash:

```text
9453a9635148ae4d998306e0ac921c534d35d4d97dde3934c8aea02104e48c5f
```

Known source-universe shape:

```text
ROWS 102
TABLES 172-183
LANE SOURCE_NATIVE_FUTURES
PROVIDER_MAPPING_STATUS UNRESOLVED
LOCAL_CONTRACT_IDENTITY_STATUS UNRESOLVED
MARKET_DATA_READINESS_STATUS CLOSED
SUBSTITUTION_POLICY FAIL_CLOSED_NO_DROP_NO_SUBSTITUTE_NO_REWEIGHT
PRODUCTION_USE_STATUS NOT_AUTHORIZED
```

## Gate Decision

The next clean readiness gate after the machine-readable source-universe lock is:

```text
APPENDIX_C_SOURCE_NATIVE_PROVIDER_MAPPING_READINESS_SHAPE_GATE_DRAFT
```

This draft defines what must be true before a later provider mapping execution gate may begin.

It does not map any provider symbols.

## Provider Mapping Is A Separate Readiness Family

Appendix C source universe identity is now locked at process/source scope. Provider mapping remains unresolved.

Provider mapping must be treated as a separate readiness family because the book source explicitly warns that author broker market codes may vary across brokers and may differ from official exchange codes.

Therefore:

- `author_market_code` is a source field, not a provider symbol;
- `exchange` is a source field, not proof of local exchange availability;
- `multiplier` is a source field, not proof of local contract equivalence;
- `currency` is a source field, not proof of local quote convention;
- `first_source_year` is a source dataset field, not proof of local history availability.

## Required Future Mapping Artifact Fields

A future provider mapping execution artifact must be machine-readable and must preserve the original source row fields.

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
- `local_canonical_instrument_id`;
- `provider_name`;
- `provider_symbol`;
- `provider_exchange`;
- `provider_currency`;
- `provider_multiplier`;
- `provider_contract_family`;
- `provider_instrument_status`;
- `mapping_status`;
- `mapping_evidence_type`;
- `mapping_evidence_reference`;
- `mapping_review_status`;
- `substitution_status`;
- `failure_reason`;
- `notes`;

Allowed `mapping_status` values:

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

The default for every row must remain:

```text
UNRESOLVED
```

until an explicit later mapping execution gate is authorized.

## Local Canonical ID Policy

Future local canonical IDs must be Carver-local identifiers, not raw provider symbols.

Required properties:

- deterministic;
- stable across providers;
- tied to `row_id`;
- source-native futures only;
- no CFD identifiers;
- no ETF/cash-index/proxy identifiers;
- no old QuantLab symbol names as default authority;
- explicit if a local id is pending or blocked.

Recommended future shape:

```text
CARVER_<asset_family>_<source_or_contract_descriptor>
```

This draft does not create local canonical IDs.

## Exactness Rules

Future mapping execution must check, at minimum:

- descriptive instrument match;
- source-native futures contract family;
- exchange or explicitly accepted source-native equivalent;
- currency;
- multiplier;
- contract variant;
- active/inactive status;
- local availability;
- provider symbol provenance;
- ambiguity across nearby instruments.

Any mismatch must fail closed unless separately escalated and locked.

## Micro, Mini, Full, And Variant Handling

Micro, mini, e-mini, full-size, ultra, sector, swap, last-day, cross-currency, and crypto variants must be treated as distinct source identities.

Examples from the locked universe include:

- `S&P 500 (micro)` / `MES`;
- `Dow Jones industrial (micro)` / `MYM`;
- `Nasdaq (micro)` / `MNQ`;
- `WTI Crude (mini)` / `QM`;
- `Henry Hub Gas (mini)` / `QG`;
- `Gold (micro)` / `MGC`;
- `10-year Ultra US` / `TN`;
- `Brent Crude last day` / `BZ`.

A future mapping gate must not substitute:

- full-size for micro;
- micro for full-size;
- mini for standard;
- cash index for futures;
- ETF for futures;
- CFD for futures;
- different exchange contract for source contract;
- continuous symbol for discrete source identity;
- nearby market because the source member is missing.

## Unresolved, Ambiguous, Or Unavailable Members

Default behavior:

```text
FAIL_CLOSED_NO_DROP_NO_SUBSTITUTE_NO_REWEIGHT
```

This applies to:

- no provider symbol found;
- multiple plausible provider symbols found;
- exchange mismatch;
- currency mismatch;
- multiplier mismatch;
- inactive or delisted provider instrument;
- insufficient evidence;
- provider symbol found only as CFD;
- provider symbol found only as cash, ETF, spread, option, or synthetic proxy;
- provider symbol found only as a different contract variant.

The future mapping execution artifact must record the row as blocked or unresolved. It must not drop the row, substitute a nearby contract, or reweight the portfolio.

## Evidence Requirements

A future mapping execution gate must define acceptable evidence before use.

Potential evidence types:

- provider instrument master export;
- provider contract specification page;
- exchange contract specification page;
- broker/platform instrument metadata export;
- manually reviewed source-native futures spec artifact.

Forbidden as standalone authority:

- old QuantLab mapping files;
- old CFD adapter symbols;
- old NinjaTrader exports not reintroduced through a clean Carver artifact;
- copied market data folders;
- chart labels;
- informal memory;
- performance results;
- backtest outputs;
- broker CFD symbol lists;
- convenience ticker guesses.

## Provider Mapping Execution Gate Requirements

A later provider mapping execution gate must explicitly state:

- provider(s) to inspect;
- allowed evidence source(s);
- whether provider APIs, local instrument masters, screenshots, or static spec files may be inspected;
- whether any generated machine-readable mapping file may be created;
- how failed rows are represented;
- whether a lean hostile audit is required before any data readiness work;
- that no market rows may be parsed unless separately authorized.

This draft does not grant that execution.

## Relationship To Contract Identity

Provider mapping and local contract identity are adjacent but distinct.

Provider mapping asks:

```text
Which local/provider instrument, if any, corresponds to this Appendix C row?
```

Contract identity readiness asks:

```text
What are the locked local contract facts needed before data and sizing work?
```

Local contract identity should remain closed until provider mapping evidence rules are locked.

## Relationship To Data Readiness

Provider mapping is not data readiness.

Even after a future provider symbol is mapped, Carver will still need separate gates for:

- exchange/session calendar;
- completed-bar definition;
- roll rule;
- back-adjustment rule;
- contract multiplier and point value confirmation;
- data availability;
- stale/missing-bar policy;
- annual risk source;
- price risk source;
- FX source;
- cost source;
- carry curve-leg availability.

## Rejected Interpretations

### Author Market Code Equals Provider Symbol

Rejected.

Reason:

```text
SOURCE_MARKET_CODE_IS_NOT_LOCAL_PROVIDER_MAPPING
```

The book itself warns that market codes may vary across brokers.

### Provider Mapping Can Drop Missing Members

Rejected.

Reason:

```text
COMPLETE_102_MEMBER_UNIVERSE_IDENTITY_FAILS_CLOSED_ON_MISSING_MEMBERS
```

Dropping or reweighting a missing member changes the portfolio.

### Provider Mapping Can Use CFD Symbols

Rejected.

Reason:

```text
APPENDIX_C_LANE_IS_SOURCE_NATIVE_FUTURES
```

CFD adapters remain closed and require a separate future gate after source-native behavior exists.

### Provider Mapping Can Borrow Old QuantLab Files

Rejected.

Reason:

```text
OLD_QUANTLAB_ACTIVE_PIPELINE_STATE_REMAINS_QUARANTINED
```

Old symbols, mappings, adapters, and data-prep scripts are not active authority.

### Provider Mapping Opens Market Data Work

Rejected.

Reason:

```text
PROVIDER_MAPPING_IS_NOT_MARKET_ROW_READINESS
```

No market-row parsing, NinjaTrader export, diagnostics, or backtests are opened by provider mapping readiness.

## Audit Requirements

This provider mapping readiness shape draft should receive a lean regular hostile audit, preferably by subagent, before it is treated as locked.

Audit focus:

- no provider mapping execution is smuggled into the draft;
- no provider API, real data, market-row parsing, NinjaTrader export, diagnostics, or backtests are opened;
- source universe identity remains separate from provider availability;
- author market codes are not promoted to provider symbols;
- exactness rules are fail-closed;
- missing, ambiguous, inactive, unavailable, multiplier-mismatched, exchange-mismatched, currency-mismatched, and variant-mismatched rows fail closed;
- micro/mini/full and other contract variants cannot be silently substituted;
- CFD adapters and old QuantLab active-pipeline use remain closed;
- no deployment, trading, promotion, Opus/GPT execution, remote operations, remote push, or GitHub action is opened.

Regular hostile audit results should be preserved automatically as separate process-only audit-result records.

## Next Proposed Authorization

If this draft passes lean hostile audit, the next clean gate may be a process-only provider mapping execution gate with no market rows.

```text
Operator authorizes one process-only Carver Appendix C source-native provider
mapping execution gate.

Scope:
Create a process/source mapping artifact for the audited Appendix C
machine-readable 102-row universe, using only separately specified static
source-native provider evidence, and record MAPPED/BLOCKED/UNRESOLVED status
for each row without touching market rows.

Allowed:
Read-only inspection of the audited Appendix C machine-readable universe lock
and explicitly specified static provider evidence, plus creation of provider
mapping process/source documentation or machine-readable mapping artifact.

Forbidden:
No code edits, no tests, no real market data, no market-row parsing, no
NinjaTrader export, no diagnostics, no backtests, no OOS, no Lockbox, no
Forward, no CFD adapters, no old QuantLab pipeline use, no tuning, no
deployment, no trading, no promotion, no silent substitution/drop/reweight, no
Opus/GPT execution, no remote operations.
```

## Non-Authorization

This readiness-shape draft authorizes no code edits, no tests, no real-data execution, no provider API access, no provider mapping execution, no market-row parsing, no NinjaTrader export, no diagnostics, no backtests, no returns, no PnL, no Sharpe, no drawdown, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old-adapter import, no old workspace pipeline use, no tuning, no deployment, no trading, no promotion, no production data readiness claim, no Opus/GPT execution, no remote push, and no GitHub action.
