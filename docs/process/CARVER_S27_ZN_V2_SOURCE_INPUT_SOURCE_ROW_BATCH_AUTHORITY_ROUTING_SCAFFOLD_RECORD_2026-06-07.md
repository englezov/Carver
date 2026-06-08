# S27_V2 Source-Input Source-Row-Batch Authority Routing Scaffold Record

Date: 2026-06-07

Status:

```text
PROCESS_ONLY_S27_V2_SOURCE_INPUT_SOURCE_ROW_BATCH_AUTHORITY_ROUTING_SCAFFOLD_NOT_REPLAY_AUTHORIZATION
```

## Authorization

The operator authorized a consolidated S27_V2 parser/file replay scaffold-routing loop, limited to inert authority-routing and contract-binding scaffolds after active-trust routing external `PASS`.

This record covers only the source-input/source-row-batch authority-routing slice inside that consolidated gate.

## Scope

Patched files:

```text
src/carver/spine/s27_v2_replay/source_input_selection_contract.py
src/carver/spine/s27_v2_replay/source_input_manifest_contract.py
src/carver/spine/s27_v2_replay/level_compatibility_input_contract.py
src/carver/spine/s27_v2_replay/runtime_history_input_contract.py
```

Upstream authority already locally audited cleanly:

```text
src/carver/spine/s27_v2_replay/source_row_batch_contract.py
src/carver/spine/s27_v2_replay/parser_output_contract.py
```

## Change Summary

`SourceInputSelectionContractBundle.validate_against_external_authority(...)` now requires a validated `SourceRowBatchSetContract` and `ParserOutputBatchSetContract` in addition to the `SourceRowSelectionExternalAuthorityHandle`.

The source-input selection scaffold now validates `SourceRowBatchSetContract` against parser-output authority before accepting source-row-batch hashes. Per-role expected source-row-batch family-contract hashes and source-row-batch hashes are derived from the validated source-row-batch family contracts via the locked `REQUIRED_SOURCE_ROW_FAMILY_BY_INPUT_ROLE` map.

The source-input manifest, level-compatibility input, and runtime-history input scaffolds now pass the source-row-batch and parser-output authority objects through the active-trust routing path before consuming embedded source-input maps.

Two stale source-input helper methods that returned the coarse bundle-level source-row-batch contract/set hashes as per-role authority were removed so future audits cannot mistake them for an active authority route.

## Guardrail

This scaffold remains inert. It introduces no parser/file replay execution path and does not run or authorize parser execution, file replay, diagnostics, tests/backtests, OOS, Lockbox, Forward, provider/API calls, downloads, Git actions, adapter work, deployment, trading, promotion, result interpretation, or source-faithful replay evidence claims.

## Next Required Check

Run a local hostile audit under the consolidated scaffold-routing loop to verify:

- source-input selection no longer self-authenticates source-row-batch authority;
- source-row-batch authority is derived from a validated `SourceRowBatchSetContract` that itself binds parser-output authority;
- downstream source-input manifest, level-compatibility, and runtime-history routes pass those authority objects rather than reverting to fail-closed no-argument validation or caller-supplied maps;
- no execution surface or forbidden stage transition was introduced.
