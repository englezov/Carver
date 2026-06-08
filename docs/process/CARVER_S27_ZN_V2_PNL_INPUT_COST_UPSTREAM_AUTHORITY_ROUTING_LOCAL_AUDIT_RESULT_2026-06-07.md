# S27_V2 PnL-Input Cost And Upstream Authority Routing Local Audit Result

Date: 2026-06-07

Status:

```text
PROCESS_ONLY_S27_V2_PNL_INPUT_COST_UPSTREAM_AUTHORITY_ROUTING_LOCAL_AUDIT_PASS_NOT_REPLAY_AUTHORIZATION
```

## Scope

Local hostile audit of the PnL-input/cost and upstream authority-routing scaffold under the consolidated S27_V2 parser/file replay scaffold-routing loop.

Audited files:

```text
src/carver/spine/s27_v2_replay/pnl_input_contract.py
src/carver/spine/s27_v2_replay/cost_input_contract.py
src/carver/spine/s27_v2_replay/cost_contract.py
src/carver/spine/s27_v2_replay/fill_input_contract.py
src/carver/spine/s27_v2_replay/source_input_manifest_contract.py
src/carver/spine/s27_v2_replay/trust_root.py
docs/process/CARVER_S27_ZN_V2_PNL_INPUT_COST_UPSTREAM_AUTHORITY_ROUTING_SCAFFOLD_RECORD_2026-06-07.md
```

## Verdict

```text
PASS
```

Findings:

```text
P0: none
P1: none
P2: none
P3: one downstream validation-routing note
```

## Audit Conclusions

The audit found that no-argument `PnlInputContractBundle.validate()` fails closed and that `validate_against_cost_authority(...)` is the routed authority path.

The audit found that routed PnL validation validates `CostInputContractBundle` through fill/order/source-row authority and validates `CostContractBundle` before consuming cost/fill authority.

The audit found that PnL active authority is derived from routed trust-root, source-universe handle, order, position, source-input manifest, fill, and cost values, and that top-level PnL authority fields are compared against those routed values before field contracts are accepted.

The audit accepted the transition, price-row, bridge, fill-hash-set, and cost-hash-set boundaries as nearest-validated-upstream scaffold bindings because the process record explicitly avoids source-faithful replay evidence claims.

The audit found no stale PnL-input authority bypass and no forbidden execution surface or stage transition.

## P3 Downstream Note

`ValidationInputContractBundle` still treats `pnl_input_contract_hash` as a local validation-input field and derives its expected map from self-fields rather than from a routed `PnlInputContractBundle` object. This is downstream of the audited PnL-input/cost routing patch and should be addressed in validation/trusted-output routing.

## Non-Authorization

This local audit result does not authorize price selection, transition replay, PnL computation, ledger construction, result interpretation, parser/file replay execution, provider/API access, downloads, diagnostics, tests/backtests, OOS, Lockbox, Forward, Git actions, adapter work, deployment, trading, promotion, or source-faithful replay evidence claims.

Validation/trusted-output scaffold-routing may proceed only within the existing consolidated inert scaffold-routing authorization.
