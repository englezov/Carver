# S09 MES Spread Slippage TBBO Bounded Acquisition Result

Date: 2026-06-03

Status:

```text
PASS_TBBO_BOUNDED_RAW_ACQUISITION_WITH_PROVIDER_DEGRADED_DAYS_NO_SPREAD_LOCK
```

Result:

Databento raw TBBO DBN data was requested for the authorized bounded
source-native spread/slippage route. This is a raw data acquisition, not a
spread/slippage value extraction and not a cost lock.

Scope:

- lane_class: SOURCE_NATIVE_FUTURES
- source_row: APPENDIX_C_174_006
- root: MES
- dataset: GLBX.MDP3
- schema: tbbo
- raw_symbols: MESM9, MESU9, MESZ9, MESH0, MESM0
- window: 2019-05-05 through 2020-04-05
- raw_dbn_files: 5
- raw_dbn_total_size_bytes: 696973929
- provider_quality_warnings: 2020-02-27 degraded; 2020-02-28 degraded

Written artifacts:

- `docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/spread_slippage_tbbo_bounded_acquisition/status/20260603_S09_MES_SPREAD_SLIPPAGE_TBBO_BOUNDED_ACQUISITION_status.json`
- `docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/spread_slippage_tbbo_bounded_acquisition/raw_provider_output/20260603_S09_MES_SPREAD_SLIPPAGE_TBBO_BOUNDED_ACQUISITION_raw_tbbo_receipt_ledger.csv`
- `docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/spread_slippage_tbbo_bounded_acquisition/provenance/20260603_S09_MES_SPREAD_SLIPPAGE_TBBO_BOUNDED_ACQUISITION_provenance.md`

Next decision:

Authorize source-native extraction from the acquired TBBO files to produce a
predeclared spread/slippage policy or keep spread/slippage fail-closed. Any
extraction must explicitly account for the degraded provider days listed above.

Boundary:

No MBP-1 data, spread/slippage value lock, cost ledger rows, cost computation,
diagnostics, backtests, TEST, VALIDATION, Lockbox, Forward, deployment,
trading, promotion, Git staging, commit, push, PR, or remote operations were
performed.
