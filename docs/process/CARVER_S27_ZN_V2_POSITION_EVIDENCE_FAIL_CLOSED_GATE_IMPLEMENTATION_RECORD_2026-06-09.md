# S27_V2 Position Evidence Fail-Closed Gate Implementation Record

Date: 2026-06-09

Status:

```text
LOCAL_IMPLEMENTATION_COMPLETE_PENDING_LOCAL_HOSTILE_AUDIT
```

## Authorization

Operator authorized the `S27_V2` local-only position evidence fail-closed gate after external PASS on the forecast executable remediation-pack slice.

Authorized scope:

- build a non-result position-evidence readiness artifact;
- consume the active forecast executable bundle;
- record PASS/FAIL_CLOSED status for forecast authority, forecast-to-position divisor, base position, capital/account value, risk target, multiplier/currency, rounding policy, and initial/current position context;
- add focused local verification tests and local hostile audits.

Non-authorized scope:

- no desired-position rows;
- no order/fill/cost/PnL/result emission;
- no backtests or result-scored runs;
- no result interpretation or PnL evaluation;
- no provider/API access, downloads, new data, OOS/Lockbox/Forward;
- no tuning, adapter work, deployment, trading, promotion, Git actions, or source-faithful evidence claim.

## Implemented Surface

New module:

```text
src/carver/spine/s27_v2_replay/position_evidence_gate.py
```

New focused tests:

```text
tests/test_s27_v2_position_evidence_gate.py
```

The gate builds:

```text
PositionEvidenceGateBundle
```

The bundle is locked to:

```text
strategy_id = S27_V2_ZN
instrument = ZN
lane = SOURCE_NATIVE_FUTURES
input_pack = docs/researchops/s27_v2_local_replay_inputs/ZN/20260609_runtime_evidence_recon_znm6_20260413_declared_pack
```

## Evidence Statuses

The gate records one active PASS:

```text
FORECAST_AUTHORITY = PASS_ACTIVE_FORECAST_AUTHORITY_NOT_POSITION
```

The gate records fail-closed status for all position prerequisites:

```text
FORECAST_TO_POSITION_DIVISOR = FAIL_CLOSED_POSITION_EVIDENCE_UNRESOLVED
BASE_POSITION = FAIL_CLOSED_POSITION_EVIDENCE_UNRESOLVED
CAPITAL_ACCOUNT_VALUE = FAIL_CLOSED_POSITION_EVIDENCE_UNRESOLVED
RISK_TARGET = FAIL_CLOSED_POSITION_EVIDENCE_UNRESOLVED
MULTIPLIER_CURRENCY = FAIL_CLOSED_POSITION_EVIDENCE_UNRESOLVED
ROUNDING_POLICY = FAIL_CLOSED_POSITION_EVIDENCE_UNRESOLVED
INITIAL_CURRENT_POSITION_CONTEXT = FAIL_CLOSED_POSITION_EVIDENCE_UNRESOLVED
```

This means desired-position emission is still not ready.

## Authority Boundary

`PositionEvidenceGateBundle.validate()`:

- validates the embedded `ForecastExecutableBundle`;
- rebuilds the active forecast executable bundle from the audited remediation pack;
- requires the embedded forecast bundle to equal the active rebuilt bundle;
- rebuilds the active position-evidence checks from that active forecast bundle;
- requires supplied checks to equal the active rebuilt checks;
- preserves the locked fail-closed gate tuple.

Standalone check validation is structural only and does not accept the bundle as authority. The accepting path is the gate bundle validation that rebuilds active upstream forecast authority.

## Emission Boundary

The bundle requires:

```text
forecast_authority_accepted = True
position_evidence_ready = False
desired_position_rows_emitted = False
order_rows_emitted = False
fill_rows_emitted = False
cost_rows_emitted = False
pnl_rows_emitted = False
result_scored_run_emitted = False
source_faithful_evidence_claimed = False
```

Any forged downstream flag fails validation.

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

## Current Disposition

This implementation is local-only and pending local hostile audit result.

It is not a desired-position ledger, not an order/fill/cost/PnL/result surface, not a backtest, not result interpretation, and not a source-faithful evidence claim.
