# CARVER S27 ZN V2 2023 TEST Row 1378 TBBO Policy Decision

Date: 2026-06-21

Status:

```text
ROW1378_FIRST_POST_FILL_TBBO_ENGINEERING_SPREAD_CONVENTION_ACCEPTED_NOT_BOOK_EXPLICIT_NOT_RESULT
```

## Scope

This record is limited to S27_V2 2023 TEST row `1378`, `ZNM3`, `SELL 2`, fill candidate `2023-03-31T00:00:00Z`.

The primary bounded TBBO request from `2023-03-30T23:59:55Z` through `2023-03-31T00:00:05Z` and the 60-second bounded retry from `2023-03-30T23:59:00Z` through `2023-03-31T00:00:05Z` both failed to find an eligible at-or-before-fill TBBO quote. Both requests returned only the first post-fill quote:

```text
ts_event = 2023-03-31T00:00:00.183796035Z
bid = 114.515625
ask = 114.53125
quote_lag_seconds = 0.183796035
```

The declared completed hourly fill candidate close for row `1378` is `114.515625`. The first post-fill TBBO bid is also `114.515625`.

## Decision

The following row-specific engineering convention is accepted for local-only mechanical TEST artifact completion:

```text
ROW1378_FIRST_POST_FILL_TBBO_QUOTE_SPREAD_EVIDENCE_ENGINEERING_CONVENTION_NOT_BOOK_EXPLICIT
```

This convention is not book-explicit, not source-faithful Carver authority, and not a general post-fill quote policy. It is bounded to row `1378` because:

- bounded at-or-before-fill TBBO evidence was unavailable;
- the first post-fill quote is less than one second after the fill timestamp;
- the selected SELL bid equals the declared completed fill-candidate close;
- the bid/ask quote is positive and non-crossed;
- the selected row remains local-only mechanical construction and not result interpretation.

## Non-Authorizations

This decision does not authorize provider/API access, downloads, new data acquisition, broader TEST pack expansion, VALIDATION, OOS, Lockbox, Forward, result interpretation, PnL evaluation beyond mechanical construction, tuning, Git actions, GPT/Opus packet preparation, adapter/deployment/trading/promotion, or source-faithful evidence claims.
