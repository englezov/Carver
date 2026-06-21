# S27 ZN V2 Runtime Evidence Gate Local Audit Result

Date: 2026-06-09

## Verdict

`PASS` after follow-up patches.

No P0/P1/P2 findings remain in the authorized `S27_V2_LOCAL_ONLY_RUNTIME_EVIDENCE_GATE` scope.

## Scope Audited

Files:

- `src/carver/spine/s27_v2_replay/runtime_evidence_gate.py`
- `tests/test_s27_v2_runtime_evidence_gate.py`
- `tests/test_s27_v2_local_replay_slice1.py`

Scope:

- all-four-family Phase 2 indexed row-hash/close-price regression coverage;
- runtime-evidence gate status semantics;
- fail-closed gate label binding;
- authorized input-pack path boundary;
- no forbidden provider/API/download/OOS/Lockbox/Forward/backtest/result/PNL/Git/adapter/deployment/trading/promotion/source-faithful evidence surface.

## Audit Loop

Initial code audit verdict: `FAIL`.

Findings:

- P1: self-consistent forged runtime-evidence check statuses could validate if bundle hash was recomputed.
- P2: daily/hourly level bridge could become locally passed on identical closes without a source-locked bridge proof.

Patch result:

- required check statuses are locked by check label;
- fail-closed label tuple must exactly match failed checks;
- daily/hourly level bridge remains fail-closed in this gate.

Second audit verdict: `FAIL`.

Findings:

- P1: self-consistent check gate-label forgery could validate if failed check labels and fail-closed tuple were both forged.
- P2: the builder accepted arbitrary local input-pack paths.

Patch result:

- required gate labels are locked by check label;
- `build_runtime_evidence_gate()` is locked to the authorized first-populated pack path;
- regression tests cover check gate-label forgery and out-of-scope path rejection.

Final code audit verdict: `PASS`.

Final governance/path audit verdict: `PASS`.

## Verification

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

## Non-Authorization Confirmation

This audit did not authorize or perform provider/API access, downloads, new data acquisition, OOS/Lockbox/Forward access, backtests, result-scored runs, forecast/order/fill/cost/PnL/result evidence emission, result interpretation, PnL/result evaluation, tuning, adapter work, deployment, trading, promotion, Git staging/commit/push/PR, or source-faithful evidence claims.
