# S27 ZN V2 Replay Construction Interface Scaffold Record

Date: 2026-06-08

Status:

```text
PROCESS_ONLY_S27_ZN_V2_REPLAY_CONSTRUCTION_INTERFACE_SCAFFOLD_RECORD_NOT_PIPELINE_AUTHORIZATION
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Operator Authorization

The operator authorized the next S27_V2 inert local-row replay construction scaffold slice only, limited to non-executing construction interfaces and contract-binding hardening after the pushed scaffold checkpoint.

The authorization explicitly excluded provider/API access, downloads, reading/parsing source data files, parser/file replay execution, diagnostics, tests/backtests, OOS/Lockbox/Forward, Git actions, adapter work, deployment, trading, promotion, result interpretation, and any source-faithful replay evidence claim.

## Patch Scope

Added:

```text
src/carver/spine/s27_v2_replay/construction_interfaces.py
```

The new scaffold defines inert construction-interface contracts for the already locked replay construction phase tuple. It does not expose a runner, file reader, parser, replay loop, diagnostic, test, backtest, result surface, adapter, deployment hook, or trading surface.

## Binding Behavior

`ReplayConstructionInterfaceBundle` validates against already-declared scaffold authorities:

- `S27ReplayPlanningConfig`
- `ParserFileReplayConstructionContract`
- `TrustedReplayBuilderPlan`
- `ArtifactManifestPlan`

It derives active input hashes from those validated objects rather than from caller-supplied active maps. Phase-local construction phase contract hashes and builder step plan hashes are injected only for the matching locked phase. Planned output artifact hashes are derived from `ParserFileReplayConstructionContract.construction_phases`.

Standalone validation of `ReplayConstructionInputBinding`, `ReplayConstructionOutputDeclaration`, and `ReplayConstructionPhaseInterface` fails closed. The only authoritative validation route is through `ReplayConstructionInterfaceBundle.validate()`, which derives the active authority context from validated upstream scaffold objects before calling internal bundle-authority helpers.

Each `ReplayConstructionPhaseInterface` must match:

- the locked phase index and phase label;
- the locked input-label tuple for that phase;
- active input hashes derived from upstream scaffold authorities;
- the exact required input-hash tuple declared by the matching `ConstructionPhaseBoundary`, excluding phase-local interface anchors for the phase contract and builder step plan;
- the exact required input-hash tuple declared by each matching builder ledger emission;
- the locked planned output artifact family tuple for that phase;
- planned output artifact hashes derived from construction-contract artifact references.

After the first GPT Extended Pro external audit, the phase input tuple was hardened so:

- runtime-history construction must bind the produced level-compatibility artifact;
- fill construction must bind the source-input manifest artifact and source-row-selection authority;
- planned active evidence artifact types must match the locked required tuple exactly.

## Non-Authorization Preservation

The scaffold preserves:

```text
S27_V2_REPLAY_NON_AUTHORIZATION
```

This record authorizes no execution, no data access, no replay evidence, and no result interpretation.

## Current Status

The construction-interface scaffold has been added but has not been locally hostile audited or externally audited under this record.

Next authorized checkpoint should be a local hostile audit of this inert construction-interface scaffold before further construction-interface expansion or external handoff.
