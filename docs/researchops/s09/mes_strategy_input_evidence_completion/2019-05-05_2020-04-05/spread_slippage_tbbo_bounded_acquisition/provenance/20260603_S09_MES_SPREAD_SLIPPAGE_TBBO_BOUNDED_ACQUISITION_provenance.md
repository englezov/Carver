# S09 MES Spread Slippage TBBO Bounded Acquisition Provenance

Date: 2026-06-03

Status:

```text
PASS_TBBO_BOUNDED_RAW_ACQUISITION_WITH_PROVIDER_DEGRADED_DAYS_NO_SPREAD_LOCK
```

Authorized scope:

- gate: S09_MES_SPREAD_SLIPPAGE_SOURCE_OR_POLICY_TBBO_BOUNDED_ACQUISITION_GATE
- lane_class: SOURCE_NATIVE_FUTURES
- provider: DATABENTO_HISTORICAL
- dataset: GLBX.MDP3
- schema: tbbo
- stype_in: raw_symbol
- raw_symbols: MESM9, MESU9, MESZ9, MESH0, MESM0
- window: 2019-05-05 through 2020-04-05
- route: raw tbbo DBN acquisition only
- provider_quality_warnings: 2020-02-27 degraded; 2020-02-28 degraded

Written receipt:

- `docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/spread_slippage_tbbo_bounded_acquisition/raw_provider_output/20260603_S09_MES_SPREAD_SLIPPAGE_TBBO_BOUNDED_ACQUISITION_raw_tbbo_receipt_ledger.csv`

Boundary:

Raw TBBO DBN files were acquired for later source-native spread/slippage
extraction. No MBP-1 data was downloaded. No spread/slippage policy or value
was selected or locked. No cost ledger rows, cost computation, risk-adjusted
cost computation, speed eligibility computation, forecast computation,
diagnostics, backtests, TEST, VALIDATION, Lockbox, Forward, deployment,
trading, promotion, Git staging, commit, push, PR, or remote operations were
performed.
