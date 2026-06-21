# S27 ZN V2 Contract/Input Chain P1-004-A Trust/Evidence Binding External Re-Audit Handoff

Date: 2026-06-07

Status:

```text
PROCESS_ONLY_S27_ZN_V2_CONTRACT_INPUT_CHAIN_P1_004_A_TRUST_EVIDENCE_BINDING_EXTERNAL_REAUDIT_HANDOFF_NOT_EXECUTION_AUTHORIZATION
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Consolidated Operator Gate

This handoff was prepared under the consolidated P1-004-A authority-remediation loop after local hostile audit returned `PASS`.

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
S27_V2_P1_004_A_TRUST_EVIDENCE_BINDING_REAUDIT_SOURCE_PACKET_2026-06-07.zip
```

Zip SHA256:

```text
AD1713F159D35248A9AE4CC486AF59D7C338D2BC258CBC1F9615DFF117BEC522
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

The external auditor should decide whether `P1-004-A` is now closed by the trust/evidence binding patch.

Specific checks:

```text
require_evidence_manifest_matches_trust_root(...) is a shared runner-equivalent trust/evidence binding helper.
The helper requires EvidenceManifest.active_evidence_manifest_hash to match ReplayTrustRoot.active_evidence_manifest_hash.
The helper requires SOURCE_INPUT_UNIVERSE_MANIFEST to match ReplayTrustRoot.source_input_universe_manifest_hash.
The helper requires SOURCE_ROW_BATCH_CONTRACT to match ReplayTrustRoot.source_row_batch_contract_hash.
The helper requires SOURCE_ROW_BATCH_SET to match ReplayTrustRoot.source_row_batch_set_hash.
The helper requires SOURCE_ROW_LOCATOR to match ReplayTrustRoot.source_row_locator_hash.
The helper requires SOURCE_ROW_SELECTION_AUTHORITY to match ReplayTrustRoot.source_row_selection_authority_hash.
SourceInputManifestContractBundle._validate_active_trust_authority(...) calls the helper before accepting SourceRowSelectionExternalAuthorityHandle.
TrustedReplayBundleScaffold.validate() uses the same helper, avoiding runner/manifest drift.
No execution/provider/download/parser/replay/test/backtest/git/adapter/deployment/trading/promotion surface was introduced.
```

## Gate

Parser/file replay implementation must not proceed from this handoff alone. It remains blocked until external re-audit result is received and a separate operator authorization is given.

## Non-Authorization

This handoff authorizes no provider/API calls, downloads, parser execution, file replay, diagnostics, tests/backtests, OOS, Lockbox, Forward, Git staging, commits, pushes, PRs, adapter work, deployment, trading, promotion, tuning, result interpretation, or source-faithful replay evidence claim.
