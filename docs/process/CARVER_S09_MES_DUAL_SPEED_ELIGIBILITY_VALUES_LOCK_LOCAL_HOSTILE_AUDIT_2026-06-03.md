# S09 MES Dual Speed Eligibility Values Local Hostile Audit

Date: 2026-06-03

Status:

```text
LOCAL_HOSTILE_AUDIT_DUAL_SPEED_ELIGIBILITY_VALUES_LOCKED_NO_ELIGIBLE_SET_NO_BACKTEST
```

Checks:

- two scenarios are present
- six EWMAC spans are evaluated per scenario
- threshold is locked to 0.15 SR
- eligibility values match turnover times risk-adjusted cost versus threshold
- eligible row count is 12
- eligible speed set is not locked
- Table 36 FDM row is not locked
- forecasts, diagnostics, and backtests were not run
- TEST, VALIDATION, Lockbox, and Forward were not accessed
- Git staging, commit, push, and PR were not performed

This local audit must be reviewed by a spawned hostile-audit subagent.
