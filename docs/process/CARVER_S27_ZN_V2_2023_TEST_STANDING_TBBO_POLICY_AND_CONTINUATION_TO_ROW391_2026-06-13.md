# S27 V2 ZN 2023 TEST Standing TBBO Policy And Continuation To Row 391

Date: 2026-06-13

Status:

```text
LOCAL_PASS_2023_TEST_STANDING_TBBO_BATCH_AND_CONTINUATION_TO_ROW391_SESSION_EOD_BLOCKER_NOT_RESULT
```

Supersession note:

```text
SUPERSEDED_FOR_CURRENT_ROW391_STATUS_BY_CARVER_S27_ZN_V2_2023_TEST_ROW391_SESSION_END_MARKET_ORDER_IMPLEMENTATION_AND_LOCAL_AUDIT_2026-06-13
```

This record remains the historical standing-TBBO evidence record that led to
the row-391 blocker. The current post-implementation run state is recorded in
`docs/process/CARVER_S27_ZN_V2_2023_TEST_ROW391_SESSION_END_MARKET_ORDER_IMPLEMENTATION_AND_LOCAL_AUDIT_2026-06-13.md`.

## Scope

This record covers the operator-authorized standing bounded market-order TBBO spread evidence policy and the controlled local-only 2023 TEST mechanical continuation after the row-346 target-position-zero checkpoint.

The standing policy authorized bounded DataBento/provider access only for market-order rows already listed by the active local TEST runner requirements ledger. It did not authorize broad provider/API access, general historical downloads, VALIDATION, OOS, Lockbox, Forward, result interpretation, PnL evaluation beyond mechanical construction, tuning, adapter/deployment/trading/promotion, Git actions, GPT packet preparation, or source-faithful evidence claims.

## TBBO Requirements Discovery

The TEST market-order TBBO requirements discovery was patched so already-bound evidence is derived from the active combined TBBO registry, not only from the original row-1/row-2 prebound dictionary.

After the standing batch and retry, the active requirements manifest reports:

```text
total_market_order_rows = 85
already_bound_tbbo_count = 85
missing_tbbo_requirement_count = 0
terminal_status = STOPPED_ON_NEW_BLOCKER_CLASS_SECONDARY_FILLED_ORDER_ACROSS_UNRESOLVED_SESSION_EOD_GAP_NOT_RESULT
requirements_ledger_sha256 = B333FCCF77055AF25D2B0C0AF1BE50D1E52A4D2DF221FA0E715A87A832020F9D
```

Requirements ledger:

```text
docs/researchops/s27_v2_market_spread_evidence/ZN/20260612_2023_test_market_order_tbbo_requirements_discovery/market_order_tbbo_requirements.csv
```

## Standing TBBO Evidence

The first standing batch requested only the 33 rows still missing TBBO evidence after the prior combined registry.

```text
status = FAIL_CLOSED_STANDING_BOUNDED_DATABENTO_TBBO_BATCH_INCOMPLETE_NOT_RESULT
requirements_count = 33
selected_row_count = 26
failed_row_count = 7
failed_row_indices = 356,381,395,397,416,426,427
status_sha256 = 1ECA159A5722823FA83FAE6C87C7DA70AA63A0649E94B4E9A13B706D22378419
```

The single standing retry requested only the seven failed rows with the authorized wider retry window and at-or-before-fill selection.

```text
status = PASS_STANDING_BOUNDED_DATABENTO_TBBO_FAILED_WINDOW_RETRY_SELECTED_NOT_RESULT
requirements_count = 7
selected_row_count = 7
failed_row_count = 0
status_sha256 = FCDF17B6857EAB25CF90CBA27A1F4800823A3669C462B6EFD9BC7A63EFCD9040
```

## Combined Registry

The active combined TBBO registry now includes:

```text
old prebound / batch / retry / row215 evidence = 52 rows
standing batch selected evidence = 26 rows
standing retry selected evidence = 7 rows
total = 85 rows
row_index_min = 1
row_index_max = 435
registry_sha256 = BB0B7E50E713E63701F1BCE83CB974DADD4DA419E2387006018623470756B367
```

Combined registry:

```text
docs/researchops/s27_v2_market_spread_evidence/ZN/20260612_2023_test_combined_market_order_tbbo_registry/combined_market_order_tbbo_registry.csv
```

## Mechanical Continuation

The controlled 2023 TEST mechanical artifact run now advances through row 390 and stops at row 391.

```text
candidate_row_count = 391
supported_mechanical_row_count = 390
fail_closed_row_index = 391
fail_closed_reason = SECONDARY_FILLED_ORDER_ACROSS_UNRESOLVED_SESSION_EOD_GAP_NOT_RESULT
final_position_contracts = 4
cumulative_gross_pnl_amount = 8796.875
cumulative_commission_amount = 593.4
cumulative_spread_amount = 0.0
cumulative_net_pnl_amount = 8203.475
```

The row-391 blocker is:

```text
row_index = 391
decision_timestamp_utc = 2023-01-26T20:00:00Z
raw_symbol = ZNH3
starting_position_contracts = 4
desired_position_contracts = 12
position_change_contracts = 8
order_side = BUY
adjacent_target_position = 5
fill_candidate_timestamp_utc = 2023-01-26T21:00:00Z
fill_candidate_close = 114.8125
same_session = FALSE
market_spread_cost_status = FAIL_CLOSED_MARKET_ORDER_ACROSS_UNRESOLVED_SESSION_EOD_GAP
```

This is no longer a missing-spread blocker. It is a session/EOD policy blocker.

Run artifact hashes:

```text
run_manifest_sha256 = A1E485EEC72447E1F79947E7DEEBEBA974686589171FF2A428B058C9A2F46A62
evidence_manifest_sha256 = 966EE57EF2923F7F8D484516F73B3147CAB2804E0BAB0A75C0D378C44E1430A7
trusted_bundle_sha256 = 72A5E7E3406E50E3D4882590C4B52B3A6A4681BAA567B5719E973D4309480667
run_bundle_sha256 = 9F970BDECECE277187457256B36EF842964D73345DC9FFBB561FBAFC6BF81845
```

## Local Verification

Commands run:

```text
python -m py_compile src\carver\spine\s27_v2_replay\test_mechanical_run.py tools\databento\carver_s27_v2_2023_test_standing_market_order_tbbo_acquisition.py
python -m py_compile src\carver\spine\s27_v2_replay\test_mechanical_run.py tools\databento\carver_s27_v2_2023_test_standing_market_order_tbbo_failed_window_retry.py
python -m pytest tests\test_s27_v2_2023_test_mechanical_run.py -q
python -m pytest tests\test_s27_v2_pretest_development_recon_completion.py tests\test_s27_v2_2023_test_mechanical_run.py -q
```

Results:

```text
85 passed in 252.30s
146 passed in 263.38s
```

## Local Hostile Audit Remediation

A read-only local hostile audit found one P2 boundary-hardening issue: the standing TBBO acquisition path validated the requirements-ledger row hash but did not independently recompute `request_start_utc` and `request_end_utc` as `fill_candidate_timestamp_utc +/- 5 seconds` before calling DataBento. The current artifacts were bounded, but a self-consistent forged requirements ledger could have widened future provider access.

Remediation:

```text
tools/databento/carver_s27_v2_2023_test_standing_market_order_tbbo_acquisition.py
```

now recomputes and enforces the exact `fill +/- 5s` request window before provider access.

The retry path:

```text
tools/databento/carver_s27_v2_2023_test_standing_market_order_tbbo_failed_window_retry.py
```

now also rejects requirements rows that claim result or source-faithful authority, and validates the original source request window before deriving the bounded retry window.

Focused regression tests added:

```text
test_standing_tbbo_acquisition_rejects_self_consistent_broadened_request_window
test_standing_tbbo_retry_rejects_result_or_source_faithful_claim
```

Post-remediation verification:

```text
python -m py_compile tools\databento\carver_s27_v2_2023_test_standing_market_order_tbbo_acquisition.py tools\databento\carver_s27_v2_2023_test_standing_market_order_tbbo_failed_window_retry.py tests\test_s27_v2_2023_test_mechanical_run.py
python -m pytest tests\test_s27_v2_2023_test_mechanical_run.py::test_standing_tbbo_acquisition_rejects_self_consistent_broadened_request_window tests\test_s27_v2_2023_test_mechanical_run.py::test_standing_tbbo_retry_rejects_result_or_source_faithful_claim -q
python -m pytest tests\test_s27_v2_2023_test_mechanical_run.py -q
python -m pytest tests\test_s27_v2_pretest_development_recon_completion.py tests\test_s27_v2_2023_test_mechanical_run.py -q
```

Results:

```text
2 passed in 2.18s
87 passed in 282.35s
148 passed in 285.37s
```

Local re-audit result:

```text
PASS_NO_P0_P1_P2_PRIOR_P2_CLOSED
```

The re-audit noted one P3 coverage gap: the retry flag regression covered `source_faithful_evidence_claimed` but not `result_interpretation_authorized`. The test was parameterized to cover both flags.

Final focused verification:

```text
python -m pytest tests\test_s27_v2_2023_test_mechanical_run.py::test_standing_tbbo_acquisition_rejects_self_consistent_broadened_request_window tests\test_s27_v2_2023_test_mechanical_run.py::test_standing_tbbo_retry_rejects_result_or_source_faithful_claim -q
python -m pytest tests\test_s27_v2_2023_test_mechanical_run.py -q
```

Results:

```text
3 passed in 2.83s
88 passed in 272.06s
```

## Non-Authorization

This checkpoint is mechanical artifact construction only. It does not authorize result interpretation, performance evaluation, tuning, source-faithful evidence claims, promotion, deployment, trading, Git actions, VALIDATION, OOS, Lockbox, or Forward access.

## Next Gate

The next local-only gate should resolve or fail-close row 391 as a session/EOD policy class:

```text
S27_V2 2023 TEST row-391 session/EOD market-order policy and implementation gate
```

External GPT/Opus audits remain deferred until a consolidated phase checkpoint unless a genuinely new machinery class or final audit requires them.
