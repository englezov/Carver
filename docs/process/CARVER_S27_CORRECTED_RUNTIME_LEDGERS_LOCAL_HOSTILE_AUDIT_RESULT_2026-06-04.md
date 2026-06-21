# Carver S27 Corrected Runtime Ledgers Local Hostile Audit Result

Date: 2026-06-04

Mode: subagent local hostile audit over concrete corrected runtime ledgers and converted runner handoff. No provider/API access, no data download, no diagnostics, no backtest, no Git operation.

Auditor:

```text
subagent: 019e923c-e9a3-7ac2-afe4-4c9713a77448
nickname: Godel
```

## Verdict

```text
BLOCKING_FINDINGS: NONE
AUDIT_DISPOSITION: PASS_RUNTIME_LEDGER_HANDOFF_READY_FOR_SEPARATELY_AUTHORIZED_CORRECTED_S27_BACKTEST
```

The corrected runtime-ledger handoff is sufficient for a separately operator-authorized corrected S27 backtest to be run next, excluding the backtest itself.

## Evidence

The audit verified that exactly four root runtime CSVs exist under:

```text
docs/researchops/s26_s27_backtest_readiness/ZN_S27_SINGLE_INSTRUMENT/2022-01-01_2023-12-31/corrected_runtime_ledgers
```

The four root runtime CSVs are:

```text
s26_sigma_runtime_rows.csv
s26_daily_ewma5_equilibrium_runtime_rows.csv
s27_daily_ewmac16_64_trend_runtime_rows.csv
s27_daily_ten_year_vqm_runtime_rows.csv
```

Each has `11775` data rows.

All four CSVs have matching `as_of` sets:

```text
unique timestamps: 11775
first as_of: 2022-01-04T00:00:00Z
last as_of: 2023-12-29T22:00:00Z
```

All four headers include:

```text
source_artifact_sha256
forecast_target_source_artifact_sha256
```

The audit found no blank or malformed SHA-256 values.

## Runtime Labels

Corrected runtime and method labels are consistent across all rows:

```text
PREVALIDATED_S26_ZN_SIGMA_PERCENT_RUNTIME_VALUE
PREVALIDATED_S26_DAILY_BACK_ADJUSTED_EWMA5_EQUILIBRIUM_RUNTIME_VALUE
PREVALIDATED_S27_EWMAC16_TREND_RUNTIME_VALUE
PREVALIDATED_S27_V_Q_M_VOL_ATTENUATION_RUNTIME_VALUE
LOCKED_DAILY_S13_TEN_YEAR_V_Q_M_ATTENUATION_RUNTIME
```

The canonical constants are in:

```text
src/carver/spine/s26_s27.py
```

## No-Lookahead Evidence

All four ledgers have:

```text
no_lookahead_status: PASS_NO_LOOKAHEAD
```

Dependency dates are strictly prior with zero blanks or violations for sigma, equilibrium, trend, and V/Q/M.

## Status And Validation Evidence

The generated status JSON records:

```text
backtest_run: NO
diagnostics_run: NO
new_data_download: NO
provider_api_access: NO
oos_access: NO
lockbox_access: NO
forward_access: NO
status: PASS_S27_ZN_2022_2023_CORRECTED_RUNTIME_LEDGERS_NOT_BACKTEST
```

The generated validation ledger passes runtime row matching, no provider API access, no new data download, no diagnostics/backtest, and no OOS/Lockbox/Forward checks.

## Runner Handoff

The converted runner expects exactly the corrected runtime filenames:

```text
tools/databento/carver_s27_zn_2022_2023_retargeted_dev_recon_backtest.py
```

The authorization gates remain separate:

```text
runtime-ledger prep: CARVER_OPERATOR_AUTHORIZES_S27_RUNTIME_LEDGERS
backtest runner:     CARVER_OPERATOR_AUTHORIZES_S27_BACKTEST
```

Runtime-ledger readiness alone is not backtest authorization.

## Non-Authorization

This audit authorizes no provider/API call, no data download, no diagnostics, no backtest, no returns, no PnL, no positions, no OOS, no Lockbox, no Forward, no deployment, no trading, no promotion, no Git staging, no commit, no push, and no PR.
