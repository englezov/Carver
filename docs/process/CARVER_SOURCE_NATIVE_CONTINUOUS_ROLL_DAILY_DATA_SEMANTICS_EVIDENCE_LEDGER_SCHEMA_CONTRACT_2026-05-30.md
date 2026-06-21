# Carver Source-Native Continuous/Roll Daily Data Semantics Evidence Ledger Schema Contract

Date: 2026-05-30

Status:

```text
PROCESS_ONLY_CARVER_SOURCE_NATIVE_CONTINUOUS_ROLL_DAILY_DATA_SEMANTICS_EVIDENCE_LEDGER_SCHEMA_CONTRACT_NOT_SOURCE_EXTRACTION_NOT_EVIDENCE_EXECUTION_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Define the exact future output schema and fail-closed contract for a separately authorized source-native continuous/roll daily data semantics evidence execution gate.

This artifact does not execute the evidence gate. It does not extract book source text, inspect public/provider documentation, inspect official exchange pages, log in to any provider, call any API, download data, parse market rows, create evidence ledgers, build continuous contracts, create strategy input, run diagnostics, run backtests, compute forecasts, compute positions, compute costs, compute carry, compute trend, compute volatility/risk, access OOS/Lockbox/Forward, deploy, trade, promote, stage Git changes, commit, push, update a PR, or perform remote operations.

## Governing Artifacts

Evidence execution draft:

```text
docs/process/CARVER_SOURCE_NATIVE_CONTINUOUS_ROLL_DAILY_DATA_SEMANTICS_EVIDENCE_EXECUTION_GATE_DRAFT_2026-05-30.md
```

Evidence packet:

```text
docs/process/CARVER_SOURCE_NATIVE_CONTINUOUS_ROLL_DAILY_DATA_SEMANTICS_EVIDENCE_PACKET_2026-05-30.md
```

Local-source preflight:

```text
docs/process/CARVER_SOURCE_NATIVE_CONTINUOUS_ROLL_DAILY_DATA_SEMANTICS_LOCAL_SOURCE_PREFLIGHT_2026-05-30.md
```

Two-gate handoff:

```text
docs/process/CARVER_DAILY_DATA_FOUNDATION_TWO_GATE_AUTHORIZATION_READY_PACKET_2026-05-30.md
```

Completion matrix:

```text
docs/process/CARVER_DAILY_DATA_FOUNDATION_COMPLETION_CRITERIA_AND_EVIDENCE_MATRIX_2026-05-30.md
```

## Future Output Root

If the future gate is separately authorized, outputs must be written under:

```text
docs/researchops/source_native_futures_daily_data_library/continuous_roll_semantics_evidence/2026-05-30/
```

Required future files:

```text
CARVER_SOURCE_NATIVE_CONTINUOUS_ROLL_EVIDENCE_SOURCE_INDEX_2026-05-30.md
CARVER_16_SYMBOL_CONTINUOUS_ROLL_EVIDENCE_REQUIREMENTS_2026-05-30.csv
CARVER_16_SYMBOL_CONTINUOUS_ROLL_PROVIDER_CAPABILITY_STATUS_2026-05-30.csv
CARVER_16_SYMBOL_CONTINUOUS_ROLL_LIFECYCLE_EVIDENCE_NEEDS_2026-05-30.csv
CARVER_SOURCE_NATIVE_CONTINUOUS_ROLL_EVIDENCE_PACKET_SHA256SUMS_2026-05-30.txt
```

## Source Index MD Contract

Future file:

```text
CARVER_SOURCE_NATIVE_CONTINUOUS_ROLL_EVIDENCE_SOURCE_INDEX_2026-05-30.md
```

Required sections:

```text
Status
Scope
Local Source Inputs And Hashes
Book Source Ranges Reviewed
Provider Static Documentation Reviewed
Exchange Or Official Product Sources Reviewed
Existing Local Quarantine Provenance Reviewed
Evidence Boundaries
Blocked Or Unresolved Source Classes
Output Ledgers
Audit Requirement
Non-Authorization
```

Future required status:

```text
PROCESS_SOURCE_CARVER_SOURCE_NATIVE_CONTINUOUS_ROLL_DAILY_DATA_SEMANTICS_EVIDENCE_EXECUTION_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

Required local input hashes:

| Role | SHA256 |
|---|---|
| Local book authority, `Carver.pdf` | `AA052B8D942767A7547ECDBB09FBED22F2412FB7B1036D24AB854738308582B6` |
| Continuous/roll shape gate | `8EA38676F008BDE787F7FD2F80D360A1FC49785BAF8FC3CD07F0EAE6A2CB04E1` |
| Continuous/roll evidence packet | `E124735263D1A1049DB49ED25103FA7F0F11EF011D6B101307B7402CE45B38ED` |
| Continuous/roll evidence execution draft | `B8D01832AC4D285E4805ABC55060B5EE7B578C19EFD8CA0E5C835D23E1CC7335` |
| Goal completion matrix | `0123D4C7000A604E5748F861DB71AB1AD9D858C8260E983687365DA75662F450` |
| Current authorization queue | `1BFEC1D73BFDD755C422D43F18C717B10507A6A36C64899322E23F0CCAD8DCDC` |

The source index must state that it is evidence only and does not build continuous series or create strategy input.

## Evidence Requirements CSV Contract

Future file:

```text
CARVER_16_SYMBOL_CONTINUOUS_ROLL_EVIDENCE_REQUIREMENTS_2026-05-30.csv
```

Future expected row scope, not current proof:

```text
ONE_ROW_PER_LOCKED_SYMBOL_OR_PRODUCT_FAMILY_REQUIREMENT
MINIMUM_SYMBOL_COVERAGE: 16 locked pilot symbols
```

Future required columns, in order:

| Column | Required value/domain |
|---|---|
| `foundation_scope` | `SOURCE_NATIVE_FUTURES_DAILY_DATA_FOUNDATION` |
| `ledger_label` | `CONTINUOUS_ROLL_EVIDENCE_REQUIREMENTS_ONLY` |
| `book_symbol` | one of the 16 locked pilot symbols |
| `product_family` | Treasury rates, Equity index, Energy, Agriculture grains/oilseeds, or Livestock |
| `current_dated_contract` | existing locked dated contract if applicable |
| `required_carver_source_range` | source range class from the evidence packet |
| `required_provider_doc_class` | provider static documentation class |
| `required_exchange_doc_class` | official exchange/product/rulebook documentation class |
| `roll_trigger_evidence_status` | one of the evidence status values below |
| `adjustment_policy_evidence_status` | one of the evidence status values below |
| `settlement_close_evidence_status` | one of the evidence status values below |
| `lifecycle_evidence_status` | one of the evidence status values below |
| `provider_condition_policy_status` | one of the evidence status values below |
| `lineage_requirement_status` | one of the evidence status values below |
| `carry_raw_price_caveat_status` | required for carry-relevant interpretation; otherwise `NOT_APPLICABLE_FOR_TREND_ONLY_EVIDENCE` |
| `strategy_use_status` | `BLOCKED_PENDING_CONTINUOUS_ROLL_POLICY` or stricter |
| `blocker` | explicit blocker or `NONE_FOR_POLICY_DECISION_ONLY` |
| `evidence_execution_status` | `EVIDENCE_ONLY_NOT_STRATEGY_INPUT_NOT_BACKTEST_READY` |

Allowed future evidence status values:

```text
EVIDENCE_READY_FOR_POLICY_DECISION
EVIDENCE_PARTIAL_REQUIRES_MORE_STATIC_SOURCE
EVIDENCE_BLOCKED_PROVIDER_SEMANTICS_UNCLEAR
EVIDENCE_BLOCKED_EXCHANGE_LIFECYCLE_UNCLEAR
EVIDENCE_BLOCKED_SETTLEMENT_CLOSE_UNCLEAR
EVIDENCE_BLOCKED_LINEAGE_UNCLEAR
EVIDENCE_BLOCKED_CARRY_RAW_PRICE_UNCLEAR
EVIDENCE_NOT_REVIEWED_FAIL_CLOSED
```

No value may imply:

```text
STRATEGY_READY
BACKTEST_READY
FORECAST_READY
POSITION_READY
DEPLOYMENT_OR_TRADING_READY
```

## Provider Capability Status CSV Contract

Future file:

```text
CARVER_16_SYMBOL_CONTINUOUS_ROLL_PROVIDER_CAPABILITY_STATUS_2026-05-30.csv
```

Future expected row scope, not current proof:

```text
ONE_ROW_PER_PROVIDER_CAPABILITY_QUESTION_PER_SYMBOL_OR_PRODUCT_FAMILY
```

Future required columns, in order:

| Column | Required value/domain |
|---|---|
| `provider` | `DATABENTO` or another separately authorized static provider doc class |
| `dataset_or_doc_scope` | provider dataset/doc scope reviewed |
| `book_symbol_or_family` | locked symbol or product family |
| `capability_question` | continuous availability, symbol syntax, adjustment policy, roll rule, lineage, ohlcv-1d close/settlement, definition metadata, condition metadata, or settlement source |
| `static_source_reference` | source reference or `UNRESOLVED_FAIL_CLOSED` |
| `evidence_status` | allowed evidence status value |
| `provider_api_access` | `NO` |
| `provider_login` | `NO` |
| `market_data_download` | `NO` |
| `continuous_contract_download` | `NO` |
| `market_row_parsing` | `NO` |
| `strategy_use_status` | `BLOCKED_PENDING_CONTINUOUS_ROLL_POLICY` or stricter |
| `blocker` | explicit blocker or `NONE_FOR_POLICY_DECISION_ONLY` |

Provider-built continuous contracts, if identified, must remain:

```text
REFERENCE_ONLY_UNTIL_SOURCE_AND_LINEAGE_AUDITED
```

## Lifecycle Evidence Needs CSV Contract

Future file:

```text
CARVER_16_SYMBOL_CONTINUOUS_ROLL_LIFECYCLE_EVIDENCE_NEEDS_2026-05-30.csv
```

Future expected row scope, not current proof:

```text
ONE_ROW_PER_SYMBOL_OR_PRODUCT_FAMILY_LIFECYCLE_REQUIREMENT
```

Future required columns, in order:

| Column | Required value/domain |
|---|---|
| `book_symbol` | one of the 16 locked pilot symbols |
| `product_family` | Treasury rates, Equity index, Energy, Agriculture grains/oilseeds, or Livestock |
| `delivery_or_cash_settlement_class` | physical delivery, cash settled, unresolved, or other explicitly sourced class |
| `listed_contract_months_evidence_status` | allowed evidence status value |
| `first_notice_evidence_status` | allowed evidence status value or `NOT_APPLICABLE_SOURCE_REQUIRED` |
| `last_trade_evidence_status` | allowed evidence status value |
| `expiration_or_termination_evidence_status` | allowed evidence status value |
| `delivery_or_cash_settlement_evidence_status` | allowed evidence status value |
| `daily_settlement_or_close_publication_evidence_status` | allowed evidence status value |
| `holiday_session_reference_status` | allowed evidence status value |
| `roll_safety_blocker` | explicit blocker or `NONE_FOR_POLICY_DECISION_ONLY` |
| `strategy_use_status` | `BLOCKED_PENDING_CONTINUOUS_ROLL_POLICY` or stricter |

Physically delivered products must fail closed unless first-notice, last-trade, delivery-window, and roll-safety evidence are sufficient for a later policy decision.

Cash-settled products must fail closed unless expiration, final settlement, and daily close/settlement evidence are sufficient for a later policy decision.

## SHA256SUMS Contract

Future file:

```text
CARVER_SOURCE_NATIVE_CONTINUOUS_ROLL_EVIDENCE_PACKET_SHA256SUMS_2026-05-30.txt
```

Required contents:

```text
SHA256  CARVER_SOURCE_NATIVE_CONTINUOUS_ROLL_EVIDENCE_SOURCE_INDEX_2026-05-30.md
SHA256  CARVER_16_SYMBOL_CONTINUOUS_ROLL_EVIDENCE_REQUIREMENTS_2026-05-30.csv
SHA256  CARVER_16_SYMBOL_CONTINUOUS_ROLL_PROVIDER_CAPABILITY_STATUS_2026-05-30.csv
SHA256  CARVER_16_SYMBOL_CONTINUOUS_ROLL_LIFECYCLE_EVIDENCE_NEEDS_2026-05-30.csv
```

The actual SHA256 values must be computed only after the future files are created by the separately authorized evidence execution gate.

## Future Fail-Closed Validation Checklist

The future evidence execution must fail closed if any of the following occurs:

- any required local source/process input hash differs from the local-source preflight;
- any evidence ledger omits one of the 16 locked pilot symbols or its product-family coverage;
- any row implies strategy readiness, backtest readiness, forecast readiness, position readiness, deployment readiness, or trading readiness;
- any provider API call, provider login, provider portal use, new market-data request, or data download occurs;
- any market row is parsed;
- any continuous contract is downloaded;
- any continuous series is constructed;
- any dated-contract fragment table is promoted to strategy input;
- any narrow ZN precedent is promoted into global 16-symbol policy without evidence;
- any source class is missing but not labeled blocked or unresolved;
- any evidence status lacks an explicit blocker when blocked or partial;
- any forbidden operation is attempted.

## Current Goal Completion State

Current broad-goal completion state remains:

```text
NOT_COMPLETE
```

Reason:

```text
This schema contract defines future evidence-ledger expectations only. It does not extract continuous/roll source evidence, create evidence ledgers, decide policy, execute the dated-contract fragment table, or create strategy-facing data.
```

## Non-Authorization

This schema contract authorizes no provider API access, no provider login, no provider account portal use, no new market-data request, no data download, no market-row parsing, no table execution, no book-source extraction, no public/provider documentation inspection, no official exchange page inspection, no evidence-ledger creation, no raw or sanitized archive modification, no continuous-contract download, no continuous-series construction, no diagnostics, no backtests, no forecasts, no positions, no costs, no carry, no trend, no volatility/risk calculations, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.
