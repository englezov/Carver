# S27 V2 2023 TEST Row 1356 TBBO Policy Decision

Date: 2026-06-16

Status:

```text
ROW1356_NEAREST_AFTER_FILL_ENGINEERING_SPREAD_CONVENTION_ACCEPTED_NOT_BOOK_EXPLICIT_NOT_RESULT
```

## Scope

This record is limited to the S27_V2 2023 TEST row 1356 market-order spread evidence blocker after bounded row-1356 TBBO evidence failed closed with post-fill-only quotes.

- Row index: `1356`
- Raw symbol: `ZNM3`
- Decision timestamp: `2023-03-29T23:00:00Z`
- Fill candidate timestamp: `2023-03-30T00:00:00Z`
- Order side: `SELL`
- Order quantity: `2`
- Starting position: `8`
- Desired position: `6`
- Position change: `-2`
- Market-order reason: `BOOK_REQUIRED_TARGET_POSITION_GAP_GREATER_THAN_ONE_CONTRACT`

## Evidence Inspected

Row-1356 bounded TBBO evidence record:

```text
docs/process/CARVER_S27_ZN_V2_2023_TEST_ROW1356_MARKET_ORDER_TBBO_EVIDENCE_2026-06-16.md
```

Row-1356 bounded TBBO output root:

```text
docs/researchops/s27_v2_market_spread_evidence/ZN/20260616_2023_test_row1356_market_order_tbbo
```

Raw DBN SHA256:

```text
E6D5A558A453532EEA88F81C3501A7EF8EC2E0CD5D3F30BAF3197AA0C106F9EF
```

Raw CSV SHA256:

```text
AC539F45B3A4D24F6018A33B1182FBE74AA4788A748151778DDE995F4B2216CC
```

Selected-spread registry SHA256:

```text
F3F62EA496D478F410B38856D5371FB7B2D0A1C497EFFA61BFE01DB1D65A1813
```

Provider-condition ledger SHA256:

```text
DEF071B43839F2226962C5C5FB8E0EE910F99AADDB735839B1080ED35552F35D
```

## Failed Strict Rule

The strict at-or-before-fill quote rule remains:

```text
LATEST_NON_CROSSED_POSITIVE_TBBO_AT_OR_BEFORE_FILL_TIMESTAMP
```

That rule failed closed for row 1356 because no non-crossed positive TBBO quote at or before `2023-03-30T00:00:00Z` was present in the bounded row-1356 request.

The bounded request returned two quotes, both after the fill timestamp:

| ts_event | bid | ask | bid_size | ask_size |
| --- | ---: | ---: | ---: | ---: |
| `2023-03-30T00:00:00.099806785Z` | `114.484375` | `114.5` | `56` | `468` |
| `2023-03-30T00:00:00.624029447Z` | `114.484375` | `114.5` | `195` | `440` |

The declared completed hourly fill bar for `2023-03-30T00:00:00Z` has close `114.484375`. The first post-fill TBBO bid is also `114.484375`.

## Decision

For row 1356 only, accept the following engineering spread convention for future local-only TEST mechanical continuation:

```text
ROW1356_FIRST_POST_FILL_TBBO_QUOTE_SPREAD_EVIDENCE_ENGINEERING_CONVENTION_NOT_BOOK_EXPLICIT
```

The accepted quote is:

- Quote timestamp: `2023-03-30T00:00:00.099806785Z`
- Quote lag after fill timestamp: `0.099806785` seconds
- Bid: `114.484375`
- Ask: `114.5`
- Full spread: `0.015625` points
- ZN point value: `1000 USD`
- Full spread value per contract: `15.625 USD`
- SELL-side executable bid evidence: `114.484375`

This convention may be used only as local-only TEST mechanical spread evidence for row 1356. It is not book-explicit Carver authority, not source-faithful evidence, not result interpretation, and not a backtest/result claim.

## Rationale

The strict no-lookahead at-or-before quote rule is preferable and remains the default. Row 1356 is a provider timestamp-edge case: the first available TBBO event is approximately 100 milliseconds after the completed fill timestamp, and its bid equals the already-declared completed hourly close used by the market-fill machinery.

This matches the previously accepted row-215 policy shape, while preserving row-specific labeling and preventing general post-fill quote use. Row 704 remains a separate no-eligible-TBBO class because its remediation required an alternate source-native MBP-1/top-of-book evidence stream rather than accepting a naked no-quote convention.

## Boundaries

This record does not authorize:

- provider/API access;
- downloads;
- new data acquisition;
- broader TEST continuation;
- VALIDATION access;
- OOS access;
- Lockbox access;
- Forward access;
- market-order/fill/cost/PnL emission;
- result interpretation;
- PnL evaluation beyond mechanical construction;
- tuning;
- adapter work;
- deployment;
- trading;
- promotion;
- Git actions;
- GPT packet preparation;
- source-faithful evidence claims.

Any implementation consuming this policy requires separate explicit operator authorization.

## Local Hostile Audit

No separate subagent audit was run for this process-only gate. A local process-only self-audit found:

```text
P0: none
P1: none
P2: none
```

Audit notes:

- The strict at-or-before-fill rule remains default and still failed for row 1356.
- The row-1356 post-fill convention is accepted only because the first post-fill TBBO quote is within one second and the SELL bid equals the declared completed fill close.
- The policy is row-specific and not book-explicit/source-faithful.
- No provider/API access, new data, broader TEST continuation, result interpretation, Git action, GPT packet, tuning, adapter/deployment/trading/promotion, or protected-window access was authorized or performed.

## Next Authorization Prompt

```text
Operator authorizes S27_V2 2023 TEST row-1356 post-fill TBBO engineering convention implementation and mechanical continuation gate, after row-1356 TBBO policy decision, limited to already-local 2023 TEST artifacts and already-acquired row-1356 TBBO evidence.

This authorizes Codex to bind the row-1356 first post-fill TBBO quote at 2023-03-30T00:00:00.099806785Z with bid 114.484375, ask 114.5, quote lag 0.099806785 seconds, and label ROW1356_FIRST_POST_FILL_TBBO_QUOTE_SPREAD_EVIDENCE_ENGINEERING_CONVENTION_NOT_BOOK_EXPLICIT; update deterministic selected-spread/combined TBBO registries; emit deterministic local-only SELL 2 market-order/fill/cost/mechanical-PnL metadata where evidence is sufficient; preserve result/backtest/source-faithful evidence fail-closed gates; continue the controlled TEST mechanical artifact run only until the next genuine blocker; run focused local verification tests; run one local hostile audit if available; and record process/current-state outputs.

No provider/API access, downloads, new data acquisition, broader TEST continuation beyond the next blocker, VALIDATION, OOS, Lockbox, Forward, result interpretation, PnL evaluation beyond mechanical construction, tuning, adapter/deployment/trading/promotion, Git actions, GPT packet preparation, or source-faithful evidence claim.

If row facts drift, if the first post-fill TBBO quote is not exactly bound, if the not-book-explicit engineering label is lost, if spread is double-counted despite bid-side fill accounting, if protected windows would be crossed, or if implementation requires provider/API/download/new data/Git/adapter/deployment/trading/promotion, Codex must fail closed and ask the operator.
```
