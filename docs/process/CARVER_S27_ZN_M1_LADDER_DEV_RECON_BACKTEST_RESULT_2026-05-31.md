# Carver S27 ZN M1-Style Sizing Ladder Dev/Reconciliation Backtest Result

Status:

```text
PASS_S27_ZN_M1_STYLE_LADDER_DEV_RECON_BACKTEST_NOT_ALPHA
```

Supersession:

```text
SUPERSEDES_R2_COMPARISON_FED_RESULT_FAIL_CLOSED_STALE_DAILY_RUNTIME_DEPENDENCY
```

Superseded fail-closed record: `docs\researchops\s26_s27_m1_ladder\ZN_S27\2022-01-01_2023-12-31\status\20260531_S27_ZN_M1_LADDER_DEV_RECON_BACKTEST_SUPERSEDED_FAIL_CLOSED_status.json`.

Gate: `S27_ZN_M1_STYLE_SIZING_LADDER_DEV_RECON_BACKTEST`

## Dev/Reconciliation Ladder Inputs

- Capital: `$100000.0`.
- Target risk: `0.2`.
- Instrument weight: `1.0`.
- IDM: `1.0`.
- ZN multiplier: `1000.0`.
- FX: `1.0`.
- Annual risk source: `S27_RUNTIME_SIGMA_PRICE_BRIDGE_DERIVED_ANNUAL_RISK_NO_LOOKAHEAD`.
- Daily runtime lag policy: `STRICT_PRIOR_GT_0_AND_NON_STALE_MAX_10_DAYS`.
- Max accepted daily runtime lag: `1`.
- Forecast-to-position divisor: `10.0`.
- Rounding policy: `NEAREST`.

## Result

- Requested window: `2022-01-01` through `2023-12-31`.
- Effective backtest window: `2022-01-04` through `2023-12-29`.
- Source forecast status: `PASS_RETARGETED_S27_ZN_DEV_RECON_UNIT_PLUMBING_NO_COST_BACKTEST_NOT_ALPHA`.
- Blocked dependency rows before ladder: `4`.
- Forecast rows: `11771`.
- Ladder rows: `11771`.
- Backtest rows: `11770`.
- Rounded position counts: `{-8: 3, -7: 10, -6: 16, -5: 37, -4: 69, -3: 143, -2: 315, -1: 1372, 0: 9233, 1: 489, 2: 64, 3: 15, 4: 2, 5: 1, 6: 2}`.
- Position-change sides: `3306`.
- Roll-transition fee sides: `6`.
- Total fee sides: `3312`.
- Gross PnL: `$10343.75`.
- Estimated ETF fees: `$5001.12`.
- Net after ETF fees: `$5342.630000000004`.

## Boundary

This is Development/Reconciliation only. It uses existing local retargeted ZN source-native quarantine artifacts only. The effective window may be narrower than the requested 2022-2023 window because only source hourly rows with strict prior daily sigma/trend/V/Q/M runtime are accepted; any missing rows remain blocked rather than filled or reused from stale runtime. It is not OOS, not Lockbox, not Forward, not deployment, not trading, and not promotion. Costs are ETF public per-side commission only; spread, slippage, prop-firm drawdown rules, margin, order-fill quality, and capital constraints beyond the locked capital number remain outside this gate.
