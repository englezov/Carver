# Carver S09 MES Official CME 2019 Fee Schedule Permitted Route Subagent Hostile Audit Result

Date: 2026-06-03

Status:

```text
PASS
```

Audit scope:

```text
official_cme_2019_fee_schedule_archive_permitted_route
```

Authorized lane and row:

- lane_class: SOURCE_NATIVE_FUTURES
- root: MES
- row_id: APPENDIX_C_174_006
- machinery_development_slice: 2019-05-05 through 2020-04-05
- selected_evidence_name: historical_mes_cost_values

Files inspected:

- `docs/process/CARVER_S09_MES_OFFICIAL_CME_2019_FEE_SCHEDULE_PERMITTED_ROUTE_RESULT_2026-06-03.md`
- `docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/cost_source_extracts/20260603_S09_MES_HISTORICAL_COST_SOURCE_EXTRACTION_status.csv`
- `docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/cost_source_extracts/cme_2019_fee_schedule_download_blocker_extract.md`
- `docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/cost_source_extracts/20260603_S09_MES_HISTORICAL_COST_SOURCE_EXTRACTION_sha256.txt`
- `docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/cost/20260603_S09_MES_HISTORICAL_COST_VALUE_status.json`
- `docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/cost/20260603_S09_MES_HISTORICAL_COST_VALUE_ledger.csv`
- `docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/status/20260603_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_status.json`
- `docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/evidence/20260603_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_required_evidence_ledger.csv`

Findings:

1. PASS: The result artifact stays within the authorized `official_cme_2019_fee_schedule_archive_permitted_route` scope. It records CME's official historical-fees page and official CME 2019 fee schedule archive route only.
2. PASS: The attempt did not use unofficial mirrors, current-fee defaults, user-agent spoofing, retired-window artifacts, old workspace state, CFD assumptions, or QuantLab artifacts as authority.
3. PASS: The official CME archive was not retrieved after the automated-access block. The blocker extract records that CME returned an automated-access block page instead of a ZIP archive.
4. PASS: `exchange_fee_value` remains `FAIL_CLOSED_S09_MES_EXCHANGE_FEE_VALUE_NOT_EXTRACTED`.
5. PASS: `clearing_regulatory_fee_value` remains `FAIL_CLOSED_S09_MES_CLEARING_REGULATORY_FEE_VALUE_NOT_EXTRACTED`.
6. PASS: Broker commission remains untouched as `FAIL_CLOSED_S09_MES_BROKER_COMMISSION_SOURCE_NOT_NAMED`.
7. PASS: Spread/slippage remains untouched as `FAIL_CLOSED_S09_MES_SPREAD_SLIPPAGE_POLICY_NOT_LOCKED`.
8. PASS: `historical_mes_cost_values` remains fail-closed and is not locked.
9. PASS: The historical cost value ledger is header-only with zero cost rows.
10. PASS: Global evidence status remains `FAIL_CLOSED_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_NOT_READY`.
11. PASS: `remaining_evidence_count` remains `6`.
12. PASS: No cost computation, risk-adjusted cost computation, speed eligibility computation, forecast computation, diagnostics, backtests, TEST, VALIDATION, Lockbox, Forward, Git, deployment, trading, promotion, CFD adapter work, QuantLab use, or retired-window promotion was found in the inspected gate artifacts.
13. PASS: Header-only risk-adjusted cost and speed ledgers remain placeholders with no computed rows.
14. PASS: The SHA256 manifest matches the inspected cost-source extraction artifacts.

Observation:

- The official CME archive path appears in two official CME path variants across the artifacts:
  - `https://www.cmegroup.com/company/clearing-fees/historical-fees/files/cme-fee-schedules-2019.zip`
  - `https://www.cmegroup.com/content/dam/cmegroup/company/clearing-fees/files/cme-fee-schedule-2019.zip`
  This is not a failure for this gate because both references are CME-owned paths, no archive was retrieved from either route for value extraction, and the cost values remain fail-closed. Before a future value extraction gate, the exact official archive route should be normalized to the route actually retrieved or operator-provided.

Verification performed:

- Read mandatory Carver governance files.
- Read official CME-route result artifact.
- Read cost-source extraction status ledger and blocker extract.
- Read historical cost value status and ledger.
- Read global evidence status and required evidence ledger.
- Recomputed SHA256 for all files listed in the cost-source extraction hash manifest.
- Searched scoped gate artifacts for contamination and unauthorized-scope markers.
- Confirmed there are no ZIP, XLSX, or XLS archive files under the machinery-slice cost-source extract folder.
- Confirmed historical cost, risk-adjusted cost, speed eligibility, and eligible speed/FDM ledgers contain headers only where present.

Subagent dispatch note:

```text
No managed subagent-dispatch tool was exposed in this session. This hostile audit result was written from the current audit executor after direct worktree inspection, without running backtests or diagnostics.
```

Final disposition:

```text
PASS_OFFICIAL_CME_ROUTE_ATTEMPT_REMAINED_FAIL_CLOSED_AND_WITHIN_AUTHORIZED_SCOPE
```
