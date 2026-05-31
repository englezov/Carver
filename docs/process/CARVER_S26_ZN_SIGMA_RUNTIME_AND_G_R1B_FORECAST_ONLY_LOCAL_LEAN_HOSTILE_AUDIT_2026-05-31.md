# Carver S26 ZN Sigma Runtime And G_R1B Forecast-Only Local Lean Hostile Audit

Date: 2026-05-31

Mode:

```text
LOCAL_LEAN_HOSTILE_AUDIT_RESULT_G_R1B_PASS_FORECAST_ONLY_WITH_SIGMA_SCOPE_LABEL
```

## Scope Audited

Audited artifacts:

```text
docs/process/CARVER_S26_ZN_SIGMA_RUNTIME_AND_G_R1B_FORECAST_ONLY_EXECUTION_RESULT_2026-05-31.md
docs/researchops/s26_s27_hourly_bridge/ZN_S26_WORKED_EXAMPLE/2026-05-18_2026-05-22/sigma_percent_runtime/2026-05-31/runtime/20260531_G_R1B_ZNM6_sigma_percent_runtime_value.json
docs/researchops/s26_s27_hourly_bridge/ZN_S26_WORKED_EXAMPLE/2026-05-18_2026-05-22/forecast_only_output/2026-05-31/forecast_rows/20260531_G_R1B_ZNM6_S26_forecast_output_only.csv
docs/researchops/s26_s27_hourly_bridge/ZN_S26_WORKED_EXAMPLE/2026-05-18_2026-05-22/forecast_only_output/2026-05-31/provenance/20260531_G_R1B_ZNM6_S26_forecast_output_only_status.json
```

## Findings

### Critical

None.

No artifact emits or authorizes returns, PnL, Sharpe, drawdown, diagnostics, backtests, positions, orders, costs, carry, trend computation, S27 overlay, OOS, Lockbox, Forward, deployment, trading, promotion, Git operations, or remote operations.

### High

None.

The forecast output is one row and is labeled:

```text
S26_FORECAST_OUTPUT_ONLY_NOT_DIAGNOSTIC_NOT_BACKTEST_NOT_POSITION
```

The input identity remains:

```text
APPENDIX_C_172_004 / ZN / 42000661 / ZNM6
```

### Medium

M-1. Sigma runtime method is intentionally narrower than a full S03 position-sizing blend.

The runtime value uses the short-run EWMA(32) annualized percentage-return current-risk component, not a full S03 long-run/short-run blended position-sizing risk estimate. This is acceptable only for the current S26 forecast-price-risk bridge because the execution result explicitly labels:

```text
NOT_FULL_S03_POSITION_SIZING_BLEND
```

and does not emit position sizing. A future position-sizing, S09/S10/S11, or portfolio gate must not reuse this runtime value as a full variable-risk estimate.

### Low

L-1. Source window is short by design.

The ZNM6 source window has 34 daily rows and 33 returns after excluding degraded provider-condition rows and avoiding the 2026-05-22 same-day daily row. This is sufficient for the bounded G_R1B bridge but is not a production volatility history.

## Verdict

```text
BLOCKING_FINDINGS: NO
AUDIT_DISPOSITION: PASS_G_R1B_S26_ZN_HOURLY_FORECAST_OUTPUT_ONLY_SCOPE
```

## Non-Authorization

This audit authorizes no additional provider API access, no additional data download, no market-row expansion, no diagnostics, no backtests, no returns, no PnL, no Sharpe, no drawdown, no positions, no orders, no costs, no carry, no trend computation, no S27 overlay, no volatility/risk use beyond the explicitly recorded S26 sigma runtime value, no OOS, no Lockbox, no Forward, no CFD adapters, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.
