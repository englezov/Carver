# CARVER S27 ZN V2 2023 TEST Row-1 Market-Order Metadata Implementation And Local Audit

Date: 2026-06-12

Status: LOCAL_PASS_MARKET_ORDER_FILL_METADATA_FAIL_CLOSED_ON_MARKET_SPREAD_NOT_RESULT

## Authorization

Operator authorized the S27_V2 local-only TEST row-1 market-order implementation gate after the market-order source-lock/planning gate, limited to the audited 2023 TEST row-1 target-position gap from `0` to `2` contracts.

The gate authorized deterministic local-only market-order ledger construction for row 1 only, including:

- active TEST input-pack/run artifact binding;
- desired-position/current-position binding;
- full-gap `BUY 2` market-order row emission;
- trigger source condition `BOOK_REQUIRED_TARGET_POSITION_GAP_GREATER_THAN_ONE_CONTRACT`;
- exact next completed hourly fill-row binding at `2023-01-03T01:00:00Z`;
- market fill provenance `MARKET_PRICE_FROM_NEXT_COMPLETED_CLOSE`;
- market fill price `112.5625`;
- same-session, no-roll, and initial-empty-working-state proofs;
- accepted `2.30 USD` per contract per side commission binding;
- explicit fail-closed treatment for numeric market spread cost and PnL/result emission.

This gate did not authorize provider/API access, downloads, new data acquisition, VALIDATION, OOS, Lockbox, Forward, broader TEST continuation beyond the row-1 blocker, result interpretation, PnL evaluation beyond mechanical row construction, tuning, adapter work, deployment, trading, promotion, Git actions, or source-faithful evidence claims.

## Implementation

Patched:

- `src/carver/spine/s27_v2_replay/test_mechanical_run.py`
- `tests/test_s27_v2_2023_test_mechanical_run.py`

The row-1 target-position gap branch now emits metadata only:

- `market_order_ledger.csv`: one full-gap `BUY 2` market-order metadata row.
- `market_fill_metadata_ledger.csv`: one next-completed-hour market-fill metadata row.
- `fail_closed_ledger.csv`: one blocker row preserving the hard stop before numeric market spread cost, PnL, or result emission.

The result-bearing ledgers remain empty for this row-1 TEST gate:

- `cost_ledger.csv`
- `pnl_ledger.csv`
- `validation_ledger.csv`

The positive fill ledger remains empty too:

- `fill_ledger.csv`

This is deliberate. The market-fill metadata row records the source-bound market fill candidate and accepted commission, while actual numeric market-spread cost and downstream PnL/result remain fail-closed.

## Row-1 Bound Facts

Market-order metadata:

- row index: `1`
- decision timestamp: `2023-01-03T00:00:00Z`
- raw symbol: `ZNH3`
- current position before order: `0`
- target position after fill: `2`
- side: `BUY`
- quantity: `2`
- trigger source condition: `BOOK_REQUIRED_TARGET_POSITION_GAP_GREATER_THAN_ONE_CONTRACT`
- row hash: `3c1861259eb8b3081ffb7e762f6899a3f9664007426309451aeef204d5227491`

Market-fill metadata:

- fill timestamp: `2023-01-03T01:00:00Z`
- raw symbol: `ZNH3`
- side: `BUY`
- quantity: `2`
- fill price: `112.5625`
- fill price provenance: `MARKET_PRICE_FROM_NEXT_COMPLETED_CLOSE`
- fill source row hash: `42DE9DA73BB9D701F46DD0FE9F77454848854E363B03D2A82280A3083B6C217E`
- same session: `TRUE`
- roll boundary status: `NO_ROLL_BOUNDARY_SAME_RAW_SYMBOL`
- working state before: `EMPTY_INITIAL_WORKING_STATE`
- position after fill: `2`
- commission per contract: `2.3`
- commission amount: `4.6`
- market spread cost status: `FAIL_CLOSED_NUMERIC_MARKET_SPREAD_COST_UNRESOLVED_NOT_RESULT`
- PnL emission status: `FAIL_CLOSED_PNL_NOT_EMITTED_MARKET_SPREAD_COST_UNRESOLVED`
- row hash: `ec04b7061d5c2f0dd1e9a21c313f216152a5e4393bf5a069a7c42bb2810853e0`

Fail-closed row:

- fail-closed reason: `FAIL_CLOSED_MARKET_SPREAD_COST_UNRESOLVED_BEFORE_PNL_NOT_RESULT`
- secondary fail-closed reason: `MARKET_ORDER_AND_FILL_METADATA_EMITTED_COST_FAIL_CLOSED_BEFORE_PNL`
- result status: `FAIL_CLOSED_RESULT_ROW_NOT_EMITTED_NOT_AUTHORIZED`
- backtest status: `FAIL_CLOSED_BACKTEST_RESULT_NOT_EMITTED_NOT_AUTHORIZED`
- source-faithful evidence claimed: `FALSE`
- row hash: `4422f0f1f063cc5886bbd6de9fcc0a24f63032171b80dbae4570edbe922d867c`

## Artifact Hashes

Run directory:

`docs/researchops/s27_v2_local_replay_runs/ZN/20260612_2023_test_mechanical_artifact_run`

Hashes after implementation:

- `run_manifest.json`: `5401BCE6D1AB1F9642989315B8B324FCFF03F308F8707CE0CD5653E90E83B6F2`
- `evidence_manifest.json`: `591D85E605F8AABE060F2256098B5F0B76463A2B24D0B3BB5334CA8B85C7957B`
- `trusted_bundle.json`: `127D3899F536F1802FF85ABA54CD7A4B47A6654A375D47F21943D46E563E41C9`
- `run_bundle.json`: `6B4ABCE45E74F305DD091751CD13C58DD0D309030461FA8E04F7DBCEB0E78926`
- `market_order_ledger.csv`: `E559B81033385A79A8CD6E1ED781649B476DDB37321FD836D77E78CF30EA41E5`
- `market_fill_metadata_ledger.csv`: `6DF3F066C210DCE72F60856A7EC05E1A729C8D1CE31E4C251249833F50E83466`
- `fail_closed_ledger.csv`: `086270A760E4C4509303FB376D0605E6E4B0644001ABB2A9A00256423D78D1E1`

The audit verified that manifest artifact-file hashes match `evidence_manifest.json` and `SHA256SUMS.csv`.

## Verification

Focused verification passed:

- `python -m py_compile src\carver\spine\s27_v2_replay\test_mechanical_run.py tests\test_s27_v2_2023_test_mechanical_run.py`
- `python -m pytest tests\test_s27_v2_2023_test_mechanical_run.py -q`
  - result: `20 passed`
- `python -m pytest tests\test_s27_v2_pretest_development_recon_completion.py tests\test_s27_v2_2023_test_mechanical_run.py -q`
  - result: `81 passed`

Additional read-only artifact audit passed:

- all run-manifest artifact files are present;
- every artifact file hash matches `SHA256SUMS.csv`;
- every ledger hash matches `evidence_manifest.json`;
- exactly one market-order metadata row is present;
- exactly one market-fill metadata row is present;
- exactly one fail-closed row is present;
- `cost_ledger.csv`, `pnl_ledger.csv`, `validation_ledger.csv`, `fill_ledger.csv`, and `limit_order_ledger.csv` are header-only;
- trusted bundle preserves `source_faithful_evidence_claimed = false`;
- result status remains `FAIL_CLOSED_RESULT_ROW_NOT_EMITTED_NOT_AUTHORIZED`.

## Local Hostile Audit

Local hostile audit status: PASS_NO_P0_P1_P2_FOUND_IN_SCOPE.

The audit checked:

- package-root exports do not expose `test_mechanical_run`;
- row-1 market-order branch is evaluated before adjacent-limit execution;
- target-position gap `0 -> 2` emits full-gap `BUY 2` market-order metadata;
- fill metadata binds the exact next completed hourly row at `2023-01-03T01:00:00Z`;
- fill provenance is `MARKET_PRICE_FROM_NEXT_COMPLETED_CLOSE`;
- fill price is `112.5625`;
- commission binds to accepted `2.30 USD` per contract per side and computes `4.6`;
- numeric market-spread cost remains unresolved and fail-closed;
- actual cost, PnL, result, validation, and source-faithful evidence rows are not emitted;
- VALIDATION, OOS, Lockbox, Forward, provider/API, downloads, new data, tuning, adapter work, deployment, trading, promotion, and Git actions remain unauthorized.

Subagent note: the local subagent tool was not exposed in this Codex session when searched, so the local hostile audit was performed as a direct read-only audit in the main session. This does not replace the authorized GPT 5.5 external hostile audit.

## Current Status

`LOCAL_PASS_PENDING_GPT55_EXTERNAL_AUDIT_NOT_TEST_RESULT_NOT_SOURCE_FAITHFUL_EVIDENCE`

The next step is a GPT 5.5 Extended Pro external hostile audit packet for this row-1 market-order metadata implementation.
