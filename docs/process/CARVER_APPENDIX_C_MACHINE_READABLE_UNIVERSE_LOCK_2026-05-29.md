# Carver Appendix C Machine-Readable Universe Lock

Date: 2026-05-29

Status:

```text
PROCESS_SOURCE_CARVER_APPENDIX_C_MACHINE_READABLE_UNIVERSE_LOCK_NOT_DATA_NOT_IMPLEMENTATION
```

## Purpose

Record the deterministic machine-readable source-universe lock for the Carver Appendix C Jumbo portfolio before provider mapping or data work.

This artifact converts the audited Appendix C transcription/source packet into a 102-row CSV source-universe lock with fail-closed readiness defaults.

It is not market data, provider mapping, data readiness, code implementation, diagnostics, backtests, deployment, trading, or promotion.

## Source Inputs

Audited source packet:

```text
docs/process/CARVER_APPENDIX_C_JUMBO_UNIVERSE_TRANSCRIPTION_SOURCE_PACKET_2026-05-29.md
```

Source-packet audit result:

```text
docs/process/CARVER_APPENDIX_C_JUMBO_UNIVERSE_TRANSCRIPTION_SOURCE_PACKET_HOSTILE_AUDIT_RESULT_2026-05-29.md
```

The source packet received:

```text
NO BLOCKING FINDINGS
AUDIT_DISPOSITION: PASS_PROCESS_ONLY_SOURCE_PACKET_SCOPE
```

Narrow book source:

```text
Carver.pdf Appendix C, PDF pages 690-695, Tables 172-183
```

## Machine-Readable Artifact

CSV artifact:

```text
docs/researchops/portfolios/CARVER_APPENDIX_C_JUMBO_UNIVERSE_LOCK_2026-05-29.csv
```

Current SHA-256:

```text
9453a9635148ae4d998306e0ac921c534d35d4d97dde3934c8aea02104e48c5f
```

The hash is a source-process integrity check for this checked-in CSV artifact. It is not a market-data checksum.

## Schema

The CSV columns are deterministic and ordered:

```text
row_id
appendix_table
pdf_pages
source_group
descriptive_name
author_market_code
exchange
currency
multiplier
first_source_year
lane_class
provider_mapping_status
local_contract_identity_status
market_data_readiness_status
substitution_policy
production_use_status
```

## Required Defaults

Every row must carry:

```text
lane_class = SOURCE_NATIVE_FUTURES
provider_mapping_status = UNRESOLVED
local_contract_identity_status = UNRESOLVED
market_data_readiness_status = CLOSED
substitution_policy = FAIL_CLOSED_NO_DROP_NO_SUBSTITUTE_NO_REWEIGHT
production_use_status = NOT_AUTHORIZED
```

## Deterministic Row Identity

`row_id` uses:

```text
APPENDIX_C_<table>_<three_digit_index_within_table>
```

Examples:

```text
APPENDIX_C_172_001
APPENDIX_C_183_013
```

The row id is a process/source identity handle. It is not a provider symbol or trading identifier.

## Verification Result

Local mechanical verification of the CSV recorded:

```text
ROWS 102
TABLES 172,173,174,175,176,177,178,179,180,181,182,183
COUNTS 172=10,173=11,174=6,175=8,176=8,177=12,178=2,179=9,180=8,181=9,182=6,183=13
LANES SOURCE_NATIVE_FUTURES
PROVIDER UNRESOLVED
MARKET CLOSED
SUBSTITUTION FAIL_CLOSED_NO_DROP_NO_SUBSTITUTE_NO_REWEIGHT
PRODUCTION NOT_AUTHORIZED
DUP_ROW_IDS none
```

This verification is a process/source artifact check only. It is not a code test, market-data test, diagnostic, or backtest.

## Provider Mapping Boundary

The `author_market_code` column remains the broker market code used in the book source.

It is not:

- a local provider symbol;
- an official exchange code claim;
- a tradable contract id;
- a NinjaTrader instrument name;
- a CFD symbol;
- a continuous futures symbol;
- a permission to substitute another instrument.

Provider mapping remains a future readiness gate.

## Missing-Member Boundary

The locked default policy is:

```text
FAIL_CLOSED_NO_DROP_NO_SUBSTITUTE_NO_REWEIGHT
```

This applies before provider mapping and remains the baseline for later readiness work unless a separate operator-authorized source/governance artifact changes it.

## What This Lock Opens

This lock opens only a stable source-universe input for future process/readiness work.

Possible next process gates:

- provider mapping readiness shape;
- local contract identity packet;
- risk/FX/cost readiness shape;
- trend/carry eligibility readiness shape;
- post-lock decision on which readiness branch comes first.

Each later gate requires separate authorization.

## What Remains Closed

Still closed:

- code edits;
- tests;
- real-data execution;
- market-row parsing;
- NinjaTrader export;
- diagnostics;
- backtests;
- returns;
- PnL;
- Sharpe;
- drawdown;
- OOS;
- Lockbox;
- Forward;
- CFD adapters;
- old QuantLab active-pipeline use;
- tuning;
- deployment;
- trading;
- promotion;
- provider mapping;
- production source locks beyond Appendix C universe identity;
- local data readiness claims;
- GitHub push or remote operation.

## Audit Requirements

This machine-readable universe lock should receive a lean regular hostile audit before it is treated as locked.

Audit focus:

- CSV has exactly 102 rows;
- row ids are unique;
- tables 172-183 are represented;
- table counts match the audited transcription packet;
- schema is exactly the declared schema;
- fail-closed defaults are present on every row;
- author market codes are not promoted into local provider mappings;
- source/process lock does not open real data, diagnostics, backtests, implementation, provider mapping, CFD adapter work, old QuantLab active-pipeline use, deployment, trading, promotion, Opus/GPT execution, or remote operations.

Regular hostile audit results should be preserved automatically as separate process-only audit-result records.

## Non-Authorization

This machine-readable universe lock authorizes no code edits, no tests, no real-data execution, no market-row parsing, no NinjaTrader export, no diagnostics, no backtests, no returns, no PnL, no Sharpe, no drawdown, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old-adapter import, no old workspace pipeline use, no tuning, no deployment, no trading, no promotion, no provider mapping, no production data readiness claim, no Opus/GPT execution, no remote push, and no GitHub action.
