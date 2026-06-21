# S27_V2 2023 TEST Row-1378 Post-Fill TBBO Pack-Exhaustion Local Audit

Date: 2026-06-21

Status: LOCAL_PASS_ROW1378_POST_FILL_TBBO_PACK_EXHAUSTION_AFTER_REAUDIT_NOT_RESULT

## Scope

This local hostile re-audit covered only the row-1378 post-fill TBBO engineering convention binding and declared-pack exhaustion remediation for the S27_V2 2023 TEST mechanical artifact checkpoint.

No provider/API access, downloads, new data acquisition, broader TEST expansion, VALIDATION, OOS, Lockbox, Forward, result interpretation, tuning, Git actions, GPT/Opus packet preparation, adapter work, deployment, trading, promotion, or source-faithful evidence claim was authorized or performed.

## Verification

- Active 2023 TEST run artifacts are bounded at candidate rows `1378` and supported rows `1378`.
- Active fail-closed row index is `0`.
- Active fail-closed reason is `NO_FAIL_CLOSED_BLOCKER_DECLARED_PACK_EXHAUSTED_NOT_RESULT`.
- `fail_closed_ledger.csv` is header-only.
- Last PnL row is row `1378`, ending position `3`, cumulative gross PnL `-98750.0`, cumulative commission `2881.9000000000005`, cumulative spread `0.0`, cumulative net PnL `-101631.9`, with `source_faithful_evidence_claimed = FALSE`.
- Standalone row-1378 selected-spread registry binds `2023-03-31T00:00:00.183796035Z`, bid `114.515625`, ask `114.53125`, lag `0.183796035`, and label `ROW1378_FIRST_POST_FILL_TBBO_QUOTE_SPREAD_EVIDENCE_ENGINEERING_CONVENTION_NOT_BOOK_EXPLICIT`.
- Combined market-order TBBO registry binds the same row-1378 quote and links to the source registry via source row hash `d420b9be6d9da1376f82478243ea1ed07b995cc5f605735dbc516649c1707732` and source ledger SHA256 `871c087bbc2c42b7d0bbb48af74eb0241ec7fc412c572905c9d3b0010c84a397`.
- Row-1378 cost ledger uses bid-fill/no-separate-spread accounting with selected combined-registry row hash `9f191b171dd25e625f140a14431a6691279b3c2a4ff0d92b7d050345d58022f4` and combined registry SHA256 `33f7b270d546e9a4d37a7bafa7c6607c181dd96fa68c3b9019669e8e18b34552`.
- No stale old combined-registry hash literal remains under `src`, `tests`, `docs/process`, or `tools/databento`.
- The old row-1378 acquisition helper remains a prior bounded evidence acquisition tool only; it is not imported/exported by the package root or runtime completion path, and is quarantined by the remediation record.

## Local Test Evidence

- `python -m pytest tests/test_s27_v2_fast_runner_cache.py tests/test_s27_v2_fast_order_generator.py tests/test_s27_v2_fast_downstream_generator.py tests/test_s27_v2_fast_generated_segment_assembler.py tests/test_s27_v2_fast_evidence_planner.py tests/test_s27_v2_fast_execution_state.py tests/test_s27_v2_fast_segment_emitter.py tests/test_s27_v2_test_incremental_runner.py -q` returned `81 passed`.
- `python -m pytest tests/test_s27_v2_2023_test_mechanical_run.py::test_2023_test_mechanical_run_fails_closed_without_result_claim -q` returned `1 passed`.

## Local Hostile Re-Audit

Subagent re-audit returned:

- P0 findings: none.
- P1 findings: none.
- P2 findings: none.
- P3 note: the old row-1378 acquisition helper physically remains and contains Databento/API/download code, but it is quarantined as prior bounded evidence tooling and is not imported/exported by the package root or runtime completion path.

## Decision

Local continuation/checkpoint status is PASS for the row-1378 declared-pack exhaustion checkpoint.

This PASS is not result interpretation, not performance evaluation, not a backtest-result claim, and not a source-faithful evidence claim.
