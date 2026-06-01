# Local Hostile Audit - S27 ZN Ladder Attribution

Mode: automatic local hostile audit over same-input attribution artifacts.

CRITICAL: None for declared attribution/reconciliation scope.

HIGH: None. The script uses existing local ZN artifacts only and does not open provider/API access, new data, OOS, Lockbox, Forward, deployment, trading, promotion, Git operations, CFD adapters, or old QuantLab active pipelines.

MEDIUM: The result prepares a tiny Lockbox case but does not open it. Any future Lockbox access still requires a separate operator gate.

MEDIUM: 2024 is retained as validation-style non-Lockbox evidence, not pristine Lockbox evidence.

LOW: Costs remain ETF public per-side commission only; spread, slippage, order-fill quality, and prop-firm rules remain outside this attribution.

Verdict:

```text
BLOCKING_FINDINGS: NO_FOR_DECLARED_ATTRIBUTION_SCOPE
AUDIT_DISPOSITION: PASS_S27_ZN_LADDER_ATTRIBUTION_AND_BASELINE_RECONCILIATION_NOT_LOCKBOX
```
