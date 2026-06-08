# S27 ZN V2 Replay Scaffolding Local Hostile Audit Authorization Gate

Date: 2026-06-06

Status:

```text
PROCESS_ONLY_S27_ZN_V2_REPLAY_SCAFFOLDING_LOCAL_HOSTILE_AUDIT_AUTHORIZATION_GATE_NOT_AUDIT_OR_REPLAY_AUTHORIZATION
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Purpose

This record defines the next operator gate after S27 V2 replay schema/code scaffolding.

The scaffolding package exists at:

```text
src/carver/spine/s27_v2_replay/
```

The scaffolding record is:

```text
docs/process/CARVER_S27_ZN_V2_REPLAY_SCHEMA_CODE_SCAFFOLDING_RECORD_2026-06-06.md
```

## Current State

The scaffolding package is schema-only and isolated from:

```text
src/carver/spine/s27_v2.py
```

Static text/file inspection recorded:

```text
ALL_EXPECTED_SCAFFOLD_FILES_PRESENT
NO_PROVIDER_API_DOWNLOAD_BACKTEST_DIAGNOSTIC_SUBPROCESS_CLI_FILE_OPEN_SURFACE_FOUND_BY_TEXT_SCAN
RUNNER_ENTRY_POINT_FAILS_CLOSED_WITH_ReplayExecutionBlocked
```

Python import/compile/test execution was intentionally not run under the schema/code scaffolding authorization.

## Next Narrow Authorization Text

If the operator wants to proceed, the next authorization should be explicit and narrow:

```text
Operator authorizes local hostile audit of S27_V2 replay schema/code scaffolding only, no provider/API, no downloads, no parser/file replay execution, no diagnostics, no backtests, no OOS/Lockbox/Forward, no git actions, no adapter work, no deployment, no trading, no promotion.
```

## Audit Scope

The local hostile audit should inspect:

- whether `src/carver/spine/s27_v2_replay/` remains isolated from old diagnostic S27 runners;
- whether `src/carver/spine/s27_v2.py` was left unchanged by scaffolding;
- whether all plan-named scaffold modules exist;
- whether exported symbols match actual modules;
- whether schemas mirror the approved provenance design;
- whether `build_trusted_replay_bundle` fails closed;
- whether any parser/file replay, provider/API, download, diagnostic, backtest, OOS, Lockbox, Forward, Git, adapter, deployment, trading, promotion, or result-interpretation surface was introduced;
- whether unresolved source-faithfulness gates remain explicit fail-closed labels.

## Non-Authorization

This record does not authorize:

- local hostile audit execution;
- Python import/compile/test execution;
- provider/API calls;
- downloads;
- credential use;
- parser execution;
- file replay;
- diagnostics;
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
- tuning after results.

Any transition beyond this process gate requires separate explicit operator authorization.
