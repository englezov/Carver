# S27_V2 PnL-Input Cost And Upstream Authority Routing Scaffold Record

Date: 2026-06-07

Status:

```text
PROCESS_ONLY_S27_V2_PNL_INPUT_COST_UPSTREAM_AUTHORITY_ROUTING_SCAFFOLD_NOT_REPLAY_AUTHORIZATION
```

## Authorization

The operator authorized a consolidated S27_V2 parser/file replay scaffold-routing loop, limited to inert authority-routing and contract-binding scaffolds after active-trust routing external `PASS`.

This record covers only the PnL-input/cost and upstream authority-routing slice inside that consolidated gate.

## Scope

Patched file:

```text
src/carver/spine/s27_v2_replay/pnl_input_contract.py
```

Upstream authority dependencies:

```text
src/carver/spine/s27_v2_replay/cost_input_contract.py
src/carver/spine/s27_v2_replay/cost_contract.py
src/carver/spine/s27_v2_replay/fill_input_contract.py
src/carver/spine/s27_v2_replay/fill_contract.py
src/carver/spine/s27_v2_replay/order_contract.py
src/carver/spine/s27_v2_replay/position_contract.py
src/carver/spine/s27_v2_replay/source_input_manifest_contract.py
```

## Change Summary

`PnlInputContractBundle.validate()` now fails closed. PnL input validation requires the routed `validate_against_cost_authority(...)` path.

That routed path validates `CostInputContractBundle` through its fill/order/source-row authority route before consuming cost authority, and separately validates `CostContractBundle`.

PnL input expected-source authority is now derived as follows:

- trust-root input binds to the routed `ReplayTrustRoot.replay_trust_root_hash`;
- source-universe input binds to the routed `SourceRowSelectionExternalAuthorityHandle.source_universe_contract_bundle_hash`;
- transition and working-state inputs bind to the validated order contract bundle;
- position-source input binds to the validated position contract bundle;
- start/end price-row proof inputs bind to the validated source-input manifest selected-row hash for `DAILY_CURRENT_CONTRACT_ROW_HASH`;
- raw-symbol continuity and roll-bridge inputs bind to the validated source-input manifest hash;
- contract multiplier and currency inputs bind to validated cost contract policy hashes;
- fill and cost hash-set inputs bind to the validated fill and cost contract bundle hashes;
- local PnL formula/cost-application/quarantine policy inputs bind to the PnL input policy hash.

The patch also compares the PnL input bundle's explicit top-level authority fields to those routed active authority values before expected-source maps or field contracts can be accepted.

## Row-Output Boundary Notes

This scaffold does not yet define separate transition-ledger-row, price-row proof, raw-symbol continuity proof, roll-bridge proof, fill-row hash-set, or cost-row hash-set authority objects.

Until those future objects exist under separate authorized scaffolds, these PnL inputs are bound to their nearest validated upstream authority object rather than to caller-supplied or self-derived expected maps. This is an inert routing scaffold only and is not source-faithful replay evidence.

## Guardrail

This scaffold remains inert. It introduces no price selection, no transition replay, no PnL computation, no ledger construction, no result interpretation, no parser/file replay execution path, diagnostics, tests/backtests, OOS, Lockbox, Forward, provider/API calls, downloads, Git actions, adapter work, deployment, trading, promotion, or source-faithful replay evidence claim.

## Next Required Check

Run a local hostile audit under the consolidated scaffold-routing loop to verify:

- PnL input no longer accepts its broad authority map solely from caller-supplied/self fields;
- cost input is validated through the fill/order/source-row authority route before PnL consumes cost/fill authority;
- routed trust-root, source-universe, position, order, source-input, fill, and cost authority values are used before PnL expected-source maps are accepted;
- row-output boundary notes are accurate and do not claim source-faithful replay evidence;
- no execution surface or forbidden stage transition was introduced.
