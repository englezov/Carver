# S27_V2 No-PnL Executable Metadata Local Hostile Audit Result

Date: 2026-06-09

Status:

```text
LOCAL_HOSTILE_AUDIT_PASS
```

## Scope

Local hostile audit of the `S27_V2` no-PnL executable metadata gate.

Audited files:

```text
src/carver/spine/s27_v2_replay/no_pnl_executable.py
tests/test_s27_v2_no_pnl_executable.py
src/carver/spine/s27_v2_replay/no_cost_executable.py
src/carver/spine/s27_v2_replay/no_fill_executable.py
src/carver/spine/s27_v2_replay/order_transition_executable.py
src/carver/spine/s27_v2_replay/__init__.py
docs/process/CARVER_S27_ZN_V2_NO_PNL_EXECUTABLE_METADATA_IMPLEMENTATION_RECORD_2026-06-09.md
docs/process/CARVER_S27_ZN_V2_PNL_EVIDENCE_PNL_EXECUTABLE_PLANNING_GATE_2026-06-09.md
```

Forbidden scope preserved:

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

## Audit Method

Two independent subagents performed read-only hostile audits.

Sidecar A checked:

- active no-cost bundle binding;
- `NO_ORDER` and order quantity zero;
- `NO_POSITION_CHANGE_NO_ORDER`;
- fill/cost/PnL/result/backtest fail-closed boundaries;
- `NOT_APPLICABLE` PnL amount/currency;
- bundle-only authority;
- package-root export boundary;
- absence of forbidden provider/backtest/Git/result/source-faithful surfaces.

Sidecar B checked:

- caller-supplied no-cost bundle forgery;
- self-consistent no-PnL row/bundle hash forgery;
- PnL-required flags;
- PnL amount/currency/provenance forgery;
- actual `PnlLedgerRow`, result, and backtest flags;
- non-authorization drift;
- package-root export holes.

## Verdict

```text
PASS
```

P0 findings:

```text
NONE
```

P1 findings:

```text
NONE
```

P2 findings:

```text
NONE
```

P3 findings:

```text
NONE
```

## Confirmed Properties

The local hostile audits confirmed:

- `NoPnlExecutableMetadataRow.validate()` is standalone non-authority and always fails closed;
- `NoPnlExecutableBundle.validate()` rebuilds active no-cost authority from the audited remediation pack and exact-compares it;
- active no-PnL row construction binds the externally passed no-order/no-fill/no-cost path;
- `pnl_required = False`;
- `pnl_rows_emitted = False`;
- `actual_pnl_ledger_emitted = False`;
- actual PnL ledger status remains `FAIL_CLOSED_ACTUAL_PNL_LEDGER_NOT_EMITTED`;
- result row, backtest result, and result interpretation flags remain false;
- PnL amount and currency are `NOT_APPLICABLE`;
- forged no-cost bundles, no-PnL rows, row hashes, bundle hashes, PnL amounts, PnL currency, PnL provenance, and downstream flags are rejected;
- no `PnlLedgerRow` import or actual PnL/result emission surface exists in the no-PnL executable module;
- package-root exports remain narrow.

## Verification Referenced By Audit

Focused verification already passed:

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

## Boundary

This local audit result is not an external audit result, not an actual PnL ledger, not a result row, not a backtest, not result interpretation, not PnL evaluation, not promotion evidence, and not a source-faithful evidence claim.
