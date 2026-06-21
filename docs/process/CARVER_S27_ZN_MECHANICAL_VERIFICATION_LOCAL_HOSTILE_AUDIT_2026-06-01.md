# Carver S27 ZN Mechanical Verification Local Hostile Audit

Mode: automatic local hostile audit over the mechanical verifier. No provider API access, no data download, no OOS, no Lockbox, no Forward, no tuning, no deployment, no trading, no promotion, and no Git operation.

## Findings

CRITICAL: None.

HIGH: None.

MEDIUM: None. The verifier recomputes formula, runtime, position, PnL, fee, roll, and boundary checks from existing local artifacts only.

LOW: Episode win rate is preserved as accounting evidence only and must not be treated as an alpha statistic or tuning target.

## Verdict

```text
BLOCKING_FINDINGS: NO
AUDIT_DISPOSITION: PASS_S27_ZN_MECHANICAL_VERIFICATION_DEV_RECON
```
