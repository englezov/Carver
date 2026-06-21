# S27_V2 Order-Input Position Authority Routing Scaffold Record

Date: 2026-06-07

Status:

```text
PROCESS_ONLY_S27_V2_ORDER_INPUT_POSITION_AUTHORITY_ROUTING_SCAFFOLD_NOT_REPLAY_AUTHORIZATION
```

## Authorization

The operator authorized a consolidated S27_V2 parser/file replay scaffold-routing loop, limited to inert authority-routing and contract-binding scaffolds after active-trust routing external `PASS`.

This record covers only the order-input/position authority-routing slice inside that consolidated gate.

## Scope

Patched file:

```text
src/carver/spine/s27_v2_replay/order_input_contract.py
```

Upstream authority dependencies:

```text
src/carver/spine/s27_v2_replay/position_input_contract.py
src/carver/spine/s27_v2_replay/position_contract.py
src/carver/spine/s27_v2_replay/forecast_input_contract.py
src/carver/spine/s27_v2_replay/forecast_contract.py
```

## Change Summary

`OrderInputContractBundle.validate()` now fails closed. Order input validation requires the routed `validate_against_position_authority(...)` path.

That routed path validates `PositionInputContractBundle` through its forecast/runtime-history authority route before consuming position authority, and separately validates `PositionContractBundle`.

Order input expected-source authority is now derived as follows:

- position component inputs derive from locked `PositionComponentContract.component_contract_hash` values;
- desired-position ledger output input binds to the validated `PositionContractBundle.desired_position_contract_bundle_hash`;
- order-kind, transition-kind, working-order state context, and local policy inputs remain bound to the order input policy hash.

The patch binds the cited position input contract hash, position contract bundle hash, source-input manifest contract hash, and position/forecast authority relationship before order input source maps can be accepted.

## Ledger-Output Note

This scaffold does not yet define a separate desired-position ledger-row output authority object. Until that future object exists under a separate authorized scaffold, the single desired-position ledger-output input is bound to the validated position contract bundle rather than to caller-supplied or self-derived expected maps.

## Guardrail

This scaffold remains inert. It introduces no order generation, limit pricing, tick rounding execution, working-order state advancement, fill execution, parser/file replay execution path, diagnostics, tests/backtests, OOS, Lockbox, Forward, provider/API calls, downloads, Git actions, adapter work, deployment, trading, promotion, result interpretation, or source-faithful replay evidence claim.

## Next Required Check

Run a local hostile audit under the consolidated scaffold-routing loop to verify:

- order input no longer self-authenticates position authority with coarse top-level position hashes;
- position input is validated through the forecast/runtime-history authority route before order consumes position input/contract authority;
- position component authority is derived from validated position component contracts;
- desired-position ledger output is at least bound to the validated position contract bundle and not a caller-supplied expected map;
- no execution surface or forbidden stage transition was introduced.
