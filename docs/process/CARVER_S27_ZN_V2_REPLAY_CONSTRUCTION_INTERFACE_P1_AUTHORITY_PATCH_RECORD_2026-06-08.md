# S27 ZN V2 Replay Construction Interface P1 Authority Patch Record

Date: 2026-06-08

Status:

```text
PROCESS_ONLY_S27_ZN_V2_REPLAY_CONSTRUCTION_INTERFACE_P1_AUTHORITY_PATCH_RECORD_NOT_PIPELINE_AUTHORIZATION
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Trigger

GPT Extended Pro returned `FAIL` on the replay construction-interface external hostile audit with two P1 phase-boundary authority omissions and one P3 planned-evidence hardening note.

The external fail synthesis is:

```text
docs/process/CARVER_S27_ZN_V2_REPLAY_CONSTRUCTION_INTERFACE_EXTERNAL_AUDIT_FAIL_SYNTHESIS_2026-06-08.md
```

## Code Patch

Patched:

```text
src/carver/spine/s27_v2_replay/construction_interfaces.py
src/carver/spine/s27_v2_replay/artifact_manifest_plan.py
```

## P1-001 Closure

`RUNTIME_HISTORY_CONSTRUCTION` now requires:

```text
SOURCE_INPUT_MANIFEST_HASH
DAILY_HOURLY_CONTINUOUS_LEVEL_COMPATIBILITY_LEDGER_HASH
SOURCE_ROW_BATCH_SET_HASH
ROW_LOCATOR_HASH
SESSION_CALENDAR_POLICY_HASH
ROLL_CALENDAR_POLICY_HASH
CONSTRUCTION_PHASE_CONTRACT_HASH
BUILDER_STEP_PLAN_HASH
```

The non-anchor input hashes must match the corresponding `ConstructionPhaseBoundary.required_input_hashes`.

## P1-002 Closure

`FILL_CONSTRUCTION` now requires:

```text
SOURCE_INPUT_MANIFEST_HASH
LIMIT_ORDER_LEDGER_HASH
MARKET_ORDER_LEDGER_HASH
WORKING_ORDER_TRANSITION_LEDGER_HASH
REMAINING_LIMIT_ORDER_LEDGER_HASH
CANCELED_LIMIT_ORDER_LEDGER_HASH
SOURCE_ROW_SELECTION_AUTHORITY_HASH
SESSION_CALENDAR_POLICY_HASH
CONSTRUCTION_PHASE_CONTRACT_HASH
BUILDER_STEP_PLAN_HASH
```

The fill phase therefore binds both the source-input manifest artifact and source-row-selection authority before fill construction-interface validation can pass.

## Builder-Plan Binding

For every construction step ledger emission, `ReplayConstructionInterfaceBundle.validate()` now requires:

```text
emission.required_input_hashes == phase_contract.required_input_hashes
```

This keeps the construction-interface phase bindings, construction phase boundary, and trusted replay builder plan aligned.

## P3 Closure

`PlannedEvidenceManifest.validate()` now requires the active planned evidence artifact-type tuple to match:

```text
REQUIRED_EVIDENCE_MANIFEST_ARTIFACT_TYPES
```

This rejects required-plus-extra active planned artifacts and aligns planned evidence semantics with runtime `EvidenceManifest` exact active coverage.

## Non-Authorization

This patch authorizes no provider/API access, no downloads, no reading/parsing source data files, no parser/file replay execution, no diagnostics, no tests/backtests, no OOS/Lockbox/Forward, no Git actions, no adapter work, no deployment, no trading, no promotion, no result interpretation, and no source-faithful replay evidence claim.
