# S27_V2 Pre-2023 Valuation Mark Declared Pack Local Audit Result

Date: 2026-06-11

Status:

```text
LOCAL_HOSTILE_AUDIT_PASS_NO_P0_P1_P2_P3_FINDINGS
```

Scope:

```text
S27_V2_PRE2023_DEVELOPMENT_RECON_POST_FILL_VALUATION_MARK_ROW_DECLARATION_GATE
```

Audited artifacts:

```text
tools/databento/carver_s27_v2_pre2023_valuation_mark_pack.py
tests/test_s27_v2_pre2023_valuation_mark_pack.py
docs/researchops/s27_v2_local_replay_inputs/ZN/20260611_pre2023_dev_recon_valuation_mark_znh2_20220103T03_declared_pack
docs/process/CARVER_S27_ZN_V2_PRE2023_VALUATION_MARK_DECLARED_PACK_RECORD_2026-06-11.md
docs/researchops/s27_v2_local_replay_runs/ZN/20260611_pre2023_oldest_dev_recon_2022_controlled_run
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
fill_timestamp_utc = 2022-01-03T02:00:00Z
valuation_mark_completed_timestamp_utc = 2022-01-03T03:00:00Z
raw_symbol = ZNH2
close_price = 130.296875
strategy_facing_hourly_available_bars_line = 4
raw_provider_hourly_csv_line = 27
valuation_convention_label = SOURCE_NATIVE_ENGINEERING_VALUATION_ASSUMPTION_NOT_BOOK_EXPLICIT
```

The audit confirmed that the selected mark row is the exact next completed
local `ZNH2` hourly row strictly after the controlled-run fill timestamp. The
strategy-facing ledger row, raw provider row, selected line numbers, selected
line hashes, file hashes, and canonical row hashes are bound in the declared
pack manifest.

The audit also confirmed that the declared pack is local-only, pre-2023, and
does not emit PnL, result rows, backtest evidence, result interpretation, PnL
evaluation, promotion evidence, trading evidence, or source-faithful evidence
claims.

Verification run before audit:

```text
python -m py_compile tools\databento\carver_s27_v2_pre2023_valuation_mark_pack.py
python -m pytest tests\test_s27_v2_pre2023_valuation_mark_pack.py tests\test_s27_v2_development_recon_run.py -q
21 passed
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
NO_RESULT_INTERPRETATION
NO_PNL_EVALUATION
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
S27_V2_PRE2023_DEVELOPMENT_RECON_ACTUAL_PNL_LEDGER_IMPLEMENTATION_GATE
```

The next gate requires separate operator authorization. This audit does not
authorize provider/API access, downloads, new data acquisition, TEST,
VALIDATION, OOS, Lockbox, Forward, result interpretation, PnL evaluation beyond
future mechanical row construction, tuning, adapter work, deployment, trading,
promotion, Git actions, or source-faithful evidence claims.
