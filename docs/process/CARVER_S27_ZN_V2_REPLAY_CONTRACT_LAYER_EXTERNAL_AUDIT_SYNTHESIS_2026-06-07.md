# S27 ZN V2 Replay Contract Layer External Audit Synthesis

Date: 2026-06-07

Status:

```text
PROCESS_ONLY_S27_ZN_V2_REPLAY_CONTRACT_LAYER_EXTERNAL_AUDIT_SYNTHESIS_NOT_PATCH_OR_EXECUTION_AUTHORIZATION
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Source

Operator supplied the GPT Extended Pro / GPT-5.5 external hostile-audit result for the locally audited S27_V2 replay contract-layer scaffold packet:

```text
docs/process/CARVER_S27_ZN_V2_REPLAY_CONTRACT_LAYER_EXTERNAL_AUDIT_HANDOFF_2026-06-07.md
```

The external audit inspected the source packet:

```text
S27_V2_REPLAY_CONTRACT_LAYER_SOURCE_PACKET_2026-06-07.zip
```

The external audit reported observed source zip SHA256:

```text
3423e076dc5d2e27249de07e24d04b07cb38eb5a39f4df8dc6979477421651b8
```

## Verdict

```text
PASS_WITH_REQUIRED_EDITS
```

The external audit found:

```text
P0: NONE
P1: 2
P2: 3
P3: 2
```

The audit confirmed no parser/file replay, provider/API/download, diagnostic/test/backtest, OOS/Lockbox/Forward, adapter, deployment, trading, promotion, or active execution surface in the source packet.

## P1 Findings

### P1-1 Stale Evidence Supersession Trust-Root Binding

The audit found that stale-evidence supersession is represented but not explicitly trust-root-bound as a named manifest artifact.

Affected surfaces:

```text
src/carver/spine/s27_v2_replay/trust_root.py
src/carver/spine/s27_v2_replay/runner.py
src/carver/spine/s27_v2_replay/constants.py
src/carver/spine/s27_v2_replay/evidence_manifest.py
src/carver/spine/s27_v2_replay/artifact_manifest_plan.py
```

Required hardening:

```text
Add stale_evidence_supersession_manifest_hash to ReplayTrustRoot.
Add STALE_EVIDENCE_SUPERSESSION_MANIFEST to required evidence artifact types.
Cross-check that artifact in TrustedReplayBundleScaffold.validate().
Require superseded_artifacts to be tuple-valued in evidence_manifest.py and artifact_manifest_plan.py.
```

### P1-2 Complete Unresolved-Gate Coverage

The audit found that unresolved-gate coverage is distributed across labels but not machine-checked as one locked gate tuple.

Affected surfaces:

```text
src/carver/spine/s27_v2_replay/constants.py
src/carver/spine/s27_v2_replay/construction_contract.py
src/carver/spine/s27_v2_replay/replay_builder_plan.py
src/carver/spine/s27_v2_replay/validation_contract.py
```

Required hardening:

```text
Add REQUIRED_UNRESOLVED_GATE_LABELS as the complete locked gate tuple.
Enforce exact gate coverage in at least one top-level construction/planning/validation contract surface.
Ensure no unknown gate and no missing gate can pass.
```

## P2 Findings

### P2-1 Capacity/Speed Binding

Capacity/speed exists as a label but not as a bound validation/evidence artifact.

Recommended before parser implementation and required before any performance interpretation:

```text
Add capacity_speed_eligibility_policy_hash or capacity_speed_eligibility_manifest_hash as a first-class validation/evidence placeholder.
Optionally add CAPACITY_SPEED_ELIGIBILITY_POLICY to evidence artifact types.
```

### P2-2 Forecast/Position Arithmetic Proof Boundary

Forecast and position validators are intentionally partial. Future implementation must not treat current validators as source-faithfulness proof.

Required before any replay-evidence claim:

```text
Either add explicit formula fields/checks, or ensure the future trusted runner recomputes all arithmetic from local rows and emits validation/provenance ledger formula bindings.
```

### P2-3 Complete Order-Plan Set Proof

Individual order rows are constrained, but no concrete order-plan bundle proves the complete adjacent limit set for each step.

Required before parser/file replay execution:

```text
Add an OrderPlanLedgerRow or OrderPlanBundle contract binding expected/emitted limit-order set hashes, market-order trigger/no-market proof, cap-bound omissions, tick policy, and order-plan hash.
```

## P3 Findings

### P3-1 Handoff Hash Manifest

The handoff packet had a file list but no self-contained machine-readable hash manifest.

Recommended:

```text
Add a packet/source hash manifest with file-level SHA256 hashes and source zip SHA256.
```

### P3-2 Direct Submodule Imports

Direct submodule imports can expose structural dataclasses, but package-root export is properly fail-closed.

Recommended:

```text
Maintain root export discipline in future slices.
```

## Current Gate

Parser/file replay implementation remains blocked until the P1 items are patched and locally re-audited.

This synthesis authorizes no code patch, no parser/file replay execution, no diagnostics, no tests/backtests, no provider/API calls, no downloads, no OOS, no Lockbox, no Forward, no Git actions, no adapter work, no deployment, no trading, no promotion, no result interpretation, and no source-faithful replay evidence claim.

## Next Required Authorization

The next step requires separate explicit operator authorization for a narrow P1 hardening patch only.
