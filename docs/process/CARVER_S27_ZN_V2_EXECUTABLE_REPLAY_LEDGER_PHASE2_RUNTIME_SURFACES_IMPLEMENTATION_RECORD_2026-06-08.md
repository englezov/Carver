# S27 ZN V2 Executable Replay Ledger Phase 2 Runtime Surfaces Implementation Record

Date: 2026-06-08

Status:

```text
S27_V2_LOCAL_ONLY_EXECUTABLE_REPLAY_LEDGER_PHASE2_RUNTIME_SURFACES_IMPLEMENTED_NOT_RESULT
```

Authorization:

```text
S27_V2_LOCAL_ONLY_EXECUTABLE_REPLAY_LEDGER_IMPLEMENTATION_PHASE_2
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Scope

This implementation adds a controlled local-only Phase 2 executable replay
surface for non-result runtime surfaces only.

Implemented code:

```text
src/carver/spine/s27_v2_replay/executable_replay.py
```

Focused verification additions:

```text
tests/test_s27_v2_local_replay_slice1.py
```

The Phase 2 builder wraps the externally passed Phase 1 fail-closed builder and
then constructs in-memory, content-hash-bound rows for:

- `DAILY_HOURLY_CONTINUOUS_LEVEL_COMPATIBILITY_LEDGER`;
- `RUNTIME_REPLAY_LEDGER_EWMA5_EWMAC_SIGMA_VQM`.

For the current one-row oldest local ZN development pack, level compatibility
fails closed because daily continuous, daily current-contract, hourly decision,
and hourly fill close prices are not identical and no bridge proof is executable
in this phase. Runtime history fails closed because the pack lacks the locked
minimum strict-prior daily history needed for EWMAC(16,64), sigma, and V/Q/M.

## Implemented Guards

The Phase 2 surface:

- preserves the Phase 1 byte-manifest and active-construction recomputation
  guard;
- records level/runtime contract hashes in Phase 1 provenance;
- records active parsed close-price tuples in Phase 1 provenance;
- binds Phase 2 source-manifest, level-contract, runtime-contract, row-hash, and
  close-price fields back to Phase 1 provenance;
- requires level PASS/FAIL status to match active parsed close prices;
- requires runtime level-pass dependency to match the active level row status;
- keeps runtime numeric values un-emitted;
- keeps forecast, order, fill, cost, PnL, scored-result, and source-faithful
  evidence flags false.

## Verification

Focused local verification:

```text
python -m pytest tests\test_s27_v2_local_replay_slice1.py -q
67 passed
```

Compile check:

```text
python -m compileall -q src\carver\spine\s27_v2_replay\executable_replay.py tests\test_s27_v2_local_replay_slice1.py
PASS
```

## Non-Authorization

This record does not authorize provider/API access, downloads, new data
acquisition, OOS, Lockbox, Forward, backtests, result-scored runs, result
interpretation, PnL/result evaluation, tuning, adapter work, deployment,
trading, promotion, Git actions, or source-faithful evidence claims.
