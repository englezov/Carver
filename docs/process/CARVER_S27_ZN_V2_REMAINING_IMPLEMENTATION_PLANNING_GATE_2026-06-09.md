# S27_V2 Remaining Implementation Planning Gate

Date: 2026-06-09

Status:

```text
PROCESS_ONLY_REMAINING_IMPLEMENTATION_PLAN_NOT_EXECUTION_NOT_RESULT
```

## Authorization

Operator authorized a local-only implementation-planning gate after:

- runtime-history executable remediation-pack local PASS;
- external PASS;
- P3 cleanup PASS.

This record defines the minimal remaining phases from runtime-history readiness toward forecast, position, order, fill, cost, PnL, validation, and backtest-readiness machinery.

This record authorizes no implementation, parser/file replay execution, forecast/order/fill/cost/PnL/result emission, backtest, result interpretation, provider/API, download, OOS, Lockbox, Forward, Git action, adapter, deployment, trading, promotion, or source-faithful evidence claim.

## Current S27_V2 State

Completed and audited:

- book source lock;
- inert replay contracts/scaffolding;
- local parser/file replay construction;
- declared ZN input packs;
- runtime-evidence remediation pack;
- runtime-history executable remediation surface;
- P3 hardening cleanup for runtime-history executable validation.

Current executable boundary:

```text
runtime-history readiness is locally proved for the remediation pack,
but runtime numeric values are not emitted.
```

Still unresolved or not yet executable:

- runtime numeric state ledger values;
- S26/S27 forecast math ledger;
- desired position ledger;
- adjacent-position limit-order ledger;
- working-order transition lifecycle;
- market-order fallback cases;
- fill ledger;
- book/source-native cost policy;
- PnL ledger;
- validation/provenance/trusted bundle for result-producing artifacts;
- backtest-readiness gate;
- source-faithful evidence claim.

## Minimal Remaining Phases

### Phase A: Runtime Numeric State And Forecast Ledger

Purpose:

Emit deterministic local-only runtime numeric state and forecast rows for the audited remediation pack, if every input binds to active runtime evidence.

Scope:

- EWMA5 daily equilibrium;
- hourly current price;
- previous completed daily current-contract close;
- Strategy 3 sigma percent;
- sigma-price bridge;
- S26 raw forecast;
- S26 risk-adjusted forecast;
- EWMAC(16,64) trend sign;
- S27 trend veto;
- V/Q/M attenuation multiplier;
- S27 scalar `20.0` as book-approximate implementation freeze;
- capped S27 forecast.

Fail-closed conditions:

- any source-row mismatch;
- any incomplete-bar or lookahead ambiguity;
- zero-sign behavior not explicitly handled;
- level bridge mismatch;
- sigma/EWMAC/V/Q/M evidence mismatch;
- attempt to emit position/order/fill/cost/PnL/result rows.

Output class:

```text
FORECAST_LEDGER_ONLY_NOT_POSITION_NOT_RESULT
```

### Phase B: Desired Position Ledger

Purpose:

Convert capped forecast to desired rounded position using book/source-locked position sizing inputs.

Required before implementation:

- capital/account value policy;
- instrument multiplier/currency policy;
- risk target/divisor policy;
- rounding policy;
- initial position policy.

Likely fail-closed:

Current S27_V2 evidence does not yet source-lock all position sizing inputs. If any of these remain unresolved, Phase B must emit a fail-closed desired-position blockage rather than a desired position.

Output class:

```text
DESIRED_POSITION_LEDGER_OR_FAIL_CLOSED_POSITION_SIZING
```

### Phase C: Order And Working-State Ledger

Purpose:

Implement S26/S27 book execution machinery from desired position and current working state.

Required source-locked behavior:

- adjacent-position implied limit prices;
- one-lot buy/sell limit orders where the book permits both sides;
- cap-bound cases where a limit side is not placed;
- target-position gaps greater than one contract;
- market-order fallback cases;
- end-of-day cancellation/reset;
- overnight/session gap behavior;
- roll interaction;
- initial working-order state.

Likely fail-closed:

Working-order lifecycle is still explicitly blocked. This phase should probably first emit order-policy fail-closed ledgers unless the missing lifecycle decisions are source-locked.

Output class:

```text
ORDER_TRANSITION_LEDGER_OR_FAIL_CLOSED_WORKING_ORDER_POLICY
```

### Phase D: Fill Ledger

Purpose:

Apply one-hour-lag fill assumptions to limit and market orders using completed hourly fill bars.

Required:

- fill price rule for limit orders;
- fill price rule for market orders;
- one-hour lag binding;
- missing/holiday/early-close behavior;
- no same-hour or incomplete-bar fill use;
- roll/session boundary behavior.

Output class:

```text
FILL_LEDGER_OR_FAIL_CLOSED_FILL_POLICY
```

### Phase E: Cost Policy And Cost Ledger

Purpose:

Apply source-native cost rules to fills.

Project-wide rule:

```text
Use book/source costs first.
If insufficient, infer a plausible book-era/source-native retail futures cost model.
Do not use prop-firm, CFD, adapter, or personal trading costs.
```

Required classification:

```text
BOOK_EXPLICIT_COSTS
SOURCE_NATIVE_INFERRED_RETAIL_FUTURES_COSTS
FAIL_CLOSED_COSTS_UNRESOLVED
```

Book-locked S27/S26 behavior:

- all orders pay commission;
- market orders also require normal bid-ask spread treatment;
- limit-order fills do not use adapter/prop-firm costs.

Likely fail-closed:

The current cost row contains policy hashes but no audited book/source-native numeric cost model. Before PnL, either book explicit costs must be found or an inferred retail futures cost packet must be created and audited.

Output class:

```text
COST_LEDGER_OR_FAIL_CLOSED_COST_POLICY
```

### Phase F: PnL, Validation, And Trusted Bundle

Purpose:

Compute deterministic local-only PnL rows from fills, held position state, prices, and cost rows only after upstream ledgers are source-bound.

Required:

- fill ledger PASS;
- cost ledger PASS;
- held-position state;
- price source for mark-to-market;
- roll/contract continuity treatment;
- validation ledger proving no forged upstream rows;
- provenance/hash ledger;
- trusted bundle assembly.

Output class:

```text
PNL_LEDGER_LOCAL_ONLY_NOT_BACKTEST_RESULT_UNTIL_SEPARATE_GATE
```

### Phase G: Backtest-Readiness Gate

Purpose:

Decide whether the machinery is ready for exactly one separately authorized local-only backtest/scored result on a declared development/reconciliation window.

This phase must check:

- all source-lock requirements;
- no unresolved execution/cost/position gates;
- no OOS/Lockbox/Forward access;
- no tuning after seeing results;
- window length authorization;
- audit readiness packet.

Output class:

```text
BACKTEST_READINESS_ONLY_NOT_BACKTEST
```

## Recommended Authorization Queue

### Gate 1: Runtime Numeric State And Forecast Ledger

```text
Operator authorizes S27_V2 local-only runtime numeric state and forecast executable ledger implementation, after runtime-history executable remediation-pack external PASS and P3 cleanup, limited to emitting deterministic local-only runtime numeric state and forecast ledger rows for the audited remediation pack only.

This authorizes code/tests/process records/local hostile audits for EWMA5 equilibrium, hourly current price, previous completed daily close sigma bridge, S26 raw/risk-adjusted forecast, EWMAC(16,64) trend veto, V/Q/M attenuation, S27 scalar/cap, and forecast-row validation.

No provider/API, downloads, new data, OOS/Lockbox/Forward, backtests, result-scored runs, position/order/fill/cost/PnL/result emission, result interpretation, PnL evaluation, tuning, adapter work, deployment, trading, promotion, Git actions, or source-faithful evidence claim.
```

### Gate 2: Position Sizing Evidence Planning

```text
Operator authorizes S27_V2 local-only desired-position evidence planning gate after forecast ledger local/external PASS, limited to identifying the exact book/source-native capital, risk target, multiplier/currency, rounding, and initial-position evidence required before desired-position emission.

No provider/API, downloads, new data, OOS/Lockbox/Forward, backtests, result-scored runs, order/fill/cost/PnL/result emission, result interpretation, PnL evaluation, tuning, adapter work, deployment, trading, promotion, Git actions, or source-faithful evidence claim.
```

### Gate 3: Execution Policy Planning

```text
Operator authorizes S27_V2 local-only execution-policy planning gate after forecast ledger local/external PASS, limited to source-locking or fail-closing adjacent limit orders, market-order fallback cases, one-hour lag fills, end-of-day reset, session/overnight behavior, roll interaction, and initial working-order state.

No provider/API, downloads, new data, OOS/Lockbox/Forward, backtests, result-scored runs, fill/cost/PnL/result emission, result interpretation, PnL evaluation, tuning, adapter work, deployment, trading, promotion, Git actions, or source-faithful evidence claim.
```

### Gate 4: Cost Policy Evidence Packet

```text
Operator authorizes S27_V2 local-only source-native cost policy evidence gate, limited to finding book/source cost assumptions first and, only if insufficient, preparing an explicitly labeled inferred book-era/source-native retail futures cost model for ZN.

Prop-firm fees, evaluation fees, payout rules, CFD broker spreads/swaps, adapter costs, and personal trading costs are not allowed as source-faithful strategy costs.

No provider/API, downloads, new data, OOS/Lockbox/Forward, backtests, result-scored runs, PnL/result emission, result interpretation, PnL evaluation, tuning, adapter work, deployment, trading, promotion, Git actions, or source-faithful evidence claim.
```

## Recommendation

Do not implement position/order/fill/cost/PnL next.

The next smallest useful implementation gate is Gate 1: runtime numeric state and forecast ledger only. It is the narrowest bridge from the current runtime-history PASS into actual S27 logic, and it keeps position sizing, execution, costs, fills, PnL, and backtest-readiness safely outside the next patch.
