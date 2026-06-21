# S27 ZN V2 Contract/Input Chain GPT P1-004 Authority Re-Audit Synthesis

Date: 2026-06-07

Status:

```text
PROCESS_ONLY_S27_ZN_V2_CONTRACT_INPUT_CHAIN_GPT_P1_004_AUTHORITY_REAUDIT_SYNTHESIS_NOT_EXECUTION_AUTHORIZATION
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Source

GPT Extended Pro external hostile re-audit of the locally re-audited S27 V2 contract/input chain hardening patch.

## Verdict

```text
FAIL
```

GPT found no P0 issue, but found that prior `P1-004` remained partially open.

## Closed Prior Items

GPT accepted these prior blockers as closed in the static packet:

```text
P1-001 packet completeness
P1-002 forecast sigma bridge
P1-003 V/Q/M history binding
P2-001 construction artifact coverage
P3-001 controlled fail-closed error taxonomy
```

## Remaining P1

### P1-004 Expected Source Hash Maps Are Still Not Anchored To Active Authority

GPT accepted that downstream input bundles now compare observed field-level source hashes to expected maps, but rejected the maps themselves as still caller-supplied.

Concrete failure mode described by GPT:

```text
A forged trusted-bundle contract can set an expected-source map entry to an arbitrary valid SHA256 hash, set the corresponding field source hash to the same arbitrary hash, and set the top-level upstream hash to a different valid hash. The prior validator checked the field against the map, but not the map against the active top-level upstream authority.
```

GPT also flagged the source-input manifest and source-input selection root layers as too weak if their per-field or per-role hashes are not tied to active source-input-selection, source-row-batch, source-universe, row-locator, or raw-file-hash authority.

## Required Remediation

Patch scope:

```text
S27_V2_CONTRACT_INPUT_CHAIN_P1_004_ACTIVE_AUTHORITY_ANCHORING_PATCH_ONLY
```

Required changes:

- derive expected maps from active top-level/upstream fields inside validation, or bind them to an active authority object that itself is tied to the trust root/evidence manifest and upstream bundle hashes;
- make trusted-bundle expected input hashes match top-level trust-root, evidence-manifest, construction, validation-input, validation-bundle, validation-ledger, provenance-ledger, local-audit, and policy hashes;
- patch source-input selection and source-input manifest so their per-role/per-field hashes are tied to active upstream authority rather than only SHA shape;
- preserve all non-authorization constraints.

## Non-Authorization

This synthesis authorizes no provider/API calls, downloads, parser execution, file replay, diagnostics, tests/backtests, OOS, Lockbox, Forward, Git staging, commits, pushes, PRs, adapter work, deployment, trading, promotion, tuning, result interpretation, or source-faithful replay evidence claim.
