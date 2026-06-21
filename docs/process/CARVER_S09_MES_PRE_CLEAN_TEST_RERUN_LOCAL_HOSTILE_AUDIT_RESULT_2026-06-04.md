# S09 MES Pre Clean TEST Rerun Local Hostile Audit Result

Date: 2026-06-04

Status:

```text
LOCAL_HOSTILE_AUDIT_PASS_S09_MES_PRE_CLEAN_TEST_RERUN_READY_FOR_OPERATOR_CONSIDERATION
```

## Scope

This local hostile audit reviewed whether the S09 MES pre-clean-TEST-rerun
remediation resolved the Opus/Hume blockers and whether the machinery is ready
for operator consideration of a separately authorized clean TEST rerun.

No provider API access, new market-data request, data download, backtest,
diagnostic, TEST rerun, VALIDATION, Lockbox, Forward, Git staging, commit,
push, PR, deployment, trading, or promotion was performed.

## Verdict

PASS for operator consideration.

The old diagnostic TEST receipt is preserved as historical diagnostic-only
evidence and no longer blocks the future clean-rerun preflight. The future
clean-rerun path uses a distinct `RUN_ID`, while the existing authorized input
artifacts are read through `ORIGINAL_DIAGNOSTIC_TEST_RUN_ID`.

Observed by hostile subagent:

- old diagnostic receipt exists: `True`;
- clean-rerun receipt exists: `False`;
- clean-rerun artifacts under the output root: `0`;
- live preflight returned `AUTHORIZED_READY_FOR_EXACTLY_ONE_TEST_BACKTEST`;
- existing authorized input artifacts keyed to the old diagnostic id both
  exist.

## Controls Checked

- default S09 MES lineage remains fail-closed unless a complete explicit
  readiness contract is supplied;
- TEST runner supplies a complete locked readiness contract to
  `build_s09_mes_lineage`;
- `_assert_lineage_readiness_locked` still blocks any `FAIL_CLOSED` or
  `PROVISIONAL` readiness status;
- Sunday Globex daily rows are preserved as source-native completed trading
  dates only when the consumed lineage row carries
  `SUNDAY_GLOBEX_PROVIDER_DATE_ADMITTED_AS_SOURCE_COMPLETED_TRADING_DATE`;
- unlabeled Sunday lineage rows fail closed;
- cold degraded OHLCV admission is shape-based and non-date-specific;
- state-history warmup remains separate from scored TEST rows.

## Verification

Hostile subagent verification:

```text
python -B -m unittest tests.test_s09_mes_test_window_backtest_guard tests.test_s09_mes_lineage_synthetic
```

Observed result:

```text
Ran 110 tests
OK
```

Known warning:

```text
ResourceWarning: unclosed event loop <ProactorEventLoop ...>
```

The warning was emitted after test completion and did not change the test exit
status.

## Boundary

This audit result does not authorize the clean TEST rerun. It authorizes no
provider API access, no new market-data request, no data download, no market-row
parsing beyond unit-test fixtures, no diagnostics, no backtests, no forecasts
as evidence, no positions as evidence, no costs as evidence, no TEST rerun, no
VALIDATION, no Lockbox, no Forward, no CFD adapter execution, no old QuantLab
active pipeline use, no tuning, no deployment, no trading, no promotion, no Git
staging, no commit, no push, no PR, and no remote operation.
