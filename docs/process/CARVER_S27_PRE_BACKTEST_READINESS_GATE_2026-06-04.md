# Carver S27 Pre-Backtest Readiness Gate

Date: 2026-06-04

Lane: SOURCE_NATIVE_FUTURES

Status:

```text
PROCESS_ONLY_S27_PRE_BACKTEST_READINESS_GATE_NOT_BACKTEST_AUTHORIZATION
```

## Purpose

Define the stage required before the operator can authorize a corrected S27 backtest after the 2026-06-04 source-faithfulness fix.

This gate does not run a backtest.

## Current Decision

Use the same prior scored windows first for comparison, but only after the corrected machinery has all required runtime ledgers. New S27-specific windows may be designed later as a separate gate.

## Required Runtime Inputs

Before any corrected S27 backtest can run, the execution gate must have one hash-bound row per forecast timestamp for:

- S26 daily back-adjusted EWMA5 equilibrium runtime;
- S26 hourly current-price forecast row;
- S26 sigma percent runtime;
- S27 daily EWMAC16/64 trend runtime;
- S27 daily ten-year V/Q/M volatility attenuation runtime;
- S27 scalar/cap/no-FDM/no-buffering rules;
- M1 sizing/execution/cost semantics if positions or PnL are emitted.

## Required Runtime Labels

```text
S26 daily equilibrium runtime: PREVALIDATED_S26_DAILY_BACK_ADJUSTED_EWMA5_EQUILIBRIUM_RUNTIME_VALUE
S26 daily equilibrium method: LOCKED_DAILY_BACK_ADJUSTED_EWMA5_EQUILIBRIUM_RUNTIME
S27 trend runtime: PREVALIDATED_S27_EWMAC16_TREND_RUNTIME_VALUE
S27 trend method: LOCKED_DAILY_EWMAC16_64_TREND_OVERLAY_RUNTIME
S27 volatility runtime: PREVALIDATED_S27_V_Q_M_VOL_ATTENUATION_RUNTIME_VALUE
S27 volatility method: LOCKED_DAILY_S13_TEN_YEAR_V_Q_M_ATTENUATION_RUNTIME
stale executable status: FAIL_CLOSED_STALE_S27_EXECUTABLES_PENDING_DAILY_RUNTIME_CONVERSION
```

## History Budget

The binding S27 state-history budget is the V/Q/M dependency:

```text
10 years of completed daily source-native futures history
+ strict-prior state warmup
+ scored window
```

Daily EWMA5 and daily EWMAC16/64 are shorter dependencies, but they do not reduce the ten-year V/Q/M requirement.

## Window Policy

For the immediate corrected comparison:

```text
same scored windows as the prior S27 run
prior-window bars allowed for state warmup only
no future-stage data
no scored row outside the current stage window
```

For any later redesigned S27 program:

```text
freeze new DEV/TEST/VALIDATION windows before execution
base the window budget on trade count, ten-year runtime availability, and no-lookahead state masks
```

## Stale Executables

The following old executables remain fail-closed until converted to consume the locked daily runtime ledgers:

- `tools/databento/carver_s27_candidate_comparison_2022_2023.py`
- `tools/databento/carver_s27_zn_2024_validation_backtest.py`
- `tools/audit/carver_s27_zn_mechanical_verifier.py`

The 2022-2023 retargeted runner has been converted:

```text
tools/databento/carver_s27_zn_2022_2023_retargeted_dev_recon_backtest.py
```

It now requires corrected runtime ledgers and explicit operator authorization through:

```text
CARVER_OPERATOR_AUTHORIZES_S27_BACKTEST=AUTHORIZED_CORRECTED_S27_ZN_2022_2023_BACKTEST
```

Without that value it exits before input checks, folder creation, parsing, or backtest execution.

## Next Authorized Work Needed Before Backtest

1. Ask the operator for explicit corrected S27 backtest authorization.

## Runtime Ledger Execution

The operator authorized corrected runtime-ledger creation only, using:

```text
CARVER_OPERATOR_AUTHORIZES_S27_RUNTIME_LEDGERS=AUTHORIZED_CORRECTED_S27_ZN_2022_2023_RUNTIME_LEDGERS
```

The authorized runtime-ledger prep was executed:

```text
tools/databento/carver_s27_zn_2022_2023_corrected_runtime_ledgers.py
```

Result document:

```text
docs/process/CARVER_S27_CORRECTED_RUNTIME_LEDGERS_EXECUTION_RESULT_2026-06-04.md
```

The four corrected runtime CSVs now exist under:

```text
docs/researchops/s26_s27_backtest_readiness/ZN_S27_SINGLE_INSTRUMENT/2022-01-01_2023-12-31/corrected_runtime_ledgers
```

Each runtime CSV has `11775` rows and corrected runtime/method labels. The generated status records no provider/API access, no new data download, no diagnostics, no backtest, no positions, no OOS, no Lockbox, no Forward, and no Git operations.

## Runtime Ledger Hostile Audit

Subagent local hostile audit was completed:

```text
docs/process/CARVER_S27_CORRECTED_RUNTIME_LEDGERS_LOCAL_HOSTILE_AUDIT_RESULT_2026-06-04.md
```

Disposition:

```text
BLOCKING_FINDINGS: NONE
AUDIT_DISPOSITION: PASS_RUNTIME_LEDGER_HANDOFF_READY_FOR_SEPARATELY_AUTHORIZED_CORRECTED_S27_BACKTEST
```

## Code Prepared In This Gate

- S27 readiness gate now requires daily EWMA5 equilibrium, daily EWMAC16/64 trend, daily ten-year V/Q/M, and stale executable fail-closed status.
- `tools/databento/carver_s26_zn_daily_ewma5_equilibrium_runtime.py` now exists as the runtime-only producer for the missing daily equilibrium dependency.
- `tools/databento/carver_s27_zn_ewmac16_trend_runtime.py` now emits `LOCKED_DAILY_EWMAC16_64_TREND_OVERLAY_RUNTIME`.
- `tools/databento/carver_s27_zn_vqm_ten_year_vol_runtime.py` now emits `LOCKED_DAILY_S13_TEN_YEAR_V_Q_M_ATTENUATION_RUNTIME`.
- `tools/databento/carver_s27_zn_2022_2023_retargeted_dev_recon_backtest.py` now consumes corrected runtime ledgers by `as_of` and requires explicit operator authorization before execution.
- `tools/databento/carver_s27_zn_2022_2023_corrected_runtime_ledgers.py` now exists as the local runtime-ledger prep script for the 2022-2023 target window. It requires a separate runtime-ledger authorization value before input checks, folder creation, parsing, or writing.
- `tests/test_s27_corrected_runtime_ledger_prep.py` locks the runtime-prep auth guard, four-ledger shape, corrected method labels, and strict-prior daily/V/Q/M dependency behavior.
- `docs/process/CARVER_S27_CORRECTED_RUNTIME_LEDGERS_EXECUTION_RESULT_2026-06-04.md` records the authorized corrected runtime-ledger execution and observed output hashes.
- `docs/process/CARVER_S27_CORRECTED_RUNTIME_LEDGERS_LOCAL_HOSTILE_AUDIT_RESULT_2026-06-04.md` records the subagent local hostile audit result over the concrete runtime ledgers and converted runner handoff.

## Non-Authorization

This gate authorizes no provider/API call, no data download, no market-row parsing, no diagnostics, no backtest, no returns, no PnL, no positions, no OOS, no Lockbox, no Forward, no deployment, no trading, no promotion, no Git staging, no commit, no push, and no PR.
