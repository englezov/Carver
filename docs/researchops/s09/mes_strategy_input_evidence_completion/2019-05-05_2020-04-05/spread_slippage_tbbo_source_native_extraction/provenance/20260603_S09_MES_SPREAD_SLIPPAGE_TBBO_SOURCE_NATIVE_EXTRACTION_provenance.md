# S09 MES TBBO Spread Slippage Source-Native Extraction Provenance

Date: 2026-06-03

Status:

```text
LOCKED_SOURCE_NATIVE_TBBO_MEDIAN_SPREAD_SLIPPAGE_VALUE
```

Scope:

- gate: S09_MES_SPREAD_SLIPPAGE_TBBO_SOURCE_NATIVE_EXTRACTION_AND_DEGRADED_DAY_POLICY_LOCK
- lane_class: SOURCE_NATIVE_FUTURES
- source_row: APPENDIX_C_174_006
- root: MES
- dataset: GLBX.MDP3
- schema: tbbo
- machinery_development_slice: 2019-05-05 through 2020-04-05
- degraded_provider_dates: 2020-02-27, 2020-02-28
- degraded_day_policy: EXCLUDE_DEGRADED_PROVIDER_DAYS_FROM_ESTIMATOR_PRESERVE_IN_QUARANTINE

Estimator:

Valid top-of-book rows require positive bid, positive ask, positive bid size,
positive ask size, and ask greater than bid. Degraded provider dates are
excluded from the estimator and preserved in summary counts. The median valid
spread is rounded up to the MES tick and converted with the locked 5 USD point
multiplier.

Locked value:

- valid_quote_rows_used: 30519879
- degraded_quote_rows_excluded: 936077
- crossed_or_empty_rows_rejected: 619
- median_spread_points: 0.25
- locked_spread_slippage_round_turn_usd: 1.25

Written summary:

- `docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/spread_slippage_tbbo_source_native_extraction/summary/20260603_S09_MES_SPREAD_SLIPPAGE_TBBO_SOURCE_NATIVE_EXTRACTION_summary.csv`

Boundary:

No new provider download, MBP-1 data, risk-adjusted cost computation, speed
eligibility computation, forecast computation, diagnostics, backtests, TEST,
VALIDATION, Lockbox, Forward, deployment, trading, promotion, Git staging,
commit, push, PR, or remote operations were performed.
