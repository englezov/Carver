# S27_V2 Position Evidence Remediation Source-Lock Gate

Date: 2026-06-09

Status:

```text
PROCESS_SOURCE_POSITION_EVIDENCE_REMEDIATION_SOURCE_LOCK_NOT_POSITION_EMISSION
```

## Authorization

Operator authorized a local-only `S27_V2` position evidence remediation source-lock gate.

Authorized scope:

- source-lock or explicitly fail-close forecast-to-position divisor;
- source-lock or explicitly fail-close base/optimal position formula;
- source-lock or explicitly fail-close capital/account value;
- source-lock or explicitly fail-close risk target;
- source-lock or explicitly fail-close ZN multiplier/currency/effective-date evidence;
- source-lock or explicitly fail-close rounding/tie-break policy;
- source-lock or explicitly fail-close initial/current position context.

Non-authorized scope:

- no provider/API access;
- no downloads or new data;
- no OOS/Lockbox/Forward;
- no backtests or result-scored runs;
- no desired-position/order/fill/cost/PnL/result emission;
- no result interpretation;
- no tuning;
- no Git actions;
- no adapter work, deployment, trading, promotion, or source-faithful evidence claim.

## Source Material Inspected

Process/source records:

```text
docs/process/CARVER_S27_ZN_BOOK_SOURCE_LOCK_2026-06-05.md
docs/process/CARVER_S27_ZN_V2_POSITION_EVIDENCE_FAIL_CLOSED_GATE_EXTERNAL_AUDIT_SYNTHESIS_2026-06-09.md
docs/process/CARVER_S27_ZN_V2_POSITION_EVIDENCE_REMEDIATION_PLANNING_GATE_2026-06-09.md
docs/process/CARVER_PROJECT_WIDE_SOURCE_NATIVE_COST_POLICY_RULE_2026-06-09.md
docs/process/CARVER_APPENDIX_C_CONTRACT_SPECIFICATION_SOURCE_PACKET_2026-05-30.md
docs/process/CARVER_APPENDIX_C_STATIC_CONTRACT_SPECIFICATION_EVIDENCE_INTAKE_2026-05-30.md
```

Local code inspected as diagnostic/failure-map evidence only:

```text
src/carver/spine/m1.py
src/carver/spine/s26_s27.py
```

Focused local `Carver.pdf` text extraction was performed with bundled `pypdf` for position-sizing terms. This was book-source inspection only; no market rows, provider data, replay execution, diagnostics, tests, or backtests were run.

Relevant PDF page regions inspected:

```text
70-80: single-instrument position sizing, capital, target risk, and optimal position framework
122-130: portfolio weights and IDM examples
444-448: rounded versus unrounded optimal positions
480-488: Strategy 26 fast mean-reversion optimal position and execution discussion
502-503: Strategy 27 overlay sequence and modified optimal-position equation references
687-689: appendix/index references around scaled forecasts and divide-by-10 convention
```

PDF formula rendering was not available without installing additional tools, so formulas that require visual equation confirmation are treated conservatively where the text extraction omitted equation bodies.

## Locked And Fail-Closed Decisions

### 1. Forecast Authority

Decision:

```text
PASS_EXTERNAL_FORECAST_AUTHORITY_FOR_POSITION_INPUT_ONLY
```

Basis:

- forecast executable remediation-pack slice passed external hostile audit;
- position evidence fail-closed gate passed external hostile audit;
- active forecast authority is accepted only through bundle validation and active rebuild.

Boundary:

```text
NOT_POSITION_EMISSION
```

### 2. Forecast-To-Position Divisor

Decision:

```text
SOURCE_LOCK_PARTIAL_DIVISOR_10_CONVENTION_PENDING_VISUAL_FORMULA_AUDIT
```

Current locked shape:

```text
forecast_multiplier = capped_forecast / 10.0
```

Basis:

- general Carver forecast-to-position convention is consistent with scaled forecast treatment;
- pre-v2 diagnostic code uses `capped_forecast / 10.0`;
- existing source-lock sequence requires S27 capped forecast to proceed into optimal position;
- extracted book references identify scaled forecast divide-by-10 convention, but the exact S27 formula body was not visually rendered in this gate.

Disposition:

```text
FAIL_CLOSED_FOR_DESIRED_POSITION_EMISSION_UNTIL_EXTERNAL_SOURCE_LOCK_AUDIT_OR_VISUAL_FORMULA_EXTRACT_CONFIRMS
```

### 3. Base / Optimal Position Formula

Decision:

```text
SOURCE_LOCK_PARTIAL_BASE_POSITION_FORMULA_FAMILY
```

Current locked formula family:

```text
base_unrounded_contracts =
    capital * target_risk * instrument_weight * idm
    / (current_price * contract_multiplier * fx_rate * annual_percentage_risk)
```

For the standalone single-instrument ZN development/reconciliation path, the candidate context is:

```text
instrument_weight = 1.0
idm = 1.0
fx_rate = 1.0 for USD-denominated ZN
```

Basis:

- book position-sizing text establishes capital, target risk, instrument risk, and optimal contracts as the base sizing framework;
- existing `m1.size_contracts` implements the same formula family;
- S27 source-lock states the S27 forecast chain proceeds to optimal position after scalar and cap;
- portfolio weights and IDM are portfolio constructs; standalone ZN must not import portfolio IDM unless separately source-locked.

Disposition:

```text
PARTIAL_PASS_FORMULA_FAMILY_NOT_READY_FOR_EMISSION
```

Blocked until the dependent input policies below are resolved.

### 4. Capital / Account Value

Decision:

```text
FAIL_CLOSED_CAPITAL_ACCOUNT_VALUE_UNRESOLVED
```

Basis:

- the book framework requires trading capital/account value;
- current S27_V2 records do not source-lock a fixed account value for the remediation pack or future development/reconciliation desired-position ledger;
- choosing capital after seeing forecast/result artifacts would be tuning risk.

Required future treatment:

```text
OPERATOR_FIXED_CAPITAL_POLICY_BEFORE_RESULTS_OR_BOOK_EXPLICIT_CAPITAL_IF_FOUND
```

Any chosen capital must be labelled:

```text
BOOK_EXPLICIT_CAPITAL
```

or:

```text
OPERATOR_FIXED_DEVELOPMENT_CAPITAL_ASSUMPTION_NOT_TUNED
```

### 5. Risk Target

Decision:

```text
FAIL_CLOSED_RISK_TARGET_POLICY_UNRESOLVED
```

Candidate evidence:

```text
20% annual target risk appears in book examples and pre-v2 diagnostic labels.
```

Basis:

- the book position-sizing framework requires predetermined annual target risk;
- extracted text indicates target risk must be selected from conservative constraints rather than blindly assumed;
- current S27_V2 source-lock does not yet prove that standalone S27 ZN should use exactly `20%` under this remediation pack.

Required future treatment:

```text
BOOK_EXPLICIT_RISK_TARGET_OR_OPERATOR_FIXED_RISK_TARGET_ASSUMPTION_BEFORE_RESULTS
```

### 6. ZN Multiplier / Currency / Effective Date

Decision:

```text
SOURCE_STATIC_CANDIDATE_ZN_USD_1000_PER_POINT_FAIL_CLOSED_EFFECTIVE_DATE_BINDING
```

Candidate locked fields from existing static evidence:

```text
instrument = ZN
currency = USD
point_value_or_multiplier = 1000 USD per full price point
minimum_tick = 0.015625
tick_value = 15.625 USD
```

Basis:

- Appendix C and static contract-spec evidence records identify ZN as 10-year US Treasury Note futures;
- official/static evidence intake records USD currency, USD 100000 face value Treasury notes, point value USD 1000 per full price point, tick size 0.015625, and tick value 15.625;
- existing static evidence records still distinguish official/current static fields from production contract identity and active/effective-date locks.

Disposition:

```text
FAIL_CLOSED_FOR_POSITION_EMISSION_UNTIL_SELECTED_ZNM6_EFFECTIVE_DATE_AND_CONTRACT_IDENTITY_BINDING
```

Required future treatment:

- bind selected raw symbol `ZNM6` to the multiplier/currency policy;
- bind the effective date to the selected decision timestamp;
- preserve the distinction between point value, quote unit, tick value, and cost/PnL use.

### 7. Rounding / Tie-Break Policy

Decision:

```text
SOURCE_LOCK_WHOLE_CONTRACT_ROUNDING_REQUIRED_FAIL_CLOSED_TIE_BREAK
```

Locked source shape:

```text
futures positions must be whole integer contracts; optimal unrounded positions are rounded before execution.
```

Current unresolved detail:

```text
tie-break behavior for exactly half-contract values
```

Basis:

- book text distinguishes unrounded optimal positions from rounded tradable contract positions;
- current code uses Python `round`, but Python banker-rounding is not source-locked;
- a desired-position ledger needs deterministic handling of `+0.5`, `-0.5`, and zero.

Disposition:

```text
FAIL_CLOSED_FOR_DESIRED_POSITION_EMISSION_UNTIL_TIE_BREAK_POLICY_IS_SOURCE_LOCKED_OR_OPERATOR_LABELLED
```

### 8. Initial / Current Position Context

Decision:

```text
FAIL_CLOSED_INITIAL_CURRENT_POSITION_CONTEXT_UNRESOLVED
```

Basis:

- desired-position rows can be emitted without generating orders only if their boundary is explicit, but any later order/fill work needs current held position;
- S26/S27 execution machinery explicitly depends on current position and working orders;
- current S27_V2 records do not source-lock first-row starting position for the remediation pack.

Required future treatment:

```text
FIRST_DEVELOPMENT_RECON_ROW_INITIAL_POSITION_POLICY
```

Candidate:

```text
initial_position = 0
```

Disposition:

```text
NOT_ACCEPTED_WITHOUT_OPERATOR_FIXED_POLICY_OR_SOURCE_EXCERPT
```

## Remediation Summary

The current status for desired-position prerequisites is:

| Prerequisite | Status |
|---|---|
| Forecast authority | `PASS_EXTERNAL_FORECAST_AUTHORITY_FOR_POSITION_INPUT_ONLY` |
| Forecast-to-position divisor | `FAIL_CLOSED_PENDING_VISUAL_FORMULA_OR_EXTERNAL_SOURCE_LOCK_AUDIT` |
| Base/optimal formula family | `PARTIAL_PASS_FORMULA_FAMILY_NOT_READY_FOR_EMISSION` |
| Capital/account value | `FAIL_CLOSED_CAPITAL_ACCOUNT_VALUE_UNRESOLVED` |
| Risk target | `FAIL_CLOSED_RISK_TARGET_POLICY_UNRESOLVED` |
| ZN multiplier/currency/effective date | `FAIL_CLOSED_EFFECTIVE_DATE_BINDING_REQUIRED` |
| Rounding/tie-break | `FAIL_CLOSED_TIE_BREAK_POLICY_UNRESOLVED` |
| Initial/current position | `FAIL_CLOSED_INITIAL_CURRENT_POSITION_CONTEXT_UNRESOLVED` |

## Minimal Remaining Blockers Before Desired-Position Emission

Desired-position emission remains blocked by:

```text
CAPITAL_ACCOUNT_VALUE
RISK_TARGET_POLICY
ROUNDING_TIE_BREAK_POLICY
INITIAL_CURRENT_POSITION_CONTEXT
ZNM6_EFFECTIVE_DATE_MULTIPLIER_CURRENCY_BINDING
DIRECT_EXTERNAL_AUDIT_OR_VISUAL_FORMULA_CONFIRMATION_FOR_DIVISOR_10
```

## Next Gate Recommendation

Do not proceed to order/fill/cost.

Do not proceed directly to desired-position executable emission.

Recommended next gate:

```text
S27_V2_POSITION_POLICY_DECISION_AND_EVIDENCE_BINDING_GATE
```

Purpose:

- operator fixes capital/account value before any desired-position result exists, or book source explicitly supplies it;
- operator fixes risk target before results, or book source explicitly supplies it;
- choose and label rounding tie-break convention if book does not specify it;
- choose and label initial position policy for the first development/reconciliation row;
- bind ZNM6 multiplier/currency/effective-date evidence from already-local static/provider definition evidence;
- if possible, perform a visual/source formula audit for the divisor-10 S27 position equation.

This next gate still should not emit desired-position rows unless the operator explicitly includes a desired-position executable ledger authorization after the evidence binding passes.

## Non-Authorization

This record authorizes no provider/API access, downloads, new data, OOS/Lockbox/Forward, backtests, result-scored runs, desired-position/order/fill/cost/PnL/result emission, result interpretation, tuning, Git actions, adapter work, deployment, trading, promotion, or source-faithful evidence claim.
