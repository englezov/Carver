# Carver S27 ZN V2 Market-Order Policy Source Lock And Implementation Plan

Date: 2026-06-12

Status:

```text
PROCESS_ONLY_MARKET_ORDER_POLICY_SOURCE_LOCK_AND_IMPLEMENTATION_PLAN_NOT_IMPLEMENTATION_NOT_TEST_RERUN
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Authorization

Operator authorized a local-only market-order execution policy source-lock and
implementation-planning gate after GPT 5.5 PASS on the repaired 2023 TEST row-1
market-order fail-closed packet.

This gate is process-only. It does not emit market-order rows, fill rows, cost
rows, PnL rows, result rows, TEST reruns, result interpretation, provider/API
access, downloads, new data, VALIDATION, OOS, Lockbox, Forward, Git actions,
adapter work, deployment, trading, promotion, tuning, or source-faithful
evidence claims.

## Inputs Inspected

- `docs/process/CARVER_S27_ZN_BOOK_SOURCE_LOCK_2026-06-05.md`
- `docs/process/CARVER_S26_EXECUTION_SEMANTICS_SOURCE_LOCK_RESULT_2026-05-31.md`
- `docs/process/CARVER_S27_ZN_POSITION_EXECUTION_COST_SEMANTICS_LOCK_2026-05-31.md`
- `src/carver/spine/s27_v2_replay/test_mechanical_run.py`
- `src/carver/spine/s27_v2_replay/orders.py`
- `src/carver/spine/s27_v2_replay/fills.py`
- `src/carver/spine/s27_v2_replay/costs.py`
- `src/carver/spine/s27_v2_replay/transitions.py`
- `docs/researchops/s27_v2_local_replay_inputs/ZN/20260612_2023_test_declared_pack/*`
- `docs/researchops/s27_v2_local_replay_runs/ZN/20260612_2023_test_mechanical_artifact_run/*`
- GPT 5.5 repaired packet PASS pasted by operator on 2026-06-12.

No fresh PDF extraction was performed in this gate. The book authority used here
is the existing source-lock artifact, which records local inspection of
`Carver.pdf` pages 475-506 and the relevant S26/S27 execution passages.

## Current Row-1 TEST Blocker

The repaired TEST packet is byte-verifiable and now fails closed at the first
TEST row:

```text
decision_timestamp_utc = 2023-01-03T00:00:00Z
raw_symbol = ZNH3
starting_position_contracts = 0
desired_position_contracts = 2
position_change_contracts = 2
order_side = BUY
adjacent_target_position = 1
market_order_required = TRUE
market_order_rows_emitted = FALSE
market_order_reason = BOOK_REQUIRED_TARGET_POSITION_GAP_GREATER_THAN_ONE_CONTRACT
fail_closed_reason = FAIL_CLOSED_BOOK_REQUIRED_MARKET_ORDER_FOR_TARGET_GAP_GT_ONE_NOT_AUTHORIZED_NOT_RESULT
```

The repaired GPT 5.5 packet audit returned `PASS`; the previous packet
construction failure was caused by missing zip entries, not by corrupted local
artifacts. The repaired packet ZIP SHA256 recorded by GPT is:

```text
4e5487034e2a62f2850062f9f73ffc2a243d277dd367eee023321eb83a1ec606
```

The current fail-closed state is correct and must not be bypassed by adjacent
limit-order logic.

## Source-Locked Market-Order Decisions

The S27 v2 book source lock requires explicit execution ledgers, including:

- desired rounded position;
- adjacent-position implied limit prices;
- working limit-order state;
- single-lot adjacent limit orders where the book permits them;
- cancellation/reset of working orders at end-of-day boundaries;
- one-hour-lag limit fill decision;
- market-order cases required by the book, including target-position gaps
  greater than one contract, cap-bound cases where a limit side is not placed,
  and overnight/session gap cases;
- one-hour-lag market-order fill decision;
- roll handling, labeled book-native only where source support exists;
- commission rows for all orders;
- spread-cost rows for market orders when required;
- PnL rows tied to fills and held position state.

For the row-1 TEST blocker, the only active source condition is:

```text
TARGET_POSITION_GAP_GREATER_THAN_ONE_CONTRACT
```

The required order class is therefore:

```text
MARKET_ORDER
```

The market order must target the full current-to-desired position gap, not only
the adjacent single-lot step:

```text
current_position_before_order = 0
target_position_after_fill = 2
quantity = 2
side = BUY
trigger_source_condition = BOOK_REQUIRED_TARGET_POSITION_GAP_GREATER_THAN_ONE_CONTRACT
```

Adjacent limit-order calculation must remain downstream of the market-order
gap classifier and must not run for this row.

## Fill Timing And Price Policy

The source-lock requires a one-hour-lag market-order fill decision. The current
v2 structural fill surface already has the only completed-bar-compatible market
fill provenance:

```text
MARKET_PRICE_FROM_NEXT_COMPLETED_CLOSE
```

For a normal same-session row, the implementation plan is:

```text
decision row = 2023-01-03T00:00:00Z ZNH3
fill candidate row = exact next completed hourly ZNH3 row at 2023-01-03T01:00:00Z
fill price provenance = MARKET_PRICE_FROM_NEXT_COMPLETED_CLOSE
market fill price = fill candidate close price = 112.5625
```

This is the local completed-bar market-fill proxy. It is not an intrabar fill,
not a bid/ask quote fill, and not a source-faithful performance claim by itself.
If a later book-attached audit rejects this completed-close proxy, the TEST
runner must fail closed again rather than silently substitute another price.

## Cost Policy Boundary

The source-lock records:

```text
LIMIT_ORDER_FILL_COST = COMMISSION_ONLY
MARKET_ORDER_FILL_COST = COMMISSION_PLUS_NORMAL_BID_ASK_SPREAD
ALL_ORDERS_PAY_COMMISSION
```

The current TEST input pack cost row is:

```text
commission_per_contract_per_side = 2.30 USD
spread_cost_policy = LIMIT_FILL_COMMISSION_ONLY_NO_MARKET_SPREAD
```

Therefore the current TEST pack is sufficient for commission but not sufficient
for numeric market-order spread cost. A market-order implementation may emit the
market order and fill only if it also binds one of the following before cost/PnL:

1. a source-locked book/source-native normal ZN bid/ask spread;
2. a separately accepted inferred source-native retail futures normal spread
   assumption, clearly labeled as inferred and not book-explicit;
3. an explicit fail-closed market-cost state that prevents PnL/result emission.

Prop-firm fees, CFD spreads/swaps, adapter-specific costs, or personal trading
costs remain prohibited as source-faithful strategy costs.

## Session, Roll, And Working-State Constraints

For row 1, the declared decision, fill, and valuation rows all use the same raw
symbol `ZNH3` and same session id:

```text
UTC_ZN_2023_TEST_2023-01-02T22:00:00Z_2023-01-03T21:00:00Z
```

The market-order implementation must still validate:

- exact next completed hourly fill row;
- same raw symbol unless a separately source-locked roll bridge exists;
- same-session normal transition for this row;
- no open working limit order before the first row;
- no adjacent limit-order order plan emitted for the same target-gap blocker;
- no roll-boundary or overnight recompute path unless separately source-locked.

## Implementation Plan For The Next Gate

The next implementation gate should be narrow and must cover:

1. Add row-1 market-order order-plan construction to `test_mechanical_run.py`.
2. Emit a market-order ledger row for target gaps greater than one contract.
3. Bind the market order to active desired-position row, starting position,
   full target position, quantity, side, trigger source condition, and row hash.
4. Use the exact next completed hourly fill row for the market fill decision.
5. Emit a market fill row using `MARKET_PRICE_FROM_NEXT_COMPLETED_CLOSE`.
6. Add transition metadata for the normal one-hour same-session market fill.
7. Bind commission cost to the accepted `2.30 USD` per contract per side cost
   policy.
8. Resolve market spread cost before actual PnL emission:
   - if numeric normal spread is source/inference-accepted, emit market spread
     and total cost rows;
   - otherwise emit an explicit market-cost fail-closed row and do not emit PnL
     or result rows.
9. Preserve machine-freeze guards for unresolved market-spread, session/EOD,
   roll, degraded-provider, zero-sign, and protected-window states.
10. Run focused local verification and local hostile audit before any external
    packet or TEST continuation claim.

## Next Exact Operator Authorization Prompt

```text
Operator authorizes S27_V2 local-only TEST row-1 market-order implementation gate, after the market-order source-lock/planning gate, limited to the audited 2023 TEST row-1 target-position gap from 0 to 2 contracts.

This authorizes Codex to implement deterministic local-only market-order ledger construction for the row-1 TEST blocker only: active TEST input-pack/run artifact binding, desired-position/current-position binding, full-gap BUY 2 market-order row emission, trigger_source_condition = BOOK_REQUIRED_TARGET_POSITION_GAP_GREATER_THAN_ONE_CONTRACT, exact next completed hourly fill-row binding at 2023-01-03T01:00:00Z, market fill provenance MARKET_PRICE_FROM_NEXT_COMPLETED_CLOSE, market fill price 112.5625, same-session/no-roll/initial-empty-working-state proofs, accepted 2.30 USD per contract per side commission binding, and explicit fail-closed treatment for numeric market spread cost and PnL/result emission unless a source-native normal spread policy is separately locked within this gate.

This authorizes focused local verification tests, one consolidated local hostile audit with subagents, process/current-state records, and a GPT 5.5 external hostile-audit packet after local PASS.

No provider/API access, downloads, new data acquisition, VALIDATION, OOS, Lockbox, Forward, broader TEST continuation beyond the row-1 market-order blocker, result interpretation, PnL evaluation beyond mechanical row construction, tuning, adapter work, deployment, trading, promotion, Git staging/commit/push/PR, or source-faithful evidence claim.

If numeric market spread cost cannot be source-locked or explicitly inference-accepted, Codex must emit market-order/fill metadata only as far as authorized and fail closed before actual PnL/result emission.
```

## Non-Authorization

This record authorizes no implementation, no row emission, no TEST rerun, no
provider/API access, no downloads, no new data, no VALIDATION, no OOS, no
Lockbox, no Forward, no result interpretation, no PnL evaluation, no tuning, no
adapter work, no deployment, no trading, no promotion, no Git actions, and no
source-faithful evidence claim.
