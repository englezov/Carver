# S09 MES Spread Slippage TBBO Source-Native Extraction And Degraded-Day Policy Lock Hostile Audit Result

Date: 2026-06-03

Status:

```text
ARTIFACT_HASH_VERIFIED_S09_MES_SPREAD_SLIPPAGE_TBBO_LOCK_NO_RAW_DBN_RESCAN_NO_BACKTEST
```

Mode:

Operator instructed final verification using written artifacts and SHA manifests
only. No raw Databento DBN files were rescanned during this completion pass.
The previously launched separate audit worker was interrupted by the operator
before it wrote this file; this result is therefore an artifact/hash hostile
audit completion record at the requested path.

Scope verified:

- lane_class: SOURCE_NATIVE_FUTURES
- source_row: APPENDIX_C_174_006
- root: MES
- provider/dataset/schema: Databento GLBX.MDP3 TBBO
- machinery_development_slice: 2019-05-05 through 2020-04-05
- degraded_provider_dates: 2020-02-27 and 2020-02-28
- degraded_day_policy: EXCLUDE_DEGRADED_PROVIDER_DAYS_FROM_ESTIMATOR_PRESERVE_IN_QUARANTINE

Artifact checks:

- summary rows: 5 MES contract files represented
- valid_quote_rows_used: 30519879
- degraded_quote_rows_excluded: 936077
- crossed_or_empty_rows_rejected: 619
- median_spread_points: 0.25
- locked_spread_slippage_round_turn_usd: 1.25
- charge_timing: ROUND_TURN
- cost ledger rows: exactly 4 complete historical cost component rows
- cost components: exchange_fee, clearing_regulatory_fee, broker_commission, spread_slippage
- historical cost status: LOCKED_S09_MES_HISTORICAL_COST_VALUES_NOT_RISK_ADJUSTED_COST
- total_round_turn_cost_per_trade_currency: 2.93

SHA manifest checks:

- spread_slippage_tbbo_source_native_extraction manifest: 7 entries, 0 mismatches
- historical_cost_value manifest: 3 entries, 0 mismatches
- historical_cost_source_extraction manifest: 57 entries, 0 mismatches

Boundary checks:

- no risk-adjusted cost computation
- no speed eligibility computation
- no forecast computation
- no diagnostics
- no backtests
- no TEST
- no VALIDATION
- no Lockbox
- no Forward
- no deployment
- no trading
- no promotion
- no Git staging
- no commit
- no push
- no PR
- no remote operations
- READY_FOR_BACKTEST absent
- READY_FOR_LOCKBOX absent

Finding:

No artifact/hash inconsistency found in the written spread/slippage extraction,
historical cost value, or cost-source evidence manifests. The lock is bounded to
complete historical cost component evidence only and does not authorize the next
risk-adjusted-cost, speed eligibility, strategy-readiness, diagnostic, backtest,
TEST, VALIDATION, Lockbox, Forward, deployment, trading, promotion, or Git stage.
