# S09 MES Dual Cost Scenario Policy Provenance

Date: 2026-06-03

Status:

```text
LOCKED_S09_MES_DUAL_COST_SCENARIO_POLICY_NOT_RISK_ADJUSTED_COST
```

Operator decision:

Run both cost models and calculate based on both before any backtest result is
seen.

Scenarios:

- CONSERVATIVE_LIVE_FUTURES_PASS_THROUGH: 2.93 USD round turn, 0.064048% of locked annualized USD price risk
- ETF_SIM_FEE_ALL_IN_EXCHANGE_NFA_EXCLUDED: 2.49 USD round turn, 0.054430% of locked annualized USD price risk

Unit bridge:

- annualized USD price risk = locked daily point risk * 16 * MES 5 USD/point multiplier
- this policy remains pre-backtest and does not itself lock formal risk-adjusted cost values

Boundary:

This is a cost-scenario policy lock. It does not lock formal risk-adjusted
cost values, speed eligibility, forecasts, diagnostics, backtests, TEST,
VALIDATION, Lockbox, Forward, deployment, trading, promotion, Git staging,
commit, push, PR, or remote operations.
