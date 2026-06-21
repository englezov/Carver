# Carver S27 ZN V2 GPT Reaudit Public Boundary Remediation

Date: 2026-06-06

Status:

```text
PROCESS_ONLY_S27_V2_PUBLIC_BOUNDARY_REMEDIATION_NOT_BACKTEST_AUTHORIZATION
```

## Scope

This record covers the local response to the GPT Extended Pro re-audit of the S27 V2 market-fallback implementation slice.

Authorized work was limited to local implementation/test repair. This record authorizes no provider/API use, no downloads, no diagnostics, no backtests, no OOS, no Lockbox, no Forward, no Git staging, no commit, and no push.

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Re-Audit Findings Addressed

GPT reported that the narrow cap-bound market-fallback builder path no longer had the prior P0, but identified public-boundary P1 blockers:

- forged `S27V2WorkingOrderState` could bypass order-plan validation;
- forged market orders with arbitrary triggers could be filled through the public fill primitive;
- `build_s27_v2_order_plan` accepted caller-supplied desired positions not proven from the forecast context;
- overnight gap reset used stale prior desired position rather than recomputing the next-session optimal target.

## Local Remediation

The S27 V2 implementation slice now:

- validates working order state by reconstructing and validating an equivalent `S27V2OrderPlan` before transition handling;
- allowlists source-locked market-order triggers;
- rejects order plans where `desired_rounded_position` does not equal nearest rounding of `capped_forecast / 10 * base_position_contracts`;
- fails closed on `OVERNIGHT_GAP_MARKET_RESET` until a next-session recomputed desired-position primitive exists.

The overnight decision is deliberately conservative. The current primitive cannot recompute the next-session optimal position from next-session source rows, so it must not emit a market reset ledger as source-faithful evidence.

## Test Coverage Added Or Repaired

The synthetic test suite now includes:

- source-consistent desired-position contexts for market-order tests;
- rejection of desired positions not implied by the forecast context;
- rejection of forged market-order triggers;
- rejection of forged working states before overnight reset;
- overnight multi-row replay fail-closed behavior when no recomputed next-session target is available.

Verification run:

```text
python -m pytest tests\test_s27_v2_source_lock_synthetic.py -q
39 passed
```

Compile check:

```text
python -m compileall -q src\carver\spine\s27_v2.py tests\test_s27_v2_source_lock_synthetic.py
PASS
```

## Remaining Gates

This does not make S27 V2 backtest-ready. Remaining gates include:

- next-session overnight target recomputation design;
- local source-row replay over real cached ZN rows;
- Strategy 3 sigma provenance;
- daily/hourly level compatibility proof;
- roll/session calendar proof;
- spread-unit and cost proof;
- external hostile re-audit before any diagnostic or backtest authorization.
