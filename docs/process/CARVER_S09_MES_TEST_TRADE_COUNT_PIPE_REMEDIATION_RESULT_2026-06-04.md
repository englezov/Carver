# S09 MES TEST Trade Count Pipe Remediation Result

Date: 2026-06-04

Status:

```text
S09_MES_TEST_TRADE_COUNT_PIPE_REMEDIATED_PENDING_HOSTILE_AUDIT
```

## Scope

This record documents remediation of the TEST trade-count pipe after the clean
rerun failed closed at:

```text
FAIL_CLOSED TEST trade count 1 < 100
```

No clean TEST rerun, provider API access, new market-data request, data
download, VALIDATION, Lockbox, Forward, Git staging, commit, push, PR,
deployment, trading, or promotion was performed during this remediation.

## Root Cause

The pipe overloaded `trade_count` with two different meanings:

- statistical sample count for a fractional contract-equivalent research
  backtest;
- whole-contract-equivalent executability crossing count.

The implementation gated the TEST sample on whole-contract-equivalent position
changes of at least `1.0`, while the backtest execution model is explicitly:

```text
NEXT_COMPLETED_BAR_CLOSE_TO_CLOSE_FRACTIONAL_CONTRACT_EQUIVALENT_NO_BUFFER_NO_ROUNDING
```

That made the sample gate measure executability scale rather than the
fractional research trade-event sample.

## Remediation

The pipe now reports separate metrics:

- `fractional_trade_event_count`;
- `whole_contract_equivalent_change_count`;
- `fractional_turnover_contract_equivalent`;
- `max_position_change_contract_equivalent`;
- `trade_count_sample_definition`;
- `whole_contract_count_definition`.

The minimum TEST sample gate is attached to:

```text
fractional_trade_event_count >= 100
```

The whole-contract count is retained as:

```text
EXECUTABILITY_DIAGNOSTIC_NOT_STATISTICAL_SAMPLE_GATE
```

This remediation does not rerun TEST and does not declare a TEST result.

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

Known warning:

```text
ResourceWarning: unclosed event loop <ProactorEventLoop ...>
```

The warning was emitted after test completion and did not change the test exit
status.

## Boundary

This remediation does not authorize another TEST rerun. It authorizes no
provider access, no data download, no later-window access, no threshold tuning
from TEST performance, no VALIDATION, no Lockbox, no Forward, no deployment, no
trading, no promotion, and no Git operation.
