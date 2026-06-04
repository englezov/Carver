# S09 MES Daily Price-Risk Values Evidence Lock Provenance

Status:

```text
LOCKED_SOURCE_NATIVE_DAILY_PRICE_RISK_VALUE
```

Scope:

- gate: S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_GATE
- selected_evidence_name: daily_price_risk_values
- lane_class: SOURCE_NATIVE_FUTURES
- source_row: APPENDIX_C_174_006
- author_market_code: MES
- machinery_development_slice: 2019-05-05 through 2020-04-05
- runtime_input_lock_scope: oldest minimum machinery-development slice only
- design_ordering: oldest authorized completed source-native data first

Locked daily price-risk rows:

- row_count: 255
- first_completed_trading_date: 2019-06-11
- last_completed_trading_date: 2020-04-05

Source-native evidence basis:

- local machinery-development continuous lineage:
  `docs/researchops/s09/mes_machinery_dev_lineage/2019-05-05_2020-04-05/continuous_series/20260603_S09_MES_MACHINERY_DEV_LINEAGE_continuous_daily_mes_machinery_only.csv`
- locked annual-risk runtime ledger:
  `docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/risk/20260603_S09_MES_ANNUAL_RISK_RUNTIME_ledger.csv`
- continuous lineage SHA256:
  `2E81D6BA6A0692B7DC6AB77FBFE54436BF60429D4733C2559DA34A845B402F6D`
- annual-risk ledger SHA256:
  `B5FE8304A0EF62F4527565218B3EFF0C9C483F0CD26C100465EB819BA7B535B4`
- combined daily-price source SHA256:
  `472687826BE78705EFFB28B99FADC46EC6C21261358A5446D9CFAF4D4496057E`
- official lifecycle evidence, roll_trading_day_semantics evidence, and annual_risk_runtime_values evidence must already be locked

Runtime rule:

- daily_price_risk_currency = current_price * annual_percentage_risk / 16
- current_price is the same completed-bar adjusted_close from local machinery lineage
- annual_percentage_risk is the same completed-bar locked annual-risk runtime value
- completed bars only

Boundary preserved:

This is daily_price_risk_values source-native evidence locking only. It does
not lock historical cost values, risk-adjusted cost, speed eligibility,
eligible speed set, Table 36 FDM, or global hash-bound strategy-input readiness.

no Databento API access, no provider login, no new provider download, no market-row parsing, no risk runtime computation, no cost computation, no speed eligibility computation, no forecast computation, no diagnostics, no returns, no PnL, no positions, no carry, no TEST, no VALIDATION, no OOS, no Lockbox, no Forward, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR, and no remote operations were performed.
