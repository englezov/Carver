# Carver S27 ZN Opus Round 2 Blocker Close Local Hostile Audit

Mode: automatic local hostile audit over the Opus Round 2 blocker-close artifacts. No provider API access, no data download, no OOS, no Lockbox, no Forward, no tuning, no deployment, no trading, no promotion, and no Git operation.

## Findings

CRITICAL: None. The audited mechanical verifier has no disallowed implementation/spine imports, runtime lag is strict-prior with zero lag-0 rows, and roll fee sides reconcile.

HIGH: Scalar calibration caveat. The final S27 ZN capped forecast mean absolute value does not meet Opus' proposed [9, 11] single-sample heuristic in either period. This is recorded as a caveat and no tuning was performed.

MEDIUM: Residual positive nulls are now attributed against constant-long and deterministic random-position baselines. The baselines do not prove alpha and remain bug-detection/accounting evidence only.

LOW: Random-position baselines are deterministic 64-trial local nulls, not statistical validation or promotion evidence.

## Verdict

```text
BLOCKING_FINDINGS: NO
AUDIT_DISPOSITION: PASS_OPUS_ROUND2_MECHANICAL_BLOCKERS_CLOSED_WITH_SCALAR_HEURISTIC_CAVEAT
SCALAR_HEURISTIC_FAILURES_RECORDED: 2
```
