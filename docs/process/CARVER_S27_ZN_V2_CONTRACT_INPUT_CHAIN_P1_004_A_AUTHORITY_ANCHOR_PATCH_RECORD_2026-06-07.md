# S27 ZN V2 Contract/Input Chain P1-004-A Authority Anchor Patch Record

Date: 2026-06-07

Status:

```text
PROCESS_ONLY_S27_ZN_V2_CONTRACT_INPUT_CHAIN_P1_004_A_AUTHORITY_ANCHOR_PATCH_RECORD_NOT_EXECUTION_AUTHORIZATION
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Operator Authorization

The operator authorized a narrow S27_V2 P1-004-A source-row-selection authority-anchor patch only.

Authorized scope:

```text
non-self-authenticating binding of SourceRowSelectionAuthorityContract to active trust-root/evidence-manifest authority or validated upstream source-row/locator membership proof
```

Explicit exclusions:

```text
no provider/API
no downloads
no parser/file replay execution
no diagnostics
no tests/backtests
no OOS/Lockbox/Forward
no git actions
no adapter work
no deployment
no trading
no promotion
```

## Trigger

GPT Extended Pro external hostile re-audit of the prior non-self-authority patch returned `FAIL` with only `P1-004-A` still open.

External synthesis:

```text
docs/process/CARVER_S27_ZN_V2_CONTRACT_INPUT_CHAIN_P1_004_NON_SELF_AUTHORITY_EXTERNAL_REAUDIT_SYNTHESIS_2026-06-07.md
```

Closed by that audit:

```text
P1-004-B
P1-004-C
P1-004-D
```

Remaining finding:

```text
P1-004-A SourceRowSelectionAuthorityContract remained caller-supplied/self-authenticating one layer up.
```

## Patched Files

```text
src/carver/spine/s27_v2_replay/constants.py
src/carver/spine/s27_v2_replay/trust_root.py
src/carver/spine/s27_v2_replay/runner.py
src/carver/spine/s27_v2_replay/replay_config.py
src/carver/spine/s27_v2_replay/source_input_selection_contract.py
```

## Patch Summary

### First-Class Evidence/Trust-Root Anchor

Added the following required active evidence-manifest artifact types:

```text
SOURCE_ROW_BATCH_CONTRACT
SOURCE_ROW_BATCH_SET
SOURCE_ROW_SELECTION_AUTHORITY
```

Added the corresponding trust-root fields:

```text
source_row_batch_contract_hash
source_row_batch_set_hash
source_row_selection_authority_hash
```

Updated the fail-closed trusted replay scaffold to require active evidence-manifest entries for these hashes to match the trust root.

### Source-Input Selection Binding

`SourceInputSelectionContractBundle` now carries:

```text
ReplayTrustRoot
EvidenceManifest
```

The bundle validates both and requires:

```text
trust_root.active_evidence_manifest_hash == evidence_manifest.active_evidence_manifest_hash
trust_root.source_row_batch_contract_hash == bundle.source_row_batch_contract_hash
trust_root.source_row_batch_set_hash == bundle.source_row_batch_set_hash
trust_root.source_input_universe_manifest_hash == bundle.source_universe_contract_bundle_hash
trust_root.source_row_locator_hash == bundle.row_locator_contract_bundle_hash
trust_root.source_row_selection_authority_hash == bundle.source_row_selection_authority_hash
evidence_manifest[SOURCE_ROW_SELECTION_AUTHORITY] == bundle.source_row_selection_authority_hash
```

The selected-row authority is therefore no longer accepted solely because the bundle and embedded authority agree with each other.

### Membership Proof Binding

Added per-role membership proof hashes:

```text
selected_row_membership_proof_hash_by_input_role
selected_row_locator_membership_proof_hash_by_input_role
```

`SourceInputRoleSelectionContract` now requires corresponding per-role proof hashes, and `SourceInputSelectionContractBundle` requires each role contract to match the authority-derived proof maps.

## Non-Execution

No parser, file replay, diagnostics, tests, backtests, OOS, Lockbox, Forward, provider/API, downloads, git actions, adapter work, deployment, trading, promotion, result interpretation, or source-faithful evidence claim were performed or authorized by this patch.

## Next Gate

The next safe gate is local hostile audit of this P1-004-A authority-anchor patch.

Parser/file replay implementation remains blocked until this patch is locally re-audited, externally re-audited cleanly, and separately authorized by the operator.
