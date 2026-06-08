# S27 ZN V2 Contract/Input Chain P1-004-A Selected-Row Authority Content-Binding External Re-Audit Handoff

Date: 2026-06-07

Status:

```text
PROCESS_ONLY_S27_ZN_V2_CONTRACT_INPUT_CHAIN_P1_004_A_SELECTED_ROW_AUTHORITY_CONTENT_BINDING_EXTERNAL_REAUDIT_HANDOFF_NOT_EXECUTION_AUTHORIZATION
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Consolidated Operator Gate

This handoff was prepared under the consolidated P1-004-A authority-remediation loop after local hostile re-audit returned `PASS`.

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

## Handoff Folder

Folder:

```text
C:\Users\apops\Desktop\GPT
```

The folder was cleaned before packet creation.

`Carver.pdf` copied:

```text
NO
```

Rationale:

```text
GPT already has the book attached in the app/library for this thread.
```

## Source Packet

Zip:

```text
S27_V2_P1_004_A_SELECTED_ROW_AUTHORITY_CONTENT_BINDING_REAUDIT_SOURCE_PACKET_2026-06-07.zip
```

Zip SHA256:

```text
A22D8B325C843691F5F073406B125378A4BE7A22B7A9A11DBB506F382B68FFEE
```

Zip entry count:

```text
53
```

Zip contents:

```text
src/carver/spine/m0.py
src/carver/spine/s27_v2_replay/*.py
```

## Audit Question

The external auditor should decide whether `P1-004-A` is now closed by the selected-row authority content-binding patch.

Specific checks:

```text
SourceRowSelectionAuthorityContract.validate() recomputes content-bound hashes before selected-row maps can be consumed.
selected_row_hash_by_input_role and selected_row_locator_hash_by_input_role are included in source_row_selection_authority_hash.
selected_row_membership_proof_hash_by_input_role is content-bound to selected_row_membership_proof_set_hash.
selected_row_locator_membership_proof_hash_by_input_role is content-bound to selected_row_locator_membership_proof_set_hash.
SourceInputSelectionContractBundle.validate_against_external_authority(...) validates source_row_selection_authority before _validate_contract_only_shape() reads _active_* maps.
The earlier trust/evidence binding remains intact.
No execution/provider/download/parser/replay/test/backtest/git/adapter/deployment/trading/promotion surface was introduced.
```

## Gate

Parser/file replay implementation must not proceed from this handoff alone. It remains blocked until external re-audit result is received and a separate operator authorization is given.

## Non-Authorization

This handoff authorizes no provider/API calls, downloads, parser execution, file replay, diagnostics, tests/backtests, OOS, Lockbox, Forward, Git staging, commits, pushes, PRs, adapter work, deployment, trading, promotion, tuning, result interpretation, or source-faithful replay evidence claim.
