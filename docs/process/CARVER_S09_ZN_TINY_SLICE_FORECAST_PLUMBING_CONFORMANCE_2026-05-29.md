# Carver S09 ZN Tiny-Slice Forecast Plumbing Conformance

Date: 2026-05-29

Status:

```text
CARVER_S09_ZN_TINY_SLICE_FORECAST_PLUMBING_CONFORMANCE_COMPLETE_NOT_DIAGNOSTIC_NOT_BACKTEST
```

## Purpose

Run the first narrow S09 forecast-construction plumbing check on the ready source-native ZN continuous daily chain.

This is a machinery conformance artifact only. It verifies that completed daily ZN bars can flow through the S09 EWMAC32/EWMAC64 forecast block after the ZN continuous-readiness gate.

## Prior Gates

```text
docs/process/CARVER_S09_REAL_DATA_READINESS_GATE_2026-05-29.md
docs/process/CARVER_ZN_NATIVE_DAILY_EXPORT_PARSER_VALIDATION_2026-05-29.md
docs/process/CARVER_ZN_CONTINUOUS_CONSTRUCTION_READINESS_GATE_2026-05-29.md
```

## Locked Scope

```text
lane class: SOURCE_NATIVE_FUTURES
instrument: ZN
source contract months: 09-25, 12-25, 03-26, 06-26
roll dates inherited from readiness gate: 2025-09-22, 2025-12-22, 2026-03-23
available adjusted completed daily rows: 259
tiny-slice input rows consumed: 257
first input date consumed: 2025-06-02
as-of completed date: 2026-05-28
eligible S09 speeds: EWMAC32, EWMAC64
```

The conformance code consumes exactly the last `257` adjusted completed daily rows, matching the S09 warm-up boundary for EWMAC64's slow leg (`64 * 4 = 256`) plus one completed bar.

## Price-Risk Sentinel

This pass uses:

```text
price_risk_mode: UNIT_PRICE_RISK_CONFORMANCE_ONLY_NOT_SOURCE_RISK
daily_price_risk_value: 1.0
interpretable_signal: FALSE
```

The daily price-risk source is not settled by this artifact. Therefore the forecast output below is plumbing metadata only. It is not a source-interpretable S09 signal, not a trading signal, not a performance result, and not promotion evidence.

Before any interpretable S09 signal, diagnostic, or strategy evaluation, a separate gate must lock the daily price-risk source atom.

## Plumbing Output Metadata

```text
final_forecast_unit_risk_only: -1.87693350348
EWMAC32 raw/unit-risk: -0.951093592834
EWMAC32 scalar: 2.79
EWMAC32 capped forecast: -2.65355112401
EWMAC64 raw/unit-risk: -0.51883767053
EWMAC64 scalar: 1.91
EWMAC64 capped forecast: -0.990979950712
FDM: 1.03
```

These values are retained only to prove deterministic plumbing from the quarantined completed-bar files through the S09/M2 forecast block. No raw market rows are committed.

## Implemented Surface

Code:

```text
src/carver/spine/s09_zn_package.py
```

Tests:

```text
tests/test_s09_zn_package_synthetic.py
```

The continuous-chain conformance path fails closed if:

- lane class is not `SOURCE_NATIVE_FUTURES`;
- the S09 ZN package is not valid;
- the continuous ZN chain is not ready;
- the source contract-month set differs from `09-25, 12-25, 03-26, 06-26`;
- the roll dates differ from `2025-09-22, 2025-12-22, 2026-03-23`;
- fewer than 257 adjusted completed daily bars are available;
- any consumed adjusted bar is not exact ZN;
- any consumed adjusted bar has a contract month outside the locked ZN chain;
- consumed adjusted bar months move backward in the locked ZN chain order;
- the price-risk mode is anything other than the unit conformance sentinel;
- the price-risk sentinel value is not exactly `1.0`;
- the price-risk timestamp does not align to the final completed bar.

The older exact `ZN JUN26` direct probe path remains strict and separate; it was not weakened to accept the multi-contract continuous chain.

## Verification

```text
python -m unittest tests.test_s09_zn_package_synthetic -v
6 passed

python -m compileall -q src tests
passed

python -m unittest discover -s tests -v
91 passed

git ls-files -- data/**
no tracked data files

subagent hostile audit:
PROCESS_SAFE_FOR_S09_ZN_TINY_SLICE_CONFORMANCE
```

The hostile-audit blocker on metadata-only chain validation was patched by binding the consumed adjusted bars to the locked ZN chain months and roll dates.

## Non-Authorization

This artifact authorizes no strategy computation beyond the stated forecast-construction plumbing check, no returns, no PnL, no Sharpe, no drawdown, no hit rate, no costs, no turnover, no diagnostics, no backtests, no OOS, no Lockbox, no Forward, no CFD adapter, no old QuantLab import, no tuning, no deployment, no trading, no promotion, and no remote push by inference.
