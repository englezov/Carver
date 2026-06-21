# S27 ZN V2 Executable Replay Ledger Phase 1 Fail-Closed Implementation Record

Date: 2026-06-08

Status:

```text
S27_V2_LOCAL_ONLY_EXECUTABLE_REPLAY_LEDGER_PHASE1_FAIL_CLOSED_IMPLEMENTED_NOT_RESULT
```

Authorization:

```text
S27_V2_LOCAL_ONLY_EXECUTABLE_REPLAY_LEDGER_IMPLEMENTATION_PHASE_1_FAIL_CLOSED
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Scope

This implementation adds a deterministic fail-closed executable replay-ledger
surface for S27_V2.

Implemented code:

```text
src/carver/spine/s27_v2_replay/executable_replay.py
```

Focused verification additions:

```text
tests/test_s27_v2_local_replay_slice1.py
```

The new surface consumes validated local construction objects and a controlled
construction run manifest. It emits in-memory fail-closed provenance,
validation, gate-row, and bundle dataclasses only.

It does not emit forecast rows, desired-position rows, order rows, transition
rows, fill rows, commission rows, spread-cost rows, PnL rows, scored-result
rows, backtest artifacts, source-faithful evidence, or promotion material.

## Implemented Guards

The phase 1 builder:

- recomputes active local construction artifacts from the input declaration and
  rejects stale construction artifacts;
- validates the controlled construction run manifest from manifest bytes, not a
  caller-supplied hash;
- binds manifest input-pack and construction-output paths to the executable
  bundle paths;
- validates manifest authorization, boundaries, non-authorizations,
  verification status, and row-family summary;
- requires the exact locked 34 construction artifact JSON files;
- verifies construction artifact byte SHA256 values under the controlled output
  directory;
- requires every construction artifact file to parse as a JSON object;
- binds key artifact JSON hashes back to active construction objects;
- binds full per-family row-hash tuples, not first-row-only hashes;
- requires each executable ledger gate to use the locked per-ledger blocker and
  reason mapping;
- requires the validation ledger unresolved-gate set to equal the exact union of
  gate-row blockers;
- blocks every executable result/evidence emission flag.

## Expected Phase 1 Outcome

For the current oldest local ZN development pack, the expected phase 1 outcome
remains:

```text
FAIL_CLOSED_EXECUTABLE_REPLAY_LEDGER_SURFACE_PASS_NO_RESULT
```

This means the machinery proves that it refuses to emit S27 forecast/order/fill
cost/PnL rows when required history or policy evidence is unresolved.

## Verification

Focused local verification:

```text
python -m pytest tests\test_s27_v2_local_replay_slice1.py -q
58 passed
```

Compile check:

```text
python -m compileall -q src\carver\spine\s27_v2_replay\executable_replay.py
PASS
```

## Non-Authorization

This record does not authorize provider/API access, downloads, new data
acquisition, OOS, Lockbox, Forward, backtests, result-scored runs, result
interpretation, PnL/result evaluation, tuning, adapter work, deployment,
trading, promotion, Git actions, or source-faithful evidence claims.
