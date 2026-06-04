# S09 MES Dual Speed Eligibility Values Subagent Hostile Audit Result

Supersession:

```text
SUPERSEDED_BY_CORRECTED_S09_MES_RISK_COST_UNIT_BRIDGE_ALL_SPEEDS_SURVIVE
```

This historical audit reviewed the earlier no-surviving-speed artifact and is
no longer current. The live corrected speed artifact has 12 eligible rows and
does not lock the eligible speed set or Table 36 FDM row. See
`docs/process/CARVER_S09_MES_RISK_COST_UNIT_BRIDGE_CORRECTION_RESULT_2026-06-03.md`.

Date: 2026-06-03

Status:

```text
PASS
```

Scope:

- row: APPENDIX_C_174_006
- root: MES
- lane: SOURCE_NATIVE_FUTURES
- machinery-development slice: 2019-05-05 through 2020-04-05
- evidence family: speed_eligibility_values

Checks performed:

- Re-read README.md, the Carver source-native research charter, the clean workspace migration record, and the lane classification / adapter quarantine rules.
- Verified the dual speed eligibility ledger exists at docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/speed/20260603_S09_MES_DUAL_SPEED_ELIGIBILITY_ledger.csv.
- Verified status JSON, provenance, result, local hostile audit, and SHA manifest are present.
- Verified both scenarios are present:
  - CONSERVATIVE_LIVE_FUTURES_PASS_THROUGH
  - ETF_SIM_FEE_ALL_IN_EXCHANGE_NFA_EXCLUDED
- Verified each scenario has exactly six spans: 2, 4, 8, 16, 32, 64.
- Verified threshold_sr is 0.15 on all rows.
- Recomputed annualized_cost_burden_sr as turnover * risk_adjusted_cost_per_trade_sr for all 12 rows; mismatches: 0.
- Verified all 12 eligible flags are False.
- Verified eligible_row_count is 0.
- Verified status is LOCKED_S09_MES_DUAL_SPEED_ELIGIBILITY_VALUES_NO_SURVIVING_SPEED_NOT_ELIGIBLE_SET_NOT_BACKTEST.
- Verified speed_eligibility_values_lock is YES_DUAL_SCENARIO.
- Verified eligible_speed_set_lock is NO.
- Verified table36_fdm_row_lock is NO.
- Verified backtests_run is NO.
- Verified TEST / VALIDATION / Lockbox / Forward access is NO.
- Verified Git operations are NO.
- Scanned locked speed artifacts for CFD_ADAPTER contamination and promotion markers; matches: 0.
- Verified SHA manifest records: 5; mismatches: 0.

Boundary confirmation:

No forecasts, diagnostics, backtests, TEST, VALIDATION, Lockbox, Forward, provider/API/network access, Git staging, commit, push, PR, remote operations, deployment, trading, or promotion were performed by this audit.

Concerns:

- No arithmetic, status, authorization-boundary, SHA, or source-native contamination concerns found.
- The dedicated separate subagent tool was not exposed in this session; this audit was performed under the same hostile-audit constraints and wrote only this requested result file.
