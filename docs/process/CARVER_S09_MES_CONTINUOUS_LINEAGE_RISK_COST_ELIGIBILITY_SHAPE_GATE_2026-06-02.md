# Carver S09 MES Continuous Lineage Risk Cost Eligibility Shape Gate

Date: 2026-06-02

Status:

```text
PROCESS_ONLY_S09_MES_CONTINUOUS_LINEAGE_RISK_COST_ELIGIBILITY_SHAPE_NOT_EXECUTION_NOT_BACKTEST
```

## Purpose

Define the exact next execution gate after the successful MES Databento daily expansion:

```text
docs/process/CARVER_S09_MES_DEV_RECON_DATA_EXPANSION_RESULT_2026-06-02.md
```

The expansion produced quarantine-only dated-contract MES daily rows. It did not create an S09 strategy-facing input.

This shape gate defines what a later separately authorized execution must prove before any S09 Development/Reconciliation backtest can be opened.

## Lane

```text
SOURCE_NATIVE_FUTURES
```

No CFD assumptions, CFD symbols, CFD costs, CFD sessions, broker clocks, old adapter code, old `QuantLab_v3` active-pipeline state, or provider-built continuous symbols may be used as source authority.

## Current Inputs

Primary expansion artifacts:

```text
docs/researchops/s09/mes_dev_recon_data_expansion/2022-01-03_2023-12-29/
```

Expansion status:

```text
PASS_S09_MES_DAILY_EXPANSION_QUARANTINE_ONLY_NOT_LINEAGE_NOT_BACKTEST
```

Locked dated-contract source symbols:

```text
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

Target Development/Reconciliation comparison window:

```text
2022-01-03 through 2023-12-29
```

Quarantine row status:

```text
sanitized_rows: 3018
target_window_rows: 2065
provider_errors: 0
failed_validation_checks: 0
degraded_or_unresolved_provider_condition_rows: 5
```

The 5 degraded/unresolved rows remain quarantined and may not become strategy input.

## Execution Gate Name

The next execution gate, if separately authorized, should be:

```text
S09_MES_CONTINUOUS_LINEAGE_RISK_COST_ELIGIBILITY_EXECUTION_GATE
```

## Required Execution Scope

A future execution may use only:

- the current MES S09 source-atom/synthetic-conformance artifacts;
- the MES preflight artifact and audit record;
- the MES Databento daily expansion gate/result/audit records;
- the hash-bound MES expansion output tree;
- official/static CME or provider lifecycle evidence explicitly named by the execution gate;
- static fee/cost evidence explicitly named by the execution gate.

It may not call Databento, request new data, inspect new symbols, download continuous contracts, parse provider-built continuous symbols, or expand the window unless separately authorized.

## Required Output Root

If execution is authorized, write only under:

```text
docs/researchops/s09/mes_continuous_lineage_risk_cost_eligibility/2022-01-03_2023-12-29/
```

Required artifact classes:

- input-hash manifest;
- provider-condition admission ledger;
- official/static lifecycle evidence ledger;
- roll-plan ledger;
- local additive back-adjustment ledger;
- source-lineage ledger;
- local continuous daily MES series ledger;
- annual percentage risk readiness/runtime ledger;
- daily price-risk runtime ledger;
- cost-source and risk-adjusted-cost ledger;
- S09 speed/cost eligibility ledger;
- strategy-facing-input readiness status;
- provenance/status/SHA records;
- local hostile audit record.

## Provider-Condition Admission Rule

Admit a dated-contract row only when all are true:

```text
lane_class == SOURCE_NATIVE_FUTURES
provider == DATABENTO_HISTORICAL
dataset == GLBX.MDP3
schema == ohlcv-1d
root == MES
raw_symbol in locked MES raw-symbol set
provider_condition_classification == NORMAL_PROVIDER_CONDITION
strategy_readiness_status == QUARANTINE_ONLY_NOT_STRATEGY_INPUT before admission
timestamp is provider UTC daily bar timestamp
source_raw_sha256 is present
```

Reject, label, and count:

```text
degraded provider-condition rows
unknown provider-condition rows
duplicate raw_symbol/date rows
non-MES rows
non-ohlcv-1d rows
provider-built continuous rows
ES/NQ/full-size substitute rows
unhashable rows
filled/interpolated/repaired rows
```

## Lifecycle Evidence Requirement

The execution gate must use hash-bound static official/source-native lifecycle evidence for MES contracts sufficient to lock, for each roll transition:

```text
product family = Micro E-mini S&P 500 futures
venue/exchange normalization
currency
contract month cycle
cash-settled lifecycle class
expiration / termination / final-settlement blocker date
first normal-provider old/new overlap date on or before the roll buffer
```

Databento definition metadata may be used as a cross-check, but cannot silently replace official/static lifecycle evidence if blocker dates are missing or ambiguous.

## Roll Rule

Locked first-pass roll class:

```text
STATIC_LIFECYCLE_BUFFER_ROLL
```

MES lifecycle class:

```text
CASH_SETTLED_EQUITY_INDEX
```

Roll rule:

```text
cash_settled_roll_buffer = 5 completed trading days before the earliest locked expiration, termination, or final-settlement blocker
roll_transition_date = latest completed trading date on or before the buffer date where both old and new source contracts have normal provider-condition rows
search_order = descending from buffer date toward earlier dates
fallback_if_lifecycle_blocker_missing = FAIL_CLOSED_LIFECYCLE_EVIDENCE_MISSING
fallback_if_old_new_overlap_missing = FAIL_CLOSED_ROLL_PAIR_MISSING
fallback_if_provider_condition_not_normal = FAIL_CLOSED_PROVIDER_CONDITION_NOT_NORMAL_ON_ROLL_PAIR
```

Expected transition family, subject to official lifecycle evidence:

```text
MESH1 -> MESM1
MESM1 -> MESU1
MESU1 -> MESZ1
MESZ1 -> MESH2
MESH2 -> MESM2
MESM2 -> MESU2
MESU2 -> MESZ2
MESZ2 -> MESH3
MESH3 -> MESM3
MESM3 -> MESU3
MESU3 -> MESZ3
MESZ3 -> MESH4
```

Forbidden roll triggers:

```text
volume switch
open-interest switch
provider smart-symbol roll
provider-built continuous roll date
manual convenience roll
post-result roll-date adjustment
strategy-performance-informed roll choice
```

## Back-Adjustment Requirement

If roll transitions pass, construct a local additive back-adjusted daily close series only for Development/Reconciliation.

Required labels:

```text
adjustment_method = LOCAL_ADDITIVE_BACK_ADJUSTMENT_OLD_HISTORY_TO_NEW_CONTRACT_LEVEL
adjusted_price_semantics = LOCAL_BACK_ADJUSTED_TRADE_BAR_CLOSE_NOT_OFFICIAL_SETTLEMENT
provider_built_adjustment = NO
ratio_adjustment = NO
strategy_use_scope = DEVELOPMENT_RECONCILIATION_ONLY
```

For each roll, record:

```text
roll_transition_date
old_contract
new_contract
old_close_on_roll_date
new_close_on_roll_date
roll_gap_or_offset
cumulative_adjustment_before_roll
adjustment_applies_to_dates_before
source_old_row_sha256
source_new_row_sha256
```

## Annual Risk And Daily Price Risk Requirement

The existing S09 source gate locks only the conversion:

```text
daily_price_risk = current_price * annual_percentage_risk / 16
```

The execution gate must still lock or fail-close the upstream annual percentage risk runtime.

Required annual-risk evidence:

```text
completed normal-provider continuous daily rows only
no current/future-row leakage
S03-family volatility convention explicitly cited or separately locked
first usable date after warm-up explicitly recorded
missing/gap/degraded-row behavior explicitly recorded
annualization convention = 256 trading days
```

The execution gate must fail closed if the requested 2022-2023 window does not have enough pre-window context to compute the chosen annual-risk runtime without leakage.

Daily price-risk rows may be emitted only after annual-risk runtime passes. They must align exactly to completed daily bars and may not use a stale or future risk timestamp.

## Cost And Speed Eligibility Requirement

S09 cannot assume all six EWMAC speeds survive real-data cost filtering.

The execution gate must lock or fail-close:

```text
MES commission/fee source
MES contract multiplier and point value
per-trade cost in source-native units
risk-adjusted cost per trade
0.15 SR threshold interpretation
speed-specific turnover/cost eligibility rule
eligible EWMAC speed set
Table 36 FDM row for the eligible speed set
```

If cost evidence is unavailable, ambiguous, or not source-native, the result must be:

```text
FAIL_CLOSED_S09_MES_COST_ELIGIBILITY_NOT_LOCKED
```

No CFD/prop-firm fee schedule may substitute for source-native futures cost evidence.

## Strategy-Facing Input Readiness

The future execution may mark the MES series strategy-facing only if all pass:

```text
continuous_lineage_status == PASS
roll_plan_status == PASS
back_adjustment_status == PASS
provider_condition_admission_status == PASS_NORMAL_ROWS_ONLY
annual_risk_runtime_status == PASS
daily_price_risk_runtime_status == PASS
cost_source_status == PASS
risk_adjusted_cost_status == PASS
speed_cost_eligibility_status == PASS
eligible_speed_set_status == PASS
```

Otherwise it must fail closed and explicitly record blockers.

## Non-Authorization

This shape gate authorizes no provider API access, no new data download, no market-row parsing, no continuous lineage construction, no risk runtime execution, no cost execution, no S09 forecast computation, no diagnostics, no backtests, no returns, no PnL, no Sharpe, no drawdown, no positions, no carry, no CFD adapter work, no old QuantLab pipeline use, no tuning, no TEST, no VALIDATION, no OOS, no Lockbox, no Forward, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update, and no remote repository operations.
