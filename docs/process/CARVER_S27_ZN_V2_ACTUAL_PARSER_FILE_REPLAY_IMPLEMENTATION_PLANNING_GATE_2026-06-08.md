# S27 ZN V2 Actual Parser/File Replay Implementation Planning Gate

Date: 2026-06-08

Status:

```text
PROCESS_ONLY_S27_ZN_V2_ACTUAL_PARSER_FILE_REPLAY_IMPLEMENTATION_PLANNING_GATE_NOT_PIPELINE_AUTHORIZATION
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Purpose

This record defines the first consolidated implementation authorization needed to move from inert S27_V2 scaffolds into controlled local file/hash/parser/ledger construction work.

This record does not authorize that work. It only names the future permissions that must be explicitly granted.

## Current Entry Conditions

The next implementation gate may rely on these completed checkpoints:

- source-lock and provenance design records exist;
- contract/input authority routing chain is locally and externally audited for its scope;
- construction scaffold checkpoint passed external audit and local P3 hardening;
- construction-interface P1 authority patch passed Opus alternate external audit and regular GPT corroborating audit;
- implementation-boundary and phase-registry scaffold passed local hostile audit;
- `ReplayConstructionInterfaceBundle` remains the authority boundary for future builder surfaces;
- `ParserFileReplayImplementationBoundaryAndPhaseRegistry` remains fail-closed until actual implementation authorization is granted.

## First Consolidated Implementation Scope

The first real implementation gate should be named:

```text
S27_V2_LOCAL_ONLY_PARSER_FILE_REPLAY_IMPLEMENTATION_SLICE_1
```

It should be a consolidated gate, not another one-file-at-a-time authorization loop.

The gate should permit implementation code and local verification only for the first deterministic local-only replay construction path. It should remain ZN-only and S27_V2-only.

## Permissions The Future Gate Must Explicitly Grant

The future gate must explicitly grant these permissions if the operator wants the implementation to proceed:

1. Open and read only declared local input files named by `ReplayInputDirectoryDeclaration`.
2. Compute SHA256 hashes from the bytes of those declared local files.
3. Parse declared local daily/hourly/session/roll/cost rows into existing S27_V2 structural row dataclasses.
4. Construct parser-output batch contracts from parsed local rows.
5. Construct raw-file hash set, source-universe, source-row-batch, row-locator, and source-row-selection authority artifacts.
6. Construct source-input manifest rows and source-input manifest contract artifacts.
7. Construct daily/hourly level-compatibility ledger rows and contract artifacts.
8. Construct runtime-history, forecast, desired-position, order, transition, fill, cost, PnL, validation, provenance/hash, evidence-manifest, and trusted-bundle artifacts only as local deterministic replay construction outputs.
9. Run local verification tests limited to this S27_V2 local-only replay implementation slice.
10. Write output artifacts only under a declared S27_V2 local replay output path, with no OOS/Lockbox/Forward paths and no provider/download locations.

## Required Implementation Guards

The future implementation must:

- accept only a validated `ReplayConstructionInterfaceBundle` or a validated derivative authority object;
- keep the phase order locked to `PLANNED_CONSTRUCTION_PHASES`;
- keep future builder surface names locked to `REQUIRED_FUTURE_BUILDER_SURFACE_BY_PHASE`;
- keep phase inputs locked to `REQUIRED_INTERFACE_INPUT_LABELS_BY_PHASE`;
- keep artifact outputs locked to `REQUIRED_CONSTRUCTION_ARTIFACT_FAMILIES_BY_PHASE`;
- reject any undeclared file, undeclared parser, undeclared row family, or undeclared artifact family;
- preserve completed-bar and strict-prior policy bindings;
- preserve no-provider/no-download assertions;
- fail closed on source-level mismatch, stale evidence, unresolved policy hashes, row-family mismatch, duplicate rows, missing required rows, degraded rows not allowed by policy, unbound selected-row authority, or artifact hash mismatch;
- keep all source-faithfulness claims blocked until replay output is locally audited and externally audited.

## Implementation Order For Slice 1

The first consolidated implementation slice should proceed in this order:

1. Build local file byte hashing for declared files only.
2. Build parser entrypoints for declared parser families only, without provider/API/download fallback.
3. Build parser-output batch construction and row-family validation.
4. Build source-row batch and row-locator construction.
5. Build source-input selection and source-input manifest construction.
6. Build level-compatibility construction.
7. Build runtime-history construction.
8. Build forecast and desired-position construction.
9. Build order and transition construction.
10. Build fill construction.
11. Build cost construction.
12. Build PnL construction.
13. Build validation/provenance/evidence/trusted-bundle assembly.
14. Run local verification tests limited to the authorized slice.

The implementation can be done internally in sub-slices, but the operator authorization should be consolidated for the full local-only implementation slice to avoid repeated small gates.

## Still Excluded From The Future Gate

The first implementation gate should still exclude:

- provider/API calls;
- downloads;
- new data acquisition;
- OOS, Lockbox, or Forward access;
- backtests or result-scored runs;
- diagnostics outside local implementation verification;
- result interpretation;
- PnL/result evaluation;
- tuning;
- adapter work;
- deployment;
- trading;
- promotion;
- Git staging, commits, pushes, PRs.

## External Audit Position

External audit is not required before writing the first implementation slice because the construction-interface checkpoint has external support and the implementation-boundary scaffold has local hostile audit `PASS`.

However, after the first implementation slice is locally audited, a focused external hostile audit should inspect:

- implementation boundary preservation;
- local file/hash/parser restrictions;
- phase and artifact binding;
- fail-closed behavior;
- absence of provider/API/download/OOS/Lockbox/Forward/backtest/result surfaces.

## Recommended Consolidated Authorization Prompt

```text
Operator authorizes S27_V2_LOCAL_ONLY_PARSER_FILE_REPLAY_IMPLEMENTATION_SLICE_1, limited to controlled local-only implementation code and local verification for declared S27_V2 ZN input files under the audited construction-interface and implementation-boundary scaffolds.

This authorizes Codex to open and read only files declared by ReplayInputDirectoryDeclaration, compute SHA256 hashes for those declared local files, parse declared local daily/hourly/session/roll/cost rows into existing S27_V2 structural row dataclasses, construct parser-output batch contracts, raw-file hash set, source-universe, source-row-batch, row-locator, source-row-selection authority, source-input manifest, level-compatibility, runtime-history, forecast, desired-position, order, transition, fill, cost, PnL, validation, provenance/hash, evidence-manifest, and trusted-bundle artifacts as deterministic local replay construction outputs only.

This also authorizes local verification tests limited to this S27_V2 local-only implementation slice, local hostile audits with subagents after meaningful checkpoints, and narrowly scoped follow-up patches for local P0/P1/P2 findings inside this exact implementation scope.

This does not authorize provider/API access, downloads, new data acquisition, OOS/Lockbox/Forward access, backtests, result-scored runs, diagnostics outside local implementation verification, result interpretation, PnL/result evaluation, tuning, adapter work, deployment, trading, promotion, Git staging/commit/push/PR, or any source-faithful replay evidence claim until local and external audits explicitly pass.
```

## Non-Authorization

This planning gate authorizes no provider/API access, no downloads, no reading/parsing source data files, no parser/file replay execution, no diagnostics, no tests/backtests, no OOS/Lockbox/Forward, no Git actions, no adapter work, no deployment, no trading, no promotion, no result interpretation, and no source-faithful replay evidence claim.
