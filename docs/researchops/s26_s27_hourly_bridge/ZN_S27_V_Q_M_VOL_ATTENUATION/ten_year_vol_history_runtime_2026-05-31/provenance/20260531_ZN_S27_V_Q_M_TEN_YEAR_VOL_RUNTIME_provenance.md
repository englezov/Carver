# Carver S27 ZN V/Q/M Ten-Year Vol Runtime Provenance

Status:

```text
PASS_S27_ZN_V_Q_M_TEN_YEAR_VOL_RUNTIME_LEDGER_DEV_RECON_ONLY
```

Gate: `S27_ZN_V_Q_M_TEN_YEAR_VOL_HISTORY_DATABENTO_EXECUTION_OR_FAIL_CLOSED_DECISION`

Boundary:

This artifact is a Development/Reconciliation runtime-dependency artifact only. It is not a strategy test and does not authorize diagnostics, backtests, positions, costs, carry, deployment, trading, promotion, OOS, Lockbox, Forward, Git, or remote repository operations.

Source method:

- Databento GLBX.MDP3 dated ZN daily `ohlcv-1d` contract rows only.
- Local additive back-adjusted dated-contract chain.
- Strategy-3-style EWMA(32) annualized percentage sigma.
- Ten-year rolling average using 2560 prior daily sigma observations.
- Historical quantile of relative volatility with no lookahead.
- EWMA(10) smoothing of `2 - 1.5 * Q`.
- Runtime rows align one-for-one to existing S26 hourly forecast rows and use only daily V/Q/M rows strictly before the S26 completed trading date.
