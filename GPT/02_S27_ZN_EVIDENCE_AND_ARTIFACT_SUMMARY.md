# S27 ZN Evidence And Artifact Summary

## Files Opus Should Treat As Packet Evidence

Primary process records:

```text
docs/process/CARVER_S27_ZN_TOUCHED_HISTORY_DEV_RECON_BACKTEST_RESULT_2026-06-01.md
sha256: D752D1D92D0ABD9CC60887A6E243D159B54FAE80EBDDCE327C31454AA3288036

docs/process/CARVER_S27_ZN_2025_2026_TOUCHED_SUPPORT_DEV_RECON_BACKTEST_RESULT_2026-06-01.md
sha256: BB8AD1B14FA82EC378BD6AC33ED63FD4AF9D8DD8CBA9D55BF1553E901CF6AAFE

docs/process/CARVER_S27_ZN_2025_2026_TOUCHED_SUPPORT_DEV_RECON_LOCAL_HOSTILE_AUDIT_2026-06-01.md
sha256: 0A81F752F0A56817D57C4AC635A19C83D16F51FFFCE1293EEC7AF91C746A6D09
```

Important evidence roots:

```text
docs/researchops/s26_s27_ladder_attribution/ZN_S27/2022_2024/
docs/researchops/s26_s27_pre_lockbox_robustness/ZN_S27/2022_2024/
docs/researchops/s26_s27_pre_lockbox_mcpt/ZN_S27/2022_2024/
docs/researchops/s26_s27_touched_history/ZN_S27/2022-01-04_2026-05-22/
docs/researchops/s26_s27_touched_support_backtest/ZN_S27/2025-01-01_2026-05-22/
```

## 2022-2024 Touched-History Result

Status:

```text
PASS_S27_ZN_TOUCHED_HISTORY_DEV_RECON_BACKTEST_NOT_LOCKBOX_NOT_PROMOTION
```

Usable hourly evidence:

```text
2022-01-04 through 2024-12-31
```

The requested touched-history outer boundary through `2026-05-22` could not be interpreted as complete hourly evidence because post-2024 local support was daily runtime/V/Q/M support only.

Combined 2022-2024 same-input summary:

| Variant | Net after recorded fee | Gross | Recorded fees | Daily win rate |
|---|---:|---:|---:|---:|
| UNIT_NO_LADDER_SAME_INPUT | 9048.16 | 11421.88 | 2373.72 | 0.559908 |
| M1_LADDER_SAME_INPUT | 29961.45 | 40312.50 | 10351.05 | 0.634286 |
| DELTA_M1_MINUS_UNIT | 20913.30 | 28890.62 | 7977.33 | 0.613734 |

Year details from same-input ladder attribution:

| Window | Unit net | M1 ladder net | Delta net | Evidence label |
|---|---:|---:|---:|---|
| 2022-2023 | 1751.69 | 5342.63 | 3590.94 | DEVELOPMENT_RECONCILIATION_FROZEN_INITIAL_ZN_CLAIM |
| 2024 | 7296.47 | 24618.82 | 17322.36 | VALIDATION_STYLE_NON_LOCKBOX_RETAINED_NOT_PRISTINE_LOCKBOX |

## 2025-2026 Touched-Support Result

Status:

```text
FAIL_CLOSED_S27_ZN_2025_2026_TOUCHED_SUPPORT_PROVIDER_DEGRADED_DAYS_AVAILABLE_ROWS_ONLY_NOT_COMPLETE_BACKTEST
```

Effective hourly rows:

```text
2025-01-02 through 2026-05-22
```

This window used Databento hourly ZN rows plus existing local daily runtime/V/Q/M support through `2026-05-22`. It is touched-support Development/Reconciliation only, not Lockbox.

Available-row numeric result:

| Variant | Net after recorded fee | Gross | Recorded fees | Daily win rate |
|---|---:|---:|---:|---:|
| UNIT_NO_LADDER_SAME_INPUT | -10442.45 | -8562.50 | 1879.95 | 0.517857 |
| M1_LADDER_SAME_INPUT | -25697.16 | -15593.75 | 10103.41 | 0.613181 |
| DELTA_M1_MINUS_UNIT | -15254.71 | -7031.25 | 8223.46 | 0.607450 |

Year split:

| Year | Unit net | M1 ladder net | Delta net |
|---|---:|---:|---:|
| 2025 | -6243.19 | -7222.12 | -978.93 |
| 2026 through 2026-05-22 | -4199.26 | -18475.04 | -14275.78 |

Provider degraded dates inside the requested window:

```text
2025-09-17
2025-09-24
2025-11-28
2026-03-15
2026-03-16
2026-04-10
```

Complete-window interpretation is fail-closed. The numeric result is preserved only as available-row diagnostic context.

## Cost Boundary

All reported net values use:

```text
ETF_PUBLIC_PER_SIDE_COMMISSION_ONLY_NO_SPREAD_NO_SLIPPAGE
```

The futures-realistic cost model remains:

```text
FAIL_CLOSED_FUTURES_REALISTIC_COST_READINESS_NOT_EXECUTED
```

Opus should treat all PnL after this fee model as non-promotional and not production-cost-complete.
