# S27_V2 Positive-Action Actual PnL Ledger Local Audit Result

Date: 2026-06-11

Status:

```text
LOCAL_HOSTILE_AUDIT_PASS_POSITIVE_ACTION_ACTUAL_PNL_LEDGER_NOT_RESULT_NOT_BACKTEST_NOT_SOURCE_FAITHFUL_EVIDENCE
```

## Scope

This local hostile audit covered only the actual PnL ledger implementation for the audited `ZNM6` positive-action short fill and declared next-completed-hourly valuation mark row.

Audited implementation:

```text
src/carver/spine/s27_v2_replay/positive_action_actual_pnl_executable.py
tests/test_s27_v2_positive_action_actual_pnl_executable.py
docs/process/CARVER_S27_ZN_V2_POSITIVE_ACTION_ACTUAL_PNL_LEDGER_IMPLEMENTATION_2026-06-11.md
```

## Non-Authorization

This audit authorizes no provider/API access, no market-data downloads, no new data acquisition, no OOS, no Lockbox, no Forward, no backtests, no result-scored runs, no result emission, no result interpretation, no PnL evaluation beyond mechanical row construction, no tuning, no adapter work, no deployment, no trading, no promotion, no Git actions, and no source-faithful evidence claim.

## Audit Results

### Arithmetic And Evidence-Binding Audit

Subagent:

```text
019eadd5-fe07-7fe2-a68b-72f5bcb37084
```

Verdict:

```text
PASS
```

Findings:

```text
P0: none
P1: none
P2: none
P3: none
```

The audit confirmed:

- active actual-cost and fill bundle comparison is enforced before PnL acceptance;
- actual-cost/fill row hashes are bound in the PnL row;
- valuation manifest, valuation CSV, and valuation local-audit byte hashes are pinned;
- valuation source-row byte and canonical hashes are bound;
- static ZN point value/currency and non-book-explicit valuation convention are bound;
- short mark-to-market arithmetic is mechanically correct for the audited row.

Current mechanical build output:

```text
gross_pnl_amount = 0.0
total_cost_amount = 2.3
net_pnl_amount = -2.3
pnl_currency = USD
valuation_convention_hash = 840b4f7c4ce55d7adf62a69b7404207be5a768e01224492eec04b1156f58cc95
```

### Boundary Audit

Subagent:

```text
019eadd6-606a-72e1-883e-82449915bcb0
```

Verdict:

```text
PASS
```

Findings:

```text
P0: none
P1: none
P2: none
P3: none
```

The audit confirmed:

- the surface emits only actual PnL ledger mechanics and metadata;
- result rows, backtests, result interpretation, PnL evaluation beyond row construction, promotion, trading, and source-faithful evidence claims remain blocked;
- package root does not export the builder;
- tests cover package-root export leakage and downstream flag forgeries;
- process records preserve local Development/Reconciliation mechanics only.

## Focused Tests

Focused tests passed:

```text
python -m pytest tests\test_s27_v2_positive_action_actual_pnl_executable.py -q --tb=short
54 passed in 284.51s (0:04:44)
```

Adjacent fill/actual-cost regression tests passed:

```text
python -m pytest tests\test_s27_v2_positive_action_fill_executable.py tests\test_s27_v2_positive_action_actual_cost_executable.py -q --tb=short
75 passed in 108.55s (0:01:48)
```

Package-root/export and mechanical build spot checks passed:

```text
python -m pytest tests\test_s27_v2_positive_action_actual_pnl_executable.py::test_positive_action_actual_pnl_is_not_package_root_exported tests\test_s27_v2_positive_action_actual_pnl_executable.py::test_positive_action_actual_pnl_builds_single_mechanical_row -q --tb=short
2 passed in 13.83s
```

## Decision

The actual PnL ledger implementation is locally audited as:

```text
PASS_LOCAL_POSITIVE_ACTION_ACTUAL_PNL_LEDGER_MECHANICAL_ROW_NOT_RESULT_NOT_BACKTEST_NOT_SOURCE_FAITHFUL_EVIDENCE
```

Result rows, backtests, result-scored runs, result interpretation, PnL evaluation beyond mechanical row construction, source-faithful evidence claims, provider/API access, market-data downloads, new data acquisition, OOS/Lockbox/Forward, Git actions, adapter/deployment/trading/promotion, and tuning remain unauthorized.
