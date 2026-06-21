# S27 ZN V2 Executable Replay Ledger Phase 1 Fail-Closed Local Audit Result

Date: 2026-06-08

Status:

```text
LOCAL_HOSTILE_AUDIT_PASS_NO_P0_P1_P2_FINDINGS
```

Audited scope:

```text
src/carver/spine/s27_v2_replay/executable_replay.py
tests/test_s27_v2_local_replay_slice1.py
```

Related implementation record:

```text
docs/process/CARVER_S27_ZN_V2_EXECUTABLE_REPLAY_LEDGER_PHASE1_FAIL_CLOSED_IMPLEMENTATION_RECORD_2026-06-08.md
```

## Audit Loop

The local hostile audit was performed with two subagents.

Initial findings included:

- caller-supplied construction manifest hash;
- first-row-only row-family provenance binding;
- per-ledger blocker and reason maps not locked in validators;
- unresolved-gate set not exact-bound to gate rows;
- source-row-batch contract hash using the set hash rather than contract hash;
- construction manifest boundary/artifact-file validation too permissive.

All P1/P2 findings were patched inside the authorized fail-closed executable
ledger phase scope.

## Final Re-Audit Result

Final local hostile re-audit result:

```text
PASS - no P0/P1/P2 findings.
```

Confirmed closures:

- exact 34 construction artifact file set is locked;
- each listed construction artifact file is byte-SHA checked under the
  controlled construction output path;
- construction artifacts parse as JSON objects;
- key artifact JSON hashes bind active construction objects;
- `source_row_batch_contract_hash` uses the actual contract hash, not set hash;
- per-ledger blocker and reason mappings are locked;
- unresolved gate set exactly matches gate-row blockers;
- no provider/API, download, OOS, Lockbox, Forward, backtest, result, PnL
  interpretation, Git, adapter, deployment, trading, or promotion surface was
  introduced.

## Verification

Focused local verification after all audit patches:

```text
python -m pytest tests\test_s27_v2_local_replay_slice1.py -q
58 passed
```

Compile check:

```text
python -m compileall -q src\carver\spine\s27_v2_replay\executable_replay.py
PASS
```

## Boundary

This audit result is not a backtest, not a result-scored run, not PnL
interpretation, not promotion, and not a source-faithful evidence claim.

Any move from fail-closed executable surfaces into nonblocked runtime-history,
forecast, order, fill, cost, or PnL ledgers requires separate explicit operator
authorization and sufficient audited input history/policy evidence.
