# S27 V2 ZN 2023 TEST Row 1356 Market-Order TBBO Evidence

Date: 2026-06-16

Status:

```text
FAIL_CLOSED_ROW1356_BOUNDED_DATABENTO_TBBO_INCOMPLETE_NOT_RESULT
```

This record is written under `S27_V2_2023_TEST_ROW1356_BOUNDED_MARKET_ORDER_TBBO_EVIDENCE_AND_CONTINUATION_GATE` and the standing bounded market-order TBBO spread evidence policy.

Row index: `1356`
Selected quote timestamp: ``
Quote age seconds: ``
Bid: ``
Ask: ``
Selected executable SELL market fill price: ``

Provider condition: `FAIL_CLOSED_NO_FRESH_NON_CROSSED_TBBO_QUOTE_SELECTED`

## Bounded Request

```text
provider: DATABENTO_HISTORICAL
dataset: GLBX.MDP3
schema: tbbo
stype_in: raw_symbol
raw_symbol: ZNM3
request_start_utc: 2023-03-29T23:59:55Z
request_end_utc: 2023-03-30T00:00:05Z
fill_candidate_timestamp_utc: 2023-03-30T00:00:00Z
order_side: SELL
order_quantity: 2
```

## Failure Detail

The bounded request returned two quote rows and no provider error, but both quote events were after the fill timestamp:

```text
2023-03-30T00:00:00.099806785Z bid 114.484375 ask 114.5
2023-03-30T00:00:00.624029447Z bid 114.484375 ask 114.5
```

No at-or-before-fill fresh, positive, non-crossed TBBO quote was available in the authorized row-1356 window, so no selected SELL executable bid evidence was bound and no TEST continuation was run.

## Hash Binding

```text
raw_dbn_sha256: E6D5A558A453532EEA88F81C3501A7EF8EC2E0CD5D3F30BAF3197AA0C106F9EF
raw_csv_sha256: AC539F45B3A4D24F6018A33B1182FBE74AA4788A748151778DDE995F4B2216CC
selected_spread_registry_sha256: F3F62EA496D478F410B38856D5371FB7B2D0A1C497EFFA61BFE01DB1D65A1813
provider_condition_ledger_sha256: DEF071B43839F2226962C5C5FB8E0EE910F99AADDB735839B1080ED35552F35D
selected_spread_row_hash: 00c2e2a413edcf7881f3915232c137929cc62f972276e7a4fd3402fd968bc5ed
provider_condition_row_hash: b8e5e1e95bdaceefc00c68d66aaae0114ca49b503ef1c394ae4cc833313c06a9
```

## Local Verification

`py_compile` passed for the row-1356 acquisition tool and patched TEST runner. The generated SHA256 manifest checked `8` files with `0` mismatches.

This evidence gate does not authorize broader provider/API access, general downloads, broader TEST continuation beyond the next mechanical blocker, result interpretation, PnL evaluation, tuning, source-faithful evidence claims, VALIDATION, OOS, Lockbox, Forward, adapter work, deployment, trading, promotion, Git actions, or external audit packet preparation.
