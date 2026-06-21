# S27_V2 No-PnL Executable Metadata Implementation Record

Date: 2026-06-09

Status:

```text
LOCAL_IMPLEMENTATION_COMPLETE_LOCAL_HOSTILE_AUDIT_PASS
```

## Authorization

Operator authorized a local-only no-PnL executable metadata gate after external PASS on the no-cost executable metadata surface and the PnL planning gate.

Authorized scope:

- active no-cost bundle binding;
- `NO_ORDER` and order quantity zero verification;
- `NO_POSITION_CHANGE_NO_ORDER` verification;
- `fill_required = False`;
- `actual_fill_ledger_emitted = False`;
- `cost_required = False`;
- `actual_cost_ledger_emitted = False`;
- `pnl_required = False`;
- `pnl_rows_emitted = False`;
- actual PnL/result/backtest emission fail-closed;
- `NOT_APPLICABLE` PnL amount/currency metadata;
- rejection of forged no-cost bundles, no-PnL rows, PnL-required flags, PnL amounts/currency/provenance, and downstream result/source-faithful evidence flags.

Non-authorized scope:

- no provider/API access;
- no downloads or new data;
- no OOS/Lockbox/Forward;
- no backtests or result-scored runs;
- no actual positive fill emission;
- no actual commission/spread/cost ledger emission;
- no actual PnL ledger emission;
- no result emission;
- no result interpretation or PnL evaluation;
- no tuning;
- no adapter work, deployment, trading, promotion;
- no Git actions;
- no source-faithful evidence claim.

## Implementation

Added:

```text
src/carver/spine/s27_v2_replay/no_pnl_executable.py
tests/test_s27_v2_no_pnl_executable.py
```

The new surface follows the externally passed no-cost pattern:

- public standalone `NoPnlExecutableMetadataRow.validate()` always fails closed;
- `NoPnlExecutableBundle.validate()` is the only accepting authority path;
- bundle validation rebuilds the active no-cost bundle from the audited `ZNM6` remediation pack and exact-compares it;
- the active no-PnL row is rebuilt from the active no-cost metadata and exact-compared;
- policy and row hashes bind the no-order/no-fill/no-cost/no-PnL branch;
- actual `PnlLedgerRow`, result row, backtest row, result interpretation, and source-faithful evidence surfaces remain absent and fail-closed.

## Active Metadata Semantics

The active no-PnL metadata row is expected to bind:

```text
order_kind = NO_ORDER
order_quantity = 0
transition_kind = NO_POSITION_CHANGE_NO_ORDER
fill_required = False
actual_fill_ledger_emitted = False
cost_required = False
actual_cost_ledger_emitted = False
pnl_required = False
pnl_rows_emitted = False
actual_pnl_ledger_emitted = False
actual_result_row_emitted = False
actual_backtest_result_emitted = False
result_interpretation_emitted = False
pnl_amount = NOT_APPLICABLE
pnl_currency = NOT_APPLICABLE
pnl_provenance = NO_ORDER_NO_FILL_NO_COST_NO_PNL
```

## Verification

Focused local verification passed:

```text
python -m py_compile src\carver\spine\s27_v2_replay\no_pnl_executable.py tests\test_s27_v2_no_pnl_executable.py
python -m pytest tests\test_s27_v2_no_pnl_executable.py -q
python -m pytest tests\test_s27_v2_no_cost_executable.py tests\test_s27_v2_no_pnl_executable.py -q
```

Results:

```text
py_compile passed
tests\test_s27_v2_no_pnl_executable.py: 20 passed
tests\test_s27_v2_no_cost_executable.py tests\test_s27_v2_no_pnl_executable.py: 43 passed
```

Emitted no-PnL metadata hashes:

```text
bundle_hash = dece5d5a334003dbdd7c1c791c8583ed5dffc8088207a825d626fd15060bc6a7
no_pnl_row_hash = 05730dd1af11e552e68d3cb04f4b517b1f4de1e0b18041d67b8a7a410ec4b05e
no_cost_bundle_hash = 5cd63d10bd15c494713b6635c75a9a123ef943e8805e4482b4c22fe7b93dab99
no_cost_row_hash = f8f07f2f218678a3be6d703025eae9bc643270735550cfba55dd58d0c1075193
no_fill_bundle_hash = 7752233b992fd25cd729c0422a385a24e6aee30dddfffc5c9b91ba4a7296fe5c
no_fill_row_hash = bf7c4f60c182035fdb2b651ab4c9b65bba49c77255eaec00a429875e68da7b97
```

Selected active row:

```text
raw_symbol = ZNM6
selected_decision_timestamp_utc = 2026-04-13T03:00:00Z
order_kind = NO_ORDER
order_quantity = 0
transition_kind = NO_POSITION_CHANGE_NO_ORDER
pnl_required = False
pnl_rows_emitted = False
actual_pnl_ledger_status = FAIL_CLOSED_ACTUAL_PNL_LEDGER_NOT_EMITTED
pnl_amount = NOT_APPLICABLE
pnl_currency = NOT_APPLICABLE
```

## Local Hostile Audit

Local hostile audit passed:

```text
docs/process/CARVER_S27_ZN_V2_NO_PNL_EXECUTABLE_METADATA_LOCAL_AUDIT_RESULT_2026-06-09.md
```

Two independent read-only sidecars returned `PASS` with no P0/P1/P2/P3 findings.

Confirmed:

- active no-cost bundle binding;
- `NO_ORDER` and order quantity zero;
- `NO_POSITION_CHANGE_NO_ORDER`;
- no-fill and no-cost binding;
- no-PnL metadata only;
- actual `PnlLedgerRow`, result row, backtest result row, and result interpretation fail-closed;
- `NOT_APPLICABLE` PnL amount/currency;
- bundle-only authority;
- forged no-cost/no-PnL/downstream flag rejection;
- no package-root export leak;
- no forbidden provider/API/download/backtest/Git/adapter/deployment/trading/promotion/source-faithful evidence surfaces.

## Boundary

This record is not an actual PnL ledger, not a result row, not a backtest, not result interpretation, not PnL evaluation, not promotion evidence, and not a source-faithful evidence claim.
