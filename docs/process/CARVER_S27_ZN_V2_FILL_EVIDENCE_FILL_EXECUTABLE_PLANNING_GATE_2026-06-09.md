# S27_V2 Fill Evidence / Fill Executable Planning Gate

Date: 2026-06-09

Status:

```text
PROCESS_ONLY_FILL_PLANNING_AFTER_ORDER_TRANSITION_EXTERNAL_PASS
```

## Authorization

Operator authorized a local-only fill-evidence/fill-executable planning gate after external PASS on the order/transition executable remediation-pack surface.

Authorized scope:

- inspect current `S27_V2` code/tests/process records and source-lock artifacts;
- record the order/transition external PASS synthesis;
- identify whether the no-order/no-position-change transition should produce an explicit no-fill metadata row or remain fail-closed;
- define required evidence for any future actual fill ledger;
- propose the next exact implementation authorization.

Non-authorized scope:

- no provider/API access;
- no downloads or new data;
- no OOS/Lockbox/Forward;
- no backtests or result-scored runs;
- no actual fill emission unless separately authorized after this planning gate;
- no cost emission;
- no PnL/result emission;
- no result interpretation or PnL evaluation;
- no tuning;
- no adapter work, deployment, trading, promotion;
- no Git actions;
- no source-faithful evidence claim.

## External PASS Context

The order/transition executable surface externally passed:

```text
docs/process/CARVER_S27_ZN_V2_ORDER_TRANSITION_EXECUTABLE_EXTERNAL_AUDIT_SYNTHESIS_2026-06-09.md
```

External audit confirmed:

- active desired-position authority binding;
- zero-delta/no-order enforcement;
- content-bound order-intent/transition/bundle hashes;
- standalone row non-authority;
- fail-closed adjacent limit, market fallback, tick rounding, and working-order lifecycle;
- no limit/market/fill/cost/PnL/result/backtest/provider/API/download/Git/source-faithful evidence surface.

## Current Upstream State

The order/transition executable surface emits deterministic metadata:

```text
order_kind = NO_ORDER
order_side = NONE
order_quantity = 0
transition_kind = NO_POSITION_CHANGE_NO_ORDER
position_change_contracts = 0
ending_position_without_fill = 0
```

The source-sensitive execution policies remain:

```text
ADJACENT_LIMIT_ORDER_POLICY = FAIL_CLOSED_UNRESOLVED_NOT_EMITTED
MARKET_FALLBACK_POLICY = FAIL_CLOSED_UNRESOLVED_NOT_EMITTED
TICK_ROUNDING_POLICY = FAIL_CLOSED_UNRESOLVED_NOT_EMITTED
WORKING_ORDER_LIFECYCLE = FAIL_CLOSED_UNRESOLVED_NOT_EMITTED
```

## Fill Source Requirements

The source lock says true S27/S26 execution ultimately requires:

- explicit adjacent-position limit-order machinery;
- working limit-order state;
- one-hour-lag limit fill decisions;
- one-hour-lag market-order fill decisions;
- market-order cases required by the book;
- roll/session/overnight interaction policy;
- commissions for all orders;
- market-order spread-cost treatment where required;
- PnL rows tied to fills and held position state.

Current fill scaffolds require actual order and transition authority:

- order plan reference;
- limit-order or market-order hash;
- working-order transition hash;
- next completed hourly fill-row hash;
- fill timestamp identity binding;
- limit fill price equals submitted limit;
- market fill price from next completed close;
- fill quantity and side binding;
- no cost accounting inside fill contract.

## Planning Decision

The current no-order/no-position-change transition should **not** produce an actual `FillLedgerRow`.

Reason:

- there is no limit order row;
- there is no market order row;
- `order_quantity = 0`;
- no order was submitted;
- no working order was opened, carried, canceled, or filled;
- adjacent limit, market fallback, tick rounding, and working-order lifecycle remain fail-closed;
- actual `FillLedgerRow` schema requires positive quantity, order kind, side, fill price, order hashes, transition hash, and fill price provenance.

The minimal next implementation should therefore emit **non-result no-fill metadata only**, or keep actual fill emission fail-closed.

Recommended next surface:

```text
S27_V2_NO_FILL_EXECUTABLE_METADATA_GATE
```

It should consume the externally passed order/transition executable bundle and emit a bundle-only authoritative no-fill metadata row proving:

```text
active_order_transition_bundle_hash = externally passed local active order/transition bundle
order_kind = NO_ORDER
order_quantity = 0
transition_kind = NO_POSITION_CHANGE_NO_ORDER
fill_required = False
fill_rows_emitted = False
filled_order_hash = NOT_APPLICABLE
fill_price = NOT_APPLICABLE
fill_quantity = 0
fill_price_provenance = NOT_APPLICABLE
actual_fill_ledger_emitted = False
```

The no-fill metadata row must not be treated as a fill, cost input, PnL input, result, backtest, or source-faithful evidence.

## Required Guards For No-Fill Metadata

The no-fill metadata gate must:

- rebuild the active order/transition executable bundle from the audited remediation pack;
- exact-compare the supplied order/transition bundle to active authority;
- require active order intent row `NO_ORDER`;
- require active order quantity `0`;
- require active transition kind `NO_POSITION_CHANGE_NO_ORDER`;
- require active transition `fill_rows_emitted = False`;
- require all actual fill fields to be not applicable or zero;
- reject any true cost/PnL/result/source-faithful-evidence flag;
- reject forged order/transition bundles, no-fill rows, hashes, fill-required flags, fill quantity, fill price, fill provenance, filled-order hashes, and downstream flags;
- keep package-root exports unchanged.

## Required Evidence Before Actual Fill Ledger

An actual fill ledger remains blocked until a future source-bound order slice emits an actual limit or market order.

Actual fill ledger implementation will require:

- active order/transition bundle with an emitted limit or market order;
- order hash and order-plan hash;
- working-order transition hash;
- exact next completed hourly fill-row proof;
- fill timestamp identity;
- completed-bar one-hour lag proof;
- branch-specific fill condition:
  - limit fill uses submitted executable limit price;
  - market fill uses next completed close price;
- quantity and side binding to the order;
- session gap/overnight/roll handling where applicable;
- fail-closed behavior for unresolved working-order lifecycle, missing next-hour bar, incompatible timestamp, non-completed bar, missing fill condition, missing price provenance, or missing order hash.

Cost, PnL, result, backtest, and source-faithful evidence claims remain separate later gates.

## Next Authorization Prompt

```text
Operator authorizes S27_V2 local-only no-fill executable metadata gate, after external PASS on the order/transition executable remediation-pack surface and this fill planning gate, limited to emitting deterministic non-result no-fill metadata for the audited ZNM6 remediation pack and externally passed no-order/no-position-change order-transition surface.

This authorizes code/tests/process records/local hostile audits for no-fill metadata only: active order/transition bundle binding, NO_ORDER/order_quantity-zero verification, NO_POSITION_CHANGE_NO_ORDER transition verification, fill_required=False, fill_rows_emitted=False, NOT_APPLICABLE actual-fill fields, fail-closed actual FillLedgerRow emission, and rejection of forged order/transition bundles, no-fill rows, fill-required flags, fill quantities/prices/provenance, and downstream cost/PnL/result/source-faithful evidence flags.

No provider/API, downloads, new data, OOS/Lockbox/Forward, backtests, result-scored runs, actual positive fill emission, cost emission, PnL/result emission, result interpretation, PnL evaluation, tuning, adapter work, deployment, trading, promotion, Git actions, or source-faithful evidence claim.
```

## Boundary

This planning record is not implementation, not a fill ledger, not a cost row, not PnL, not a result interpretation, not promotion evidence, and not a source-faithful evidence claim.

