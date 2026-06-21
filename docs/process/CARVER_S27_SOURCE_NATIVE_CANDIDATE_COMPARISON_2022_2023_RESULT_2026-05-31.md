# Carver S27 Source-Native Candidate Comparison 2022-2023 Result

Status:

```text
PASS_S27_SOURCE_NATIVE_CANDIDATE_COMPARISON_DEV_RECON_ARTIFACTS_CREATED_NOT_ALPHA
```

Gate: `S27_SOURCE_NATIVE_CANDIDATE_COMPARISON_2022_2023_DEV_RECON`

## Summary

| Root | Group | Status | Effective Window | Gross | ETF Fees | Net | Blocker |
|---|---:|---|---|---:|---:|---:|---|
| ZT | bond | PASS_S27_CANDIDATE_DEV_RECON_UNIT_PLUMBING_ETF_COST_BACKTEST_NOT_ALPHA | 2022-01-03 to 2023-12-29 | -10062.5 | 8181.76 | -18244.260000000002 |  |
| ZF | bond | PASS_S27_CANDIDATE_DEV_RECON_UNIT_PLUMBING_ETF_COST_BACKTEST_NOT_ALPHA | 2022-01-03 to 2023-12-29 | -250.0 | 8107.499999999999 | -8357.499999999995 |  |
| ZN | bond | PASS_S27_CANDIDATE_DEV_RECON_UNIT_PLUMBING_ETF_COST_BACKTEST_NOT_ALPHA | 2022-01-03 to 2023-12-29 | 22406.25 | 5889.0 | 16517.250000000004 |  |
| MES | index | FAIL_CLOSED_S27_CANDIDATE_COMPARISON_NOT_EXECUTABLE |  to  |  |  |  | insufficient daily sigma rows for ten-year V/Q/M: 473 |
| MNQ | index | FAIL_CLOSED_S27_CANDIDATE_COMPARISON_NOT_EXECUTABLE |  to  |  |  |  | insufficient daily sigma rows for ten-year V/Q/M: 473 |

## Boundary

This is Development/Reconciliation only. It uses source-native futures Databento rows, local dated-contract continuous construction, S27 forecast machinery, unit-base position plumbing, and ETF public per-side commission-only costs. It is not an alpha claim, not OOS, not Lockbox, not Forward, not deployment, not trading, and not promotion.

The authoritative comparison artifacts are the `R2` artifacts. Earlier non-`R2` same-day partial artifacts were superseded after fixing daily dated-contract request envelopes so one-digit futures symbols are not requested across ambiguous decade windows.
