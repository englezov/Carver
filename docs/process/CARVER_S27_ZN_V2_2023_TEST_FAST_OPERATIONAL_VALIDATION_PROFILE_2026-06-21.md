# CARVER S27 ZN V2 2023 TEST Fast Operational Validation Profile

Date: 2026-06-21

Status: `LOCAL_PASS_FAST_OPERATIONAL_VALIDATION_PROFILE_AFTER_LOCAL_REAUDIT_REMEDIATION_NOT_RESULT`

## Scope

This record covers the performance/incremental-validation remediation for the S27_V2 2023 TEST fast runner. The purpose was to stop normal TEST continuation from repeatedly invoking checkpoint-proof active-file replay while preserving the checkpoint proof path for explicit audit gates.

This record does not authorize TEST continuation, provider/API access, downloads, new data acquisition, VALIDATION, OOS, Lockbox, Forward, result interpretation, tuning, Git actions, GPT/Opus packet preparation, adapter/deployment/trading/promotion, or source-faithful evidence claims.

## Implementation

Added `src/carver/spine/s27_v2_replay/fast_validation_profiles.py` with:

- `OPERATIONAL_SEGMENT_HASH_AND_GENERATED_ROWS_NOT_FULL_PROOF`
- `CHECKPOINT_PROOF_PARITY_ORACLE_EXPLICIT_ONLY`

The default `FastRunnerRequest.validation_profile` is now operational. Normal `run_2023_test_fast_runner()` validates the segment bundle, generated order/downstream/segment rows, cache snapshot byte hashes, row hashes, bundle hashes, TBBO plan hash, non-authorizations, result/source-faithful fail-closed flags, and generated segment assembly without replaying `IncrementalSegmentBundle.validate_against_active_files()`.

Checkpoint-proof validation remains available through the explicit checkpoint-proof profile and builder defaults. The proof path still gates `validate_against_active_files()` inside:

- `fast_execution_state.py`
- `fast_segment_emitter.py`
- `fast_order_generator.py`
- `fast_downstream_generator.py`
- `fast_generated_segment_assembler.py`
- `fast_test_runner.py`

## Verification

Focused verification passed:

- `python -m compileall src/carver/spine/s27_v2_replay/fast_validation_profiles.py src/carver/spine/s27_v2_replay/fast_execution_state.py src/carver/spine/s27_v2_replay/fast_segment_emitter.py src/carver/spine/s27_v2_replay/fast_order_generator.py src/carver/spine/s27_v2_replay/fast_downstream_generator.py src/carver/spine/s27_v2_replay/fast_generated_segment_assembler.py src/carver/spine/s27_v2_replay/fast_test_runner.py`
- `PYTHONPATH=src python -m pytest tests/test_s27_v2_fast_runner_cache.py -q` returned `16 passed in 35.67s`
- `PYTHONPATH=src python -m pytest tests/test_s27_v2_fast_order_generator.py tests/test_s27_v2_fast_downstream_generator.py tests/test_s27_v2_fast_generated_segment_assembler.py -q` returned `34 passed in 487.00s`

Direct operational facade timing:

- `run_2023_test_fast_runner()` completed the current row `704` through `1377` generated segment in approximately `5.53` seconds after remediation.
- The generated segment row count was `674`.
- A regression test now monkeypatches `IncrementalSegmentBundle.validate_against_active_files()` to raise and confirms the default operational runner does not call it.

## Local Hostile Audit

Local hostile audit subagent initially returned `FAIL` with one P1: the default operational path still invoked repeated active-file checkpoint replay through `build_fast_execution_state_verification()`.

Remediation added `validation_profile` to `build_fast_execution_state_verification()` and threaded it through `fast_test_runner.py` and `fast_segment_emitter.py`. Operational mode now calls `IncrementalSegmentBundle.validate()`, while checkpoint-proof mode still calls `validate_against_active_files()`.

Targeted re-audit returned `PASS`: the default operational path no longer invokes `validate_against_active_files()` during normal `run_2023_test_fast_runner()`, and checkpoint-proof validation still has explicit access to active-file replay.

## Current Boundary

The fast runner remediation machinery is locally passed through operational validation-profile separation. Row `1374` and later row-class artifacts remain WIP/parity fixtures until accepted by future controlled continuation under the fast runner. The conservative external trust baseline remains row `703`.

Next useful gate: a separately authorized controlled local-only TEST continuation using the fast operational runner and checkpoint/segment verifier, with external GPT/Opus audits reserved for consolidated phase checkpoints only.
