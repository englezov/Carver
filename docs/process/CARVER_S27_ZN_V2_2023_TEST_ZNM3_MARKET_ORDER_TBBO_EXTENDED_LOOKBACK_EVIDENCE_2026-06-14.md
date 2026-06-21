# S27 V2 2023 TEST ZNM3 Market-Order TBBO Extended-Lookback Evidence

Date: 2026-06-14

Status:

```text
FAIL_CLOSED_ZNM3_EXTENDED_LOOKBACK_DATABENTO_TBBO_INCOMPLETE_NOT_RESULT
```

This process record was written by the five-row ZNM3-only bounded DataBento TBBO extended-lookback evidence acquisition tool.

Rows:

```text
702, 703, 704, 708, 829
```

Selected row count: `4`
Failed row count: `1`
Failed rows: `704`

Engineering label if quote age exceeds the prior 60-second retry policy:

```text
ZNM3_EXTENDED_LOOKBACK_AT_OR_BEFORE_FILL_TBBO_ENGINEERING_CONVENTION_NOT_BOOK_EXPLICIT
```

Selected rows:

```json
[
  {
    "ask_px_00": 112.71875,
    "bid_px_00": 112.703125,
    "quote_age_seconds": 147.140036,
    "row_index": "702",
    "selected_quote_ts_event": "2023-02-16T02:57:32.859964579Z",
    "selection_status": "PASS_ZNM3_EXTENDED_LOOKBACK_AT_OR_BEFORE_FILL_TBBO_SELECTED_NOT_RESULT"
  },
  {
    "ask_px_00": 112.78125,
    "bid_px_00": 112.765625,
    "quote_age_seconds": 276.013223,
    "row_index": "703",
    "selected_quote_ts_event": "2023-02-16T03:55:23.986777151Z",
    "selection_status": "PASS_ZNM3_EXTENDED_LOOKBACK_AT_OR_BEFORE_FILL_TBBO_SELECTED_NOT_RESULT"
  },
  {
    "ask_px_00": 112.78125,
    "bid_px_00": 112.765625,
    "quote_age_seconds": 67.579802,
    "row_index": "708",
    "selected_quote_ts_event": "2023-02-16T08:58:52.420198009Z",
    "selection_status": "PASS_ZNM3_EXTENDED_LOOKBACK_AT_OR_BEFORE_FILL_TBBO_SELECTED_NOT_RESULT"
  },
  {
    "ask_px_00": 111.984375,
    "bid_px_00": 111.96875,
    "quote_age_seconds": 64.916322,
    "row_index": "829",
    "selected_quote_ts_event": "2023-02-24T01:58:55.083678217Z",
    "selection_status": "PASS_ZNM3_EXTENDED_LOOKBACK_AT_OR_BEFORE_FILL_TBBO_SELECTED_NOT_RESULT"
  }
]
```

This evidence gate does not authorize broader TEST continuation beyond a separate mechanical continuation step, result interpretation, PnL evaluation, tuning, source-faithful evidence claims, VALIDATION, OOS, Lockbox, Forward, adapter work, deployment, trading, promotion, Git actions, or external audit packet preparation.
