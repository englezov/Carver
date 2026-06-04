# S09 MES Risk Cost Unit Bridge Correction Result

Date: 2026-06-03

Status:

```text
CORRECTED_S09_MES_RISK_COST_UNIT_BRIDGE_ANNUALIZED_USD_RISK_NOT_BACKTEST
```

Correction:

- the earlier no-surviving-speed conclusion was unsafe
- USD round-turn cost must not be divided by the daily point-risk denominator alone
- corrected denominator: daily point risk * 16 * MES 5 USD/point multiplier
- locked daily point risk: 57.18365213859373
- locked annualized USD risk per contract: 4574.6921710874985

Corrected dual risk-adjusted cost values:

- conservative live futures pass-through: 2.93 / 4574.6921710874985 = 0.000640
- ETF simulated-fee all-in exchange/NFA-excluded: 2.49 / 4574.6921710874985 = 0.000544

Corrected speed screen:

- all six EWMAC spans survive under both cost scenarios
- locked speed rows: 12
- eligible speed set and Table 36 FDM remain separate downstream locks

Supersession:

Any 2026-06-03 artifact or statement that concluded no surviving speed from a
daily-denominator cost screen is superseded by this correction and by the
rewritten dual risk-adjusted-cost and dual speed-eligibility ledgers.

Boundary:

No forecast computation, diagnostics, returns, PnL, positions, carry,
backtests, TEST, VALIDATION, OOS, Lockbox, Forward, deployment, trading,
promotion, Git staging, commit, push, PR, or remote operations were performed.
