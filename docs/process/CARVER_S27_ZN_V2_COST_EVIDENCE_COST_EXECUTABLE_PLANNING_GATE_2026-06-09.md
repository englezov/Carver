# S27_V2 Cost Evidence / Cost Executable Planning Gate

Date: 2026-06-09

Status:

```text
PROCESS_ONLY_COST_PLANNING_AFTER_NO_FILL_EXTERNAL_PASS
```

## Authorization

Operator authorized a local-only cost-evidence/cost-executable planning gate after external PASS on the no-fill executable metadata surface.

Authorized scope:

- inspect current `S27_V2` code/tests/process records and source-lock artifacts;
- record the no-fill external PASS synthesis;
- identify whether the no-order/no-fill transition should produce explicit no-cost metadata or remain fail-closed;
- define required evidence for any future actual commission/spread cost ledger;
- propose the next exact implementation authorization.

Non-authorized scope:

- no provider/API access;
- no downloads or new data;
- no OOS/Lockbox/Forward;
- no backtests or result-scored runs;
- no actual fill emission;
- no cost emission unless separately authorized after this planning gate;
- no PnL/result emission;
- no result interpretation or PnL evaluation;
- no tuning;
- no adapter work, deployment, trading, promotion;
- no Git actions;
- no source-faithful evidence claim.

## External PASS Context

The no-fill executable metadata surface externally passed:

```text
docs/process/CARVER_S27_ZN_V2_NO_FILL_EXECUTABLE_EXTERNAL_AUDIT_SYNTHESIS_2026-06-09.md
```

External audit confirmed:

- active order/transition bundle binding;
- `NO_ORDER` and order quantity `0`;
- `NO_POSITION_CHANGE_NO_ORDER`;
- no-fill metadata only;
- `NOT_APPLICABLE` actual-fill fields;
- fail-closed actual `FillLedgerRow` emission;
- standalone no-fill row non-authority;
- forged order/transition/no-fill/downstream flag rejection;
- no package-root export leak;
- no provider/API, download, new data, OOS/Lockbox/Forward, backtest, result-scored run, cost, PnL/result, tuning, adapter/deployment/trading/promotion, Git, or source-faithful evidence surface.

## Current Upstream State

The active upstream path is:

```text
order_kind = NO_ORDER
order_quantity = 0
transition_kind = NO_POSITION_CHANGE_NO_ORDER
fill_required = False
fill_rows_emitted = False
actual_fill_ledger_emitted = False
actual_fill_ledger_status = FAIL_CLOSED_ACTUAL_FILL_LEDGER_NOT_EMITTED
filled_order_hash = NOT_APPLICABLE
fill_price = NOT_APPLICABLE
fill_quantity = 0
fill_price_provenance = NOT_APPLICABLE
```

Therefore this gate has no actual order and no actual fill to cost.

## Cost Source Requirements

The source lock says true S27/S26 execution ultimately requires:

- commissions for all orders;
- market-order spread costs where market orders are required;
- limit-order fills as commission-only;
- market-order fills as commission plus normal bid-ask spread;
- PnL rows tied to fills and held position state.

Project-wide cost policy:

- use book/source costs first;
- if the book does not specify enough costs, infer a plausible source-native retail futures cost model from capital size, instrument, contract type, and realistic retail broker fee schedules;
- label inferred costs as inferred assumptions;
- do not use prop-firm fees, evaluation fees, payout rules, CFD broker spreads, swaps, adapter-specific costs, or personal trading costs as source-faithful strategy costs.

## Existing Cost Scaffold Boundary

Current `CostLedgerRow` is tied to an actual `FillLedgerRow`.

The actual cost row schema requires:

- `FillLedgerRow.validate()`;
- positive fill quantity;
- positive commission per contract;
- positive commission amount;
- cost calculation policy hash;
- branch-specific treatment:
  - limit fill: commission-only, zero spread, no spread-policy/unit/space;
  - market fill: positive spread and positive spread cost;
- total cost amount equal to commission amount plus spread cost.

Current `CostInputContractBundle.validate()` also fails closed without fill authority.

Because the active no-fill path has no actual `FillLedgerRow`, an actual `CostLedgerRow` is not admissible for this remediation pack state.

## Planning Decision

The current no-order/no-fill transition should **not** produce an actual `CostLedgerRow`.

Reason:

- there is no limit order;
- there is no market order;
- there is no actual fill;
- `fill_quantity = 0`;
- actual fill ledger emission remains fail-closed;
- current `CostLedgerRow` requires a valid positive-quantity `FillLedgerRow`;
- true commission/spread cost rows are source-relevant only after an actual order/fill branch exists.

The minimal next implementation should therefore emit **non-result no-cost metadata only**, or keep actual cost emission fail-closed.

Recommended next surface:

```text
S27_V2_NO_COST_EXECUTABLE_METADATA_GATE
```

It should consume the externally passed no-fill executable metadata bundle and emit a bundle-only authoritative no-cost metadata row proving:

```text
active_no_fill_bundle_hash = externally passed local active no-fill bundle
cost_required = False
cost_rows_emitted = False
actual_cost_ledger_emitted = False
actual_commission_ledger_emitted = False
actual_spread_cost_ledger_emitted = False
commission_amount = 0
spread_amount = 0
spread_cost_amount = 0
total_cost_amount = 0
total_cost_currency = NOT_APPLICABLE
cost_reason = NO_ORDER_NO_FILL_NO_COST
actual_cost_ledger_status = FAIL_CLOSED_ACTUAL_COST_LEDGER_NOT_EMITTED
```

The no-cost metadata row must not be treated as a commission ledger, spread-cost ledger, cost input, PnL input, result, backtest, or source-faithful evidence.

## Required Guards For No-Cost Metadata

The no-cost metadata gate must:

- rebuild the active no-fill executable bundle from the audited remediation pack;
- exact-compare the supplied no-fill bundle to active authority;
- require active no-fill metadata to bind `NO_ORDER`;
- require active order quantity `0`;
- require active transition `NO_POSITION_CHANGE_NO_ORDER`;
- require `fill_required = False`;
- require `fill_rows_emitted = False`;
- require `actual_fill_ledger_emitted = False`;
- require all cost amounts to be zero;
- require actual commission, spread-cost, and cost ledger emission to be false;
- reject any positive commission, positive spread, positive spread cost, total cost, cost currency, cost policy, filled-order hash, or fill hash pretending to be actual cost evidence;
- reject any true PnL/result/source-faithful-evidence flag;
- reject forged no-fill bundles, no-cost rows, hashes, cost-required flags, cost amounts, cost provenance, and downstream flags;
- keep package-root exports unchanged.

## Required Evidence Before Actual Cost Ledger

An actual cost ledger remains blocked until a future source-bound fill slice emits an actual limit or market fill.

Actual cost ledger implementation will require:

- active actual `FillLedgerRow` with positive fill quantity;
- filled order hash and order kind;
- branch evidence for limit fill versus market fill;
- book/source commission policy, or explicitly labeled inferred source-native retail futures commission assumption if the book is insufficient;
- market spread policy and spread unit for market fills;
- ZN multiplier/currency evidence for price-space spread cost if spread is price-space;
- USD currency conversion evidence or explicit `USD/USD = 1.0` policy;
- total cost arithmetic proof:
  - commission amount equals per-contract commission times fill quantity;
  - limit fill spread amount and spread cost are zero;
  - market fill spread cost is positive and bound to spread policy;
  - total cost equals commission amount plus spread cost;
- no PnL accounting inside cost rows;
- fail-closed behavior for unresolved commission, spread, multiplier, currency, deflation, fill authority, branch, or arithmetic evidence.

PnL, result, backtest, and source-faithful evidence claims remain separate later gates.

## Next Authorization Prompt

```text
Operator authorizes S27_V2 local-only no-cost executable metadata gate, after external PASS on the no-fill executable metadata surface and this cost planning gate, limited to emitting deterministic non-result no-cost metadata for the audited ZNM6 remediation pack and externally passed no-order/no-fill surface.

This authorizes code/tests/process records/local hostile audits for no-cost metadata only: active no-fill bundle binding, NO_ORDER/order_quantity-zero verification, NO_POSITION_CHANGE_NO_ORDER verification, fill_required=False, actual_fill_ledger_emitted=False, cost_required=False, cost_rows_emitted=False, actual commission/spread/cost ledger emission fail-closed, zero commission/spread/total-cost metadata, and rejection of forged no-fill bundles, no-cost rows, cost-required flags, positive cost amounts, cost provenance, and downstream PnL/result/source-faithful evidence flags.

No provider/API, downloads, new data, OOS/Lockbox/Forward, backtests, result-scored runs, actual positive fill emission, actual commission/spread/cost ledger emission, PnL/result emission, result interpretation, PnL evaluation, tuning, adapter work, deployment, trading, promotion, Git actions, or source-faithful evidence claim.
```

## Boundary

This planning record is not implementation, not a commission ledger, not a spread-cost ledger, not a cost row, not PnL, not a result interpretation, not promotion evidence, and not a source-faithful evidence claim.
