# S27 ZN V2 Level Compatibility Contract Scaffolding Local Audit Result

Date: 2026-06-06

Status:

```text
PROCESS_ONLY_S27_ZN_V2_LEVEL_COMPATIBILITY_CONTRACT_SCAFFOLDING_LOCAL_AUDIT_RESULT_NOT_PIPELINE_AUTHORIZATION
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Audit Scope

Local hostile audit performed by subagent:

```text
Hilbert
```

Audit target:

```text
src/carver/spine/s27_v2_replay/level_compatibility_contract.py
src/carver/spine/s27_v2_replay/level_compatibility.py
src/carver/spine/s27_v2_replay/__init__.py
docs/process/CARVER_S27_ZN_V2_LEVEL_COMPATIBILITY_CONTRACT_SCAFFOLDING_RECORD_2026-06-06.md
docs/process/CARVER_S27_ZN_V2_REPLAY_SCHEMA_CODE_SCAFFOLDING_RECORD_2026-06-06.md
docs/process/CARVER_S27_ZN_V2_TRUST_ROOT_DESIGN_CURRENT_STATE_AND_AUTHORIZATION_QUEUE_2026-06-06.md
```

Audit boundary:

```text
STATIC_SOURCE_ONLY
NO_EDITS
NO_IMPORT_COMPILE_TEST
NO_PARSER_FILE_REPLAY_EXECUTION
NO_DIAGNOSTICS
NO_BACKTESTS
NO_PROVIDER_API
NO_DOWNLOADS
NO_OOS_LOCKBOX_FORWARD
NO_GIT_ACTIONS
NO_ADAPTER_DEPLOYMENT_TRADING_PROMOTION
```

## Verdict

Hilbert returned:

```text
PASS_WITH_P2_REQUIRED_EDIT
```

Severity findings:

```text
P0: None
P1: None
P2: Verdict proof hashes were length-checked but not bound to supplied proof contracts.
P3: None
```

## Finding

`LevelCompatibilityContractBundle.validate()` checked that `verdict_contract.required_proof_contract_hashes` had the expected length, but did not require it to equal:

```text
tuple(proof.proof_contract_hash for proof in self.proof_contracts)
```

This left a narrow P2 metadata-binding gap: a caller-supplied verdict could reference arbitrary valid SHA256-shaped proof hashes rather than the actual supplied proof contracts.

## Non-Finding Confirmations

The audit confirmed:

- no P0/P1 finding;
- no provider/API/download/parser/replay/diagnostic/test/backtest/subprocess/Git surface;
- package root remains fail-closed and does not export level-compatibility contract classes;
- proof labels and reason codes are locked;
- no row comparison or bridge arithmetic is implemented.

## Gate Effect

The next step is a narrow patch of the P2 verdict-to-proof hash binding gap, followed by local hostile re-audit.

Parser/file replay execution, diagnostics, tests/backtests, provider/API calls, downloads, OOS, Lockbox, Forward, Git actions, adapter work, deployment, trading, promotion, result interpretation, and source-faithful replay evidence claims remain unauthorized.

## Non-Authorizations

This audit result does not authorize:

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

Any transition beyond this audit result requires separate explicit operator authorization.
