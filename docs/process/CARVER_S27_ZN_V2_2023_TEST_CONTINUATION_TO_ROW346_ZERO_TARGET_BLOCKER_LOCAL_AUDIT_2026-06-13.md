# S27_V2 2023 TEST Continuation To Row 346 Zero-Target Blocker Local Audit

Date: 2026-06-13

## Scope

This record covers the controlled local-only 2023 TEST continuation after the row-304 external-logic/meta-audit classification:

```text
ROW304_EXTERNAL_LOGIC_REAUDIT_PASS_PACKET_HYGIENE_FAIL_NOT_BLOCKING_LOCAL_CONTINUATION
```

The continuation used already-local 2023 ZN TEST files and audited S27_V2 machinery only. It did not use provider/API access, downloads, new data acquisition, VALIDATION, OOS, Lockbox, Forward, result interpretation, tuning, adapter work, deployment, trading, promotion, Git actions, or source-faithful evidence claims.

## Implementation

`src/carver/spine/s27_v2_replay/test_mechanical_run.py` was patched so the preselection mechanics in `_row_mechanics()` recognize the already accepted row-304 session-open engineering market-reset class using the same bounded predicate as the accepting execution path.

The predicate remains exact and row-specific. It requires:

- row index `304`;
- `ZNH3` decision, fill, and valuation rows;
- decision timestamp `2023-01-20T21:00:00Z`;
- fill timestamp `2023-01-20T22:00:00Z`;
- valuation mark timestamp `2023-01-23T00:00:00Z`;
- position change `BUY 2`;
- decision timestamp equal to prior declared session end;
- fill timestamp equal to next declared session open;
- session change between decision, fill, and valuation mark;
- valuation convention `SOURCE_NATIVE_ENGINEERING_VALUATION_ASSUMPTION_NOT_BOOK_EXPLICIT`;
- selected DataBento TBBO evidence at `2023-01-20T21:59:59.924187905Z`;
- selected ask `115.0625`;
- source evidence type `BATCH_AT_OR_BEFORE_FILL_TBBO`;
- fresh non-crossed TBBO selection status.

This aligns pack selection with the already hardened accepting execution path and does not generalize row-304 behavior to other overnight/session-open rows.

## Resulting Local Mechanical Run State

The 2023 TEST declared pack and mechanical run were rebuilt locally.

Pack:

- test window start: `2023-01-03T00:00:00Z`;
- candidate row count: `346`;
- supported mechanical row count declared by pack manifest: `345`;
- fail-closed blocker row: `346`;
- fail-closed blocker timestamp: `2023-01-24T19:00:00Z`;
- fail-closed reason: `FAIL_CLOSED_ADJACENT_LIMIT_FORMULA_UNSUPPORTED_TARGET_POSITION_ZERO_NOT_RESULT`.

Row-346 blocker facts:

- raw symbol: `ZNH3`;
- starting position: `1`;
- desired position: `0`;
- position change: `-1`;
- order side: `SELL`;
- adjacent target position: `0`;
- formula status: `FAIL_CLOSED_ADJACENT_LIMIT_FORMULA_UNSUPPORTED_TARGET_POSITION_ZERO_NOT_RESULT`.

Run:

- candidate row count: `346`;
- supported mechanical rows: `345`;
- fail-closed row index: `346`;
- final supported position: `1`;
- cumulative gross mechanical PnL metadata: `8750.0`;
- cumulative commission metadata: `503.70000000000016`;
- cumulative spread metadata: `0.0`;
- cumulative net mechanical PnL metadata: `8246.3`.

These values are mechanical construction metadata only. They are not result interpretation, performance evaluation, source-faithful evidence, promotion evidence, or trading evidence.

## Hashes

Current run artifact hashes:

- `run_manifest.json`: `B91505C68E293C8CDA33531DC09C83AFF71FEC6C19BF198DFC9BB47F147B94EB`;
- `evidence_manifest.json`: `7FC0CB4CFF431AF8BB7565D11EA840DB495C7F9664B4C0D1B775543EDF858A67`;
- `trusted_bundle.json`: `932D2A62452BAB93DFE6F362F0D8C3E30075B9A0584C96113F74F49B762135E5`;
- `run_bundle.json`: `0DED8AD4CE34F4E200011575492A0E82DD587BE98EB349E9359C358B370A7950`;
- `SHA256SUMS.csv`: `EB5806CB45DD37912AA22D4F192C193AB7DA78A2987C7BEB7BE476B5234AA9CA`;
- `fail_closed_ledger.csv`: `436FEE6A591B2480F6B076AA0B33ECFA50B5512F2F4102A92FF20E01CF88E0FA`;
- `pnl_ledger.csv`: `F6B1F1311A2454FC7AE330C1FF901A5723D2544A9D189FC8C98741B158611788`.

Local hash binding verification passed for:

- `SHA256SUMS.csv`;
- `evidence_manifest.json`;
- `trusted_bundle.json`.

## Verification

Commands run:

```text
python -m py_compile src\carver\spine\s27_v2_replay\test_mechanical_run.py tests\test_s27_v2_2023_test_mechanical_run.py
python -m pytest tests\test_s27_v2_2023_test_mechanical_run.py -q
python -m pytest tests\test_s27_v2_pretest_development_recon_completion.py tests\test_s27_v2_2023_test_mechanical_run.py -q
```

Results:

```text
75 passed in 127.12s
136 passed in 131.54s
```

## Local Hostile Audit

One read-only local hostile-audit subagent returned:

```text
P0: None
P1: None
P2: None
P3: None
```

The audit confirmed:

- row 304 remains tightly bounded and not generalized;
- the TEST pack/run extends to row 346 and stops on the target-position-zero adjacent-limit formula blocker;
- tests bind the new terminal state and preserve row-304 forged-mutation coverage;
- result/backtest/source-faithful evidence gates remain fail-closed.

## Current Status

Status:

```text
LOCAL_PASS_2023_TEST_CONTINUATION_TO_ROW346_ZERO_TARGET_BLOCKER_NOT_RESULT
```

The next unresolved class is:

```text
FAIL_CLOSED_ADJACENT_LIMIT_FORMULA_UNSUPPORTED_TARGET_POSITION_ZERO_NOT_RESULT
```

The next useful gate is a local-only policy/source-lock or implementation-planning gate for target-position-zero adjacent limit behavior. It must decide whether the Carver/source-native execution formula supports a final `SELL 1` toward target position zero, whether a distinct flatten/zero-target rule is required, or whether row 346 remains fail-closed.

## Non-Authorizations

This record does not authorize:

- provider/API access;
- downloads;
- new data acquisition;
- broader TEST continuation beyond row 346;
- VALIDATION;
- OOS;
- Lockbox;
- Forward;
- result interpretation;
- PnL evaluation beyond mechanical construction;
- tuning;
- adapter work;
- deployment;
- trading;
- promotion;
- Git staging, commit, push, or PR;
- source-faithful evidence claims.
