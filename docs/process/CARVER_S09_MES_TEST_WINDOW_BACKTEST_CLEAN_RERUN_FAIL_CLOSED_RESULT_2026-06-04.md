# S09 MES TEST Window Backtest Clean Rerun Fail-Closed Result

Date: 2026-06-04

Status:

```text
FAIL_CLOSED_S09_MES_TEST_CLEAN_RERUN_TRADE_COUNT_BELOW_MINIMUM_NO_RESULT_RECEIPT
```

## Scope

The operator authorized the S09 MES TEST-area clean backtest rerun using the
existing authorized TEST download artifacts.

The runner used:

```text
python tools\databento\carver_s09_mes_test_window_backtest.py --execute-authorized-test-backtest --use-existing-authorized-test-download
```

No provider API access, new market-data request, data download, VALIDATION,
Lockbox, Forward, Git staging, commit, push, PR, deployment, trading, or
promotion was performed.

## Result

The first attempt failed closed before writing a clean-rerun result or receipt
because the runner was reading only TEST rows and not the authorized
machinery-development slice required for state-history warmup.

Remediation:

- spliced the authorized machinery-development sanitized rows into lineage
  construction as warmup-only state history;
- merged machinery-development and TEST definition ledgers;
- kept forecast and PnL scoring confined to the TEST window.

Focused verification after remediation:

```text
Ran 110 tests
OK
```

The second attempt reached the trade-count gate and failed closed:

```text
FAIL_CLOSED TEST trade count 1 < 100
```

No clean-rerun execution receipt was written.

## Interpretation

The current locked trade-count gate uses whole-contract-equivalent position
changes as the minimum sample-count test. Under that pre-rerun locked
definition, S09 MES TEST does not meet the minimum `100` trade-count threshold.

Changing the trade-count gate to fractional churn, nonzero position-change
events, or another sample definition after this fail-closed observation would
be a governance change and requires a separate operator decision before any
further rerun.

## Supersession Note

This interpretation records the pipe state at the time of the fail-closed
attempt. It is superseded for future rerun consideration by:

```text
docs/process/CARVER_S09_MES_TEST_TRADE_COUNT_PIPE_REMEDIATION_RESULT_2026-06-04.md
```

That later remediation separates fractional research trade-event sample count
from whole-contract-equivalent executability diagnostics. This fail-closed
record remains historical and does not itself authorize another rerun.

## Boundary

This fail-closed record is not a TEST performance result, not VALIDATION, not
Lockbox, not Forward, not deployment, not trading, and not promotion. It
authorizes no additional rerun, no threshold change, no provider access, no
data download, no later-window access, and no Git operation.
