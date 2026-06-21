# Carver S09 MES Official Lifecycle Roll Semantics Annual Risk And Cost Source Lock Gate

Date: 2026-06-03

Status:

```text
PROCESS_ONLY_S09_MES_SOURCE_LOCK_GATE_NOT_EXECUTION_NOT_BACKTEST
```

## Purpose

Define the next clean gate after:

```text
docs/process/CARVER_S09_MES_CONTINUOUS_LINEAGE_RISK_COST_ELIGIBILITY_EXECUTION_RESULT_2026-06-03.md
```

That prior execution built a provisional local MES daily continuous lineage from the existing Databento dated-contract quarantine archive. It intentionally failed closed:

```text
FAIL_CLOSED_S09_MES_STRATEGY_INPUT_NOT_READY_LIFECYCLE_RISK_COST_SPEED_NOT_LOCKED
```

This gate defines the exact evidence and outputs required to turn that provisional lineage into a strategy-input candidate, or to keep it fail-closed, before any S09 forecast or backtest.

## Current Decision On Databento Access

Operator has authorized Databento API access if needed at this stage.

This gate does not currently need a Databento OHLCV request, a new provider download, or a wider symbol/window request. Existing local S09 MES Databento artifacts already contain the dated-contract daily bars and Databento definition cross-checks needed for the provisional lineage.

Databento may be used later only for metadata/symbology/definition cross-checks explicitly named by the execution gate. It must not be used to request new OHLCV rows, continuous contracts, expanded symbols, or expanded windows under this process-only artifact.

## Lane

```text
SOURCE_NATIVE_FUTURES
```

No CFD assumptions, CFD symbols, prop-firm fees, broker-clock sessions, old `QuantLab_v3` active-pipeline state, provider-built continuous series, or performance-informed roll choices may be used as source authority.

## Required Execution Gate Name

A later separately authorized execution should use:

```text
S09_MES_OFFICIAL_LIFECYCLE_ROLL_SEMANTICS_ANNUAL_RISK_AND_COST_SOURCE_LOCK_EXECUTION_GATE
```

## Locked Inputs

The later execution may inspect only:

- the S09 source atom and synthetic conformance artifacts;
- the S09 MES daily Databento expansion artifacts;
- the S09 MES provisional continuous lineage artifacts;
- current local Carver process/source artifacts;
- `Carver.pdf` for book-source atoms;
- official/static CME, exchange, broker/fee, and Databento metadata or definition evidence explicitly named by the execution gate.

The later execution must preserve the MES root and the current Development/Reconciliation target window:

```text
root: MES
row_id: APPENDIX_C_174_006
target_window: 2022-01-03 through 2023-12-29
source_dated_contracts:
  MESH1
  MESM1
  MESU1
  MESZ1
  MESH2
  MESM2
  MESU2
  MESZ2
  MESH3
  MESM3
  MESU3
  MESZ3
  MESH4
```

## Required Evidence Locks

### 1. Official MES Lifecycle Evidence

Lock or fail-close official/static evidence for every contract in the MES chain:

```text
product family
venue/exchange normalization
currency
contract multiplier
point value
minimum tick
tick value
quarterly/month code cycle
cash-settlement status
last-trade / termination / final-settlement blocker
listed/active status for the relevant historical contract
source URL or local static file
source SHA256 or immutable archive hash
```

Databento definitions may cross-check product code, expiration timestamp, venue, currency, multiplier, and tick size, but they may not replace missing official/static lifecycle evidence.

### 2. Roll Trading-Date Semantics

Resolve or fail-close whether the current provider-date roll plan can be treated as Carver completed daily bars.

The execution must decide:

```text
provider_timestamp_authority
provider_trading_date_authority
exchange_local_session_date_authority
Sunday/holiday row policy
roll buffer count basis
roll date if buffer lands on non-business or Sunday provider label
old/new overlap search calendar
```

Current provisional state:

```text
roll_plan_status: PROVISIONAL_PROVIDER_DATE_ROLL_PLAN_TRADING_DAY_SEMANTICS_NOT_LOCKED
```

No S09 forecast may be computed while this remains unresolved.

### 3. S03 Annual-Risk Runtime

Lock or fail-close the upstream annual percentage risk runtime needed by S09 daily price risk.

The execution must cite and lock:

```text
annual percentage risk method
short volatility component
long-run volatility component if used
blend or floor/cap behavior if used
annualization convention
warm-up requirement
first usable date
missing/degraded row policy
no-lookahead rule
timestamp alignment to completed daily bar
```

If the 2021-01-01 warm-up start is insufficient for a source-faithful annual-risk runtime on 2022-01-03, the result must fail closed and name the required additional pre-window history.

### 4. Daily Price-Risk Runtime

The source-locked S09 conversion remains:

```text
daily_price_risk = current_price * annual_percentage_risk / 16
```

The execution must prove that `current_price`, `annual_percentage_risk`, and the emitted `daily_price_risk` share the same completed-bar timestamp and do not use current/future unavailable state.

### 5. Source-Native MES Cost Source

Lock or fail-close a source-native cost source for MES. Required fields:

```text
commission source
exchange fee source
clearing/NFA/regulatory fee source where applicable
bid/ask spread or slippage treatment
per-side versus round-turn convention
currency
contract multiplier/point-value conversion
effective date or historical applicability
source URL or local static file
source SHA256 or immutable archive hash
```

Forbidden substitutes:

```text
CFD spreads
prop-firm fee schedules
old QuantLab adapter costs
ETF placeholder costs
post-result cost choices
```

If spread or slippage cannot be source-locked, the cost ledger must label the resulting S09 eligibility status as fail-closed or explicitly limited to a commission/fee-only development diagnostic that is not strategy-ready.

### 6. Risk-Adjusted Cost And Speed Eligibility

Lock or fail-close:

```text
risk_adjusted_cost_per_trade
0.15 SR cost threshold production interpretation
speed-specific turnover/cost eligibility
eligible EWMAC speed set
Table 36 FDM row selected by the eligible speed set
```

No default assumption that all six speeds survive is allowed.

## Required Output Artifacts For The Later Execution

The later execution should write under a locked S09 MES source-lock output root and produce:

```text
official_lifecycle_evidence_ledger.csv
roll_trading_date_semantics_decision.md
annual_risk_runtime_source_lock.md/csv
daily_price_risk_runtime_lock.csv
mes_source_native_cost_source_ledger.csv
risk_adjusted_cost_and_speed_eligibility_ledger.csv
strategy_input_readiness_status.json/csv
provenance.md
sha256_manifest.json/csv
local_hostile_audit_result.md
```

The strategy input may be marked ready only if all statuses pass:

```text
official_lifecycle_evidence_status == LOCKED
roll_trading_day_semantics_status == LOCKED
annual_risk_runtime_status == LOCKED
daily_price_risk_runtime_status == LOCKED
cost_source_status == LOCKED
risk_adjusted_cost_status == LOCKED
speed_cost_eligibility_status == LOCKED
eligible_speed_set_status == LOCKED
strategy_input_readiness_status == READY_FOR_S09_DEV_RECON_FORECAST_GATE_NOT_BACKTEST
```

Any unresolved status must preserve:

```text
FAIL_CLOSED_S09_MES_STRATEGY_INPUT_NOT_READY
```

## Stop Boundary

Passing this source-lock gate would not authorize a backtest. The next gate after a clean pass would be a separate S09 MES Development/Reconciliation forecast-only gate, followed only later by a separately authorized Development/Reconciliation backtest gate.

## Non-Authorization

This artifact authorizes no Databento OHLCV request, no provider login, no new data download, no market-row parsing, no continuous-lineage reconstruction, no risk runtime execution, no cost computation, no S09 forecast computation, no diagnostics, no backtests, no returns, no PnL, no Sharpe, no drawdown, no positions, no carry, no CFD adapter work, no old QuantLab active-pipeline use, no tuning, no TEST, no VALIDATION, no OOS, no Lockbox, no Forward, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.
