# Carver Source-Native Continuous/Roll Daily Data Semantics Evidence Execution Gate Draft

Date: 2026-05-30

Status:

```text
PROCESS_ONLY_CARVER_SOURCE_NATIVE_CONTINUOUS_ROLL_DAILY_DATA_SEMANTICS_EVIDENCE_EXECUTION_GATE_DRAFT_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Draft the exact future execution gate for gathering static source/provider evidence needed to decide source-native continuous/rolled daily futures semantics before any broad Carver strategy machinery.

This draft does not execute the gate. It does not browse provider APIs, log in, download market data, parse market rows, build continuous contracts, create strategy input, run diagnostics, run backtests, compute forecasts, compute positions, compute costs, compute carry, compute trend, compute volatility/risk, deploy, trade, promote, stage Git changes, commit, push, update a PR, or perform remote operations.

## Required Separate Authorization

The future execution gate must be separately authorized by the operator before any source extraction, public/provider documentation browsing, official exchange-spec inspection, or evidence-ledger creation.

Required future status string:

```text
PROCESS_SOURCE_CARVER_SOURCE_NATIVE_CONTINUOUS_ROLL_DAILY_DATA_SEMANTICS_EVIDENCE_EXECUTION_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Governing Evidence Packet

Evidence packet:

```text
docs/process/CARVER_SOURCE_NATIVE_CONTINUOUS_ROLL_DAILY_DATA_SEMANTICS_EVIDENCE_PACKET_2026-05-30.md
```

Shape gate:

```text
docs/process/CARVER_SOURCE_NATIVE_CONTINUOUS_ROLL_DAILY_DATA_SEMANTICS_SHAPE_GATE_2026-05-30.md
```

Subagent audit:

```text
docs/process/CARVER_SOURCE_NATIVE_CONTINUOUS_ROLL_DAILY_DATA_SEMANTICS_EVIDENCE_PACKET_LEAN_HOSTILE_AUDIT_RESULT_2026-05-30.md
AUDIT_DISPOSITION: PASS_PROCESS_ONLY_CONTINUOUS_ROLL_EVIDENCE_PACKET_SCOPE
```

## Future Allowed Evidence Sources

If separately authorized, future execution may inspect only:

```text
local Carver.pdf source pages;
current Carver process/source artifacts;
public/static Databento documentation pages;
public/static exchange or official product-spec/rulebook pages;
public/static CME Group product and settlement/expiration references;
already-created local Databento quarantine provenance and metadata records.
```

Forbidden evidence sources for that gate:

```text
Databento API calls
provider login
provider account portal
new market-data requests
historical OHLCV downloads
continuous-contract downloads
market-row parsing
old QuantLab active-pipeline files
CFD adapter state
broker execution state
```

## Future Output Root

If separately authorized, output should be written under:

```text
docs/researchops/source_native_futures_daily_data_library/continuous_roll_semantics_evidence/2026-05-30/
```

Required outputs:

```text
CARVER_SOURCE_NATIVE_CONTINUOUS_ROLL_EVIDENCE_SOURCE_INDEX_2026-05-30.md
CARVER_16_SYMBOL_CONTINUOUS_ROLL_EVIDENCE_REQUIREMENTS_2026-05-30.csv
CARVER_16_SYMBOL_CONTINUOUS_ROLL_PROVIDER_CAPABILITY_STATUS_2026-05-30.csv
CARVER_16_SYMBOL_CONTINUOUS_ROLL_LIFECYCLE_EVIDENCE_NEEDS_2026-05-30.csv
CARVER_SOURCE_NATIVE_CONTINUOUS_ROLL_EVIDENCE_PACKET_SHA256SUMS_2026-05-30.txt
```

## Future Evidence Requirements

The future execution must identify or fail-close evidence for:

```text
Carver Strategy One price/roll/back-adjusted futures source framing;
M0 completed-bar and roll/back-adjustment foundation atoms;
Databento continuous-contract availability and documentation;
Databento continuous-contract adjustment/roll/lineage semantics if available;
Databento ohlcv-1d close versus settlement semantics;
Databento definition/reference metadata lifecycle fields;
exchange first-notice / last-trade / expiration / delivery / cash-settlement rules;
daily settlement or close source semantics by product family;
provider-condition degraded-row policy implications for continuous rows;
raw dated-contract lineage requirement for any later continuous row;
carry-specific raw price and curve-leg caveats for S10/S11/P06/P07.
```

## Future Product Families

The future evidence ledgers must cover the current 16-symbol pilot families:

```text
ZT, ZF, ZN: Treasury rates
MES, MNQ, M2K, MYM: Equity index
QM, RB: Energy
ZC, ZS, ZM, ZL, ZW: Agriculture grains/oilseeds
HE, LE: Livestock
```

Every row must default to:

```text
STRATEGY_USE_STATUS: BLOCKED_PENDING_CONTINUOUS_ROLL_POLICY
```

## Required Future Status Decisions

The future execution must classify each symbol/family as one of:

```text
EVIDENCE_READY_FOR_POLICY_DECISION
EVIDENCE_PARTIAL_REQUIRES_MORE_STATIC_SOURCE
EVIDENCE_BLOCKED_PROVIDER_SEMANTICS_UNCLEAR
EVIDENCE_BLOCKED_EXCHANGE_LIFECYCLE_UNCLEAR
EVIDENCE_BLOCKED_SETTLEMENT_CLOSE_UNCLEAR
EVIDENCE_BLOCKED_LINEAGE_UNCLEAR
```

No status may imply strategy readiness.

## Automatic Audit Requirement

The future execution must preserve an automatic lean hostile audit result covering:

```text
source/provider evidence boundaries
no provider API or login
no market data download
no market-row parsing
no continuous-series construction
no strategy input
no ZN precedent promoted globally
no dated-contract fragment promoted to strategy input
no diagnostics/backtests/forecasts/positions/costs/carry/trend/risk
```

## Next Gate After Future Execution

If the future evidence execution passes, the next clean gate should be:

```text
CARVER_SOURCE_NATIVE_CONTINUOUS_ROLL_DAILY_DATA_POLICY_DECISION_GATE
```

That later decision would choose whether to:

```text
use provider-built continuous series as reference-only;
use provider-built continuous series as source authority after lineage proof;
build local continuous series from dated contracts;
require official settlement/close evidence first;
keep continuous/roll strategy input blocked.
```

## Non-Authorization

This draft authorizes no provider API access, no provider login, no new market-data request, no data download, no market-row parsing, no table execution, no continuous-contract download, no continuous-series construction, no diagnostics, no backtests, no forecasts, no positions, no costs, no carry, no trend, no volatility/risk calculations, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.
