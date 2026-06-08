# S27 ZN V2 Contract/Input Chain P1-004-A Trust/Evidence Binding External Re-Audit Synthesis

Date: 2026-06-07

Status:

```text
PROCESS_ONLY_S27_ZN_V2_CONTRACT_INPUT_CHAIN_P1_004_A_TRUST_EVIDENCE_BINDING_EXTERNAL_REAUDIT_SYNTHESIS_NOT_EXECUTION_AUTHORIZATION
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Scope

GPT Extended Pro audited the new `S27_V2_P1_004_A_TRUST_EVIDENCE_BINDING_REAUDIT_SOURCE_PACKET_2026-06-07.zip`.

This was an external hostile re-audit of the locally passed trust/evidence binding patch.

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

GPT found no P0 findings, no P2 findings, and no execution surface.

GPT accepted that the prior trust/evidence binding gap was fixed:

```text
EvidenceManifest active entries are checked against ReplayTrustRoot.
SourceInputManifestContractBundle calls the shared helper before accepting SourceRowSelectionExternalAuthorityHandle.
TrustedReplayBundleScaffold uses the same helper.
```

## Remaining P1 Finding

`P1-004-A` remained open because the selected-row and selected-locator maps inside `SourceRowSelectionAuthorityContract` were still caller-supplied payload and were not content-bound to the active `SOURCE_ROW_SELECTION_AUTHORITY` artifact hash before becoming authority.

GPT identified these caller-supplied maps:

```text
selected_row_hash_by_input_role
selected_row_locator_hash_by_input_role
selected_row_membership_proof_hash_by_input_role
selected_row_locator_membership_proof_hash_by_input_role
```

GPT required that these maps be derived from a verified authority payload rather than merely read from a dataclass that declares the trusted hash.

GPT also required membership-proof maps to be content-bound to their proof-set hashes before role contracts consume them.

## Gate

Parser/file replay implementation remains blocked.

The next authorized action under the consolidated P1-004-A authority-remediation loop is a narrow selected-row authority payload content-binding patch, followed by local hostile audit and external re-audit packet preparation only if local audit passes.

## Non-Authorization

This synthesis authorizes no provider/API calls, downloads, parser execution, file replay, diagnostics, tests/backtests, OOS, Lockbox, Forward, Git staging, commits, pushes, PRs, adapter work, deployment, trading, promotion, tuning, result interpretation, or source-faithful replay evidence claim.
