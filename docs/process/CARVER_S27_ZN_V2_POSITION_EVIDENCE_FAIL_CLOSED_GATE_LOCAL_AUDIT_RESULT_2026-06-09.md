# S27_V2 Position Evidence Fail-Closed Gate Local Audit Result

Date: 2026-06-09

Status:

```text
LOCAL_HOSTILE_AUDIT_PASS
```

## Scope

Audited the `S27_V2` local-only position evidence fail-closed gate.

Primary files:

```text
src/carver/spine/s27_v2_replay/position_evidence_gate.py
tests/test_s27_v2_position_evidence_gate.py
src/carver/spine/s27_v2_replay/forecast_executable.py
docs/process/CARVER_S27_ZN_V2_DESIRED_POSITION_EVIDENCE_PLANNING_GATE_2026-06-09.md
```

The audit scope was limited to:

- active forecast authority binding;
- PASS only for forecast authority;
- FAIL_CLOSED for forecast-to-position divisor, base position, capital/account value, risk target, multiplier/currency, rounding policy, and initial/current position context;
- rejection of self-consistent forged checks and bundles;
- no desired-position/order/fill/cost/PnL/result emission;
- no forbidden provider/API/download/backtest/Git/trading/promotion/source-faithful evidence surface.

## Focused Verification

Compile:

```text
python -m py_compile src\carver\spine\s27_v2_replay\position_evidence_gate.py tests\test_s27_v2_position_evidence_gate.py
```

Result:

```text
PASS
```

Focused tests:

```text
python -m pytest tests\test_s27_v2_forecast_executable.py tests\test_s27_v2_position_evidence_gate.py -q
```

Result:

```text
51 passed in 207.25s
```

## Local Hostile Audit Verdicts

Two independent read-only local hostile audits were run with subagents.

### Audit 1

Verdict:

```text
PASS
```

Findings:

```text
No P0/P1/P2 blockers found for the exact fail-closed position evidence gate.
```

Key points:

- embedded forecast bundle is validated, active forecast bundle is rebuilt from the locked remediation pack, and exact equality is required;
- only `FORECAST_AUTHORITY` is PASS;
- divisor, base position, capital/account value, risk target, multiplier/currency, rounding, and initial/current position context are all FAIL_CLOSED;
- desired-position/order/fill/cost/PnL/result/source-faithful evidence flags are built false and rejected if forged true;
- active checks are rebuilt and compared exactly;
- tests cover forged forecast bundles, promoted unresolved checks, mutated check content, emission flags, missing forecast acceptance, and fail-closed drift.

P3:

```text
None material.
```

### Audit 2

Verdict:

```text
PASS
```

Findings:

```text
No P0/P1/P2 findings in the scoped gate.
```

Key points:

- caller-supplied forecast authority is not trusted;
- caller-supplied checks are not self-authorizing;
- forged PASS/readiness is fail-closed;
- downstream emission is blocked at both upstream forecast authority and this position gate;
- hashes are content-bound but not sole authority;
- focused hostile tests cover the core failure modes.

P3:

```text
None material.
```

## Local Disposition

The position evidence fail-closed gate is locally passed.

This is a readiness artifact only. It is not a desired-position ledger, not an order/fill/cost/PnL/result surface, not a backtest, not result interpretation, and not a source-faithful evidence claim.

## Next Gate

The next useful gate is an external hostile audit packet for this locally passed position evidence fail-closed gate, or a separately authorized evidence-remediation gate for the unresolved position-sizing prerequisites.

Neither path is authorized by this audit result.
