# S27_V2 Pre-2023 Controlled Development/Reconciliation Run Implementation

Date: 2026-06-11

Status:

```text
LOCAL_CONTROLLED_DEV_RECON_RUN_EMITTED_NOT_RESULT_NOT_PROMOTION
```

Authorization:

```text
S27_V2_CONTROLLED_LOCAL_ONLY_DEVELOPMENT_RECON_RUN_PRE2023_ZN
```

## Scope

This gate used the locally audited pre-2023 ZN declared input pack:

```text
docs/researchops/s27_v2_local_replay_inputs/ZN/20260611_pre2023_oldest_dev_recon_2022_declared_pack
```

The run output was written to:

```text
docs/researchops/s27_v2_local_replay_runs/ZN/20260611_pre2023_oldest_dev_recon_2022_controlled_run
```

This is Development/Reconciliation mechanical run construction only. It is not a
TEST, VALIDATION, OOS, Lockbox, Forward, result-scored run, result
interpretation, PnL evaluation, promotion, trading, deployment, or
source-faithful evidence claim.

## Code And Tests

Code:

```text
src/carver/spine/s27_v2_replay/development_recon_run.py
```

Focused tests:

```text
tests/test_s27_v2_development_recon_run.py
```

Verification:

```text
python -m py_compile src\carver\spine\s27_v2_replay\development_recon_run.py src\carver\spine\s27_v2_replay\multi_row_development_runner.py
python -m pytest tests\test_s27_v2_development_recon_run.py tests\test_s27_v2_pre2023_databento_pack.py tests\test_s27_v2_multi_row_development_runner.py -q
50 passed
```

## Selected Row

```text
raw_symbol = ZNH2
selected_decision_timestamp_utc = 2022-01-03T01:00:00Z
selected_fill_timestamp_utc = 2022-01-03T02:00:00Z
selected_previous_daily_timestamp_utc = 2021-12-31T00:00:00Z
```

Point-in-time level binding:

```text
point_in_time_roll_cutoff_date = 2021-12-31
future_roll_deltas_after_cutoff_excluded = YES
daily_current_raw_close = 130.34375
daily_continuous_close = 130.34375
hourly_decision_close = 130.34375
```

## Mechanical Ledger Outputs

Forecast:

```text
ewma5_equilibrium_value = 130.44663094825498
raw_mean_reversion_forecast_value = 0.10288094825497751
sigma_price_value = 0.3803519871778355
risk_adjusted_forecast_before_veto_value = 0.2704887886043172
ewmac16_64_trend_value = 0.2528923936318108
trend_veto_decision = PERMIT_MEAN_REVERSION
capped_forecast_value = 4.894376401547715
```

Desired position:

```text
base_position_contracts = 16.432147617721743
desired_unrounded_contracts = 8.04251155269258
desired_position_contracts = 8
position_change_contracts = 8
```

Order/fill/cost:

```text
order_side = BUY
order_quantity = 8
adjacent_target_position = 1
formula_implied_limit_price = 130.43383880644942
limit_order_price = 130.421875
fill_candidate_close = 130.328125
fill_executed = TRUE
fill_price = 130.421875
commission_amount = 18.4 USD
spread_cost_amount = 0.0 USD
```

PnL/result:

```text
pnl_status = FAIL_CLOSED_ACTUAL_PNL_LEDGER_NOT_EMITTED_VALUATION_MARK_ROW_NOT_DECLARED
result_status = FAIL_CLOSED_RESULT_ROW_NOT_EMITTED_NOT_AUTHORIZED
```

No actual PnL ledger row is emitted because no post-fill valuation mark row is
declared for this 2022 run. The PnL ledger artifact is fail-closed metadata
only.

## Hashes

```text
run_bundle.json = 7668d2f2212d382355efc00ca80e2345e7418b32661fc4c4612ede9ef6a0ad30
run_manifest.json = a72939853fc3acffcb48122dec689fd22dbc30bcc2136cb142007a41acd28553
trusted_bundle.json = 8cc16c9d7100f67090c2ea6f80c220e4edd0eb86eddabf85e86f776634350368
```

## Non-Authorizations

This record does not authorize provider/API access, downloads, new data
acquisition, TEST, VALIDATION, OOS, Lockbox, Forward, result interpretation, PnL
evaluation beyond mechanical row construction, tuning, adapter work, deployment,
trading, promotion, Git staging/commit/push/PR, or source-faithful evidence
claims.
