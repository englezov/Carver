# S27_V2 PnL Evidence / PnL Executable Planning Gate

Date: 2026-06-09

Status:

```text
PROCESS_ONLY_PNL_PLANNING_AFTER_NO_COST_EXTERNAL_PASS
```

## Authorization

Operator authorized a local-only PnL-evidence/PnL-executable planning gate after external PASS on the no-cost executable metadata surface.

Authorized scope:

- inspect current `S27_V2` code/tests/process records and source-lock artifacts;
- record the no-cost external PASS synthesis;
- identify whether the no-order/no-fill/no-cost transition should produce explicit no-PnL metadata or remain fail-closed;
- define required evidence for any future actual PnL ledger;
- propose the next exact implementation authorization.

Non-authorized scope:

- no provider/API access;
- no downloads or new data;
- no OOS/Lockbox/Forward;
- no backtests or result-scored runs;
- no actual fill emission;
- no actual cost emission;
- no PnL emission unless separately authorized after this planning gate;
- no result emission;
- no result interpretation or PnL evaluation;
- no tuning;
- no adapter work, deployment, trading, promotion;
- no Git actions;
- no source-faithful evidence claim.

## External PASS Context

The no-cost executable metadata surface externally passed:

```text
docs/process/CARVER_S27_ZN_V2_NO_COST_EXECUTABLE_EXTERNAL_AUDIT_SYNTHESIS_2026-06-09.md
```

External audit confirmed:

- active no-fill bundle binding;
- `NO_ORDER` and order quantity `0`;
- `NO_POSITION_CHANGE_NO_ORDER`;
- `fill_required = False`;
- fail-closed actual fill ledger binding;
- no-cost metadata only;
- fail-closed actual commission, spread-cost, and cost ledger emission;
- zero commission, spread, spread-cost, and total-cost metadata;
- standalone no-cost row non-authority;
- forged no-fill/no-cost/downstream flag rejection;
- no package-root export leak;
- no provider/API, download, backtest, Git, PnL, result, or source-faithful evidence surface.

## Current Upstream State

The active upstream path is:

```text
order_kind = NO_ORDER
order_quantity = 0
transition_kind = NO_POSITION_CHANGE_NO_ORDER
fill_required = False
actual_fill_ledger_emitted = False
cost_required = False
cost_rows_emitted = False
actual_commission_ledger_emitted = False
actual_spread_cost_ledger_emitted = False
actual_cost_ledger_emitted = False
commission_amount = 0.0
spread_amount = 0.0
spread_cost_amount = 0.0
total_cost_amount = 0.0
total_cost_currency = NOT_APPLICABLE
cost_provenance = NO_ORDER_NO_FILL_NO_COST
```

Therefore this gate has no actual fill, no actual cost, and no position-change event to evaluate as an actual PnL event.

## PnL Source Requirements

The source lock says true S27/S26 execution ultimately requires:

- explicit execution ledgers;
- fill ledgers;
- commission and spread-cost ledgers;
- PnL rows tied to fills and held position state;
- no target-position close-to-close shortcut PnL.

Current `PnlLedgerRow` requires:

- replay identity;
- replay trust-root hash;
- source-universe hash;
- previous-step or initial-state hash;
- starting and ending working-state hashes;
- starting and ending position;
- transition hash;
- position source hash;
- PnL formula policy hash;
- close-only start/end price source row hashes;
- raw-symbol continuity or roll-bridge proof;
- contract multiplier value and source hashes;
- currency policy or conversion proof as applicable;
- cost application policy hash;
- fill hash-set hash;
- cost hash-set hash;
- PnL hash.

Current `PnlInputContractBundle.validate()` fails closed without cost and upstream replay authority.

Because the active no-cost path has no actual fill/cost hash sets and no actual PnL event, an actual `PnlLedgerRow` is not admissible for this remediation pack state.

## Planning Decision

The current no-order/no-fill/no-cost transition should **not** produce an actual `PnlLedgerRow`.

Reason:

- there is no limit order;
- there is no market order;
- there is no actual fill;
- there is no actual commission/spread/cost event;
- active order quantity is zero;
- active transition is `NO_POSITION_CHANGE_NO_ORDER`;
- actual fill and actual cost ledger emission remain fail-closed;
- current `PnlLedgerRow` is a real ledger tied to transition, price, fill, cost, and position state;
- emitting an actual PnL row on this zero-action metadata branch risks creating result-like evidence before the backtest/result gates.

The minimal next implementation should therefore emit **non-result no-PnL metadata only**, or keep actual PnL emission fail-closed.

Recommended next surface:

```text
S27_V2_NO_PNL_EXECUTABLE_METADATA_GATE
```

It should consume the externally passed no-cost executable metadata bundle and emit a bundle-only authoritative no-PnL metadata row proving:

```text
active_no_cost_bundle_hash = externally passed local active no-cost bundle
pnl_required = False
pnl_rows_emitted = False
actual_pnl_ledger_emitted = False
actual_result_row_emitted = False
actual_backtest_result_emitted = False
pnl_amount = NOT_APPLICABLE
pnl_currency = NOT_APPLICABLE
pnl_provenance = NO_ORDER_NO_FILL_NO_COST_NO_PNL
actual_pnl_ledger_status = FAIL_CLOSED_ACTUAL_PNL_LEDGER_NOT_EMITTED
result_interpretation_emitted = False
source_faithful_evidence_claimed = False
```

The no-PnL metadata row must not be treated as a `PnlLedgerRow`, result row, backtest row, result interpretation, promotion evidence, or source-faithful evidence claim.

## Required Guards For No-PnL Metadata

The no-PnL metadata gate must:

- rebuild the active no-cost executable bundle from the audited remediation pack;
- exact-compare the supplied no-cost bundle to active authority;
- require active no-cost metadata to bind `NO_ORDER`;
- require active order quantity `0`;
- require active transition `NO_POSITION_CHANGE_NO_ORDER`;
- require `fill_required = False`;
- require `actual_fill_ledger_emitted = False`;
- require `cost_required = False`;
- require `cost_rows_emitted = False`;
- require `actual_cost_ledger_emitted = False`;
- require all active cost amounts to be zero;
- require `pnl_required = False`;
- require `pnl_rows_emitted = False`;
- require actual PnL, result, and backtest result emission to be false;
- require PnL amount and currency to be `NOT_APPLICABLE`;
- reject any nonzero PnL amount, PnL currency, price-row proof, multiplier proof, cost/fill hash set, or formula policy pretending to be actual PnL evidence;
- reject any true result, result-interpretation, source-faithful-evidence, promotion, backtest, OOS, Lockbox, Forward, provider/API, download, adapter, deployment, trading, tuning, or Git flag;
- reject forged no-cost bundles, no-PnL rows, hashes, PnL-required flags, PnL amounts, PnL provenance, and downstream flags;
- keep package-root exports unchanged.

## Required Evidence Before Actual PnL Ledger

An actual PnL ledger remains blocked until a future source-bound path emits actual execution/fill/cost and position-state evidence.

Actual PnL ledger implementation will require:

- active actual transition with position state;
- previous-step or initial-state hash;
- starting and ending working-order state hashes;
- starting and ending position;
- active position source hash;
- active actual fill hash-set;
- active actual cost hash-set;
- close-only start and end price row hashes;
- raw-symbol continuity proof or roll-bridge proof;
- ZN contract multiplier value and source proof;
- currency policy and conversion proof as applicable;
- PnL formula policy;
- cost application policy;
- explicit no-target-position-shortcut proof;
- no result interpretation inside PnL rows;
- fail-closed behavior for missing price rows, incompatible roll bridge, missing multiplier/currency evidence, missing fill/cost authority, missing transition state, or any target-position shortcut.

Result rows, backtests, result interpretation, promotion, and source-faithful evidence claims remain separate later gates.

## Next Authorization Prompt

```text
Operator authorizes S27_V2 local-only no-PnL executable metadata gate, after external PASS on the no-cost executable metadata surface and this PnL planning gate, limited to emitting deterministic non-result no-PnL metadata for the audited ZNM6 remediation pack and externally passed no-order/no-fill/no-cost surface.

This authorizes code/tests/process records/local hostile audits for no-PnL metadata only: active no-cost bundle binding, NO_ORDER/order_quantity-zero verification, NO_POSITION_CHANGE_NO_ORDER verification, fill_required=False, actual_fill_ledger_emitted=False, cost_required=False, actual_cost_ledger_emitted=False, pnl_required=False, pnl_rows_emitted=False, actual PnL/result/backtest emission fail-closed, NOT_APPLICABLE PnL amount/currency metadata, and rejection of forged no-cost bundles, no-PnL rows, PnL-required flags, PnL amounts/currency/provenance, and downstream result/source-faithful evidence flags.

No provider/API, downloads, new data, OOS/Lockbox/Forward, backtests, result-scored runs, actual positive fill emission, actual commission/spread/cost ledger emission, actual PnL ledger emission, result emission, result interpretation, PnL evaluation, tuning, adapter work, deployment, trading, promotion, Git actions, or source-faithful evidence claim.
```

## Boundary

This planning record is not implementation, not a PnL ledger, not a result row, not a backtest, not result interpretation, not promotion evidence, and not a source-faithful evidence claim.
