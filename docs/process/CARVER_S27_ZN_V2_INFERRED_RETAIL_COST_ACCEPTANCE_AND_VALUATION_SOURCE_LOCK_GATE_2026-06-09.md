# S27_V2 Inferred Retail Cost Acceptance And Valuation Source-Lock Gate

Date: 2026-06-09

Status:

```text
PROCESS_ONLY_INFERRED_RETAIL_COST_ACCEPTED_FOR_LOCAL_DEV_RECON_VALUATION_FAIL_CLOSED
```

## Authorization

Operator authorized the `S27_V2 inferred retail cost acceptance and valuation source-lock gate` after local PASS on the numeric cost assumption and valuation policy source-lock gate.

Scope was limited to:

- accepting or rejecting the prepared NinjaTrader free-plan ZN inferred retail futures cost candidate of `2.30 USD` per contract per side;
- either source-locking the first post-fill valuation/end-mark policy from explicit book/source evidence or keeping valuation fail-closed.

## Non-Authorization

This record authorizes no provider/API access, no market-data download, no OOS, no Lockbox, no Forward, no backtest, no result-scored run, no actual cost emission, no actual PnL ledger emission, no result emission, no result interpretation, no PnL evaluation, no tuning, no adapter work, no deployment, no trading, no promotion, no Git action, and no source-faithful evidence claim.

## Inputs Inspected

```text
Carver.pdf
docs/process/CARVER_S27_ZN_BOOK_SOURCE_LOCK_2026-06-05.md
docs/process/CARVER_PROJECT_WIDE_SOURCE_NATIVE_COST_POLICY_RULE_2026-06-09.md
docs/process/CARVER_S27_ZN_V2_NUMERIC_COST_ASSUMPTION_AND_VALUATION_POLICY_SOURCE_LOCK_GATE_2026-06-09.md
docs/process/CARVER_S27_ZN_V2_NUMERIC_COST_ASSUMPTION_AND_VALUATION_POLICY_SOURCE_LOCK_LOCAL_AUDIT_RESULT_2026-06-09.md
docs/process/CARVER_S27_ZN_V2_POSITIVE_ACTION_NUMERIC_COST_VALUATION_REMEDIATION_GATE_2026-06-09.md
docs/process/CARVER_S27_ZN_V2_POSITIVE_ACTION_COST_IMPLEMENTATION_RECORD_2026-06-09.md
docs/process/CARVER_S27_ZN_V2_POSITIVE_ACTION_PNL_BLOCKED_IMPLEMENTATION_RECORD_2026-06-09.md
```

No provider API, credentialed source, market-data download, diagnostic, backtest, result-scored run, actual cost emission, actual PnL emission, or Git action was used.

## Cost Acceptance Decision

The book/source lock gives treatment shape but no ZN-specific numeric commission:

```text
ALL_ORDERS_PAY_COMMISSION
LIMIT_ORDER_FILL_COST = COMMISSION_ONLY
MARKET_ORDER_FILL_COST = COMMISSION_PLUS_NORMAL_BID_ASK_SPREAD
BOOK_EXPLICIT_NUMERIC_ZN_COMMISSION = FAIL_CLOSED_NOT_FOUND
```

The project-wide cost policy permits `SOURCE_NATIVE_INFERRED_RETAIL_FUTURES_COSTS` when the book does not specify enough costs, provided prop-firm, CFD, adapter, and personal costs are rejected and the assumption is clearly labeled.

Accepted inferred cost assumption:

```text
S27_V2_INFERRED_RETAIL_COST_ACCEPTANCE = ACCEPTED_FOR_LOCAL_ONLY_DEV_RECON_IMPLEMENTATION
classification = SOURCE_NATIVE_INFERRED_RETAIL_FUTURES_COSTS
not_classification = BOOK_EXPLICIT_COSTS
accepted_cost_candidate = NINJATRADER_FREE_PLAN_ALL_IN_ZN_2_30_USD_PER_CONTRACT_PER_SIDE
accepted_commission_per_contract = 2.30
accepted_commission_unit = USD_PER_CONTRACT_PER_SIDE_ALL_IN_RETAIL_FUTURES_TRANSACTION_FEE
candidate_round_turn_equivalent = 4.60
instrument = ZN / ZNM6
positive_action_fill_scope = LIMIT_FILL_SELL_1_AT_2026-04-13T14:00:00Z
```

Rationale:

- the book does not provide source-exact ZN commission;
- the prepared candidate is source-native retail futures evidence, not prop-firm, CFD, adapter, or personal-account cost;
- the free-plan assumption avoids amortizing paid subscription plans into strategy costs;
- the candidate is conservative relative to the paid NinjaTrader plans recorded in the prior source-lock gate;
- TradeStation retail pricing was used only as a broad retail-futures plausibility cross-check, not as the accepted source.

Boundary:

```text
ACTUAL_COST_EMISSION_AUTHORIZED = FALSE
ACTUAL_PNL_EMISSION_AUTHORIZED = FALSE
RESULT_OR_BACKTEST_AUTHORIZED = FALSE
SOURCE_FAITHFUL_EVIDENCE_CLAIM = FALSE
```

The accepted cost assumption may be used only after separate operator authorization for an actual local-only cost ledger implementation gate.

## Valuation Source-Lock Decision

Book/source evidence inspected supports these general rules:

```text
futures holding PnL uses price changes times point value
trading costs are separated from holding PnL
back-adjusted prices reflect rolling PnL while ignoring trading costs
S26/S27 fills are tested with hourly one-hour-lag assumptions
PnL rows must be tied to fills and held position state
```

This is not enough to source-lock the first post-fill valuation/end-mark timestamp for the audited open short position after:

```text
fill_timestamp_utc = 2026-04-13T14:00:00Z
fill_price = 111.046875
position_after_fill = -1
```

Rejected for this gate:

```text
FIRST_POST_FILL_VALUATION_CANDIDATE = NEXT_COMPLETED_HOURLY_CLOSE_AFTER_FILL
candidate_status = NOT_ACCEPTED_NOT_SOURCE_LOCKED
```

Reason:

The book supports hourly backtesting and one-hour-lag execution assumptions, but this gate did not find explicit book/source evidence that the first valuation mark for a newly opened S27 position must be the next completed hourly close rather than same fill-candidate close, session close, next daily close, realized-only until exit, or another mark ledger convention.

Decision:

```text
VALUATION_END_MARK_POLICY = FAIL_CLOSED_NOT_SOURCE_LOCKED
ACTUAL_PNL_LEDGER = FAIL_CLOSED_VALUATION_END_MARK_POLICY_NOT_SOURCE_LOCKED
BACKTEST_READINESS = FAIL_CLOSED_VALUATION_END_MARK_POLICY_NOT_SOURCE_LOCKED
```

## Decision Hashes

Canonical decision blocks are the UTF-8 bytes of the exact text blocks below, including final newline.

```text
COST_ACCEPTANCE_DECISION_BLOCK_SHA256 = 68cfd732aa2b38ef0aa88c686690ad98c25bf3a1a597835bf706a6354eaefa58
VALUATION_FAIL_CLOSED_DECISION_BLOCK_SHA256 = 580a20ac566b48e0591bf55100bb47d24aca6dea6a0b4260650f0eb0056c1b7d
```

`COST_ACCEPTANCE_DECISION_BLOCK`:

```text
decision=S27_V2_INFERRED_RETAIL_COST_ACCEPTED_FOR_LOCAL_ONLY_DEV_RECON_IMPLEMENTATION
accepted_cost_candidate=NINJATRADER_FREE_PLAN_ALL_IN_ZN_2_30_USD_PER_CONTRACT_PER_SIDE
accepted_commission_per_contract=2.30
unit=USD_PER_CONTRACT_PER_SIDE_ALL_IN_RETAIL_FUTURES_TRANSACTION_FEE
scope=ZNM6_S27_V2_POSITIVE_ACTION_LIMIT_FILL_AND_LATER_LOCAL_ONLY_DEV_RECON_COST_LEDGER_IMPLEMENTATION_ONLY
classification=SOURCE_NATIVE_INFERRED_RETAIL_FUTURES_COSTS
not_classification=BOOK_EXPLICIT_COSTS
actual_cost_emission_authorized=false
source_faithful_evidence_claim=false
```

`VALUATION_FAIL_CLOSED_DECISION_BLOCK`:

```text
decision=VALUATION_END_MARK_POLICY_FAIL_CLOSED_NOT_SOURCE_LOCKED
first_post_fill_valuation_candidate=NEXT_COMPLETED_HOURLY_CLOSE_AFTER_FILL
candidate_status=NOT_ACCEPTED_NOT_SOURCE_LOCKED
required_before_pnl=explicit_book_or_source_lock_plus_local_hostile_audit
actual_pnl_emission_authorized=false
backtest_readiness=false
```

## Rejected Cost Classes

```text
PROP_FIRM_COSTS
EVALUATION_FEES
PAYOUT_RULES
CFD_BROKER_SPREADS
CFD_SWAPS
ADAPTER_COSTS
PERSONAL_ACCOUNT_COSTS
```

## Next Gate Recommendation

The next useful gate is actual cost metadata/ledger implementation only, not PnL or backtest readiness:

```text
S27_V2_POSITIVE_ACTION_ACTUAL_COST_LEDGER_IMPLEMENTATION_USING_ACCEPTED_INFERRED_RETAIL_COST
```

That future gate may use the accepted `2.30 USD` per-contract-per-side inferred retail futures cost assumption for the audited local-only positive-action limit fill, but it must still forbid PnL/result/backtest emission because valuation remains fail-closed.

## Boundary

This record is a policy/evidence decision record only. It is not an actual cost ledger, not an actual PnL ledger, not a result, not backtest readiness, not result interpretation, not PnL evaluation, and not a source-faithful evidence claim.
