# S09 MES Dual Cost Scenario Policy Lock Result

Date: 2026-06-03

Status:

```text
LOCKED_S09_MES_DUAL_COST_SCENARIO_POLICY_NOT_RISK_ADJUSTED_COST
```

Decision:

Both cost models are locked for all future S09 MES calculations until replaced
by a new pre-result operator policy:

- CONSERVATIVE_LIVE_FUTURES_PASS_THROUGH: 2.93 USD round turn; 0.064048% of locked annualized USD price risk.
- ETF_SIM_FEE_ALL_IN_EXCHANGE_NFA_EXCLUDED: 2.49 USD round turn; 0.054430% of locked annualized USD price risk.

Correction note:

The policy ratio is expressed against annualized USD price risk to avoid
reintroducing the superseded daily-denominator cost-screen mistake.

Boundary:

No formal risk-adjusted cost value lock, no speed eligibility computation, no
forecast computation, no diagnostics, no backtests, no TEST, no VALIDATION, no
Lockbox, no Forward, no deployment, no trading, no promotion, no Git staging,
no commit, no push, no PR, and no remote operations were performed.
