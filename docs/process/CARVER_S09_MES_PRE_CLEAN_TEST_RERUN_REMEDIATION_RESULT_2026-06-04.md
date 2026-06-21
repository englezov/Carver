# S09 MES Pre Clean TEST Rerun Remediation Result

Date: 2026-06-04

Status:

```text
S09_MES_PRE_CLEAN_TEST_RERUN_REMEDIATION_READY_FOR_OPERATOR_CONSIDERATION
```

## Scope

This record documents remediation of the remaining Opus/Hume concerns after
the window state-warmup/scoring-mask audit.

No provider API access, new market-data request, data download, backtest,
diagnostic, TEST rerun, VALIDATION, Lockbox, Forward, Git staging, commit,
push, PR, deployment, trading, or promotion was performed.

## Remediated Items

Cold degraded OHLCV policy:

- replaced the post-fail date-specific degraded-day rescue disposition with
  `COLD_SHAPE_BASED_POLICY_LOCKED_BEFORE_STAGE_ACCESS`;
- removed dependency on the old row overlay CSV path;
- removed date-specific admission logic from degraded provider-condition rows;
- degraded rows are admitted only when provider condition is `DEGRADED` and
  OHLCV shape is finite and internally consistent;
- unresolved provider conditions remain quarantined.

Warmup/scoring seam evidence:

- added a real S09 forecast-engine test at the first TEST scoring date using
  the previous-window state-history window;
- added a synthetic MES lineage roll test that crosses the
  `2020-04-05` / `2020-04-06` warmup/scoring seam and verifies additive
  adjustment continuity.

Scored-count clarity:

- added `completed_dates_field_scope` to future status payloads;
- added `scored_completed_dates`;
- added `total_state_plus_scoring_completed_dates`;
- updated rendered provenance, result, and local-audit text to describe scored
  completed dates separately from state-history completed dates.

Discrete trade-count concern:

- preserved the whole-contract-equivalent trade-count rule as explicit
  discrete-trade evidence, not fractional-churn evidence.

Lineage/readiness contract:

- preserved default S09 MES lineage as fail-closed unless a complete explicit
  readiness status contract is supplied;
- added a complete locked readiness status contract for the TEST runner path;
- made `evaluate_s09_mes_lineage_strategy_readiness` report the result's actual
  readiness contract instead of hard-coded fail-closed values;
- kept `_assert_lineage_readiness_locked` fail-closed on any `FAIL_CLOSED` or
  `PROVISIONAL` status.

Source-native daily completed-date policy:

- preserved daily Sunday Globex rows as source-native completed trading dates
  rather than silently rewriting all Sunday daily rows to Monday;
- carried an explicit `completed_trading_date_policy` label from sanitizer to
  lineage rows;
- changed the cadence guard from reject-only Sunday blocking to fail-closed
  admission unless Sunday rows carry
  `SUNDAY_GLOBEX_PROVIDER_DATE_ADMITTED_AS_SOURCE_COMPLETED_TRADING_DATE`;
- retained duplicate completed-date protection after policy application.

Superseded diagnostic receipt handling:

- preserved the original TEST backtest receipt as historical diagnostic-only
  evidence;
- assigned the future clean rerun a distinct `RUN_ID`;
- read the old authorized TEST download artifacts through
  `ORIGINAL_DIAGNOSTIC_TEST_RUN_ID`;
- kept the one-run guard active for the clean-rerun receipt path.

## Verification

Fresh focused verification:

```text
python -m py_compile tools\databento\carver_s09_mes_test_window_backtest.py src\carver\spine\s09_mes_lineage.py
python -m unittest tests.test_s09_mes_test_window_backtest_guard tests.test_s09_mes_lineage_synthetic
```

Observed result:

```text
Ran 110 tests
OK
```

Resource warning:

```text
ResourceWarning: unclosed event loop <ProactorEventLoop ...>
```

The warning was emitted after test completion and did not change the test exit
status.

## Current Disposition

The remediation is locally implemented, focused verification passes, and local
hostile subagent audit passed. The machinery is ready for operator
consideration of a separately authorized clean TEST rerun.

This record itself does not authorize the clean TEST rerun.

## Boundary

This remediation result authorizes no provider API access, no new market-data
request, no data download, no market-row parsing beyond unit-test fixtures, no
diagnostics, no backtests, no forecasts as evidence, no positions as evidence,
no costs as evidence, no TEST rerun, no VALIDATION, no Lockbox, no Forward, no
CFD adapter execution, no old QuantLab active pipeline use, no tuning, no
deployment, no trading, no promotion, no Git staging, no commit, no push, no
PR, and no remote operation.
