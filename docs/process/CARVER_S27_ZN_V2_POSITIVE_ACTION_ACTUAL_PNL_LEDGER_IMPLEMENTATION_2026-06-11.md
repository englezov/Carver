# S27_V2 Positive-Action Actual PnL Ledger Implementation

Date: 2026-06-11

Status:

```text
LOCAL_POSITIVE_ACTION_ACTUAL_PNL_LEDGER_IMPLEMENTED_NOT_RESULT_NOT_BACKTEST_NOT_SOURCE_FAITHFUL_EVIDENCE
```

## Authorization

Operator authorized the `S27_V2 positive-action actual PnL ledger implementation gate` after local PASS on the declared valuation mark-row pack.

Scope was limited to the audited `ZNM6` positive-action short fill at:

```text
fill_timestamp_utc = 2026-04-13T14:00:00Z
fill_price = 111.046875
fill_quantity = 1
position_after_fill = -1
```

and the declared next-completed-hourly valuation mark row at:

```text
valuation_mark_completed_timestamp_utc = 2026-04-13T15:00:00Z
valuation_mark_close_price = 111.046875
valuation_convention = SOURCE_NATIVE_ENGINEERING_VALUATION_ASSUMPTION_NOT_BOOK_EXPLICIT
```

## Non-Authorization

This implementation authorizes no provider/API access, no market-data downloads, no new data acquisition, no OOS, no Lockbox, no Forward, no backtests, no result-scored runs, no result emission, no result interpretation, no PnL evaluation beyond mechanical row construction, no tuning, no adapter work, no deployment, no trading, no promotion, no Git actions, and no source-faithful evidence claim.

## Files

Implemented:

```text
src/carver/spine/s27_v2_replay/positive_action_actual_pnl_executable.py
```

Focused tests:

```text
tests/test_s27_v2_positive_action_actual_pnl_executable.py
```

File SHA256:

```text
positive_action_actual_pnl_executable.py = 86AC516D3B38B58ECDC9E67AD6E3AC0B15633CC7D87F7B4F13EA2CB3613E989B
test_s27_v2_positive_action_actual_pnl_executable.py = 61BE905A88C11DEEE193AAA82FE579AF506135D764236376D35FFE3693DEE5AE
```

## Active Binding

The actual PnL bundle rebuilds and validates:

- active positive-action actual-cost bundle;
- active limit-fill row;
- accepted inferred retail commission cost `2.30 USD` per contract per side;
- declared valuation mark manifest bytes;
- declared valuation mark CSV bytes;
- declared valuation mark local audit bytes;
- static ZN point value `1000 USD` per full point;
- result/backtest/source-faithful evidence non-authorizations.

Pinned valuation mark hashes:

```text
valuation_mark_manifest_sha256 = f5a5eb85ee5acfb13e914e2cfc0d3583c41f8c133ee79c188c70881d3e23b90e
valuation_mark_csv_sha256 = b859f397e62ed3e8acef743003e3a543929d246d5bb98d95fa9f2fbd08758e26
valuation_mark_local_audit_sha256 = 550dcff7234d43691f0ce9ecdda674df7897de96fe4de177b8ce97f8d22b86c8
valuation_mark_source_row_text_sha256 = f39f5056c9d1e122e6f62d82e8918745e10233aa95abef9949ac5f50be6f98da
valuation_mark_source_row_canonical_json_sha256 = a8d60ee8a26ee10b8460fea2f46c656eba0eeb7be507badd4fe44434de8b413a
```

## Mechanical PnL Row

Build output:

```text
ACTUAL_PNL_BUILD_PASS
bundle_hash e0a5e01d1a944822c0af107f3b65e1c7ec90e2c7a8e0b40dff722cef3472a80e
row_hash 709c2dac4a586dd7d41843bddba6fbb71685d09162cf471089bd0377a8ab8c90
actual_cost_bundle_hash e7c001459aec5c7b6d8a8cdecad089ccb07a9e18da053135473c173044314a1d
actual_cost_row_hash 9eed2343d8d77c534dbda0a4302b952506e94e1b9ba35f7b236ef9e1c833d9b9
fill_bundle_hash 196328c2cd7471999f249bda21064f09c1fd7efd5252437d6122541df2cbf211
limit_fill_row_hash 2a0870fc368c839a337aac47865bdb19df5315d57a6c894e047b44819ddfe801
```

Mechanical arithmetic:

```text
gross_pnl_amount = (111.046875 - 111.046875) * abs(1) * 1000.0 = 0.0 USD
commission_cost_amount = 2.30 USD
spread_cost_amount = 0.0 USD
total_cost_amount = 2.30 USD
net_pnl_amount = 0.0 - 2.30 = -2.30 USD
```

The row is an actual PnL ledger row for local Development/Reconciliation mechanics only. It is not a result row, not a backtest, not result interpretation, not PnL evaluation, not promotion, and not a source-faithful evidence claim.

## Tests

Focused test results:

```text
python -m pytest tests\test_s27_v2_positive_action_actual_pnl_executable.py -q --tb=short
54 passed in 284.51s (0:04:44)
```

Adjacent chain regression tests:

```text
python -m pytest tests\test_s27_v2_positive_action_fill_executable.py tests\test_s27_v2_positive_action_actual_cost_executable.py -q --tb=short
75 passed in 108.55s (0:01:48)
```

## Boundary

The module is not exported from package root. Standalone row validation raises `CarverBlocked`; only the bundle path accepts, and only after rebuilding active cost and valuation mark evidence.

Result rows, backtest rows, result interpretation, PnL evaluation beyond mechanical row construction, source-faithful evidence claims, provider/API access, downloads/new data, OOS/Lockbox/Forward, Git actions, adapter/deployment/trading/promotion, and tuning remain unauthorized.
