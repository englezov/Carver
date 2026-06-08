# S27 ZN V2 Parser/File Replay Pre-Implementation Planning Slice

Date: 2026-06-08

Status:

```text
PROCESS_ONLY_S27_ZN_V2_PARSER_FILE_REPLAY_PRE_IMPLEMENTATION_PLANNING_SLICE_NOT_PIPELINE_AUTHORIZATION
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Authorization Scope

This record was created after the operator authorized the next inert parser/file replay pre-implementation planning slice, following:

```text
OPUS_ALTERNATE_CONSTRUCTION_INTERFACE_EXTERNAL_REAUDIT_PASS
GPT_REGULAR_CONSTRUCTION_INTERFACE_CORROBORATING_PASS
```

The corroborating packet hash was:

```text
4FDCC8D8A92E66AE7225909CFE4BB4FFA44BA5BCE511ACD41E06EEC33D202B34
```

This is a planning artifact only. It identifies the minimum remaining non-executing scaffold needed before any actual parser/file replay implementation authorization.

## Current Audited Base

The current S27 V2 base has the following inert, audited scaffold layers:

- book source lock and non-forgeable provenance design;
- trust-root and evidence-manifest scaffolds;
- contract/input authority routing chain;
- canonical serialization policy scaffold;
- file declaration and parser-source declaration scaffold;
- replay planning config;
- parser plan bundle;
- parser/file replay construction contract;
- trusted replay builder plan;
- artifact manifest plan;
- replay construction interface bundle;
- fail-closed runner boundary.

The construction-interface P1 authority patch is externally clean for its narrow scope based on Opus alternate external `PASS`, with regular GPT corroborating `PASS`.

## Minimal Remaining Scaffold Before Actual Implementation

One final non-executing implementation-boundary scaffold is sufficient before asking for actual parser/file replay implementation authorization.

That scaffold should be:

```text
S27_V2_PARSER_FILE_REPLAY_IMPLEMENTATION_BOUNDARY_AND_PHASE_REGISTRY
```

It should remain inert and should not read files, parse rows, construct ledgers, run tests, or emit replay artifacts.

The scaffold should define:

1. A parser/file replay execution authorization boundary object.
2. A phase-to-builder registry locked to `PLANNED_CONSTRUCTION_PHASES`.
3. A required-builder-surface map for the future implementation.
4. A rule that every future builder surface must receive the validated `ReplayConstructionInterfaceBundle` or a validated derivative authority object.
5. A rule that every future builder surface must raise the existing fail-closed replay exception unless explicit future parser/file replay implementation authorization is present.
6. A rule that local file read/parsing permission is separate from declaration-only file metadata.
7. A rule that any emitted artifact hash in future implementation must trace to the corresponding construction-interface output declaration.

This boundary is intentionally smaller than another full contract layer. Its job is to prevent the future implementation from bypassing the already-audited scaffolds.

## Builder Surface Map

Future implementation surfaces should map one-to-one to the locked construction phases:

```text
CANONICAL_SERIALIZATION_AND_HASH_POLICY_VALIDATION
FILE_DECLARATION_AND_RAW_FILE_HASH_SET_BINDING
SOURCE_UNIVERSE_AND_ROW_LOCATOR_CONSTRUCTION
DAILY_HOURLY_LEVEL_COMPATIBILITY_CONSTRUCTION
RUNTIME_HISTORY_CONSTRUCTION
FORECAST_AND_DESIRED_POSITION_CONSTRUCTION
ORDER_AND_TRANSITION_CONSTRUCTION
FILL_CONSTRUCTION
COST_CONSTRUCTION
PNL_CONSTRUCTION
VALIDATION_PROVENANCE_EVIDENCE_MANIFEST_CONSTRUCTION
FINAL_TRUSTED_REPLAY_BUNDLE_ASSEMBLY
```

Each future surface must bind to the existing construction-interface phase input labels and planned output artifact families. The future implementation should not introduce a parallel phase order, parallel artifact family list, or parallel source authority map.

## What Actual Implementation Authorization Must Name

The next real implementation authorization must explicitly name:

- whether local source-data files may be opened and read;
- whether raw file hashes may be computed from file bytes;
- whether declared files may be parsed into local source-row dataclasses;
- whether parser-output batch contracts may be constructed from parsed rows;
- whether source-row batch ledgers and row-locator ledgers may be constructed;
- whether source-input manifest rows may be constructed;
- whether level-compatibility ledgers may be constructed;
- whether runtime-history, forecast, position, order, fill, cost, PnL, validation, provenance, and evidence ledgers may be constructed;
- whether local verification tests may be run;
- whether output files may be written.

Absent explicit permission, all of those remain forbidden.

## Still Forbidden Here

This planning slice does not authorize:

- provider/API calls;
- downloads;
- reading/parsing source data files;
- parser/file replay execution;
- diagnostics;
- tests/backtests;
- OOS, Lockbox, or Forward access;
- Git actions;
- adapter work;
- deployment;
- trading;
- promotion;
- result interpretation;
- PnL/result evaluation;
- source-faithful replay evidence claims.

## Fail-Closed Gates To Preserve

Future code work must keep the following gates fail-closed until separately resolved or explicitly bound by future implementation authorization:

- Strategy 3 sigma source and sigma bridge;
- ZN tick rounding;
- working-limit lifecycle;
- overnight recompute and order reset;
- nonzero roll bridge;
- session calendar;
- roll calendar;
- commission policy;
- spread policy and spread-space arithmetic;
- multiplier and currency policy;
- capacity/speed interpretation;
- stale-evidence manifest supersession.

## Local Hostile Audit Questions For The Next Scaffold

When the implementation-boundary scaffold is added, the local hostile audit should ask:

1. Can any future builder surface run without an explicit parser/file replay implementation authorization object?
2. Can any file read or parser call occur through declaration-only file metadata?
3. Can any builder surface bypass `ReplayConstructionInterfaceBundle` authority?
4. Can any future artifact hash be accepted without matching the construction-interface output declaration for its phase?
5. Can a new phase, artifact family, parser family, or row family be introduced outside the locked tuples?
6. Does the scaffold preserve all non-authorizations and the existing fail-closed runner boundary?

## Recommended Next Authorization

The next useful gate is a narrow inert code-scaffold slice:

```text
S27_V2_PARSER_FILE_REPLAY_IMPLEMENTATION_BOUNDARY_AND_PHASE_REGISTRY_SCAFFOLD
```

That gate should allow only non-executing code scaffolding and local hostile audit for the implementation boundary and phase registry. It should not allow file reads, parsing, replay execution, diagnostics, tests/backtests, provider/API, downloads, Git actions, adapter work, deployment, trading, promotion, result interpretation, or source-faithful replay evidence claims.

## Non-Authorization

This record authorizes no provider/API access, no downloads, no reading/parsing source data files, no parser/file replay execution, no diagnostics, no tests/backtests, no OOS/Lockbox/Forward, no Git actions, no adapter work, no deployment, no trading, no promotion, no result interpretation, and no source-faithful replay evidence claim.
