# Carver S27 EWMAC16 Trend Source Gate Result

Date: 2026-05-31

Status:

```text
FAIL_CLOSED_S27_EWMAC16_TREND_RUNTIME_SOURCE_BACK_ADJUSTED_CONTINUOUS_DAILY_NOT_AVAILABLE
```

## Gate

```text
S27_EWMAC16_TREND_OVERLAY_REAL_HOURLY_SOURCE_GATE
```

## Purpose

Decide whether the current Carver workspace can source-faithfully emit the real S27 EWMAC(16,64) trend runtime ledger aligned to the S26 ZN extended forecast-series-only rows.

This gate performs no provider API access, no data download, no new market-row parsing, no diagnostics, no backtests, no positions, no costs, no carry, no S27 forecast execution, no testing, and no promotion.

## Source Requirement

S27 source atoms require:

```text
trend dependency: EWMAC(16,64), shorthand EWMAC16
trend input: back-adjusted prices for the trend overlay
trend role: overlay/condition; not a co-weighted forecast block
```

Current source-atom record:

```text
docs/process/CARVER_S26_S27_SOURCE_ATOM_SHEET_2026-05-30.md
```

The S26 ZN extended forecast-series-only bridge now exists, but that does not by itself provide the S27 trend input.

## Evidence Inspected

Continuous/roll policy decision:

```text
docs/process/CARVER_SOURCE_NATIVE_CONTINUOUS_ROLL_DAILY_DATA_POLICY_DECISION_2026-05-30.md
SHA256: ACF98D89492626474450776D1337DCA7D8879D9FFA273AEDE3DE91BB6A14D2DF
```

Current local continuous daily lineage policy status:

```text
docs/researchops/source_native_futures_daily_data_library/local_continuous_daily_lineage/16_SYMBOL/2026-05-30_ROLL_CHAIN_EXPANSION_RERUN/CARVER_16_SYMBOL_LOCAL_CONTINUOUS_DAILY_POLICY_STATUS_2026-05-30.csv
SHA256: DBFA60F914E9AFE287A8418C5DFAC7C18E53B2287A0C8C9D51C21C019DE64AEB
```

Current local continuous daily roll plan:

```text
docs/researchops/source_native_futures_daily_data_library/local_continuous_daily_lineage/16_SYMBOL/2026-05-30_ROLL_CHAIN_EXPANSION_RERUN/CARVER_16_SYMBOL_LOCAL_CONTINUOUS_DAILY_ROLL_PLAN_2026-05-30.csv
SHA256: B562A35472FEBCE4B7B8EA3E524E8A4BDE2D58A7DB4E285E360F8465E35AA7F2
```

## Current Continuous-Lineage State

The local continuous status ledger records:

```text
execution_status: LOCAL_CONTINUOUS_DAILY_LINEAGE_RERUN_FAIL_CLOSED_LIFECYCLE_EVIDENCE_MISSING_NO_SERIES_CONSTRUCTED
continuous_series_constructed: NO
strategy_input_created: NO
trend_computed: NO
provider_built_continuous_used_as_source: NO
provider_api_access: NO_LOCAL_RERUN_USED_EXISTING_AUTHORIZED_EXPANSION_ARTIFACTS
```

The ZN roll-plan row records:

```text
book_symbol: ZN
old_source_contract: ZNH6
new_source_contract: ZNM6
roll_transition_date: BLOCKED_NO_ROLL_TRANSITION_DATE
first_notice_blocker_status: BLOCKED_LIFECYCLE_EVIDENCE_NOT_LOCKED
last_trade_blocker_status: BLOCKED_LIFECYCLE_EVIDENCE_NOT_LOCKED
expiration_or_final_settlement_blocker_status: BLOCKED_LIFECYCLE_EVIDENCE_NOT_LOCKED
roll_plan_status: ROLL_PLAN_BLOCKED_LIFECYCLE_EVIDENCE_MISSING
blocker: ADJACENT_DATED_CONTRACT_ROWS_AVAILABLE_BUT_STATIC_LIFECYCLE_BLOCKER_DATES_NOT_LOCKED_FOR_ROLL_TRANSITION_SELECTION
```

## Decision

```text
S27_EWMAC16_REAL_TREND_RUNTIME_LEDGER: NOT_EMITTED
S27_EWMAC16_SOURCE_STATUS: FAIL_CLOSED_BACK_ADJUSTED_CONTINUOUS_DAILY_NOT_AVAILABLE
```

Reason:

The source-faithful S27 trend overlay needs a locked back-adjusted continuous daily price input. The current Carver continuous-lineage path explicitly has no constructed continuous series and no strategy input. Provider-built continuous symbols are reference-only under the current policy. Dated ZNM6 closes are useful evidence but are not a substitute for a source-locked back-adjusted continuous trend input.

## Forbidden Substitutions

This gate explicitly rejects:

```text
NO_DATED_ZNM6_CLOSES_AS_EWMAC16_TREND_INPUT
NO_PROVIDER_BUILT_CONTINUOUS_SERIES_AS_SOURCE_AUTHORITY
NO_UNADJUSTED_CONTINUOUS_PRICE_AS_BACK_ADJUSTED_INPUT
NO_MES_SP500_OR_OTHER_INSTRUMENT_SUBSTITUTE
NO_DAILY_TREND_RUNTIME_ROW_WITHOUT_LINEAGE
NO_S27_FORECAST_SERIES_EXECUTION
```

## Next Required Gate

For the ZN worked-example path:

```text
ZN_LOCAL_CONTINUOUS_DAILY_LIFECYCLE_EVIDENCE_AND_LINEAGE_REPAIR_GATE
```

Minimum requirement:

```text
Resolve or fail-close the ZN lifecycle blocker evidence for ZNH6 -> ZNM6, select a deterministic roll transition date, construct a local additive back-adjusted continuous daily ZN lineage with explicit source rows and hashes, then separately emit an S27 EWMAC16 trend runtime ledger aligned to the S26 forecast rows.
```

Alternative if the operator chooses not to repair local continuous lineage:

```text
S27_REMAINS_BLOCKED_AT_REAL_TREND_RUNTIME_DEPENDENCY
```

## Non-Authorization

This result authorizes no provider API access, no data download, no market-row parsing beyond read-only inspection of existing local ledgers, no continuous-series construction, no trend computation, no S27 forecast computation, no diagnostics, no backtests, no returns, no PnL, no positions, no orders, no fills, no costs, no carry, no volatility/risk calculation, no testing, no OOS, no Lockbox, no Forward, no CFD adapters, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.
