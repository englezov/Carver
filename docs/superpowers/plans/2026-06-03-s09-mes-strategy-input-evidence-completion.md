# S09 MES Strategy Input Evidence Completion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** After explicit operator authorization, complete the S09/MES source-native strategy-input evidence gate by locking lifecycle, roll semantics, runtime risk, cost, speed eligibility, FDM, and provenance evidence needed before any forecast-input or backtest gate.

**Architecture:** Extend the guard-only `S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_GATE` module into an authorized, fail-closed local artifact writer. The execution may consume only explicitly authorized local/hash-bound S09/MES machinery-slice inputs and operator-named source-native evidence, and must emit CSV/JSON/Markdown/SHA256 artifacts that remain fail-closed unless every required evidence row is locked. The gate must not compute forecasts, diagnostics, positions, returns, PnL, or backtests.

**Tech Stack:** Python 3.11 standard library, `unittest`, existing `carver.spine` S09/MES helpers, local CSV/JSON/Markdown/SHA256 artifacts, PowerShell commands from `C:\Users\openclaw\Desktop\Carver`.

---

## Scope Lock

This plan is not authorization and must not be executed until the operator explicitly authorizes:

```text
Operator authorizes one bounded S09 MES source-native strategy-input evidence completion gate using oldest authorized completed source-native data first.
```

Scope:

```text
gate: S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_GATE
lane_class: SOURCE_NATIVE_FUTURES
source_row: APPENDIX_C_174_006
author_market_code: MES
machinery_development_slice: 2019-05-05 through 2020-04-05
runtime_input_lock_scope: oldest minimum machinery-development slice only
design_ordering: oldest authorized completed source-native data first
```

No Databento API access unless explicitly restated by the operator.

No forecast computation, diagnostics, returns, PnL, positions, carry, TEST, VALIDATION, OOS, Lockbox, Forward, deployment, trading, promotion, Git staging, commit, push, PR, or remote operations.

Git staging, commit, push, PR, and remote operations require separate explicit operator authorization.

## Files

Modify:

```text
tools/databento/carver_s09_mes_strategy_input_evidence_completion.py
tests/test_s09_mes_lineage_synthetic.py
tests/test_s09_mes_readiness_synthetic.py
```

Create after explicit execution authorization only:

```text
docs/process/CARVER_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_RESULT_2026-06-03.md
docs/process/CARVER_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_LOCAL_HOSTILE_AUDIT_2026-06-03.md
docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/
```

Expected output families:

```text
evidence/<STAMP>_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_required_evidence_ledger.csv
lifecycle/<STAMP>_S09_MES_LIFECYCLE_EVIDENCE_ledger.csv
roll/<STAMP>_S09_MES_ROLL_TRADING_DAY_SEMANTICS_ledger.csv
risk/<STAMP>_S09_MES_ANNUAL_RISK_RUNTIME_ledger.csv
risk/<STAMP>_S09_MES_DAILY_PRICE_RISK_ledger.csv
cost/<STAMP>_S09_MES_HISTORICAL_COST_VALUE_ledger.csv
cost/<STAMP>_S09_MES_RISK_ADJUSTED_COST_ledger.csv
speed/<STAMP>_S09_MES_SPEED_ELIGIBILITY_ledger.csv
speed/<STAMP>_S09_MES_ELIGIBLE_SPEED_SET_AND_FDM_ledger.csv
status/<STAMP>_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_status.json
provenance/<STAMP>_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_provenance.md
hashes/<STAMP>_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_sha256.txt
```

## Task 1: Authorized Execution Guard And Header-Only Bundle

**Files:**
- Modify: `tools/databento/carver_s09_mes_strategy_input_evidence_completion.py`
- Modify: `tests/test_s09_mes_lineage_synthetic.py`

- [ ] **Step 1: Write the failing authorized writer test**

Add a test requiring an authorized run to write the header-only fail-closed artifact packet under:

```text
docs/researchops/s09/mes_strategy_input_evidence_completion/2019-05-05_2020-04-05/
```

The test must assert:

```text
status == FAIL_CLOSED_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_NOT_READY
strategy_input_readiness_status == FAIL_CLOSED_S09_MES_STRATEGY_INPUT_NOT_READY
databento_api_access == NO
market_row_parsing == NO
forecast_computation == NO
diagnostics_run == NO
backtests_run == NO
test_validation_lockbox_forward_access == NO
```

- [ ] **Step 2: Verify the test fails**

Run:

```powershell
& 'C:\Users\openclaw\AppData\Local\Programs\Python\Python311\python.exe' -m unittest tests.test_s09_mes_lineage_synthetic.S09MESLineageSyntheticTests.test_s09_mes_strategy_input_evidence_completion_written_packet_is_hash_bound_fail_closed
```

Expected: fail because the writer/result packet is not implemented.

- [ ] **Step 3: Implement the minimal writer**

Use `build_s09_mes_strategy_input_evidence_completion_artifact_bundle` to create the header-only fail-closed bundle. Write only local artifacts after `run_s09_mes_strategy_input_evidence_completion` passes. Do not parse data or inspect provider state.

- [ ] **Step 4: Write result and local hostile audit docs**

Create:

```text
docs/process/CARVER_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_RESULT_2026-06-03.md
docs/process/CARVER_S09_MES_STRATEGY_INPUT_EVIDENCE_COMPLETION_LOCAL_HOSTILE_AUDIT_2026-06-03.md
```

Both docs must state this is fail-closed and not strategy-input ready.

- [ ] **Step 5: Run focused verification**

Run:

```powershell
& 'C:\Users\openclaw\AppData\Local\Programs\Python\Python311\python.exe' -m unittest tests.test_s09_mes_lineage_synthetic.S09MESLineageSyntheticTests.test_s09_mes_strategy_input_evidence_completion_written_packet_is_hash_bound_fail_closed
```

Expected: `OK`.

## Task 2: Lifecycle And Roll Semantics Evidence Contracts

**Files:**
- Modify: `tools/databento/carver_s09_mes_strategy_input_evidence_completion.py`
- Modify: `tests/test_s09_mes_lineage_synthetic.py`

- [ ] **Step 1: Write the failing lifecycle/roll evidence test**

The test must require ledger rows for `official_lifecycle_evidence` and `roll_trading_day_semantics`. Rows must fail closed unless source labels are non-empty, SHA256 values are valid, dates are exact completed dates, and every path stays inside the machinery slice.

- [ ] **Step 2: Verify the test fails**

Run the single new test with `unittest`.

- [ ] **Step 3: Implement lifecycle and roll renderers**

Add CSV renderers for:

```text
lifecycle/<STAMP>_S09_MES_LIFECYCLE_EVIDENCE_ledger.csv
roll/<STAMP>_S09_MES_ROLL_TRADING_DAY_SEMANTICS_ledger.csv
```

Keep rows fail-closed unless all lifecycle and roll semantics evidence is locked.

- [ ] **Step 4: Run focused verification**

Run the single new lifecycle/roll test and then:

```powershell
& 'C:\Users\openclaw\AppData\Local\Programs\Python\Python311\python.exe' -m unittest tests.test_s09_mes_lineage_synthetic
```

## Task 3: Runtime Risk And Daily Price Risk Evidence Contracts

**Files:**
- Modify: `tools/databento/carver_s09_mes_strategy_input_evidence_completion.py`
- Modify: `tests/test_s09_mes_readiness_synthetic.py`

- [ ] **Step 1: Write the failing risk evidence test**

The test must require `annual_risk_runtime_values` and `daily_price_risk_values` to be computed only from locked source-native completed bars and hash-bound input evidence. It must reject missing warmup, incomplete bars, non-MES roots, non-USD/inconsistent values, and stale window paths.

- [ ] **Step 2: Verify the test fails**

Run the single new readiness test with `unittest`.

- [ ] **Step 3: Implement risk evidence renderers**

Add renderers for:

```text
risk/<STAMP>_S09_MES_ANNUAL_RISK_RUNTIME_ledger.csv
risk/<STAMP>_S09_MES_DAILY_PRICE_RISK_ledger.csv
```

Use the locked formula:

```text
daily_price_risk = current_price * annual_percentage_risk / 16
```

- [ ] **Step 4: Run focused verification**

Run:

```powershell
& 'C:\Users\openclaw\AppData\Local\Programs\Python\Python311\python.exe' -m unittest tests.test_s09_mes_readiness_synthetic
```

## Task 4: Historical Cost, Risk-Adjusted Cost, Speed, And FDM Contracts

**Files:**
- Modify: `tools/databento/carver_s09_mes_strategy_input_evidence_completion.py`
- Modify: `tests/test_s09_mes_readiness_synthetic.py`

- [ ] **Step 1: Write the failing cost/speed/FDM test**

The test must require:

```text
historical_mes_cost_values
risk_adjusted_cost_values
speed_eligibility_values
eligible_speed_set
table36_fdm_row
hash_bound_provenance
```

It must reject current-fee defaults, broker/source omissions, non-USD cost values, missing spread/slippage policy, all-six-speed assumption, wrong 0.15 SR threshold, wrong turnover table, and FDM selection before eligible speed set is locked.

- [ ] **Step 2: Verify the test fails**

Run the single new readiness test with `unittest`.

- [ ] **Step 3: Implement cost/speed/FDM renderers**

Add renderers for:

```text
cost/<STAMP>_S09_MES_HISTORICAL_COST_VALUE_ledger.csv
cost/<STAMP>_S09_MES_RISK_ADJUSTED_COST_ledger.csv
speed/<STAMP>_S09_MES_SPEED_ELIGIBILITY_ledger.csv
speed/<STAMP>_S09_MES_ELIGIBLE_SPEED_SET_AND_FDM_ledger.csv
```

No default all-six-speed assumption is allowed.

- [ ] **Step 4: Run focused verification**

Run:

```powershell
& 'C:\Users\openclaw\AppData\Local\Programs\Python\Python311\python.exe' -m unittest tests.test_s09_mes_readiness_synthetic
```

## Task 5: Strategy Input Readiness Handoff

**Files:**
- Modify: `tools/databento/carver_s09_mes_strategy_input_evidence_completion.py`
- Modify: `tests/test_s09_mes_lineage_synthetic.py`
- Modify: `tests/test_s09_mes_readiness_synthetic.py`

- [ ] **Step 1: Write the failing readiness handoff test**

The test must prove the evidence-completion packet cannot claim strategy-input readiness unless every required evidence row is locked and hash-bound.

- [ ] **Step 2: Verify the test fails**

Run the single new handoff test with `unittest`.

- [ ] **Step 3: Implement readiness handoff status**

When all evidence is locked, emit:

```text
READY_FOR_S09_MES_DEV_RECON_FORECAST_INPUT_GATE_NOT_BACKTEST
```

This is not a backtest authorization.

- [ ] **Step 4: Run full verification**

Run:

```powershell
& 'C:\Users\openclaw\AppData\Local\Programs\Python\Python311\python.exe' -m unittest tests.test_s09_mes_lineage_synthetic tests.test_s09_mes_readiness_synthetic tests.test_s09_full_source_atom_synthetic tests.test_s09_m2_synthetic tests.test_s09_phase1_synthetic tests.test_s09_readiness_synthetic tests.test_s09_zn_package_synthetic tests.test_continuous_synthetic
& 'C:\Users\openclaw\AppData\Local\Programs\Python\Python311\python.exe' -m py_compile src/carver/spine/s09_mes_readiness.py src/carver/spine/s09_mes_lineage.py src/carver/spine/__init__.py tools/databento/carver_s09_mes_strategy_input_evidence_completion.py tests/test_s09_mes_readiness_synthetic.py tests/test_s09_mes_lineage_synthetic.py
```

Expected:

```text
all S09 synthetic tests pass
py_compile exits 0
```

## Self-Review

Spec coverage:

```text
source-native futures lane: covered
MES Appendix C row lock: covered
2019-05-05 through 2020-04-05 machinery-development slice: covered
oldest authorized completed source-native data first: covered
official_lifecycle_evidence: covered
roll_trading_day_semantics: covered
annual_risk_runtime_values: covered
daily_price_risk_values: covered
historical_mes_cost_values: covered
risk_adjusted_cost_values: covered
speed_eligibility_values: covered
eligible_speed_set: covered
table36_fdm_row: covered
hash_bound_provenance: covered
no forecast/backtest/OOS/Lockbox/Forward/promotion/Git: covered
```

Placeholder scan:

```text
No placeholder markers are intentionally present.
```

Type consistency:

```text
The plan uses the existing `S09MESStrategyInputEvidenceCompletionConfig`, `run_s09_mes_strategy_input_evidence_completion`, and `build_s09_mes_strategy_input_evidence_completion_artifact_bundle` names introduced before this plan.
```
