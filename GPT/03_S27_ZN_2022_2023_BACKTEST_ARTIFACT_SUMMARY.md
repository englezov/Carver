# S27 ZN 2022-2023 100k Development/Reconciliation Backtest Artifact Summary

Status:

```text
PASS_S27_ZN_M1_STYLE_LADDER_DEV_RECON_BACKTEST_NOT_ALPHA
```

## Corrected Result

Main status artifact:

```text
docs/researchops/s26_s27_m1_ladder/ZN_S27/2022-01-01_2023-12-31/status/20260531_S27_ZN_M1_LADDER_DEV_RECON_BACKTEST_status.json
SHA256: 7A1F05915BD3E189268F73125E2C0F8442A716B5787AAAB2A54158F79FF496BA
```

Status summary:

```text
gate: S27_ZN_M1_STYLE_SIZING_LADDER_DEV_RECON_BACKTEST
status: PASS_S27_ZN_M1_STYLE_LADDER_DEV_RECON_BACKTEST_NOT_ALPHA
requested_window: 2022-01-01 through 2023-12-31
effective_window: 2022-01-04 through 2023-12-29
capital_usd: 100000.0
target_risk: 0.20
instrument_weight: 1.0
IDM: 1.0
ZN multiplier: 1000.0
FX: 1.0
forecast_to_position_divisor: 10.0
rounding_policy: NEAREST
source_daily_runtime_lag_policy: STRICT_PRIOR_GT_0_AND_NON_STALE_MAX_10_DAYS
source_daily_runtime_lag_max_days: 1
```

Row counts:

```text
source_hourly_rows: 11775
blocked_dependency_rows_before_ladder: 4
forecast_rows: 11771
ladder_rows: 11771
position_rows: 11771
backtest_rows: 11770
```

Position distribution:

```text
-8: 3
-7: 10
-6: 16
-5: 37
-4: 69
-3: 143
-2: 315
-1: 1372
0: 9233
1: 489
2: 64
3: 15
4: 2
5: 1
6: 2
```

PnL and fees:

```text
gross_pnl_usd: 10343.75
position_change_sides: 3306
roll_transition_fee_sides: 6
total_fee_sides: 3312
estimated_etf_fees_usd: 5001.12
net_after_etf_fees_usd: 5342.630000000004
cost_status: ETF_PUBLIC_PER_SIDE_COMMISSION_ONLY_NO_SPREAD_OR_SLIPPAGE
```

Non-authorization fields in the status:

```text
provider_api_access: NO
new_data_download: NO
diagnostics_run: NO_SHARPE_NO_DRAWDOWN_NO_ALPHA_STATISTICS
oos_access: NO
lockbox_access: NO
forward_access: NO
deployment: NO
trading: NO
promotion: NO
git_operations: NO
```

## Key CSV Artifacts

Base position ladder:

```text
docs/researchops/s26_s27_m1_ladder/ZN_S27/2022-01-01_2023-12-31/ladder_rows/20260531_S27_ZN_M1_LADDER_DEV_RECON_BACKTEST_base_position_ladder_rows.csv
SHA256: 59CEE99A514900D2944B92D0A25645A118F65496C410BF36FA3DBE8D467E4659
rows: 11771
columns: 25
first accepted timestamp: 2022-01-04T04:00:00Z
last accepted timestamp: 2023-12-29T22:00:00Z
first source daily runtime date: 2022-01-03
last source daily runtime date: 2023-12-28
```

Desired positions:

```text
docs/researchops/s26_s27_m1_ladder/ZN_S27/2022-01-01_2023-12-31/position_rows/20260531_S27_ZN_M1_LADDER_DEV_RECON_BACKTEST_desired_position_rows.csv
SHA256: 2ACE24564B68B5AF309389F44C7D533B396C28D8D5972451933ECBC74D487D1E
rows: 11771
columns: 17
integer futures sizing only: YES
```

Backtest rows:

```text
docs/researchops/s26_s27_m1_ladder/ZN_S27/2022-01-01_2023-12-31/backtest_rows/20260531_S27_ZN_M1_LADDER_DEV_RECON_BACKTEST_ladder_backtest_rows.csv
SHA256: 034C0491677E7676178D4E65F692E2AF338A7B163D352887B56809DDCF0D25CF
rows: 11770
columns: 25
first entry: 2022-01-04T04:00:00Z
last exit: 2023-12-29T22:00:00Z
```

S27 forecast rows:

```text
docs/researchops/s26_s27_backtest_readiness/ZN_S27_SINGLE_INSTRUMENT/2022-01-01_2023-12-31/retargeted_dev_recon_backtest/forecast_rows/20260531_S27_ZN_2022_2023_RETARGETED_DEV_RECON_BACKTEST_s27_forecast_rows.csv
SHA256: 6409165FAD733A77E1FF0E74683080C10D4AAD9A75AB5914A2E8FAB721BF1A9D
rows: 11771
columns: 24
```

Local extended daily runtime:

```text
docs/researchops/s26_s27_backtest_readiness/ZN_S27_SINGLE_INSTRUMENT/2022-01-01_2023-12-31/local_extended_daily_runtime/runtime_rows/20260531_S27_ZN_2022_2023_LOCAL_EXTENDED_DAILY_RUNTIME_daily_runtime_rows.csv
SHA256: F54CA0DCC34E5F15C58A0412E8CAFB6E0A3F9176EFEA7B408E069268639EFB18
rows: 4750
columns: 11
window: 2011-01-02 through 2026-05-22
```

## Superseded Fail-Closed Result

The prior stale-runtime result must not be accepted as evidence.

Fail-closed status artifact:

```text
docs/researchops/s26_s27_m1_ladder/ZN_S27/2022-01-01_2023-12-31/status/20260531_S27_ZN_M1_LADDER_DEV_RECON_BACKTEST_SUPERSEDED_FAIL_CLOSED_status.json
SHA256: DF3CA3882A2053F7F48075E0AA0482E0E287C5EBDEF2471BD7DE1D016734094B
status: SUPERSEDED_FAIL_CLOSED_STALE_DAILY_RUNTIME_DEPENDENCY
```

Supersession reason:

```text
S27 forecast rows feeding the ladder used source_vqm_completed_trading_date=2020-12-21 for all 2022-2023 hourly rows, creating a 378-day stale runtime lag on the first 2022 row.
```

First observed fail-closed stale row:

```text
derived_completed_bar_end_utc: 2022-01-03T05:00:00Z
completed_trading_date: 2022-01-03
source_vqm_completed_trading_date: 2020-12-21
runtime_lag_days: 378
```

