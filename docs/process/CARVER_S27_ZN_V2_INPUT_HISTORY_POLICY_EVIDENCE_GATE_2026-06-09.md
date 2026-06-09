# S27_V2 Input-History And Policy-Evidence Gate

Date: 2026-06-09

Status:

```text
PROCESS_ONLY_S27_V2_INPUT_HISTORY_POLICY_EVIDENCE_GATE_NOT_REPLAY_NOT_BACKTEST
```

Authorization:

```text
S27_V2_LOCAL_ONLY_INPUT_HISTORY_POLICY_EVIDENCE_GATE
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Purpose

This record identifies the local-only ZN history and policy evidence needed before S27_V2 can move from the externally passed Phase 2 fail-closed runtime surface into nonblocked runtime-history ledgers.

This is a process-only inventory and gap plan. It is not parser/file replay execution, not a diagnostic, not a backtest, not result interpretation, not PnL evaluation, not promotion, and not a source-faithful evidence claim.

## Entry Condition

The Phase 2 runtime-surface executable replay-ledger patch received an external hostile audit `PASS`:

```text
docs/process/CARVER_S27_ZN_V2_EXECUTABLE_REPLAY_LEDGER_PHASE2_EXTERNAL_AUDIT_SYNTHESIS_2026-06-09.md
```

The Phase 2 external audit left one forward hardening note for future multi-row packs:

```text
Before reusing Phase 2 on a future multi-row input-history pack, bind each level row hash to the exact same indexed parsed row or selected manifest row whose close price is used, rather than relying on active row-hash membership plus the first close-price tuple entry.
```

That note is a required condition for any multi-row runtime-history use.

## Current Declared Pack

Current S27_V2 local declared input pack:

```text
docs/researchops/s27_v2_local_replay_inputs/ZN/20260608_oldest_dev_recon_znh2_20220103_declared_pack
```

This pack has exactly the seven row-family CSVs required by `ReplayInputDirectoryDeclaration`, but each row family has one row only:

```text
DAILY_CONTINUOUS_COMPLETED_BAR = 1
DAILY_CURRENT_CONTRACT_COMPLETED_BAR = 1
HOURLY_DECISION_COMPLETED_BAR = 1
HOURLY_FILL_COMPLETED_BAR = 1
SESSION_CALENDAR = 1
ROLL_CALENDAR = 1
COST_PARAMETER = 1
```

The one-row pack is useful for declared-file parsing, byte-hash binding, authority binding, and fail-closed behavior. It is not enough to emit nonblocked S27 runtime history because strict-prior daily history, EWMAC(16,64), sigma history, V/Q/M history, and policy evidence remain unresolved.

Cost parameters in this pack are policy hashes only. Numeric commission, spread, tick, multiplier, and currency cost evidence is not claimed by this pack.

## Local History Inventory

Oldest suitable local ZN area already used as the one-row pack source:

```text
docs/researchops/s26_s27_candidate_comparison/2022-01-01_2023-12-31/ZN
```

Important correction:

```text
DO_NOT_TREAT_2022_2023_AS_THE_S27_V2_DEV_RECON_SLICE
```

The `2022-01-01_2023-12-31` path is only an already-local source/artifact area label from older diagnostic work. It is not the v2 development/reconciliation window and must not be promoted into the v2 target slice. The correct v2 target is the earliest local contiguous slice after the required strict-prior indicators and policy evidence are populated, with warmup rows used only as warmup and not as scored/result interpretation.

Local provenance for that area records:

```text
daily_continuous_rows = 4033
hourly_continuous_rows = 11797
hourly_source_rows = 20899
daily_roll_transition_count = 39
hourly_roll_transition_count = 8
effective_backtest_start = 2022-01-03
effective_backtest_start_reason = FIRST_ROW_WITH_STRICT_PRIOR_DAILY_SIGMA_TREND_AND_V_Q_M_RUNTIME
```

The raw/local provider inventory includes:

```text
raw_provider_output .dbn files = 98
raw_provider_output *_provider.csv files = 98
raw_provider_metadata symbology JSON files present
local_lineage daily/hourly continuous and inactive ledgers present
daily/hourly roll plans present
```

The files are already-local provider artifacts. The local provenance states that a Databento API key was read historically and not written to artifacts; current S27_V2 work does not require Databento access, a provider/API call, or a new download. No NinjaTrader authority was identified in the inspected local records.

## Local Artifact Disposition

The 2022-2023 ZN candidate area contains old runtime, forecast, position, and backtest/result artifacts. Those artifacts are not S27_V2 source-faithful evidence and must not be reused as runtime authority.

Permitted future use, with separate authorization, is limited to already-local source material and lineage inputs being re-normalized into S27_V2 declared row-family CSVs with fresh byte hashes, selected-row authority, source-input manifests, and replay construction artifacts. The selected v2 pack must be anchored to the first eligible post-warmup timestamp, not to the old `2022-2023` diagnostic window label.

Superseded/diagnostic only:

```text
daily_runtime_rows/*
forecast_rows/*
position_rows/*
backtest_rows/*
summary/*
status/result fields such as gross_pnl_usd, net_after_etf_fees_usd, rounded_position_counts
```

Potential local source candidates for a future S27_V2 multi-row pack:

```text
raw_provider_output/*.dbn
raw_provider_output/*_provider.csv
raw_provider_metadata/*_symbology.json
local_lineage/*_daily_continuous_lineage.csv
local_lineage/*_hourly_continuous_lineage.csv
local_lineage/*_daily_roll_plan.csv
local_lineage/*_hourly_roll_plan.csv
```

## Minimal Requirements For Nonblocked Runtime History

S27_V2 runtime-history construction must be able to recompute or bind these from completed, strict-prior, local-only rows:

```text
EWMA5 daily equilibrium
EWMAC(16,64) daily trend gate
previous completed daily current-contract close for sigma-price bridge
percentage sigma input and source-locked sigma method
V = current_percentage_sigma / ten_year_rolling_mean(current_percentage_sigma)
Q = expanding/admissible quantile of V
M = EWMA span 10 of raw_multiplier = 2 - 1.5 * Q
daily/hourly level compatibility or explicit bridge proof
hourly decision completed bar
hourly fill completed bar
session calendar coverage
roll calendar coverage
cost/tick/multiplier/currency policy evidence status
```

Minimum practical history thresholds:

```text
EWMA5 equilibrium: at least 5 prior completed daily continuous rows, but more is preferred for stable warmup.
EWMAC(16,64): at least 64 prior completed daily continuous rows, with explicit warmup status.
M EWMA10: at least 10 admissible raw multiplier observations, with explicit warmup status.
V ten-year mean: up to 2560 daily observations where available; where fewer exist, the rule must explicitly fail closed or carry a source-locked admissible warmup convention.
Q expanding/admissible quantile: inception-through-current admissible observations only, never future observations.
Sigma: source-locked completed daily percentage-volatility input; if Strategy 3 sigma remains unresolved, runtime must fail closed before forecast evidence.
```

The existing local provenance suggests enough daily and hourly rows may exist for development/reconciliation multi-row runtime work, but that is not yet an S27_V2 claim. It must be proven by a fresh declared input pack and replay construction.

## Policy Evidence Requirements

For nonblocked runtime-history rows:

```text
daily/hourly completed-bar convention must be carried and validated
session calendar must cover every decision/fill timestamp
roll plan must cover every selected contract transition
daily continuous and hourly current price levels must be compatible or bridge-proved
source-row hash and selected-row locator must bind each runtime row to exact source rows
```

For later order/fill/cost/PnL phases, still unresolved and fail-closed unless separately source-locked:

```text
ZN tick size and rounding policy
multiplier and currency authority
commission policy
spread policy for market orders
working limit-order lifecycle
overnight/session reset behavior
roll/order interaction behavior
market-order fallback cases
capital/unit position sizing authority
```

## Required Gaps Before Multi-Row Runtime Use

1. Patch or extend Phase 2 provenance validation so each level row hash binds to the exact indexed parsed row or selected manifest row whose close price is used.
2. Build a fresh multi-row S27_V2 declared ZN input pack from explicitly named already-local source files, choosing the earliest contiguous local slice after all required indicators and policy evidence are populated.
3. Keep all old runtime/forecast/backtest outputs diagnostic only; do not import them as S27_V2 authority.
4. Recompute or reconstruct the seven row families through S27_V2 declarations with byte SHA256 hashes and selected-row authority.
5. Run focused local verification and local hostile audit of the multi-row declared pack before using it for executable runtime ledgers.
6. Preserve fail-closed status for sigma, V/Q/M, level compatibility, tick/session/roll/cost, multiplier/currency, and working-order lifecycle whenever evidence is insufficient.

## Recommended Next Authorization

```text
Operator authorizes S27_V2_LOCAL_ONLY_FIRST_POPULATED_ZN_INPUT_PACK_P3_HARDENING_AND_BUILD, after the input-history/policy-evidence gate, limited to Phase 2 indexed selected-row/close-price binding hardening and building one fresh multi-row declared ZN input pack from explicitly named already-local ZN source files, selecting the earliest contiguous local slice after EWMA5, EWMAC(16,64), sigma, V/Q/M, level-compatibility, session/roll, and policy-evidence requirements are populated.

This authorizes Codex to patch Phase 2 provenance/validation so each level row hash binds to the exact indexed parsed/selected row whose close price is used, read only the explicitly named already-local source/provider/lineage/roll files needed to identify and build that first post-warmup pack, compute SHA256 hashes, normalize rows into the seven S27_V2 row-family CSVs required by ReplayInputDirectoryDeclaration, write the multi-row declared input pack and manifests, run focused local verification tests, record process/current-state outputs, and run local hostile audits with subagents.

No provider/API access, downloads, new data acquisition, OOS/Lockbox/Forward access, backtests, result-scored runs, result interpretation, PnL/result evaluation, tuning, adapter work, deployment, trading, promotion, Git staging/commit/push/PR, or source-faithful evidence claim.
```

## Non-Authorization

This record does not authorize provider/API access, downloads, new data acquisition, OOS, Lockbox, Forward, parser/file replay execution, diagnostics, backtests, result-scored runs, result interpretation, PnL/result evaluation, tuning, adapter work, deployment, trading, promotion, Git actions, or source-faithful evidence claims.
