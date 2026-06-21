# S27 V2 ZN 2023 TEST Row 215 TBBO Policy Decision

Date: 2026-06-12

Status:

```text
ROW215_NEAREST_AFTER_FILL_ENGINEERING_SPREAD_CONVENTION_ACCEPTED_NOT_BOOK_EXPLICIT_NOT_RESULT
```

## Scope

This record is limited to the S27_V2 2023 TEST row 215 market-order spread evidence blocker.

- Row index: `215`
- Raw symbol: `ZNH3`
- Decision timestamp: `2023-01-16T16:00:00Z`
- Fill candidate timestamp: `2023-01-16T17:00:00Z`
- Order side: `SELL`
- Order quantity: `2`
- Starting position: `2`
- Desired position: `0`
- Position change: `-2`
- Market-order reason: `BOOK_REQUIRED_TARGET_POSITION_GAP_GREATER_THAN_ONE_CONTRACT`

## Evidence Inspected

Requirements ledger:

```text
docs/researchops/s27_v2_market_spread_evidence/ZN/20260612_2023_test_market_order_tbbo_requirements_discovery/market_order_tbbo_requirements.csv
```

Failed-window retry output:

```text
docs/researchops/s27_v2_market_spread_evidence/ZN/20260612_2023_test_market_order_tbbo_failed_window_retry
```

Row 215 retry raw DBN SHA256:

```text
D0E90468C0B3DE8449BE1A3EC1F00E86B58E9BEA070692701D09D3807D558854
```

Row 215 retry raw CSV SHA256:

```text
E61AF6FE47224E084AFDFC8CEA381463C93D869F5E36E35EAC0A29E62DCF65D0
```

2023 TEST hourly source ledger SHA256:

```text
2E0949A79484D508051CEA66D450DE8123691EF7B7D160A29EC0D18F790E8CCB
```

## Failed Strict Rule

The strict at-or-before-fill quote rule remains:

```text
LATEST_NON_CROSSED_POSITIVE_TBBO_AT_OR_BEFORE_FILL_TIMESTAMP
```

That rule failed closed for row 215 because no non-crossed positive TBBO quote at or before `2023-01-16T17:00:00Z` was present in either bounded request.

The bounded retry returned two quotes, both after the fill timestamp:

| ts_event | bid | ask | bid_size | ask_size |
| --- | ---: | ---: | ---: | ---: |
| `2023-01-16T17:00:00.681503831Z` | `114.625` | `114.640625` | `538` | `266` |
| `2023-01-16T17:00:03.383914463Z` | `114.625` | `114.640625` | `538` | `265` |

The declared completed hourly fill bar for `2023-01-16T17:00:00Z` is provider-available and has close `114.625`. The first post-fill TBBO bid is also `114.625`.

## Decision

For row 215 only, accept the following engineering spread convention for future local-only TEST mechanical continuation:

```text
ROW215_FIRST_POST_FILL_TBBO_QUOTE_SPREAD_EVIDENCE_ENGINEERING_CONVENTION_NOT_BOOK_EXPLICIT
```

The accepted quote is:

- Quote timestamp: `2023-01-16T17:00:00.681503831Z`
- Quote lag after fill timestamp: `0.681503831` seconds
- Bid: `114.625`
- Ask: `114.640625`
- Full spread: `0.015625` points
- ZN point value: `1000 USD`
- Full spread value per contract: `15.625 USD`
- SELL-side executable bid evidence: `114.625`

This convention may be used only as local-only Development/TEST mechanical spread evidence for row 215. It is not book-explicit Carver authority, not a source-faithful evidence claim, and not result interpretation.

## Rationale

The strict no-lookahead at-or-before quote rule is preferable and remains the default. Row 215 is a provider timestamp edge case: the first available TBBO event is 681 milliseconds after the completed fill timestamp, and its bid equals the already-declared completed hourly close used by the market-fill machinery.

Accepting this quote as a row-specific engineering spread convention prevents a single timestamp-edge TBBO gap from stopping the mechanical TEST artifact run, while preserving explicit labeling and auditability.

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
- result interpretation;
- PnL evaluation;
- tuning;
- adapter work;
- deployment;
- trading;
- promotion;
- Git actions;
- GPT packet preparation;
- source-faithful evidence claims.

Any implementation consuming this policy requires separate explicit operator authorization.
