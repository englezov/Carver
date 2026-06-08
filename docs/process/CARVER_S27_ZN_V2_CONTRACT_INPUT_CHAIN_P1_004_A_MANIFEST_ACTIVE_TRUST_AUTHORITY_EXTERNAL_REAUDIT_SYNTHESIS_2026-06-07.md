# S27 ZN V2 Contract/Input Chain P1-004-A Manifest Active Trust Authority External Re-Audit Synthesis

Date: 2026-06-07

Status:

```text
PROCESS_ONLY_S27_ZN_V2_CONTRACT_INPUT_CHAIN_P1_004_A_MANIFEST_ACTIVE_TRUST_AUTHORITY_EXTERNAL_REAUDIT_SYNTHESIS_NOT_EXECUTION_AUTHORIZATION
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Scope

GPT Extended Pro audited the new `S27_V2_P1_004_A_MANIFEST_ACTIVE_TRUST_REAUDIT_SOURCE_PACKET_2026-06-07.zip`, not the prior packet.

This was an external hostile re-audit of the locally passed manifest active-trust-authority patch.

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

## Verdict

```text
FAIL
```

GPT found no P0 findings and no P2 findings.

GPT accepted that:

```text
SourceInputManifestContractBundle no longer stores the external authority handle as a normal field.
SourceInputManifestContractBundle.validate() fails closed.
validate_against_active_trust_authority(...) requires ReplayTrustRoot, EvidenceManifest, and SourceRowSelectionExternalAuthorityHandle.
The old direct self-contained manifest-handle bypass is closed.
The public package/root boundary remains non-executing.
```

## Remaining P1 Finding

`P1-004-A` was still not closed because the manifest active-trust path did not fully bind the evidence manifest entries for source-row-batch contract, source-row-batch set, source universe, and row locator back to the matching `ReplayTrustRoot` fields before those entries could feed the external handle and source-input-selection authority.

GPT identified that `runner.py` already had a stronger trust-root/evidence-manifest binding pattern, but `SourceInputManifestContractBundle.validate_against_active_trust_authority(...)` did not call a shared equivalent check.

Required direct bindings:

```text
EvidenceManifest.active_hash_by_type("SOURCE_INPUT_UNIVERSE_MANIFEST")
    == ReplayTrustRoot.source_input_universe_manifest_hash

EvidenceManifest.active_hash_by_type("SOURCE_ROW_BATCH_CONTRACT")
    == ReplayTrustRoot.source_row_batch_contract_hash

EvidenceManifest.active_hash_by_type("SOURCE_ROW_BATCH_SET")
    == ReplayTrustRoot.source_row_batch_set_hash

EvidenceManifest.active_hash_by_type("SOURCE_ROW_LOCATOR")
    == ReplayTrustRoot.source_row_locator_hash

EvidenceManifest.active_hash_by_type("SOURCE_ROW_SELECTION_AUTHORITY")
    == ReplayTrustRoot.source_row_selection_authority_hash
```

GPT recommended extracting a shared helper or inlining the missing checks in the manifest validator before accepting the external authority handle.

## Gate

Parser/file replay implementation may not proceed from this packet.

The next authorized action under the consolidated P1-004-A authority-remediation loop is a narrow trust-root/evidence-manifest binding patch, followed by local hostile audit and external re-audit packet preparation only if local audit passes.

## Non-Authorization

This synthesis authorizes no provider/API calls, downloads, parser execution, file replay, diagnostics, tests/backtests, OOS, Lockbox, Forward, Git staging, commits, pushes, PRs, adapter work, deployment, trading, promotion, tuning, result interpretation, or source-faithful replay evidence claim.
