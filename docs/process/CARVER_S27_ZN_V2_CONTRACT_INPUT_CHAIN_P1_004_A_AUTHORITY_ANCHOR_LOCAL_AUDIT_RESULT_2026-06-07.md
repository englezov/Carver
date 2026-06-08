# S27 ZN V2 Contract/Input Chain P1-004-A Authority Anchor Local Audit Result

Date: 2026-06-07

Status:

```text
PROCESS_ONLY_S27_ZN_V2_CONTRACT_INPUT_CHAIN_P1_004_A_AUTHORITY_ANCHOR_LOCAL_AUDIT_RESULT_NOT_EXECUTION_AUTHORIZATION
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Scope

Local hostile audit of:

```text
docs/process/CARVER_S27_ZN_V2_CONTRACT_INPUT_CHAIN_P1_004_A_AUTHORITY_ANCHOR_PATCH_RECORD_2026-06-07.md
```

Audit constraints:

```text
static source/document reads only
no file edits by auditor
no provider/API
no downloads
no parser/file replay execution
no diagnostics
no tests/backtests
no OOS/Lockbox/Forward
no git actions
no adapter work
no deployment/trading/promotion
```

## Verdict

```text
FAIL
```

## P0 Findings

```text
NONE
```

No execution/provider/test/backtest surface was found in the inspected patch scope. The fail-closed public runner boundary still raises `ReplayExecutionBlocked` unconditionally.

## P1 Findings

### P1-004-A Still Not Closed

Finding:

```text
The patch adds ReplayTrustRoot and EvidenceManifest to SourceInputSelectionContractBundle, but both are still embedded caller-supplied objects at the same boundary as SourceRowSelectionAuthorityContract.
```

Affected files:

```text
src/carver/spine/s27_v2_replay/source_input_selection_contract.py
src/carver/spine/s27_v2_replay/trust_root.py
src/carver/spine/s27_v2_replay/evidence_manifest.py
```

Reason:

```text
_validate_active_trust_root_authority() checks that the embedded trust root, embedded evidence manifest, and embedded source-row-selection authority agree with each other. It does not bind them to an already-active external trust-root/evidence authority outside SourceInputSelectionContractBundle.
```

Forgery path:

```text
A caller can forge a mutually consistent ReplayTrustRoot, EvidenceManifest, SourceRowSelectionAuthorityContract, expected maps, and role contracts. ReplayTrustRoot.validate() only shape-checks hashes. EvidenceManifest.validate() checks entry structure and required artifact types, but does not derive or verify active_evidence_manifest_hash from entries. Membership proof maps are still SHA-map checked inside the authority contract rather than anchored outside the same caller-supplied bundle.
```

## P2 Findings

```text
NONE
```

## P3 Notes

```text
NONE
```

## Required Next Fix Direction

The next patch should introduce a trust/evidence authority handle that is already outside `SourceInputSelectionContractBundle`, or a validated upstream membership-proof artifact whose hash is anchored outside the caller-supplied source-input-selection bundle.

The source-input-selection bundle must consume that external authority handle/hash rather than carrying the trust root and evidence manifest objects as peer caller-supplied bundle fields.

## Gate

Parser/file replay implementation remains blocked.

The next safe gate is a narrow P1-004-A external-authority-handle patch only, followed by local hostile re-audit.

## Non-Authorization

This local audit result authorizes no provider/API calls, downloads, parser execution, file replay, diagnostics, tests/backtests, OOS, Lockbox, Forward, Git staging, commits, pushes, PRs, adapter work, deployment, trading, promotion, tuning, result interpretation, or source-faithful replay evidence claim.
