# Carver S27 Book Source-Faithfulness Fix Result

Date: 2026-06-04

Lane: SOURCE_NATIVE_FUTURES

Status:

```text
PASS_CODE_BOUNDARY_FIX_ONLY_NO_BACKTEST_NO_DATA_ACCESS
```

Scope:

- Strategy 27 fast mean reversion machinery now requires the S26 equilibrium input as a prevalidated daily back-adjusted EWMA5 runtime.
- S27 trend overlay runtimes now fail closed unless labeled as daily EWMAC16/64 runtimes.
- S27 volatility attenuation runtimes now fail closed unless labeled as daily S13 ten-year V/Q/M attenuation runtimes.
- The old hourly-close EWMA5 equilibrium path is no longer accepted by the S26/S27 forecast handoff.
- The old vague `LOCKED_EWMAC16_TREND_OVERLAY_RUNTIME` and `LOCKED_S13_STYLE_V_Q_M_ATTENUATION_RUNTIME` labels are rejected.

Implementation Files:

- `src/carver/spine/s26_s27.py`
- `src/carver/spine/__init__.py`
- `tests/test_s26_s27_fast_mean_reversion_synthetic.py`
- `tools/databento/carver_s26_zn_extended_sigma_and_forecast_series.py`
- `tools/databento/carver_s27_candidate_comparison_2022_2023.py`
- `tools/databento/carver_s27_zn_2022_2023_retargeted_dev_recon_backtest.py`
- `tools/databento/carver_s27_zn_2024_validation_backtest.py`
- `tools/audit/carver_s27_zn_mechanical_verifier.py`

Fail-Closed Legacy Executables:

The old S27 candidate comparison, retargeted dev/recon backtest, 2024 validation backtest, and mechanical verifier are now stopped at `main()` because they recompute S26 EWMA5 from hourly rows. They must be converted to locked daily EWMA5 equilibrium runtime inputs before reuse.

Verification:

```text
python -m py_compile src/carver/spine/__init__.py src/carver/spine/s26_s27.py tests/test_s26_s27_fast_mean_reversion_synthetic.py tools/databento/carver_s26_zn_extended_sigma_and_forecast_series.py tools/databento/carver_s27_candidate_comparison_2022_2023.py tools/databento/carver_s27_zn_2022_2023_retargeted_dev_recon_backtest.py tools/databento/carver_s27_zn_2024_validation_backtest.py tools/audit/carver_s27_zn_mechanical_verifier.py
python -m unittest tests.test_s26_s27_fast_mean_reversion_synthetic
```

Focused unit-test result:

```text
Ran 42 tests in 0.052s
OK
```

Boundary:

No provider/API calls, no data download, no market-row parsing, no diagnostics, no backtest, no validation rerun, no OOS/Lockbox/Forward access, no position output, no Git staging, no commit, no push, and no alpha/promotional claim were performed.

Remaining Gate:

This fixes the code-level source-faithfulness boundary. A future authorized S27 validation/backtest gate still needs separately prevalidated daily equilibrium, daily EWMAC16/64 trend, and daily ten-year V/Q/M volatility runtime ledgers before any result can be interpreted as book-faithful.
