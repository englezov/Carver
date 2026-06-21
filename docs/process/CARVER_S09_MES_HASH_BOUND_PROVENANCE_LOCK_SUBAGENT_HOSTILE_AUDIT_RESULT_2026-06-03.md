# S09 MES Hash-Bound Provenance Lock Subagent Hostile Audit Result

Date: 2026-06-03

Auditor:

```text
Noether
```

Status:

```text
PASS_S09_MES_HASH_BOUND_PROVENANCE_LOCK_READ_ONLY_HOSTILE_AUDIT
```

Scope:

- `tools/databento/carver_s09_mes_hash_bound_provenance_lock.py`
- `docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/status/20260603_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_status.json`
- `docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/evidence/20260603_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_required_evidence_ledger.csv`
- `docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/hashes/20260603_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_sha256.txt`
- `tests/test_s09_mes_lineage_synthetic.py`

Findings:

- Guard code enforces source-native MES row/window, explicit hash-bound lock, upstream locked statuses, and blocks readiness, forecasts, diagnostics, backtests, TEST, VALIDATION, Lockbox, Forward, and Git.
- Final status is `LOCKED_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETE_NOT_BACKTEST_AUTHORIZATION`.
- `remaining_evidence_count` is `0`.
- Strategy readiness is only awaiting `S09_MES_STRATEGY_INPUT_READINESS_GATE`.
- Required evidence ledger has all rows `LOCKED_SOURCE_NATIVE_EVIDENCE`, including `hash_bound_provenance`.
- SHA256 manifest excludes `/hashes/` paths and recomputed cleanly for `111` entries.
- Tests cover hostile configs including no authorization, CFD adapter lane, wrong root/row/window, readiness, forecasts, diagnostics, backtests, later-window access, and Git.

Verification Reported By Auditor:

```text
python -B -m unittest tests.test_s09_mes_lineage_synthetic.S09MESLineageSyntheticTests.test_s09_mes_hash_bound_provenance_lock_completes_evidence_without_readiness_or_backtest tests.test_s09_mes_lineage_synthetic.S09MESLineageSyntheticTests.test_s09_mes_strategy_input_evidence_completion_written_packet_is_hash_bound_locked_no_readiness
Ran 2 tests ... OK
```

Boundary:

No backtests, diagnostics, forecasts, provider/API access, TEST, VALIDATION,
Lockbox, Forward, Git staging, commit, push, PR, deployment, trading, or
promotion were performed by the hostile audit.
