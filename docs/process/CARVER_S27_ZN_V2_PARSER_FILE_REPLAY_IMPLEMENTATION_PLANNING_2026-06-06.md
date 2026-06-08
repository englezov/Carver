# S27 ZN V2 Parser/File Replay Implementation Planning

Date: 2026-06-06

Status:

```text
PROCESS_ONLY_S27_ZN_V2_PARSER_FILE_REPLAY_IMPLEMENTATION_PLANNING_NOT_EXECUTION_OR_BACKTEST_AUTHORIZATION
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Authorization Boundary

Operator authorization received:

```text
operator authorizes parser/file replay implementation planning
```

This artifact is process-only parser/file replay implementation planning. It authorizes no provider/API calls, no downloads, no parser/file replay execution, no diagnostics, no tests/backtests, no OOS, no Lockbox, no Forward, no Git actions, no adapter work, no deployment, no trading, no promotion, and no result interpretation.

This planning artifact does not authorize code edits beyond process documentation.

## Gate Evidence

The prior scaffold external re-audit passed:

```text
docs/process/CARVER_S27_ZN_V2_GPT_P2_EXTERNAL_AUDIT_FINDING_PATCH_EXTERNAL_REAUDIT_SYNTHESIS_2026-06-06.md
```

GPT gate decision:

```text
PARSER_FILE_REPLAY_IMPLEMENTATION_PLANNING_MAY_PROCEED
```

Boundary preserved:

```text
PARSER_FILE_REPLAY_EXECUTION_AND_SOURCE_FAITHFUL_REPLAY_EVIDENCE_CLAIMS_REMAIN_UNAUTHORIZED
```

## Current Scaffold Boundary

Current scaffold package:

```text
src/carver/spine/s27_v2_replay/
```

Current package file count:

```text
19
```

Current public runner boundary remains fail-closed:

```text
build_trusted_replay_bundle
```

It must continue to raise `ReplayExecutionBlocked` until a later operator authorization explicitly permits parser/file replay execution.

## Planning Objective

Plan the next implementation slice so that future code work can add parser/file replay construction surfaces without executing them.

The next implementation must make the trusted replay bundle buildable only from explicitly supplied local file paths, policies, and hashes, while keeping actual file parsing/replay execution behind a separate gate.

## Planned Module Additions

Future code authorization should add planning/scaffolding-only modules under:

```text
src/carver/spine/s27_v2_replay/
```

Planned modules:

```text
file_contract.py
parser_plan.py
replay_config.py
replay_builder_plan.py
artifact_manifest_plan.py
```

These modules must define inert dataclasses and validators only. They must not open files, glob directories, parse CSV/PDF/JSON, execute replay, call providers, download data, start subprocesses, run CLIs, or compute strategy results.

## Planned File Contract

`file_contract.py` should define structural rows for local-only input declarations:

```text
LocalFileDeclaration
RawSourceFileDeclaration
ParserSourceDeclaration
RuntimeDependencyDeclaration
ReplayInputDirectoryDeclaration
```

Required fields should include:

- declared path string;
- expected artifact type;
- expected SHA256 content hash;
- expected row family;
- expected raw symbol family where applicable;
- expected time zone policy hash;
- expected canonical serialization policy hash;
- operator-supplied authorization label;
- no-provider/no-download assertion label.

Validators may require non-empty paths and hashes. They must not verify file existence or read file contents under this planning authorization.

## Planned Replay Config

`replay_config.py` should define:

```text
S27ReplayPlanningConfig
ReplayWindowDeclaration
ReplayPolicyHashSet
ReplayAuthorizationBoundary
```

The config should bind:

- strategy id `S27_V2_ZN`;
- lane `SOURCE_NATIVE_FUTURES`;
- instrument `ZN`;
- requested local replay window labels;
- local-only source declarations;
- source lock hash;
- local data contract hash;
- provenance design hash;
- source universe manifest hash;
- raw file hash set hash;
- row locator hash;
- canonical serialization policy hashes;
- session and roll policy hashes;
- tick rounding policy hash or fail-closed unresolved status;
- commission/spread/multiplier/currency policy hashes;
- daily/hourly compatibility policy hash;
- active evidence manifest hash;
- non-authorization tuple.

This config is not a replay request and must not be interpreted as permission to access rows or run replay.

## Planned Parser Plan

`parser_plan.py` should define inert parser-intent structures:

```text
DailyParserPlan
HourlyParserPlan
SessionParserPlan
RollParserPlan
CostParameterParserPlan
ParserPlanBundle
```

Each plan should bind:

- parser/extractor source hash;
- expected input artifact types;
- expected output row schema family;
- canonical row locator policy hash;
- completed-bar policy hash;
- strict-prior policy hash;
- duplicate/missing/degraded row policy hashes;
- fail-closed reason codes.

The parser plan must not implement parsing. It is a contract for a future authorized parser implementation.

## Planned Replay Builder Plan

`replay_builder_plan.py` should define:

```text
TrustedReplayBuilderPlan
ReplayConstructionStepPlan
ReplayLedgerEmissionPlan
ReplayFailClosedGatePlan
```

The construction plan should order future implementation as:

1. canonical serialization/hash policy validation;
2. file declaration and raw file hash-set binding;
3. source universe and row locator construction;
4. daily/hourly level compatibility construction;
5. runtime history construction;
6. forecast and desired position construction;
7. order and transition construction;
8. fill construction;
9. cost construction;
10. PnL construction;
11. validation/provenance/evidence manifest construction;
12. final trusted replay bundle assembly.

Each step must name the structural schema outputs it is allowed to emit and the hash inputs it must bind.

## Planned Evidence Manifest Integration

`artifact_manifest_plan.py` should define the planned artifact families needed before execution authorization:

```text
SOURCE_LOCK
LOCAL_DATA_CONTRACT
PROVENANCE_DESIGN
RUNNER_IMPLEMENTATION
PARSER_EXTRACTOR_SOURCE
DEPENDENCY_RUNTIME_MANIFEST
REPLAY_CONFIG
SOURCE_INPUT_UNIVERSE_MANIFEST
RAW_SOURCE_FILE_HASH_SET
SOURCE_ROW_LOCATOR
CANONICAL_SERIALIZATION_SCHEMA
HASH_ALGORITHM_VERSION
DECIMAL_FLOAT_NORMALIZATION_POLICY
TIMEZONE_NORMALIZATION_POLICY
ROW_ORDERING_COLLATION_POLICY
SESSION_CALENDAR_POLICY
ROLL_CALENDAR_POLICY
TICK_ROUNDING_POLICY
COMMISSION_POLICY
SPREAD_UNIT_POLICY
CONTRACT_MULTIPLIER_CURRENCY_POLICY
DAILY_HOURLY_COMPATIBILITY_POLICY
```

The planned manifest must require `ACTIVE_EVIDENCE` for active entries and `SUPERSEDED_EVIDENCE` for superseded entries, matching the current scaffold.

## Required Fail-Closed Gates

Future code must preserve fail-closed gates for:

```text
BLOCKED_SOURCE_UNRESOLVED_CANONICAL_SERIALIZATION_AND_HASH_POLICY
BLOCKED_SOURCE_UNRESOLVED_NON_FORGEABLE_TRUST_ROOT
BLOCKED_SOURCE_UNRESOLVED_SOURCE_UNIVERSE_AND_ROW_LOCATOR_HASHES
BLOCKED_SOURCE_UNRESOLVED_DAILY_HOURLY_LEVEL_COMPATIBILITY_PROOF
BLOCKED_SOURCE_UNRESOLVED_FORECAST_HISTORY_STATE_HASHES
BLOCKED_SOURCE_UNRESOLVED_STRATEGY3_SIGMA_PROVENANCE
BLOCKED_SOURCE_UNRESOLVED_ZN_TICK_ROUNDING_POLICY
BLOCKED_SOURCE_UNRESOLVED_INITIAL_POSITION_POLICY
BLOCKED_SOURCE_UNRESOLVED_WORKING_LIMIT_LIFECYCLE
BLOCKED_SOURCE_UNRESOLVED_OVERNIGHT_RECOMPUTED_TARGET
BLOCKED_SOURCE_UNRESOLVED_NONZERO_ROLL_BRIDGE
BLOCKED_SOURCE_UNRESOLVED_TRUSTED_COST_ROW_AMOUNT_UNIT_SCHEMA
BLOCKED_SOURCE_UNRESOLVED_CAPACITY_SPEED_ELIGIBILITY
BLOCKED_SOURCE_UNRESOLVED_STALE_EVIDENCE_SUPERSESSION_MANIFEST
```

No planned module may resolve one of these gates by assumption.

## Planned Static Validation

After future planning-code scaffolding is authorized and implemented, static validation should check:

- no file-open/read/glob/path-enumeration surface;
- no provider/API/download surface;
- no parser execution surface;
- no replay execution surface;
- no diagnostics/backtest surface;
- no Git action surface;
- package-root exports remain fail-closed and structural-warning only;
- new planning dataclasses remain inert;
- current `build_trusted_replay_bundle()` still raises `ReplayExecutionBlocked`.

## Future Audit Checkpoint

After future planning-code scaffolding is authorized and implemented:

```text
LOCAL_HOSTILE_AUDIT_OF_PARSER_FILE_REPLAY_PLANNING_SCAFFOLD
```

That audit should inspect only static source and process records unless separately authorized otherwise.

## Next Required Authorization

The next step is not automatically authorized.

If the operator wants code scaffolding for this planning layer, the next authorization should be narrow:

```text
Operator authorizes S27_V2 parser/file replay planning code scaffolding only, no provider/API, no downloads, no parser/file replay execution, no diagnostics, no tests/backtests, no OOS/Lockbox/Forward, no git actions, no adapter work, no deployment, no trading, no promotion.
```

That authorization would still not permit parser execution, file replay, diagnostics, tests/backtests, OOS, Lockbox, Forward, provider/API calls, downloads, Git actions, adapter work, deployment, trading, promotion, result interpretation, or source-faithful replay evidence claims.
