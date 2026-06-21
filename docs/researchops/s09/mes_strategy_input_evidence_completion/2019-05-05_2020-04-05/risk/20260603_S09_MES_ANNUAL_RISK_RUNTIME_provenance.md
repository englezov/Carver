# S09 MES Annual-Risk Runtime Values Evidence Lock Provenance

Status:

```text
LOCKED_SOURCE_NATIVE_ANNUAL_RISK_RUNTIME_VALUE
```

Scope:

- gate: S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_GATE
- selected_evidence_name: annual_risk_runtime_values
- lane_class: SOURCE_NATIVE_FUTURES
- source_row: APPENDIX_C_174_006
- author_market_code: MES
- machinery_development_slice: 2019-05-05 through 2020-04-05
- runtime_input_lock_scope: oldest minimum machinery-development slice only
- design_ordering: oldest authorized completed source-native data first

Locked annual-risk rows:

- row_count: 255
- first_completed_trading_date: 2019-06-11
- last_completed_trading_date: 2020-04-05

Source-native evidence basis:

- local machinery-development continuous lineage:
  `docs/researchops/s09/mes_machinery_dev_lineage/2019-05-05_2020-04-05/continuous_series/20260603_S09_MES_MACHINERY_DEV_LINEAGE_continuous_daily_mes_machinery_only.csv`
- local machinery lineage SHA256 manifest:
  `docs/researchops/s09/mes_machinery_dev_lineage/2019-05-05_2020-04-05/hashes/20260603_S09_MES_MACHINERY_DEV_LINEAGE_sha256.json`
- continuous lineage SHA256:
  `2E81D6BA6A0692B7DC6AB77FBFE54436BF60429D4733C2559DA34A845B402F6D`
- official lifecycle evidence and roll_trading_day_semantics evidence must already be locked

Runtime rule:

- current risk component: EWMA32 annualized percentage-return sigma
- long-run component: no-lookahead equal-weight annualized percentage-return RMS using history through each completed date
- annualization convention: 256 trading days
- blend: 30/70 long-run/current EWMA32 annual-risk blend
- completed bars only

Boundary preserved:

This is annual_risk_runtime_values source-native evidence locking only. It does
not lock daily price risk, historical cost values, risk-adjusted cost, speed
eligibility, eligible speed set, Table 36 FDM, or global hash-bound
strategy-input readiness.

no Databento API access, no provider login, no new provider download, no market-row parsing, no cost computation, no speed eligibility computation, no forecast computation, no diagnostics, no returns, no PnL, no positions, no carry, no TEST, no VALIDATION, no OOS, no Lockbox, no Forward, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR, and no remote operations were performed.
