# S27 ZN V2 Replay Contract Layer GPT P1 Hardening Patch Record

Date: 2026-06-07

Status:

```text
PROCESS_ONLY_S27_ZN_V2_REPLAY_CONTRACT_LAYER_GPT_P1_HARDENING_PATCH_RECORD_NOT_EXECUTION_AUTHORIZATION
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Authorization Boundary

Operator authorization received:

```text
Operator authorizes S27_V2 replay contract-layer GPT P1 hardening patch only, covering stale-evidence supersession trust-root binding and complete unresolved-gate coverage, no provider/API, no downloads, no parser/file replay execution, no diagnostics, no tests/backtests, no OOS/Lockbox/Forward, no git actions, no adapter work, no deployment, no trading, no promotion.
```

This patch record documents only static scaffold hardening for the two GPT P1 contract-layer findings. It authorizes no parser execution, file replay, diagnostics, tests/backtests, OOS, Lockbox, Forward, provider/API calls, downloads, Git actions, adapter work, deployment, trading, promotion, result interpretation, or source-faithful replay evidence claim.

## Source Audit Input

The patch responds to:

```text
docs/process/CARVER_S27_ZN_V2_REPLAY_CONTRACT_LAYER_EXTERNAL_AUDIT_SYNTHESIS_2026-06-07.md
```

GPT returned:

```text
PASS_WITH_REQUIRED_EDITS
```

The two P1 findings patched here were:

```text
P1-1 Stale Evidence Supersession Trust-Root Binding
P1-2 Complete Unresolved-Gate Coverage
```

## Patched Code Surfaces

Patched files:

```text
src/carver/spine/s27_v2_replay/constants.py
src/carver/spine/s27_v2_replay/trust_root.py
src/carver/spine/s27_v2_replay/runner.py
src/carver/spine/s27_v2_replay/evidence_manifest.py
src/carver/spine/s27_v2_replay/artifact_manifest_plan.py
src/carver/spine/s27_v2_replay/construction_contract.py
src/carver/spine/s27_v2_replay/replay_builder_plan.py
src/carver/spine/s27_v2_replay/validation_contract.py
```

## Stale Evidence Supersession Trust-Root Binding

The patch added a first-class trust-root binding for:

```text
ReplayTrustRoot.stale_evidence_supersession_manifest_hash
```

The active evidence manifest required artifact tuple now includes:

```text
STALE_EVIDENCE_SUPERSESSION_MANIFEST
```

The trusted replay bundle scaffold cross-checks that the active evidence manifest hash for `STALE_EVIDENCE_SUPERSESSION_MANIFEST` equals the trust-root field.

Both active evidence-manifest code paths now require `superseded_artifacts` to be tuple-valued:

```text
EvidenceManifest.superseded_artifacts
PlannedEvidenceManifest.superseded_artifacts
```

## Complete Unresolved-Gate Coverage

The patch added a single locked unresolved-gate tuple:

```text
REQUIRED_UNRESOLVED_GATE_LABELS
```

The patch binds this tuple in three contract-layer surfaces:

```text
construction_contract.py
replay_builder_plan.py
validation_contract.py
```

The construction and replay-builder contracts reject unknown gate labels and require supplied phase/step gates to cover the complete locked set. The validation contract requires its supplied `required_unresolved_gate_labels` tuple to exactly match `REQUIRED_UNRESOLVED_GATE_LABELS`.

## Preserved Boundaries

The package-root export boundary remains fail-closed. No new contract dataclasses, trust-root internals, required-gate constants, or stale-evidence artifact types were exported from:

```text
src/carver/spine/s27_v2_replay/__init__.py
```

The only package-root execution-facing function remains:

```text
build_trusted_replay_bundle
```

It remains a fail-closed scaffold stub.

## Static Verification

Static text verification found:

```text
INTENDED_P1_BINDINGS_FOUND
NO_FORBIDDEN_EXECUTION_PROVIDER_DOWNLOAD_BACKTEST_DIAGNOSTIC_TEXT_MATCHES_IN_REPLAY_PACKAGE
PACKAGE_ROOT_EXPORT_BOUNDARY_UNCHANGED_BY_TEXT_SCAN
NO_STATIC_INSTANTIATION_SITES_FOUND_FOR_CHANGED_DATACLASS_SIGNATURES
```

Python import, compile, unit-test, diagnostic, parser/file replay, and backtest execution were intentionally not run under this authorization.

## Next Gate

The next gate is a local hostile audit of this narrow GPT P1 hardening patch under the standing local hostile-audit pre-approval rule.

That audit must remain static/read-only and must not run parser/file replay, diagnostics, tests/backtests, provider/API calls, downloads, OOS, Lockbox, Forward, Git actions, adapter work, deployment, trading, promotion, result interpretation, or source-faithful replay evidence claims.
