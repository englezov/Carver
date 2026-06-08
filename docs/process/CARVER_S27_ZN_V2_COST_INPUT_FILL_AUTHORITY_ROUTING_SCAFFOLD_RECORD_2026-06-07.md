# S27_V2 Cost-Input Fill Authority Routing Scaffold Record

Date: 2026-06-07

Status:

```text
PROCESS_ONLY_S27_V2_COST_INPUT_FILL_AUTHORITY_ROUTING_SCAFFOLD_NOT_REPLAY_AUTHORIZATION
```

## Authorization

The operator authorized a consolidated S27_V2 parser/file replay scaffold-routing loop, limited to inert authority-routing and contract-binding scaffolds after active-trust routing external `PASS`.

This record covers only the cost-input/fill authority-routing slice inside that consolidated gate.

## Scope

Patched file:

```text
src/carver/spine/s27_v2_replay/cost_input_contract.py
```

Upstream authority dependencies:

```text
src/carver/spine/s27_v2_replay/fill_input_contract.py
src/carver/spine/s27_v2_replay/fill_contract.py
src/carver/spine/s27_v2_replay/order_input_contract.py
src/carver/spine/s27_v2_replay/order_contract.py
src/carver/spine/s27_v2_replay/source_input_manifest_contract.py
```

## Change Summary

`CostInputContractBundle.validate()` now fails closed. Cost input validation requires the routed `validate_against_fill_authority(...)` path.

That routed path validates `FillInputContractBundle` through its order/source-row authority route before consuming fill authority, and separately validates `FillContractBundle`.

Cost input expected-source authority is now derived as follows:

- fill ledger output inputs bind to the validated `FillContractBundle.fill_contract_bundle_hash`;
- cost branch, spread-space, multiplier proof, currency proof, and local policy inputs bind to the cost input policy hash.

The patch binds the cited source-input manifest contract hash, fill input contract hash, fill contract bundle hash, fill/source-input manifest relationship, fill/order relationship, and fill source manifest hash before cost input source maps can be accepted.

## Ledger-Output Note

This scaffold does not yet define separate fill ledger-row output authority objects. Until those future objects exist under a separate authorized scaffold, fill ledger-output inputs are bound to the validated fill contract bundle rather than to caller-supplied or self-derived expected maps.

## Guardrail

This scaffold remains inert. It introduces no commission computation, spread computation, cost ledger construction, PnL accounting, parser/file replay execution path, diagnostics, tests/backtests, OOS, Lockbox, Forward, provider/API calls, downloads, Git actions, adapter work, deployment, trading, promotion, result interpretation, or source-faithful replay evidence claim.

## Next Required Check

Run a local hostile audit under the consolidated scaffold-routing loop to verify:

- cost input no longer self-authenticates fill authority with coarse fill input hashes;
- fill input is validated through the order/source-row authority route before cost consumes fill input/contract authority;
- fill ledger outputs are at least bound to the validated fill contract bundle and not caller-supplied expected maps;
- cost branch/spread-space/local policy inputs are not incorrectly bound to fill authority;
- no execution surface or forbidden stage transition was introduced.
