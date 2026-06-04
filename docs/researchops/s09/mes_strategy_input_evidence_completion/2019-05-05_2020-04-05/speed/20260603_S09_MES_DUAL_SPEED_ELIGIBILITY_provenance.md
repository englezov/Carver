# S09 MES Dual Speed Eligibility Values Provenance

Date: 2026-06-03

Status:

```text
LOCKED_S09_MES_DUAL_SPEED_ELIGIBILITY_VALUES_ALL_SPEEDS_SURVIVE_NOT_ELIGIBLE_SET_NOT_BACKTEST
```

Inputs:

- locked dual risk-adjusted cost status: LOCKED_S09_MES_DUAL_RISK_ADJUSTED_COST_VALUES_NOT_SPEED_NOT_BACKTEST
- threshold: 0.15 SR
- spans: 2,4,8,16,32,64
- machinery-development slice: 2019-05-05 through 2020-04-05

Result:

The speed eligibility values are locked for both scenarios. All evaluated rows
survive the locked threshold after the annualized USD risk unit correction.
The eligible speed set and Table 36 FDM row remain separate downstream locks.

Eligible rows:

- 12 of 12

Boundary:

This locks speed eligibility values only. It does not lock an eligible speed
set, select a Table 36 FDM row, compute forecasts, run diagnostics, run
backtests, access TEST, VALIDATION, Lockbox, Forward, deploy, trade, promote,
stage Git, commit, push, create a PR, or perform remote operations.
