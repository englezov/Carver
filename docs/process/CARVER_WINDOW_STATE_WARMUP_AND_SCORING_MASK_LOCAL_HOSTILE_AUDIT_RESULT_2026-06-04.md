# Carver Window State Warmup And Scoring Mask Local Hostile Audit Result

Date: 2026-06-04

Status:

```text
PASS_LOCAL_HOSTILE_AUDIT_WINDOW_STATE_WARMUP_AND_SCORING_MASK_REMEDIATION
```

## Scope

Audited artifacts:

- `docs/process/CARVER_WINDOW_STATE_WARMUP_AND_SCORING_MASK_DOCTRINE_2026-06-04.md`
- `tools/databento/carver_s09_mes_test_window_backtest.py`
- `tests/test_s09_mes_test_window_backtest_guard.py`

The audit was read-only. It did not run the backtest script, access or download
provider data, rerun TEST, access VALIDATION, access Lockbox, access Forward,
stage Git changes, commit, push, open a PR, deploy, trade, or promote.

## Findings

Blocking findings:

```text
NONE
```

Confirmed controls:

- The doctrine locks `previous_window_for_state_warmup_only -> current_window_for_scoring_only`.
- TEST may use the machinery-development slice only as non-scored state history.
- VALIDATION may use TEST only as non-scored state history.
- LOCKBOX may use VALIDATION only as non-scored state history.
- The S09 MES TEST runner exposes state-history and scoring masks.
- Sanitized pre-TEST rows are retained for state warmup but labeled non-scored.
- Forecast rows are emitted only inside the TEST scoring window.
- Backtest rows require both signal date and next PnL date inside the TEST scoring window.
- State-history dates cannot contribute to scored trade count, costs, PnL, summaries, or performance.
- The old S09 MES TEST result remains diagnostic-only.

## Verification

Focused verification:

```text
python -m py_compile tools\databento\carver_s09_mes_test_window_backtest.py
python -m unittest tests.test_s09_mes_test_window_backtest_guard tests.test_s09_mes_lineage_synthetic
```

Observed result:

```text
Ran 101 tests
OK
```

## Boundary

This audit result authorizes no provider API access, no new market-data
request, no data download, no market-row parsing beyond unit-test fixtures, no
diagnostics, no backtests, no forecasts as evidence, no positions as evidence,
no costs as evidence, no TEST rerun, no VALIDATION, no Lockbox, no Forward, no
CFD adapter execution, no old QuantLab active pipeline use, no tuning, no
deployment, no trading, no promotion, no Git staging, no commit, no push, no
PR, and no remote operation.
