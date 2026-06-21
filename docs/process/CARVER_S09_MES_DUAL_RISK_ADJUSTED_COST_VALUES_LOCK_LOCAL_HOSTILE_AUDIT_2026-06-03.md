# S09 MES Dual Risk-Adjusted Cost Values Local Hostile Audit

Date: 2026-06-03

Status:

```text
LOCAL_HOSTILE_AUDIT_DUAL_RISK_ADJUSTED_COST_VALUES_LOCKED_NO_SPEED_NO_BACKTEST
```

Checks:

- both scenarios are present: CONSERVATIVE_LIVE_FUTURES_PASS_THROUGH; ETF_SIM_FEE_ALL_IN_EXCHANGE_NFA_EXCLUDED
- conservative risk-adjusted cost is 0.000640
- ETF all-in simulated-fee risk-adjusted cost is 0.000544
- speed eligibility was not computed
- forecasts were not computed
- diagnostics were not run
- backtests were not run
- TEST, VALIDATION, Lockbox, and Forward were not accessed
- Git staging, commit, push, and PR were not performed

This local audit must be reviewed by a spawned hostile-audit subagent.
