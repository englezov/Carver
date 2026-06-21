# Carver S09 MES Speed Eligibility Helper Local Hostile Audit

Date: 2026-06-03

Scoped files:

```text
src/carver/spine/s09_mes_readiness.py
src/carver/spine/__init__.py
tests/test_s09_mes_readiness_synthetic.py
```

## Purpose

Record the local hostile audit trail for the synthetic MES speed eligibility helper added before executing the MES roll-date/runtime-risk/cost gate.

This helper is guard machinery only. It consumes an already locked, precomputed risk-adjusted cost per trade in SR units and applies the source-locked Strategy 9 cost threshold and turnover table. It does not compute costs, parse market rows, request provider data, compute forecasts, run diagnostics, or run backtests.

## Helper Surface

```text
S09MESRiskAdjustedCostSpeedEligibilityRequest
S09MESRiskAdjustedCostSpeedEligibilityResult
s09_mes_speed_eligibility_from_risk_adjusted_cost
```

Source constants:

```text
S09_MES_COST_THRESHOLD_SR = 0.15
S09_MES_EWMAC_TURNOVER_BY_SPAN = {
    2: 98.5,
    4: 50.2,
    8: 25.4,
    16: 13.2,
    32: 7.6,
    64: 5.2,
}
```

## Initial Audit Findings

```text
CRITICAL: none
HIGH: speed eligibility helper did not enforce the required 0.15 SR threshold
MEDIUM: none
LOW: tests did not fail-close threshold identity or threshold/turnover source-status branches
```

Initial disposition:

```text
AUDIT_DISPOSITION: FAIL_WITH_HIGH_FINDING_S09_MES_SPEED_THRESHOLD_NOT_STRICTLY_SOURCE_LOCKED
```

## Fixes Applied

```text
threshold_sr must equal S09_MES_COST_THRESHOLD_SR
threshold source must be locked
turnover source must be locked
non-0.15 threshold rejects
unresolved threshold source rejects
unresolved turnover source rejects
```

The helper remains limited to precomputed risk-adjusted cost input. It does not produce strategy readiness by itself; it only supplies the eligible speed set and Table 36 FDM needed by a later readiness gate after all other components are locked.

## Follow-Up Audit Disposition

```text
CRITICAL: none
HIGH: none
MEDIUM: none
LOW: none
AUDIT_DISPOSITION: PASS_FOLLOW_UP_LOCAL_HOSTILE_AUDIT_S09_MES_SPEED_THRESHOLD_STRICTLY_SOURCE_LOCKED
```

## Verification

Fresh local verification after fixes:

```text
python -m unittest tests.test_s09_mes_readiness_synthetic
Ran 9 tests
OK

python -m unittest tests.test_s09_mes_lineage_synthetic tests.test_s09_mes_readiness_synthetic tests.test_s09_full_source_atom_synthetic tests.test_s09_m2_synthetic tests.test_s09_phase1_synthetic tests.test_s09_readiness_synthetic tests.test_s09_zn_package_synthetic tests.test_continuous_synthetic
Ran 66 tests
OK

python -m py_compile src/carver/spine/s09_mes_readiness.py src/carver/spine/s09_mes_lineage.py src/carver/spine/__init__.py tests/test_s09_mes_readiness_synthetic.py tests/test_s09_mes_lineage_synthetic.py
exit 0
```

## Non-Authorization

This audit authorizes no Databento API access, no provider login, no OHLCV request, no new data download, no market-row parsing, no risk runtime execution, no cost computation, no S09 forecast computation, no diagnostics, no backtests, no returns, no PnL, no positions, no carry, no CFD adapter work, no old QuantLab active-pipeline use, no tuning, no TEST, no VALIDATION, no OOS, no Lockbox, no Forward, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.
