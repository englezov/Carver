# S27 ZN V2 Replay Builder Plan Construction-Order Hardening Record

Date: 2026-06-08

Status:

```text
PROCESS_ONLY_S27_ZN_V2_REPLAY_BUILDER_PLAN_CONSTRUCTION_ORDER_HARDENING_RECORD_NOT_REPLAY_EVIDENCE
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

This record preserves a narrow inert scaffold-construction patch. It authorizes no provider/API access, no downloads, no parser/file replay execution, no source-data file reads or parsing, no diagnostics, no tests/backtests, no OOS, no Lockbox, no Forward, no Git actions, no adapter work, no deployment, no trading, no promotion, no result interpretation, no PnL/result evaluation, and no source-faithful replay evidence claim.

## Patch Scope

Patched module:

```text
src/carver/spine/s27_v2_replay/replay_builder_plan.py
```

The patch hardens the inert replay-builder plan so it must bind to the already locked construction scaffold constants in:

```text
src/carver/spine/s27_v2_replay/construction_contract.py
src/carver/spine/s27_v2_replay/constants.py
```

## Hardening Decisions

The builder plan now requires:

- construction step count and step labels to match the locked construction phase tuple exactly;
- each step index to match the locked step label at that position;
- ledger-emission artifact families to match the locked artifact tuple for that construction phase;
- each ledger-emission schema family to match the locked schema family for its artifact family;
- each ledger-emission output hash label to be locked as `<ARTIFACT_FAMILY>_HASH`;
- every locked artifact family to be covered exactly once across the builder plan;
- every unresolved fail-closed gate to be covered exactly once in locked order;
- standalone `ReplayLedgerEmissionPlan.validate()` to fail closed unless the emission is validated through a locked construction step.

This closes the scaffold gap where a builder plan could previously be merely ordered and syntactically hashed while still omitting, duplicating, or misplacing construction artifacts or fail-closed gates.

## Non-Execution Statement

The patch does not open files, enumerate directories, read source data, hash local data files, parse rows, select rows, construct replay rows, compute forecasts, compute desired positions, create orders, create fills, compute costs, compute PnL, construct validation ledgers, run audits, prepare external audit packets, run diagnostics, run tests/backtests, call providers/APIs, download data, stage or commit Git changes, perform adapter work, deploy, trade, promote, interpret results, or claim source-faithful replay evidence.

## Next Gate

This patch requires local hostile audit before it can be treated as a locally clean construction-scaffold slice.
