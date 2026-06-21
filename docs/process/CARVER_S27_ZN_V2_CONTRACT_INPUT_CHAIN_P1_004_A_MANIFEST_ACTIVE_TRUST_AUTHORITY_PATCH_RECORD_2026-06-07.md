# S27 ZN V2 Contract/Input Chain P1-004-A Manifest Active Trust Authority Patch Record

Date: 2026-06-07

Status:

```text
PROCESS_ONLY_S27_ZN_V2_CONTRACT_INPUT_CHAIN_P1_004_A_MANIFEST_ACTIVE_TRUST_AUTHORITY_PATCH_RECORD_NOT_EXECUTION_AUTHORIZATION
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Consolidated Operator Gate

This patch was made under the consolidated P1-004-A authority-remediation loop.

Still excluded:

```text
provider/API
downloads
parser/file replay execution
diagnostics
tests/backtests
OOS/Lockbox/Forward
git actions
adapter work
deployment
trading
promotion
result interpretation
source-faithful replay evidence claim
```

## Trigger

GPT Extended Pro external re-audit of the external-authority-handle patch returned `FAIL` because the handle was still accepted as a caller-supplied field at the `SourceInputManifestContractBundle` boundary without validation against an actual `ReplayTrustRoot` and `EvidenceManifest` pair.

External synthesis:

```text
docs/process/CARVER_S27_ZN_V2_CONTRACT_INPUT_CHAIN_P1_004_A_EXTERNAL_AUTHORITY_HANDLE_EXTERNAL_REAUDIT_SYNTHESIS_2026-06-07.md
```

## Patched File

```text
src/carver/spine/s27_v2_replay/source_input_manifest_contract.py
```

## Patch Summary

Removed:

```text
source_row_selection_external_authority as a normal SourceInputManifestContractBundle field
```

Changed:

```text
SourceInputManifestContractBundle.validate()
```

The no-argument manifest validation path now fails closed:

```text
S27 v2 source input manifest requires active trust authority
```

Added:

```text
SourceInputManifestContractBundle.validate_against_active_trust_authority(
    replay_trust_root,
    evidence_manifest,
    source_row_selection_external_authority,
)
```

This path requires `ReplayTrustRoot`, `EvidenceManifest`, and `SourceRowSelectionExternalAuthorityHandle` at the point the manifest consumes source-input selected-row authority.

It now requires:

```text
external_authority.replay_trust_root_hash == replay_trust_root.replay_trust_root_hash
external_authority.active_evidence_manifest_hash == replay_trust_root.active_evidence_manifest_hash
external_authority.active_evidence_manifest_hash == evidence_manifest.active_evidence_manifest_hash
external_authority.source_row_selection_authority_hash == replay_trust_root.source_row_selection_authority_hash
external_authority.source_row_selection_authority_hash == evidence_manifest.active_hash_by_type("SOURCE_ROW_SELECTION_AUTHORITY")
external_authority.source_row_batch_contract_hash == evidence_manifest.active_hash_by_type("SOURCE_ROW_BATCH_CONTRACT")
external_authority.source_row_batch_set_hash == evidence_manifest.active_hash_by_type("SOURCE_ROW_BATCH_SET")
external_authority.row_locator_contract_bundle_hash == evidence_manifest.active_hash_by_type("SOURCE_ROW_LOCATOR")
external_authority.source_universe_contract_bundle_hash == evidence_manifest.active_hash_by_type("SOURCE_INPUT_UNIVERSE_MANIFEST")
```

Only after these checks does the manifest call:

```text
source_input_selection_contract_bundle.validate_against_external_authority(...)
```

## Non-Execution

No parser, file replay, diagnostics, tests, backtests, OOS, Lockbox, Forward, provider/API, downloads, git actions, adapter work, deployment, trading, promotion, result interpretation, or source-faithful evidence claim were performed or authorized by this patch.

## Next Gate

Continue the consolidated loop with local hostile audit of this manifest active-trust-authority patch.
