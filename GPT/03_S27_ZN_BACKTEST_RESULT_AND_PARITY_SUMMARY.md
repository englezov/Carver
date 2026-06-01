# S27 ZN Backtest Result, Parity, And Mechanical Verification Summary

Status:

```text
RESULT_AND_VERIFICATION_SUMMARY_FOR_HOSTILE_AUDIT
```

## Primary Result Artifacts

| Artifact | SHA256 |
|---|---:|
| `docs/process/CARVER_S27_ZN_M1_LADDER_DEV_RECON_BACKTEST_RESULT_2026-05-31.md` | `266675E1E3A615DAF048A45FD821CBA8662020290B6D8FBB24B931F2BB21625D` |
| `docs/process/CARVER_S27_ZN_2024_VALIDATION_BACKTEST_RESULT_2026-06-01.md` | `C805DC758F8471ECCCD559D8293B1332B9E114CF1C9DBC944E4BBD7F22EDC3EE` |
| `docs/process/CARVER_S27_ZN_BACKTEST_PARITY_VERIFICATION_RESULT_2026-06-01.md` | `350FE44B1046488F8F22F03AB95B333607695CDA7E941D6C2EEDB852D0E768F4` |
| `docs/process/CARVER_S27_ZN_MECHANICAL_VERIFICATION_RESULT_2026-06-01.md` | `EA3E6E7C0FE9EF3E8178E9041060136BDE08F080DC50D75E0411815513BA2FF6` |
| `docs/process/CARVER_S27_ZN_OPUS_RECOMMENDATION_VERIFICATION_CLOSEOUT_2026-06-01.md` | `98D44F61B2E21A84549B7C91BA3ACB08E550950A36A992CA3123FB180E93019A` |
| `docs/process/CARVER_S27_ZN_MECHANICAL_VERIFICATION_LOCAL_HOSTILE_AUDIT_2026-06-01.md` | `C96C2A7681DEC26FFC0C64D51E709CC3EFABB51B16D5193E56014834211DD8BD` |

## ZN 2022-2023 Initial Test

Status:

```text
PASS_S27_ZN_M1_STYLE_LADDER_DEV_RECON_BACKTEST_NOT_ALPHA
```

Window:

```text
requested: 2022-01-01 through 2023-12-31
effective: 2022-01-04 through 2023-12-29
```

Mechanical verification summary:

| Field | Value |
|---|---:|
| mechanical checks | 40/40 |
| gross PnL | 10343.75 |
| estimated ETF fees | 5001.12 |
| net after ETF fees | 5342.630000000004 |
| nonzero sign episodes | 1015 |
| winning episodes | 643 |
| episode win rate | 0.6334975369458128 |
| total fee sides | 3312 |
| max runtime lag days | 1 |

By year from original backtest summary:

| Year | Gross | Fees | Net |
|---|---:|---:|---:|
| 2022 | 6390.62 | 2189.50 | 4201.12 |
| 2023 | 3953.12 | 2811.62 | 1141.50 |

## ZN 2024 Validation Artifact

Status:

```text
PASS_S27_ZN_2024_VALIDATION_BACKTEST_NOT_ALPHA
```

Window:

```text
requested: 2024-01-01 through 2024-12-31
effective: 2024-01-02 through 2024-12-31
```

Mechanical verification summary:

| Field | Value |
|---|---:|
| mechanical checks | 40/40 |
| gross PnL | 29968.75 |
| estimated ETF fees | 5349.93 |
| net after ETF fees | 24618.820000000003 |
| nonzero sign episodes | 699 |
| winning episodes | 474 |
| episode win rate | 0.6781115879828327 |
| total fee sides | 3543 |
| max runtime lag days | 1 |

## Existing Parity Verification

Existing local parity verifier status:

```text
PASS_S27_ZN_BACKTEST_PARITY_VERIFIED_BEFORE_LOCKBOX
```

Parity result:

| Period | Stage | Net | Replay Net | Inverted Null Net | Delayed Null Net | Shuffled Null Net |
|---|---|---:|---:|---:|---:|---:|
| ZN_2022_2023_INITIAL_TEST | INITIAL_TEST | 5342.630000000004 | 5342.630000000004 | -15344.869999999997 | -10606.949999999997 | 3494.020000000003 |
| ZN_2024_VALIDATION | VALIDATION | 24618.820000000003 | 24618.820000000003 | -35318.68 | 9151.580000000002 | -14674.314999999999 |

Existing parity verifier checks:

- aggregate PnL replay from forecast/hourly rows;
- row-level spot replay;
- lookahead checks on runtime lag and position timing;
- timestamp lineage subset checks;
- inverted, one-bar delayed, and day-shuffled null tests.

## Mechanical Verifier Output Artifacts

Root:

```text
docs/researchops/s26_s27_mechanical_verification/ZN_S27/2022_2024/
```

Generated ledgers:

| Ledger | SHA256 |
|---|---:|
| `checks/20260601_S27_ZN_2022_2024_MECHANICAL_VERIFIER_check_ledger.csv` | `164B1DED1C6A8C7652D86982E49AAC8A631D0379386B037D8D6D976E1134AB77` |
| `episodes/20260601_S27_ZN_2022_2024_MECHANICAL_VERIFIER_episode_ledger.csv` | `C94920CFA99CC90A8CE71ECDB2755276AFE03B5161A2C50DC674CF033A842A3C` |
| `fees/20260601_S27_ZN_2022_2024_MECHANICAL_VERIFIER_fee_ledger.csv` | `F0D8CE802175C23F06AAD7ED516363EDC45D3DD14FB7EF5E98DB9654B13CE37C` |
| `roll_runtime/20260601_S27_ZN_2022_2024_MECHANICAL_VERIFIER_roll_runtime_ledger.csv` | `D018D1BB16B88BD4E2B8ADB3A1CA631B30BBD2996DA874AD062257CACFDA13EA` |
| `summary/20260601_S27_ZN_2022_2024_MECHANICAL_VERIFIER_summary.csv` | `D93A1F28655B632CB07356528BED6997835466F9ECC01D9A91561472A2FE9980` |
| `status/20260601_S27_ZN_2022_2024_MECHANICAL_VERIFIER_status.json` | `86122913CD8A71DD8C2DDE90B330730563A8F4251D2742D268F2E309348D52F9` |
| `provenance/20260601_S27_ZN_2022_2024_MECHANICAL_VERIFIER_provenance.json` | `8AC32E59C1127D4A7368FE3B90FB8493C62332C1CE24D7F469520D1C6F50AB5B` |

Mechanical verifier status:

```text
PASS_S27_ZN_MECHANICAL_VERIFICATION_DEV_RECON
```

It recomputes S26 EWMA(5), S27 EWMAC(16,64), V/Q/M EWMA(10), sigma-price bridge, S27 adjusted forecast, scalar 20.0, cap +/-20, base position, forecast multiplier, rounded position, close-to-close PnL, fee sides, roll-transition fee sides, runtime lag, provider condition, and no-promotion boundaries.
