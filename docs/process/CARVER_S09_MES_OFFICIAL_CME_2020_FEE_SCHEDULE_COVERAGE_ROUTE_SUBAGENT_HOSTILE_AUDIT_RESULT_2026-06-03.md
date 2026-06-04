# Carver S09 MES Official CME 2020 Fee Schedule Coverage Route Hostile Audit Result

Date: 2026-06-03

Status:

```text
PASS_BOUNDED_2020_CME_EXCHANGE_FEE_COVERAGE_EXTRACTED_REMAINING_COST_BLOCKERS_FAIL_CLOSED
```

Tooling note:

```text
PARENT_THREAD_SPAWNED_HOSTILE_AUDIT_SUBAGENT
```

The standing operator instruction is to use subagents for hostile audits. The
parent thread spawned a fresh hostile-audit subagent for this bounded 2020 CME
coverage audit. Any subagent-local tool exposure limitation is not a failure of
the parent-thread spawn requirement.

Authorized audit scope:

```text
official_cme_2020_fee_schedule_coverage_permitted_route
```

Target coverage:

```text
2020-01-01 through 2020-04-05 exchange-fee coverage only
```

Artifacts audited:

- `C:\Users\openclaw\Desktop\cme-fee-schedules-2020.zip`
- `docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/cost_source_extracts/official_cme_2020_fee_schedule_archive/cme-fee-schedules-2020.zip`
- `docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/cost_source_extracts/official_cme_2020_fee_schedule_archive/cme-fee-schedules-2020/cme-fee-schedule-2020-01-01.xls`
- `docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/cost_source_extracts/official_cme_2020_fee_schedule_archive/cme-fee-schedules-2020/cme-fee-schedule-2020-02-01.xls`
- `docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/cost_source_extracts/official_cme_2020_fee_schedule_archive/cme-fee-schedules-2020/cme-fee-schedule-2020-03-01.xls`
- `docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/cost_source_extracts/official_cme_2020_fee_schedule_archive/cme-fee-schedules-2020/cme-fee-schedule-2020-04-01.xls`
- `docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/cost_source_extracts/cme_2020_fee_schedule_archive_exchange_fee_extract.md`
- `docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/cost_source_extracts/cme_2020_fee_schedule_download_blocker_extract.md`
- `docs/process/CARVER_S09_MES_OFFICIAL_CME_2020_FEE_SCHEDULE_COVERAGE_ROUTE_RESULT_2026-06-03.md`
- `docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/cost_source_extracts/20260603_S09_MES_HISTORICAL_COST_SOURCE_EXTRACTION_status.csv`
- `docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/cost_source_extracts/20260603_S09_MES_HISTORICAL_COST_SOURCE_EXTRACTION_sha256.txt`
- `docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/cost/20260603_S09_MES_HISTORICAL_COST_VALUE_ledger.csv`
- `docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/status/20260603_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_status.json`

Findings:

1. PASS: The operator-provided archive exists at:

```text
C:\Users\openclaw\Desktop\cme-fee-schedules-2020.zip
```

2. PASS: The clean-workspace archive copy exists at:

```text
docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/cost_source_extracts/official_cme_2020_fee_schedule_archive/cme-fee-schedules-2020.zip
```

3. PASS: The Desktop archive and clean-workspace copy are hash-identical:

```text
F7BB5F63C6E8B978075ABC79A55F79D28396CE09DA0B9B41DD6610FACC9DAFD4
```

4. PASS: The archive was expanded locally in the clean Carver workspace. The
   four audited schedule files for the remaining machinery-development slice
   are present:

```text
cme-fee-schedule-2020-01-01.xls
cme-fee-schedule-2020-02-01.xls
cme-fee-schedule-2020-03-01.xls
cme-fee-schedule-2020-04-01.xls
```

5. PASS: Independent XLS inspection of the `Equity` sheets supports the
   extracted Non-Members / Globex - Outrights / Micro E-mini Index / Futures
   exchange fee value:

```text
cme-fee-schedule-2020-01-01.xls | Equity | row 36 | physical column 11 (xlrd zero-based column 10) | 0.20 USD per side
cme-fee-schedule-2020-02-01.xls | Equity | row 36 | physical column 11 (xlrd zero-based column 10) | 0.20 USD per side
cme-fee-schedule-2020-03-01.xls | Equity | row 36 | physical column 11 (xlrd zero-based column 10) | 0.20 USD per side
cme-fee-schedule-2020-04-01.xls | Equity | row 36 | physical column 11 (xlrd zero-based column 10) | 0.20 USD per side
```

6. PASS: The column headers identify physical column 11 as
   `Micro E-mini Index / Futures`, and the surrounding rows identify row 35 as
   the Non-Members block and row 36 as the Globex - Outrights row.

7. PASS: The extraction artifact and route-result artifact now mark
   `official_cme_2020_fee_schedule_coverage` as:

```text
PARTIAL_SOURCE_NATIVE_CME_2020_EXCHANGE_FEE_COVERAGE_EXTRACTED
```

8. PASS: The stale automated-access blocker was not erased. It is retained as
   superseded by the later operator-provided official archive extraction.

9. PASS: The refreshed source-extraction SHA256 manifest includes the 2020
   extraction artifact, the 2020 archive ZIP, and extracted 2020 schedule files.

10. PASS: No evidence was found of user-agent spoofing, mirror substitution,
    current-fee substitution, CFD assumptions, QuantLab active use, or
    retired-window contamination in the audited 2020 route artifacts.

11. PASS: The active historical MES cost ledger remains header-only. No cost
    rows were written.

12. PASS: `historical_mes_cost_values` remains fail-closed:

```text
FAIL_CLOSED_S09_MES_HISTORICAL_COST_VALUES_NOT_LOCKED
```

13. PASS: The global S09 evidence-completion gate remains fail-closed with
    `remaining_evidence_count: 6`.

14. PASS: The only remaining cost-source blockers represented after the 2020
    extraction are:

```text
broker_current_fee_static_historical_policy
spread_slippage_source_or_policy
```

15. PASS: No cost computation, risk-adjusted cost computation, speed
    eligibility computation, forecast computation, diagnostics, backtests,
    TEST, VALIDATION, Lockbox, Forward, deployment, trading, promotion, Git
    staging, commit, push, PR, or remote operation was performed by this audit.

Conclusion:

```text
PASS_BOUNDED_2020_CME_EXCHANGE_FEE_COVERAGE_ROUTE_READY_COST_VALUES_STILL_FAIL_CLOSED
```

The final official CME 2020 archive route is clean for the authorized
2020-01-01 through 2020-04-05 CME exchange-fee portion only. Combined with the
already extracted 2019 official CME schedule rows, source-native CME exchange
fee coverage is now extracted for the full machinery-development slice. Full
`historical_mes_cost_values` remains fail-closed until the operator resolves
`broker_current_fee_static_historical_policy` and
`spread_slippage_source_or_policy`.
