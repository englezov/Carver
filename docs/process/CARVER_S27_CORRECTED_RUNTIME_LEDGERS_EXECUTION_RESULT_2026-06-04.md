# Carver S27 Corrected Runtime Ledgers Execution Result

Date: 2026-06-04

Lane: SOURCE_NATIVE_FUTURES

Status:

```text
PASS_S27_ZN_2022_2023_CORRECTED_RUNTIME_LEDGERS_NOT_BACKTEST
```

## Authorization

The operator authorized corrected runtime-ledger creation only.

Execution used:

```text
CARVER_OPERATOR_AUTHORIZES_S27_RUNTIME_LEDGERS=AUTHORIZED_CORRECTED_S27_ZN_2022_2023_RUNTIME_LEDGERS
```

This was not backtest authorization.

## Command

```text
python tools/databento/carver_s27_zn_2022_2023_corrected_runtime_ledgers.py
```

## Output Root

```text
docs/researchops/s26_s27_backtest_readiness/ZN_S27_SINGLE_INSTRUMENT/2022-01-01_2023-12-31/corrected_runtime_ledgers
```

## Runtime CSVs

```text
s26_sigma_runtime_rows.csv
s26_daily_ewma5_equilibrium_runtime_rows.csv
s27_daily_ewmac16_64_trend_runtime_rows.csv
s27_daily_ten_year_vqm_runtime_rows.csv
```

Each runtime CSV has `11775` rows.

Observed forecast target coverage:

```text
first as_of: 2022-01-04T00:00:00Z
last as_of:  2023-12-29T22:00:00Z
first completed trading date: 2022-01-04
last completed trading date:  2023-12-29
```

## File Sizes And Hashes

```text
s26_sigma_runtime_rows.csv
size: 5906035 bytes
sha256: 128598FDBEFEF56AB74D82BF2E6CA38386C62780D23B7A346D177B79B68A917B

s26_daily_ewma5_equilibrium_runtime_rows.csv
size: 6095290 bytes
sha256: 534740DD88E3DD396991EDC477D8BFB1FC7680BBBA5B833D58878A2D33CE2F3B

s27_daily_ewmac16_64_trend_runtime_rows.csv
size: 6100846 bytes
sha256: 6AE50B702A63C20972976637973D51A9A9ED603DB409C6E54FA7F59CF096A260

s27_daily_ten_year_vqm_runtime_rows.csv
size: 6234621 bytes
sha256: 0636621516FF626686A372F5BFDAD9ABAA81D92EC2C22E410B63F039A537065B
```

## Label Verification

Observed runtime and method labels:

```text
s26_sigma_runtime_rows.csv
runtime_status: PREVALIDATED_S26_ZN_SIGMA_PERCENT_RUNTIME_VALUE
method_status: LOCKED_TO_PART_ONE_S03_VARIABLE_RISK_FAMILY

s26_daily_ewma5_equilibrium_runtime_rows.csv
runtime_status: PREVALIDATED_S26_DAILY_BACK_ADJUSTED_EWMA5_EQUILIBRIUM_RUNTIME_VALUE
method_status: LOCKED_DAILY_BACK_ADJUSTED_EWMA5_EQUILIBRIUM_RUNTIME

s27_daily_ewmac16_64_trend_runtime_rows.csv
runtime_status: PREVALIDATED_S27_EWMAC16_TREND_RUNTIME_VALUE
method_status: LOCKED_DAILY_EWMAC16_64_TREND_OVERLAY_RUNTIME

s27_daily_ten_year_vqm_runtime_rows.csv
runtime_status: PREVALIDATED_S27_V_Q_M_VOL_ATTENUATION_RUNTIME_VALUE
method_status: LOCKED_DAILY_S13_TEN_YEAR_V_Q_M_ATTENUATION_RUNTIME
```

All rows had:

```text
no_lookahead_status: PASS_NO_LOOKAHEAD
source_artifact_sha256: present
forecast_target_source_artifact_sha256: present
```

## Status Claims

The generated status JSON records:

```text
provider_api_access: NO
new_data_download: NO
diagnostics_run: NO
backtest_run: NO
position_output: NO
oos_access: NO
lockbox_access: NO
forward_access: NO
deployment: NO
trading: NO
promotion: NO
git_operations: NO
validation_status: PASS
```

## Remaining Gate

Before any corrected S27 backtest can run:

1. Ask the operator for explicit corrected S27 backtest authorization.

The local hostile audit over the concrete runtime ledgers and converted runner is recorded in:

```text
docs/process/CARVER_S27_CORRECTED_RUNTIME_LEDGERS_LOCAL_HOSTILE_AUDIT_RESULT_2026-06-04.md
```

## Non-Authorization

This result authorizes no provider/API call, no data download, no diagnostics, no backtest, no returns, no PnL, no positions, no OOS, no Lockbox, no Forward, no deployment, no trading, no promotion, no Git staging, no commit, no push, and no PR.
