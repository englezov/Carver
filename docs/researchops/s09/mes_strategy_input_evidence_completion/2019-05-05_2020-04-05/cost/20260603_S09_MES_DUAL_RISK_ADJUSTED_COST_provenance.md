# S09 MES Dual Risk-Adjusted Cost Values Provenance

Date: 2026-06-03

Status:

```text
LOCKED_S09_MES_DUAL_RISK_ADJUSTED_COST_VALUES_NOT_SPEED_NOT_BACKTEST
```

Inputs:

- locked dual cost scenario policy: LOCKED_S09_MES_DUAL_COST_SCENARIO_POLICY_NOT_RISK_ADJUSTED_COST
- machinery-development slice: 2019-05-05 through 2020-04-05
- completed trading date: 2020-03-02

Locked values:

- CONSERVATIVE_LIVE_FUTURES_PASS_THROUGH: 0.000640 SR cost per trade, using 4574.6921710874985 annualized USD risk per contract
- ETF_SIM_FEE_ALL_IN_EXCHANGE_NFA_EXCLUDED: 0.000544 SR cost per trade, using 4574.6921710874985 annualized USD risk per contract

Boundary:

This locks formal dual-scenario risk-adjusted cost values only. It does not
compute speed eligibility, forecasts, diagnostics, backtests, TEST,
VALIDATION, Lockbox, Forward, deployment, trading, promotion, Git staging,
commit, push, PR, or remote operations.
