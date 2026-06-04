# S09 MES Annual-Risk Runtime Values Evidence Artifact Contract

Date: 2026-06-03

Status:

```text
PROCESS_ONLY_S09_MES_ANNUAL_RISK_RUNTIME_VALUES_EVIDENCE_ARTIFACT_CONTRACT_NOT_AUTHORIZATION_NOT_EXECUTION
```

Scope:

- selected_evidence_name: annual_risk_runtime_values
- official_lifecycle_evidence_status: LOCKED_SOURCE_NATIVE_EVIDENCE
- roll_trading_day_semantics_status: LOCKED_SOURCE_NATIVE_EVIDENCE
- remaining_evidence_count: 8
- lane_class: SOURCE_NATIVE_FUTURES
- root: MES
- row_id: APPENDIX_C_174_006
- machinery_development_slice: 2019-05-05 through 2020-04-05
- runtime_input_lock_scope: oldest minimum machinery-development slice only
- design_ordering: oldest authorized completed source-native data first

Contracted artifact:

- relative_path: `docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/risk/20260603_S09_MES_ANNUAL_RISK_RUNTIME_ledger.csv`
- schema: `completed_trading_date,long_run_annual_risk,current_ewma32_annual_risk,annual_percentage_risk,source_label,source_sha256,status`
- required_status: `LOCKED_SOURCE_NATIVE_ANNUAL_RISK_RUNTIME_VALUE`

Validation rules:

- completed bars only
- completed_trading_date must be exact date values
- long_run_annual_risk must be finite and positive
- current_ewma32_annual_risk must be finite and positive
- annual_percentage_risk must equal the locked 30/70 annual-risk blend
- source_label must be non-empty
- source_sha256 must be valid SHA256
- status must equal `LOCKED_SOURCE_NATIVE_ANNUAL_RISK_RUNTIME_VALUE`

Non-authorization:

This contract performs:

- no Databento API access
- no provider login
- no source extraction
- no market-row parsing
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
