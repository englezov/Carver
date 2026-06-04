# Carver S09 MES Strategy Input Readiness Synthetic Guard Local Hostile Audit

Date: 2026-06-02

Status:

```text
PROCESS_ONLY_LOCAL_HOSTILE_AUDIT_RECORD_NOT_DATA_NOT_BACKTEST
```

## Scope

Audit target:

```text
src/carver/spine/s09_mes_readiness.py
tests/test_s09_mes_readiness_synthetic.py
docs/process/CARVER_S09_MES_STRATEGY_INPUT_READINESS_SYNTHETIC_GUARD_2026-06-02.md
src/carver/spine/__init__.py
```

Mode:

```text
READ_ONLY_SUBAGENT_HOSTILE_AUDIT_WITH_REAUDIT
```

No data access, provider access, market-row parsing, continuous-lineage execution, risk runtime execution, cost execution, diagnostics, backtests, forecasts, positions, carry, OOS, Lockbox, Forward, CFD adapter work, old QuantLab active-pipeline use, Git operations, remote operations, deployment, trading, or promotion were authorized or performed by the audit.

## Initial Findings

No Critical, High, or Medium findings.

Initial Low findings:

- `speed_eligibility_basis` was fail-closed but wording-fragile because it rejected any string containing `ASSUM`, including a future label such as `NON_ASSUMPTION_COST_SCREEN_LOCKED`.
- Tests proved core failure modes but did not individually assert every required status field.

Initial disposition:

```text
BLOCKING_FINDINGS: NO
AUDIT_DISPOSITION: PASS_S09_MES_SYNTHETIC_STRATEGY_INPUT_READINESS_GUARD_WITH_LOW_COVERAGE_HARDENING_NOTES
```

## Patches Applied

The guard now rejects explicit assumption labels only:

```text
ASSUMED_*
ASSUMED
ASSUMPTION
ASSUMED_ALL_SIX_SPEEDS
```

It permits non-assumption evidence labels such as:

```text
NON_ASSUMPTION_COST_SCREEN_LOCKED
LOCKED_COST_SCREEN_ALL_SIX_SPEEDS_SURVIVE
```

The tests now assert:

- every component status fails closed when unresolved;
- explicit `ASSUMED_ALL_SIX_SPEEDS` fails closed;
- all six EWMAC speeds can pass when backed by locked cost-screen evidence and Table 36 FDM `1.26`;
- a `NON_ASSUMPTION...` basis does not fail closed merely because it contains the substring `ASSUM`.

## Re-Audit Result

Re-audit findings:

```text
NON_ASSUMPTION_COST_SCREEN_LOCKED passes
explicit ASSUMED_* labels fail closed
all-six speeds pass with locked cost-screen basis and FDM 1.26
every component status is individually tested
no data/provider/backtest authority introduced
```

Verification reported by subagent:

```text
python -m unittest tests.test_s09_mes_readiness_synthetic
Ran 7 tests OK
```

Full local relevant suite after patch:

```text
python -m unittest tests.test_s09_mes_readiness_synthetic tests.test_s09_full_source_atom_synthetic tests.test_s09_m2_synthetic tests.test_s09_phase1_synthetic tests.test_s09_readiness_synthetic tests.test_s09_zn_package_synthetic tests.test_continuous_synthetic
Ran 53 tests OK
```

## Final Disposition

```text
BLOCKING_FINDINGS: NO
AUDIT_DISPOSITION: PASS_PRIOR_LOW_FINDINGS_CLOSED
```

## Non-Authorization

This audit record authorizes no provider API access, no new data download, no market-row parsing, no continuous lineage construction, no risk runtime execution, no cost execution, no S09 forecast computation, no diagnostics, no backtests, no returns, no PnL, no Sharpe, no drawdown, no positions, no carry, no CFD adapter work, no old QuantLab pipeline use, no tuning, no TEST, no VALIDATION, no OOS, no Lockbox, no Forward, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update, and no remote repository operations.
