# S09 MES Eligible Speed Set And Table 36 FDM Local Hostile Audit

Date: 2026-06-03

Status:

```text
LOCAL_HOSTILE_AUDIT_ELIGIBLE_SPEED_SET_TABLE36_FDM_LOCKED_NO_BACKTEST
```

Checks:

- corrected dual speed eligibility status is consumed
- both cost scenarios survive all six spans
- eligible speed set is 2|4|8|16|32|64
- Table 36 FDM is 1.26
- hash-bound provenance remains unlocked
- strategy input readiness remains fail-closed
- forecasts, diagnostics, and backtests were not run
- TEST, VALIDATION, Lockbox, and Forward were not accessed
- Git staging, commit, push, and PR were not performed

This local audit must be reviewed by a spawned hostile-audit subagent.
