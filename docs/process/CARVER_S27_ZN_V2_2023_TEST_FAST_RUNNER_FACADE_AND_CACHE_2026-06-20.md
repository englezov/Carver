# S27_V2 2023 TEST Fast Runner Facade And Cache

Date: 2026-06-20

## Status

Local implementation checkpoint: `LOCAL_PASS_FAST_RUNNER_FACADE_CACHE_COMPACT_SEGMENT_AND_EXECUTION_STATE_VERIFIER_NOT_RESULT`

This record extends the incremental-runner remediation with the first operational facade for future fast TEST-scale artifact construction. It does not continue TEST, acquire provider data, run a backtest, interpret results, tune, promote, deploy, trade, or claim source-faithful evidence.

## Implemented

Added `src/carver/spine/s27_v2_replay/replay_artifact_cache.py`.

The cache is keyed by SHA256 of current file bytes, not timestamps. CSV and JSON reads are cached under `(path, sha256)`, so byte changes invalidate cache entries automatically.

Added `src/carver/spine/s27_v2_replay/fast_test_runner.py`.

The facade exposes:

- `segment_mode`: validates the row-703 checkpoint and row 704-1377 segment through the incremental bridge.
- `fast_mode`: currently aliases the same segment engine, fast primitive engine, and execution-state segment verifier while full operational row emission remains pending.
- `proof_mode`: fail-closed unless a separate explicit checkpoint proof gate authorizes slow proof verification.

The facade primes the SHA cache over the declared pack manifest, pack SHA256 file, runtime/decision source ledgers, run manifest, evidence manifest, runtime/forecast/desired/PnL/fail-closed ledgers, and TBBO requirements ledger. It returns a deterministic bundle hash, cache snapshot, primitive-engine bundle, primitive parity report, execution-state verification, segment bundle, TBBO batch plan, and compact artifact-family plan.

`write_segment_metadata()` now emits compact segment artifacts:

- `checkpoint_manifest.json`
- `segment_manifest.json`
- `segment_ledger_hashes.json`
- one `_segment.csv` file for each run ledger family over rows 704-1377 only
- `fail_closed_ledger_terminal.csv` for row 1378 only

This is meant to prevent future audit packets from carrying whole rewritten historical ledgers when only a segment changed.

## Verification

Focused local checks:

```text
python -m py_compile src/carver/spine/s27_v2_replay/replay_artifact_cache.py src/carver/spine/s27_v2_replay/fast_test_runner.py src/carver/spine/s27_v2_replay/test_incremental_runner.py tests/test_s27_v2_test_incremental_runner.py tests/test_s27_v2_fast_runner_cache.py
python -m pytest -q tests/test_s27_v2_test_incremental_runner.py tests/test_s27_v2_fast_runner_cache.py tests/test_s27_v2_fast_row_engine.py tests/test_s27_v2_fast_execution_state.py
```

Result:

```text
45 passed in 15.86s
```

Coverage includes:

- cache invalidation by file byte hash;
- `segment_mode` and `fast_mode` facade validation;
- explicit `proof_mode` fail-closed behavior;
- compact segment artifact emission;
- row-703 checkpoint preservation;
- row-1378 blocker preservation;
- deterministic missing-TBBO batch planning;
- package-root export leak checks;
- no import/call of `test_mechanical_run.py` or `run_2023_test_mechanical_artifacts`.
- exact row-window locking for row 703 baseline, rows 704-1377 segment, and row 1378 terminal blocker;
- locked declared pack/run/TBBO requirement roots before artifact reads;
- facade artifact-family and cache-snapshot anti-forgery checks;
- deep-copy JSON cache reads.
- active-byte cache snapshot ref validation;
- standalone incremental bundle exact-window validation.
- facade binding of primitive-engine parity and execution-state segment verification.
- TBBO plan terminal-row cap, cumulative roll-forward, market-fill source binding, and duplicate sparse row-index regressions.

## Local Hostile Audit

One local hostile audit subagent initially found one P1 and two P2 issues:

- caller-controlled segment windows could bypass the default 704-1377 / 1378 boundary;
- artifact roots were caller-overridable before a root-lock guard;
- facade validation did not bind the artifact family plan and full cache snapshot tightly enough.

The audit also noted P3 hardening items for deep-copy JSON cache reads, broader no-slow-runner regression coverage, and wording around TEST continuation. All were remediated and covered by focused regressions before this record was finalized.

A re-audit found two remaining P2s around self-consistent cache-snapshot forgery and standalone incremental bundle window forgery. Both were remediated by binding cache refs to the expected locked artifact paths and active byte hashes, and by enforcing row `704` through `1377` plus terminal row `1378` directly in `IncrementalSegmentBundle.validate()`.

Later primitive-engine integration removed the facade's arbitrary metadata-output write surface. Compact segment artifact writing remains available only through the explicit incremental metadata writer, not as a fast-runner side effect.

Later execution-state integration added `src/carver/spine/s27_v2_replay/fast_execution_state.py`. The facade now validates the row `704` through `1377` segment's carried position, order-intent class, fill/cost/PnL row coherence, and result/backtest/source-faithful fail-closed boundaries without invoking the proof-heavy runner.

## Remaining Work

The true operational fast mechanical row emitter still needs extraction. The current facade is deliberately labeled:

```text
FAST_RUNNER_FACADE_INCREMENTAL_SEGMENT_PRIMITIVES_AND_EXECUTION_STATE_NOT_FULL_PROOF
```

The next implementation step should generate order/transition/fill/cost/PnL segment rows from parsed row objects and policy registries, then emit compact segment artifacts from generated in-memory rows instead of existing full-run artifact slices.

## Non-Authorizations

This record does not authorize provider/API access, downloads, new data acquisition, broader TEST continuation, VALIDATION, OOS, Lockbox, Forward, result interpretation, PnL evaluation beyond mechanical construction, tuning, adapter work, deployment, trading, promotion, Git actions, GPT packet preparation, or source-faithful evidence claims.
