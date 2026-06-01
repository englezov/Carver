# Carver S27 ZN Backtest Parity Verification Result

Status:

```text
PASS_S27_ZN_BACKTEST_PARITY_VERIFIED_BEFORE_LOCKBOX
```

Gate: `S27_ZN_BACKTEST_PARITY_VERIFICATION_BEFORE_LOCKBOX`

## Summary

| Period | Stage | Net | Replay Net | Inverted Null Net | Delayed Null Net | Shuffled Null Net |
|---|---|---:|---:|---:|---:|---:|
| ZN_2022_2023_INITIAL_TEST | INITIAL_TEST | 5342.630000000004 | 5342.630000000004 | -15344.869999999997 | -10606.949999999997 | 3494.020000000003 |
| ZN_2024_VALIDATION | VALIDATION | 24618.820000000003 | 24618.820000000003 | -35318.68 | 9151.580000000002 | -14674.314999999999 |

## Boundary

This verifier uses existing local ZN artifacts only. It does not request provider data, download market rows, open OOS/Lockbox/Forward, tune parameters, deploy, trade, promote, or claim alpha. Null tests are bug-detection checks only.
