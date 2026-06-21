# CARVER S27 ZN V2 2023 TEST Row-1 Market-Order Spread-Cost Policy Remediation

Date: 2026-06-12

Status:

```text
PROCESS_ONLY_MARKET_ORDER_SPREAD_COST_CANDIDATE_PREPARED_PENDING_OPERATOR_ACCEPTANCE_NOT_COST_EMISSION
```

## Authorization

Operator authorized the S27_V2 local-only TEST row-1 market-order spread-cost policy remediation gate after GPT 5.5 PASS on the row-1 market-order metadata packet.

Scope was limited to resolving or explicitly fail-closing numeric market spread cost treatment for the audited 2023 TEST row-1 `BUY 2` market fill.

This gate authorizes no provider/API access, downloads, new data acquisition, VALIDATION, OOS, Lockbox, Forward, broader TEST continuation, actual PnL/result emission, result interpretation, PnL evaluation, tuning, adapter work, deployment, trading, promotion, Git actions, or source-faithful evidence claim.

## Inputs Inspected

Already-local records and artifacts:

```text
docs/process/CARVER_S27_ZN_BOOK_SOURCE_LOCK_2026-06-05.md
docs/process/CARVER_S27_ZN_POSITION_EXECUTION_COST_SEMANTICS_LOCK_2026-05-31.md
docs/process/CARVER_PROJECT_WIDE_SOURCE_NATIVE_COST_POLICY_RULE_2026-06-09.md
docs/process/CARVER_S27_ZN_V2_NUMERIC_COST_ASSUMPTION_AND_VALUATION_POLICY_SOURCE_LOCK_GATE_2026-06-09.md
docs/process/CARVER_S27_ZN_V2_INFERRED_RETAIL_COST_ACCEPTANCE_AND_VALUATION_SOURCE_LOCK_GATE_2026-06-09.md
docs/process/CARVER_S27_ZN_V2_POSITIVE_ACTION_ACTUAL_COST_IMPLEMENTATION_RECORD_2026-06-09.md
docs/process/CARVER_S27_ZN_V2_MARKET_ORDER_POLICY_SOURCE_LOCK_AND_IMPLEMENTATION_PLAN_2026-06-12.md
docs/process/CARVER_S27_ZN_V2_2023_TEST_ROW1_MARKET_ORDER_METADATA_GPT55_AUDIT_PASS_2026-06-12.md
docs/researchops/s27_v2_local_replay_inputs/ZN/20260612_2023_test_declared_pack/cost_parameter.csv
docs/researchops/s27_v2_local_replay_inputs/ZN/20260612_2023_test_declared_pack/runtime_evidence_ledger.csv
docs/researchops/s27_v2_local_replay_inputs/ZN/20260612_2023_test_declared_pack/hourly_fill_completed_bar.csv
src/carver/spine/s27_v2_replay/desired_position_executable.py
src/carver/spine/s27_v2_replay/costs.py
```

No fresh PDF extraction, provider/API access, market-data download, diagnostic, backtest, result-scored run, or Git action was used.

## Book / Source Decision

The S27 book source lock records the cost treatment shape:

```text
ALL_ORDERS_PAY_COMMISSION
LIMIT_ORDER_FILL_COST = COMMISSION_ONLY
MARKET_ORDER_FILL_COST = COMMISSION_PLUS_NORMAL_BID_ASK_SPREAD
```

The book/source records inspected in this gate do not lock a numeric ZN market-order spread amount.

Decision:

```text
BOOK_EXPLICIT_NUMERIC_ZN_MARKET_ORDER_SPREAD = FAIL_CLOSED_NOT_FOUND
```

## Current TEST Cost Row

The declared 2023 TEST input pack cost row is:

```text
cost_policy_id = S27_V2_ZN_ACCEPTED_INFERRED_RETAIL_FUTURES_COST_2026_06_11
instrument = ZN
currency = USD
commission_per_contract_per_side = 2.30
spread_cost_policy = LIMIT_FILL_COMMISSION_ONLY_NO_MARKET_SPREAD
cost_policy_status = INFERRED_RETAIL_FUTURES_COST_ACCEPTED_FOR_LOCAL_TEST_MECHANICAL_ONLY_NOT_BOOK_EXPLICIT
readiness_status = READY_COST_PARAMETER_FOR_LOCAL_TEST_MECHANICAL_ONLY
```

This row is sufficient for commission but not sufficient for market-order spread cost because its spread policy is explicitly limit-fill-only.

Decision:

```text
TEST_COST_PARAMETER_MARKET_SPREAD_AUTHORITY = FAIL_CLOSED_NOT_MARKET_SPREAD_AUTHORITY
```

## Static ZN Arithmetic Evidence

Already-local static/position evidence binds:

```text
ZN point value = 1000.0 USD per full price point
ZN tick size = 0.015625 price points
ZN tick value = 15.625 USD
```

This is sufficient to compute spread-cost arithmetic if, and only if, a numeric normal-spread convention is separately accepted.

It is not by itself a book-explicit normal-spread lock.

## Candidate A: One-Tick Market, Half-Spread Entry Cost

Prepared candidate:

```text
decision = S27_V2_TEST_ROW1_MARKET_ORDER_SPREAD_COST_CANDIDATE_PREPARED_PENDING_OPERATOR_ACCEPTANCE
classification = SOURCE_NATIVE_ENGINEERING_SPREAD_ASSUMPTION_NOT_BOOK_EXPLICIT
instrument = ZN/ZNH3
static_tick_size_points = 0.015625
static_point_value_usd_per_point = 1000.0
static_tick_value_usd = 15.625
normal_bid_ask_full_spread_candidate_points = 0.015625
market_entry_cost_convention = HALF_SPREAD_FROM_MID_OR_COMPLETED_CLOSE_PROXY
spread_amount_points_charged_per_contract = 0.0078125
spread_cost_usd_per_contract = 7.8125
row1_fill_quantity = 2
row1_spread_cost_amount_usd = 15.625
row1_commission_amount_usd = 4.6
row1_total_market_order_cost_before_pnl_usd = 20.225
source_faithful_evidence_claim = false
actual_cost_emission_authorized = false
```

Candidate A rationale:

- the market-fill metadata uses completed close as the local market-price proxy;
- when a close/mid proxy is used as the trade price and spread is modeled separately, a one-tick-wide bid/ask market implies a half-spread entry cost for one market order side;
- it is less punitive than a full-tick-per-side cost and more aligned with separating mid-price movement from execution spread.

Decision block SHA256:

```text
fd71f50c3d78b2de29222060516c29b14ba3677771df98fed770bdc9d5d7a436
```

## Candidate B: One Full Tick Per Market Order Side

Prepared alternate candidate:

```text
decision = S27_V2_TEST_ROW1_MARKET_ORDER_SPREAD_COST_CONSERVATIVE_ALTERNATE_PREPARED_PENDING_OPERATOR_ACCEPTANCE
classification = SOURCE_NATIVE_ENGINEERING_SPREAD_ASSUMPTION_NOT_BOOK_EXPLICIT
instrument = ZN/ZNH3
static_tick_size_points = 0.015625
static_point_value_usd_per_point = 1000.0
static_tick_value_usd = 15.625
normal_bid_ask_full_spread_candidate_points = 0.015625
market_entry_cost_convention = FULL_ONE_TICK_PER_MARKET_ORDER_SIDE_CONSERVATIVE
spread_amount_points_charged_per_contract = 0.015625
spread_cost_usd_per_contract = 15.625
row1_fill_quantity = 2
row1_spread_cost_amount_usd = 31.25
row1_commission_amount_usd = 4.6
row1_total_market_order_cost_before_pnl_usd = 35.85
source_faithful_evidence_claim = false
actual_cost_emission_authorized = false
```

Candidate B rationale:

- it is deliberately more conservative;
- it may overcharge relative to a mid/close-proxy half-spread convention;
- it remains an inferred engineering assumption, not book-explicit authority.

Decision block SHA256:

```text
001486ead8c0a9f0f7d12884645a36eb372fa4f33075424071d816db13b74e86
```

## Rejected Cost Classes

Rejected for S27 source-native strategy costs:

```text
PROP_FIRM_COSTS
EVALUATION_FEES
PAYOUT_RULES
CFD_BROKER_SPREADS
CFD_SWAPS
ADAPTER_COSTS
PERSONAL_ACCOUNT_COSTS
```

## Remediation Decision

This gate does not accept either candidate for actual cost emission.

Decision:

```text
MARKET_ORDER_SPREAD_COST_POLICY = PREPARED_PENDING_OPERATOR_ACCEPTANCE_OR_FAIL_CLOSED_DECISION
ACTUAL_MARKET_SPREAD_COST_LEDGER = FAIL_CLOSED_CANDIDATE_NOT_ACCEPTED
ACTUAL_PNL_LEDGER = FAIL_CLOSED_MARKET_SPREAD_COST_NOT_ACCEPTED
RESULT_OR_BACKTEST = FAIL_CLOSED_NOT_AUTHORIZED
SOURCE_FAITHFUL_EVIDENCE_CLAIM = FALSE
```

## Recommendation

Recommended next gate:

```text
S27_V2_TEST_ROW1_MARKET_ORDER_SPREAD_COST_ACCEPTANCE_AND_ACTUAL_COST_IMPLEMENTATION_GATE
```

The recommended default is Candidate A:

```text
ONE_TICK_NORMAL_BID_ASK_FULL_SPREAD_WITH_HALF_SPREAD_MARKET_ENTRY_COST
```

Reason:

The current market-fill price is a completed close proxy, not a quoted ask for a buy or bid for a sell. Charging half the accepted one-tick full bid/ask spread as a separate execution cost is the cleaner arithmetic convention for a mid/close proxy. Candidate B remains available if the operator wants a deliberately conservative full-tick-per-side penalty.

Either accepted candidate must remain labeled:

```text
SOURCE_NATIVE_ENGINEERING_SPREAD_ASSUMPTION_NOT_BOOK_EXPLICIT
```

and must not be described as book-explicit or source-faithful Carver authority.

## Boundary

This record is a policy/remediation artifact only. It is not an emitted cost row, not an emitted PnL row, not a result, not a backtest, not result interpretation, not PnL evaluation, not tuning, and not a source-faithful evidence claim.
