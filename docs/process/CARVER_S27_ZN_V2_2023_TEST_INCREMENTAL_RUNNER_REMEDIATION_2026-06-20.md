# S27_V2 2023 TEST Incremental Runner Remediation

Date: 2026-06-20

## Status

Local implementation checkpoint: `LOCAL_PASS_INCREMENTAL_RUNNER_REMEDIATION_TESTS_NOT_RESULT`

This record documents the remediation response to the S27_V2 2023 TEST row-by-row continuation bottleneck. The previous proof-heavy row runner remains available as a checkpoint/proof verifier, but it is no longer the intended operational continuation path.

## Problem

The row-level TEST continuation loop became performance-blocked. Each small continuation rebuilt or revalidated the full artifact chain, and each market-order blocker tended to create a one-row evidence/audit cycle. That workflow is not viable for TEST, VALIDATION, Lockbox, or future strategy work.

The conservative trust baseline remains the externally clean row-703 checkpoint. Later row-class artifacts, including row 1374 continuation artifacts, are treated as WIP/parity fixtures until validated by the new incremental verifier. No promotion or source-faithful evidence claim is made.

## Implemented Remediation

Added `src/carver/spine/s27_v2_replay/test_incremental_runner.py`.

The new module introduces a two-layer bridge:

- Incremental checkpoint binding from row 703.
- Segment-only validation for appended rows 704 through 1377 plus terminal row-1378 fail-closed blocker.
- Immutable file references keyed by SHA256 for the declared pack manifest, pack SHA256 file, run manifest, evidence manifest, and combined TBBO registry files.
- Segment ledger hashes computed only over compact row slices, not over replayed historical proof state.
- A deterministic missing-TBBO batch plan built from the existing requirements ledger.
- Bundle validation that rejects self-consistent forged segment metadata by rebuilding from active local files.

The implementation does not call provider/API, does not acquire data, does not continue TEST, and does not run the full proof-heavy runner.

## Safety Boundaries

The remediation preserves:

- source-native futures lane;
- completed-bar-only TEST mechanics;
- 2023 TEST-only row boundaries for the inspected segment;
- protected-window preservation;
- result/backtest/source-faithful evidence fail-closed gates;
- no tuning, promotion, deployment, trading, adapter work, or Git action.

The package root is not extended. The incremental runner is importable only as an explicit submodule and is not exported from `carver.spine.s27_v2_replay.__all__`.

## Verification

Focused local checks:

```text
python -m py_compile src/carver/spine/s27_v2_replay/test_incremental_runner.py tests/test_s27_v2_test_incremental_runner.py
python -m pytest -q tests/test_s27_v2_test_incremental_runner.py
```

Result:

```text
14 passed in 4.61s
```

Coverage includes:

- row-703 checkpoint binding;
- explicit rejection of non-row-703 checkpoints;
- segment validation for rows 704 through 1377;
- dense segment continuity enforcement;
- row-1378 terminal missing-TBBO blocker preservation;
- row-704 roll-boundary suppression parity;
- row-1374 market-order/fill/cost/PnL parity from existing artifacts;
- forged checkpoint hash rejection;
- self-consistent forged segment-hash rejection against active files;
- non-authorization drift rejection;
- non-2023 timestamp rejection;
- missing immutable file reference rejection;
- deterministic missing-TBBO batch planning;
- package-root export leak check.

## Local Hostile Audit

One local hostile audit subagent initially found two P1 issues and two P2 issues:

- row-703 was not hard-enforced as the baseline;
- incomplete dense segments could be accepted;
- non-2023 timestamps could pass boundary validation;
- immutable file references were optional.

All four findings were remediated in `test_incremental_runner.py` and covered by focused regressions. The re-audit returned P0 none, P1 none, P2 none. The only re-audit P3 was this stale test-count note, now corrected.

## Current Operating Policy

Do not resume row-by-row TEST continuation through the proof-heavy runner.

The next useful implementation step is to finish replacing continuation with a true fast mechanical row engine that consumes parsed rows and policy registries directly, then emits segment artifacts. The current remediation is the first performance-safe bridge: it validates and packages existing emitted rows cheaply, proving the checkpoint/resume and segment-audit shape before more engine extraction work.

External GPT/Opus hostile audits should be reserved for consolidated checkpoints, not row-level blockers.

## Non-Authorizations

This record does not authorize provider/API access, downloads, new data acquisition, VALIDATION, OOS, Lockbox, Forward, result interpretation, PnL evaluation beyond mechanical construction, tuning, adapter work, deployment, trading, promotion, Git actions, GPT packet preparation, or source-faithful evidence claims.
