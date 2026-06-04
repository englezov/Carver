# S09 MES Dual Speed Eligibility Values Lock Result

Date: 2026-06-03

Status:

```text
LOCKED_S09_MES_DUAL_SPEED_ELIGIBILITY_VALUES_ALL_SPEEDS_SURVIVE_NOT_ELIGIBLE_SET_NOT_BACKTEST
```

Locked threshold:

```text
0.15 SR
```

Result:

- rows locked: 12
- eligible rows: 12
- conservative scenario survives all spans: TRUE
- ETF all-in simulated-fee scenario survives all spans: TRUE

Correction note:

This supersedes any earlier 2026-06-03 no-surviving-speed artifact that divided
USD costs by a daily point-risk denominator.

Boundary:

No eligible speed set lock, no Table 36 FDM row lock, no forecast computation,
no diagnostics, no backtests, no TEST, no VALIDATION, no Lockbox, no Forward,
no deployment, no trading, no promotion, no Git staging, no commit, no push,
no PR, and no remote operations were performed.
