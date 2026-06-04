# S09 MES Historical Cost Value Provenance

Date: 2026-06-03

Status:

```text
LOCKED_S09_MES_HISTORICAL_COST_VALUES_NOT_RISK_ADJUSTED_COST
```

Cost components:

- exchange_fee: 0.20 USD PER_SIDE from official CME historical fee extraction
- clearing_regulatory_fee: 0.02 USD PER_SIDE from NFA assessment-fee source extraction
- broker_commission: 0.62 USD PER_SIDE from operator-authorized ETF static selected-broker policy
- spread_slippage: 1.25 USD ROUND_TURN from source-native TBBO median spread extraction

Spread/slippage source:

- `docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/spread_slippage_tbbo_source_native_extraction/summary/20260603_S09_MES_SPREAD_SLIPPAGE_TBBO_SOURCE_NATIVE_EXTRACTION_summary.csv`
- degraded_day_policy: EXCLUDE_DEGRADED_PROVIDER_DAYS_FROM_ESTIMATOR_PRESERVE_IN_QUARANTINE

Boundary:

Historical cost values are locked as component evidence only. No risk-adjusted
cost, speed eligibility, forecast computation, diagnostics, backtests, TEST,
VALIDATION, Lockbox, Forward, deployment, trading, promotion, Git staging,
commit, push, PR, or remote operations were performed.
