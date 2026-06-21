# Carver S27 ZN Futures-Realistic Cost Test Manifest Record

Status:

```text
PROCESS_ONLY_COST_TEST_MANIFEST_DEFINED_NOT_EXECUTED
```

## Scope

This record preserves the machine-readable cost-test manifest required by the S27 ZN pre-Lockbox robustness protocol.

Manifest:

```text
docs/researchops/s26_s27_cost_model/ZN_S27/CARVER_S27_ZN_FUTURES_REALISTIC_COST_TEST_MANIFEST_2026-06-01.csv
```

## Boundary

The manifest defines tests only. It does not execute a futures-realistic cost model and does not close Opus CRITICAL-1.

Before any Lockbox-facing interpretation, a later gate must still lock or fail-close:

- exchange, clearing, NFA/regulatory, broker, routing, and margin/funding assumptions;
- ZN tick value and fee side counts;
- spread/slippage scenarios;
- limit-order fill and no-fill policy;
- breakeven cost per side;
- separate unit/no-ladder and M1-ladder cost sensitivity.

## Non-Authorization

This record authorizes no provider API access, no new data download, no market-row parsing, no new diagnostics, no backtests, no forecasts, no positions, no cost execution, no OOS, no Lockbox, no Forward, no CFD adapters, no old QuantLab active-pipeline use, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.
