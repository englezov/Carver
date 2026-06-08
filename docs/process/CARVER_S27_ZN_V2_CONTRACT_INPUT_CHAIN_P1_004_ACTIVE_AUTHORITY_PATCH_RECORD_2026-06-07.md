# S27 ZN V2 Contract/Input Chain P1-004 Active Authority Patch Record

Date: 2026-06-07

Status:

```text
PROCESS_ONLY_S27_ZN_V2_CONTRACT_INPUT_CHAIN_P1_004_ACTIVE_AUTHORITY_PATCH_RECORD_NOT_EXECUTION_AUTHORIZATION
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Trigger

GPT Extended Pro external hostile re-audit returned `FAIL` because `P1-004` remained partially open. The prior patch made field-level source hashes equal expected maps, but the maps themselves were still caller-supplied and not anchored to active upstream authority.

## Patched Scope

### Shared Validation

Patched:

```text
src/carver/spine/s27_v2_replay/validation.py
```

Change:

```text
require_hash_map_matches_active_authority()
```

This helper validates both observed and active authority maps against the locked label tuple, then requires exact map equality and raises `CarverBlocked` on mismatch.

### Downstream Input Bundles

Patched:

```text
src/carver/spine/s27_v2_replay/level_compatibility_input_contract.py
src/carver/spine/s27_v2_replay/runtime_history_input_contract.py
src/carver/spine/s27_v2_replay/forecast_input_contract.py
src/carver/spine/s27_v2_replay/position_input_contract.py
src/carver/spine/s27_v2_replay/order_input_contract.py
src/carver/spine/s27_v2_replay/fill_input_contract.py
src/carver/spine/s27_v2_replay/cost_input_contract.py
src/carver/spine/s27_v2_replay/pnl_input_contract.py
src/carver/spine/s27_v2_replay/validation_input_contract.py
```

Changes:

- retained locked expected-source maps;
- added internally-derived active source-authority maps;
- required each caller-supplied expected map to match the internally-derived active authority map before field-level source hashes are checked against it.

### Source-Input Root Layers

Patched:

```text
src/carver/spine/s27_v2_replay/source_input_selection_contract.py
src/carver/spine/s27_v2_replay/source_input_manifest_contract.py
```

Changes:

- source-input selection now binds per-role source-row-batch contract and row-batch hashes to active top-level source-row-batch authority;
- source-input manifest now binds per-field role contract, selected row, and selected row-locator hashes to active source-input-selection and row-locator authority;
- these root-layer per-role/per-field hashes are no longer accepted only as SHA-shaped values.

### Final Trusted Bundle

Patched:

```text
src/carver/spine/s27_v2_replay/trusted_bundle_contract.py
```

Changes:

- added explicit top-level fields for:

```text
replay_trust_root_hash
active_evidence_manifest_hash
validation_ledger_hash
provenance_ledger_hash
local_hostile_audit_result_hash
```

- derived the trusted-bundle expected source map internally from:

```text
replay_trust_root_hash
active_evidence_manifest_hash
construction_contract_hash
validation_input_contract_hash
validation_contract_bundle_hash
validation_ledger_hash
provenance_ledger_hash
local_hostile_audit_result_hash
trusted_bundle_policy_hash
```

- required the caller-supplied expected map to match this active map before individual trusted-bundle input fields are validated.

## Static Inspection

Static scan confirmed every contract containing `expected_source_contract_hash_by_input_label` now also calls:

```text
require_hash_map_matches_active_authority()
```

## Local Audit Finding Patch

The first local hostile audit of this patch found:

```text
P1: CostInputContractBundle used an undefined cost_contract_bundle_hash attribute while deriving active authority.
P2: source-input selected-row and selected-row-locator hashes were still too coarse for a strict role-to-field authority chain.
```

Additional patch:

```text
src/carver/spine/s27_v2_replay/cost_input_contract.py
src/carver/spine/s27_v2_replay/source_input_selection_contract.py
src/carver/spine/s27_v2_replay/source_input_manifest_contract.py
```

Changes:

- corrected cost active authority derivation to use the existing `fill_contract_bundle_hash`;
- added selected-row and selected-row-locator expected maps to source-input selection;
- added role-level active selected-row and selected-row-locator maps to source-input manifest;
- made manifest fields resolve selected-row and selected-row-locator authority through their locked source-input roles.

The follow-up local re-audit confirmed the cost P1 was fixed, but still found the source-input row/locator authority too coarse. A second narrow patch then:

- added explicit active selected-row and selected-row-locator authority maps to source-input selection;
- added the validated `SourceInputRoleSelectionContract` tuple to source-input manifest;
- required source-input manifest active role, row, and locator maps to match the corresponding validated role-selection contracts before manifest fields can consume them.

## Non-Authorization

This patch record authorizes no provider/API calls, downloads, parser execution, file replay, diagnostics, tests/backtests, OOS, Lockbox, Forward, Git staging, commits, pushes, PRs, adapter work, deployment, trading, promotion, tuning, result interpretation, or source-faithful replay evidence claim.
