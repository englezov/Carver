# Local Lean Hostile Audit - S27 ZN Touched-History Dev/Recon Backtest

Mode: automatic local hostile audit over existing local artifacts only. No provider API access, no data download, no OOS, no Lockbox, no Forward, no Git operations.

## Findings

CRITICAL: None.

HIGH: Post-2024 through `2026-05-22` is fail-closed for hourly S27 backtesting. Local daily runtime support is not source-frequency-compatible hourly evidence.

MEDIUM: Futures-realistic costs remain fail-closed. The reproduced backtest uses the recorded ETF/public per-side commission-only assumption and no spread/slippage.

LOW: Summary statistics are touched-history Development/Reconciliation only and must not be read as validation, Lockbox, or promotion evidence.

## Verdict

```text
BLOCKING_FINDINGS: NO_FOR_TOUCHED_HISTORY_DEV_RECON_SCOPE
AUDIT_DISPOSITION: PASS_TOUCHED_HISTORY_DEV_RECON_NOT_LOCKBOX_NOT_PROMOTION
```
