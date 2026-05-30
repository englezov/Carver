# Carver Daily Data Foundation Next-Step Handoff Decision

Date: 2026-05-30

Status:

```text
PROCESS_ONLY_CARVER_DAILY_DATA_FOUNDATION_NEXT_STEP_HANDOFF_DECISION_NOT_DATA_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Record the clean handoff after the process-only daily data foundation shape gates.

This decision identifies the next separately authorized gates needed to move from:

```text
quarantined dated-contract archive
```

to:

```text
plumbing-only Development/Reconciliation table
```

and then eventually to:

```text
source-native continuous/rolled daily futures strategy input
```

without silently promoting dated-contract fragments into strategy machinery.

## Current Completed Process Inputs

Decision and review:

```text
docs/process/CARVER_16_SYMBOL_DAILY_LIBRARY_DEV_RECON_OR_CONTINUOUS_ROLL_DECISION_GATE_2026-05-30.md
docs/process/CARVER_16_SYMBOL_DAILY_LIBRARY_LOCAL_HOSTILE_READINESS_REVIEW_2026-05-30.md
```

Shape gates:

```text
docs/process/CARVER_16_SYMBOL_DATED_CONTRACT_FRAGMENT_DEV_RECON_TABLE_SHAPE_GATE_2026-05-30.md
docs/process/CARVER_SOURCE_NATIVE_CONTINUOUS_ROLL_DAILY_DATA_SEMANTICS_SHAPE_GATE_2026-05-30.md
```

Lean audit:

```text
docs/process/CARVER_DAILY_DATA_FOUNDATION_SHAPE_GATES_LEAN_HOSTILE_AUDIT_RESULT_2026-05-30.md
AUDIT_DISPOSITION: PASS_PROCESS_ONLY_DAILY_DATA_FOUNDATION_SHAPE_GATE_SCOPE
```

## Current Foundation State

The source-native daily data foundation has:

```text
SOURCE_NATIVE_FUTURES lane
16 locked manifest symbols
4568 quarantined Databento dated-contract archive rows
4483 normal provider-condition rows eligible for plumbing-only fragment table
85 degraded provider-condition rows excluded/quarantined
0 blocked or unresolved provider-condition rows
non-strategy schema/date join smoke test pass
```

The foundation does not yet have:

```text
executed dated-contract fragment Dev/Reconciliation table
continuous or rolled daily strategy series
roll rule
back-adjustment policy
settlement/close policy
carry-leg policy
strategy-facing data input
diagnostics
backtests
forecasts
positions
costs
carry
trend
volatility/risk calculations
promotion
```

## Decision

Selected next concrete gate:

```text
CARVER_16_SYMBOL_DATED_CONTRACT_FRAGMENT_DEV_RECON_TABLE_EXECUTION_GATE
```

Execution boundary if separately authorized:

```text
READ_EXISTING_LOCAL_QUARANTINE_ARTIFACTS_ONLY
CREATE_PLUMBING_ONLY_TABLE_FROM_4483_NORMAL_PROVIDER_CONDITION_ROWS
EXCLUDE_85_DEGRADED_ROWS
PRESERVE_HASH_LINEAGE
LABEL_NOT_STRATEGY_INPUT_NOT_BACKTEST_READY
NO_PROVIDER_ACCESS
NO_NEW_DOWNLOAD
NO_STRATEGY_MATH
```

Required parallel/next semantic gate before broad strategy machinery:

```text
CARVER_SOURCE_NATIVE_CONTINUOUS_ROLL_DAILY_DATA_SEMANTICS_EVIDENCE_PACKET
```

Purpose:

```text
IDENTIFY_SOURCE_AND_PROVIDER_EVIDENCE_FOR_ROLL_CONTINUOUS_DAILY_STRATEGY_SERIES
```

## Why This Order

The dated-contract fragment table can prove:

- schema loading;
- manifest enforcement;
- row exclusion mechanics;
- completed-date joins;
- hash lineage;
- downstream interface plumbing.

It cannot prove:

- continuous history;
- roll logic;
- back-adjusted price semantics;
- settlement/close semantics;
- strategy readiness;
- performance relevance.

Therefore the next execution should be the small, fenced table only if separately authorized, while the strategic foundation must continue through continuous/roll evidence before any book strategy machinery.

## Required Execution Gate Conditions

Before the dated-contract fragment table can be executed, the execution gate must explicitly authorize:

```text
local parsing of existing sanitized/provider-condition/validation CSV artifacts only
creation of the four output artifacts named by the shape gate
automatic lean hostile audit result preservation
```

The execution gate must not authorize:

```text
provider API access
new market-data request
new data download
raw archive modification
continuous-series construction
strategy-facing interpretation
returns
diagnostics
backtests
forecasts
positions
costs
carry
trend
volatility/risk calculations
OOS
Lockbox
Forward
CFD adapters
old QuantLab active-pipeline use
tuning
deployment
trading
promotion
Git staging
commit
push
PR update/opening
remote operations
```

## Required Continuous/Roll Evidence Gate Conditions

Before continuous/rolled daily data can be built, the evidence packet must identify:

```text
Carver source framing for price series and roll expectations
Databento continuous-contract capability and documentation if considered
exchange lifecycle evidence for front/next selection
roll trigger candidates and evidence
settlement versus close evidence
adjustment policy candidates
provider-condition gap policy
lineage requirements from continuous row back to dated contracts
fail-closed rules for missing or degraded rows
```

No continuous-contract download, provider API call, or market-row parsing is opened by this decision.

## Non-Authorization

This handoff decision authorizes no provider API access, no new market-data request, no data download, no market-row parsing, no table execution, no continuous-series construction, no diagnostics, no backtests, no forecasts, no positions, no costs, no carry, no trend, no volatility/risk calculations, no OOS, no Lockbox, no Forward, no CFD adapter execution, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.
