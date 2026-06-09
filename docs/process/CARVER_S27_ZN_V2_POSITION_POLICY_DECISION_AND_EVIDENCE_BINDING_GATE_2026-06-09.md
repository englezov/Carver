# S27_V2 Position Policy Decision And Evidence Binding Gate

Date: 2026-06-09

Status:

```text
PROCESS_ONLY_POSITION_POLICY_BOUND_NOT_DESIRED_POSITION_EMISSION
```

## Authorization

Operator authorized `S27_V2_POSITION_POLICY_DECISION_AND_EVIDENCE_BINDING_GATE`.

Authorized scope:

- fix capital/account value, risk target, rounding tie-break, and initial/current position policies before any desired-position result exists;
- bind `ZNM6` multiplier, currency, and effective-date evidence from already-local static/provider definition evidence;
- confirm or externally audit divisor-10 position formula authority;
- create process records, perform focused local evidence inspection, add non-result readiness code/tests only if needed, and run local hostile audits with subagents.

Non-authorized scope:

- no provider/API access;
- no downloads or new data;
- no OOS/Lockbox/Forward;
- no backtests or result-scored runs;
- no desired-position/order/fill/cost/PnL/result emission;
- no result interpretation or tuning;
- no Git actions;
- no adapter work, deployment, trading, promotion, or source-faithful evidence claim.

## Evidence Inspected

Book/source records:

```text
Carver.pdf local focused text extraction around position sizing, Strategy 26, and Strategy 27
docs/process/CARVER_S27_ZN_BOOK_SOURCE_LOCK_2026-06-05.md
docs/process/CARVER_S27_ZN_V2_POSITION_EVIDENCE_REMEDIATION_SOURCE_LOCK_GATE_2026-06-09.md
docs/process/CARVER_PROJECT_WIDE_SOURCE_NATIVE_COST_POLICY_RULE_2026-06-09.md
```

Already-local static/provider evidence:

```text
docs/researchops/contract_specs/CARVER_APPENDIX_C_STATIC_CONTRACT_SPEC_EVIDENCE_INTAKE_2026-05-30.csv
sha256: 908D9C147BABF839FF4475F4286BF9E7828921F274F2D1A4A7A4CB5C2B7EAD1D

docs/researchops/s27_v2_local_replay_inputs/ZN/20260609_runtime_evidence_recon_znm6_20260413_declared_pack/cost_parameter.csv
sha256: E6B7C69A712FD7A5EFFBABBD4C809F24C1A6DFABBFB1CE317B387C923AC7F098

docs/researchops/s26_s27_hourly_bridge/ZN_S27_EWMAC16_TREND_DEPENDENCY/zn_lifecycle_databento_definition_probe_2026-05-31/raw_provider_metadata/20260531_ZN_S27_EWMAC16_LIFECYCLE_DEFINITION_PROBE_definition_dataframe.csv
sha256: CB1908E05CD41037A681A1A9AEDE56EB93001AD7C4576B048B15C87B0EC00742

docs/researchops/s26_s27_hourly_bridge/ZN_S27_EWMAC16_TREND_DEPENDENCY/zn_lifecycle_databento_definition_probe_2026-05-31/ledger/20260531_ZN_S27_EWMAC16_LIFECYCLE_DEFINITION_PROBE_lifecycle_definition_ledger.csv
sha256: CBC5385EAFC2E60E31A7F25EA1D79590CCC847D935E4FD7C3AE25C01789E6A58
```

This gate used already-local files only. It did not access providers, download data, run replay, run diagnostics, run backtests, emit desired-position rows, or make a source-faithful evidence claim.

## Binding Decisions

### 1. Capital / Account Value

Decision:

```text
PASS_BOOK_EXAMPLE_DEVELOPMENT_CAPITAL_FIXED_BEFORE_DESIRED_POSITION_RESULTS
```

Locked value for the current S27_V2 ZN development/reconciliation position-policy path:

```text
capital_account_value = 500000.0
capital_currency = USD
capital_policy_label = BOOK_EXAMPLE_ARBITRARY_CAPITAL_500000_USD_FIXED_BEFORE_DESIRED_POSITION_RESULTS
```

Basis:

- focused local `Carver.pdf` inspection of the S26 US 10-year bond worked example found the book's single-instrument example using arbitrary USD 500,000 capital;
- this policy is fixed before any S27_V2 desired-position result exists;
- this is a development/reconciliation book-example capital policy, not portfolio capital, not tuning, and not a promotion/evaluation account value.

Future change rule:

```text
Any change to capital/account value requires a new pre-result operator gate and must be labelled before desired-position emission.
```

### 2. Risk Target

Decision:

```text
PASS_BOOK_EXAMPLE_RISK_TARGET_FIXED_BEFORE_DESIRED_POSITION_RESULTS
```

Locked value:

```text
annual_target_risk = 0.20
risk_target_policy_label = BOOK_USUAL_TARGET_RISK_20_PERCENT_FOR_US_10_YEAR_EXAMPLE_FIXED_BEFORE_DESIRED_POSITION_RESULTS
```

Basis:

- focused local `Carver.pdf` inspection of the S26 US 10-year bond worked example found the usual target risk of 20%;
- this policy is fixed before any S27_V2 desired-position result exists;
- this does not authorize tuning risk target after seeing desired-position, PnL, or backtest results.

### 3. Single-Instrument Formula Context

Decision:

```text
PASS_SINGLE_INSTRUMENT_CONTEXT_FOR_ZN_DEVELOPMENT_RECONCILIATION
```

Locked values:

```text
instrument_weight = 1.0
instrument_diversification_multiplier = 1.0
fx_rate = 1.0
fx_rate_currency_pair = USD/USD
```

Basis:

- the current S27_V2 path is ZN-first, single-instrument development/reconciliation;
- the book example is a single-instrument US 10-year bond futures path;
- portfolio weighting and IDM remain portfolio-level machinery and must not be imported unless separately source-locked.

### 4. Forecast-To-Position Divisor

Decision:

```text
PASS_LOCAL_DIVISOR_10_POLICY_BOUND_PENDING_EXTERNAL_AUDIT
```

Locked value:

```text
forecast_to_position_divisor = 10.0
divisor_policy_label = BOOK_SCALED_FORECAST_DIVISOR_10_LOCALLY_BOUND_FROM_S26_POSITION_AND_LIMIT_PRICE_TEXT_AND_S27_INHERITANCE_PENDING_EXTERNAL_AUDIT
```

Basis:

- focused local `Carver.pdf` inspection found S26 worked-example position/limit-price text using the scaled forecast divided through the `10` convention in the position machinery;
- S27 source-lock states S27 inherits S26 execution/position machinery after applying the trend veto, V/Q/M multiplier, S27 scalar, and forecast cap;
- this gate binds the divisor-10 policy locally, but it must still be included in the next external hostile audit because previous records treated formula rendering conservatively.

### 5. Base / Optimal Position Formula

Decision:

```text
PASS_FORMULA_FAMILY_BOUND_FOR_FUTURE_DESIRED_POSITION_LEDGER
```

Locked formula family:

```text
base_unrounded_contracts =
    capital_account_value
    * annual_target_risk
    * instrument_weight
    * instrument_diversification_multiplier
    / (
        current_price
        * contract_point_value
        * fx_rate
        * annual_percentage_risk
    )

desired_position_unrounded_contracts =
    base_unrounded_contracts * capped_forecast / forecast_to_position_divisor
```

Boundary:

```text
FORMULA_POLICY_ONLY_NOT_DESIRED_POSITION_EMISSION
```

This record binds the formula policy for the next desired-position evidence implementation, but it does not compute or emit a desired-position row.

### 6. ZNM6 Multiplier / Currency / Effective-Date Evidence

Decision:

```text
PASS_POSITION_MULTIPLIER_CURRENCY_EFFECTIVE_DATE_BOUND_FOR_ZNM6_NOT_EXECUTION_ROLL_POLICY
```

Locked position-sizing fields:

```text
instrument = ZN
selected_raw_symbol = ZNM6
selected_decision_timestamp_utc = 2026-04-13T03:00:00Z
selected_effective_trading_date = 2026-04-13
contract_point_value = 1000.0
contract_point_value_currency = USD
contract_face_value = 100000.0
minimum_tick = 0.015625
minimum_tick_value = 15.625
provider_currency = USD
provider_exchange = XCBT
provider_group = ZN
provider_asset = ZN
provider_security_type = FUT
provider_instrument_id = 42000661
provider_activation = 2025-09-19 21:30:00+00:00
provider_expiration = 2026-06-18 17:01:00+00:00
```

Evidence chain:

- Appendix C/static official spec evidence binds ZN as 10-Year U.S. Treasury Note Futures, USD currency, USD 100000 face value, USD 1000 per full price point, tick size 0.015625, and tick value 15.625.
- The local Databento definition probe binds `ZNM6` to `instrument_id = 42000661`, `USD`, `XCBT`, `ZN`, `FUT`, activation `2025-09-19 21:30:00+00:00`, and expiration `2026-06-18 17:01:00+00:00`.
- The runtime remediation pack selected `ZNM6` on `2026-04-13`, which lies after provider activation and before provider expiration.
- The remediation pack `cost_parameter.csv` row binds `raw_symbol = ZNM6`, `effective_trading_date = 2026-04-13`, `contract_multiplier_value_hash = e62e5636ad530c3c37d212511b1927fa67a4094f8ee67a8a7f353d91fe25002c`, and `currency_policy_hash = 724019dc52f3fcb5a67da2d59198c72c5a07698c1be68329eb03019bbd7103e1`.

Provider field caveat:

```text
DATABENTO_DEFINITION_CONTRACT_MULTIPLIER_FIELD_NOT_USED_AS_POINT_VALUE
```

The provider definition row carries a `contract_multiplier` field value of `2147483647`, which is not treated as the ZN point value. The point value authority for position sizing is the Appendix C/static official spec evidence (`1000 USD per full price point`). The provider definition row is used for selected-contract identity, currency, venue/group/asset, and activation/expiration binding only.

Execution boundary:

```text
ROLL_POLICY_AND_WORKING_ORDER_LIFECYCLE_REMAIN_SEPARATE_EXECUTION_GATES
```

The Databento lifecycle ledger still says first notice/delivery window fields are not provided by that schema and roll policy remains blocked pending official lifecycle evidence. This does not block position-sizing policy binding for the selected `ZNM6` row, but it still blocks execution/order/fill/roll policy claims.

### 7. Rounding / Tie-Break Policy

Decision:

```text
PASS_OPERATOR_FIXED_ROUNDING_TIE_BREAK_POLICY_BEFORE_DESIRED_POSITION_RESULTS
```

Locked policy:

```text
rounded_desired_position_contracts = nearest whole integer contract
tie_break = ROUND_HALF_AWAY_FROM_ZERO
examples:
  +0.5 -> +1
  -0.5 -> -1
  +1.5 -> +2
  -1.5 -> -2
  0.0 -> 0
```

Basis:

- the book requires futures positions to be rounded to whole tradable contracts;
- focused source inspection did not locate an explicit half-contract tie-break rule;
- the operator authorized fixing the policy before any desired-position result exists;
- this avoids Python banker-rounding being treated as hidden source authority.

Label:

```text
OPERATOR_FIXED_TIE_BREAK_CONVENTION_NOT_BOOK_EXPLICIT_NOT_TUNED
```

### 8. Initial / Current Position Context

Decision:

```text
PASS_OPERATOR_FIXED_INITIAL_POSITION_CONTEXT_BEFORE_DESIRED_POSITION_RESULTS
```

Locked policy for the first S27_V2 development/reconciliation desired-position row:

```text
initial_current_position_contracts = 0
initial_position_policy_label = INITIAL_FLAT_ZERO_FIRST_DEV_RECON_ROW_OPERATOR_FIXED_NOT_RESULT_TUNED
```

Boundary:

- this applies only to the first development/reconciliation desired-position row;
- after the first row, current position must be derived from the audited transition/fill ledger once order/fill gates exist;
- this does not authorize order/fill rows or working-order lifecycle claims.

## Updated Position Evidence Status

| Prerequisite | Status |
|---|---|
| Forecast authority | `PASS_EXTERNAL_FORECAST_AUTHORITY_FOR_POSITION_INPUT_ONLY` |
| Forecast-to-position divisor | `PASS_LOCAL_DIVISOR_10_POLICY_BOUND_PENDING_EXTERNAL_AUDIT` |
| Base/optimal formula family | `PASS_FORMULA_FAMILY_BOUND_FOR_FUTURE_DESIRED_POSITION_LEDGER` |
| Capital/account value | `PASS_BOOK_EXAMPLE_DEVELOPMENT_CAPITAL_FIXED_BEFORE_DESIRED_POSITION_RESULTS` |
| Risk target | `PASS_BOOK_EXAMPLE_RISK_TARGET_FIXED_BEFORE_DESIRED_POSITION_RESULTS` |
| ZNM6 multiplier/currency/effective date | `PASS_POSITION_MULTIPLIER_CURRENCY_EFFECTIVE_DATE_BOUND_FOR_ZNM6_NOT_EXECUTION_ROLL_POLICY` |
| Rounding/tie-break | `PASS_OPERATOR_FIXED_ROUNDING_TIE_BREAK_POLICY_BEFORE_DESIRED_POSITION_RESULTS` |
| Initial/current position | `PASS_OPERATOR_FIXED_INITIAL_POSITION_CONTEXT_BEFORE_DESIRED_POSITION_RESULTS` |

## Remaining Boundaries

This gate is enough to prepare the next non-result desired-position evidence/readiness implementation gate, subject to local and external hostile audit.

It is not enough to proceed to:

```text
ORDER_LEDGER
FILL_LEDGER
COST_LEDGER
PNL_LEDGER
BACKTEST_READINESS
RESULT_INTERPRETATION
SOURCE_FAITHFUL_EVIDENCE_CLAIM
```

Still separate future gates:

- desired-position executable ledger implementation and audit;
- order/working-order lifecycle policy;
- fill policy and one-hour-lag execution assumptions;
- source-native cost model under the project-wide cost policy rule;
- PnL/validation/trusted-bundle machinery;
- backtest-readiness authorization.

## Next Gate Recommendation

Recommended next gate:

```text
S27_V2_POSITION_POLICY_DECISION_AND_EVIDENCE_BINDING_EXTERNAL_AUDIT
```

Purpose:

- hostile-audit the newly fixed capital, risk target, divisor-10, formula, `ZNM6` multiplier/currency/effective-date binding, rounding tie-break, and initial-position policy;
- verify that no desired-position/order/fill/cost/PnL/result emission or source-faithful evidence claim has occurred;
- decide whether a separately authorized desired-position executable ledger can proceed.

## Non-Authorization

This record authorizes no provider/API access, downloads, new data, OOS/Lockbox/Forward, backtests, result-scored runs, desired-position/order/fill/cost/PnL/result emission, result interpretation, tuning, Git actions, adapter work, deployment, trading, promotion, or source-faithful evidence claim.
