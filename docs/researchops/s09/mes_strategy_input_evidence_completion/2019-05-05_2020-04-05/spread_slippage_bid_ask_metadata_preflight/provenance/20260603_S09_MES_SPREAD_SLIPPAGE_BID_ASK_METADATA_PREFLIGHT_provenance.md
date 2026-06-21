# S09 MES Spread Slippage Bid Ask Metadata Preflight Provenance

Date: 2026-06-03

Status:

```text
PASS_METADATA_PREFLIGHT_ESTIMATED_NO_RAW_BID_ASK_DOWNLOAD
```

Authorized scope:

- gate: S09_MES_SPREAD_SLIPPAGE_SOURCE_OR_POLICY_HISTORICAL_BID_ASK_DATA_GATE
- lane_class: SOURCE_NATIVE_FUTURES
- provider: DATABENTO_HISTORICAL
- dataset: GLBX.MDP3
- schemas: mbp-1, tbbo
- stype_in: raw_symbol
- raw_symbols: MESM9, MESU9, MESZ9, MESH0, MESM0
- window: 2019-05-05 through 2020-04-05
- route: metadata get_record_count and get_cost only

Written data:

- `docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/spread_slippage_bid_ask_metadata_preflight/metadata/20260603_S09_MES_SPREAD_SLIPPAGE_BID_ASK_METADATA_PREFLIGHT_cost_record_estimates.csv`

Boundary:

No raw bid/ask records were downloaded. No spread/slippage policy was selected
or locked. No cost ledger rows, cost computation, risk-adjusted cost
computation, speed eligibility computation, forecast computation, diagnostics,
backtests, TEST, VALIDATION, Lockbox, Forward, deployment, trading, promotion,
Git staging, commit, push, PR, or remote operations were performed.
