# Carver S27 Pre-Backtest Readiness Local Hostile Audit

Date: 2026-06-04

Mode: local hostile audit over the S27 pre-backtest readiness gate. No provider/API access, no data download, no market-row parsing, no diagnostics, no backtest, no positions, no PnL, no Git operation.

## Audited Artifacts

```text
docs/process/CARVER_S27_PRE_BACKTEST_READINESS_GATE_2026-06-04.md
docs/process/CARVER_S27_BOOK_SOURCE_FAITHFULNESS_FIX_RESULT_2026-06-04.md
docs/process/CARVER_S27_CORRECTED_RUNTIME_LEDGERS_EXECUTION_RESULT_2026-06-04.md
docs/process/CARVER_S27_CORRECTED_RUNTIME_LEDGERS_LOCAL_HOSTILE_AUDIT_RESULT_2026-06-04.md
src/carver/spine/s26_s27.py
src/carver/spine/__init__.py
tools/databento/carver_s26_zn_daily_ewma5_equilibrium_runtime.py
tools/databento/carver_s27_zn_ewmac16_trend_runtime.py
tools/databento/carver_s27_zn_vqm_ten_year_vol_runtime.py
tools/databento/carver_s27_zn_2022_2023_retargeted_dev_recon_backtest.py
tools/databento/carver_s27_zn_2022_2023_corrected_runtime_ledgers.py
tests/test_s26_s27_fast_mean_reversion_synthetic.py
tests/test_s27_corrected_backtest_runner_preflight.py
tests/test_s27_corrected_runtime_ledger_prep.py
```

## Critical

None.

The readiness gate does not authorize a backtest. It requires the corrected daily runtime dependencies and keeps stale S27 backtest executables fail-closed, except for the converted 2022-2023 retargeted runner which still requires explicit operator authorization before execution.

The corrected runtime ledgers have now been executed under separate runtime-ledger authorization and audited by subagent. The audit found no blocking findings for the runtime-ledger handoff.

## High

None.

The previously invalid hourly S26 EWMA5 path is not restored. The S27 readiness gate now requires:

```text
PREVALIDATED_S26_DAILY_BACK_ADJUSTED_EWMA5_EQUILIBRIUM_RUNTIME_VALUE
LOCKED_DAILY_EWMAC16_64_TREND_OVERLAY_RUNTIME
LOCKED_DAILY_S13_TEN_YEAR_V_Q_M_ATTENUATION_RUNTIME
FAIL_CLOSED_STALE_S27_EXECUTABLES_PENDING_DAILY_RUNTIME_CONVERSION
```

## Medium

The previous blocking operational item has been closed:

```text
CORRECTED_RUNTIME_LEDGERS_EXECUTED_AND_SUBAGENT_AUDITED
```

The only remaining gate before execution is explicit corrected S27 backtest authorization.

The corrected runtime-ledger prep script now exits before input checks, folder creation, parsing, or writing unless:

```text
CARVER_OPERATOR_AUTHORIZES_S27_RUNTIME_LEDGERS=AUTHORIZED_CORRECTED_S27_ZN_2022_2023_RUNTIME_LEDGERS
```

The converted 2022-2023 runner now exits before input checks, folder creation, parsing, or backtest execution unless:

```text
CARVER_OPERATOR_AUTHORIZES_S27_BACKTEST=AUTHORIZED_CORRECTED_S27_ZN_2022_2023_BACKTEST
```

## Low

The immediate comparison should reuse the old scored windows first, but only after corrected runtime ledgers exist. New S27-specific windows should be frozen later as a separate window-design gate.

## Verification

```text
python -m py_compile src/carver/spine/__init__.py src/carver/spine/s26_s27.py tests/test_s26_s27_fast_mean_reversion_synthetic.py tests/test_s27_corrected_backtest_runner_preflight.py tests/test_s27_corrected_runtime_ledger_prep.py tools/databento/carver_s26_zn_daily_ewma5_equilibrium_runtime.py tools/databento/carver_s27_zn_ewmac16_trend_runtime.py tools/databento/carver_s27_zn_vqm_ten_year_vol_runtime.py tools/databento/carver_s27_candidate_comparison_2022_2023.py tools/databento/carver_s27_zn_local_extended_daily_runtime_2022_2023.py tools/databento/carver_s27_zn_2022_2023_retargeted_dev_recon_backtest.py tools/databento/carver_s27_zn_2022_2023_corrected_runtime_ledgers.py
python -m unittest tests.test_s26_s27_fast_mean_reversion_synthetic
python -m unittest tests.test_s27_corrected_backtest_runner_preflight
python -m unittest tests.test_s27_corrected_runtime_ledger_prep
python -m unittest tests.test_s26_s27_fast_mean_reversion_synthetic tests.test_s27_corrected_backtest_runner_preflight tests.test_s27_corrected_runtime_ledger_prep
```

Focused test result:

```text
Ran 42 S26/S27 spine tests
OK

Ran 3 corrected-runner preflight tests
OK

Ran 3 corrected runtime-ledger prep tests
OK

Ran 48 focused S26/S27 readiness tests
OK
```

## Disposition

```text
AUDIT_DISPOSITION: PASS_PRE_BACKTEST_READINESS_GATE_READY_FOR_SEPARATELY_AUTHORIZED_CORRECTED_S27_BACKTEST
```

## Non-Authorization

This audit authorizes no provider/API call, no data download, no market-row parsing, no diagnostics, no backtest, no returns, no PnL, no positions, no OOS, no Lockbox, no Forward, no deployment, no trading, no promotion, no Git staging, no commit, no push, and no PR.
