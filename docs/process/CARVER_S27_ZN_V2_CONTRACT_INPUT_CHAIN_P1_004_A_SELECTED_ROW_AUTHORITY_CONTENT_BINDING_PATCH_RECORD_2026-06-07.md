# S27 ZN V2 Contract/Input Chain P1-004-A Selected-Row Authority Content-Binding Patch Record

Date: 2026-06-07

Status:

```text
PROCESS_ONLY_S27_ZN_V2_CONTRACT_INPUT_CHAIN_P1_004_A_SELECTED_ROW_AUTHORITY_CONTENT_BINDING_PATCH_RECORD_NOT_EXECUTION_AUTHORIZATION
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

GPT Extended Pro external re-audit of the trust/evidence binding patch returned `FAIL` because the selected-row and selected-locator maps inside `SourceRowSelectionAuthorityContract` were not content-bound to the active `SOURCE_ROW_SELECTION_AUTHORITY` artifact hash before becoming authority.

External synthesis:

```text
docs/process/CARVER_S27_ZN_V2_CONTRACT_INPUT_CHAIN_P1_004_A_TRUST_EVIDENCE_BINDING_EXTERNAL_REAUDIT_SYNTHESIS_2026-06-07.md
```

## Patched File

```text
src/carver/spine/s27_v2_replay/source_input_selection_contract.py
```

## Patch Summary

Added deterministic content hashing helpers:

```text
_ordered_hash_map_payload(...)
_canonical_sha256(...)
```

Changed:

```text
SourceRowSelectionAuthorityContract.validate()
```

After strict status/hash/map-shape checks, the authority now recomputes:

```text
selected_row_membership_proof_set_hash
selected_row_locator_membership_proof_set_hash
source_row_selection_authority_hash
```

The authority hash payload includes:

```text
source-row-batch contract hash
source-row-batch set hash
source-universe contract bundle hash
row-locator contract bundle hash
selected-row hash map by locked input role
selected-row-locator hash map by locked input role
selected-row membership-proof hash map by locked input role
selected-row-locator membership-proof hash map by locked input role
membership proof-set hashes
authority policy hash
authority status
```

Changed:

```text
SourceInputSelectionContractBundle.validate_against_external_authority(...)
```

The bundle now validates `source_row_selection_authority` before `_validate_contract_only_shape()` can read `_active_*` maps from it.

## Local Audit Follow-Up

The first local hostile audit found one P1 ordering issue: content-bound validation existed, but `_validate_contract_only_shape()` still read the active maps before `_validate_source_row_selection_authority(...)` ran.

The follow-up ordering patch moved `self.source_row_selection_authority.validate()` ahead of `_validate_contract_only_shape()`.

## Non-Execution

No parser, file replay, diagnostics, tests, backtests, OOS, Lockbox, Forward, provider/API, downloads, git actions, adapter work, deployment, trading, promotion, result interpretation, or source-faithful evidence claim were performed or authorized by this patch.

## Next Gate

Continue the consolidated loop with local hostile re-audit of the selected-row authority content-binding patch.
