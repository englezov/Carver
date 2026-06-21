# S27 ZN V2 Contract/Input Chain P1-004 Second External Re-Audit Synthesis

Date: 2026-06-07

Status:

```text
PROCESS_ONLY_S27_ZN_V2_CONTRACT_INPUT_CHAIN_P1_004_SECOND_EXTERNAL_REAUDIT_SYNTHESIS_NOT_EXECUTION_AUTHORIZATION
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Source

GPT Extended Pro external hostile re-audit of the P1-004 active-authority patch.

## Verdict

```text
FAIL
```

GPT found no P0 issue and accepted the final trusted-bundle authority portion as materially improved, but found that upstream/intermediate P1-004 authority leaks remained.

## P1 Findings

### P1-004-A Source-Input Selected-Row Authority Still Self-Authenticating

GPT found that source-input selection selected-row and selected-row-locator active maps were still caller-supplied bundle fields. Expected maps and role contracts could agree with those caller maps without proving authority from source-row, locator, raw-file, or trust-root lineage.

### P1-004-B Source-Input Manifest Could Cite One Selection Bundle While Consuming Another Embedded Role Tuple

GPT found that source-input manifest carried cited source-input-selection hashes but actually derived active role/row/locator authority from an embedded role-selection tuple that was not proven to be the tuple that produced the cited selection bundle.

### P1-004-C Runtime-History And Level-Compatibility Did Not Bind Selected Row/Locator Hashes To Manifest Authority

GPT found that runtime-history and level-compatibility input fields carried selected-row and selected-row-locator hashes but only checked them as SHA-shaped values, while only the manifest-field contract hash was expected-map checked.

### P1-004-D Validation And PnL Active Authority Maps Collapsed Distinct Source Kinds

GPT found validation and PnL input contracts mapped distinct locked source kinds to coarse unrelated authority hashes, such as trust-root/evidence/manifest all mapping to source-input-manifest contract hash, and several PnL source kinds mapping to source-input-manifest or cost-input contract hashes.

## Required Remediation

Patch scope:

```text
S27_V2_CONTRACT_INPUT_CHAIN_P1_004_NON_SELF_AUTHORITY_PATCH_ONLY
```

Required changes:

- introduce non-self-authenticating selected-row authority for source-input selection;
- bind source-input manifest to the cited source-input-selection bundle, not an unrelated embedded tuple;
- make level-compatibility and runtime-history verify manifest-field, selected-row, and selected-row-locator hashes against validated source-input manifest authority;
- make validation and PnL active authority maps label-specific and source-kind-specific.

## Non-Authorization

This synthesis authorizes no provider/API calls, downloads, parser execution, file replay, diagnostics, tests/backtests, OOS, Lockbox, Forward, Git staging, commits, pushes, PRs, adapter work, deployment, trading, promotion, tuning, result interpretation, or source-faithful replay evidence claim.
