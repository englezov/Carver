# S09 MES Eligible Speed Set And Table 36 FDM Row Lock Subagent Hostile Audit Result

Date: 2026-06-03

Status:

```text
PASS
```

Auditor:

```text
Darwin
```

Scope:

- formal eligible speed set lock
- formal Table 36 FDM row lock
- S09 MES Appendix C row APPENDIX_C_174_006
- machinery-development slice 2019-05-05 through 2020-04-05
- corrected dual speed eligibility ledger as source

Findings:

- eligible_spans are locked to 2|4|8|16|32|64
- Table 36 FDM is locked to 1.26
- source hash matches the corrected dual speed eligibility ledger
- remaining_evidence_count is 1
- hash_bound_provenance_lock remains NO
- strategy input readiness remains fail-closed
- no forecast computation, diagnostics, backtests, TEST, VALIDATION, Lockbox,
  Forward, Git staging, commit, push, PR, deployment, trading, or promotion
  was introduced

Verification:

```text
python -m unittest tests.test_s09_mes_lineage_synthetic
82 tests OK
```

Parent verification also ran:

```text
python -m unittest tests.test_s09_mes_readiness_synthetic tests.test_s09_mes_lineage_synthetic
120 tests OK
```
