# S27 ZN V2 Contract/Input Chain P1-004-A Trust/Evidence Binding Patch Record

Date: 2026-06-07

Status:

```text
PROCESS_ONLY_S27_ZN_V2_CONTRACT_INPUT_CHAIN_P1_004_A_TRUST_EVIDENCE_BINDING_PATCH_RECORD_NOT_EXECUTION_AUTHORIZATION
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

GPT Extended Pro external re-audit of the manifest active-trust-authority patch returned `FAIL` because the manifest active-trust path accepted evidence-manifest entries for source universe, source row batch contract, source row batch set, and row locator without requiring those entries to match the corresponding `ReplayTrustRoot` fields.

External synthesis:

```text
docs/process/CARVER_S27_ZN_V2_CONTRACT_INPUT_CHAIN_P1_004_A_MANIFEST_ACTIVE_TRUST_AUTHORITY_EXTERNAL_REAUDIT_SYNTHESIS_2026-06-07.md
```

## Patched Files

```text
src/carver/spine/s27_v2_replay/evidence_manifest.py
src/carver/spine/s27_v2_replay/runner.py
src/carver/spine/s27_v2_replay/source_input_manifest_contract.py
```

## Patch Summary

Added shared helper:

```text
require_evidence_manifest_matches_trust_root(
    replay_trust_root,
    evidence_manifest,
)
```

The helper validates both objects and requires `EvidenceManifest.active_evidence_manifest_hash` to match `ReplayTrustRoot.active_evidence_manifest_hash`.

It then requires each active evidence artifact family to match its matching trust-root field, including:

```text
SOURCE_INPUT_UNIVERSE_MANIFEST
RAW_SOURCE_FILE_HASH_SET
SOURCE_ROW_BATCH_CONTRACT
SOURCE_ROW_BATCH_SET
SOURCE_ROW_LOCATOR
SOURCE_ROW_SELECTION_AUTHORITY
```

The helper also preserves the broader runner-equivalent trust/evidence checks for source lock, local data contract, provenance design, runner implementation, parser/extractor source, dependency/runtime manifest, replay config, canonical serialization policy, session/roll/tick/cost/spread/multiplier/compatibility policies, and stale-evidence supersession manifest.

Changed:

```text
TrustedReplayBundleScaffold.validate()
```

The runner now uses the shared helper rather than maintaining a separate local trust/evidence binding list.

Changed:

```text
SourceInputManifestContractBundle._validate_active_trust_authority(...)
```

The manifest active-trust path now calls the shared trust/evidence helper before validating or accepting `SourceRowSelectionExternalAuthorityHandle`.

## Intended Closure

The source-input manifest can no longer accept a handle whose source universe, row batch contract, row batch set, row locator, or row-selection-authority hashes are only internally consistent with `EvidenceManifest`. They must also be active evidence entries matching the supplied `ReplayTrustRoot`.

## Non-Execution

No parser, file replay, diagnostics, tests, backtests, OOS, Lockbox, Forward, provider/API, downloads, git actions, adapter work, deployment, trading, promotion, result interpretation, or source-faithful evidence claim were performed or authorized by this patch.

## Next Gate

Continue the consolidated loop with local hostile audit of this trust/evidence binding patch.
