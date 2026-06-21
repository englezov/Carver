# S27 ZN V2 Contract/Input Chain P1-004-A Selected-Row Authority Content-Binding Local Audit Result

Date: 2026-06-07

Status:

```text
PROCESS_ONLY_S27_ZN_V2_CONTRACT_INPUT_CHAIN_P1_004_A_SELECTED_ROW_AUTHORITY_CONTENT_BINDING_LOCAL_AUDIT_RESULT_NOT_EXECUTION_AUTHORIZATION
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Scope

Local hostile audit was run with spawned subagents under the consolidated P1-004-A authority-remediation loop.

The audit scope was limited to the selected-row authority payload content-binding patch and the ordering fix.

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

## First Local Audit

Verdict:

```text
FAIL
```

The first local audit found no P0/P2/P3 findings and no execution surface, but found one P1 ordering issue:

```text
SourceInputSelectionContractBundle.validate_against_external_authority(...)
called _validate_contract_only_shape() before _validate_source_row_selection_authority(...).
_validate_contract_only_shape() consumed _active_* maps before source_row_selection_authority.validate() recomputed content-bound hashes.
```

The ordering issue was patched by validating `source_row_selection_authority` before `_validate_contract_only_shape()`.

## Local Re-Audit

Verdict:

```text
PASS
```

The local hostile re-audit found no P0/P1/P2/P3 findings.

The audit found that the selected-row authority issue appears closed:

```text
SourceInputSelectionContractBundle.validate_against_external_authority(...) validates the external handle, then validates source_row_selection_authority before _validate_contract_only_shape() can read _active_* maps.
SourceRowSelectionAuthorityContract.validate() calls _validate_content_bound_hashes() after strict hash/map shape checks.
Selected-row and selected-locator maps are content-bound into source_row_selection_authority_hash.
Selected-row membership-proof maps are content-bound to selected_row_membership_proof_set_hash.
Selected-row-locator membership-proof maps are content-bound to selected_row_locator_membership_proof_set_hash.
Ordering is locked by require_hash_map() and _ordered_hash_map_payload().
```

The audit also confirmed that the public runner/package remains non-executing:

```text
build_trusted_replay_bundle(...) raises ReplayExecutionBlocked.
The package root exports only the fail-closed runner boundary and constants.
```

## Non-Execution

No edits, provider/API calls, downloads, parser/file replay execution, diagnostics, tests/backtests, OOS, Lockbox, Forward, Git actions, adapter work, deployment, trading, promotion, or result interpretation were performed by the audit subagents.

## Next Gate

Under the consolidated P1-004-A loop, prepare a GPT Extended Pro external hostile re-audit handoff packet for this locally passed selected-row authority content-binding patch.
