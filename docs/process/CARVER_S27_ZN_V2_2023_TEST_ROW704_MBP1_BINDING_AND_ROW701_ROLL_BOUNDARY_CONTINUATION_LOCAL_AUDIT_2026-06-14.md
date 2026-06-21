# S27 V2 2023 TEST Row 704 MBP-1 Binding And Row 701 Roll-Boundary Continuation Local Audit

Date: 2026-06-14

Status:

```text
LOCAL_PASS_ROW704_MBP1_BOUND_ROW701_ROLL_BOUNDARY_FAIL_CLOSED_NOT_RESULT
```

## Scope

Operator authorized S27_V2 2023 TEST row-704 MBP-1 top-of-book evidence binding and mechanical continuation after local PASS on bounded row-704 MBP-1 acquisition.

Scope was limited to consuming the selected row-704 alternative source-native MBP-1/top-of-book evidence, preserving the not-TBBO/not-book-explicit label, preventing bid-fill/spread double-counting, preserving result/backtest/source-faithful fail-closed gates, and continuing only until the next genuine fail-closed blocker.

This gate authorized no provider/API access, no downloads, no new data acquisition, no VALIDATION, no OOS, no Lockbox, no Forward, no result interpretation, no PnL evaluation beyond mechanical construction, no tuning, no adapter/deployment/trading/promotion, no Git actions, no GPT packet preparation, and no source-faithful evidence claim.

## Code Changes

Patched:

```text
src/carver/spine/s27_v2_replay/test_mechanical_run.py
tests/test_s27_v2_2023_test_mechanical_run.py
```

The runner now:

- includes the row-704 MBP-1 selected-spread registry in the active combined market-spread registry;
- carries row-704 with evidence type `ROW704_ALTERNATIVE_SOURCE_NATIVE_MBP1_TOP_OF_BOOK_AT_OR_BEFORE_FILL`;
- preserves the source evidence label `ALTERNATIVE_SOURCE_NATIVE_MBP1_TOP_OF_BOOK_EVIDENCE_NOT_BOOK_EXPLICIT_NOT_TBBO`;
- allows the bounded 300-second max-age guard for this row-704 alternative evidence only;
- preserves bid-fill/no-separate-spread accounting where the market fill price uses the selected bid;
- stops fail-closed before order/fill/cost/PnL emission if a live order lands on a declared roll-boundary date.

## Row 704 Evidence Binding

The row-704 MBP-1 evidence remains byte/hash/provenance bound:

```text
raw_symbol: ZNM3
fill_timestamp_utc: 2023-02-16T05:00:00Z
selected_quote_ts_event: 2023-02-16T04:59:22.531807131Z
quote_age_seconds: 37.468192999999999
bid_px_00: 112.765625
ask_px_00: 112.78125
selected_executable_market_fill_price: 112.765625
source_evidence_type: ROW704_ALTERNATIVE_SOURCE_NATIVE_MBP1_TOP_OF_BOOK_AT_OR_BEFORE_FILL
selection_status: PASS_ROW704_MBP1_TOP_OF_BOOK_AT_OR_BEFORE_FILL_SELECTED_NOT_RESULT
evidence_label: ALTERNATIVE_SOURCE_NATIVE_MBP1_TOP_OF_BOOK_EVIDENCE_NOT_BOOK_EXPLICIT_NOT_TBBO
selected_registry_sha256: 24EACC1EE68DE6E343724BAD1F6119E1D5D6AA8508A7D6A84C775C4BB52AD16C
```

Combined registry readback:

```text
row_count: 158
registry_sha256: 6230b0907161f1128ccb424786225f2f539cc3ba16ea12ac1faca749cee4b48c
```

Important boundary: row `704` evidence is bound in the registry, but the active TEST run does not consume row `704`, because the expanded roll calendar exposes an earlier row `701` roll-boundary blocker.

## Active TEST Continuation Result

The controlled 2023 TEST declared pack and mechanical artifact run now stop earlier than row `704`:

```text
candidate_rows: 701
supported_rows: 700
fail_closed_row_index: 701
decision_timestamp_utc: 2023-02-16T01:00:00Z
raw_symbol: ZNM3
starting_position_contracts: 0
desired_position_contracts: -1
position_change_contracts: -1
order_side: SELL
adjacent_target_position: -1
fill_candidate_timestamp_utc: 2023-02-16T02:00:00Z
roll_boundary_date: 2023-02-16
fail_closed_reason: FAIL_CLOSED_LIVE_ORDER_ON_UNRESOLVED_ROLL_BOUNDARY_DATE_NOT_RESULT
```

The row-701 fail-closed row preserves:

```text
market_order_required: FALSE
market_order_rows_emitted: FALSE
market_fill_metadata_rows_emitted: FALSE
commission_amount: 0.0
market_spread_cost_status: FAIL_CLOSED_LIVE_ORDER_ON_UNRESOLVED_ROLL_BOUNDARY_DATE
result_status: FAIL_CLOSED_RESULT_ROW_NOT_EMITTED_NOT_AUTHORIZED
backtest_status: FAIL_CLOSED_BACKTEST_RESULT_NOT_EMITTED_NOT_AUTHORIZED
source_faithful_evidence_claimed: FALSE
row_hash: 9e3b19af8e32dbf6ea45aca189551c4697e020505b9003a760020c8ad0ba2862
```

Requirements discovery now stops at the same row-701 roll-boundary class:

```text
total_market_order_rows: 143
missing_tbbo_requirement_count: 0
already_bound_tbbo_count: 143
terminal_status: STOPPED_ON_NEW_BLOCKER_CLASS_FAIL_CLOSED_LIVE_ORDER_ON_UNRESOLVED_ROLL_BOUNDARY_DATE_NOT_RESULT
requirements_ledger_sha256: e9dec2ba8694055ee3ce231f0f5cbc5df4a41524a5f622aa6bc5254c5cf32dda
```

Run artifact readback:

```text
run_status: LOCAL_2023_TEST_MECHANICAL_ARTIFACT_RUN_FAIL_CLOSED_NOT_RESULT
run_manifest_hash: c6d73ea9a82255d4bafc6a6c4cd8ce0b31748ae1dc21e0f4181e0354d37d3135
evidence_manifest_hash: 2280806570e17864a197ad93db676bef6574dfba2f6f98c5765777ee61f10cfb
trusted_bundle_hash: 2ba7d12005b743729d1b121093a36982fa92ae89f88b3224cdc621c756a7e4fe
```

## Verification

Passed:

```text
python -m py_compile src\carver\spine\s27_v2_replay\test_mechanical_run.py tests\test_s27_v2_2023_test_mechanical_run.py tools\databento\carver_s27_v2_2023_test_row704_mbp1_top_of_book_acquisition.py
```

Passed direct bundle/readback verification:

```text
bundle_validate: PASS
bundle_supported_rows: 700
bundle_fail_closed_row_index: 701
bundle_fail_closed_reason: FAIL_CLOSED_LIVE_ORDER_ON_UNRESOLVED_ROLL_BOUNDARY_DATE_NOT_RESULT
combined_registry_rows: 158
row704_evidence_type: ROW704_ALTERNATIVE_SOURCE_NATIVE_MBP1_TOP_OF_BOOK_AT_OR_BEFORE_FILL
row704_selection_status: PASS_ROW704_MBP1_TOP_OF_BOOK_AT_OR_BEFORE_FILL_SELECTED_NOT_RESULT
requirements_rows: 143
requirements_missing: 0
requirements_bound: 143
requirements_max_row: 635
```

Not claimed as passing:

```text
pytest tests\test_s27_v2_2023_test_mechanical_run.py -q
```

The focused pytest file was attempted and timed out at 20 minutes before completion. No full pytest PASS is claimed for this gate.

## Local Hostile Audit

Read-only local hostile audit returned:

```text
P0: none
P1: none
P2: none
```

Audit notes:

- row-704 MBP-1 evidence is preserved as alternative source-native top-of-book evidence, not TBBO and not book-explicit authority;
- row-704 hash ledger entries match current file bytes and the selected row hash recomputes exactly;
- combined-registry historical names still include `TBBO`, but the row-level source evidence type and evidence labels remain explicit;
- side-specific market fill price enforcement and no-separate-spread accounting remain intact;
- row `701` now stops before market-evidence continuation because roll-boundary detection emits a fail-closed row and breaks;
- no active provider/API/download/Git/VALIDATION/OOS/Lockbox/Forward/result/source-faithful surface was introduced.

## Current State

The active checkpoint is:

```text
LOCAL_PASS_ROW704_MBP1_BOUND_ROW701_ROLL_BOUNDARY_FAIL_CLOSED_NOT_RESULT
```

The next useful gate is row-701 live-order roll-boundary policy decision. Row `704` MBP-1 evidence is ready and bound, but row `701` is now the next genuine unresolved policy class.

## Next Authorization Prompt

```text
Operator authorizes S27_V2 2023 TEST row-701 live-order roll-boundary policy decision gate, after local PASS on row-704 MBP-1 evidence binding and mechanical continuation to the earlier row-701 roll-boundary blocker, limited to already-local 2023 TEST artifacts and audited S27_V2 machinery.

Scope is limited to row 701 / the live-order-on-declared-roll-boundary class: ZNM3, decision 2023-02-16T01:00:00Z, starting position 0, desired position -1, position change SELL 1, adjacent target -1, fill candidate 2023-02-16T02:00:00Z, same_session TRUE, declared roll-boundary date 2023-02-16, and current fail-closed reason FAIL_CLOSED_LIVE_ORDER_ON_UNRESOLVED_ROLL_BOUNDARY_DATE_NOT_RESULT.

This gate may inspect current S27_V2 code/tests/process records, session/roll calendar evidence, source-lock execution notes, and local TEST artifacts to decide whether live adjacent-limit or market orders on a declared roll-transition date must fail closed, cancel/no-fill, defer until after roll, use old-symbol/new-symbol handling, or another explicit source-native rule. It may produce process/current-state records, focused tests only if needed, one local hostile audit, and the exact next implementation authorization if a bounded policy is source-locked or explicitly accepted as a local-only engineering convention.

No provider/API access, downloads, new data acquisition, broader TEST continuation, VALIDATION, OOS, Lockbox, Forward, result interpretation, PnL evaluation beyond mechanical construction, tuning, adapter/deployment/trading/promotion, Git actions, GPT packet preparation, or source-faithful evidence claim.
```

## Non-Authorization

This record does not authorize provider/API access, downloads, new data, broader TEST continuation, VALIDATION, OOS, Lockbox, Forward, result interpretation, PnL evaluation beyond mechanical construction, tuning, adapter/deployment/trading/promotion, Git actions, GPT packet preparation, or source-faithful evidence claims.
