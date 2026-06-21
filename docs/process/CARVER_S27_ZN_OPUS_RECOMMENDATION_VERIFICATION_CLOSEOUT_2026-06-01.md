# Carver S27 ZN Opus Recommendation Verification Closeout

Date: 2026-06-01

Status:

```text
PASS_S27_ZN_OPUS_RECOMMENDED_MECHANICAL_VERIFICATION_DEV_RECON_ONLY
```

## Scope

This closeout records the remaining Opus-recommended verification work after the scalar issue was resolved.

It covers:

```text
input-lineage/no-lookahead audit
independent forecast/position/PnL verification
roll/back-adjustment and runtime-alignment checks
fee/episode/null-test review
local hostile audit preservation
Development/Reconciliation disposition
```

No provider API access, no new data download, no new market-row parsing, no OOS, no Lockbox, no Forward, no tuning, no deployment, no trading, no promotion, and no Git operation was performed by this closeout.

## Scalar Blocker Disposition

Resolved before this closeout:

```text
docs/process/CARVER_S27_SCALAR_BLOCKER_DISPOSITION_2026-06-01.md
docs/process/CARVER_S27_SCALAR_BLOCKER_LOCAL_LEAN_HOSTILE_AUDIT_2026-06-01.md
```

Result:

```text
S26 scalar: 9.3
S27 scalar: 20.0 / around 20 per Chapter 27 p. 502
BACKTEST_RESULT_SCALAR_STATUS: NOT_FAILED_BY_SCALAR_ATOM
```

## Evidence Matrix

| Opus recommendation | Evidence | Disposition |
|---|---|---|
| Input-lineage/no-lookahead audit | `docs/researchops/s26_s27_parity/ZN_S27/2022_2024/lookahead/20260601_S27_ZN_2022_2024_PARITY_VERIFIER_lookahead_ledger.csv`; `docs/researchops/s26_s27_mechanical_verification/ZN_S27/2022_2024/roll_runtime/20260601_S27_ZN_2022_2024_MECHANICAL_VERIFIER_roll_runtime_ledger.csv` | PASS. Runtime lags are strict-prior and non-stale; max lag is 1 day in both periods. |
| Independent forecast verification | `tools/audit/carver_s27_zn_mechanical_verifier.py`; `docs/researchops/s26_s27_mechanical_verification/ZN_S27/2022_2024/checks/20260601_S27_ZN_2022_2024_MECHANICAL_VERIFIER_check_ledger.csv` | PASS. Recomputes S26 EWMA(5), daily EWMAC(16,64), V/Q/M EWMA(10), adjusted raw forecast, sigma bridge, S27 scalar 20.0, and cap. |
| Independent position/PnL verification | Same mechanical verifier and check ledger | PASS. Recomputes base position, forecast multiplier, desired unrounded/rounded contracts, close-to-close PnL, fee sides, and net PnL. |
| Roll/back-adjustment and runtime alignment | Mechanical roll/runtime ledger plus existing local lineage files | PASS at Development/Reconciliation mechanical scope. Roll events are explicitly ledgered and fee-sided; runtime rows are aligned strict-prior. This is not a production continuous-contract authority claim. |
| Fee/episode/null-test review | `docs/researchops/s26_s27_mechanical_verification/ZN_S27/2022_2024/fees/20260601_S27_ZN_2022_2024_MECHANICAL_VERIFIER_fee_ledger.csv`; `docs/researchops/s26_s27_mechanical_verification/ZN_S27/2022_2024/episodes/20260601_S27_ZN_2022_2024_MECHANICAL_VERIFIER_episode_ledger.csv`; `docs/researchops/s26_s27_parity/ZN_S27/2022_2024/null_tests/20260601_S27_ZN_2022_2024_PARITY_VERIFIER_null_antistrategy_ledger.csv` | PASS as accounting/bug-detection evidence only. Episode win rate and null tests are not alpha statistics and must not tune parameters, symbols, costs, or windows. |
| Local hostile audit preservation | `docs/process/CARVER_S27_ZN_BACKTEST_PARITY_VERIFICATION_LOCAL_HOSTILE_AUDIT_2026-06-01.md`; `docs/process/CARVER_S27_ZN_MECHANICAL_VERIFICATION_LOCAL_HOSTILE_AUDIT_2026-06-01.md` | PASS. |

## Mechanical Verification Summary

```text
Verifier: tools/audit/carver_s27_zn_mechanical_verifier.py
Status: PASS_S27_ZN_MECHANICAL_VERIFICATION_DEV_RECON
```

| Period | Checks | Net after fees | Gross PnL | Fees | Episodes | Episode win rate | Fee sides | Max runtime lag |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| ZN_2022_2023_INITIAL_TEST | 38/38 | 5342.630000000004 | 10343.75 | 5001.12 | 1015 | 0.6334975369458128 | 3312 | 1 |
| ZN_2024_VALIDATION | 38/38 | 24618.820000000003 | 29968.75 | 5349.93 | 699 | 0.6781115879828327 | 3543 | 1 |

## Null-Test Review

Null tests remain bug-detection only:

| Period | Base net | Inverted net | One-bar delayed net | Day-shuffled net | Interpretation |
|---|---:|---:|---:|---:|---|
| ZN_2022_2023_INITIAL_TEST | 5342.630000000004 | -15344.869999999997 | -10606.949999999997 | 3494.020000000003 | Inversion and delay break the result; day shuffle remains positive, so it is not a decisive anti-alpha proof. |
| ZN_2024_VALIDATION | 24618.820000000003 | -35318.68 | 9151.580000000002 | -14674.314999999999 | Inversion and day shuffle break the result; one-bar delay remains positive, so it is not a decisive anti-alpha proof. |

These mixed null results do not mechanically fail the result, but they also do not prove alpha. They only support the narrower conclusion that the implementation is not trivially sign-flipped or solely a one-row accounting artifact.

## Development/Reconciliation Disposition

```text
BLOCKING_FINDINGS: NO
AUDIT_DISPOSITION: PASS_S27_ZN_OPUS_RECOMMENDED_MECHANICAL_VERIFICATION_DEV_RECON_ONLY
MECHANICAL_TRUST_STATUS: MECHANICALLY_VERIFIED_AT_DEV_RECON_SCOPE
ALPHA_CLAIM_STATUS: NOT_AUTHORIZED
PROMOTION_STATUS: CLOSED
OOS_LOCKBOX_FORWARD_STATUS: CLOSED
```

This closeout means the current S27 ZN result is mechanically stronger than the earlier replay-only state. It does not make the result production-ready, deployment-ready, prop-firm-ready, or alpha-claim-ready.

## Remaining Closed

The following remain closed unless separately authorized:

```text
OOS
Lockbox
Forward
parameter tuning
symbol/window/cost selection after seeing results
production continuous-contract authority
official settlement substitution
limit-order fill simulation
spread/slippage model
prop-firm flattening rule
CFD adapter execution
old QuantLab active-pipeline use
deployment
trading
promotion
```
