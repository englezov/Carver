# S27_V2 First-Populated ZN Multi-Row Declared Input Pack Provenance

Date: 2026-06-09

Status:

```text
LOCAL_INPUT_PACK_DECLARED_FOR_PARSER_REPLAY_CONSTRUCTION_ONLY_NOT_EVIDENCE
```

Authorization:

```text
S27_V2_LOCAL_ONLY_FIRST_POPULATED_ZN_INPUT_PACK_P3_HARDENING_AND_BUILD
```

## Scope

This pack is a local-only S27_V2 declared input pack for parser/replay construction and fail-closed runtime-surface development. It is not a backtest, not a scored run, not result interpretation, not PnL evaluation, not promotion, and not a source-faithful evidence claim.

The old path label `2022-01-01_2023-12-31` is not the S27_V2 development/reconciliation slice. It is only the location of already-local source/provider/lineage artifacts that were inspected and re-normalized where permitted.

## Selected Slice Rule

Target rule:

```text
FIRST_CONTIGUOUS_LOCAL_SLICE_AFTER_REQUIRED_INDICATORS_POPULATED_OR_FAIL_CLOSED
```

Selected candidate row:

```text
decision completed hour: 2022-01-03T05:00:00Z
fill completed hour: 2022-01-03T06:00:00Z
previous completed daily current-contract row: 2022-01-02T00:00:00Z
raw symbol: ZNH2
```

The selected row is the first local S27 ZN candidate row available in the already-local hourly source material after the old populated-indicator marker. This does not make the old forecast/runtime rows authority.

## Row Families

```text
DAILY_CONTINUOUS_COMPLETED_BAR = 64 rows
DAILY_CURRENT_CONTRACT_COMPLETED_BAR = 1 row
HOURLY_DECISION_COMPLETED_BAR = 8 rows
HOURLY_FILL_COMPLETED_BAR = 8 rows
SESSION_CALENDAR = 1 row
ROLL_CALENDAR = 1 row
COST_PARAMETER = 1 row
```

The daily continuous file places the selected previous daily row first, followed by 63 locally available strict-prior daily rows. This shape supports current source-input selection scaffolding, which selects the first row per family, while carrying enough local row count for runtime-history count checks.

## Source Boundaries

Already-local source/provider/lineage files inspected:

```text
docs/researchops/s26_s27_candidate_comparison/2022-01-01_2023-12-31/ZN/local_lineage/20260531_S27_SOURCE_NATIVE_CANDIDATE_COMPARISON_2022_2023_R2_ZN_daily_continuous_lineage.csv
docs/researchops/s26_s27_candidate_comparison/2022-01-01_2023-12-31/ZN/local_lineage/20260531_S27_SOURCE_NATIVE_CANDIDATE_COMPARISON_2022_2023_R2_ZN_hourly_continuous_lineage.csv
docs/researchops/s26_s27_candidate_comparison/2022-01-01_2023-12-31/ZN/local_lineage/20260531_S27_SOURCE_NATIVE_CANDIDATE_COMPARISON_2022_2023_R2_ZN_hourly_roll_plan.csv
docs/researchops/s26_s27_candidate_comparison/2022-01-01_2023-12-31/ZN/daily_runtime_rows/20260531_S27_SOURCE_NATIVE_CANDIDATE_COMPARISON_2022_2023_R2_ZN_sigma_rows.csv
docs/researchops/s26_s27_candidate_comparison/2022-01-01_2023-12-31/ZN/daily_runtime_rows/20260531_S27_SOURCE_NATIVE_CANDIDATE_COMPARISON_2022_2023_R2_ZN_vqm_rows.csv
docs/researchops/s26_s27_candidate_comparison/2022-01-01_2023-12-31/ZN/forecast_rows/20260531_S27_SOURCE_NATIVE_CANDIDATE_COMPARISON_2022_2023_R2_ZN_s27_forecast_rows.csv
docs/researchops/s26_s27_candidate_comparison/2022-01-01_2023-12-31/ZN/raw_provider_output/20260531_S27_SOURCE_NATIVE_CANDIDATE_COMPARISON_2022_2023_ZN_daily_ZNH2_provider.csv
```

No provider/API access, downloads, new data acquisition, OOS, Lockbox, Forward, backtests, result-scored runs, Git actions, adapter work, deployment, trading, or promotion occurred.

## Fail-Closed Caveats

The local R2 V/Q/M ledger ends at:

```text
2020-12-21
```

The selected hourly decision row is:

```text
2022-01-03T05:00:00Z
```

Therefore this pack must not be treated as nonblocked V/Q/M runtime evidence. The selected daily sigma is carried from the already-local forecast sigma bridge row to satisfy the current parser schema, but that does not source-lock Strategy 3 sigma or make the old forecast row authority.

Future executable runtime work must remain fail-closed until daily continuity, sigma, V/Q/M, level compatibility, session/roll, cost/tick/multiplier/currency, and working-order lifecycle evidence are source-locked or recomputed under S27_V2 authority.
