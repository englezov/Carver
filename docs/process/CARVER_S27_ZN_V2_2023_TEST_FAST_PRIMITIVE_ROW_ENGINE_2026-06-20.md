# S27_V2 2023 TEST Fast Primitive Row Engine

Date: 2026-06-20

## Status

Local implementation checkpoint: `LOCAL_PASS_FAST_PRIMITIVE_ROW_ENGINE_PARITY_NOT_RESULT`

This record extends the S27_V2 TEST runner remediation with the first true fast row-mechanics extraction. It computes runtime, forecast, and absolute desired-position primitives directly from the declared 2023 TEST input pack instead of reusing full-run artifact rows for those primitive calculations.

This is not full execution extraction. Order/transition/fill/cost/PnL mechanics still need to be extracted in later slices.

## Implemented

Added `src/carver/spine/s27_v2_replay/fast_row_engine.py`.

The primitive engine:

- locks to `docs/researchops/s27_v2_local_replay_inputs/ZN/20260612_2023_test_declared_pack`;
- verifies the declared pack manifest hashes for `runtime_evidence_ledger.csv` and `hourly_decision_completed_bar.csv`;
- parses 1,378 declared runtime/decision rows via the SHA256 artifact cache;
- computes runtime numeric rows;
- computes raw forecast, sigma-price bridge, trend veto, V/Q/M attenuation, scalar, cap, and capped forecast;
- computes base position and absolute desired position using the accepted capital/risk/divisor/multiplier policies;
- emits in-memory primitive row bundles with deterministic hashes;
- validates parity against existing runtime, forecast, and desired-position ledgers for rows `1`, `2`, `303`, `304`, `547`, and `1374`.

The fast-runner facade now binds the primitive-engine bundle and parity report before accepting `fast_mode` or `segment_mode`.

## Verification

Focused local checks:

```text
python -m py_compile src/carver/spine/s27_v2_replay/replay_artifact_cache.py src/carver/spine/s27_v2_replay/fast_row_engine.py src/carver/spine/s27_v2_replay/fast_test_runner.py src/carver/spine/s27_v2_replay/test_incremental_runner.py tests/test_s27_v2_test_incremental_runner.py tests/test_s27_v2_fast_runner_cache.py tests/test_s27_v2_fast_row_engine.py
python -m pytest -q tests/test_s27_v2_test_incremental_runner.py tests/test_s27_v2_fast_runner_cache.py tests/test_s27_v2_fast_row_engine.py
```

Result:

```text
34 passed in 11.77s
```

Coverage includes:

- declared-pack primitive row construction;
- runtime/forecast/desired parity against existing ledgers;
- evidence-manifest byte-hash binding for compared parity ledgers;
- primitive rows-to-bundle hash binding before parity checks;
- locked parity-row sample enforcement;
- desired primitive parity checks for timestamp, capped forecast, desired position, and base position, with the fast primitive row status/hash self-bound into the parity report;
- locked pack root rejection;
- forged primitive bundle rejection;
- locked run-root parity rejection;
- facade binding of primitive bundle and parity report;
- existing incremental bridge/cache/facade hardening regressions.

## Local Hostile Audit

One local hostile audit subagent initially found two P1 issues and three P2 issues:

- parity against existing ledgers was not evidence-manifest byte-hash bound;
- parity did not bind supplied primitive rows back to the primitive bundle hashes;
- parity row selection was caller-controlled;
- desired-position parity was narrower than the emitted primitive row;
- the fast facade exposed an arbitrary metadata-output write surface.

All findings were remediated. The facade no longer writes segment metadata as a side effect; compact artifact writing remains available only through the explicit incremental metadata writer. Focused regressions now cover the remediations. A re-audit found no remaining P0/P1/P2 findings and one P3 documentation wording issue, remediated here.

## Remaining Work

The next extraction slice, partially completed by `CARVER_S27_ZN_V2_2023_TEST_FAST_EXECUTION_STATE_VERIFIER_2026-06-20.md`, should move from segment verification to operational segment emission:

- checkpoint state carry-forward;
- adjacent-limit order construction;
- market-order requirement classification;
- fill/cost/PnL row construction;
- terminal blocker handling;
- segment artifact emission from in-memory rows instead of existing full-run artifacts.

## Non-Authorizations

This record does not authorize provider/API access, downloads, new data acquisition, broader TEST continuation, VALIDATION, OOS, Lockbox, Forward, result interpretation, PnL evaluation beyond mechanical construction, tuning, adapter work, deployment, trading, promotion, Git actions, GPT packet preparation, or source-faithful evidence claims.
