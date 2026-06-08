# S27 ZN V2 File Declaration Construction Scaffold Record

Date: 2026-06-08

Status:

```text
PROCESS_ONLY_S27_ZN_V2_FILE_DECLARATION_CONSTRUCTION_SCAFFOLD_NOT_REPLAY_EVIDENCE
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

This record preserves a narrow inert file-declaration scaffold patch. It authorizes no provider/API access, no downloads, no parser/file replay execution, no source-data file reads or parsing, no diagnostics, no tests/backtests, no OOS, no Lockbox, no Forward, no Git actions, no adapter work, no deployment, no trading, no promotion, no result interpretation, no PnL/result evaluation, and no source-faithful replay evidence claim.

## Patch Scope

Patched module:

```text
src/carver/spine/s27_v2_replay/file_contract.py
```

Reference locks:

```text
src/carver/spine/s27_v2_replay/row_locator_contract.py
src/carver/spine/s27_v2_replay/constants.py
```

## Hardening Decisions

The file-declaration scaffold now requires:

- local file declarations to remain declaration-only;
- raw source file declarations to remain declaration-only;
- parser source declarations to remain declaration-only;
- runtime dependency declarations to remain declaration-only;
- replay input directory declarations to remain declaration-only;
- local file expected row families to be members of the locked row-locator family tuple;
- replay input directory raw source file declarations to match the locked row-family tuple exactly;
- parser source declarations to be unique and match the locked parser-source tuple exactly;
- replay input directory declarations to preserve S27 V2 replay non-authorizations.

This closes the scaffold gap where a future replay input directory declaration could be structurally valid while omitting, duplicating, reordering, or substituting local row-family declarations.

## Non-Execution Statement

The patch does not open files, enumerate directories, read source data, hash local data files, parse rows, select rows, construct replay rows, compute forecasts, compute desired positions, create orders, create fills, compute costs, compute PnL, construct validation ledgers, run audits, prepare external audit packets, run diagnostics, run tests/backtests, call providers/APIs, download data, stage or commit Git changes, perform adapter work, deploy, trade, promote, interpret results, or claim source-faithful replay evidence.

## Next Gate

This patch requires local hostile audit before it can be treated as a locally clean construction-scaffold slice.
