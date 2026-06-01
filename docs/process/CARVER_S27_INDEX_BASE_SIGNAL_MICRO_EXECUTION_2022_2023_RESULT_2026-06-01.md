# Carver S27 ES Base Signal To MES Micro Futures Execution 2022-2023 Result

Status:

```text
PASS_S27_INDEX_BASE_SIGNAL_MICRO_FUTURES_EXECUTION_DEV_RECON_ARTIFACTS_CREATED_NOT_ALPHA
```

Gate: `S27_INDEX_BASE_SIGNAL_MICRO_FUTURES_EXECUTION_DEV_RECON`

## Summary

| Pair | Signal | Execution | Status | Effective Window | Gross | Fees | Net | External Adapter Gate | Blocker |
|---|---|---|---|---|---:|---:|---:|---|---|
| ES_SIGNAL_TO_MES_EXECUTION | ES | MES | PASS_S27_INDEX_BASE_SIGNAL_TO_MICRO_FUTURES_EXECUTION_DEV_RECON_NOT_ALPHA | 2022-01-03 to 2023-12-29 | -4991.25 | 797.44 | -5788.6900000000005 | CFD_ADAPTER_GATE_REQUIRED_SEPARATE_NOT_OPENED |  |

## Interpretation

This ES-first gate uses ES as the source-native base-futures signal authority because MES does not have enough daily history to support the S27 V/Q/M runtime. MES is treated only as the micro futures execution variant using its own hourly execution bars.

NQ to MNQ is not part of this result. The interrupted NQ attempt remains unfinished and must not be treated as pass, fail, or zero PnL until a separate bounded run is completed.

Any CFD adapter is outside this source-native futures artifact and requires a separate explicit gate. No CFD broker data, session, spread, swap, fill, or symbol mapping was accessed or used.

This is Development/Reconciliation only. It is not alpha, OOS, Lockbox, Forward, deployment, trading, promotion, or a production sizing/cost lock.
