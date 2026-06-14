# S27 V2 ZN 2023 TEST Market-Order TBBO Failed-Window Retry

Date: 2026-06-12

Status:

```text
FAIL_CLOSED_BOUNDED_DATABENTO_TBBO_FAILED_WINDOW_RETRY_INCOMPLETE_NOT_RESULT
```

This process record was written by the bounded DataBento TBBO failed-window retry tool.

Scope:

- Failed row indices: `78, 208, 210, 212, 215, 220, 306, 328, 329, 335, 340`
- Retry lookback seconds: `60`
- Retry lookahead seconds: `5`
- Selection rule: `LATEST_NON_CROSSED_POSITIVE_TBBO_AT_OR_BEFORE_FILL_TIMESTAMP`
- Post-fill quote selection: `DISALLOWED_TO_AVOID_LOOKAHEAD`

Counts:

- Requirements count: `11`
- Selected row count: `10`
- Failed row count: `1`
- Failed row indices after retry: `215`

This evidence gate does not authorize broader TEST continuation, result interpretation, PnL evaluation, tuning, source-faithful evidence claims, VALIDATION, OOS, Lockbox, Forward, adapter work, deployment, trading, promotion, Git actions, or external audit packet preparation.
