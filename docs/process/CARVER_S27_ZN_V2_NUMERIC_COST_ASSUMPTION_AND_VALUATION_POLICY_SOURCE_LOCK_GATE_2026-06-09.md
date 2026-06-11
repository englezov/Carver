# S27_V2 Numeric Cost Assumption And Valuation Policy Source-Lock Gate

Date: 2026-06-09

Status:

```text
PROCESS_ONLY_NUMERIC_COST_ASSUMPTION_PREPARED_PENDING_OPERATOR_ACCEPTANCE_VALUATION_FAIL_CLOSED
```

## Authorization

Operator authorized the `S27_V2 numeric cost assumption and valuation policy source-lock gate` after local PASS on the positive-action numeric cost and valuation remediation gate.

Scope was limited to resolving or explicitly fail-closing the remaining cost and valuation blockers before any actual cost, PnL, or backtest-readiness implementation.

## Non-Authorization

This record authorizes no provider/API access, no market-data download, no OOS, no Lockbox, no Forward, no backtest, no result-scored run, no actual cost emission, no actual PnL ledger emission, no result emission, no result interpretation, no PnL evaluation, no tuning, no adapter work, no deployment, no trading, no promotion, no Git action, and no source-faithful evidence claim.

## Inputs Inspected

Already-local records:

```text
Carver.pdf
docs/process/CARVER_S27_ZN_BOOK_SOURCE_LOCK_2026-06-05.md
docs/process/CARVER_PROJECT_WIDE_SOURCE_NATIVE_COST_POLICY_RULE_2026-06-09.md
docs/process/CARVER_S27_ZN_V2_POSITIVE_ACTION_COST_IMPLEMENTATION_RECORD_2026-06-09.md
docs/process/CARVER_S27_ZN_V2_POSITIVE_ACTION_NUMERIC_COST_VALUATION_REMEDIATION_GATE_2026-06-09.md
docs/process/CARVER_S27_ZN_V2_POSITIVE_ACTION_NUMERIC_COST_VALUATION_REMEDIATION_LOCAL_AUDIT_RESULT_2026-06-09.md
docs/researchops/s27_v2_local_replay_inputs/ZN/20260609_positive_action_recon_znm6_20260413T13_declared_pack/cost_parameter.csv
```

Public source-native retail futures fee evidence inspected:

```text
https://ninjatrader.com/PDF/ninjatrader_futures_commissions.pdf
https://www.nfa.futures.org/faqs/members/nfa-assessment-fees.html
https://www.tradestation.com/pricing/
```

No provider API, credentialed source, market-data download, backtest, diagnostic, or Git action was used.

## Book Cost Decision

Local inspection of `Carver.pdf` and the existing S27 source lock supports the cost treatment shape:

```text
ALL_ORDERS_PAY_COMMISSION
LIMIT_ORDER_FILL_COST = COMMISSION_ONLY
MARKET_ORDER_FILL_COST = COMMISSION_PLUS_NORMAL_BID_ASK_SPREAD
```

For the audited positive-action row:

```text
raw_symbol = ZNM6
decision_timestamp_utc = 2026-04-13T13:00:00Z
fill_timestamp_utc = 2026-04-13T14:00:00Z
order_side = SELL
fill_quantity = 1
fill_price = 111.046875
order_kind = LIMIT
market_order_emitted = False
spread_cost_applicable = False
```

Therefore the future cost formula shape remains:

```text
commission_amount = commission_per_contract * abs(fill_quantity)
spread_cost_amount = 0.0
total_cost_amount = commission_amount
total_cost_currency = USD
```

This gate did not find a book-source exact numeric ZN commission amount. Book examples for other instruments do not become ZN futures authority.

Decision:

```text
BOOK_EXPLICIT_NUMERIC_ZN_COMMISSION = FAIL_CLOSED_NOT_FOUND
```

## Retail Futures Inferred Cost Candidate

Because the book/source records do not specify enough numeric ZN costs, this gate prepared a clearly labeled source-native retail futures inferred cost candidate.

Primary candidate source:

```text
source = NinjaTrader futures commissions PDF
source_updated = 2025-11-13
retrieved_date = 2026-06-09
instrument = ZN 10Y TREASURY NOTE FUTURES
exchange = CBOT
```

NinjaTrader itemized ZN row:

```text
exchange_and_nfa_clearing_usd_per_contract_per_side = 0.82
clearing_usd_per_contract_per_side = 0.19
commission_lifetime_usd_per_contract_per_side = 0.59
commission_monthly_usd_per_contract_per_side = 0.99
commission_free_usd_per_contract_per_side = 1.29
all_in_lifetime_usd_per_contract_per_side = 1.60
all_in_monthly_usd_per_contract_per_side = 2.00
all_in_free_usd_per_contract_per_side = 2.30
```

NFA cross-check:

```text
official_nfa_assessment_fee_usd_per_side = 0.02
effective_since = 2018-01-01
```

TradeStation retail cross-check:

```text
regular_futures_commission_0_to_500_contracts_usd_per_contract_per_side = 1.75
clearing_fee_0_to_500_contracts_usd_per_contract_per_side = 0.10
exchange_execution_and_clearing_fees_apply = True
```

Prepared candidate assumption:

```text
SOURCE_NATIVE_INFERRED_RETAIL_FUTURES_COST_CANDIDATE = NINJATRADER_FREE_PLAN_ALL_IN_ZN_2_30_USD_PER_CONTRACT_PER_SIDE
candidate_commission_per_contract_for_s27_limit_fill = 2.30
candidate_commission_unit = USD_PER_CONTRACT_PER_SIDE_ALL_IN_RETAIL_FUTURES_TRANSACTION_FEE
candidate_components = EXCHANGE_AND_NFA_CLEARING_PLUS_CLEARING_PLUS_BROKER_COMMISSION_AS_PUBLISHED_BY_NINJATRADER
candidate_plan_basis = FREE_PLAN_NO_SUBSCRIPTION_CONSERVATIVE_RETAIL_DEFAULT
candidate_round_turn_equivalent = 4.60
```

Reason for choosing the free-plan candidate as the default candidate:

```text
It avoids amortizing a monthly or lifetime platform plan fee into strategy costs, is conservative relative to the paid NinjaTrader plans, and is still a source-native retail futures cost rather than prop-firm, CFD, adapter, or personal-account cost.
```

This candidate is not accepted for actual cost emission in this gate.

Decision:

```text
INFERRED_RETAIL_FUTURES_COST_ASSUMPTION = PREPARED_PENDING_OPERATOR_ACCEPTANCE_AND_EXTERNAL_AUDIT
ACTUAL_COST_LEDGER = FAIL_CLOSED_CANDIDATE_NOT_ACCEPTED
```

## Evidence Block Hashes

Canonical evidence blocks used by this process record:

```text
NINJATRADER_ZN_FEE_EVIDENCE_BLOCK_SHA256 = 99894537628469d8cd001d52fc60d294bb6caf48036be83eedbcb4be093e1208
NFA_ASSESSMENT_EVIDENCE_BLOCK_SHA256 = 4e9c4cf1958557f9e3665aa6e405ba252787f5639b66f15eb12f3cab57662282
TRADESTATION_RETAIL_BROKER_CROSSCHECK_BLOCK_SHA256 = cce399db97abcb8db982a36b0cf01bc343368b4aa96aaaca66e91667053fac7a
CARVER_BOOK_COST_VALUATION_EVIDENCE_BLOCK_SHA256 = 44d2e014196cf474685bdfb6b2ad3a5bab876eb3ab20b7f104b114bce4b659bd
```

These hashes bind the local process evidence summaries, not raw provider data and not a market-data artifact.

Canonical block bytes hashed above are the UTF-8 bytes of these exact text blocks, including final newline.

`NINJATRADER_ZN_FEE_EVIDENCE_BLOCK`:

```text
source_url=https://ninjatrader.com/PDF/ninjatrader_futures_commissions.pdf
retrieved_date=2026-06-09
source_updated=2025-11-13
source_type=retail_futures_broker_fee_schedule
instrument=ZN 10Y TREASURY NOTE FUTURES
exchange=CBOT
exchange_and_nfa_clearing_usd_per_contract_per_side=0.82
clearing_usd_per_contract_per_side=0.19
commission_lifetime_usd_per_contract_per_side=0.59
commission_monthly_usd_per_contract_per_side=0.99
commission_free_usd_per_contract_per_side=1.29
all_in_lifetime_usd_per_contract_per_side=1.60
all_in_monthly_usd_per_contract_per_side=2.00
all_in_free_usd_per_contract_per_side=2.30
plan_fee_note=The 3 listed commission rates are associated to NinjaTrader account plans; rate depends on selected plan.
```

`NFA_ASSESSMENT_EVIDENCE_BLOCK`:

```text
source_url=https://www.nfa.futures.org/faqs/members/nfa-assessment-fees.html
retrieved_date=2026-06-09
source_type=official_nfa_assessment_fee_faq
futures_assessment_fee_usd_per_side=0.02
effective_statement=As of January 1, 2018, the NFA assessment fee payable by FCMs for futures contracts is 0.02 USD per side, invoiced to customers.
round_turn_note=NFA FAQ describes futures assessment as calculated on round-turn basis but invoice/accrual timing may vary.
```

`TRADESTATION_RETAIL_BROKER_CROSSCHECK_BLOCK`:

```text
source_url=https://www.tradestation.com/pricing/
retrieved_date=2026-06-09
source_type=retail_futures_broker_pricing_crosscheck
regular_futures_commission_0_to_500_contracts_usd_per_contract_per_side=1.75
clearing_fee_0_to_500_contracts_usd_per_contract_per_side=0.10
exchange_execution_and_clearing_fees_apply=true
futuresplus_fee_usd_per_contract_per_side=1.75
```

`CARVER_BOOK_COST_VALUATION_EVIDENCE_BLOCK`:

```text
source=Carver.pdf local reference
retrieved_date=2026-06-09
cost_pages_inspected=26-30,99-105,482-492,497-498,503,505
book_cost_shape=commissions plus spread costs generally; fast limit-order strategies commission-only for limit fills; market orders one-hour lag with normal bid-ask spread assumptions; all orders incur commissions.
book_numeric_cost_status=explicit examples for micro/e-mini S&P but no source-exact numeric ZN commission_per_contract found.
valuation_pages_inspected=26-30,482-492,497-498
valuation_status=book supports PnL decomposition using mid prices and costs, and hourly one-hour-lag fill assumptions, but no explicit first post-fill valuation/end-mark timestamp policy for an open S27 ZN position was source-locked in this gate.
```

## Rejected Cost Classes

Rejected as source-faithful S27 costs:

```text
PROP_FIRM_COSTS
EVALUATION_FEES
PAYOUT_RULES
CFD_BROKER_SPREADS
CFD_SWAPS
ADAPTER_COSTS
PERSONAL_ACCOUNT_COSTS
```

## Valuation / End-Mark Policy

Book/source records support the general PnL decomposition:

```text
futures holding PnL uses price changes times point value
trading costs are separated from holding PnL
back-adjusted prices reflect rolling PnL while ignoring trading costs
S26/S27 fills are tested with hourly one-hour-lag assumptions
```

This gate did not find an explicit source-locked first post-fill valuation/end-mark timestamp policy for an open S27 ZN position after the audited 2026-04-13T14:00:00Z fill.

Unresolved choices remain:

```text
first mark at same completed fill-candidate close
first mark at next completed hourly close
first mark at session close
first mark at next daily close
realized-only until exit
separate mark-to-market ledger using a source-locked hourly close series
```

Conservative candidate policy for a future gate:

```text
FIRST_POST_FILL_VALUATION_CANDIDATE = NEXT_COMPLETED_HOURLY_CLOSE_AFTER_FILL
candidate_reason = avoids same-bar fill/mark self-use and matches the hourly replay lane better than daily settlement for an hourly strategy
candidate_status = PLANNED_ONLY_NOT_ACCEPTABLE_WITHOUT_EXPLICIT_BOOK_OR_SOURCE_LOCK_AND_EXTERNAL_AUDIT
```

Decision:

```text
VALUATION_END_MARK_POLICY = FAIL_CLOSED_NOT_SOURCE_LOCKED
ACTUAL_PNL_LEDGER = FAIL_CLOSED_NUMERIC_COST_NOT_ACCEPTED_AND_VALUATION_UNRESOLVED
BACKTEST_READINESS = FAIL_CLOSED_NUMERIC_COST_NOT_ACCEPTED_AND_VALUATION_UNRESOLVED
```

## Resolved And Unresolved

Resolved:

```text
book/source cost treatment shape
limit-fill spread cost not applicable
retail futures numeric cost candidate prepared
prop/CFD/adapter/personal costs rejected
valuation candidate identified but not locked
```

Still unresolved before actual cost/PnL/backtest readiness:

```text
operator acceptance of the inferred retail futures cost candidate
external audit of the cost candidate and evidence hashes
explicit book/source-lock and external audit of the first post-fill valuation/end-mark policy
actual cost ledger implementation
actual PnL ledger implementation
backtest-readiness closure
```

## Next Gate Recommendation

Recommended next gate:

```text
S27_V2_INFERRED_RETAIL_COST_ACCEPTANCE_AND_VALUATION_SOURCE_LOCK_GATE
```

Purpose:

- accept or reject the prepared `2.30 USD per contract per side` ZN inferred retail futures cost candidate;
- either source-lock the `NEXT_COMPLETED_HOURLY_CLOSE_AFTER_FILL` valuation candidate from explicit book/source evidence or keep valuation fail-closed;
- run a hostile audit of both decisions before any actual cost/PnL/backtest-readiness implementation;
- preserve no provider/API, no market-data download, no backtest, no result interpretation, and no source-faithful evidence claim.

## Boundary

This record is a policy/evidence source-lock record only. It is not an emitted cost row, not an emitted PnL row, not a result, not a backtest-readiness claim, and not source-faithful strategy evidence.
