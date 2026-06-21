# S27_V2 Desired-Position Evidence Planning Gate

Date: 2026-06-09

Status:

```text
PROCESS_ONLY_DESIRED_POSITION_EVIDENCE_PLAN_NOT_POSITION_EMISSION
```

## Authorization

Operator authorized a local-only desired-position evidence planning gate after external PASS on the forecast executable remediation-pack slice.

This planning gate may inspect current S27_V2 code/tests/process records and source-lock artifacts to define required evidence before desired-position ledger emission.

This record authorizes no implementation, no desired-position/order/fill/cost/PnL/result emission, no backtest, no provider/API, no download, no new data, no OOS/Lockbox/Forward, no Git action, no adapter/deployment/trading/promotion, and no source-faithful evidence claim.

## Current State

Externally passed upstream gate:

```text
S27_V2 forecast executable remediation-pack slice
```

Current upstream artifact:

```text
forecast_row_hash = 0b0893fee9d98478f0b35d642fc4d93a4153908ffd94c97f3a1eccfd040b4130
forecast_bundle_hash = e06ddaa874ab0581529062d7e234be4a53628078ff1e4f2e57ade6d673a3137a
trend_veto_decision = ZERO_FORECAST_BY_TREND_VETO
capped_forecast = 0.0
```

This is forecast-ledger metadata only. It is not a position row, not PnL, not a backtest, not result interpretation, and not a source-faithful evidence claim.

## Source-Locked Position Chain

The book/source-lock sequence after forecast is:

```text
S27 capped forecast -> optimal/base position sizing -> desired rounded position -> S26 execution machinery
```

Current source-lock language supports:

- final capped forecast is converted toward position only after the S27 overlays and scalar/cap;
- S26/S27 execution is limit-order based, not close-to-close target-position PnL;
- execution/cost/PnL must stay outside desired-position evidence planning.

Existing pre-v2/diagnostic code records the candidate formula shape:

```text
forecast_multiplier = capped_forecast / 10.0
desired_unrounded_contracts = base_unrounded_contracts * forecast_multiplier
desired_rounded_contracts = round(desired_unrounded_contracts)
```

But v2 may not emit desired-position rows until the evidence below is source-bound under the v2 trust model.

## Required Evidence Before Desired-Position Emission

### 1. Forecast Authority

Required:

- active forecast executable bundle hash;
- active forecast row hash;
- capped forecast value and hash;
- scalar/cap policy hash;
- explicit confirmation that forecast row is from `ForecastExecutableBundle.validate()`, not standalone row validation.

Current status:

```text
PASS_EXTERNAL_FOR_FORECAST_ONLY
```

Disposition:

```text
AVAILABLE_AS_UPSTREAM_INPUT_FOR_FUTURE_POSITION_GATE
```

### 2. Forecast-To-Position Divisor

Required:

- source-lock or audited code/source artifact for divisor `10.0`;
- explicit label distinguishing book/source-native divisor from arbitrary implementation constant;
- policy hash for `capped_forecast / 10.0`.

Current status:

```text
PARTIALLY_PRESENT_IN_PRE_V2_DIAGNOSTIC_CODE_NOT_V2_SOURCE_AUTHORITY
```

Disposition:

```text
SOURCE_LOCK_OR_EXTERNAL_AUDIT_REQUIRED_BEFORE_POSITION_EMISSION
```

### 3. Base Position / Optimal Position

Required:

- book/source-native position sizing rule for base position;
- capital/account value policy;
- target risk policy;
- annual risk input used for sizing;
- ZN contract multiplier and currency policy;
- FX policy if non-USD instruments appear later;
- row-level hash binding to the selected decision timestamp;
- no-lookahead proof.

Current status:

```text
UNRESOLVED_FOR_V2_POSITION_EMISSION
```

Notes:

Existing pre-v2 `S27ZNPrevalidatedBasePosition` expects:

```text
PREVALIDATED_M1_BASE_POSITION_LOCKED
CAPITAL_TARGET_RISK_ANNUAL_RISK_LOCKED_NO_LOOKAHEAD
ZN_MULTIPLIER_USD_FX_LOCKED
```

Those labels are useful as a failure map, but not sufficient v2 authority by themselves.

Disposition:

```text
FAIL_CLOSED_UNTIL_SOURCE_BOUND_BASE_POSITION_EVIDENCE_EXISTS
```

### 4. Contract Multiplier / Currency

Required:

- ZN multiplier value;
- USD currency policy;
- source of multiplier/currency;
- byte/hash binding to local evidence;
- effective date;
- explicit separation from cost/PnL usage.

Current remediation pack status:

```text
READY_COST_PARAMETER_HASHES_LOCAL_ONLY_FAIL_CLOSED_FOR_EXECUTION
```

The pack contains multiplier/currency hashes, but current runtime evidence deliberately keeps multiplier/currency policy fail-closed.

Disposition:

```text
FAIL_CLOSED_FOR_POSITION_EMISSION_UNTIL_MULTIPLIER_CURRENCY_POLICY_IS_SOURCE_BOUND
```

### 5. Rounding Policy

Required:

- book/source-native rounding rule for desired positions;
- tie-break rule;
- exact handling of positive/negative half-contract values;
- policy hash;
- explicit test cases around `+0.5`, `-0.5`, and zero.

Current status:

```text
NEAREST_EXISTS_IN_PLANNED_CONTRACTS_AND_PRE_V2_CODE_ONLY
```

Disposition:

```text
FAIL_CLOSED_UNTIL_ROUNDING_POLICY_IS_SOURCE_LOCKED_OR_OPERATOR_ACCEPTS_A_LABELLED_INFERENCE
```

### 6. Initial / Current Position Context

Required:

- current held position at the first emitted decision row;
- source of initial position;
- rule for development/reconciliation first row if no prior live/replay position exists;
- proof that desired-position ledger does not generate orders;
- policy hash binding current-position context.

Current status:

```text
UNRESOLVED
```

Disposition:

```text
FAIL_CLOSED_UNTIL_INITIAL_POSITION_POLICY_IS_SOURCE_LOCKED_OR_OPERATOR_ACCEPTS_A_LABELLED_INFERENCE
```

### 7. Desired-Position Boundary

Required:

- desired-position ledger emits only desired unrounded/rounded position metadata;
- no order generation;
- no fill generation;
- no cost rows;
- no PnL rows;
- no result interpretation;
- unresolved execution/cost gates carried forward.

Current status:

```text
PLANNED_CONTRACTS_EXIST_BUT_NO_EXECUTABLE_V2_DESIRED_POSITION_AUTHORITY
```

Disposition:

```text
MUST_PRESERVE_NON_RESULT_BOUNDARY
```

## Minimal Next Implementation Shape

The next useful implementation should not emit desired positions yet unless all evidence above is closed.

Recommended next local-only gate:

```text
S27_V2_POSITION_EVIDENCE_FAIL_CLOSED_GATE
```

Purpose:

- consume the externally passed forecast executable bundle;
- build a position-evidence readiness bundle;
- explicitly PASS only forecast authority;
- explicitly fail closed on unresolved divisor/base-position/multiplier-currency/rounding/current-position evidence;
- emit no desired-position row.

Only after that gate passes local and external audit should the project consider a narrow desired-position executable ledger gate.

## Future Authorization Queue

### Gate A: Position Evidence Fail-Closed Gate

```text
Operator authorizes S27_V2 local-only position evidence fail-closed gate after external PASS on the forecast executable remediation-pack slice, limited to building a non-result position-evidence readiness artifact that consumes the active forecast executable bundle and records PASS/FAIL_CLOSED status for forecast authority, forecast-to-position divisor, base position, capital/account value, risk target, multiplier/currency, rounding policy, and initial/current position context.

This authorizes code/tests/process records/local hostile audits only for the fail-closed evidence gate. It does not authorize desired-position/order/fill/cost/PnL/result emission, backtests, result interpretation, provider/API, downloads, new data, OOS/Lockbox/Forward, tuning, adapter work, deployment, trading, promotion, Git actions, or source-faithful evidence claims.
```

### Gate B: Desired-Position Executable Ledger

Only after Gate A local/external PASS and after missing evidence is resolved:

```text
Operator authorizes S27_V2 local-only desired-position executable ledger implementation after local/external PASS on the position evidence gate and after all position evidence prerequisites are PASS, limited to emitting deterministic desired-position ledger rows from active forecast rows and source-bound position evidence.

No order/fill/cost/PnL/result/backtest/result interpretation/provider/API/downloads/new data/OOS/Lockbox/Forward/Git/adapter/deployment/trading/promotion/source-faithful evidence claim.
```

## Recommendation

Proceed with Gate A first.

Do not implement desired-position emission next. The evidence state is not ready, and emitting a desired position now would depend on unresolved or pre-v2 diagnostic assumptions.
