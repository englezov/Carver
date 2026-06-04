# S09 MES Roll Trading-Day Semantics Evidence Artifact Contract

Date: 2026-06-03

Status:

```text
PROCESS_ONLY_S09_MES_ROLL_TRADING_DAY_SEMANTICS_EVIDENCE_ARTIFACT_CONTRACT_NOT_AUTHORIZATION_NOT_EXECUTION
```

Scope:

- selected_evidence_name: roll_trading_day_semantics
- official_lifecycle_evidence_status: LOCKED_SOURCE_NATIVE_EVIDENCE
- remaining_evidence_count: 9
- lane_class: SOURCE_NATIVE_FUTURES
- root: MES
- row_id: APPENDIX_C_174_006
- machinery_development_slice: 2019-05-05 through 2020-04-05
- runtime_input_lock_scope: oldest minimum machinery-development slice only
- design_ordering: oldest authorized completed source-native data first

Contracted artifact:

- relative_path: `docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/roll/20260603_S09_MES_ROLL_TRADING_DAY_SEMANTICS_ledger.csv`
- schema: `old_symbol,new_symbol,provider_roll_date,completed_roll_date,source_label,source_sha256,status`
- required_status: `LOCKED_SOURCE_NATIVE_ROLL_TRADING_DAY_SEMANTICS`

Validation rules:

- completed bars only
- MES symbols only
- old_symbol and new_symbol must differ
- provider_roll_date must be exact source-native provider roll date
- completed_roll_date must be exact completed trading date
- completed_roll_date must not precede provider_roll_date
- source_label must be non-empty
- source_sha256 must be valid SHA256
- no duplicate old_symbol/new_symbol roll pairs

Non-authorization:

This contract performs:

- no Databento API access
- no provider login
- no source extraction
- no market-row parsing
- no risk runtime computation
- no cost computation
- no speed eligibility computation
- no forecast computation
- no diagnostics
- no backtests
- no TEST
- no VALIDATION
- no Lockbox
- no Forward
- no deployment
- no trading
- no promotion
- no Git staging, commit, push, PR, or remote operations
