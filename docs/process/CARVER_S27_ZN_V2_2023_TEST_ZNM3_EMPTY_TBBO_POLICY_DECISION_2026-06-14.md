# S27 V2 2023 TEST ZNM3 Empty TBBO Policy Decision

Date: 2026-06-14

Status:

```text
ZNM3_EMPTY_TBBO_POLICY_DECISION_EXTENDED_BOUND_REQUEST_PREPARED_NOT_RESULT
```

## Scope

Operator authorized a policy decision gate after local PASS on the consolidated missing-market-order TBBO loop to row 702.

Scope was limited to the five ZNM3 market-order rows that remain missing after bounded batch and retry:

```text
702 ZNM3 SELL 7 2023-02-16T03:00:00Z
703 ZNM3 SELL 2 2023-02-16T04:00:00Z
704 ZNM3 SELL 4 2023-02-16T05:00:00Z
708 ZNM3 SELL 2 2023-02-16T09:00:00Z
829 ZNM3 SELL 7 2023-02-24T02:00:00Z
```

## Existing Evidence

The initial standing batch requested the deterministic `+/-5s` windows for the five rows and failed to select a fresh non-crossed TBBO quote.

The standing retry requested the existing bounded retry windows with 60 seconds pre-fill lookback and 5 seconds post-fill capture. It also failed to select a quote for the five rows.

All five retry normalized CSV outputs are header-only with zero quote rows. The retry raw DBN files exist and are hash-bound, but they do not provide selected bid-side executable evidence under the current policy.

## Decision

The five ZNM3 rows remain fail-closed under currently acquired evidence.

Rejected:

- synthetic spread;
- completed-bar close as spread proxy;
- stale quote beyond the authorized retry window without a separate policy;
- post-fill quote selection;
- book-explicit/source-faithful labeling for any engineering convention.

Accepted next-step proposal:

One additional tightly bounded extended-lookback request may be proposed for separate operator authorization. The request should be limited to the five rows above, use the smallest consistent source-native window, and select only the latest non-crossed positive SELL-side executable bid quote at or before each fill timestamp.

Proposed window:

```text
fill_timestamp - 5 minutes through fill_timestamp + 5 seconds
```

Selection rule:

```text
LATEST_NON_CROSSED_POSITIVE_TBBO_AT_OR_BEFORE_FILL_TIMESTAMP
```

If selected quote age is older than the prior 60-second retry policy but within five minutes, the row must be labeled:

```text
ZNM3_EXTENDED_LOOKBACK_AT_OR_BEFORE_FILL_TBBO_ENGINEERING_CONVENTION_NOT_BOOK_EXPLICIT
```

This label is not book-explicit authority and not source-faithful evidence.

## Hashes

```text
2E6D14F0DF19C542C4EE13BADD7360F4B065721C1334620BC72DD22F75E46CC9  standing batch selected registry
750925628B7B2EAF9A9A31215DDA75026FEA69A1D867C1B5DB1A193D692FE415  standing retry selected registry
B4A929CFB5C27DBBBE8F039DCFE70C65A2DFDCCDE55BFCE9CCB95EAA5B3625FB  standing retry raw output registry
EAE90646CD9CCCE0EFD8DB5211BB96BB3444CB676A18757ECB95A96A31AD80B6  active requirements ledger
```

## Local Hostile Audit

P0 findings: none.

P1 findings: none.

P2 findings: none.

Audit notes:

- The decision accepts no naked PASS claim from prior evidence.
- The five rows remain fail-closed until a separate bounded evidence gate produces byte-visible quotes.
- The proposed extended lookback is row-list bounded, ZNM3-only, at-or-before-fill only, and engineering-labeled if it exceeds 60 seconds.
- No provider/API access, download, new data acquisition, TEST continuation, VALIDATION, OOS, Lockbox, Forward, result interpretation, tuning, Git action, GPT packet, adapter/deployment/trading/promotion, or source-faithful evidence claim occurred in this gate.

## Next Gate

The next useful gate is exactly one bounded ZNM3 extended-lookback TBBO acquisition and continuation gate for rows 702, 703, 704, 708, and 829.
