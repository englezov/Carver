# Carver S09 MES Single-Index Root Continuous Lineage And Cost Eligibility Preflight

Date: 2026-06-02

Status:

```text
PROCESS_ONLY_S09_MES_PREFLIGHT_FAIL_CLOSED_NOT_DATA_NOT_BACKTEST
```

## Purpose

Execute the process-only preflight recommended by:

```text
docs/process/CARVER_S09_DEV_RECON_DATA_BACKTEST_READINESS_GATE_2026-06-02.md
```

This preflight chooses one index root for the first S09 single-instrument path and records whether existing local process/source artifacts are enough to proceed to a later Development/Reconciliation backtest gate.

## Decision

Selected first S09 index root:

```text
MES
```

Reason:

- MES is Carver Appendix C source-native micro S&P 500 exposure.
- MES is present in the Databento 16-symbol daily library candidate set.
- MES is a direct micro index future and does not require full-size `ES` signal substitution.
- The operator's current interest is index trend following, not bonds.

No `ES` or `NQ` substitution is authorized by this preflight.

## Evidence Inspected

Only process/source metadata and readiness records were inspected. No raw OHLCV rows were parsed and no provider/API access occurred.

### MES Canonical Manifest Row

Source:

```text
docs/researchops/source_native_futures_daily_data_library/16_SYMBOL_DAILY_LIBRARY_PROMOTION_READINESS/manifest/CARVER_16_SYMBOL_DATABENTO_DAILY_LIBRARY_CANONICAL_MANIFEST_2026-05-30.csv
```

MES row summary:

```text
row_id: APPENDIX_C_174_006
author_market_code: MES
descriptive_name: S&P 500 (micro)
provider: DATABENTO
dataset: GLBX.MDP3
schema: ohlcv-1d
databento_raw_symbol: MESM6
databento_instrument_id: 42005163
selected_source_native_dated_contract: MES_JUN_2026
selected_ninjatrader_local_contract: MES 06-26
first_completed_trading_date: 2025-04-09
last_completed_trading_date: 2026-05-29
archive_row_count: 232
provider_condition_normal_rows: 225
provider_condition_degraded_quarantined_rows: 7
strategy_facing_candidate_rows_after_excluding_degraded: 225
strategy_facing_readiness_status: PROMOTION_READINESS_CANDIDATE_NORMAL_ROWS_ONLY_NOT_DIAGNOSTIC_NOT_BACKTEST
```

Interpretation:

```text
MES_CURRENT_DATED_CONTRACT_FRAGMENT_READY_FOR_LIBRARY_PROMOTION_CANDIDATE_ONLY
MES_NOT_READY_FOR_S09_BACKTEST
```

The current MES row is a current 2026 dated-contract fragment, not a complete two-year S09 backtest input.

### 16-Symbol Daily Library Status

Source:

```text
docs/researchops/source_native_futures_daily_data_library/16_SYMBOL_DAILY_LIBRARY_PROMOTION_READINESS/provenance/CARVER_16_SYMBOL_DAILY_LIBRARY_PROMOTION_READINESS_STATUS_2026-05-30.csv
```

Status summary:

```text
manifest_rows: 16
archive_rows: 4568
normal_candidate_rows: 4483
degraded_quarantined_rows: 85
other_blocked_or_unresolved_rows: 0
diagnostics_run: NO
backtests_run: NO
forecasts_computed: NO
positions_computed: NO
strategy_data_file_created: NO
status: PASS_CANONICAL_MANIFEST_PROMOTION_READINESS_NORMAL_ROWS_ONLY_DEGRADED_ROWS_QUARANTINED
```

Interpretation:

```text
16_SYMBOL_LIBRARY_PROMOTION_READY_FOR_NON_STRATEGY_USE_ONLY
NOT_S09_STRATEGY_READY
```

### MES Adjacent Contract Availability

Source:

```text
docs/researchops/source_native_futures_daily_data_library/local_continuous_daily_lineage/16_SYMBOL/2026-05-30_ROLL_CHAIN_EXPANSION_RERUN/CARVER_16_SYMBOL_LOCAL_CONTINUOUS_DAILY_ADJACENT_PAIR_AVAILABILITY_2026-05-30.csv
```

MES summary:

```text
MES,MESH6,MESM6,MESU6,...,ADJACENT_OLD_NEW_NORMAL_ROWS_AVAILABLE
```

Interpretation:

```text
MES_ADJACENT_ROWS_AVAILABLE_FOR_CURRENT_CHAIN_RECONCILIATION
```

This clears the prior adjacent-row availability blocker for the current chain only. It does not itself select a roll date or construct a continuous series.

### MES Roll Plan Status

Source:

```text
docs/researchops/source_native_futures_daily_data_library/local_continuous_daily_lineage/16_SYMBOL/2026-05-30_ROLL_CHAIN_EXPANSION_RERUN/CARVER_16_SYMBOL_LOCAL_CONTINUOUS_DAILY_ROLL_PLAN_2026-05-30.csv
```

MES summary:

```text
MES
STATIC_LIFECYCLE_BUFFER_ROLL
MESH6 -> MESM6
BLOCKED_NO_ROLL_TRANSITION_DATE
BLOCKED_LIFECYCLE_EVIDENCE_NOT_LOCKED
ROLL_PLAN_BLOCKED_LIFECYCLE_EVIDENCE_MISSING
```

Interpretation:

```text
MES_CONTINUOUS_LINEAGE_BLOCKED_LIFECYCLE_EVIDENCE_REQUIRED
```

### Local Continuous Daily Rerun Status

Source:

```text
docs/researchops/source_native_futures_daily_data_library/local_continuous_daily_lineage/16_SYMBOL/2026-05-30_ROLL_CHAIN_EXPANSION_RERUN/CARVER_16_SYMBOL_LOCAL_CONTINUOUS_DAILY_POLICY_STATUS_2026-05-30.csv
```

Relevant status:

```text
execution_status: LOCAL_CONTINUOUS_DAILY_LINEAGE_RERUN_FAIL_CLOSED_LIFECYCLE_EVIDENCE_MISSING_NO_SERIES_CONSTRUCTED
continuous_series_constructed: NO
strategy_input_created: NO
forecasts_computed: NO
backtests_run: NO
costs_computed: NO
trend_computed: NO
```

Interpretation:

```text
NO_S09_CONTINUOUS_DAILY_INPUT_EXISTS_YET
```

### Daily Price Risk Status

Existing S09 daily price-risk conversion gate:

```text
docs/process/CARVER_S09_DAILY_PRICE_RISK_SOURCE_GATE_2026-05-29.md
```

Locked:

```text
daily_price_risk = current_price * annual_percentage_risk / 16
```

Still unresolved for MES:

```text
annual_percentage_risk source
completed-bar-only risk history
warm-up / first usable date
missing-row handling
MES-specific runtime ledger
```

### Cost And Speed Eligibility Status

S09 source atom:

```text
0.15 SR cost threshold
Table 35 turnover references
Table 36 FDM rows after eligible speed-set selection
```

Current MES machine state:

```text
MES_COST_SOURCE: NOT_LOCKED
MES_RISK_ADJUSTED_COST_PER_TRADE: NOT_LOCKED
MES_SPEED_COST_ELIGIBILITY: NOT_LOCKED
MES_ELIGIBLE_EWMAC_SPEED_SET_FOR_REAL_BACKTEST: NOT_LOCKED
```

No S09 real-data backtest may silently assume that all six EWMAC speeds survive cost filtering.

## Preflight Verdict

```text
SELECTED_ROOT: MES
S09_MES_CURRENT_STATUS: FAIL_CLOSED_NOT_READY_FOR_BACKTEST
```

Blocking conditions:

1. Current MES local daily data is only a 2025-04-09 through 2026-05-29 current-contract fragment, not a complete Development/Reconciliation backtest window.
2. No MES local continuous daily series has been constructed.
3. MES roll transition selection is blocked because lifecycle evidence is not locked.
4. MES daily annual percentage risk runtime is not locked.
5. MES cost source and risk-adjusted cost per trade are not locked.
6. MES S09 speed/cost eligibility is not locked.
7. No S09 MES strategy-facing table, forecast runtime, position runtime, cost runtime, diagnostic, or backtest exists.

## Required Next Gate

The next clean gate is:

```text
S09_MES_DEV_RECON_DATA_EXPANSION_AND_LINEAGE_REPAIR_GATE
```

That future gate must decide whether to:

- request Databento daily `ohlcv-1d` dated-contract history for the exact MES contract chain needed for a chosen <=2-year Development/Reconciliation window; or
- use only existing local artifacts and keep S09 MES fail-closed.

It must also lock or fail-close:

- exact target window;
- all dated contracts needed for the MES chain;
- lifecycle evidence for every roll transition;
- deterministic roll rule and additive back-adjustment;
- provider-condition degraded-row exclusion/retarget policy before seeing strategy results;
- annual percentage risk runtime;
- cost source and risk-adjusted cost per trade;
- S09 speed/cost eligibility.

## Non-Authorization

This preflight authorizes no provider API access, no new data download, no market-row parsing, no real-data forecast computation, no diagnostics, no backtests, no returns, no PnL, no Sharpe, no drawdown, no positions, no costs, no carry, no CFD adapter work, no old QuantLab pipeline use, no tuning, no TEST, no VALIDATION, no OOS, no Lockbox, no Forward, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update, and no remote operations.

