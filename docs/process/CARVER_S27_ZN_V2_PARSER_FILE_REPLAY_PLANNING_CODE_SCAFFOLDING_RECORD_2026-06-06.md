# S27 ZN V2 Parser/File Replay Planning Code Scaffolding Record

Date: 2026-06-06

Status:

```text
PROCESS_ONLY_S27_ZN_V2_PARSER_FILE_REPLAY_PLANNING_CODE_SCAFFOLDING_RECORD_NOT_EXECUTION_OR_BACKTEST_AUTHORIZATION
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Authorization Boundary

Operator authorization received:

```text
Operator authorizes S27_V2 parser/file replay planning code scaffolding only, no provider/API, no downloads, no parser/file replay execution, no diagnostics, no tests/backtests, no OOS/Lockbox/Forward, no git actions, no adapter work, no deployment, no trading, no promotion.
```

This record documents narrow parser/file replay planning code scaffolding only. It authorizes and performed no provider/API calls, no downloads, no parser/file replay execution, no diagnostics, no tests/backtests, no OOS, no Lockbox, no Forward, no Git actions, no adapter work, no deployment, no trading, no promotion, no result interpretation, and no source-faithful replay evidence claim.

Python import, compile, unit tests, parser execution, file replay, diagnostics, and backtests were intentionally not run.

## Governing Planning Artifact

```text
docs/process/CARVER_S27_ZN_V2_PARSER_FILE_REPLAY_IMPLEMENTATION_PLANNING_2026-06-06.md
```

## Added Files

```text
src/carver/spine/s27_v2_replay/file_contract.py
src/carver/spine/s27_v2_replay/parser_plan.py
src/carver/spine/s27_v2_replay/replay_config.py
src/carver/spine/s27_v2_replay/replay_builder_plan.py
src/carver/spine/s27_v2_replay/artifact_manifest_plan.py
```

Package file count after scaffolding:

```text
24
```

## Scaffolding Summary

`file_contract.py` adds inert declarations for:

- local file declarations;
- raw source file declarations;
- parser source declarations;
- runtime dependency declarations;
- replay input directory declarations.

These declarations validate strings and hashes only. They do not verify file existence, inspect directories, open files, parse files, call providers, download data, or run replay.

`replay_config.py` adds inert declarations for:

- replay window declaration;
- replay policy hash set;
- replay authorization boundary;
- S27 replay planning config.

The config binds strategy id `S27_V2_ZN`, lane `SOURCE_NATIVE_FUTURES`, instrument `ZN`, policy hashes, input declarations, and the non-authorization tuple. It is not a replay request.

`parser_plan.py` adds inert parser-intent declarations for:

- daily completed-bar parser plan;
- hourly completed-bar parser plan;
- session calendar parser plan;
- roll calendar parser plan;
- cost parameter parser plan;
- parser plan bundle.

These plans bind expected input/output families and policy hashes. They do not implement parsing.

`replay_builder_plan.py` adds inert declarations for:

- fail-closed gate plans;
- ledger emission plans;
- construction step plans;
- trusted replay builder plan.

These structures plan ordering and required hashes only. They do not build or execute replay.

`artifact_manifest_plan.py` adds inert declarations for:

- planned evidence artifacts;
- planned evidence manifest;
- artifact manifest plan.

The planned manifest requires active evidence status for active artifacts, superseded evidence status for superseded artifacts, unique active artifact types, and required artifact-family coverage.

## Public Boundary

Package-root exports were not widened.

The package root remains limited to:

```text
ReplayExecutionBlocked
S27_V2_REPLAY_NON_AUTHORIZATION
STRUCTURAL_SCHEMA_ONLY_NOT_SOURCE_EVIDENCE
build_trusted_replay_bundle
```

`build_trusted_replay_bundle()` remains the public fail-closed runner boundary and still requires separate authorization before parser/file replay execution can exist.

## Static Inspection Result

Static inspection performed:

```text
STATIC_TEXT_AND_FILE_INVENTORY_ONLY
```

Inspection found:

```text
EXPECTED_PLANNING_MODULES_PRESENT
PLANNING_DATACLASS_MARKERS_PRESENT
PACKAGE_ROOT_EXPORTS_NOT_WIDENED
NO_PROVIDER_API_DOWNLOAD_BACKTEST_DIAGNOSTIC_SUBPROCESS_CLI_FILE_OPEN_SURFACE_FOUND_BY_TEXT_SCAN
```

No parser execution, file replay, diagnostics, tests/backtests, provider/API calls, downloads, OOS, Lockbox, Forward, Git actions, adapter work, deployment, trading, promotion, result interpretation, or source-faithful replay evidence claim was performed.

## Next Gate

The standing local hostile-audit pre-approval rule permits a local hostile audit of this narrow parser/file replay planning code scaffolding.

Any external audit handoff, parser/file replay execution, diagnostics, tests/backtests, data access, OOS, Lockbox, Forward, Git actions, adapter work, deployment, trading, promotion, result interpretation, or source-faithful replay evidence claim still requires its own proper gate.
