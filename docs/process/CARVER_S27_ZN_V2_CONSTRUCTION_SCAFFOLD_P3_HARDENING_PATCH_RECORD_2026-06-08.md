# S27 ZN V2 Construction Scaffold P3 Hardening Patch Record

Date: 2026-06-08

Status:

```text
PROCESS_ONLY_S27_ZN_V2_CONSTRUCTION_SCAFFOLD_P3_HARDENING_PATCH_NOT_REPLAY_EVIDENCE
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Authorization Boundary

Operator direction:

```text
Finish up first, then make a neater push.
```

This patch is limited to closing the two non-blocking P3 notes from the GPT Extended Pro construction-scaffold checkpoint external audit synthesis:

```text
docs/process/CARVER_S27_ZN_V2_CONSTRUCTION_SCAFFOLD_CHECKPOINT_EXTERNAL_AUDIT_SYNTHESIS_2026-06-08.md
```

This record authorizes no provider/API access, no downloads, no parser/file replay execution, no source-data file reads or parsing, no diagnostics, no tests/backtests, no OOS, no Lockbox, no Forward, no Git actions, no adapter work, no deployment, no trading, no promotion, no result interpretation, no PnL/result evaluation, and no source-faithful replay evidence claim.

## Patch Scope

Patched modules:

```text
src/carver/spine/s27_v2_replay/evidence_manifest.py
src/carver/spine/s27_v2_replay/file_contract.py
```

## P3-001 Closure

Prior note:

```text
EvidenceManifest.validate() permits extra active artifact types.
```

Patch:

`EvidenceManifest.validate()` now requires the active evidence artifact-type tuple to match `REQUIRED_EVIDENCE_MANIFEST_ARTIFACT_TYPES` exactly. This rejects omitted, duplicated, reordered, or extra active evidence artifact types before any trust-root matching helper consumes the manifest.

## P3-002 Closure

Prior note:

```text
Parser declarations lock parser names, not output-row-family mapping.
```

Patch:

`ParserSourceDeclaration` now carries `expected_output_row_families` and validates both:

- the parser-name-to-output-row-family label mapping;
- the parser-name-to-output-row-family tuple mapping.

The mapping is grouped where required:

- daily parser -> daily continuous and daily current-contract completed-bar rows;
- hourly parser -> hourly decision and hourly fill completed-bar rows;
- session parser -> session calendar rows;
- roll parser -> roll calendar rows;
- cost parameter parser -> cost parameter rows.

`ReplayInputDirectoryDeclaration.validate()` now also flattens parser-declared output row families and requires that flattened tuple to match the locked row-family tuple exactly.

## Non-Execution Statement

The patch does not implement a parser, open files, enumerate directories, read source data, hash local data files, parse rows, select rows, construct replay rows, compute forecasts, compute desired positions, create orders, create fills, compute costs, compute PnL, construct validation ledgers, run audits, prepare external audit packets, run diagnostics, run tests/backtests, call providers/APIs, download data, stage or commit Git changes, perform adapter work, deploy, trade, promote, interpret results, or claim source-faithful replay evidence.

## Next Gate

This patch requires local hostile audit before the P3 notes can be treated as locally closed.
