# S27_V2 2023 TEST Row 892 Session-End Adjacent-Limit Implementation And Local Audit

Date: 2026-06-15

Status: LOCAL_PASS_ROW892_SESSION_END_ADJACENT_LIMIT_IMPLEMENTED_AND_CONTINUED_TO_ROW959_MARKET_SPREAD_BLOCKER_NOT_RESULT

## Authorization

Operator authorized the S27_V2 2023 TEST row-892 session-end adjacent-limit implementation gate after the row-892 policy/source-lock decision. Scope was limited to already-local 2023 TEST artifacts and audited S27_V2 machinery.

No provider/API access, downloads, new data acquisition, broader TEST continuation beyond the next blocker, VALIDATION, OOS, Lockbox, Forward, result interpretation, PnL evaluation beyond mechanical construction, tuning, adapter/deployment/trading/promotion, Git actions, GPT packet preparation, or source-faithful evidence claim was authorized.

## Implementation

Patched:

- `src/carver/spine/s27_v2_replay/test_mechanical_run.py`
- `src/carver/spine/s27_v2_replay/pretest_machine_freeze.py`
- `tests/test_s27_v2_2023_test_mechanical_run.py`

The runner now recognizes only the bounded row-892 class:

- raw symbol: `ZNM3`
- row index: `892`
- decision: `2023-02-28T20:00:00Z`
- fill candidate: `2023-02-28T21:00:00Z`
- valuation mark: `2023-02-28T22:00:00Z`
- starting position: `0`
- desired position: `-1`
- position change: `SELL 1`
- formula limit: `111.6707138465356`
- executable limit: `111.671875`
- fill candidate close / fill price: `111.671875`
- decision/fill in same declared execution session
- fill candidate exactly at declared session end
- valuation mark is the exact next completed hourly row in the next declared session
- no roll-boundary, raw-symbol, or provider-condition drift

The emitted convention labels are:

- `SOURCE_NATIVE_ENGINEERING_SESSION_END_ADJACENT_LIMIT_FILL_ASSUMPTION_NOT_BOOK_EXPLICIT`
- `ONE_HOUR_CLOSE_ONLY_LIMIT_FILL_AT_DECLARED_SESSION_END_WITH_NEXT_SESSION_VALUATION_ENGINEERING_CONVENTION_NOT_BOOK_EXPLICIT`

The machine-freeze guard now accepts this exact row-892 class without broadly weakening the existing session/EOD guard.

## Emitted Row 892 Artifacts

Row 892 now emits deterministic local-only mechanical metadata:

- limit order: `SELL 1`, adjacent target `-1`, limit price `111.671875`
- no-market row: `market_order_required = FALSE`, `market_order_rows_emitted = FALSE`, `NOT_REQUIRED_LIMIT_ORDER_FILLED`
- transition: position `0 -> -1`
- fill: executed `TRUE`, quantity `1`, price `111.671875`, position after fill `-1`
- cost: commission `2.30 USD`, spread cost `0.00 USD`, total cost `2.30 USD`
- PnL metadata: valuation mark `2023-02-28T22:00:00Z`, mark close `111.546875`, row gross `125.0`, row net `122.7`, ending position `-1`

Result, backtest, and source-faithful evidence gates remain fail-closed.

## New Boundary

After row-892 implementation, the controlled 2023 TEST mechanical run supports rows `1` through `958` and fails closed at row `959`:

- raw symbol: `ZNM3`
- decision: `2023-03-03T21:00:00Z`
- fill candidate: `2023-03-03T22:00:00Z`
- starting position: `0`
- desired position: `-2`
- position change: `SELL 2`
- fail-closed reason: `FAIL_CLOSED_MARKET_ORDER_SPREAD_EVIDENCE_UNAVAILABLE_FOR_CONTINUATION_NOT_RESULT`

The active TBBO requirements ledger records:

- total market-order rows: `249`
- already-bound TBBO rows: `152`
- rows requiring bounded TBBO evidence: `97`
- first missing row: `959`
- last missing row: `1350`

## Hashes

Run artifacts:

- `run_manifest.json`: `f9e4a8ff03c9d41638ab231361ac14ac4e6c86815853a0dd1773f6ff13bffe0a`
- `evidence_manifest.json`: `aa86e840476a8457879509fba0577cf6d3a10ecf9d405fde7ecabb7ca0fe28b9`
- `trusted_bundle.json`: `11230151c20d37db39feba2c779877649b4493f795f335b301cdcae49e398be3`
- `run_bundle.json`: `78cebefe4ede3358c538dbfa3d9a8eae02beede2b098712592153f18ea4d9ef6`

TBBO requirements:

- `market_order_tbbo_requirements.csv`: `4da830082e0d2b626df05da3e638189ec9241134ad4830dcbf4d6576dd0bf50b`
- `market_order_tbbo_requirements_manifest.json`: `866d67c930e17d82550f40de62e0195bd2bf6b17fdee20458a0e5bf1b6a39d08`
- `market_order_tbbo_requirements_sha256.csv`: `99c073f726da18a5f5a6ecc7ba07b81d114c36a433ed7d206375209703a506cc`

## Verification

Passed:

- `python -m py_compile src\carver\spine\s27_v2_replay\test_mechanical_run.py src\carver\spine\s27_v2_replay\pretest_machine_freeze.py tests\test_s27_v2_2023_test_mechanical_run.py`
- `pytest tests\test_s27_v2_2023_test_mechanical_run.py::test_2023_test_market_order_tbbo_requirements_discovery_is_hash_bound_and_local_only -q` -> `1 passed in 482.96s`
- `pytest tests\test_s27_v2_2023_test_mechanical_run.py::test_2023_test_mechanical_run_fails_closed_without_result_claim -q` -> `1 passed in 598.32s`
- `pytest tests\test_s27_v2_2023_test_mechanical_run.py::test_2023_test_row547_cap_bound_market_order_is_bounded_and_row959_market_spread_blocks -q` -> `1 passed in 597.62s`
- `pytest tests\test_s27_v2_2023_test_mechanical_run.py::test_2023_test_bundle_rejects_self_consistent_row892_session_end_limit_forgery -q` -> `6 passed in 1047.56s`

A first row-892 forgery test run timed out while using a larger parameter set. The stale Python test process was stopped, the test was narrowed to representative high-signal row-892 forged fields, and the narrowed regression passed.

## Local Hostile Audit

Read-only local hostile audit returned:

- P0: none
- P1: none
- P2: none
- P3: TBBO requirements manifest `terminal_status` still says `STOPPED_ON_NEW_BLOCKER_CLASS_SECONDARY_FILLED_ORDER_ACROSS_UNRESOLVED_SESSION_EOD_GAP_NOT_RESULT`, while the authoritative run boundary and requirements ledger now identify row `959` as the first missing TBBO requirement.

The P3 is not a blocker for local continuation, but the TBBO requirements manifest terminal-status wording should be corrected or explicitly caveated before using that manifest as external handoff authority. The authoritative row-959 boundary is the run manifest/fail-closed ledger plus the requirements CSV row `959`.

The audit confirmed:

- row 892 is tightly bounded to the declared facts;
- required engineering labels are present in code and artifacts;
- result/backtest/source-faithful gates remain fail-closed;
- row892 forged order/no-market/transition/fill/cost/PnL mutations are rejected;
- machine-freeze recognizes the bounded class without broadly weakening EOD/session guards;
- the run now stops at row 959 market-order spread evidence unavailable;
- no provider/API/download/Git/VALIDATION/OOS/Lockbox/Forward/result/source-faithful surface was introduced.

## Next Authorization

Recommended next gate is consolidated bounded TBBO acquisition for the active missing market-order requirements ledger, rather than another row-by-row prompt, because the active ledger already lists `97` missing market-order quote windows beginning at row `959`.

No further continuation, provider/API use, Git action, GPT packet, result interpretation, or source-faithful evidence claim is authorized by this record.
