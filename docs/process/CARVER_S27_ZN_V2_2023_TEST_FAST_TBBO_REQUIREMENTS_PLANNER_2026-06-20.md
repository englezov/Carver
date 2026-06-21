# S27_V2 2023 TEST Fast TBBO Requirements Planner

Date: 2026-06-20

## Status

Local implementation checkpoint: `LOCAL_PASS_FAST_TBBO_REQUIREMENTS_PLANNER_NOT_RESULT`

This record extends the S27_V2 TEST runner remediation by adding a fast TBBO requirements planner that derives missing market-order bid/ask evidence requirements from the validated fast segment artifacts and terminal fail-closed row, instead of relying on the legacy standalone requirements ledger.

This is not provider/API access, not data acquisition, not TEST continuation, not result interpretation, and not source-faithful evidence.

## Implemented

Added `src/carver/spine/s27_v2_replay/fast_evidence_planner.py`.

The planner:

- consumes `FastSegmentArtifacts`, `IncrementalSegmentBundle`, and `FastExecutionStateVerification`;
- reuses the fast segment artifact validation boundary before accepting inputs;
- scans segment market-order rows for any missing selected-spread evidence;
- preserves already supported segment market orders as supported count, not new provider requirements;
- derives the terminal row `1378` missing TBBO requirement from the fail-closed row itself;
- emits a compact `fast_tbbo_requirement_plan.json` and `fast_tbbo_requirements.csv` when explicitly written;
- rejects forged requirement rows, artifact binding drift, non-2023 timestamps, and package-root export leakage.

The current derived plan contains exactly one missing requirement:

- row `1378`;
- raw symbol `ZNM3`;
- side `SELL`;
- quantity `2`;
- source ledger `fail_closed_ledger.csv`;
- status `REQUIRES_BOUNDED_DATABENTO_TBBO_EVIDENCE`.

## Verification

Focused local checks:

```text
python -m pytest tests/test_s27_v2_test_incremental_runner.py tests/test_s27_v2_fast_runner_cache.py tests/test_s27_v2_fast_row_engine.py tests/test_s27_v2_fast_execution_state.py tests/test_s27_v2_fast_segment_emitter.py tests/test_s27_v2_fast_evidence_planner.py
```

Result:

```text
59 passed in 67.11s
```

Coverage includes:

- deriving row `1378` from validated segment/terminal artifacts;
- writing a compact requirements JSON/CSV;
- rejecting forged requirement row hashes;
- rejecting self-consistent forged requirement rows by re-deriving the active plan from validated artifacts;
- rejecting writer calls for self-consistent forged plans before any file output;
- rejecting artifact-binding drift;
- rejecting non-2023 requirement timestamps;
- preserving package-root export quarantine.

## Local Hostile Audit

One local hostile audit subagent initially found two P1 issues and one derivative P2 documentation issue:

- self-consistent forged requirement plans could be accepted because validation checked row self-hashes and plan self-hash but did not re-derive the expected plan from active artifacts;
- the writer accepted a caller-supplied plan without requiring the validated artifact/segment/verifier context;
- the tests and process records therefore overstated forged-row protection.

Remediation:

- `FastTBBORequirementPlan.validate()` now rebuilds the expected requirement plan from the validated `FastSegmentArtifacts`, `IncrementalSegmentBundle`, and `FastExecutionStateVerification`, and rejects active derivation drift;
- `write_fast_tbbo_requirement_plan()` now requires the same artifact/segment/verifier context and validates the plan before output;
- tests now cover self-consistent forged row rejection and writer rejection before file output.

Final local hostile re-audit returned P0 none, P1 none, P2 none, and P3 none. The re-audit confirmed active plan re-derivation rejects self-consistent forged plans, the writer validates against artifact/segment/verifier context before output, and no provider/API/download, TEST continuation, result/source-faithful, package-root export, or proof-heavy runner surface was introduced.

## Remaining Work

The remaining major remediation step is to replace parity-fixture segment rows with generated execution/order/fill/cost/PnL rows from declared row objects plus policy registries, then plug the fast TBBO planner into that generated segment output.

## Non-Authorizations

This record does not authorize provider/API access, downloads, new data acquisition, broader TEST continuation, VALIDATION, OOS, Lockbox, Forward, result interpretation, PnL evaluation beyond mechanical construction, tuning, adapter work, deployment, trading, promotion, Git actions, GPT packet preparation, or source-faithful evidence claims.
