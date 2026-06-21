# S27 ZN V2 Runtime Evidence Gate Implementation Record

Date: 2026-06-09

## Authorization

Operator authorized `S27_V2_LOCAL_ONLY_RUNTIME_EVIDENCE_GATE` after GPT external `PASS` on the first-populated input pack/P3 hardening.

Allowed scope was local-only code/test/process work to prove or fail closed on selected-row authority, strict-prior daily/hourly admissibility, EWMA5, EWMAC(16,64), Strategy 3 sigma, V/Q/M, daily/hourly level bridge, session/roll coverage, tick/rounding, multiplier, currency, commission/spread policy, and working-order lifecycle evidence.

This gate did not authorize provider/API access, downloads, new data acquisition, OOS/Lockbox/Forward access, backtests, result-scored runs, forecast/order/fill/cost/PnL/result evidence emission, result interpretation, PnL/result evaluation, tuning, adapter work, deployment, trading, promotion, Git actions, or source-faithful evidence claims.

## Code Changes

1. Added `src/carver/spine/s27_v2_replay/runtime_evidence_gate.py`.
2. Added focused tests in `tests/test_s27_v2_runtime_evidence_gate.py`.
3. Hardened `tests/test_s27_v2_local_replay_slice1.py` so `test_phase2_level_price_binds_exact_indexed_row_hash` covers all four level row families:
   - `DAILY_CONTINUOUS_COMPLETED_BAR`
   - `DAILY_CURRENT_CONTRACT_COMPLETED_BAR`
   - `HOURLY_DECISION_COMPLETED_BAR`
   - `HOURLY_FILL_COMPLETED_BAR`

## Authorized Pack

The gate is locked to:

`docs/researchops/s27_v2_local_replay_inputs/ZN/20260609_first_populated_dev_recon_znh2_20220103_multirow_declared_pack`

Out-of-scope local paths are rejected before manifest/CSV reads.

Manifest byte SHA256:

`5B9A6C6766C97D9C44F8E5AC7B1339D8E25E499B8FF96C2D8D1B574E76F4B781`

Runtime evidence gate bundle hash:

`4757B0C7E200A8411261E85301556E5BDD0C5778271E35528B46AA28A4CB3038`

This bundle hash is fail-closed gate metadata only. It is not a replay result, not a backtest, not PnL, and not source-faithful evidence.

## Gate Outcome

Status:

`S27_V2_RUNTIME_EVIDENCE_GATE_FAIL_CLOSED_NOT_RESULT_NOT_EVIDENCE`

Local declared/count-only checks:

- Declared file hashes: `PASS_LOCAL_DECLARED_ONLY_NOT_SOURCE_FAITHFUL_RUNTIME_EVIDENCE`
- Selected row authority: `PASS_LOCAL_DECLARED_ONLY_NOT_SOURCE_FAITHFUL_RUNTIME_EVIDENCE`
- Hourly decision/fill admissibility: `PASS_LOCAL_DECLARED_ONLY_NOT_SOURCE_FAITHFUL_RUNTIME_EVIDENCE`
- EWMA5 count: `PASS_COUNT_ONLY_NOT_SOURCE_FAITHFUL_RUNTIME_EVIDENCE`
- EWMAC(16,64) count: `PASS_COUNT_ONLY_NOT_SOURCE_FAITHFUL_RUNTIME_EVIDENCE`
- Session/roll coverage: `PASS_LOCAL_DECLARED_ONLY_NOT_SOURCE_FAITHFUL_RUNTIME_EVIDENCE`

Fail-closed checks:

- Strict-prior daily admissibility: selected row `2022-01-02`, last prior row `2020-12-21`; large gap remains unresolved.
- Strategy 3 sigma evidence: selected sigma is a carried bridge value, not source-faithful runtime evidence.
- V/Q/M evidence: local V/Q/M source latest completed trading date is `2020-12-21`, stale versus selected decision `2022-01-03T05:00:00Z`.
- Daily/hourly level bridge: local closes differ: daily continuous `132.53125`, daily current `130.34375`, hourly decision `132.453125`, hourly fill `132.4375`.
- Tick/rounding policy: no source-locked executable ZN tick/rounding policy is bound.
- Multiplier/currency policy: declared hashes exist but are not executable source-locked cost evidence.
- Commission/spread policy: declared hashes exist but are not executable source-locked cost evidence.
- Working-order lifecycle: no source-locked working limit-order lifecycle evidence is bound.

The gate emits no forecast, order, fill, cost, PnL, scored-result, or source-faithful evidence rows.

## Verification

Commands run:

```powershell
python -m pytest tests\test_s27_v2_runtime_evidence_gate.py -q
```

Result: `8 passed`

```powershell
python -m pytest tests\test_s27_v2_local_replay_slice1.py tests\test_s27_v2_runtime_evidence_gate.py -q
```

Result: `79 passed`

```powershell
python -m compileall -q src\carver\spine\s27_v2_replay\runtime_evidence_gate.py tests\test_s27_v2_runtime_evidence_gate.py
```

Result: passed

## Local Hostile Audit Findings And Patches

Two local hostile audit agents were reused because the thread had reached the subagent limit.

Initial code audit found:

- P1: self-consistent forged runtime evidence checks could validate if a forged bundle changed blocker statuses and recomputed the bundle hash.
- P2: daily/hourly level evidence could become locally passed on identical closes despite no source-locked bridge proof.

Patch:

- added locked required check status semantics by check label;
- required fail-closed gate labels to equal failed checks exactly;
- made daily/hourly level bridge remain fail-closed unless a future source-locked bridge proof is implemented.

Second audit found:

- P1: self-consistent forged check gate labels could validate if the failed check gate label and fail-closed tuple were both forged.
- P2: arbitrary local input-pack paths were accepted.

Patch:

- added locked required gate label semantics by check label;
- locked the builder to the authorized first-populated pack path;
- added regression tests for gate-label forgery and out-of-scope path rejection.

Final local hostile re-audit returned `PASS`: no P0/P1/P2 findings.

## Current State

The first-populated pack remains useful for local declared-file binding, selected-row construction authority, hourly decision/fill shape, and count-only EWMA/EWMAC preconditions. It is not ready for nonblocked runtime-history ledgers because strict-prior daily admissibility, source-faithful Strategy 3 sigma, V/Q/M, level bridge, tick/rounding, cost policy, and working-order lifecycle evidence remain fail-closed.

The next useful gate is to build or identify a better local-only runtime evidence input pack and/or source-lock the missing policy/evidence prerequisites before any nonblocked runtime-history, forecast, order, fill, cost, PnL, scored run, or source-faithful evidence claim.
