# CARVER S27 ZN V2 - 2023 TEST Cap-Bound Adjacent-Limit Policy Decision

Date: 2026-06-14

## Scope

Operator authorized the S27_V2 2023 TEST cap-bound adjacent-limit policy decision gate after local PASS on the row-547 cap-bound fail-closed classification.

Scope was limited to deciding whether cap-bound adjacent targets must remain fail-closed or may use a narrowly labeled local-only engineering convention. The gate could inspect current code, tests, process/source-lock records, and local TEST artifacts. No provider/API access, downloads, new data acquisition, TEST continuation beyond row 547, VALIDATION, OOS, Lockbox, Forward, result interpretation, tuning, adapter/deployment/trading/promotion, Git actions, GPT packet preparation, or source-faithful evidence claim was authorized.

## Row 547 Facts

- row index: `547`
- raw symbol: `ZNH3`
- decision timestamp: `2023-02-07T00:00:00Z`
- starting position: `26`
- desired position: `25`
- position change: `SELL 1`
- adjacent target: `25`
- same session: `TRUE`
- trend: `0.43902119250205374`
- base position: `12.363067774093599`
- implied target capped forecast: `20.221518199865148`
- source-locked forecast cap: `20.0`

## Source/Process Evidence

The cap-edge remediation record says adjacent order generation must precheck whether a candidate target is trend-permitted and strictly inside the forecast cap before calling implied-price inversion. Cap-side candidates that are not priceable must not silently become limit prices.

The market-order source-lock records also state that S27 V2 execution machinery includes market-order cases required by the book, including target-position gaps greater than one contract, cap-bound cases where a limit side is not placed, and overnight/session gap cases.

The trigger/roll-boundary remediation record further requires trigger-specific validation: buy/sell cap-bound market triggers require matching cap-side forecast state and a one-contract gap.

## Decision

No cap-edge adjacent-limit pricing convention is accepted.

Cap-bound adjacent targets remain unpriceable by the adjacent-limit implied-price inversion unless the target is strictly inside the forecast cap. The row-547 adjacent target `25` implies capped forecast `20.221518199865148`, which is outside/at the cap boundary relative to the source-locked `20.0` cap. The runner must not fabricate a cap-edge limit price and must not label such a price as book-explicit or source-faithful.

The source/process records support a separate class-level interpretation: when a cap-bound adjacent target means the limit side is not placed, the case may be treated as a bounded market-order-required class, but only after a separate implementation gate binds the exact row/class facts, side, quantity, forecast cap-side state, session/roll/working-state evidence, and bounded TBBO market-spread evidence.

For row 547, the candidate future class is:

`CAP_BOUND_LIMIT_SIDE_NOT_PLACED_MARKET_ORDER_REQUIRED_NOT_RESULT`

This decision does not implement that class and does not continue the TEST run.

## Local Hostile Audit

P0 findings: none.

P1 findings: none.

P2 findings: none.

Audit checks:

- no engineering cap-edge limit convention was accepted;
- cap-bound adjacent-limit targets remain fail-closed until a separate market-order implementation gate;
- the proposed future class is tied to already-recorded source/process evidence for cap-bound cases where a limit side is not placed;
- row 547 remains terminal under the current artifacts;
- no provider/API/download/new-data/protected-window/Git/GPT/result/source-faithful surface was introduced;
- no result interpretation, performance evaluation, tuning, promotion, or source-faithful evidence claim was made.

## Current Status

`POLICY_DECISION_CAP_BOUND_ADJACENT_LIMIT_NO_LIMIT_CONVENTION_MARKET_ORDER_CLASS_PENDING_NOT_RESULT`

The next useful gate is a bounded cap-bound market-order class implementation and continuation gate. That gate should allow implementation only where the row facts match the source/process class: cap-bound target, matching cap-side forecast state, one-contract gap, no unresolved roll/session/working-state evidence, and bounded TBBO market-order evidence. If any of those facts are missing or degraded, the row must remain fail-closed.
