# Local Lean Hostile Audit - S26 ZN 2022-2023 Comparison TEST

Mode: automatic local lean hostile audit over generated S26 comparison artifacts.

## Findings

CRITICAL: None.

HIGH: None.

MEDIUM: None.

The artifact stays inside the one-time 2022-2023 TEST exception for direct S26
versus existing S27 comparison. It uses existing local ZN artifacts only. It
does not call Databento, download new data, touch OOS/Lockbox/Forward, use CFD
adapters, change S27, tune any parameter/window/cost/ladder, or promote.

S26 does not consume the S27 safety stack. The generated S26 positions are
computed only from S26 capped forecast divided by 10, using unit plumbing and
nearest-contract rounding to match the existing comparison surface.

## Validation

```text
VALIDATION_ROWS: 10
BLOCKING_VALIDATION_FINDINGS: 0
```

```text
BLOCKING_FINDINGS: NO
AUDIT_DISPOSITION: PASS_S26_ZN_2022_2023_COMPARISON_TEST_SCOPE
```
