# S27 ZN V2 Contract/Input Chain P1-004-A External Authority Handle External Re-Audit Synthesis

Date: 2026-06-07

Status:

```text
PROCESS_ONLY_S27_ZN_V2_CONTRACT_INPUT_CHAIN_P1_004_A_EXTERNAL_AUTHORITY_HANDLE_EXTERNAL_REAUDIT_SYNTHESIS_NOT_EXECUTION_AUTHORIZATION
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Source

GPT Extended Pro external hostile re-audit of:

```text
docs/process/CARVER_S27_ZN_V2_CONTRACT_INPUT_CHAIN_P1_004_A_EXTERNAL_AUTHORITY_HANDLE_EXTERNAL_REAUDIT_HANDOFF_2026-06-07.md
```

## Verdict

```text
FAIL
```

The external audit found no P0 and no P2 findings, but `P1-004-A` remains open.

## Closed Items Preserved

The audit marked the following still closed:

```text
P1-004-B
P1-004-C subject to upstream A
P1-004-D
```

No execution/provider/download/parser/replay/test/backtest/git/adapter/deployment/trading/promotion surface was found.

## Remaining P1

### P1-004-A

Status:

```text
NOT_CLOSED
```

Finding:

```text
SourceRowSelectionExternalAuthorityHandle moved selected-row authority outside SourceInputSelectionContractBundle, and SourceInputSelectionContractBundle.validate() now fails closed. However, the handle is still accepted as a caller-supplied object at the SourceInputManifestContractBundle boundary and is not validated against an actual ReplayTrustRoot and EvidenceManifest pair when consumed.
```

Required fix direction:

```text
Make the handle non-self-authenticating at the point it is consumed.
```

The external audit identified a sufficient structural path:

```text
remove source_row_selection_external_authority as a normal caller-supplied field from SourceInputManifestContractBundle or make no-argument manifest validate() fail closed
add validate_against_active_trust_authority(replay_trust_root, evidence_manifest, external_authority)
require external_authority.replay_trust_root_hash == replay_trust_root.replay_trust_root_hash
require external_authority.active_evidence_manifest_hash == replay_trust_root.active_evidence_manifest_hash
require external_authority.active_evidence_manifest_hash == evidence_manifest.active_evidence_manifest_hash
require external_authority.source_row_selection_authority_hash == replay_trust_root.source_row_selection_authority_hash
require external_authority.source_row_selection_authority_hash == evidence_manifest.active_hash_by_type("SOURCE_ROW_SELECTION_AUTHORITY")
require external_authority.source_row_batch_contract_hash == evidence_manifest.active_hash_by_type("SOURCE_ROW_BATCH_CONTRACT")
require external_authority.source_row_batch_set_hash == evidence_manifest.active_hash_by_type("SOURCE_ROW_BATCH_SET")
require external_authority.row_locator_contract_bundle_hash == evidence_manifest.active_hash_by_type("SOURCE_ROW_LOCATOR")
bind source-universe value to SOURCE_INPUT_UNIVERSE_MANIFEST or explicitly resolve the naming convention
```

## Gate

Parser/file replay implementation remains blocked.

The consolidated P1-004-A authority-remediation loop remains active for narrow follow-up patching, local hostile audit, and GPT re-audit packet preparation after local pass.

## Non-Authorization

This synthesis authorizes no provider/API calls, downloads, parser execution, file replay, diagnostics, tests/backtests, OOS, Lockbox, Forward, Git staging, commits, pushes, PRs, adapter work, deployment, trading, promotion, tuning, result interpretation, or source-faithful replay evidence claim.
