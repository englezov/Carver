# S27 ZN V2 Parser/File Replay Planning Code Scaffolding Local Audit Result

Date: 2026-06-06

Status:

```text
PROCESS_ONLY_S27_ZN_V2_PARSER_FILE_REPLAY_PLANNING_CODE_SCAFFOLDING_LOCAL_AUDIT_RESULT_NOT_EXECUTION_OR_BACKTEST_AUTHORIZATION
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Scope

Audit scope supplied by the operator:

```text
You are the local hostile-audit subagent for the Carver workspace. Scope is read-only/static only. Do not edit files. Do not run provider/API calls, downloads, parser/file replay execution, diagnostics, tests, backtests, OOS/Lockbox/Forward access, git actions, adapter work, deployment, trading, or promotion. Do not import/compile/execute Python. Task: audit only the S27_V2 parser/file replay planning code scaffolding in C:\Users\apops\Desktop\Carver.
```

This record documents a static source audit only. It authorizes no provider/API calls, no downloads, no parser/file replay execution, no diagnostics, no tests/backtests, no OOS, no Lockbox, no Forward, no Git actions, no adapter work, no deployment, no trading, no promotion, no result interpretation, and no source-faithful replay evidence claim.

Python import, compile, unit tests, parser execution, file replay, diagnostics, and backtests were intentionally not run.

## Governance Read

Required governance files were read before the audit:

```text
README.md
docs/mission/CARVER_SOURCE_NATIVE_RESEARCH_CHARTER_2026-05-28.md
docs/process/CLEAN_WORKSPACE_MIGRATION_RECORD_2026-05-28.md
docs/process/LANE_CLASSIFICATION_AND_ADAPTER_QUARANTINE_RULES_2026-05-28.md
```

Governing planning artifact:

```text
docs/process/CARVER_S27_ZN_V2_PARSER_FILE_REPLAY_IMPLEMENTATION_PLANNING_2026-06-06.md
```

Scaffolding record:

```text
docs/process/CARVER_S27_ZN_V2_PARSER_FILE_REPLAY_PLANNING_CODE_SCAFFOLDING_RECORD_2026-06-06.md
```

## Files Audited

```text
src/carver/spine/s27_v2_replay/file_contract.py
src/carver/spine/s27_v2_replay/parser_plan.py
src/carver/spine/s27_v2_replay/replay_config.py
src/carver/spine/s27_v2_replay/replay_builder_plan.py
src/carver/spine/s27_v2_replay/artifact_manifest_plan.py
src/carver/spine/s27_v2_replay/__init__.py
src/carver/spine/s27_v2_replay/constants.py
```

Package file count observed:

```text
24
```

## Findings

No P0/P1/P2/P3 findings were found in this narrow static scope.

## Audit Answers

1. Inert structural planning dataclasses/validators only:

```text
PASS
```

Evidence:

- `file_contract.py` defines local file, raw source file, parser source, runtime dependency, and replay input directory declarations at lines 10, 40, 56, 72, and 86.
- `parser_plan.py` defines parser-family and parser-plan bundle structures at lines 8, 42, 52, 62, 72, 82, and 92.
- `replay_config.py` defines replay-window, policy-hash, authorization-boundary, and planning-config structures at lines 18, 36, 78, and 89.
- `replay_builder_plan.py` defines fail-closed gate, ledger emission, construction step, and builder plan structures at lines 10, 24, 40, and 62.
- `artifact_manifest_plan.py` defines planned evidence artifact, planned evidence manifest, and artifact manifest plan structures at lines 15, 31, and 57.

Static text scan found no file existence checks, content reads, directory enumeration, parser execution, replay execution, provider/API/download code, diagnostics, tests/backtests, subprocess/CLI, or result computation surface. The only `provider`/`download` scan hits were the explicit `NO_PROVIDER_API_NO_DOWNLOAD` assertion fields in `file_contract.py`, which are governance labels and guards, not provider/download code.

2. Package root remains fail-closed and does not export planning dataclasses as source-faithful evidence:

```text
PASS
```

Evidence:

- `__init__.py` imports only `S27_V2_REPLAY_NON_AUTHORIZATION`, `STRUCTURAL_SCHEMA_ONLY_NOT_SOURCE_EVIDENCE`, `ReplayExecutionBlocked`, and `build_trusted_replay_bundle` at lines 8 through 13.
- `__all__` remains limited to those four public symbols at lines 15 through 20.
- The root docstring states that row dataclasses in submodules are structural schemas only and are not source-faithful evidence unless a future trusted replay bundle emits them under the active trust root.

3. Planning surfaces are bound to the governing planning artifact:

```text
PASS
```

Evidence:

- File declarations and local-only no-provider/no-download assertions are represented in `file_contract.py`.
- Replay config binds `S27_V2_ZN`, `SOURCE_NATIVE_FUTURES`, `ZN`, input declarations, policy hashes, and `S27_V2_REPLAY_NON_AUTHORIZATION` in `replay_config.py`.
- Parser plans bind expected input artifact types, output row schema families, canonical row locator policy hash, completed-bar policy hash, strict-prior policy hash, duplicate/missing/degraded policy hashes, and fail-closed reason codes in `parser_plan.py`.
- Builder planning binds ordered construction steps, allowed ledger emissions, required input hashes, and unresolved blocked gates in `replay_builder_plan.py`.
- Artifact manifest planning binds active/superseded evidence status and required artifact-family coverage through `artifact_manifest_plan.py` and `constants.py`.

## Residual Risks And Gates

This was a read-only static audit only. It did not import, compile, execute, test, parse files, enumerate directories, recompute hashes, construct manifests, run replay, run diagnostics, run backtests, call providers/APIs, download data, access OOS/Lockbox/Forward, use Git, perform adapter work, deploy, trade, promote, interpret results, or prove source-faithful replay evidence.

The planning modules remain structural scaffolding until a future separately authorized parser/file replay implementation step constructs actual evidence under the trust root.

The next gate is an operator decision between:

```text
GPT_EXTENDED_PRO_EXTERNAL_HOSTILE_AUDIT_HANDOFF_FOR_PARSER_FILE_REPLAY_PLANNING_CODE_SCAFFOLD
```

or a separately authorized next parser/file replay implementation slice, still with no parser/file replay execution unless explicitly authorized.
