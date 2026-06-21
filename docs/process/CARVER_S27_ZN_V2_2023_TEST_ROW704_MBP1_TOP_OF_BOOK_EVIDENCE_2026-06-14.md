# S27 V2 2023 TEST Row 704 MBP-1 Top-Of-Book Evidence

Date: 2026-06-14

Status:

```text
PASS_ROW704_BOUNDED_MBP1_TOP_OF_BOOK_SELECTED_NOT_RESULT
```

## Scope

Bounded row-704-only DataBento MBP-1/top-of-book evidence acquisition after no-eligible-TBBO policy remediation.

## Request

```text
provider: DATABENTO_HISTORICAL
dataset: GLBX.MDP3
schema: mbp-1
stype_in: raw_symbol
raw_symbol: ZNM3
request_start_utc: 2023-02-16T04:55:00Z
request_end_utc: 2023-02-16T05:00:05Z
fill_timestamp_utc: 2023-02-16T05:00:00Z
```

## Evidence Label

```text
ALTERNATIVE_SOURCE_NATIVE_MBP1_TOP_OF_BOOK_EVIDENCE_NOT_BOOK_EXPLICIT_NOT_TBBO
```

## Selected Evidence

```text
selected_row_count: 1
failed_row_count: 0
quote_rows_returned: 21
provider_error_count: 0
provider_condition_status: PASS_FRESH_NON_CROSSED_MBP1_TOP_OF_BOOK_QUOTE_SELECTED
selection_status: PASS_ROW704_MBP1_TOP_OF_BOOK_AT_OR_BEFORE_FILL_SELECTED_NOT_RESULT
selected_quote_ts_event: 2023-02-16T04:59:22.531807131Z
quote_age_seconds: 37.468193
bid_px_00: 112.765625
ask_px_00: 112.78125
selected_executable_market_fill_price: 112.765625
```

## Non-Authorization

This record does not authorize TEST continuation, market-order/fill/cost/PnL/result emission, result interpretation, PnL evaluation beyond mechanical construction, VALIDATION, OOS, Lockbox, Forward, tuning, adapter/deployment/trading/promotion, Git actions, GPT packet preparation, or source-faithful evidence claims.
