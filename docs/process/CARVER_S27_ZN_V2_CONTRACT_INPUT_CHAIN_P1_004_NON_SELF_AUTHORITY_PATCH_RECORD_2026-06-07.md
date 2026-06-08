# S27 ZN V2 Contract/Input Chain P1-004 Non-Self Authority Patch Record

Date: 2026-06-07

Status:

```text
PROCESS_ONLY_S27_ZN_V2_CONTRACT_INPUT_CHAIN_P1_004_NON_SELF_AUTHORITY_PATCH_RECORD_NOT_EXECUTION_AUTHORIZATION
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Trigger

GPT Extended Pro external hostile re-audit returned `FAIL` because the prior active-authority patch still allowed self-authenticating or overly coarse active maps in upstream/intermediate source authority layers.

External synthesis:

```text
docs/process/CARVER_S27_ZN_V2_CONTRACT_INPUT_CHAIN_P1_004_SECOND_EXTERNAL_REAUDIT_SYNTHESIS_2026-06-07.md
```

## Patched Scope

### Source-Input Selection

Patched:

```text
src/carver/spine/s27_v2_replay/source_input_selection_contract.py
```

Changes:

- added `SourceRowSelectionAuthorityContract`;
- bound authority to source-row-batch contract hash, source-row-batch set hash, source-universe contract bundle hash, row-locator contract bundle hash, and authority hash;
- changed selected-row and selected-row-locator active maps to derive from the authority object rather than returning bundle fields;
- required bundle active maps to match the authority object.

### Source-Input Manifest

Patched:

```text
src/carver/spine/s27_v2_replay/source_input_manifest_contract.py
```

Changes:

- added `SourceInputSelectionContractBundle` as an explicit manifest authority input;
- required the cited selection contract hash, selection set hash, source-universe hash, and row-locator hash to match the embedded selection bundle;
- required manifest role-selection contracts and active role/row/locator maps to match the cited selection bundle.

### Level Compatibility And Runtime History

Patched:

```text
src/carver/spine/s27_v2_replay/level_compatibility_input_contract.py
src/carver/spine/s27_v2_replay/runtime_history_input_contract.py
```

Changes:

- added validated `SourceInputManifestContractBundle` authority;
- derived manifest-field contract, selected-row, and selected-row-locator authority by locked input label through the validated manifest bundle;
- required each input field to match all three values instead of checking selected-row and selected-row-locator hashes only syntactically.

### Validation Inputs

Patched:

```text
src/carver/spine/s27_v2_replay/validation_input_contract.py
```

Changes:

- added explicit top-level replay trust-root hash, active evidence-manifest hash, source-input manifest hash, validation ledger schema hash, provenance ledger schema hash, and local hostile-audit schema hash;
- mapped validation input authority by locked source kind instead of collapsing trust-root/evidence/manifest/schema authority into coarse unrelated hashes.

### PnL Inputs

Patched:

```text
src/carver/spine/s27_v2_replay/pnl_input_contract.py
```

Changes:

- added explicit top-level authority hashes for trust root, source universe, transition/working-state/position outputs, close-only price policy, start/end price rows, raw-symbol continuity, roll bridge, multiplier, currency policy, fill hash set, and cost hash set;
- replaced coarse source-kind grouping with a label-specific active authority map for every locked PnL input.

## Non-Authorization

This patch record authorizes no provider/API calls, downloads, parser execution, file replay, diagnostics, tests/backtests, OOS, Lockbox, Forward, Git staging, commits, pushes, PRs, adapter work, deployment, trading, promotion, tuning, result interpretation, or source-faithful replay evidence claim.
