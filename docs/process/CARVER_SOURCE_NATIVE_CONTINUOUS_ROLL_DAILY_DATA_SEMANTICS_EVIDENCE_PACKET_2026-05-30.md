# Carver Source-Native Continuous/Roll Daily Data Semantics Evidence Packet

Date: 2026-05-30

Status:

```text
PROCESS_ONLY_CARVER_SOURCE_NATIVE_CONTINUOUS_ROLL_DAILY_DATA_SEMANTICS_EVIDENCE_PACKET_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Identify the exact source and provider evidence required before Carver can build or admit any source-native continuous/rolled daily futures series as strategy-facing Development/Reconciliation input.

This packet is process-only. It does not fetch provider data, download continuous contracts, parse market rows, construct a continuous series, compute returns, run diagnostics, run backtests, compute forecasts, compute positions, compute costs, compute carry, compute trend, compute volatility/risk, or promote data.

## Governing Inputs

Foundation and handoff records:

```text
docs/process/CARVER_M0_SOURCE_NATIVE_FUTURES_FOUNDATION_SPEC_2026-05-28.md
docs/process/CARVER_DAILY_DATA_FOUNDATION_NEXT_STEP_HANDOFF_DECISION_2026-05-30.md
docs/process/CARVER_SOURCE_NATIVE_CONTINUOUS_ROLL_DAILY_DATA_SEMANTICS_SHAPE_GATE_2026-05-30.md
docs/process/CARVER_16_SYMBOL_DATED_CONTRACT_FRAGMENT_DEV_RECON_TABLE_SHAPE_GATE_2026-05-30.md
```

Source and architecture records:

```text
docs/researchops/candidates/CARVER_S01_BUY_AND_HOLD_SINGLE_CONTRACT_CANDIDATE_BRIEF_2026-05-28.md
docs/process/CARVER_SOURCE_NATIVE_FUTURES_DAILY_DATA_LIBRARY_ARCHITECTURE_GATE_DRAFT_2026-05-30.md
docs/process/CARVER_SOURCE_NATIVE_FUTURES_HISTORICAL_DATA_SOURCE_SELECTION_DECISION_2026-05-30.md
```

Prior narrow precedent, not global authority:

```text
docs/process/CARVER_ZN_CONTINUOUS_CONSTRUCTION_READINESS_GATE_2026-05-29.md
```

The ZN gate is useful as a cautionary narrow readiness precedent. It must not be silently promoted into a global 16-symbol or Appendix C roll policy.

## Lane

```text
SOURCE_NATIVE_FUTURES
```

No CFD assumptions, CFD adapters, broker-clock shortcuts, or old QuantLab active-pipeline state may enter this evidence path.

## Book-Side Evidence Required

### Core Futures Price/Roll Source

Required source range:

```text
Carver.pdf, Strategy One, PDF pages 21-66
```

Minimum atoms to extract or cite before execution:

```text
single futures contract framing
daily closing price usage
expiry and rolling framing
back-adjusted futures price purpose
excess-return interpretation of adjusted futures prices
profit calculation from adjusted price changes and multiplier
costs treated separately
```

Current local source summary:

```text
docs/researchops/candidates/CARVER_S01_BUY_AND_HOLD_SINGLE_CONTRACT_CANDIDATE_BRIEF_2026-05-28.md
```

Relevant process-summary atoms already recorded there:

```text
S01 introduces futures multipliers, tick size, tick value, expiry dates, rolling, back-adjusted futures prices, trading costs, profit calculation, capital, and performance assessment.
The book initially tests daily data using daily closing prices for each contract expiry date.
Back-adjustment is used to represent the profit and loss from constantly holding and rolling one futures contract while excluding trading costs.
The adjusted futures price is an excess-return series that includes spot and carry, not a total-return series.
```

Future evidence packet must re-check the actual local `Carver.pdf` pages before any lock.

### M0 Foundation Atoms

Required process source:

```text
docs/process/CARVER_M0_SOURCE_NATIVE_FUTURES_FOUNDATION_SPEC_2026-05-28.md
```

Required atoms:

```text
completed daily bars only
continuous-contract construction must be locked
contract selection and rolling rule must be locked
back-adjusted price construction must be locked
bar close timestamp semantics must be locked
holiday/session/calendar policy must be locked
fail-closed behavior for missing or invalid inputs must be locked
```

### Carry-Specific Price Evidence

Required source range before any carry or combined trend/carry strategy input:

```text
Carver.pdf, Strategy Ten, PDF pages 232-259
```

Required atoms:

```text
raw futures prices for held and comparison contracts
front/near/far contract role selection
expiry-distance annualization
raw price versus adjusted price convention for carry and PnL
sparse second-contract history warning
seasonal/wrong-sign handling
curve-leg availability and fail-closed rules
```

This packet does not open carry computation.

### Combined Strategy/Portfolio Dependence

Required source ranges before broad strategy machinery:

```text
Carver.pdf, Strategy Nine trend source range
Carver.pdf, Strategy Ten carry source range
Carver.pdf, Strategy Eleven combined trend/carry source range
Carver.pdf, Appendix C Jumbo universe range, PDF pages 690-695
```

Required implication:

```text
continuous/rolled daily prices are a shared data foundation for trend;
raw dated contract and curve-leg prices are separate required evidence for carry;
neither is solved by the dated-contract fragment plumbing table.
```

## Provider-Side Evidence Required

### Databento Evidence

Candidate evidence documents already identified by architecture records:

```text
Databento Historical documentation
Databento GLBX.MDP3 dataset documentation
Databento schemas and data formats documentation
Databento symbology standards and conventions
Databento futures examples
Databento dataset condition metadata behavior
Databento definition/reference metadata behavior
Databento continuous symbology or continuous-contract documentation if considered
```

Required Databento evidence atoms before execution:

```text
whether provider-built continuous futures are available for GLBX.MDP3;
exact continuous symbol syntax if available;
whether continuous rows are back-adjusted, ratio-adjusted, unadjusted, or otherwise transformed;
provider roll rule for each continuous series if provider-built continuous is considered;
whether provider roll rule can be audited back to dated contracts;
whether provider continuous rows preserve source instrument lineage;
whether ohlcv-1d close is trade close, settlement, or another daily close convention;
whether settlement requires a separate schema, statistics path, or official source;
how dataset-condition degraded rows apply to continuous rows;
whether definition metadata provides first notice, last trade, expiration, delivery/cash settlement, and contract lifecycle fields needed for local roll construction;
```

Provider-built continuous contracts must be treated as:

```text
REFERENCE_ONLY_UNTIL_SOURCE_AND_LINEAGE_AUDITED
```

They must not silently replace dated contracts.

### Exchange/Official Spec Evidence

For every product family in the 16-symbol pilot, required official static evidence includes:

```text
product code and exact contract family
listed contract months
first notice date policy where applicable
last trade date policy
expiration or termination date policy
delivery versus cash settlement
daily settlement or close publication semantics
holiday and session rule references
```

Product families in current 16-symbol pilot:

```text
Treasury rates: ZT, ZF, ZN
Equity index: MES, MNQ, M2K, MYM
Energy: QM, RB
Agriculture grains/oilseeds: ZC, ZS, ZM, ZL, ZW
Livestock: HE, LE
```

Special caution:

```text
physical delivery products require first-notice and delivery-window fail-closed rules;
cash-settled equity index products require expiration/cash-settlement policy;
energy and agricultural products may require product-family-specific roll timing;
carry-ready products require synchronized held and comparison contract evidence, not just a single continuous price.
```

### Existing Dated-Contract Archive Evidence

Current local quarantine archive state, as plumbing evidence only:

```text
16 dated-contract manifest rows
4568 Databento dated-contract archive rows
4483 normal provider-condition rows
85 degraded provider-condition rows quarantined
0 blocked/unresolved provider-condition rows
```

The dated archive may support future lineage and table-plumbing checks, but it is not strategy input by itself.

Required lineage proof before continuous strategy input:

```text
every continuous row maps to one or more dated-contract source rows;
every source row carries provider symbol, instrument_id, completed trading date, timestamp, provider condition status, and hash lineage;
degraded source rows are excluded, blocked, or explicitly policy-labeled;
no missing roll-date bar is silently filled;
no duplicate date survives into the continuous strategy row set;
```

## Candidate Semantics Choices To Decide Later

This packet does not choose the final policy. A later execution/decision gate must choose or fail-close:

```text
provider-built continuous as reference-only versus source authority
local continuous construction from dated contracts
front-month rule
next-contract rule
roll trigger: calendar, volume, open interest, first notice, last trade, expiry, or source-specific
back-adjustment: additive, ratio, none, or another explicit method
settlement versus close price
condition degraded row treatment
carry raw-price source versus adjusted-price source
daily completed-date and timestamp interpretation
lineage schema
```

## Fail-Closed Conditions

Continuous/roll semantics must fail closed if:

```text
roll rule is not deterministic;
provider continuous construction cannot be documented;
provider continuous construction cannot be traced to dated-contract lineage when required;
first notice / last trade / expiration evidence is missing for a physically delivered product;
settlement versus close semantics are unresolved for a strategy that depends on settlement;
degraded provider-condition rows would be silently included;
missing roll-date overlap would require fill or interpolation without explicit authorization;
symbol substitutions, full/micro/mini bridges, or Appendix C row drops are proposed without a source gate;
any strategy computation is bundled into data construction.
```

## Required Future Output For Evidence Execution

A future continuous/roll evidence execution gate should produce:

```text
CARVER_SOURCE_NATIVE_CONTINUOUS_ROLL_EVIDENCE_SOURCE_INDEX_2026-05-30.md
CARVER_16_SYMBOL_CONTINUOUS_ROLL_EVIDENCE_REQUIREMENTS_2026-05-30.csv
CARVER_16_SYMBOL_CONTINUOUS_ROLL_PROVIDER_CAPABILITY_STATUS_2026-05-30.csv
CARVER_16_SYMBOL_CONTINUOUS_ROLL_LIFECYCLE_EVIDENCE_NEEDS_2026-05-30.csv
CARVER_SOURCE_NATIVE_CONTINUOUS_ROLL_EVIDENCE_PACKET_SHA256SUMS_2026-05-30.txt
```

Minimum evidence-requirement CSV fields:

```text
book_symbol
product_family
current_dated_contract
required_carver_source_range
required_provider_doc_class
required_exchange_doc_class
roll_trigger_evidence_status
adjustment_policy_evidence_status
settlement_close_evidence_status
lifecycle_evidence_status
provider_condition_policy_status
lineage_requirement_status
strategy_use_status
blocker
```

Required default status:

```text
STRATEGY_USE_STATUS: BLOCKED_PENDING_CONTINUOUS_ROLL_POLICY
```

## Current Decision

This packet selects the next semantic evidence step:

```text
CARVER_SOURCE_NATIVE_CONTINUOUS_ROLL_DAILY_DATA_SEMANTICS_EVIDENCE_EXECUTION_GATE
```

Allowed future scope if separately authorized:

```text
read-only Carver.pdf source extraction;
read-only public/static provider documentation inspection;
read-only official exchange/static spec inspection;
creation of source/provider evidence ledgers;
no provider API access;
no market data download;
no market-row parsing.
```

Parallel immediate mechanics gate remains:

```text
CARVER_16_SYMBOL_DATED_CONTRACT_FRAGMENT_DEV_RECON_TABLE_EXECUTION_GATE
```

That gate remains closed unless separately authorized.

## Non-Authorization

This evidence packet authorizes no provider API access, no provider login, no new market-data request, no data download, no market-row parsing, no table execution, no continuous-contract download, no continuous-series construction, no diagnostics, no backtests, no forecasts, no positions, no costs, no carry, no trend, no volatility/risk calculations, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.
