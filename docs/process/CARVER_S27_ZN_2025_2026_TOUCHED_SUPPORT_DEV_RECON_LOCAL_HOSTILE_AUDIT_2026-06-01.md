# Local Lean Hostile Audit - S27 ZN 2025-2026 Touched-Support Dev/Recon Backtest

Mode: automatic local hostile audit. Databento access was authorized only for exact ZN hourly `ohlcv-1h` rows over the declared 2025-2026 window. No OOS, Lockbox, Forward, Git operations, deployment, trading, or promotion.

## Findings

CRITICAL: Provider-condition degraded dates are present inside the requested window: `2025-09-17, 2025-09-24, 2025-11-28, 2026-03-15, 2026-03-16, 2026-04-10`. The numeric result is preserved as available-row diagnostic context, but the complete-window backtest interpretation is fail-closed.

HIGH: The run is not pristine Lockbox because daily runtime/V/Q/M support history was already touched through `2026-05-22`.

MEDIUM: Futures-realistic costs remain fail-closed. The run uses recorded ETF/public per-side commission only and no spread/slippage.

LOW: The yearly and win-rate summaries are descriptive touched-support evidence only, not validation, Lockbox, or alpha evidence.

## Verdict

```text
BLOCKING_FINDINGS: YES_FOR_COMPLETE_WINDOW_BACKTEST_INTERPRETATION
AUDIT_DISPOSITION: FAIL_CLOSED_PROVIDER_DEGRADED_DAYS_NUMERIC_RESULT_AVAILABLE_ROWS_ONLY_NOT_LOCKBOX_NOT_PROMOTION
```
