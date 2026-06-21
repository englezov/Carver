# Carver S27 ZN Lockbox Readiness Decision Gate

Status:

```text
DO_NOT_OPEN_LOCKBOX_EXECUTION_GATE_YET
```

Gate: `S27_ZN_LOCKBOX_READINESS_DECISION_GATE`

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Decision

Do **not** open the S27 ZN Lockbox execution gate yet.

Reason:

```text
FUTURES_REALISTIC_COST_READINESS_FAIL_CLOSED
```

The exact source-native S27 ZN variant has been frozen for readiness review, and a candidate untouched Lockbox window is identified, but futures-realistic cost readiness is fail-closed because the current cost chapter is still a manifest/shape definition rather than an executed cost-readiness ledger.

## Frozen Variant

```text
S27_ZN_SOURCE_NATIVE_M1_LADDER_DEV_RECON_VARIANT
```

Frozen hash ledger:

```text
docs/researchops/s26_s27_lockbox_readiness/ZN_S27/20260601_S27_ZN_LOCKBOX_READINESS_DECISION/freeze/20260601_S27_ZN_LOCKBOX_READINESS_DECISION_variant_hash_freeze.csv
```

The freeze includes the source atom sheet, EWMAC/V/Q/M closure record, 2022-2023 dev/recon result, 2024 validation-style result, robustness summary, MCPT/null-stack summary, futures cost shape/manifest records, and the local audit tools used to produce the robustness and MCPT artifacts.

## Window Decision

Excluded as already touched:

```text
2022-01-01 through 2023-12-31
2024-01-01 through 2024-12-31
2011-01-02 through 2026-05-22 daily signal/runtime support history
```

Earliest strict candidate after the current touch boundary:

```text
2026-05-23 through 2026-12-31
```

That candidate is not a completed historical window as of this gate. This gate does not access that window, download it, parse it, or authorize any Lockbox run.

## Cost Readiness

Cost readiness:

```text
FAIL_CLOSED_FUTURES_REALISTIC_COST_READINESS_NOT_EXECUTED
```

Fail-closed cost components:

```text
exchange_fee
clearing_nfa_regulatory_fee
broker_commission
zn_tick_value_and_multiplier
spread_slippage_grid
limit_order_fill_model
routing_and_margin_funding
breakeven_cost_per_side
unit_and_m1_ladder_cost_sensitivity
```

Machine-readable ledger:

```text
docs/researchops/s26_s27_lockbox_readiness/ZN_S27/20260601_S27_ZN_LOCKBOX_READINESS_DECISION/cost_readiness/20260601_S27_ZN_LOCKBOX_READINESS_DECISION_cost_readiness_ledger.csv
```

## Predeclared Later Lockbox Rules

Rules are frozen for a later separately authorized Lockbox gate but are not executed here:

- exact S27 ZN source-native M1 ladder variant only;
- post-2026-05-22 candidate window only, excluding touched 2022-2024 evidence and daily signal/runtime support history through 2026-05-22;
- futures-realistic costs must be locked before execution;
- primary metric is signal-attributable M1 minus matched-average-absolute-position beta, net of futures-realistic costs;
- primary signal-attributable net PnL must be positive;
- primary null `p <= 0.05` and max-T adjusted `p <= 0.10`;
- delayed/inverted/null contamination must not explain the result;
- no fill, drop, substitution, or degraded/unresolved provider rows;
- no promotion, Forward, deployment, or trading from a Lockbox pass.

## Non-Authorization

This decision gate authorizes no provider API access, no data download, no market-row parsing, no new diagnostics, no new backtest, no forecasts, no positions, no cost execution, no OOS, no Lockbox access, no Forward, no CFD adapter, no old QuantLab active pipeline, no tuning, no deployment, no trading, no promotion, no Git staging, no commit, no push, no PR update/opening, and no remote operations.
