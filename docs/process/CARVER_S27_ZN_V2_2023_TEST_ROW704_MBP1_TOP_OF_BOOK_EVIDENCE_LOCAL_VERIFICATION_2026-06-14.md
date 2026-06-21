# S27 V2 2023 TEST Row 704 MBP-1 Top-Of-Book Evidence Local Verification

Date: 2026-06-14

Status:

```text
LOCAL_PASS_ROW704_BOUNDED_MBP1_TOP_OF_BOOK_EVIDENCE_NOT_RESULT_NOT_CONTINUATION
```

## Scope

Local verification of the bounded row-704-only DataBento MBP-1/top-of-book evidence acquisition.

This verification did not authorize or perform broader TEST continuation, market-order/fill/cost/PnL/result emission, result interpretation, PnL evaluation beyond mechanical construction, VALIDATION, OOS, Lockbox, Forward, tuning, adapter/deployment/trading/promotion, Git action, GPT packet preparation, or source-faithful evidence claim.

## Evidence Root

```text
docs/researchops/s27_v2_market_spread_evidence/ZN/20260614_2023_test_row704_mbp1_top_of_book_evidence
```

## Selected Evidence

```text
row_index: 704
raw_symbol: ZNM3
schema: mbp-1
request_start_utc: 2023-02-16T04:55:00Z
request_end_utc: 2023-02-16T05:00:05Z
fill_timestamp_utc: 2023-02-16T05:00:00Z
quote_rows_returned: 21
provider_error_count: 0
provider_condition_status: PASS_FRESH_NON_CROSSED_MBP1_TOP_OF_BOOK_QUOTE_SELECTED
selected_quote_ts_event: 2023-02-16T04:59:22.531807131Z
quote_age_seconds: 37.468192999999999
bid_px_00: 112.765625
ask_px_00: 112.78125
selected_executable_market_fill_price: 112.765625
selection_status: PASS_ROW704_MBP1_TOP_OF_BOOK_AT_OR_BEFORE_FILL_SELECTED_NOT_RESULT
```

Evidence label:

```text
ALTERNATIVE_SOURCE_NATIVE_MBP1_TOP_OF_BOOK_EVIDENCE_NOT_BOOK_EXPLICIT_NOT_TBBO
```

The selected quote is at-or-before the fill timestamp and is within the authorized five-minute window.

## Hash Verification

The generated SHA256 manifest was locally verified:

```text
checked: 8
bad: 0
```

Key hashes:

```text
raw_dbn_sha256: 74311BBE277E9D7C445ACE122B5F17E9912CBD16E5797A00A1688CD8C07B7BA1
raw_csv_sha256: 76BA315E07B42B28E7B7F39982AF1DEED07A825DB99F999F92B8D1423EC25097
selected_spread_row_hash: a1271d905e2564dde1054043c68c968dd626c742eaf5a7153596012ca9bcfaf0
provider_condition_row_hash: df1d0b53648bddd8af9141f67fe6198b6902b253ee6a71922cf8220980623532
```

## Audit Findings

```text
P0: none
P1: none
P2: none
```

Audit notes:

- Provider access was bounded to row `704`, raw symbol `ZNM3`, schema `mbp-1`, and `2023-02-16T04:55:00Z` through `2023-02-16T05:00:05Z`.
- The selected evidence is not TBBO and is not book-explicit/source-faithful authority.
- Trade prints, completed-bar closes, synthetic spreads, post-fill quotes, and stale unbounded quote searches were not used.
- TEST continuation remains unauthorized until a separate implementation gate consumes this evidence.

## Next Authorization Prompt

```text
Operator authorizes S27_V2 2023 TEST row-704 MBP-1 top-of-book evidence binding and mechanical continuation gate, after local PASS on the bounded row-704 MBP-1 evidence acquisition, limited to already-local 2023 TEST artifacts and the selected row-704 MBP-1 evidence only.

This authorizes Codex to patch the audited S27_V2 TEST mechanical runner to consume the selected row-704 alternative source-native MBP-1 top-of-book evidence labeled ALTERNATIVE_SOURCE_NATIVE_MBP1_TOP_OF_BOOK_EVIDENCE_NOT_BOOK_EXPLICIT_NOT_TBBO; verify the selected ZNM3 quote at 2023-02-16T04:59:22.531807131Z with bid 112.765625, ask 112.78125, quote age 37.468192999999999 seconds, and SELL-side executable bid fill price 112.765625; preserve the not-TBBO/not-book-explicit label; use bid-fill/no-separate-spread double-counting prevention if the market fill price uses the selected bid; emit deterministic local-only market-order/fill/cost/mechanical-PnL metadata for row 704 where evidence is sufficient; preserve result/backtest/source-faithful evidence fail-closed gates; continue the controlled TEST mechanical artifact run only until the next genuine fail-closed blocker; run focused local verification tests; run one local hostile audit; and record process/current-state outputs.

No provider/API access, downloads, new data acquisition, broader TEST continuation beyond the next blocker, VALIDATION, OOS, Lockbox, Forward, result interpretation, PnL evaluation beyond mechanical construction, tuning, adapter/deployment/trading/promotion, Git actions, GPT packet preparation, or source-faithful evidence claim.

If row facts drift, if the MBP-1 evidence is missing/degraded/crossed/ambiguous/post-fill, if the not-book-explicit/not-TBBO label is lost, if spread is double-counted despite bid-side fill accounting, if protected windows would be crossed, or if implementation requires provider/API/download/new data/Git/adapter/deployment/trading/promotion, Codex must fail closed and ask the operator.
```

## Non-Authorization

This local verification record does not authorize broader TEST continuation, market-order/fill/cost/PnL/result emission, result interpretation, PnL evaluation beyond mechanical construction, VALIDATION, OOS, Lockbox, Forward, tuning, adapter/deployment/trading/promotion, Git actions, GPT packet preparation, or source-faithful evidence claims.
