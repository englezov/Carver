# S27 ZN V2 Full Scaffold-Routing P1 Runtime And Cost-Policy Authority Patch Record

Date: 2026-06-08

Status:

```text
PROCESS_ONLY_S27_ZN_V2_FULL_SCAFFOLD_ROUTING_P1_RUNTIME_COST_POLICY_AUTHORITY_PATCH_NOT_REPLAY_AUTHORIZATION
```

## Authorization

The operator requested a consolidated fix for the GPT Extended Pro external audit failure. The patch remains inside the previously authorized inert scaffold-routing remediation scope.

## Scope

Patched files:

```text
src/carver/spine/s27_v2_replay/runtime_history_input_contract.py
src/carver/spine/s27_v2_replay/forecast_input_contract.py
src/carver/spine/s27_v2_replay/position_input_contract.py
src/carver/spine/s27_v2_replay/order_input_contract.py
src/carver/spine/s27_v2_replay/fill_input_contract.py
src/carver/spine/s27_v2_replay/cost_input_contract.py
src/carver/spine/s27_v2_replay/cost_contract.py
src/carver/spine/s27_v2_replay/pnl_input_contract.py
src/carver/spine/s27_v2_replay/validation_input_contract.py
src/carver/spine/s27_v2_replay/trusted_bundle_contract.py
```

## P1-001 Remediation

`RuntimeHistoryInputContractBundle.validate_against_active_trust_authority(...)` now requires:

```text
LevelCompatibilityInputContractBundle
LevelCompatibilityContractBundle
```

Runtime-history validation now:

- validates level-compatibility input through active trust/evidence/source-row-batch/parser-output authority;
- validates the level-compatibility contract bundle;
- binds runtime's cited `level_compatibility_input_contract_hash` and `level_compatibility_contract_hash` to those validated objects;
- binds level-compatibility source manifest and source universe to the routed authority chain;
- checks each `RuntimeHistoryLevelCompatibilityInputBindingContract.level_compatibility_input_field_contract_hash` against the validated level-compatibility input-field hash for the locked level-compatibility input label.

The two level-compatibility authority objects are now routed downstream through forecast, position, order, fill, cost, PnL, validation, and trusted-bundle scaffold validators.

## P1-002 Remediation

`CostInputContractBundle.validate_against_fill_authority(...)` now calls `require_evidence_manifest_matches_trust_root(...)` before accepting cost expected-source maps.

Cost input active authority now derives:

- fill ledger inputs from the validated fill contract bundle;
- commission policy input from `ReplayTrustRoot.commission_policy_hash`;
- spread policy and spread-space inputs from `ReplayTrustRoot.spread_unit_policy_hash`;
- multiplier and currency proof inputs from `ReplayTrustRoot.contract_multiplier_currency_policy_hash`;
- cost branch, deflation, and local calculation policy inputs from the scaffold-local `cost_input_policy_hash`.

`CostContractBundle` now has `validate_against_policy_authority(...)`, which validates the trust-root/evidence-manifest match and requires commission, spread, multiplier, and currency policy fields to match the routed trust root.

`PnlInputContractBundle.validate_against_cost_authority(...)` now validates `CostContractBundle` through `validate_against_policy_authority(...)`, and PnL multiplier/currency active authority is derived from `ReplayTrustRoot.contract_multiplier_currency_policy_hash` rather than cost-contract-local hashes.

## Guardrail

This patch is inert scaffold routing only. It introduces no parser/file replay execution, diagnostics, tests/backtests, provider/API calls, downloads, OOS, Lockbox, Forward, Git actions, adapter work, deployment, trading, promotion, result interpretation, or source-faithful replay evidence claim.

## Next Required Check

Run a local hostile audit under the consolidated scaffold-routing loop focused on the two GPT P1 findings:

- P1-001 runtime-history level-compatibility authority routing;
- P1-002 cost policy, multiplier, and currency active trust/evidence authority routing.
