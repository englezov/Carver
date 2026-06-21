# S09 MES Spread Slippage Bid Ask Metadata Preflight Result

Date: 2026-06-03

Status:

```text
PASS_METADATA_PREFLIGHT_ESTIMATED_NO_RAW_BID_ASK_DOWNLOAD
```

Result:

Databento metadata cost and record-count estimates were requested for the
authorized historical bid/ask route only. This is not a raw quote download and
not a spread/slippage cost lock.

Scope:

- lane_class: SOURCE_NATIVE_FUTURES
- source_row: APPENDIX_C_174_006
- root: MES
- dataset: GLBX.MDP3
- schemas: mbp-1, tbbo
- raw_symbols: MESM9, MESU9, MESZ9, MESH0, MESM0
- window: 2019-05-05 through 2020-04-05

Written artifacts:

- `docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/spread_slippage_bid_ask_metadata_preflight/status/20260603_S09_MES_SPREAD_SLIPPAGE_BID_ASK_METADATA_PREFLIGHT_status.json`
- `docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/spread_slippage_bid_ask_metadata_preflight/metadata/20260603_S09_MES_SPREAD_SLIPPAGE_BID_ASK_METADATA_PREFLIGHT_cost_record_estimates.csv`
- `docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/spread_slippage_bid_ask_metadata_preflight/provenance/20260603_S09_MES_SPREAD_SLIPPAGE_BID_ASK_METADATA_PREFLIGHT_provenance.md`

Metadata estimates:

```text
mbp-1 | records 532148195 | estimated_cost_usd 71.366634294391
tbbo  | records 31456575  | estimated_cost_usd 65.62352925539
```

Next decision:

Use the metadata estimates to choose between a bounded sampled bid/ask request,
a smaller pilot day request, or keeping spread/slippage fail-closed.

Boundary:

No raw bid/ask records, cost ledger rows, cost computation, diagnostics,
backtests, TEST, VALIDATION, Lockbox, Forward, deployment, trading, promotion,
Git staging, commit, push, PR, or remote operations were performed.
