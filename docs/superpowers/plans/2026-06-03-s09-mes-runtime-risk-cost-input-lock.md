# S09 MES Runtime Risk Cost Input Lock Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** After explicit operator authorization, lock the missing S09/MES source-native Development/Reconciliation runtime risk, cost, risk-adjusted cost, and speed eligibility inputs needed before any forecast-input gate.

**Architecture:** Add one fail-closed local execution script for `S09_MES_RUNTIME_RISK_COST_INPUT_LOCK_GATE`. The script may consume only explicitly authorized local/hash-bound S09/MES artifacts and operator-named cost evidence, then emits CSV/JSON/Markdown/SHA256 artifacts. If any required input is absent, ambiguous, degraded, not hash-bound, or not oldest-authorized-first, the output must fail closed and remain unusable as forecast input.

**Tech Stack:** Python 3.11 standard library, `unittest`, existing `carver.spine` S09/MES helpers, local CSV/JSON/Markdown artifacts, PowerShell invocation from `C:\Users\openclaw\Desktop\Carver`.

---

## Scope Lock

This plan is not authorization and must not be executed until the operator explicitly authorizes:

```text
Operator authorizes one bounded S09 MES source-native Development/Reconciliation runtime risk and historical cost input-lock gate using oldest authorized completed source-native data first.
```

Scope: 2019-05-05 through 2020-04-05 machinery-development slice only.

The implementation is locked to:

```text
gate: S09_MES_RUNTIME_RISK_COST_INPUT_LOCK_GATE
lane_class: SOURCE_NATIVE_FUTURES
source_row: APPENDIX_C_174_006
author_market_code: MES
machinery_development_slice: 2019-05-05 through 2020-04-05
runtime_input_lock_scope: oldest minimum machinery-development slice only
design_ordering: oldest authorized completed source-native data first
```

2022-2023 is not the Dev/Reconciliation default.
3:3:4 TEST/VALIDATION/LOCKBOX windows are separately locked and separately gated.

No Databento API access unless explicitly restated by the operator.

No forecast computation, diagnostics, returns, PnL, positions, carry, TEST, VALIDATION, OOS, Lockbox, Forward, deployment, trading, promotion, Git staging, commit, push, PR, or remote operations.

## Files

Create:

```text
tools/databento/carver_s09_mes_runtime_risk_cost_input_lock.py
docs/process/CARVER_S09_MES_RUNTIME_RISK_COST_INPUT_LOCK_RESULT_2026-06-03.md
docs/process/CARVER_S09_MES_RUNTIME_RISK_COST_INPUT_LOCK_LOCAL_HOSTILE_AUDIT_2026-06-03.md
```

Modify:

```text
tests/test_s09_mes_lineage_synthetic.py
tests/test_s09_mes_readiness_synthetic.py
```

Expected output root after authorized execution:

```text
docs/researchops/s09/mes_runtime_risk_cost_input_lock/2019-05-05_2020-04-05/
```

Expected output families:

```text
input_manifest/<STAMP>_S09_MES_RUNTIME_RISK_COST_INPUT_LOCK_input_manifest.csv
risk/<STAMP>_S09_MES_ANNUAL_RISK_RUNTIME_ledger.csv
risk/<STAMP>_S09_MES_DAILY_PRICE_RISK_RUNTIME_ledger.csv
cost/<STAMP>_S09_MES_COST_VALUE_ledger.csv
cost/<STAMP>_S09_MES_RISK_ADJUSTED_COST_ledger.csv
speed/<STAMP>_S09_MES_SPEED_ELIGIBILITY_ledger.csv
status/<STAMP>_S09_MES_RUNTIME_RISK_COST_INPUT_LOCK_status.json
provenance/<STAMP>_S09_MES_RUNTIME_RISK_COST_INPUT_LOCK_provenance.md
hashes/<STAMP>_S09_MES_RUNTIME_RISK_COST_INPUT_LOCK_sha256.txt
```

## Task 1: Authorization Guard And Input Manifest

**Files:**
- Create: `tools/databento/carver_s09_mes_runtime_risk_cost_input_lock.py`
- Modify: `tests/test_s09_mes_lineage_synthetic.py`

- [ ] **Step 1: Write the failing authorization test**

Add a test that imports `S09MESRuntimeRiskCostInputLockConfig` and `run_s09_mes_runtime_risk_cost_input_lock`, builds a config with `execution_authorized=False`, and asserts `CarverBlocked`.

- [ ] **Step 2: Run the focused test to verify it fails**

Run:

```powershell
& 'C:\Users\openclaw\AppData\Local\Programs\Python\Python311\python.exe' -m unittest tests.test_s09_mes_lineage_synthetic.S09MESLineageSyntheticTests.test_s09_mes_runtime_risk_cost_input_lock_requires_authorization
```

Expected: import failure or `CarverBlocked` guard failure before implementation.

- [ ] **Step 3: Implement the minimal guard**

Create a config dataclass with:

```text
execution_authorized
lane_class
root
row_id
target_start
target_end
design_ordering
databento_api_access_authorized
```

The guard must require `SOURCE_NATIVE_FUTURES`, `MES`, `APPENDIX_C_174_006`, `2019-05-05`, `2020-04-05`, `oldest minimum machinery-development slice only`, and `oldest authorized completed source-native data first`.

- [ ] **Step 4: Add the input manifest renderer contract**

The input manifest CSV columns are:

```text
input_name,relative_path,required_status,sha256,status
```

Rows must fail closed unless every required input is hash-bound, local, and within the authorized S09/MES Development/Reconciliation scope.

- [ ] **Step 5: Run focused tests**

Run the focused lineage suite:

```powershell
& 'C:\Users\openclaw\AppData\Local\Programs\Python\Python311\python.exe' -m unittest tests.test_s09_mes_lineage_synthetic
```

## Task 2: Runtime Annual Risk And Daily Price Risk Ledgers

**Files:**
- Modify: `tools/databento/carver_s09_mes_runtime_risk_cost_input_lock.py`
- Modify: `tests/test_s09_mes_readiness_synthetic.py`

- [ ] **Step 1: Write the failing runtime-risk execution test**

The test must prove annual-risk runtime and daily price-risk values use completed bars only, source-native MES rows only, and oldest-authorized data ordering.

- [ ] **Step 2: Run the focused test to verify it fails**

Run the single new readiness test with `unittest`.

- [ ] **Step 3: Implement annual-risk runtime ledger emission**

Emit:

```text
risk/<STAMP>_S09_MES_ANNUAL_RISK_RUNTIME_ledger.csv
```

Required columns:

```text
completed_trading_date,long_run_annual_risk,current_ewma32_annual_risk,annual_percentage_risk,source_sha256,status
```

Fail closed if the runtime risk source is not hash-bound, if a row is not a completed bar, or if the oldest authorized completed source-native data cannot support the calculation.

- [ ] **Step 4: Implement daily price-risk ledger emission**

Emit:

```text
risk/<STAMP>_S09_MES_DAILY_PRICE_RISK_RUNTIME_ledger.csv
```

Required formula:

```text
daily_price_risk = current_price * annual_percentage_risk / 16
```

- [ ] **Step 5: Run focused tests**

Run:

```powershell
& 'C:\Users\openclaw\AppData\Local\Programs\Python\Python311\python.exe' -m unittest tests.test_s09_mes_readiness_synthetic
```

## Task 3: Historical Cost Value Lock

**Files:**
- Modify: `tools/databento/carver_s09_mes_runtime_risk_cost_input_lock.py`
- Modify: `tests/test_s09_mes_readiness_synthetic.py`

- [ ] **Step 1: Write the failing cost-value lock test**

The test must require historical MES exchange/clearing/regulatory/broker/spread/slippage cost values and reject current-fee defaults, missing broker source, missing spread/slippage policy, non-USD values, and non-hash-bound sources.

- [ ] **Step 2: Run the focused test to verify it fails**

Run the single new readiness test with `unittest`.

- [ ] **Step 3: Implement cost value ledger emission**

Emit:

```text
cost/<STAMP>_S09_MES_COST_VALUE_ledger.csv
```

Required columns:

```text
completed_trading_date,component_name,amount_currency,currency,charge_timing,effective_start,effective_end,source_label,source_sha256,status
```

Required component names:

```text
exchange_fee
clearing_regulatory_fee
broker_commission
spread_slippage
```

- [ ] **Step 4: Run focused tests**

Run:

```powershell
& 'C:\Users\openclaw\AppData\Local\Programs\Python\Python311\python.exe' -m unittest tests.test_s09_mes_readiness_synthetic
```

## Task 4: Risk-Adjusted Cost And Speed Eligibility

**Files:**
- Modify: `tools/databento/carver_s09_mes_runtime_risk_cost_input_lock.py`
- Modify: `tests/test_s09_mes_readiness_synthetic.py`

- [ ] **Step 1: Write the failing risk-adjusted cost and speed test**

The test must compute risk-adjusted cost only from locked total cost and locked daily price risk, then apply the S09 0.15 SR threshold against the locked turnover table.

- [ ] **Step 2: Run the focused test to verify it fails**

Run the single new readiness test with `unittest`.

- [ ] **Step 3: Emit the risk-adjusted cost ledger**

Emit:

```text
cost/<STAMP>_S09_MES_RISK_ADJUSTED_COST_ledger.csv
```

Required columns:

```text
completed_trading_date,total_cost_per_trade_currency,daily_price_risk_currency,risk_adjusted_cost_per_trade_sr,status
```

- [ ] **Step 4: Emit the speed eligibility ledger**

Emit:

```text
speed/<STAMP>_S09_MES_SPEED_ELIGIBILITY_ledger.csv
```

Required columns:

```text
span,turnover,risk_adjusted_cost_per_trade_sr,threshold_sr,eligible,status
```

No default all-six-speed assumption is allowed.

- [ ] **Step 5: Run focused tests**

Run:

```powershell
& 'C:\Users\openclaw\AppData\Local\Programs\Python\Python311\python.exe' -m unittest tests.test_s09_mes_readiness_synthetic
```

## Task 5: Strategy Input Readiness Packet

**Files:**
- Modify: `tools/databento/carver_s09_mes_runtime_risk_cost_input_lock.py`
- Modify: `tests/test_s09_mes_lineage_synthetic.py`
- Create: `docs/process/CARVER_S09_MES_RUNTIME_RISK_COST_INPUT_LOCK_RESULT_2026-06-03.md`
- Create: `docs/process/CARVER_S09_MES_RUNTIME_RISK_COST_INPUT_LOCK_LOCAL_HOSTILE_AUDIT_2026-06-03.md`

- [ ] **Step 1: Write the failing result-boundary test**

The test must assert the result doc contains `SOURCE_NATIVE_FUTURES`, `APPENDIX_C_174_006`, `2019-05-05 through 2020-04-05`, `oldest minimum machinery-development slice only`, `oldest authorized completed source-native data first`, the separately gated 3:3:4 TEST/VALIDATION/LOCKBOX boundary, and the full no-forecast/no-backtest boundary.

- [ ] **Step 2: Run the focused test to verify it fails**

Run the single new lineage test with `unittest`.

- [ ] **Step 3: Run authorized execution**

Run only after explicit operator authorization:

```powershell
& 'C:\Users\openclaw\AppData\Local\Programs\Python\Python311\python.exe' tools\databento\carver_s09_mes_runtime_risk_cost_input_lock.py
```

Expected output:

```text
S09_MES_RUNTIME_RISK_COST_INPUT_LOCK_RESULT_WRITTEN
```

- [ ] **Step 4: Run verification**

Run:

```powershell
& 'C:\Users\openclaw\AppData\Local\Programs\Python\Python311\python.exe' -m unittest tests.test_s09_mes_lineage_synthetic tests.test_s09_mes_readiness_synthetic tests.test_s09_full_source_atom_synthetic tests.test_s09_m2_synthetic tests.test_s09_phase1_synthetic tests.test_s09_readiness_synthetic tests.test_s09_zn_package_synthetic tests.test_continuous_synthetic
& 'C:\Users\openclaw\AppData\Local\Programs\Python\Python311\python.exe' -m py_compile src/carver/spine/s09_mes_readiness.py src/carver/spine/s09_mes_lineage.py src/carver/spine/__init__.py tools/databento/carver_s09_mes_runtime_risk_cost_input_lock.py tests/test_s09_mes_readiness_synthetic.py tests/test_s09_mes_lineage_synthetic.py
```

Expected:

```text
all S09 synthetic tests pass
py_compile exits 0
```

- [ ] **Step 5: Git operations**

Do not stage or commit. Git staging, commit, push, PR, and remote operations require separate explicit operator authorization.

## Self-Review

Spec coverage:

```text
source-native futures lane: covered
MES Appendix C row lock: covered
2019-05-05 through 2020-04-05 machinery-development slice: covered
3:3:4 TEST/VALIDATION/LOCKBOX windows separately locked and separately gated: covered
oldest authorized completed source-native data first: covered
runtime annual-risk value lock: covered
daily price-risk value lock: covered
historical MES cost value lock: covered
risk-adjusted cost lock: covered
speed eligibility lock: covered
no forecast/backtest/OOS/Lockbox/Forward/promotion/Git: covered
```

Placeholder scan:

```text
No placeholder markers are intentionally present.
```

Type consistency:

```text
The named execution script and config are introduced in Task 1, then consumed by later tasks.
```
