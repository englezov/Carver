# S09 MES Spread Slippage TBBO Bounded Acquisition Local Hostile Audit

Date: 2026-06-03

Status:

```text
LOCAL_HOSTILE_AUDIT_TBBO_BOUNDED_RAW_ACQUISITION_NO_SPREAD_LOCK
```

Observed artifacts:

- `docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/spread_slippage_tbbo_bounded_acquisition/status/20260603_S09_MES_SPREAD_SLIPPAGE_TBBO_BOUNDED_ACQUISITION_status.json`
- `docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/spread_slippage_tbbo_bounded_acquisition/raw_provider_output/20260603_S09_MES_SPREAD_SLIPPAGE_TBBO_BOUNDED_ACQUISITION_raw_tbbo_receipt_ledger.csv`
- `docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/spread_slippage_tbbo_bounded_acquisition/provenance/20260603_S09_MES_SPREAD_SLIPPAGE_TBBO_BOUNDED_ACQUISITION_provenance.md`

Checks:

- lane remains SOURCE_NATIVE_FUTURES
- dataset remains GLBX.MDP3
- schema is limited to tbbo
- raw symbols are limited to MESM9, MESU9, MESZ9, MESH0, MESM0
- window remains 2019-05-05 through 2020-04-05
- no MBP-1 data
- no spread/slippage policy lock
- no cost ledger rows
- no forecast, diagnostics, backtests, TEST, VALIDATION, Lockbox, Forward, deployment, trading, promotion, or Git operations
