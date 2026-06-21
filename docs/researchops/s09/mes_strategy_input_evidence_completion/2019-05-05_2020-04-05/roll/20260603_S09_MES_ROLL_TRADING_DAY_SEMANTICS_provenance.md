# S09 MES Roll Trading-Day Semantics Evidence Lock Provenance

Status:

```text
LOCKED_SOURCE_NATIVE_ROLL_TRADING_DAY_SEMANTICS
```

Scope:

- gate: S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_GATE
- selected_evidence_name: roll_trading_day_semantics
- lane_class: SOURCE_NATIVE_FUTURES
- source_row: APPENDIX_C_174_006
- author_market_code: MES
- machinery_development_slice: 2019-05-05 through 2020-04-05
- runtime_input_lock_scope: oldest minimum machinery-development slice only
- design_ordering: oldest authorized completed source-native data first

Locked roll pairs:

MESM9->MESU9, MESU9->MESZ9, MESZ9->MESH0, MESH0->MESM0

Source-native evidence basis:

- local machinery lineage roll plan:
  `docs/researchops/s09/mes_machinery_dev_lineage/2019-05-05_2020-04-05/roll_plan/20260603_S09_MES_MACHINERY_DEV_LINEAGE_roll_plan.csv`
- local machinery lineage SHA256 manifest:
  `docs/researchops/s09/mes_machinery_dev_lineage/2019-05-05_2020-04-05/hashes/20260603_S09_MES_MACHINERY_DEV_LINEAGE_sha256.json`
- official lifecycle evidence ledger must already be locked before roll semantics lock

Boundary preserved:

This is roll_trading_day_semantics source-native evidence locking only. It does
not lock annual risk runtime values, daily price risk, historical cost values,
risk-adjusted cost, speed eligibility, eligible speed set, Table 36 FDM, or
global hash-bound strategy-input readiness.

no Databento API access, no provider login, no new provider download, no market-row parsing, no risk runtime computation, no cost computation, no speed eligibility computation, no forecast computation, no diagnostics, no returns, no PnL, no positions, no carry, no TEST, no VALIDATION, no OOS, no Lockbox, no Forward, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR, and no remote operations were performed.
