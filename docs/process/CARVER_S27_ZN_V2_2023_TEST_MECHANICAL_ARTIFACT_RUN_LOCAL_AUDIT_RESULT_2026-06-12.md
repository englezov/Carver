# S27_V2 2023 TEST Mechanical Artifact Run Local Audit Result

Date: 2026-06-12

Status:

```text
LOCAL_GPT55_P1_REMEDIATED_PASS_PENDING_EXTERNAL_REAUDIT_NOT_RESULT_NOT_SOURCE_FAITHFUL_EVIDENCE
```

## Scope

Authorized gate:

```text
S27_V2_CONTROLLED_LOCAL_ONLY_2023_TEST_INPUT_PACK_AND_MECHANICAL_ARTIFACT_RUN_GATE
```

This gate built and ran a controlled local-only mechanical TEST artifact surface for S27_V2 ZN using already-local 2023 source-native ZN files and pre-2023 strict-prior warmup/evidence. It did not authorize provider/API access, downloads, new data acquisition, VALIDATION, OOS, Lockbox, Forward, result interpretation, PnL evaluation beyond mechanical row construction, tuning, adapter work, deployment, trading, promotion, Git actions, or source-faithful evidence claims.

## Artifacts

Declared 2023 TEST input pack:

```text
docs/researchops/s27_v2_local_replay_inputs/ZN/20260612_2023_test_declared_pack
```

Input manifest SHA256:

```text
838D360BCBA75F9076791B226AAB188DC87FD7D68A84D038C5F17B96A816FD59
```

Mechanical TEST artifact run:

```text
docs/researchops/s27_v2_local_replay_runs/ZN/20260612_2023_test_mechanical_artifact_run
```

Run manifest SHA256:

```text
6C0A588272742BD3B5DDAD8465B6ED585F1FD7EB18188DFF4ECF3CE7D59671BB
```

Evidence manifest SHA256:

```text
171361FEA2E225551F892ECAAADEBDB97596D49639900A7325276C2ABD64CA81
```

Trusted bundle SHA256:

```text
DE4A867D96354C16DFCE2D723A46235AE905E2FABFA4A7720EFC3D8ECA9AFC29
```

## Mechanical TEST Boundary

The declared pack now selects one candidate TEST row and fails closed immediately before any supported mechanical ledger row:

- start: `2023-01-03T00:00:00Z`
- fail-closed row: `1`
- fail-closed timestamp: `2023-01-03T00:00:00Z`
- supported mechanical rows: `0`

The run fails closed at row `1`:

```text
FAIL_CLOSED_BOOK_REQUIRED_MARKET_ORDER_FOR_TARGET_GAP_GT_ONE_NOT_AUTHORIZED_NOT_RESULT
```

The blocker row is a `ZNH3` `BUY` transition from starting position `0` to desired position `2`, with position change `2` and adjacent target `1`. Under the source-lock, target-position gaps greater than one contract are market-order cases before adjacent-limit execution can be treated as operative. Because market-order implementation is not authorized in this TEST artifact run, row `1` is emitted only in `fail_closed_ledger.csv`; all supported mechanical ledgers are header-only with zero rows.

## Verification

Focused verification passed:

```text
python -m py_compile src\carver\spine\s27_v2_replay\test_mechanical_run.py tests\test_s27_v2_2023_test_mechanical_run.py
python -m pytest tests\test_s27_v2_2023_test_mechanical_run.py -q
```

Result:

```text
20 passed
```

Compatibility verification passed:

```text
python -m pytest tests\test_s27_v2_pretest_development_recon_completion.py tests\test_s27_v2_2023_test_mechanical_run.py -q
```

Result:

```text
81 passed
```

Supported ledgers are now bounded strictly to row `302`:

- `runtime_history_ledger.csv`
- `forecast_replay_ledger.csv`
- `desired_position_ledger.csv`
- `limit_order_ledger.csv`
- `fill_ledger.csv`
- `cost_ledger.csv`
- `pnl_ledger.csv`

After GPT P1 remediation, supported ledgers are header-only with zero rows:

- `runtime_history_ledger.csv`
- `forecast_replay_ledger.csv`
- `desired_position_ledger.csv`
- `limit_order_ledger.csv`
- `no_market_order_ledger.csv`
- `working_order_transition_ledger.csv`
- `fill_ledger.csv`
- `cost_ledger.csv`
- `pnl_ledger.csv`
- `validation_ledger.csv`

`fail_closed_ledger.csv` has exactly one row, row `1`.

## Local Hostile Audit

Two read-only subagent audits and one narrow re-audit were run.

Initial code/runner audit found one P2:

```text
P2: row 303 leaked into runtime, forecast, and desired-position supported ledgers before fail-closed break.
```

Patch:

- removed row `303` from supported runtime, forecast, and position ledgers;
- kept row `303` only in `fail_closed_ledger.csv`.

Initial narrow re-audit found one P2:

```text
P2: tests did not directly assert all supported ledger families, including cost/order/fill/PnL, stop at row 302 and exclude row 303.
```

Patch:

- added direct regression coverage for runtime, forecast, position, order, fill, cost, and PnL supported ledgers;
- asserted every supported family ends at row `302` and contains no row `303`.

Final narrow re-audit returned:

```text
PASS
P0: None
P1: None
P2: None
```

Independent artifact audit also returned PASS, confirming protected-window exclusions, strict-prior pre-2023 warmup/evidence, hash binding, and fail-closed row `303`.

## GPT P1 Remediation

GPT 5.5 external audit returned `FAIL`, with one P1:

```text
P1-01: row 303 fail-closed reason was not source-valid as the sole blocker because the row also had a two-contract target-position gap, which is a book/source-lock market-order case.
```

Patch:

- market-order-required target gaps (`abs(position_change_contracts) > 1`) are now classified before adjacent-limit formula/fill/session logic;
- the 2023 TEST mechanical artifact now fails closed at the first 2023 TEST row, row `1`;
- row `1` records `market_order_required = TRUE`, `market_order_rows_emitted = FALSE`, and `market_order_reason = BOOK_REQUIRED_TARGET_POSITION_GAP_GREATER_THAN_ONE_CONTRACT`;
- adjacent-limit/session evaluation is not used as the primary blocker for row `1`;
- supported ledgers are header-only zero-row files and are directly byte-checkable in the audit packet.

Focused verification after remediation:

```text
python -m pytest tests\test_s27_v2_2023_test_mechanical_run.py -q
```

Result:

```text
20 passed
```

Compatibility verification after remediation:

```text
python -m pytest tests\test_s27_v2_pretest_development_recon_completion.py tests\test_s27_v2_2023_test_mechanical_run.py -q
```

Result:

```text
81 passed
```

Local read-only hostile re-audit after remediation returned:

```text
PASS
P0: None
P1: None
P2: None
```

Independent artifact-byte audit after remediation returned:

```text
PASS
P0: None
P1: None
P2: None
```

## Non-Authorization

This record does not authorize result interpretation, PnL evaluation beyond mechanical row construction, source-faithful evidence claims, TEST promotion, VALIDATION, OOS, Lockbox, Forward, provider/API access, downloads, new data acquisition, tuning, adapter work, deployment, trading, Git actions, or promotion.

Next useful gate:

```text
GPT_5_5_EXTENDED_PRO_EXTERNAL_REAUDIT_OF_2023_TEST_MARKET_ORDER_FAIL_CLOSED_REMEDIATION
```
