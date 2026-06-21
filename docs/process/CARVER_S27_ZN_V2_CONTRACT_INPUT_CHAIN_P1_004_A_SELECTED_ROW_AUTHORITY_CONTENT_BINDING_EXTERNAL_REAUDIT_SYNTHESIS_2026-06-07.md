# S27 ZN V2 Contract/Input Chain P1-004-A Selected-Row Authority Content-Binding External Re-Audit Synthesis

Date: 2026-06-07

Status:

```text
PROCESS_ONLY_S27_ZN_V2_CONTRACT_INPUT_CHAIN_P1_004_A_SELECTED_ROW_AUTHORITY_CONTENT_BINDING_EXTERNAL_REAUDIT_SYNTHESIS_NOT_EXECUTION_AUTHORIZATION
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Scope

GPT Extended Pro audited the new selected-row authority content-binding packet:

```text
S27_V2_P1_004_A_SELECTED_ROW_AUTHORITY_CONTENT_BINDING_REAUDIT_SOURCE_PACKET_2026-06-07.zip
```

Packet SHA256:

```text
A22D8B325C843691F5F073406B125378A4BE7A22B7A9A11DBB506F382B68FFEE
```

This was an external hostile re-audit of the locally passed selected-row authority content-binding patch.

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
PASS
```

GPT found:

```text
P0: none
P1: none
P2: none
```

GPT explicitly marked:

```text
P1-004-A CLOSED
```

## Closure Summary

GPT found that the remaining self-authenticating payload gap is closed.

The selected-row, selected-locator, and membership-proof maps can no longer become authority merely because caller-supplied maps agree with themselves.

The accepted closure points were:

```text
SourceRowSelectionAuthorityContract.validate() checks status, upstream hashes, maps, policy hash, and authority hash before content-binding validation.
selected_row_membership_proof_hash_by_input_role is canonicalized and checked against selected_row_membership_proof_set_hash.
selected_row_locator_membership_proof_hash_by_input_role is canonicalized and checked against selected_row_locator_membership_proof_set_hash.
source_row_selection_authority_hash is recomputed from selected-row maps, selected-locator maps, membership-proof maps, proof-set hashes, upstream hashes, policy hash, artifact label, and status.
SourceInputSelectionContractBundle.validate() fails closed without an external authority handle.
validate_against_external_authority(...) validates the external handle and source_row_selection_authority before _validate_contract_only_shape() can read _active_* maps.
The earlier trust/evidence chain remains intact.
```

## P3 Note

GPT left one non-blocking P3 implementation-routing note:

```text
level_compatibility_input_contract.py and runtime_history_input_contract.py still call the no-argument source_input_manifest_contract_bundle.validate(), which intentionally fails closed.
Future implementation must route active trust authority through validate_against_active_trust_authority(...).
```

This is not a blocker to closing P1-004-A, but it remains a required future implementation-routing guard.

## Parser/File Replay Gate

Parser/file replay implementation remains blocked until separate operator authorization.

This PASS structurally unblocks P1-004-A as a candidate prerequisite only. It does not authorize provider/API access, downloads, parser execution, file replay, diagnostics, tests/backtests, OOS, Lockbox, Forward, Git actions, adapter work, deployment, trading, promotion, PnL/result interpretation, or source-faithful replay evidence claims.

## Non-Authorization

This synthesis authorizes no provider/API calls, downloads, parser execution, file replay, diagnostics, tests/backtests, OOS, Lockbox, Forward, Git staging, commits, pushes, PRs, adapter work, deployment, trading, promotion, tuning, result interpretation, or source-faithful replay evidence claim.
