# S27_V2 Local-Only Parser/File Replay Implementation Slice 5 Record

Date: 2026-06-08

Status:

```text
LOCAL_ONLY_SLICE5_IMPLEMENTED_LOCAL_AND_EXTERNAL_HOSTILE_AUDIT_PASS
```

## Scope

Operator authorization allowed the next narrow S27_V2 local-only parser/file replay implementation slice after external PASS on Slice 4.

This slice is limited to controlled local-only downstream construction scaffolding from audited order/transition outputs toward:

- fill input construction;
- inert fill contract construction.

## Implemented Files

```text
src/carver/spine/s27_v2_replay/local_replay.py
tests/test_s27_v2_local_replay_slice1.py
```

## Constructed Artifact Surface

The new local-only builder is:

```text
build_local_parser_file_replay_slice5(...)
```

It constructs:

```text
LocalParserFileReplaySlice5Artifacts
FillInputContractBundle
FillContractBundle
```

## Authority Binding

Fill input authority is derived from the active Slice 4 order input and order contract, plus the active source-input manifest hourly-fill selected-row authority.

The local-only validators recompute active expected-source maps and dependency chains from the upstream objects. They do not treat caller-supplied expected maps, policy hashes, or dependency hashes as authority.

The fill contract binds:

- active order contract bundle hash;
- source-input manifest hash;
- limit-order ledger schema;
- market-order ledger schema;
- working-order transition schema;
- fill input policy hash;
- fill component, price-provenance, branch, invariant, and bundle hashes.

## Inert Boundary

This slice constructs contract and planned-output schema artifacts only.

It does not execute parser/file replay beyond the previously authorized local slice path, does not execute fills, does not score results, does not calculate PnL, does not run a backtest, and does not claim source-faithful replay evidence.

Public fill input `validate()` remains fail-closed without required order and source-row authority.

## Local Verification

Focused local verification:

```text
python -m py_compile src\carver\spine\s27_v2_replay\local_replay.py tests\test_s27_v2_local_replay_slice1.py
python -m pytest tests\test_s27_v2_local_replay_slice1.py -q
```

Result:

```text
43 passed
```

## Non-Authorizations

This record does not authorize provider/API access, downloads, new data acquisition, OOS, Lockbox, Forward, backtests, result-scored runs, diagnostics outside local verification, result interpretation, PnL/result evaluation, tuning, adapter work, deployment, trading, promotion, Git staging, Git commit, Git push, PRs, or source-faithful replay evidence claims.
