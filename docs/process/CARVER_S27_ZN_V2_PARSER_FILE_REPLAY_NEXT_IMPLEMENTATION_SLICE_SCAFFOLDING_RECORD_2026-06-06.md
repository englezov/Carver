# S27 ZN V2 Parser/File Replay Next Implementation Slice Scaffolding Record

Date: 2026-06-06

Status:

```text
PROCESS_ONLY_S27_ZN_V2_PARSER_FILE_REPLAY_NEXT_IMPLEMENTATION_SLICE_SCAFFOLDING_NOT_EXECUTION_OR_BACKTEST_AUTHORIZATION
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Authorization Boundary

Operator authorization received:

```text
Operator authorizes S27_V2 parser/file replay next implementation slice scaffolding only, no provider/API, no downloads, no parser/file replay execution, no diagnostics, no tests/backtests, no OOS/Lockbox/Forward, no git actions, no adapter work, no deployment, no trading, no promotion.
```

This record documents only a narrow inert construction-contract scaffolding slice.

It authorizes no provider/API calls, no downloads, no parser execution, no file replay, no diagnostics, no tests/backtests, no OOS, no Lockbox, no Forward, no Git actions, no adapter work, no deployment, no trading, no promotion, no result interpretation, and no source-faithful replay evidence claim.

## Gate Evidence

The prior parser/file replay planning code scaffold external audit synthesis is:

```text
docs/process/CARVER_S27_ZN_V2_PARSER_FILE_REPLAY_PLANNING_CODE_SCAFFOLDING_EXTERNAL_AUDIT_SYNTHESIS_2026-06-06.md
```

GPT returned:

```text
PASS
```

The next implementation slice still required separate authorization, which is recorded above.

## Implemented Scaffolding

Added inert module:

```text
src/carver/spine/s27_v2_replay/construction_contract.py
```

The module defines:

```text
S27_V2_CONSTRUCTION_SCAFFOLD_ONLY_STATUS
PLANNED_CONSTRUCTION_PHASES
ConstructionArtifactReference
ConstructionPhaseBoundary
ParserFileReplayConstructionContract
```

## Purpose

This slice introduces a structural contract for future parser/file replay construction without implementing construction.

It locks the future construction phase order to:

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

The scaffolding validates only supplied metadata:

- phase index and phase label order;
- required input hashes;
- planned structural output artifact references;
- blocked source-unresolved gate statuses;
- construction contract hash;
- non-authorization tuple.

## Preserved Boundaries

The module does not:

- open files;
- read files;
- enumerate paths;
- glob directories;
- parse CSV/PDF/JSON;
- execute parser work;
- execute file replay;
- compute strategy rows;
- run diagnostics;
- run tests/backtests;
- call providers/APIs;
- download data;
- start subprocesses;
- invoke Git;
- access OOS, Lockbox, or Forward;
- perform adapter work;
- deploy, trade, promote, or interpret results.

Package-root exports were intentionally not widened. The package root still exposes only the fail-closed runner boundary and non-authorization/status warning constants.

## Next Gate

The next gate is a local hostile audit of this narrow construction-contract scaffolding slice.

That audit should be static/source-only unless the operator separately authorizes otherwise.

## Local Hostile Audit Result

The standing local hostile-audit pre-approval rule was applied to audit this narrow construction-contract scaffolding slice. The audit result is:

```text
docs/process/CARVER_S27_ZN_V2_PARSER_FILE_REPLAY_NEXT_IMPLEMENTATION_SLICE_SCAFFOLDING_LOCAL_AUDIT_RESULT_2026-06-06.md
```

The audit returned `PASS`: no P0/P1/P2/P3 findings. It confirmed the construction contract is inert structural scaffolding only, the package root remains fail-closed, no forbidden execution or IO surface was found, and the 12 construction phases are locked to the planning order with source-unresolved fail-closed guards.

The next possible implementation slice still requires separate explicit operator authorization.

## Static Text-Only Verification

Static text-only verification performed:

```text
STATIC_TEXT_AND_FILE_INVENTORY_ONLY
```

Package file count after this slice:

```text
25
```

Forbidden-surface scan:

```text
rg -n "open\(|read_csv|to_csv|requests|urllib|http|databento|download\(|download |backtest\(|diagnostic\(|subprocess|argparse|if __name__|Path\(|glob\(|os\.|sys\.|socket|git|pytest|unittest" src\carver\spine\s27_v2_replay
```

Result:

```text
NO_MATCHES
```

Package-root export check:

```text
NO_CONSTRUCTION_CONTRACT_EXPORT_FROM_PACKAGE_ROOT
```

No import, compile, test, parser execution, file replay, diagnostics, provider/API call, download, OOS, Lockbox, Forward, Git action, adapter work, deployment, trading, promotion, result interpretation, or source-faithful replay evidence claim was performed.

## Non-Authorizations

This record does not authorize:

- provider/API calls;
- downloads;
- credential use;
- parser execution;
- file replay;
- diagnostics;
- tests;
- backtests;
- OOS access;
- Lockbox access;
- Forward access;
- Git staging;
- Git commits;
- Git pushes;
- PRs;
- adapter work;
- deployment;
- trading;
- promotion;
- tuning after results;
- result interpretation;
- source-faithful replay evidence claims.

Any transition beyond this scaffolding slice requires separate explicit operator authorization.
