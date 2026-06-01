# Requested Hostile Audit And Known Anomalies

Status:

```text
REQUEST_FOR_HOSTILE_AUDIT_OF_IMPLEMENTED_VERIFICATION
```

## What We Need From Opus

Please audit the implemented S27 ZN source-native futures verification state.

The previous Opus concern was that the positive S27 ZN result might be mechanically wrong because of lookahead, roll/runtime alignment, scalar mismatch, PnL sign, fee-side undercounting, or shared-code verification weakness.

Since then, the remaining Opus recommendations were implemented:

- scalar issue resolved source-faithfully: S26 `9.3`, S27 around `20`;
- local synthetic/unit suite rerun;
- parity verifier rerun;
- new mechanical verifier implemented;
- local hostile audit preserved;
- Development/Reconciliation closeout created.

Please determine whether anything important is still missing before this can be called mechanically trusted at Development/Reconciliation scope.

## Known Weirdness

The ZN result is positive in both the initial 2022-2023 artifact and the 2024 validation artifact.

The shape is unusual:

- 2022-2023 is positive but modest after fees.
- 2024 is very positive.
- Episode win rate is high.
- Existing null tests mostly break the result, but one shuffled/null variant in 2022-2023 remains positive and one delayed-null variant in 2024 remains positive.
- Pure ES source-native result was negative.
- Archived old QuantLab US500 CFD result was positive, but that old result is not equivalent to the current source-native futures backtester.

## Archived US500 CFD Positive Anomaly

The archived `QuantLab_v3` `US500` CFD result is preserved as:

```text
PROCESS_ONLY_ARCHIVED_CFD_POSITIVE_ANOMALY_PRESERVED_NOT_SOURCE_NATIVE_AUTHORITY
```

Key old result:

| Metric | Value |
|---|---:|
| symbol | US500 CFD |
| lane | CFD_DIRECT / ICMarkets |
| window | OOS_2024 |
| completed trade episodes | 138 |
| gross PnL USD | 679.4629807946758 |
| spread cost USD | 138.0 |
| swap USD | -242.96699999999998 |
| net PnL USD | 298.49598079467575 |
| profit factor | 1.4058859723863821 |
| daily Sharpe | 1.5884131556972074 |

It remains non-authoritative because it used old CFD data, old QuantLab state machinery, old cost/execution assumptions, and old pipeline governance.

## Verification Already Performed

Fresh local verification commands:

```text
python -m unittest tests.test_s26_s27_fast_mean_reversion_synthetic -v
42 tests passed

python -m unittest discover -s tests -v
198 tests passed, 1 skipped

python tools\audit\carver_s27_zn_parity_verifier.py
PASS_S27_ZN_BACKTEST_PARITY_VERIFIED_BEFORE_LOCKBOX

python tools\audit\carver_s27_zn_mechanical_verifier.py
PASS_S27_ZN_MECHANICAL_VERIFICATION_DEV_RECON
```

Mechanical verifier produced 80 total check rows across both periods:

```text
ZN_2022_2023_INITIAL_TEST: 40/40
ZN_2024_VALIDATION: 40/40
```

## Questions For Opus

Please answer:

1. Are the current artifacts sufficient to call the S27 ZN result mechanically verified at Development/Reconciliation scope?
2. Does the mechanical verifier remain too dependent on generated artifacts from the original path?
3. Is the scalar issue fully resolved, or is there still a source-faithfulness risk?
4. Are the runtime lag/no-lookahead checks enough to rule out same-day daily close leakage into intraday hourly forecasts?
5. Are roll/back-adjustment checks enough for Development/Reconciliation, or is official settlement/continuous-authority still blocking?
6. Are the fee-side and roll-transition fee checks sufficient, given the current ETF per-side commission-only model?
7. Are the null tests correctly scoped as bug detectors only?
8. What additional blocker would you look for first if the result still feels too smooth?
9. What should the next clean gate be?

## Potential Blocking Findings To Look For

Treat any of the following as potentially blocking if still plausible:

- use of future daily runtime state in hourly rows;
- same-day daily close used for intraday forecast;
- completed trading-date error around evening sessions;
- wrong contract selected near roll;
- accidental stale sigma or V/Q/M carry-forward;
- wrong sign on `equilibrium - price`;
- wrong sign on trend-opposition gating;
- S27 scalar regression back to S26 `9.3`;
- cap leakage or missing cap;
- wrong ZN multiplier;
- PnL sign reversed;
- fee sides undercounted;
- flat bars counted as trades;
- validation artifact sharing too much code with initial artifact;
- mechanical verifier sharing the same core bug as the original backtest;
- null tests accidentally using the same bugged assumptions;
- old QuantLab or CFD assumptions leaking into source-native futures.

## Desired Verdict Format

Please produce:

```text
BLOCKING_FINDINGS: YES/NO
AUDIT_DISPOSITION: <specific disposition>
RECOMMENDED_NEXT_GATE: <single next gate>
```

Also include:

- high/medium/low findings;
- what evidence is enough;
- what evidence is still not enough;
- what remains closed.

## Non-Authorization

This packet authorizes no new provider access, no new market data, no market-row parsing, no diagnostics/backtests, no OOS, no Lockbox, no Forward, no tuning, no CFD adapter execution, no old QuantLab active-pipeline use, no deployment, no trading, no promotion, no Git operations, and no remote operations.
