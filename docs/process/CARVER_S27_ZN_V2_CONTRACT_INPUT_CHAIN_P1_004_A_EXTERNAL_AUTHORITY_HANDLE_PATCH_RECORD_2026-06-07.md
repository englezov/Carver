# S27 ZN V2 Contract/Input Chain P1-004-A External Authority Handle Patch Record

Date: 2026-06-07

Status:

```text
PROCESS_ONLY_S27_ZN_V2_CONTRACT_INPUT_CHAIN_P1_004_A_EXTERNAL_AUTHORITY_HANDLE_PATCH_RECORD_NOT_EXECUTION_AUTHORIZATION
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Consolidated Operator Gate

The operator authorized a consolidated P1-004-A remediation loop limited to closing the source-row-selection authority self-authentication finding.

Authorized within this loop:

```text
narrow trust/evidence/source-row-selection authority patches
local hostile audits with subagents after patches
follow-up patches for local P0/P1/P2 findings within P1-004-A scope
process/current-state records
GPT Extended Pro external re-audit packet preparation after local PASS
```

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

Local hostile audit of the prior authority-anchor patch returned `FAIL` because `ReplayTrustRoot` and `EvidenceManifest` were embedded as caller-supplied peer fields inside `SourceInputSelectionContractBundle`.

Local audit result:

```text
docs/process/CARVER_S27_ZN_V2_CONTRACT_INPUT_CHAIN_P1_004_A_AUTHORITY_ANCHOR_LOCAL_AUDIT_RESULT_2026-06-07.md
```

## Patched Files

```text
src/carver/spine/s27_v2_replay/source_input_selection_contract.py
src/carver/spine/s27_v2_replay/source_input_manifest_contract.py
```

## Patch Summary

Added:

```text
SourceRowSelectionExternalAuthorityHandle
```

The external handle carries only externally anchored trust/evidence/source-row-selection authority hashes and selected-row/locator membership proof-set hashes. It is not embedded inside `SourceInputSelectionContractBundle`.

Changed:

```text
SourceInputSelectionContractBundle.validate()
```

The default `validate()` path now fails closed with:

```text
S27 v2 source input selection requires an external authority handle
```

Added:

```text
SourceInputSelectionContractBundle.validate_against_external_authority(...)
```

This is now the only authority-validating path for source-input selection. It requires an external authority handle before accepting:

```text
source_row_batch_contract_hash
source_row_batch_set_hash
source_universe_contract_bundle_hash
row_locator_contract_bundle_hash
source_row_selection_authority_hash
selected_row_membership_proof_set_hash
selected_row_locator_membership_proof_set_hash
```

Changed:

```text
SourceInputManifestContractBundle
```

It now carries `source_row_selection_external_authority` outside the embedded source-input-selection bundle and calls:

```text
source_input_selection_contract_bundle.validate_against_external_authority(source_row_selection_external_authority)
```

This removes the direct self-contained validation path that allowed the selection bundle, trust root, evidence manifest, and row-selection authority to mutually authenticate inside one object boundary.

## Non-Execution

No parser, file replay, diagnostics, tests, backtests, OOS, Lockbox, Forward, provider/API, downloads, git actions, adapter work, deployment, trading, promotion, result interpretation, or source-faithful evidence claim were performed or authorized by this patch.

## Next Gate

Continue the consolidated loop with local hostile audit of this external-authority-handle patch.
