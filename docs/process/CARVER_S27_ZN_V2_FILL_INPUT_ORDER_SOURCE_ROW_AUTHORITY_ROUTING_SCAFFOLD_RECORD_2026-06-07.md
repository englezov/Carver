# S27_V2 Fill-Input Order And Source-Row Authority Routing Scaffold Record

Date: 2026-06-07

Status:

```text
PROCESS_ONLY_S27_V2_FILL_INPUT_ORDER_SOURCE_ROW_AUTHORITY_ROUTING_SCAFFOLD_NOT_REPLAY_AUTHORIZATION
```

## Authorization

The operator authorized a consolidated S27_V2 parser/file replay scaffold-routing loop, limited to inert authority-routing and contract-binding scaffolds after active-trust routing external `PASS`.

This record covers only the fill-input/order and source-row authority-routing slice inside that consolidated gate.

## Scope

Patched file:

```text
src/carver/spine/s27_v2_replay/fill_input_contract.py
```

Upstream authority dependencies:

```text
src/carver/spine/s27_v2_replay/order_input_contract.py
src/carver/spine/s27_v2_replay/order_contract.py
src/carver/spine/s27_v2_replay/source_input_manifest_contract.py
src/carver/spine/s27_v2_replay/position_input_contract.py
src/carver/spine/s27_v2_replay/position_contract.py
```

## Change Summary

`FillInputContractBundle.validate()` now fails closed. Fill input validation requires the routed `validate_against_order_authority(...)` path.

That routed path validates `SourceInputManifestContractBundle` through active trust, validates `OrderInputContractBundle` through its position/forecast/runtime-history authority route, and separately validates `OrderContractBundle`.

Fill input expected-source authority is now derived as follows:

- order ledger and working-order transition inputs bind to the validated `OrderContractBundle.order_contract_bundle_hash`;
- the exact next-completed hourly fill-row proof input binds to the validated source-input manifest selected-row hash for `HOURLY_FILL_ROW_HASH`;
- fill price provenance, fill branch, and local policy inputs remain bound to the fill input policy hash.

The patch binds the cited source-input manifest contract hash, order input contract hash, order contract bundle hash, order/source-input manifest relationship, order/position relationship, and order source manifest hash before fill input source maps can be accepted.

## Ledger-Output Note

This scaffold does not yet define separate order ledger-row or working-order transition-row output authority objects. Until those future objects exist under a separate authorized scaffold, those fill inputs are bound to the validated order contract bundle rather than to caller-supplied or self-derived expected maps.

## Guardrail

This scaffold remains inert. It introduces no fill selection, no next-row lookup, no fill price computation, no cost accounting, no parser/file replay execution path, diagnostics, tests/backtests, OOS, Lockbox, Forward, provider/API calls, downloads, Git actions, adapter work, deployment, trading, promotion, result interpretation, or source-faithful replay evidence claim.

## Next Required Check

Run a local hostile audit under the consolidated scaffold-routing loop to verify:

- fill input no longer self-authenticates order authority with coarse top-level order hashes;
- order input is validated through the position/forecast/runtime-history authority route before fill consumes order input/contract authority;
- source-row proof derives from validated source-input manifest selected-row authority for `HOURLY_FILL_ROW_HASH`;
- order ledger and transition outputs are at least bound to the validated order contract bundle and not caller-supplied expected maps;
- no execution surface or forbidden stage transition was introduced.
