# S09 MES TBBO Source-Native Spread Slippage Extract

Date: 2026-06-03

Status:

```text
LOCKED_SOURCE_NATIVE_TBBO_MEDIAN_SPREAD_SLIPPAGE_VALUE
```

Operator authorization:

```text
spread_slippage_tbbo_source_native_extraction_and_degraded_day_policy_lock
```

Source:

- provider: DATABENTO_HISTORICAL
- dataset: GLBX.MDP3
- schema: tbbo
- raw_symbols: MESM9, MESU9, MESZ9, MESH0, MESM0
- acquired_raw_tbbo_only: YES
- machinery_development_slice: 2019-05-05 through 2020-04-05
- summary: `docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/spread_slippage_tbbo_source_native_extraction/summary/20260603_S09_MES_SPREAD_SLIPPAGE_TBBO_SOURCE_NATIVE_EXTRACTION_summary.csv`

Degraded-day treatment:

```text
EXCLUDE_DEGRADED_PROVIDER_DAYS_FROM_ESTIMATOR_PRESERVE_IN_QUARANTINE
```

Locked value:

- median_spread_points: 0.25
- locked_spread_slippage_round_turn_usd: 1.25
- charge_timing: ROUND_TURN
- valid_quote_rows_used: 30519879
- degraded_quote_rows_excluded: 936077
- crossed_or_empty_rows_rejected: 619

Boundary:

This locks spread/slippage for the machinery-development historical cost family
only. It does not compute risk-adjusted cost, speed eligibility, forecasts,
diagnostics, backtests, TEST, VALIDATION, Lockbox, Forward, deployment,
trading, promotion, or Git operations.
