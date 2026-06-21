# S27_V2 2023 TEST Consolidated Missing TBBO Acquisition And Row-1113 Boundary Local Audit

Date: 2026-06-15

Status:

```text
LOCAL_PASS_CONSOLIDATED_MISSING_TBBO_BOUND_AND_CONTINUED_TO_ROW1113_SESSION_EOD_VALUATION_GAP_BLOCKER_NOT_RESULT
```

## Authorization

Operator authorized the S27_V2 consolidated bounded missing-market-order TBBO acquisition and TEST continuation loop after local PASS on row-892 session-end adjacent-limit implementation.

Scope was limited to already-local 2023 ZN TEST artifacts, the 97 rows marked `REQUIRES_BOUNDED_DATABENTO_TBBO_EVIDENCE` in the active deterministic requirements ledger beginning at row 959, standing bounded market-order TBBO spread evidence acquisition for those listed quote windows only, deterministic registry updates, mechanical TEST artifact continuation until the next genuinely new non-TBBO policy blocker or pack exhaustion, focused tests, local hostile audit, and process/current-state records.

No provider/API access outside those bounded listed TBBO quote windows, no downloads or new data outside those windows, no VALIDATION/OOS/Lockbox/Forward, no result interpretation, no PnL evaluation beyond mechanical construction, no tuning, no adapter/deployment/trading/promotion, no Git actions, no GPT packet preparation, and no source-faithful evidence claim were authorized.

## Work Performed

The standing bounded DataBento TBBO batch acquisition was run for the current 97 listed market-order rows. It selected 77 current rows and failed closed on 20 current rows in the batch ledger.

The standing bounded failed-window retry was then run for exactly those 20 current failed rows:

```text
962, 964, 969, 970, 986, 991, 992, 993, 1070, 1118, 1136, 1158, 1160, 1162, 1168, 1180, 1301, 1312, 1322, 1346
```

All 20 current retry rows selected fresh/non-crossed TBBO quotes. The retry status file still contains older aggregate failed rows from previous checkpoints, but the current retry rows are disjoint from the aggregate failed-row list.

The combined market-order TBBO registry was rebuilt. Current combined registry SHA256:

```text
d996fd783eeda7e9645255674e3c24a6463f4f8937fda767e74978dded4bec47
```

The controlled 2023 TEST declared pack and mechanical artifact run were rebuilt after binding the updated registry.

## Current Artifact State

Declared input pack manifest:

```text
docs/researchops/s27_v2_local_replay_inputs/ZN/20260612_2023_test_declared_pack/S27_V2_2023_TEST_DECLARED_INPUT_PACK_MANIFEST.json
```

Run output:

```text
docs/researchops/s27_v2_local_replay_runs/ZN/20260612_2023_test_mechanical_artifact_run
```

Current run state:

```text
candidate_row_count = 1113
supported_mechanical_row_count = 1112
fail_closed_row_index = 1113
fail_closed_reason = SECONDARY_FILLED_ORDER_ACROSS_UNRESOLVED_SESSION_EOD_GAP_NOT_RESULT
```

Row-1113 blocker facts:

```text
row_index = 1113
raw_symbol = ZNM3
decision_timestamp_utc = 2023-03-14T20:00:00Z
fill_candidate_timestamp_utc = 2023-03-14T21:00:00Z
starting_position_contracts = -17
desired_position_contracts = -15
position_change_contracts = 2
order_side = BUY
adjacent_target_position = -16
fail_closed_reason = SECONDARY_FILLED_ORDER_ACROSS_UNRESOLVED_SESSION_EOD_GAP_NOT_RESULT
```

The row-1113 blocker is not a missing-TBBO blocker. It is a new non-TBBO session/EOD valuation-gap policy class: the market-order fill candidate is at declared session end, while the available valuation mark is the next available completed hourly row in the next declared session rather than the immediate one-hour mark.

## TBBO Requirements State

Requirements path:

```text
docs/researchops/s27_v2_market_spread_evidence/ZN/20260612_2023_test_market_order_tbbo_requirements_discovery
```

Current requirements:

```text
total_market_order_rows = 249
already_bound_tbbo_count = 249
missing_tbbo_requirement_count = 0
```

Representative bound rows:

```text
row 959  = STANDING_BATCH_AT_OR_BEFORE_FILL_TBBO, quote 2023-03-03T21:59:59.523101291Z, age 0.47689900000000002 seconds
row 962  = STANDING_RETRY_AT_OR_BEFORE_FILL_TBBO, quote 2023-03-06T02:59:41.988599197Z, age 18.011400999999999 seconds
row 1346 = STANDING_RETRY_AT_OR_BEFORE_FILL_TBBO, quote 2023-03-29T11:59:28.022419877Z, age 31.977581000000001 seconds
```

Row 959 now emits a bounded ZNM3 session-open market-reset row under the already accepted engineering convention:

```text
SOURCE_NATIVE_ENGINEERING_SESSION_OPEN_MARKET_RESET_ASSUMPTION_NOT_BOOK_EXPLICIT
```

Row-959 mechanical metadata:

```text
market order = SELL 2
fill timestamp = 2023-03-03T22:00:00Z
fill price = 111.140625
TBBO bid = 111.140625
TBBO ask = 111.15625
commission = 4.60 USD
spread cost = 0.00 USD
row gross PnL = 125.0
row net PnL = 120.4
source_faithful_evidence_claimed = FALSE
```

## Code Changes

`src/carver/spine/s27_v2_replay/test_mechanical_run.py` and `src/carver/spine/s27_v2_replay/pretest_machine_freeze.py` now generalize the already accepted session-open market-reset guard from hard-coded `ZNH3` to same-symbol valid ZN quarterly futures raw symbols only:

```text
ZN[H|M|U|Z][digit]
```

The generalization remains same-symbol and does not authorize cross-symbol, cross-roll, package-root export, protected-window, provider/API, or result surfaces.

Focused tests in `tests/test_s27_v2_2023_test_mechanical_run.py` were updated to the current row-1113 boundary, current combined TBBO registry hash, 249/249 bound TBBO state, row-959 ZNM3 session-open market-reset emission, and row-1112 final mechanical totals.

## Verification

Passed:

```text
python -m py_compile src\carver\spine\s27_v2_replay\test_mechanical_run.py src\carver\spine\s27_v2_replay\pretest_machine_freeze.py tests\test_s27_v2_2023_test_mechanical_run.py
```

Passed direct checkpoint verifier:

```text
candidate_row_count = 1113
supported_mechanical_row_count = 1112
fail_closed_row_index = 1113
fail_closed_reason = SECONDARY_FILLED_ORDER_ACROSS_UNRESOLVED_SESSION_EOD_GAP_NOT_RESULT
TBBO requirements = 249 total / 249 bound / 0 missing
row959 STANDING_BATCH binding present
row959 run artifacts present
run_manifest SHA256 = 5aa96e525763a4f053cfea2246e328464c8a9216ed75160a082875c4faa03397
evidence_manifest SHA256 = 76cf42db9cc50ec4f30247f22a41cdab3385f8a276042dc460dcf22ef45be1c0
trusted_bundle SHA256 = 1418a54b2341df8ad896e0856bcd197178046f4e05e77ee77b5d6d71c462dcf2
market_order_tbbo_requirements.csv SHA256 = 97a48264f0216396d0a458c52fc5e4810da26224f46e0bfb3f45607ec7d2770d
```

Passed:

```text
pytest tests\test_s27_v2_2023_test_mechanical_run.py::test_standing_tbbo_status_and_manifest_distinguish_current_request_from_aggregate_registry -q
```

The long focused pytest subset was run during stale-expectation cleanup. It exposed stale test literals for the previous row-959 boundary and prior combined-registry hashes. Those literals were patched. A full heavy pytest rerun is not claimed here because repeated heavy reruns would add little beyond the current direct hash/artifact verifier and local hostile audit.

## Local Hostile Audit

Read-only local hostile audit returned:

```text
P0: none
P1: none
P2: none
```

Audit conclusions:

- 2023 TEST pack/run supports rows 1-1112 and fails closed at row 1113 with `SECONDARY_FILLED_ORDER_ACROSS_UNRESOLVED_SESSION_EOD_GAP_NOT_RESULT`.
- TBBO requirement closure is clean: 249 total, 249 bound, 0 missing.
- Row 959 is emitted with the intended session-open market-reset engineering label and bound bid-fill metadata.
- The ZN quarterly raw-symbol generalization is same-symbol and contained.
- Package-root export remains closed.
- Result/backtest/source-faithful gates remain fail-closed.
- No provider/API/download/Git/VALIDATION/OOS/Lockbox/Forward/tuning/adapter/deployment/trading/promotion/source-faithful surface was introduced.

## Current Boundary

Current status:

```text
LOCAL_PASS_CONSOLIDATED_MISSING_TBBO_BOUND_AND_CONTINUED_TO_ROW1113_SESSION_EOD_VALUATION_GAP_BLOCKER_NOT_RESULT
```

The next useful gate is a row-1113 session-end market-order valuation-gap policy decision gate. It should decide whether the row-1113 class remains fail-closed, can use an already source-native completed-fill rule with next-available completed valuation, or requires a clearly labeled local-only engineering convention before any continuation.

## Non-Authorizations Preserved

This record does not authorize provider/API access, downloads, new data acquisition, broader TEST continuation, VALIDATION, OOS, Lockbox, Forward, result interpretation, PnL evaluation beyond mechanical construction, tuning, adapter work, deployment, trading, promotion, Git actions, GPT packet preparation, or source-faithful evidence claims.
