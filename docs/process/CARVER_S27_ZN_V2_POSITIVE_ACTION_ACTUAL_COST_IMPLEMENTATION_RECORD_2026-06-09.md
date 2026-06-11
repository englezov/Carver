# S27_V2 Positive-Action Actual Cost Implementation Record

Date: 2026-06-09

Status:

```text
LOCAL_POSITIVE_ACTION_ACTUAL_COST_LEDGER_IMPLEMENTED_NOT_PNL_NOT_RESULT
```

## Authorization

Operator authorized the `S27_V2 positive-action actual cost ledger implementation using the locally accepted inferred retail futures cost assumption`.

Scope was limited to the audited `ZNM6` positive-action limit fill and the accepted NinjaTrader free-plan inferred retail futures cost:

```text
fill_timestamp_utc = 2026-04-13T14:00:00Z
fill_price = 111.046875
fill_quantity = 1
accepted_commission_per_contract = 2.30 USD per contract per side
```

## Non-Authorization

This implementation authorizes no provider/API access, no market-data downloads, no OOS, no Lockbox, no Forward, no backtests, no result-scored runs, no actual PnL ledger emission, no result emission, no result interpretation, no PnL evaluation, no tuning, no adapter work, no deployment, no trading, no promotion, no Git actions, and no source-faithful evidence claim.

## Implemented Surface

Added:

```text
src/carver/spine/s27_v2_replay/positive_action_actual_cost_executable.py
tests/test_s27_v2_positive_action_actual_cost_executable.py
```

Public builder:

```text
build_positive_action_actual_cost_executable(...)
```

The builder rebuilds and validates the active locally passed positive-action fill bundle, byte-hash binds the accepted inferred retail cost decision record, then emits one deterministic actual local-only cost ledger row for the audited limit fill.

Standalone actual-cost rows remain non-authoritative and fail closed outside bundle validation.

## Accepted Cost Policy Binding

The accepted inferred retail futures cost policy is:

```text
accepted_cost_policy_label = NINJATRADER_FREE_PLAN_ALL_IN_ZN_2_30_USD_PER_CONTRACT_PER_SIDE
classification = SOURCE_NATIVE_INFERRED_RETAIL_FUTURES_COSTS
not_classification = BOOK_EXPLICIT_COSTS
commission_per_contract = 2.30
commission_unit = USD_PER_CONTRACT_PER_SIDE_ALL_IN_RETAIL_FUTURES_TRANSACTION_FEE
cost_acceptance_decision_block_sha256 = 68cfd732aa2b38ef0aa88c686690ad98c25bf3a1a597835bf706a6354eaefa58
accepted_cost_decision_record_sha256 = fe3bde381260c5e9022ab52632d0aff73133293835676baa205bf916690a005d
```

Prop-firm, CFD, adapter, and personal trading costs remain explicitly rejected.

## Emitted Actual Cost

For the active `SELL 1` limit fill:

```text
commission_amount = 2.30 * abs(fill_quantity) = 2.30
spread_cost_amount = 0.0
spread_cost_reason = LIMIT_FILL_NO_MARKET_SPREAD_COST_BY_SOURCE_LOCK
total_cost_amount = 2.30
total_cost_currency = USD
```

The prior positive-action cost-policy evidence module remains a historical fail-closed evidence surface. This actual-cost surface is the later, separately authorized downstream cost ledger that consumes the accepted inferred retail cost decision.

## Boundary

Valuation and PnL remain fail-closed:

```text
VALUATION_END_MARK_POLICY = FAIL_CLOSED_NOT_SOURCE_LOCKED
ACTUAL_PNL_LEDGER = FAIL_CLOSED_VALUATION_END_MARK_POLICY_NOT_SOURCE_LOCKED
RESULT_STATUS = FAIL_CLOSED_RESULT_ROW_NOT_EMITTED_NOT_AUTHORIZED
BACKTEST_STATUS = FAIL_CLOSED_BACKTEST_RESULT_NOT_EMITTED_NOT_AUTHORIZED
```

This actual-cost row is not PnL, not a result, not a backtest, not result interpretation, not PnL evaluation, and not a source-faithful evidence claim.

## Active Hashes

```text
bundle_hash = e7c001459aec5c7b6d8a8cdecad089ccb07a9e18da053135473c173044314a1d
actual_cost_row_hash = 9eed2343d8d77c534dbda0a4302b952506e94e1b9ba35f7b236ef9e1c833d9b9
fill_bundle_hash = 196328c2cd7471999f249bda21064f09c1fd7efd5252437d6122541df2cbf211
limit_fill_row_hash = 2a0870fc368c839a337aac47865bdb19df5315d57a6c894e047b44819ddfe801
cost_parameter_file_hash = e6b7c69a712fd7a5effbabbd4c809f24c1a6dfabbfb1ce317b387c923ac7f098
cost_parameter_row_hash = 069f25beb5c42bb030081883f3b16298c1aa610cd3ecccb94ab887bdf271513c
accepted_cost_policy_hash = 8613b1a712ec58969eb477581746c3ea3a729a0a6d642982e4a8cc224defce42
accepted_cost_decision_record_hash = fe3bde381260c5e9022ab52632d0aff73133293835676baa205bf916690a005d
source_cost_treatment_hash = 2b432dbc2d5cdb8794af1462b9492065b1bd25c81f574b016d010f5bb800fa40
limit_fill_cost_treatment_hash = 7d03cd3c9784ac05cf7d7b8028d6e359231d960d4d4644089a6faf238dfb0341
prop_cfd_adapter_cost_rejection_hash = f39dbca16cdc0a8e2f9ddc051b4e036677a9b2036a5d61ee009e5388014bab64
valuation_fail_closed_decision_block_sha256 = 580a20ac566b48e0591bf55100bb47d24aca6dea6a0b4260650f0eb0056c1b7d
```

## Verification

Focused verification passed:

```text
python -m py_compile src\carver\spine\s27_v2_replay\positive_action_actual_cost_executable.py -> PASS
python -m pytest tests\test_s27_v2_positive_action_actual_cost_executable.py -q -> 43 passed
```

An adjacent combined fill/cost/actual-cost pytest run exceeded the local 180-second command cap and is not recorded as a pass or failure.

## Next Gate

The next required step is local hostile audit of the positive-action actual cost ledger surface.

Actual PnL rows, result rows, backtests, result interpretation, PnL evaluation, source-faithful evidence claims, provider/API access, market-data downloads, OOS/Lockbox/Forward access, Git actions, adapter/deployment/trading/promotion, and tuning remain unauthorized.
