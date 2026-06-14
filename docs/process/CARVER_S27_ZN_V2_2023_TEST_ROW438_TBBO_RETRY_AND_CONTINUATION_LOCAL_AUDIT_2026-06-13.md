# S27 V2 ZN 2023 TEST Row 438 TBBO Retry And Continuation Local Audit

Date: 2026-06-13

Status:

```text
LOCAL_PASS_2023_TEST_ROW438_MARKET_ORDER_TBBO_RETRY_AND_CONTINUATION_TO_ROW439_MARKET_TBBO_BLOCKER_NOT_RESULT
```

## Scope

Operator authorized a bounded row-438 market-order TBBO evidence and mechanical continuation gate after local PASS on row 437. Scope was limited to already-local 2023 TEST artifacts and bounded DataBento TBBO evidence for the row-438 ZNH3 market-order blocker only.

Forbidden surfaces remained closed: no broader provider/API access, no downloads, no new data acquisition, no VALIDATION, no OOS, no Lockbox, no Forward, no result interpretation, no PnL evaluation beyond mechanical construction, no tuning, no adapter/deployment/trading/promotion, no Git actions, no GPT packet preparation, and no source-faithful evidence claim.

## Initial Bounded Request

Row-438 initial bounded request:

- Row index: `438`
- Raw symbol: `ZNH3`
- Order side: `SELL`
- Order quantity: `3`
- Decision timestamp: `2023-01-31T01:00:00Z`
- Fill-candidate timestamp: `2023-01-31T02:00:00Z`
- Request window: `2023-01-31T01:59:55Z` through `2023-01-31T02:00:05Z`
- Provider/dataset/schema: `DATABENTO_HISTORICAL` / `GLBX.MDP3` / `tbbo`

The initial `+/-5s` request failed closed:

- Status: `FAIL_CLOSED_ROW438_BOUNDED_DATABENTO_TBBO_INCOMPLETE_NOT_RESULT`
- Quote rows returned: `0`
- Selected rows: `0`
- Provider condition: `FAIL_CLOSED_NO_FRESH_NON_CROSSED_TBBO_QUOTE_SELECTED`

Initial request hashes:

- Request manifest: `5A17AB136B7F0DC23923BDB4DB14193ED2978B84DC05C52FF9744CF09C83051D`
- Initial raw DBN: `E13133B8B45FA5F7E3529C04388AE7CEA08E0E6ADC60D92A168DB6D5AB501014`
- Initial raw CSV: `60D4C37E5D82704AA80BBE49003574DFD1639D98DBD8E5D7AD25588FFFDC2FBE`
- Initial selected-spread registry: `C50E421C27EC59D7DDF9AA2E17452F8EA30CFA6DB2C33024FB4D15A6C87EF35B`
- Initial status JSON: `94971CF0E3A7C8EB23EF3169873C637523B7AE278B5534FB191C2F119D1EAE9A`

## Bounded Retry

Under the standing bounded TBBO policy, one row-438-only retry was performed after the initial request failed closed.

Retry bounds:

- Retry request start: `2023-01-31T01:59:00Z`
- Retry request end: `2023-01-31T02:00:05Z`
- Lookback: `60` seconds
- Lookahead capture: `5` seconds
- Selection rule: `LATEST_NON_CROSSED_POSITIVE_TBBO_AT_OR_BEFORE_FILL_TIMESTAMP`
- Post-fill quote selection: `DISALLOWED_TO_AVOID_LOOKAHEAD`

Selected retry quote:

- Selected quote timestamp: `2023-01-31T01:59:47.160185221Z`
- Quote age seconds: `12.839815`
- Bid: `114.359375`
- Ask: `114.375`
- Executable SELL market fill price: `114.359375`
- Spread points: `0.015625`
- Point value: `1000`
- Spread value per contract: `15.625 USD`
- Accounting convention: `BID_FILL_PRICE_WITH_NO_SEPARATE_SPREAD_COST`
- Separate spread cost emitted: `0.0 USD`

Retry hashes:

- Retry request manifest: `6B35631B249A9FF58006478F17BA56EDEAA22B0E3ACF7FBACDE7CFDCD3625210`
- Retry selected-spread registry: `1B1F88F421B1105244A4A13E5EE069D6289CF532820D99321A51D19B5859DC0B`
- Retry raw DBN: `4C82A1B3976196062077D28BBEBA49271F1826205AAA33B0C01EE63FE960C936`
- Retry raw CSV: `DD1E56E8BCCBEC2B0D5DDEB7FAD5E7839FD531E325F3A619654D2B8B57EB0766`
- Retry provider-condition ledger: `31FC5555096A88DFE39E6D4A91C8EF5F5F8F95CEDE1450D9A27D5285FB8296DD`
- Retry status JSON: `6300591747017973B0696353A7F54A034DA1451E22FF57C1BB41B41B60CA479B`

## Implementation

Added row-specific bounded provider tools:

```text
tools/databento/carver_s27_v2_2023_test_row438_market_spread_tbbo_acquisition.py
tools/databento/carver_s27_v2_2023_test_row438_market_spread_tbbo_failed_window_retry.py
```

Patched:

```text
src/carver/spine/s27_v2_replay/test_mechanical_run.py
tests/test_s27_v2_2023_test_mechanical_run.py
```

Changes:

- Added row-438 retry registry path and evidence type to the active combined TBBO registry.
- Combined market-order TBBO registry now has `87` rows and includes row `438`; row `439` remains absent.
- Added row-438 artifact assertions and self-consistent forged row/hash mutation tests.
- Added row-438 combined registry drift test.
- Hardened TBBO requirements discovery so already-bound rows carry bound source evidence type, selected quote timestamp, quote age, selection status, selected row hash, and selected ledger hash.
- Retry-bound rows now record `max_selected_quote_age_seconds = 60.0`; missing rows retain `5.0` and `MISSING_REQUIRES_BOUNDED_TBBO_EVIDENCE` placeholders.

Provenance repair:

- Requirements ledger: `163239EAA3DD11099441F2D5CC5F37D82653081DF42B5BEE43B4DF7A88FD69BB`
- Requirements manifest: `FE28BC85FF5A0F99C5C60A05AF67964321267CC0330A6B4E91566EFBA7A40AE4`
- Combined TBBO registry: `E0F9AA148C5CFA1899E0FD287CE25327B3122C21D8864B13755697CDBCA4C9F5`

Row 438 in the requirements ledger now binds:

- `ROW438_RETRY_AT_OR_BEFORE_FILL_TBBO`
- selected quote timestamp `2023-01-31T01:59:47.160185221Z`
- quote age `12.839815`
- max selected quote age `60.0`
- selection status `PASS_FRESH_NON_CROSSED_TBBO_QUOTE_SELECTED_NOT_RESULT`

Row 439 remains:

```text
REQUIRES_BOUNDED_DATABENTO_TBBO_EVIDENCE
```

## Mechanical Run State

The regenerated controlled 2023 TEST mechanical artifact run supports rows `1` through `438` and fails closed at row `439`.

Row 438 emitted local-only market/fill/cost/mechanical-PnL metadata:

- Starting position: `19`
- Desired position: `16`
- Position change: `SELL 3`
- Fill candidate: `2023-01-31T02:00:00Z`
- Fill price: `114.359375`
- Commission: `6.8999999999999995 USD`
- Spread cost: `0.0 USD`
- Valuation mark: `2023-01-31T03:00:00Z`
- Valuation mark close: `114.375`
- Row gross mechanical PnL: `250.0`
- Row net mechanical PnL: `243.1`
- Ending position: `16`

Mechanical construction totals are recorded only as artifact fields. They are not result interpretation, performance evaluation, source-faithful evidence, promotion, or trading evidence.

Run hashes:

- Run manifest: `3BDD5D8DC4585AE9696DE92F5ACE838BA9542AF5FEC0F849FD4E516AA401F1BC`
- Evidence manifest: `99C4E1AC736A90F936006B8F4EC9F59757AB3D2A8E52ABAAA2C5FA63A3CD8E45`
- Trusted bundle: `9810484BE573CEEA6B5A31E42DD6FD6AC123560833EC49F5E1D2D1C80D9325BA`
- Run bundle file: `D2F5BA4B8FBBF70EC7E641BCC5BB5E4D5A6ABC66982C1AFFDB2ACC037F759783`
- Run SHA256SUMS: `62D0148C5DDC157FCB18ECA69315D048BDE4CE9DC850662227335F87B5E1F52E`

Next blocker:

- Row index: `439`
- Decision timestamp: `2023-01-31T02:00:00Z`
- Fill-candidate timestamp: `2023-01-31T03:00:00Z`
- Raw symbol: `ZNH3`
- Starting position: `16`
- Desired position: `18`
- Position change: `BUY 2`
- Fail-closed reason: `FAIL_CLOSED_MARKET_ORDER_SPREAD_EVIDENCE_UNAVAILABLE_FOR_CONTINUATION_NOT_RESULT`

## Verification

Passed:

```text
python -m py_compile tools\databento\carver_s27_v2_2023_test_row438_market_spread_tbbo_acquisition.py tools\databento\carver_s27_v2_2023_test_row438_market_spread_tbbo_failed_window_retry.py src\carver\spine\s27_v2_replay\test_mechanical_run.py tests\test_s27_v2_2023_test_mechanical_run.py
python -m pytest tests\test_s27_v2_2023_test_mechanical_run.py::test_2023_test_mechanical_run_fails_closed_without_result_claim tests\test_s27_v2_2023_test_mechanical_run.py::test_2023_test_bundle_rejects_self_consistent_row438_market_tbbo_forgery tests\test_s27_v2_2023_test_mechanical_run.py::test_2023_test_combined_tbbo_registry_rejects_self_consistent_row438_drift tests\test_s27_v2_2023_test_mechanical_run.py::test_2023_test_market_order_tbbo_requirements_discovery_is_hash_bound_and_local_only -q
python -m pytest tests\test_s27_v2_2023_test_mechanical_run.py -q
python -m pytest tests\test_s27_v2_pretest_development_recon_completion.py tests\test_s27_v2_2023_test_mechanical_run.py -q
```

Results:

- Focused row-438/requirements tests: `15 passed`
- P2 remediation focused tests: `14 passed`
- Focused TEST suite: `134 passed`
- Paired pretest/TEST suite: `195 passed`

One full-suite run briefly hit a Windows file-open error in a test that rewrites the requirements CSV for a forgery check. The exact failed test passed on immediate rerun, and the full suite passed after rerun.

## Local Hostile Audit

One read-only local hostile-audit subagent initially found one P2: row-438 acquisition/retry manifests still pointed to the previous requirements-ledger hash, and the current row-438 requirements row did not distinguish the retry-selected quote age from the original `+/-5s` request.

After remediation, the same local hostile-audit subagent re-audited and returned:

```text
P0: none
P1: none
P2: none
P3: none
```

The re-audit confirmed:

- Current requirements ledger hash is `163239EAA3DD11099441F2D5CC5F37D82653081DF42B5BEE43B4DF7A88FD69BB`.
- Row 438 binds `ROW438_RETRY_AT_OR_BEFORE_FILL_TBBO`, quote timestamp `2023-01-31T01:59:47.160185221Z`, quote age `12.839815`, selection status `PASS_FRESH_NON_CROSSED_TBBO_QUOTE_SELECTED_NOT_RESULT`, and max selected quote age `60.0`.
- Row 439 remains missing with bound fields set to `MISSING_REQUIRES_BOUNDED_TBBO_EVIDENCE`.
- Initial and retry row-438 manifests both bind the current requirements hash.
- No new provider/API, Git, protected-window, result-interpretation, or source-faithful claim surface was opened.

## Current Status

```text
LOCAL_PASS_2023_TEST_ROW438_MARKET_ORDER_TBBO_RETRY_AND_CONTINUATION_TO_ROW439_MARKET_TBBO_BLOCKER_NOT_RESULT
```

The next useful gate is row-439 bounded market-order TBBO evidence and mechanical continuation under the standing bounded TBBO policy or an equivalent fresh authorization.

External GPT/Opus audits remain deferred until a consolidated checkpoint unless separately authorized.

This record does not authorize broader provider/API access, downloads, new data acquisition, VALIDATION, OOS, Lockbox, Forward, result interpretation, PnL evaluation beyond mechanical construction, tuning, adapter/deployment/trading/promotion, Git actions, GPT packet preparation, or source-faithful evidence claims.
