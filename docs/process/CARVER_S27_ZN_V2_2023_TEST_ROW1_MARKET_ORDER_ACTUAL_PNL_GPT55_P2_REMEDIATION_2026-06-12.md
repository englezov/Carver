# S27_V2 2023 TEST Row-1 Market-Order Actual-PnL GPT 5.5 P2 Remediation

Date: 2026-06-12

Status:

```text
LOCAL_PASS_GPT55_P2_REMEDIATED_PENDING_EXTERNAL_REAUDIT_NOT_RESULT
```

## Scope

This record covers the narrow remediation of the GPT 5.5 hostile-audit P2 findings for the S27_V2 2023 TEST row-1 market-order actual-PnL mechanical ledger gate.

The scoped row remains:

```text
decision_timestamp_utc = 2023-01-03T00:00:00Z
fill_timestamp_utc = 2023-01-03T01:00:00Z
valuation_mark_timestamp_utc = 2023-01-03T02:00:00Z
raw_symbol = ZNH3
starting_position_contracts = 0
desired_position_contracts = 2
position_change_contracts = 2
order_side = BUY
order_quantity = 2
fill_quantity = 2
fill_price = 112.5625
valuation_mark_close = 112.59375
gross_pnl = 62.5
commission = 4.6
net_pnl = 57.9
```

This is still mechanical ledger construction only. It is not result interpretation, not a result-scored run, not promotion evidence, and not a source-faithful evidence claim.

## GPT Finding

GPT 5.5 confirmed the attached row-1 ledgers and arithmetic passed the requested mechanical PnL/cost checks, but found one P2 machine-freeze hardening gap:

```text
LOCKED_MARKET_ORDER_EXECUTED_FULL_GAP was not strictly bound to:
- market_order_required = TRUE
- market_order_rows_emitted = TRUE
- coherent side/sign for position_change_contracts
- transition ending position equal to desired position
- fill position_after_fill equal to desired position
- pnl ending_position_contracts equal to desired position
```

The actual emitted row was correct, but the guard could accept forged contradictory rows.

## Patch

Patched:

```text
src/carver/spine/s27_v2_replay/pretest_machine_freeze.py
tests/test_s27_v2_2023_test_mechanical_run.py
```

Guard changes:

- removed `LOCKED_MARKET_ORDER_EXECUTED_FULL_GAP` from the no-market-needed status set;
- require locked market-order status to have both `market_order_required = TRUE` and `market_order_rows_emitted = TRUE`;
- bind `position_change_contracts` to `desired_position_contracts - starting_position_contracts`;
- bind transition starting position to position starting position;
- require full-gap market orders to have `abs(position_change_contracts) > 1`;
- require order side to match the signed position change;
- require order quantity and fill quantity to equal the full gap;
- require executed fill;
- bind transition ending position, fill position after fill, and PnL ending position to the desired target position.

Regression tests added:

- locked market status with `market_order_required = FALSE` and `market_order_rows_emitted = FALSE` is rejected;
- wrong order side for signed position change is rejected;
- transition ending-position mismatch is rejected;
- fill position-after-fill mismatch is rejected;
- PnL ending-position mismatch is rejected.

## Verification

Focused verification passed:

```text
python -m pytest tests\test_s27_v2_2023_test_mechanical_run.py -q
27 passed
```

Neighboring pre-TEST verification passed:

```text
python -m pytest tests\test_s27_v2_pretest_development_recon_completion.py tests\test_s27_v2_2023_test_mechanical_run.py -q
88 passed
```

## Current Status

```text
LOCAL_PASS_GPT55_P2_REMEDIATED_PENDING_EXTERNAL_REAUDIT_NOT_RESULT
```

Recommended next step is a narrow GPT 5.5 re-audit of the remediated row-1 actual-PnL mechanical ledger guard, focused only on the closed P2 boundary and existing row arithmetic.

## Non-Authorizations

This record does not authorize provider/API access, downloads, new data acquisition, broader TEST continuation, VALIDATION, OOS, Lockbox, Forward, result interpretation, PnL evaluation beyond mechanical row construction, tuning, adapter work, deployment, trading, promotion, Git actions, or source-faithful evidence claims.
