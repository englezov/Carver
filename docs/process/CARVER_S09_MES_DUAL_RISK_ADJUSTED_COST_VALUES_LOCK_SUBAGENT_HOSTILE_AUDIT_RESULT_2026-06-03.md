# S09 MES Dual Risk-Adjusted Cost Values Subagent Hostile Audit

Supersession:

```text
SUPERSEDED_BY_CORRECTED_S09_MES_RISK_COST_UNIT_BRIDGE_ANNUALIZED_USD_RISK
```

This historical audit reviewed the earlier daily-denominator artifact and is no
longer current. The live corrected artifact is the annualized USD risk bridge:
daily point risk * 16 * MES 5 USD/point multiplier. See
`docs/process/CARVER_S09_MES_RISK_COST_UNIT_BRIDGE_CORRECTION_RESULT_2026-06-03.md`.

Date: 2026-06-03

Result:

```text
PASS
```

Scope audited:

- S09 MES Appendix C row `APPENDIX_C_174_006`
- machinery-development slice `2019-05-05 through 2020-04-05`
- ledger `docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/cost/20260603_S09_MES_DUAL_RISK_ADJUSTED_COST_ledger.csv`
- status JSON, provenance, result, local audit, and SHA manifest

Checks performed:

- Re-read required Carver guardrails: README, source-native charter, clean workspace migration record, and lane classification/quarantine rules.
- Confirmed lane remains `SOURCE_NATIVE_FUTURES`.
- Confirmed ledger contains exactly two scenarios.
- Confirmed `CONSERVATIVE_LIVE_FUTURES_PASS_THROUGH` value is `0.051238`, recomputed from `2.93 / 57.18365213859373`.
- Confirmed `ETF_SIM_FEE_ALL_IN_EXCHANGE_NFA_EXCLUDED` value is `0.043544`, recomputed from `2.49 / 57.18365213859373`.
- Confirmed status is `LOCKED_S09_MES_DUAL_RISK_ADJUSTED_COST_VALUES_NOT_SPEED_NOT_BACKTEST`.
- Confirmed `scenario_count=2`.
- Confirmed `speed_eligibility_computation=NO`.
- Confirmed `backtests_run=NO`.
- Confirmed `test_validation_lockbox_forward_access=NO`.
- Confirmed `git_operations=NO`.
- Confirmed no `CFD_ADAPTER` marker in the audited dual risk-adjusted-cost artifacts.
- Confirmed no `READY_FOR_BACKTEST` or `READY_FOR_LOCKBOX` marker in the audited dual risk-adjusted-cost artifacts.
- Confirmed SHA manifest has zero mismatches against current file hashes.

Concerns:

- No arithmetic, status, boundary, scenario-count, or SHA concerns found.
- The audited artifacts correctly remain a risk-adjusted-cost lock only. They do not authorize or perform speed eligibility, forecasts, diagnostics, backtests, TEST, VALIDATION, Lockbox, Forward, deployment, trading, promotion, Git staging, commit, push, PR, provider/API access, network access, or remote operations.
