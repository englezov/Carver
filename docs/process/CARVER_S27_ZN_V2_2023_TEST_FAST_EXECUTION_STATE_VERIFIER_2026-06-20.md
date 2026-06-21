# S27_V2 2023 TEST Fast Execution-State Verifier

Date: 2026-06-20

## Status

Local implementation checkpoint: `LOCAL_PASS_FAST_EXECUTION_STATE_SEGMENT_VERIFIER_NOT_RESULT`

This record extends the S27_V2 TEST runner remediation by adding a fast execution-state segment verifier. It validates carried position state, order intent class, fill/cost/PnL row coherence, and fail-closed result boundaries over the row `704` through `1377` segment from the trusted row-703 checkpoint.

This is still not broad TEST continuation and not result interpretation. It is a segment verification layer for the already-produced checkpoint artifacts, designed to replace repeated full-chain proof rebuilding during local continuation.

## Implemented

Added `src/carver/spine/s27_v2_replay/fast_execution_state.py`.

The verifier:

- resumes from the trusted row-703 checkpoint hash;
- reads only the locked row `704` through `1377` segment from the declared TEST run artifact root;
- verifies desired-position start/target/change arithmetic;
- verifies carried position continuity from one row to the next;
- verifies no-order, roll-boundary suppression, filled adjacent-limit, unfilled adjacent-limit, and market-order policy classes;
- verifies market rows, fill rows, working-order transitions, cost rows, and PnL rows bind coherently for each segment row;
- preserves `FAIL_CLOSED_RESULT_ROW_NOT_EMITTED_NOT_AUTHORIZED`, `FAIL_CLOSED_BACKTEST_RESULT_NOT_EMITTED_NOT_AUTHORIZED`, `MECHANICAL_PNL_ROW_CONSTRUCTION_ONLY_NOT_RESULT_INTERPRETATION`, and `source_faithful_evidence_claimed = FALSE`;
- returns deterministic state-transition and intent-classification row hashes;
- exposes a verification bundle through `fast_test_runner.py` for both `fast_mode` and `segment_mode`.

The locked parity sample is rows `704`, `892`, `1113`, `1355`, and `1374`, covering roll-boundary no-order suppression, session-end adjacent-limit fill, market-order fill, valuation-gap adjacent-limit fill, and the latest market-order supported row.

## Verification

Focused local checks:

```text
python -m pytest -q tests/test_s27_v2_test_incremental_runner.py tests/test_s27_v2_fast_runner_cache.py tests/test_s27_v2_fast_row_engine.py tests/test_s27_v2_fast_execution_state.py
```

Result:

```text
45 passed in 15.86s
```

Coverage includes:

- execution-state verifier construction over the row `704` through `1377` segment;
- row-count and ending-position binding;
- row hash binding for generated state-transition and intent-classification rows;
- forged generated-row rejection;
- forged segment-bundle rejection;
- terminal-row-only TBBO requirements planning for row `1378`;
- duplicate row-index rejection for sparse ledgers;
- cumulative gross/commission/spread/net PnL roll-forward from the row-703 checkpoint;
- market-fill metadata binding for side, quantity, price, and position against market/fill rows, plus timestamp, raw symbol, and source row hash against the declared `hourly_fill_completed_bar.csv` row;
- unexpected market-fill metadata rejection for non-market rows;
- locked run-root rejection;
- fast-runner facade binding of execution-state verification;
- no import/call of `test_mechanical_run.py` or `run_2023_test_mechanical_artifacts`.

## Local Hostile Audit

One local hostile audit subagent initially found two P1 issues and two P2 issues:

- the TBBO batch plan surfaced requirements beyond terminal row `1378`;
- cumulative cost/PnL roll-forward from the row-703 checkpoint was not validated;
- market-fill metadata was only lightly bound;
- sparse market ledgers could silently shadow duplicate row indexes.

All four findings were remediated. The TBBO plan is capped at row `1378`, cumulative roll-forward is checked row-by-row, market-fill metadata is coherently bound or rejected, and duplicate row indexes are rejected for segment rows and sparse ledger indexing. A re-audit found one remaining P2 around market-fill timestamp/source-row binding; this was remediated by reading the declared fill-candidate row family, byte-checking it against the input-pack manifest, and binding market-fill timestamp/raw symbol/source row hash to the matching declared fill row. Market fill price remains bound to the market/fill rows because it may be the selected TBBO bid/ask rather than the completed-bar close.

Final local hostile re-audit returned P0 none, P1 none, P2 none, P3 none. Focused tests in the re-audit returned `45 passed`.

## Remaining Work

The next extraction slice should move from verification to operational segment emission:

- generate order/transition/fill/cost/PnL segment rows in memory from declared inputs and policy registries;
- build a batch evidence planner from fast engine output rather than relying on the existing requirements ledger only;
- emit compact segment artifacts from generated in-memory rows;
- keep slow proof mode reserved for explicit checkpoint audits.

## Non-Authorizations

This record does not authorize provider/API access, downloads, new data acquisition, broader TEST continuation, VALIDATION, OOS, Lockbox, Forward, result interpretation, PnL evaluation beyond mechanical construction, tuning, adapter work, deployment, trading, promotion, Git actions, GPT packet preparation, or source-faithful evidence claims.
