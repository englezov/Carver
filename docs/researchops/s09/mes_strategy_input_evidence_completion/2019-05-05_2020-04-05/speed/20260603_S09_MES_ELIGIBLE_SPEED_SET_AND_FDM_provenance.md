# S09 MES Eligible Speed Set And Table 36 FDM Provenance

Date: 2026-06-03

Status:

```text
LOCKED_S09_MES_ELIGIBLE_SPEED_SET_AND_TABLE36_FDM_ROW_NOT_BACKTEST
```

Inputs:

- corrected dual speed eligibility status: LOCKED_S09_MES_DUAL_SPEED_ELIGIBILITY_VALUES_ALL_SPEEDS_SURVIVE_NOT_ELIGIBLE_SET_NOT_BACKTEST
- machinery-development slice: 2019-05-05 through 2020-04-05
- completed trading date: 2020-03-02

Locked values:

- eligible_spans: 2|4|8|16|32|64
- table36_fdm: 1.26

Boundary:

This locks only the eligible EWMAC speed set and matching Table 36 FDM row. It
does not lock final hash-bound provenance, compute forecasts, run diagnostics,
run backtests, access TEST, VALIDATION, Lockbox, Forward, deploy, trade,
promote, stage Git, commit, push, create a PR, or perform remote operations.
