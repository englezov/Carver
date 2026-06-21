# S09 MES Dual Risk-Adjusted Cost Values Lock Result

Date: 2026-06-03

Status:

```text
LOCKED_S09_MES_DUAL_RISK_ADJUSTED_COST_VALUES_NOT_SPEED_NOT_BACKTEST
```

Formal risk-adjusted cost values:

- CONSERVATIVE_LIVE_FUTURES_PASS_THROUGH: 2.93 USD / 4574.6921710874985 annualized USD risk per contract = 0.000640 SR cost per trade.
- ETF_SIM_FEE_ALL_IN_EXCHANGE_NFA_EXCLUDED: 2.49 USD / 4574.6921710874985 annualized USD risk per contract = 0.000544 SR cost per trade.

Unit bridge:

- daily price-risk field remains the locked daily index-point risk
- annualized USD risk per contract = daily point risk * 16 * MES 5 USD/point multiplier
- this supersedes any daily-denominator cost-screen artifact emitted earlier on 2026-06-03

Boundary:

No speed eligibility computation, no forecast computation, no diagnostics, no
backtests, no TEST, no VALIDATION, no Lockbox, no Forward, no deployment, no
trading, no promotion, no Git staging, no commit, no push, no PR, and no
remote operations were performed.
