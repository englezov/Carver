# S27 ZN V2 Canonical Serialization Construction Scaffold Record

Date: 2026-06-08

Status:

```text
PROCESS_ONLY_S27_ZN_V2_CANONICAL_SERIALIZATION_CONSTRUCTION_SCAFFOLD_NOT_REPLAY_EVIDENCE
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Authorization Boundary

Operator authorization:

```text
Operator authorizes the next consolidated S27_V2 parser/file replay implementation scaffold phase, after full scaffold-routing external PASS, limited to inert local-row replay construction code scaffolding and contract-binding hardening only.
```

This record preserves a narrow inert canonical-serialization scaffold patch. It authorizes no provider/API access, no downloads, no parser/file replay execution, no source-data file reads or parsing, no diagnostics, no tests/backtests, no OOS, no Lockbox, no Forward, no Git actions, no adapter work, no deployment, no trading, no promotion, no result interpretation, no PnL/result evaluation, and no source-faithful replay evidence claim.

## Patch Scope

Patched modules:

```text
src/carver/spine/s27_v2_replay/canonical_hash.py
src/carver/spine/s27_v2_replay/constants.py
src/carver/spine/s27_v2_replay/evidence_manifest.py
src/carver/spine/s27_v2_replay/replay_config.py
```

## Hardening Decisions

The canonical serialization scaffold now requires structural authority for:

- canonical serialization schema;
- hash algorithm version;
- field ordering policy;
- decimal/float normalization policy;
- timezone normalization policy;
- row ordering/collation policy;
- null/missing sentinel policy;
- string encoding policy;
- hash payload version policy;
- the canonical serialization policy hash itself.

`CanonicalSerializationPolicy.validate()` remains structural and fail-closed. It does not serialize payloads, compute source-row hashes, read files, parse rows, or construct replay data.

`CanonicalRowHashContract.validate()` now fails closed unless the row-hash contract is validated against an active `CanonicalSerializationPolicy`. The active-policy route binds:

- canonical serialization policy hash;
- field ordering policy hash;
- hash payload version policy hash.

`S27ReplayPlanningConfig.validate()` now rejects raw source file declarations whose canonical serialization policy hash differs from the active replay policy hash.

`EvidenceManifest` active evidence requirements now include the new canonical policy/component artifact types and `require_evidence_manifest_matches_trust_root(...)` requires those active evidence hashes to match the `ReplayTrustRoot` canonical policy fields.

## Non-Execution Statement

The patch does not implement a serializer, open files, enumerate directories, read source data, hash local data files, parse rows, select rows, construct replay rows, compute forecasts, compute desired positions, create orders, create fills, compute costs, compute PnL, construct validation ledgers, run audits, prepare external audit packets, run diagnostics, run tests/backtests, call providers/APIs, download data, stage or commit Git changes, perform adapter work, deploy, trade, promote, interpret results, or claim source-faithful replay evidence.

## Next Gate

This patch requires local hostile audit before it can be treated as a locally clean construction-scaffold slice.
