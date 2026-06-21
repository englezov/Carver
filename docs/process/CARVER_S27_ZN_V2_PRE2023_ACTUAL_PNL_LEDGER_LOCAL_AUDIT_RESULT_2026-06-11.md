# S27_V2 Pre-2023 Actual PnL Ledger Local Audit Result

Date: 2026-06-11

Status:

```text
LOCAL_HOSTILE_AUDIT_PASS_NO_P0_P1_P2_P3_FINDINGS
```

Scope:

```text
S27_V2_PRE2023_DEVELOPMENT_RECON_ACTUAL_PNL_LEDGER_IMPLEMENTATION_GATE
```

Audited artifacts:

```text
src/carver/spine/s27_v2_replay/pre2023_development_recon_actual_pnl.py
tests/test_s27_v2_pre2023_actual_pnl.py
docs/process/CARVER_S27_ZN_V2_PRE2023_ACTUAL_PNL_LEDGER_IMPLEMENTATION_2026-06-11.md
docs/researchops/s27_v2_local_replay_runs/ZN/20260611_pre2023_oldest_dev_recon_2022_actual_pnl_completion
docs/researchops/s27_v2_local_replay_runs/ZN/20260611_pre2023_oldest_dev_recon_2022_controlled_run
docs/researchops/s27_v2_local_replay_inputs/ZN/20260611_pre2023_dev_recon_valuation_mark_znh2_20220103T03_declared_pack
```

Audit result:

```text
PASS
```

Findings:

```text
P0: none
P1: none
P2: none
P3: none
```

Confirmed facts:

```text
raw_symbol = ZNH2
filled_order_side = BUY
fill_quantity = 8
fill_timestamp_utc = 2022-01-03T02:00:00Z
valuation_mark_completed_timestamp_utc = 2022-01-03T03:00:00Z
fill_price = 130.421875
valuation_mark_close_price = 130.296875
contract_point_value = 1000.0 USD
gross_pnl_amount = -1000.0 USD
commission_cost_amount = 18.4 USD
spread_cost_amount = 0.0 USD
net_pnl_amount = -1018.4 USD
```

The local hostile audit confirmed active controlled-run bundle binding, fill,
commission, spread, valuation mark manifest, valuation mark CSV, valuation mark
local-audit record, and source-line hash binding. It also confirmed the
mechanical long-position mark-to-market arithmetic:

```text
(130.296875 - 130.421875) * 8 * 1000 = -1000.0
-1000.0 - 18.4 - 0.0 = -1018.4
```

The audit confirmed standalone row validation is not authoritative, forged row
and forged bundle cases are covered, package-root export remains closed, and
result/backtest/PnL-evaluation/source-faithful evidence gates remain
false/fail-closed.

Verification before audit:

```text
python -m py_compile src\carver\spine\s27_v2_replay\pre2023_development_recon_actual_pnl.py
python -m pytest tests\test_s27_v2_pre2023_actual_pnl.py tests\test_s27_v2_pre2023_valuation_mark_pack.py tests\test_s27_v2_development_recon_run.py -q
72 passed
```

Non-authorizations preserved:

```text
NO_PROVIDER_API
NO_DOWNLOADS
NO_NEW_DATA_ACQUISITION
NO_TEST_ACCESS
NO_VALIDATION_ACCESS
NO_OOS
NO_LOCKBOX
NO_FORWARD
NO_RESULT_SCORED_RUN
NO_RESULT_INTERPRETATION
NO_PNL_EVALUATION_BEYOND_MECHANICAL_ROW_CONSTRUCTION
NO_TUNING
NO_ADAPTER_WORK
NO_DEPLOYMENT
NO_TRADING
NO_PROMOTION
NO_GIT_ACTIONS
NO_SOURCE_FAITHFUL_EVIDENCE_CLAIM
```

Next gate:

```text
S27_V2_PRE2023_DEVELOPMENT_RECON_EXTERNAL_HOSTILE_AUDIT_PACKET_OR_BACKTEST_READINESS_CLOSURE_GATE
```

This audit does not authorize provider/API access, downloads, new data
acquisition, TEST, VALIDATION, OOS, Lockbox, Forward, result interpretation,
PnL evaluation beyond mechanical row construction, tuning, adapter work,
deployment, trading, promotion, Git actions, or source-faithful evidence
claims.
