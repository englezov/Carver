# Carver S09 MES Risk Adjusted Cost Helper Local Hostile Audit

Date: 2026-06-03

Scoped files:

```text
src/carver/spine/s09_mes_readiness.py
src/carver/spine/__init__.py
tests/test_s09_mes_readiness_synthetic.py
```

## Purpose

Record the local hostile audit trail for the synthetic MES risk-adjusted cost helper added before executing the MES roll-date/runtime-risk/cost gate.

This helper is guard machinery only. It consumes already locked total cost per trade and already locked daily price risk, then computes risk-adjusted cost per trade in SR units:

```text
risk_adjusted_cost_per_trade_sr = total_cost_per_trade_currency / daily_price_risk_currency
```

It does not extract cost components, compute runtime daily price risk, parse market rows, request provider data, compute forecasts, run diagnostics, or run backtests.

## Helper Surface

```text
S09MESRiskAdjustedCostRequest
S09MESRiskAdjustedCostResult
s09_mes_risk_adjusted_cost_from_locked_inputs
```

## Audit Findings

```text
CRITICAL: none
HIGH: none
MEDIUM: none
LOW: risk-adjusted cost hostile tests did not initially cover negative, non-finite, non-numeric, or bool numeric inputs
```

Initial disposition:

```text
AUDIT_DISPOSITION: PASS_WITH_LOW_TEST_SURFACE_HARDENING_RECOMMENDED_NOT_BLOCKING
```

## Low Finding Disposition

The low finding was addressed by adding explicit fail-closed tests for:

```text
negative total cost
negative daily price risk
NaN total cost
infinite daily price risk
non-numeric total cost
bool total cost
```

The helper already rejected these through finite-positive validation; the patch hardens the synthetic test surface.

## Verification

Fresh local verification after hardening:

```text
python -m unittest tests.test_s09_mes_readiness_synthetic.S09MESReadinessSyntheticTests.test_mes_risk_adjusted_cost_uses_locked_cost_and_daily_price_risk_only tests.test_s09_mes_readiness_synthetic.S09MESReadinessSyntheticTests.test_mes_risk_adjusted_cost_fails_closed_without_locked_inputs
Ran 2 tests
OK

python -m unittest tests.test_s09_mes_readiness_synthetic
Ran 11 tests
OK

python -m unittest tests.test_s09_mes_lineage_synthetic tests.test_s09_mes_readiness_synthetic tests.test_s09_full_source_atom_synthetic tests.test_s09_m2_synthetic tests.test_s09_phase1_synthetic tests.test_s09_readiness_synthetic tests.test_s09_zn_package_synthetic tests.test_continuous_synthetic
Ran 68 tests
OK

python -m py_compile src/carver/spine/s09_mes_readiness.py src/carver/spine/s09_mes_lineage.py src/carver/spine/__init__.py tests/test_s09_mes_readiness_synthetic.py tests/test_s09_mes_lineage_synthetic.py
exit 0
```

## Non-Authorization

This audit authorizes no Databento API access, no provider login, no OHLCV request, no new data download, no market-row parsing, no risk runtime execution, no cost extraction, no cost computation from components, no S09 forecast computation, no diagnostics, no backtests, no returns, no PnL, no positions, no carry, no CFD adapter work, no old QuantLab active-pipeline use, no tuning, no TEST, no VALIDATION, no OOS, no Lockbox, no Forward, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.
