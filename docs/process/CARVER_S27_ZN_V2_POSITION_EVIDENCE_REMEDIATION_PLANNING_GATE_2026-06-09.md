# S27_V2 Position Evidence Remediation Planning Gate

Date: 2026-06-09

Status:

```text
PROCESS_ONLY_POSITION_EVIDENCE_REMEDIATION_PLAN_NOT_POSITION_EMISSION
```

## Authorization

Operator authorized a local-only position evidence remediation planning gate after external PASS on the position evidence fail-closed gate.

Authorized scope:

- inspect current `S27_V2` code/tests/process records and source-lock artifacts;
- record the external PASS synthesis;
- identify exact book/source-native evidence needed to resolve forecast-to-position divisor, base/optimal position, capital/account value, risk target, multiplier/currency, rounding policy, and initial/current position context;
- define which prerequisites can be source-locked from existing book/process evidence, which remain fail-closed, and the minimal future authorization needed before desired-position executable ledger emission.

Non-authorized scope:

- no provider/API access;
- no downloads or new data;
- no OOS/Lockbox/Forward;
- no backtests or result-scored runs;
- no desired-position/order/fill/cost/PnL/result emission;
- no result interpretation or PnL evaluation;
- no tuning;
- no adapter work, deployment, trading, promotion, Git actions, or source-faithful evidence claim.

## Upstream State

External hostile audit passed for the position evidence fail-closed gate:

```text
docs/process/CARVER_S27_ZN_V2_POSITION_EVIDENCE_FAIL_CLOSED_GATE_EXTERNAL_AUDIT_SYNTHESIS_2026-06-09.md
```

Current passed chain:

```text
forecast executable PASS
position evidence fail-closed PASS
```

Current blocked chain:

```text
desired-position executable ledger
order/working-state
fill
cost
PnL/result
backtest-readiness
```

## Source Basis Inspected

Primary process/source-lock artifacts inspected:

```text
docs/process/CARVER_S27_ZN_BOOK_SOURCE_LOCK_2026-06-05.md
docs/process/CARVER_S27_ZN_V2_DESIRED_POSITION_EVIDENCE_PLANNING_GATE_2026-06-09.md
docs/process/CARVER_S27_ZN_V2_POSITION_EVIDENCE_FAIL_CLOSED_GATE_LOCAL_AUDIT_RESULT_2026-06-09.md
docs/process/CARVER_S27_ZN_V2_POSITION_EVIDENCE_FAIL_CLOSED_GATE_EXTERNAL_AUDIT_SYNTHESIS_2026-06-09.md
docs/process/CARVER_PROJECT_WIDE_SOURCE_NATIVE_COST_POLICY_RULE_2026-06-09.md
```

Local code inspected as diagnostic/failure-map material, not as source authority:

```text
src/carver/spine/m1.py
src/carver/spine/s26_s27.py
```

`Carver.pdf` was not re-parsed under this planning gate. The planning conclusions therefore distinguish source-locked current evidence from candidate values requiring future source extraction or external audit.

## Position Evidence Remediation Matrix

| Prerequisite | Candidate Evidence Found | Current Disposition | Required Remediation |
|---|---|---|---|
| Forecast authority | Externally passed `ForecastExecutableBundle` and externally passed position evidence gate. | `PASS_EXTERNAL_FORECAST_AUTHORITY_FOR_POSITION_INPUT_ONLY` | No additional remediation before desired-position planning, but future desired-position builder must rebuild active forecast authority, not accept caller rows. |
| Forecast-to-position divisor | Pre-v2 diagnostic code uses `capped_forecast / 10.0`; process records identify this as candidate shape. | `FAIL_CLOSED_NOT_V2_SOURCE_AUTHORITY` | Source-lock the forecast-to-position divisor from `Carver.pdf` or audited source extract. If not explicit, record as labelled inference before any desired-position emission. |
| Base/optimal position formula | `m1.size_contracts` and pre-v2 labels provide a likely formula surface: capital, target risk, current price, annual risk estimate, multiplier, FX, optional weight/IDM. | `FAIL_CLOSED_UNTIL_BOOK_SOURCE_LOCKED_FOR_S27_V2` | Source-lock the base/optimal position formula from book/M1 source sections, including whether standalone ZN uses weight `1.0` and IDM `1.0`. |
| Capital/account value | No v2 source-bound capital/account policy in current S27 source-lock. | `FAIL_CLOSED_OPERATOR_OR_BOOK_POLICY_REQUIRED` | Determine book/example account capital if explicit, or require operator-approved development capital policy labelled as non-tuned and fixed before results. |
| Risk target | Pre-v2 diagnostic semantics mention `ANNUAL_TARGET_RISK_20_PERCENT_BOOK_DEFAULT_LOCK_REQUIRED_AT_TEST_GATE`. | `FAIL_CLOSED_NOT_V2_SOURCE_AUTHORITY` | Source-lock whether annual target risk is `20%` for this standalone S27 ZN context and whether it is book default, operator lab convention, or inferred development assumption. |
| Multiplier/currency | Current remediation pack carries cost-parameter hashes, but runtime evidence keeps multiplier/currency fail-closed. Other Appendix C/static contract process evidence may be useful. | `FAIL_CLOSED_PENDING_SOURCE_NATIVE_STATIC_POLICY` | Source-lock ZN contract multiplier/point value/currency/effective-date evidence from already-local static futures evidence or book/official source records; bind to the selected decision timestamp. |
| Rounding policy | Planned/pre-v2 surfaces use nearest/Python `round`, but tie-break behavior is not source-locked. | `FAIL_CLOSED_ROUNDING_POLICY_UNRESOLVED` | Source-lock whole-contract rounding rule and tie-break behavior. If book only says round to nearest contract without tie-break detail, record a labelled implementation convention and test `+0.5`, `-0.5`, and zero. |
| Initial/current position context | No v2 source-bound first-row current-position context. | `FAIL_CLOSED_INITIAL_CURRENT_POSITION_CONTEXT_UNRESOLVED` | Define initial position for development/reconciliation replay, likely flat `0` only if source/operator policy accepts it; bind any future current-position state to the prior transition/fill ledger once execution exists. |

## What Can Be Resolved From Existing Evidence

The following are likely resolvable from existing local process/code/source-lock material, but still require a narrow source-lock/remediation implementation gate:

```text
FORECAST_TO_POSITION_DIVISOR_CANDIDATE_10
BASE_POSITION_FORMULA_SHAPE_FROM_M1
SINGLE_INSTRUMENT_WEIGHT_IDM_CANDIDATE_1_1
TARGET_RISK_CANDIDATE_20_PERCENT
ZN_MULTIPLIER_CURRENCY_CANDIDATE_FROM_STATIC_EVIDENCE
```

These are not yet position-emission authority.

## What Remains Explicitly Fail-Closed

The following remain fail-closed until source-locked or operator-labelled as fixed non-tuned assumptions:

```text
CAPITAL_ACCOUNT_VALUE
ROUNDING_TIE_BREAK_POLICY
INITIAL_CURRENT_POSITION_CONTEXT
```

Multiplier/currency also remains fail-closed until a source-native static evidence route is selected and byte/hash-bound.

## Minimal Future Gate Before Desired-Position Emission

Recommended next gate:

```text
S27_V2_POSITION_EVIDENCE_REMEDIATION_SOURCE_LOCK_GATE
```

Purpose:

- extract or lock the forecast-to-position divisor;
- lock the base/optimal position formula;
- lock target risk classification;
- lock or fail-close capital/account value policy;
- lock ZN multiplier/currency/effective-date evidence;
- lock rounding policy and tie-break;
- lock initial/current position context for the first development/reconciliation row;
- update `position_evidence_gate.py` only if it remains a readiness artifact and still emits no desired-position rows.

This next gate may inspect source-lock artifacts, already-local static evidence records, and, if explicitly authorized, focused `Carver.pdf` excerpts for the position-sizing source sections. It should not emit desired-position rows.

## Gate After That

Only after the remediation source-lock gate passes local/external audit should a desired-position executable ledger gate be considered.

Future desired-position gate must:

- rebuild active forecast authority;
- rebuild active position evidence;
- require all position evidence prerequisites to PASS;
- emit desired unrounded and rounded position rows only;
- emit no orders, fills, costs, PnL, result rows, or source-faithful evidence claim;
- preserve execution/cost fail-closed gates for later slices.

## Recommended Authorization Prompt

```text
Operator authorizes S27_V2 local-only position evidence remediation source-lock gate after external PASS on the position evidence fail-closed gate and completion of the remediation planning gate, limited to source-locking or explicitly fail-closing forecast-to-position divisor, base/optimal position formula, capital/account value, risk target, ZN multiplier/currency/effective-date evidence, rounding/tie-break policy, and initial/current position context.

This authorizes Codex to inspect current S27_V2 code/tests/process records, already-local static futures evidence records, and focused Carver.pdf source excerpts only for the relevant position-sizing sections; produce process/source-lock records; add or patch non-result readiness code/tests only if needed to keep position evidence fail-closed until all prerequisites PASS; and run local hostile audits with subagents.

No provider/API, downloads, new data, OOS/Lockbox/Forward, backtests, result-scored runs, desired-position/order/fill/cost/PnL/result emission, result interpretation, PnL evaluation, tuning, adapter work, deployment, trading, promotion, Git actions, or source-faithful evidence claim.
```

## Planning Conclusion

Do not proceed to order/fill/cost.

Do not proceed directly to desired-position executable emission.

The next useful work is a source-lock/remediation gate for position-sizing prerequisites. The strongest likely blockers are capital/account policy, rounding tie-break, initial/current position context, and multiplier/currency authority binding.
