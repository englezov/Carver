# S09 MES Roll Risk Cost Execution Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** After explicit operator authorization, execute the bounded S09 MES source-native Development/Reconciliation roll-date normalization and runtime risk/cost gate without opening forecasts, diagnostics, backtests, OOS, Lockbox, Forward, deployment, trading, promotion, or Git operations.

**Architecture:** Implement a single fail-closed execution script that consumes only the authorized S09/MES local artifacts and any operator-restated static/provider evidence. Keep transformation logic in small `carver.spine` helpers with synthetic tests before execution. Emit CSV/JSON/Markdown/SHA256 artifacts under the existing S09/MES researchops root and preserve automatic local hostile audit evidence.

**Tech Stack:** Python 3.11 standard library, `unittest`, existing `carver.spine` helpers, local CSV/JSON/Markdown artifacts, PowerShell invocation from `C:\Users\openclaw\Desktop\Carver`.

---

## Scope Lock

This plan is not authorization and must not be executed until the operator explicitly authorizes:

```text
Operator authorizes one bounded S09 MES source-native Development/Reconciliation roll-date normalization and runtime risk/cost execution gate.
```

The implementation is locked to:

```text
gate: S09_MES_ROLL_DATE_NORMALIZATION_AND_RUNTIME_RISK_COST_EXECUTION_GATE
lane_class: SOURCE_NATIVE_FUTURES
source_row: APPENDIX_C_174_006
author_market_code: MES
target_window: 2022-01-03 through 2023-12-29
design_ordering: oldest authorized completed source-native data first
```

No Databento API access unless explicitly restated by the operator. No forecast computation, diagnostics, backtests, OOS, Lockbox, Forward, deployment, trading, promotion, Git staging, commit, push, PR, or remote operations.

## Files

Create:

```text
tools/databento/carver_s09_mes_roll_risk_cost_execution.py
docs/process/CARVER_S09_MES_ROLL_DATE_NORMALIZATION_RUNTIME_RISK_COST_EXECUTION_RESULT_2026-06-03.md
docs/process/CARVER_S09_MES_ROLL_DATE_NORMALIZATION_RUNTIME_RISK_COST_EXECUTION_LOCAL_HOSTILE_AUDIT_2026-06-03.md
```

Modify:

```text
src/carver/spine/s09_mes_lineage.py
src/carver/spine/s09_mes_readiness.py
src/carver/spine/__init__.py
tests/test_s09_mes_lineage_synthetic.py
tests/test_s09_mes_readiness_synthetic.py
```

Expected output root after authorized execution:

```text
docs/researchops/s09/mes_roll_date_normalization_runtime_risk_cost_execution/2022-01-03_2023-12-29/
```

Expected output families:

```text
roll_date_normalization/<STAMP>_S09_MES_ROLL_DATE_NORMALIZATION_ledger.csv
risk/<STAMP>_S09_MES_ANNUAL_RISK_RUNTIME_ledger.csv
risk/<STAMP>_S09_MES_DAILY_PRICE_RISK_RUNTIME_ledger.csv
cost/<STAMP>_S09_MES_COST_VALUE_ledger.csv
cost/<STAMP>_S09_MES_RISK_ADJUSTED_COST_ledger.csv
speed/<STAMP>_S09_MES_SPEED_ELIGIBILITY_ledger.csv
status/<STAMP>_S09_MES_ROLL_RISK_COST_EXECUTION_status.json
provenance/<STAMP>_S09_MES_ROLL_RISK_COST_EXECUTION_provenance.md
hashes/<STAMP>_S09_MES_ROLL_RISK_COST_EXECUTION_sha256.txt
```

### Task 1: Authorization And Input Hash Preflight

**Files:**
- Modify: `tests/test_s09_mes_lineage_synthetic.py`
- Create: `tools/databento/carver_s09_mes_roll_risk_cost_execution.py`

- [x] **Step 1: Write the failing test**

Add this test to `tests/test_s09_mes_lineage_synthetic.py`:

```python
def test_s09_mes_roll_risk_cost_execution_requires_explicit_authorization(self) -> None:
    from tools.databento.carver_s09_mes_roll_risk_cost_execution import (  # noqa: PLC0415
        S09MESRollRiskCostExecutionConfig,
        run_s09_mes_roll_risk_cost_execution,
    )

    config = S09MESRollRiskCostExecutionConfig(
        execution_authorized=False,
        lane_class="SOURCE_NATIVE_FUTURES",
        root="MES",
        row_id="APPENDIX_C_174_006",
        target_start="2022-01-03",
        target_end="2023-12-29",
    )

    with self.assertRaises(CarverBlocked):
        run_s09_mes_roll_risk_cost_execution(config)
```

- [x] **Step 2: Run test to verify it fails**

Run:

```powershell
& 'C:\Users\openclaw\AppData\Local\Programs\Python\Python311\python.exe' -m unittest tests.test_s09_mes_lineage_synthetic.S09MESLineageSyntheticTests.test_s09_mes_roll_risk_cost_execution_requires_explicit_authorization
```

Expected:

```text
ImportError: No module named 'tools.databento.carver_s09_mes_roll_risk_cost_execution'
FAILED
```

- [x] **Step 3: Write minimal implementation**

Create `tools/databento/carver_s09_mes_roll_risk_cost_execution.py` with:

```python
from __future__ import annotations

from dataclasses import dataclass

from carver.spine.m0 import CarverBlocked


@dataclass(frozen=True)
class S09MESRollRiskCostExecutionConfig:
    execution_authorized: bool
    lane_class: str
    root: str
    row_id: str
    target_start: str
    target_end: str


def run_s09_mes_roll_risk_cost_execution(config: S09MESRollRiskCostExecutionConfig) -> dict[str, str]:
    if not config.execution_authorized:
        raise CarverBlocked("S09 MES roll risk cost execution is not operator-authorized")
    if config.lane_class != "SOURCE_NATIVE_FUTURES":
        raise CarverBlocked("S09 MES execution is source-native futures only")
    if config.root != "MES" or config.row_id != "APPENDIX_C_174_006":
        raise CarverBlocked("S09 MES execution is locked to Appendix C MES row")
    if config.target_start != "2022-01-03" or config.target_end != "2023-12-29":
        raise CarverBlocked("S09 MES execution target window is not locked")
    return {"status": "AUTHORIZED_PREFLIGHT_ONLY_NOT_EXECUTED"}
```

- [x] **Step 4: Run test to verify it passes**

Run the same command. Expected:

```text
Ran 1 test
OK
```

- [x] **Step 5: Git operations**

Do not stage or commit. Carver forbids Git staging, commit, push, PR, and remote operations unless separately authorized.

### Task 2: Roll Date Normalization Ledger

**Files:**
- Modify: `src/carver/spine/s09_mes_lineage.py`
- Modify: `tests/test_s09_mes_lineage_synthetic.py`
- Modify: `tools/databento/carver_s09_mes_roll_risk_cost_execution.py`

- [x] **Step 1: Write the failing test**

Add this test:

```python
def test_s09_mes_roll_normalization_execution_outputs_hash_bound_completed_dates(self) -> None:
    from carver.spine import (  # noqa: PLC0415
        S09MESRollDateNormalizationAuthority,
        normalize_s09_mes_roll_provider_date,
    )

    result = normalize_s09_mes_roll_provider_date(
        provider_date=date(2022, 3, 13),
        authority_rows=(
            S09MESRollDateNormalizationAuthority(
                provider_date=date(2022, 3, 13),
                completed_trading_date=date(2022, 3, 14),
                authority_source="AUTHORIZED_CME_COMPLETED_TRADING_DAY_AUTHORITY",
                authority_sha256="A" * 64,
            ),
        ),
    )

    self.assertEqual(result, date(2022, 3, 14))
```

- [x] **Step 2: Run test to verify it passes against existing helper**

Run:

```powershell
& 'C:\Users\openclaw\AppData\Local\Programs\Python\Python311\python.exe' -m unittest tests.test_s09_mes_lineage_synthetic.S09MESLineageSyntheticTests.test_s09_mes_roll_normalization_execution_outputs_hash_bound_completed_dates
```

Expected:

```text
Ran 1 test
OK
```

- [x] **Step 3: Extend execution script output contract**

Update the execution script so the authorized path writes:

```text
roll_date_normalization/<STAMP>_S09_MES_ROLL_DATE_NORMALIZATION_ledger.csv
```

Required CSV columns:

```text
provider_date,completed_trading_date,old_symbol,new_symbol,authority_source,authority_sha256,status
```

Required row status:

```text
LOCKED_SOURCE_NATIVE_COMPLETED_TRADING_DATE
```

Unauthorised implementation note: current work adds the synthetic renderer contract
`render_s09_mes_roll_normalization_ledger_csv`; no real execution-path file write has
been run.

- [x] **Step 4: Run focused tests**

Run:

```powershell
& 'C:\Users\openclaw\AppData\Local\Programs\Python\Python311\python.exe' -m unittest tests.test_s09_mes_lineage_synthetic
```

Expected:

```text
OK
```

- [x] **Step 5: Git operations**

Do not stage or commit.

### Task 3: Annual And Daily Price Risk Runtime Ledgers

**Files:**
- Modify: `tests/test_s09_mes_readiness_synthetic.py`
- Modify: `tools/databento/carver_s09_mes_roll_risk_cost_execution.py`

- [x] **Step 1: Write the failing test**

Add this test:

```python
def test_mes_runtime_risk_values_require_same_completed_bar_timestamp(self) -> None:
    annual = s09_mes_annual_risk_from_locked_components(
        S09MESAnnualRiskBlendRequest(
            lane_class=LaneClass.SOURCE_NATIVE_FUTURES,
            completed_bar=self.completed_bar,
            long_run_annual_risk=TimedValue(0.20, self.as_of),
            long_run_status=SourceRuleStatus.LOCKED,
            current_ewma32_annual_risk=TimedValue(0.10, self.as_of),
            current_risk_status=SourceRuleStatus.LOCKED,
            blend_status=SourceRuleStatus.LOCKED,
        )
    )
    daily = s09_mes_daily_price_risk_from_locked_inputs(
        S09MESDailyPriceRiskRequest(
            lane_class=LaneClass.SOURCE_NATIVE_FUTURES,
            completed_bar=self.completed_bar,
            current_price=TimedValue(4000.0, self.as_of),
            current_price_status=SourceRuleStatus.LOCKED,
            annual_percentage_risk=TimedValue(annual.annual_percentage_risk, self.as_of),
            annual_risk_runtime_status=SourceRuleStatus.LOCKED,
            conversion_source_status=SourceRuleStatus.LOCKED,
        )
    )
    self.assertEqual(daily.daily_price_risk_currency, 32.5)
```

- [x] **Step 2: Run test**

Run:

```powershell
& 'C:\Users\openclaw\AppData\Local\Programs\Python\Python311\python.exe' -m unittest tests.test_s09_mes_readiness_synthetic.S09MESReadinessSyntheticTests.test_mes_runtime_risk_values_require_same_completed_bar_timestamp
```

Expected:

```text
Ran 1 test
OK
```

- [x] **Step 3: Extend execution script output contract**

Write:

```text
risk/<STAMP>_S09_MES_ANNUAL_RISK_RUNTIME_ledger.csv
risk/<STAMP>_S09_MES_DAILY_PRICE_RISK_RUNTIME_ledger.csv
```

Annual-risk required columns:

```text
completed_trading_date,long_run_annual_risk,current_ewma32_annual_risk,annual_percentage_risk,source_sha256,status
```

Daily price-risk required columns:

```text
completed_trading_date,current_price,annual_percentage_risk,daily_price_risk_currency,source_sha256,status
```

Unauthorised implementation note: current work adds synthetic renderer contracts
`render_s09_mes_annual_risk_runtime_ledger_csv` and
`render_s09_mes_daily_price_risk_runtime_ledger_csv`; no real runtime-risk
execution-path file write has been run.

- [x] **Step 4: Run focused tests**

Run:

```powershell
& 'C:\Users\openclaw\AppData\Local\Programs\Python\Python311\python.exe' -m unittest tests.test_s09_mes_readiness_synthetic
```

Expected:

```text
OK
```

- [x] **Step 5: Git operations**

Do not stage or commit.

### Task 4: Historical MES Cost And Risk-Adjusted Cost Ledgers

**Files:**
- Modify: `tests/test_s09_mes_readiness_synthetic.py`
- Modify: `tools/databento/carver_s09_mes_roll_risk_cost_execution.py`

- [x] **Step 1: Write the failing test**

Add this test:

```python
def test_mes_cost_and_risk_adjusted_cost_ledgers_use_locked_components_only(self) -> None:
    cost = s09_mes_total_cost_from_locked_components(self.locked_cost_request())
    risk_adjusted = s09_mes_risk_adjusted_cost_from_locked_inputs(
        S09MESRiskAdjustedCostRequest(
            lane_class=LaneClass.SOURCE_NATIVE_FUTURES,
            total_cost_per_trade_currency=cost.total_cost_per_trade_currency,
            total_cost_status=SourceRuleStatus.LOCKED,
            daily_price_risk_currency=500.0,
            daily_price_risk_status=SourceRuleStatus.LOCKED,
        )
    )
    self.assertAlmostEqual(risk_adjusted.risk_adjusted_cost_per_trade_sr, 0.00598)
```

- [x] **Step 2: Run test**

Run:

```powershell
& 'C:\Users\openclaw\AppData\Local\Programs\Python\Python311\python.exe' -m unittest tests.test_s09_mes_readiness_synthetic.S09MESReadinessSyntheticTests.test_mes_cost_and_risk_adjusted_cost_ledgers_use_locked_components_only
```

Expected:

```text
Ran 1 test
OK
```

- [x] **Step 3: Extend execution script output contract**

Write:

```text
cost/<STAMP>_S09_MES_COST_VALUE_ledger.csv
cost/<STAMP>_S09_MES_RISK_ADJUSTED_COST_ledger.csv
```

Cost ledger required columns:

```text
completed_trading_date,component_name,amount_currency,currency,charge_timing,effective_start,effective_end,source_label,source_sha256,status
```

Risk-adjusted ledger required columns:

```text
completed_trading_date,total_cost_per_trade_currency,daily_price_risk_currency,risk_adjusted_cost_per_trade_sr,status
```

Unauthorised implementation note: current work adds synthetic renderer contracts
`render_s09_mes_cost_value_ledger_csv` and
`render_s09_mes_risk_adjusted_cost_ledger_csv`; no real cost extraction or
execution-path file write has been run.

- [x] **Step 4: Run focused tests**

Run:

```powershell
& 'C:\Users\openclaw\AppData\Local\Programs\Python\Python311\python.exe' -m unittest tests.test_s09_mes_readiness_synthetic
```

Expected:

```text
OK
```

- [x] **Step 5: Git operations**

Do not stage or commit.

### Task 5: Speed Eligibility And Readiness Status

**Files:**
- Modify: `tests/test_s09_mes_readiness_synthetic.py`
- Modify: `tools/databento/carver_s09_mes_roll_risk_cost_execution.py`

- [x] **Step 1: Write the failing test**

Add this test:

```python
def test_mes_speed_eligibility_status_can_feed_readiness_only_after_locks(self) -> None:
    speed = s09_mes_speed_eligibility_from_risk_adjusted_cost(
        S09MESRiskAdjustedCostSpeedEligibilityRequest(
            lane_class=LaneClass.SOURCE_NATIVE_FUTURES,
            risk_adjusted_cost_per_trade_sr=0.006,
            risk_adjusted_cost_status=SourceRuleStatus.LOCKED,
            threshold_sr=0.15,
            threshold_status=SourceRuleStatus.LOCKED,
            turnover_status=SourceRuleStatus.LOCKED,
        )
    )
    ready = evaluate_s09_mes_strategy_input_readiness(
        replace(
            self.locked_request(),
            eligible_spans=speed.eligible_spans,
            fdm=speed.fdm,
            speed_eligibility_basis=speed.eligibility_basis,
        )
    )
    self.assertTrue(ready.ready)
```

- [x] **Step 2: Run test**

Run:

```powershell
& 'C:\Users\openclaw\AppData\Local\Programs\Python\Python311\python.exe' -m unittest tests.test_s09_mes_readiness_synthetic.S09MESReadinessSyntheticTests.test_mes_speed_eligibility_status_can_feed_readiness_only_after_locks
```

Expected:

```text
Ran 1 test
OK
```

- [x] **Step 3: Extend execution script output contract**

Write:

```text
speed/<STAMP>_S09_MES_SPEED_ELIGIBILITY_ledger.csv
status/<STAMP>_S09_MES_ROLL_RISK_COST_EXECUTION_status.json
```

Speed ledger required columns:

```text
span,turnover,risk_adjusted_cost_per_trade_sr,threshold_sr,eligible,status
```

Status JSON must contain exactly one of:

```text
READY_FOR_S09_MES_DEV_RECON_FORECAST_INPUT_GATE_NOT_BACKTEST
FAIL_CLOSED_S09_MES_STRATEGY_INPUT_NOT_READY
```

Unauthorised implementation note: current work adds synthetic renderer contracts
`render_s09_mes_speed_eligibility_ledger_csv` and
`render_s09_mes_roll_risk_cost_execution_status_json`; no real speed-eligibility
execution or execution-path file write has been run.

- [x] **Step 4: Run focused tests**

Run:

```powershell
& 'C:\Users\openclaw\AppData\Local\Programs\Python\Python311\python.exe' -m unittest tests.test_s09_mes_readiness_synthetic
```

Expected:

```text
OK
```

- [x] **Step 5: Git operations**

Do not stage or commit.

### Task 6: Automatic Local Hostile Audit And Verification

**Files:**
- Modify: `tests/test_s09_mes_lineage_synthetic.py`
- Create: `docs/process/CARVER_S09_MES_ROLL_DATE_NORMALIZATION_RUNTIME_RISK_COST_EXECUTION_RESULT_2026-06-03.md`
- Create: `docs/process/CARVER_S09_MES_ROLL_DATE_NORMALIZATION_RUNTIME_RISK_COST_EXECUTION_LOCAL_HOSTILE_AUDIT_2026-06-03.md`

- [x] **Step 1: Write the failing test**

Add this test:

```python
def test_s09_mes_roll_risk_cost_execution_result_preserves_no_backtest_boundary(self) -> None:
    result_path = (
        ROOT
        / "docs"
        / "process"
        / "CARVER_S09_MES_ROLL_DATE_NORMALIZATION_RUNTIME_RISK_COST_EXECUTION_RESULT_2026-06-03.md"
    )
    text = result_path.read_text(encoding="utf-8")

    self.assertIn("SOURCE_NATIVE_FUTURES", text)
    self.assertIn("APPENDIX_C_174_006", text)
    self.assertIn("2022-01-03 through 2023-12-29", text)
    self.assertIn("oldest authorized completed source-native data first", text)
    self.assertIn("no forecast computation", text)
    self.assertIn("no diagnostics", text)
    self.assertIn("no backtests", text)
    self.assertIn("no OOS", text)
    self.assertIn("no Lockbox", text)
    self.assertIn("no Forward", text)
```

- [x] **Step 2: Run test to verify it fails before the result exists**

Run:

```powershell
& 'C:\Users\openclaw\AppData\Local\Programs\Python\Python311\python.exe' -m unittest tests.test_s09_mes_lineage_synthetic.S09MESLineageSyntheticTests.test_s09_mes_roll_risk_cost_execution_result_preserves_no_backtest_boundary
```

Expected:

```text
FileNotFoundError
FAILED
```

- [x] **Step 3: Run authorized execution script**

Run only after explicit authorization:

```powershell
& 'C:\Users\openclaw\AppData\Local\Programs\Python\Python311\python.exe' tools/databento/carver_s09_mes_roll_risk_cost_execution.py
```

Expected output:

```text
S09_MES_ROLL_DATE_NORMALIZATION_RUNTIME_RISK_COST_EXECUTION_RESULT_WRITTEN
```

Execution note: operator authorized the bounded execution step on 2026-06-03.
The script emitted a fail-closed execution packet because required executable
runtime annual-risk, daily price-risk, historical cost, risk-adjusted cost, and
speed eligibility values were not all locked as strategy-input values. It did
not call Databento, download data, parse new market rows, compute forecasts,
run diagnostics, run backtests, access TEST/VALIDATION/OOS/Lockbox/Forward, or
perform Git operations.

- [x] **Step 4: Run verification**

Run:

```powershell
& 'C:\Users\openclaw\AppData\Local\Programs\Python\Python311\python.exe' -m unittest tests.test_s09_mes_lineage_synthetic tests.test_s09_mes_readiness_synthetic tests.test_s09_full_source_atom_synthetic tests.test_s09_m2_synthetic tests.test_s09_phase1_synthetic tests.test_s09_readiness_synthetic tests.test_s09_zn_package_synthetic tests.test_continuous_synthetic
& 'C:\Users\openclaw\AppData\Local\Programs\Python\Python311\python.exe' -m py_compile src/carver/spine/s09_mes_readiness.py src/carver/spine/s09_mes_lineage.py src/carver/spine/__init__.py tools/databento/carver_s09_mes_roll_risk_cost_execution.py tests/test_s09_mes_readiness_synthetic.py tests/test_s09_mes_lineage_synthetic.py
```

Expected:

```text
all S09 synthetic tests pass
py_compile exits 0
```

- [x] **Step 5: Git operations**

Do not stage or commit. Git staging, commit, push, PR, and remote operations require separate explicit operator authorization.

No Git staging, commit, push, PR, or remote operation was performed.

## Self-Review

Spec coverage:

```text
source-native futures lane: covered
MES Appendix C row lock: covered
2022-01-03 through 2023-12-29 Development/Reconciliation window: covered
oldest authorized completed source-native data first: covered
roll date normalization ledger: covered
annual-risk runtime ledger: covered
daily price-risk runtime ledger: covered
historical cost value ledger: covered
risk-adjusted cost ledger: covered
speed eligibility ledger: covered
no forecast/backtest/OOS/Lockbox/Forward/promotion/Git: covered
```

Placeholder scan:

```text
No placeholder markers are intentionally present.
```

Type consistency:

```text
All named helpers already exist except the explicitly planned authorized execution script and its config dataclass.
```
