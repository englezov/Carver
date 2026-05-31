# Hostile Audit Checklist And Verification Evidence

Status:

```text
OPUS_4_7_HOSTILE_AUDIT_CHECKLIST_FOR_S26_S27_MACHINE_AND_S27_ZN_BACKTEST
```

## Verification Already Run Locally

The following local verification was run after the corrected full-window artifacts were generated:

```text
python -m py_compile tools\databento\carver_s27_zn_m1_ladder_dev_recon_backtest.py
python -m py_compile tools\databento\carver_s27_zn_2022_2023_retargeted_dev_recon_backtest.py
python -m py_compile tools\databento\carver_s27_zn_local_extended_daily_runtime_2022_2023.py
python -m unittest tests.test_s26_s27_fast_mean_reversion_synthetic -v
artifact invariant and SHA verification script
secret scan: rg -n "db-[A-Za-z0-9]{20,}" docs\process docs\researchops tools src tests
local hostile audit subagent
```

Test result:

```text
Ran 42 tests
OK
```

Artifact invariant verification:

```text
PASS full-window final artifact verification
effective_backtest_start: 2022-01-04
effective_backtest_end: 2023-12-29
forecast_rows: 11771
backtest_rows: 11770
source_daily_runtime_lag_max_days: 1
gross_pnl_usd: 10343.75
estimated_etf_fees_usd: 5001.12
net_after_etf_fees_usd: 5342.630000000004
```

Secret scan result:

```text
No Databento API key pattern matches were found in docs\process docs\researchops tools src tests.
```

Local hostile audit verdict:

```text
PASS for declared local Dev/Reconciliation scope.
No blocking findings.
```

Local hostile audit medium warning:

```text
The local extended daily runtime stitch is explicitly Dev/Reconciliation-only, not production continuous-contract authority. It uses pre-2015 R2 support history with a constant bridge offset into the 2015+ V/Q/M runtime source. Provenance is clear enough for this scope, but it must not be promoted without a separate production lineage gate.
```

Local hostile audit low warning:

```text
Ladder costs include ETF public per-side commission only. Roll-transition close/open fee sides are accounted for, but spread/slippage/fill quality remain unresolved and cannot be inferred from this artifact.
```

## Hostile Audit Checklist

### Source Faithfulness

1. Verify S26/S27 source atoms against `00_Carver.pdf`.
2. Verify that the machine uses hourly bars for S26/S27 real-data forecast/backtest work.
3. Verify S27 inherits S26 scalar/cap and uses the trend/non-opposition and V/Q/M dependencies.
4. Verify the audited instrument is source-native ZN / US 10-year Note futures, not a CFD or unrelated substitute.
5. Verify no daily-only Appendix C result is being used as if it were sufficient for S26/S27.

### Runtime Alignment

1. Verify S27 forecast rows consume strict prior daily runtime only.
2. Verify accepted daily runtime lag is greater than 0 and no more than 10 calendar days.
3. Verify observed max lag is 1 day.
4. Verify no row uses `source_vqm_completed_trading_date=2020-12-21` in the accepted corrected ladder result.
5. Verify the stale R2-fed result remains fail-closed and superseded.

### Local Extended Daily Runtime

1. Verify `PASS_LOCAL_EXTENDED_DAILY_RUNTIME_DEV_RECON_ONLY`.
2. Verify pre-2015 R2 support history is deduped and bridge-offset, not silently merged.
3. Verify 2015+ rows come from the existing V/Q/M local continuous daily risk history.
4. Verify bridge day `2015-01-01` and offset `-0.28125`.
5. Verify this artifact is not described as production continuous-contract authority.

### Backtest Mechanics

1. Verify the M1-style ladder uses 100000 USD capital, target risk 20%, instrument weight 1, IDM 1, FX 1, ZN multiplier 1000.
2. Verify `forecast_to_position_divisor=10.0`.
3. Verify integer futures sizing only.
4. Verify position rows, ladder rows, and forecast rows all reconcile at 11771.
5. Verify backtest rows reconcile at 11770.
6. Verify first four source rows are blocked dependency rows, not filled.
7. Verify roll-transition fee sides are counted.
8. Verify total fee sides equal position-change sides plus roll-transition fee sides.
9. Verify costs are ETF per-side commission only; spread, slippage, limit-fill quality, margin, and prop-firm rules are unresolved.

### Governance

1. Verify no provider API access occurred in the corrected local rerun.
2. Verify no new data download occurred in the corrected local rerun.
3. Verify no OOS, Lockbox, Forward, deployment, trading, promotion, Git operation, CFD adapter, or old QuantLab active-pipeline use is authorized or observed.
4. Verify all status/provenance artifacts preserve Development/Reconciliation and not-alpha labels.

## Known Limitations To Preserve

These are not audit failures if clearly preserved:

```text
single instrument only
not a complete book portfolio
M1-style ladder reconstruction, not production allocation
local extended daily runtime is Dev/Reconciliation support history only
costs are ETF public per-side commission only
spread/slippage/fill quality unresolved
no OOS/Lockbox/Forward
no promotion or alpha claim
```

## Requested Opus Verdict Format

The requested audit should return:

```text
CRITICAL findings
HIGH findings
MEDIUM findings
LOW findings
INFORMATIONAL notes
BLOCKING_FINDINGS: YES/NO
AUDIT_DISPOSITION: <single token>
REQUIRED_FIXES_BEFORE_NEXT_GATE: <bullets>
```

