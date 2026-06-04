# Carver S09 MES Annual Risk Blend Helper Local Hostile Audit

Date: 2026-06-03

Scoped files:

```text
src/carver/spine/s09_mes_readiness.py
src/carver/spine/__init__.py
tests/test_s09_mes_readiness_synthetic.py
```

## Purpose

Record the local hostile audit trail for the synthetic MES annual percentage-risk blend helper added before executing the MES roll-date/runtime-risk/cost gate.

This helper is guard machinery only. It consumes already locked long-run annual percentage risk and already locked EWMA32 current annual percentage risk, then applies the source-locked 30/70 blend:

```text
annual_percentage_risk = 0.30 * long_run_annual_risk + 0.70 * current_ewma32_annual_risk
```

It does not compute EWMA32 runtime, parse market rows, request provider data, compute daily price risk, compute costs, compute forecasts, run diagnostics, or run backtests.

## Helper Surface

```text
S09MESAnnualRiskBlendRequest
S09MESAnnualRiskBlendResult
s09_mes_annual_risk_from_locked_components
```

Source constants:

```text
S09_MES_ANNUAL_RISK_EWMA_SPAN = 32
S09_MES_ANNUAL_RISK_LONG_RUN_WEIGHT = 0.30
S09_MES_ANNUAL_RISK_CURRENT_WEIGHT = 0.70
```

## Audit Findings

```text
CRITICAL: none
HIGH: none
MEDIUM: none
LOW: annual-risk wrapper tests initially missed float EWMA span, bool/non-finite weights, invalid weight sum, non-numeric component values, timezone-naive completed bars, and non-date-aligned completed bars
```

Initial disposition:

```text
AUDIT_DISPOSITION: PASS_WITH_LOW_TEST_SURFACE_HARDENING_RECOMMENDED_NOT_BLOCKING
```

## Low Finding Disposition

The low finding was addressed by adding explicit fail-closed tests for:

```text
ewma_span = 32.0
bool long-run weight
NaN current-risk weight
weights that do not sum to 1
infinite long-run annual risk
non-numeric current EWMA32 annual risk
timezone-naive completed bar
non-date-aligned completed bar
```

The helper already rejected these through source-shape validation; the patch hardens the MES synthetic test surface.

## Verification

Fresh local verification after hardening:

```text
python -m unittest tests.test_s09_mes_readiness_synthetic.S09MESReadinessSyntheticTests.test_mes_annual_risk_blends_locked_long_run_and_ewma32_current_risk tests.test_s09_mes_readiness_synthetic.S09MESReadinessSyntheticTests.test_mes_annual_risk_blend_fails_closed_without_locked_source_components
Ran 2 tests
OK

python -m unittest tests.test_s09_mes_readiness_synthetic
Ran 15 tests
OK

python -m unittest tests.test_s09_mes_lineage_synthetic tests.test_s09_mes_readiness_synthetic tests.test_s09_full_source_atom_synthetic tests.test_s09_m2_synthetic tests.test_s09_phase1_synthetic tests.test_s09_readiness_synthetic tests.test_s09_zn_package_synthetic tests.test_continuous_synthetic
Ran 72 tests
OK

python -m py_compile src/carver/spine/s09_mes_readiness.py src/carver/spine/s09_mes_lineage.py src/carver/spine/__init__.py tests/test_s09_mes_readiness_synthetic.py tests/test_s09_mes_lineage_synthetic.py
exit 0
```

## Non-Authorization

This audit authorizes no Databento API access, no provider login, no OHLCV request, no new data download, no market-row parsing, no EWMA32 runtime execution, no daily price-risk execution from market rows, no cost extraction, no cost computation from components, no S09 forecast computation, no diagnostics, no backtests, no returns, no PnL, no positions, no carry, no CFD adapter work, no old QuantLab active-pipeline use, no tuning, no TEST, no VALIDATION, no OOS, no Lockbox, no Forward, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.
