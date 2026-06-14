# S27 V2 2023 TEST Consolidated TBBO Completion Loop To Row 441 Local Audit

Date: 2026-06-13

Status:

```text
LOCAL_PASS_PENDING_ROW441_TBBO_POLICY_DECISION_NOT_RESULT
```

## Scope

Operator authorized a consolidated local-only 2023 TEST mechanical artifact completion loop for already-local 2023 ZN TEST files, pre-2023 strict-prior warmup/evidence, the standing bounded market-order TBBO policy, and audited S27_V2 machinery.

External GPT/Opus audits were not authorized for row-level blockers under this gate.

## Actions

- Re-ran standing bounded DataBento TBBO acquisition only for deterministic requirements-ledger rows still marked `REQUIRES_BOUNDED_DATABENTO_TBBO_EVIDENCE`.
- Selected 20 of the 23 currently missing `+/-5s` TBBO windows.
- Re-ran the authorized single bounded retry for the 3 failed rows using 60 seconds lookback and 5 seconds lookahead, while selecting only at-or-before-fill quotes.
- Recovered rows `439` and `532`; row `441` remained fail-closed with no selected TBBO quote.
- Reconstructed the standing batch and retry selected registries from already-acquired raw provider bytes to repair a mutable-registry overwrite issue.
- Patched the standing batch and retry scripts so future runs merge selected/provider/raw registries by `row_index` rather than overwriting earlier selected evidence.
- Regenerated the active combined market-order TBBO registry, TEST requirements ledger, and controlled TEST mechanical artifacts.

## Evidence State

Standing batch status:

```text
FAIL_CLOSED_STANDING_BOUNDED_DATABENTO_TBBO_BATCH_INCOMPLETE_NOT_RESULT
```

Standing batch selected rows:

```text
46
```

Standing batch failed rows:

```text
356, 381, 395, 397, 416, 426, 427, 439, 441, 532
```

Standing retry status:

```text
FAIL_CLOSED_STANDING_BOUNDED_DATABENTO_TBBO_FAILED_WINDOW_RETRY_INCOMPLETE_NOT_RESULT
```

Standing retry selected rows:

```text
9
```

Standing retry failed rows:

```text
441
```

Combined market TBBO registry row count:

```text
109
```

Requirements ledger state:

```text
ALREADY_BOUND_TBBO_EVIDENCE_AVAILABLE = 109
REQUIRES_BOUNDED_DATABENTO_TBBO_EVIDENCE = 1
```

The remaining missing row is:

```text
row_index = 441
decision_timestamp_utc = 2023-01-31T04:00:00Z
fill_candidate_timestamp_utc = 2023-01-31T05:00:00Z
raw_symbol = ZNH3
order_side = SELL
order_quantity = 3
starting_position_contracts = 17
desired_position_contracts = 14
position_change_contracts = -3
```

Row `441` initial bounded TBBO CSV and retry bounded TBBO CSV are header-only / no selected quote. The row remains fail-closed.

## Controlled TEST Run State

The regenerated controlled 2023 TEST mechanical artifact run now supports rows `1` through `440` and fails closed at row `441`.

Run manifest fields:

```text
candidate_row_count = 441
supported_mechanical_row_count = 440
fail_closed_row_index = 441
fail_closed_reason = FAIL_CLOSED_MARKET_ORDER_SPREAD_EVIDENCE_UNAVAILABLE_FOR_CONTINUATION_NOT_RESULT
final_position_contracts = 17
cumulative_gross_pnl_amount = 3937.5
cumulative_commission_amount = 857.8999999999999
cumulative_spread_amount = 0.0
cumulative_net_pnl_amount = 3079.6000000000004
```

The PnL fields above are mechanical row-construction metadata only, not result interpretation, not performance evaluation, and not a source-faithful evidence claim.

## Hashes

```text
D3BD813B29343366DDF966F5DB58DD9395FBA10DDF3F5C101D598F6349985D8B  standing batch status
BEDDF9C98C1F118E8C9607574CDF48E388B646D01A314ACA2F9D832F74819A2C  standing batch manifest
3BAB99F7B4586CDF3F05FF6EF8B086D107B7F8885D5FF5EAFE1883B2E54CC959  standing retry status
29F2A1B3CAEA46D853B541F616B93184997C144987DFE058A5F3A12F890B49CD  standing retry manifest
180EBEA16CC6F06D17FA51EE3FB4411D89831B45A6C4D61C723567C6ECDE6F03  combined market TBBO registry
2BC5B90FF9A2E9604D60281AD2E52B65764F29A7DE5C93D77D245D4CED35CB63  market-order TBBO requirements ledger
F5A470C6F85DD3019DF5331E1FF7E5C1E0E2E2F852807D604A1381AE174DA69D  run manifest
74FF220CF65549554B756471AAB3906DA77724C840E877ACE1464FA15BA3CB06  evidence manifest
CCB30139EC31EDB4D01091BBCBBC4DEDD3DB1991484DFCCCB463B81EEF5C223E  trusted bundle
37331959CA6F207DFAFEB7717FA0AD4F6CADF723A7AEC4391D65171BD6A51167  run SHA256SUMS.csv
```

## Verification

Passed:

```text
python -m pytest tests\test_s27_v2_2023_test_mechanical_run.py::test_2023_test_pack_is_declared_and_stops_at_first_fail_closed_blocker tests\test_s27_v2_2023_test_mechanical_run.py::test_2023_test_mechanical_run_fails_closed_without_result_claim -q
```

Result:

```text
2 passed in 81.51s
```

Passed:

```text
python -m pytest tests\test_s27_v2_2023_test_mechanical_run.py::test_2023_test_market_order_tbbo_requirements_discovery_is_hash_bound_and_local_only -q
```

Result:

```text
1 passed in 31.36s
```

Passed:

```text
python -m pytest tests\test_s27_v2_2023_test_mechanical_run.py::test_2023_test_market_order_tbbo_requirements_discovery_rejects_forged_row tests\test_s27_v2_2023_test_mechanical_run.py::test_2023_test_market_order_tbbo_requirements_rejects_bound_row_without_bound_hashes tests\test_s27_v2_2023_test_mechanical_run.py::test_standing_tbbo_acquisition_rejects_self_consistent_broadened_request_window -q
```

Result:

```text
3 passed in 124.34s
```

Passed:

```text
python -m pytest tests\test_s27_v2_2023_test_mechanical_run.py::test_standing_tbbo_retry_rejects_result_or_source_faithful_claim tests\test_s27_v2_2023_test_mechanical_run.py::test_2023_test_combined_tbbo_registry_rejects_self_consistent_row215_drift tests\test_s27_v2_2023_test_mechanical_run.py::test_2023_test_combined_tbbo_registry_rejects_self_consistent_row437_drift tests\test_s27_v2_2023_test_mechanical_run.py::test_2023_test_combined_tbbo_registry_rejects_self_consistent_row438_drift -q
```

Result:

```text
5 passed in 81.22s
```

Passed:

```text
python -m pytest tests\test_s27_v2_2023_test_mechanical_run.py::test_2023_test_market_order_freeze_rejects_forged_non_full_gap_status tests\test_s27_v2_2023_test_mechanical_run.py::test_2023_test_market_order_freeze_rejects_mismatched_full_gap_quantity tests\test_s27_v2_2023_test_mechanical_run.py::test_2023_test_market_order_freeze_rejects_locked_status_without_required_emitted_flags tests\test_s27_v2_2023_test_mechanical_run.py::test_2023_test_market_order_freeze_rejects_wrong_side_for_position_change tests\test_s27_v2_2023_test_mechanical_run.py::test_2023_test_market_order_freeze_rejects_target_position_mismatch -q
```

Result:

```text
7 passed in 0.92s
```

After the initial local hostile audit found P1 evidence-integrity findings, remediation verification passed:

```text
python -m pytest tests\test_s27_v2_2023_test_mechanical_run.py::test_standing_tbbo_status_and_manifest_distinguish_current_request_from_aggregate_registry tests\test_s27_v2_2023_test_mechanical_run.py::test_2023_test_combined_tbbo_registry_rejects_source_selected_registry_drift -q
```

Result:

```text
2 passed in 1.82s
```

Passed:

```text
python -m pytest tests\test_s27_v2_2023_test_mechanical_run.py::test_2023_test_mechanical_run_fails_closed_without_result_claim -q
```

Result:

```text
1 passed in 186.51s
```

Passed:

```text
python -m pytest tests\test_s27_v2_2023_test_mechanical_run.py::test_standing_tbbo_status_and_manifest_distinguish_current_request_from_aggregate_registry tests\test_s27_v2_2023_test_mechanical_run.py::test_2023_test_combined_tbbo_registry_rejects_source_selected_registry_drift tests\test_s27_v2_2023_test_mechanical_run.py::test_2023_test_market_order_tbbo_requirements_discovery_is_hash_bound_and_local_only -q
```

Result:

```text
3 passed in 133.71s
```

## Local Audit

Initial read-only hostile audit found two P1 evidence-integrity findings:

- standing batch/retry status and request-manifest fields were ambiguous after registry merge;
- the combined TBBO registry accepted selected-registry rows without independently revalidating current raw provider bytes and quote selection.

Remediation:

- standing batch/retry status and manifest files now distinguish current provider request rows from aggregate registry rows;
- selected/provider/raw registries merge by `row_index` instead of overwriting prior selected evidence;
- combined TBBO registry construction now verifies raw-output registry paths, current raw DBN/CSV SHA256 hashes, and reselects the latest eligible at-or-before-fill quote from current raw CSV bytes before accepting selected rows.

Read-only hostile re-audit found one remaining P1, recorded below.

## Second P1 Remediation

The read-only hostile re-audit found one remaining P1: a selected TBBO registry row could blank both raw hash fields, recompute its selected-row hash, and bypass raw-provider byte validation before entering the combined TBBO registry.

Remediation:

- `src/carver/spine/s27_v2_replay/test_mechanical_run.py` now exempts only the hard-coded row-1/row-2 prebound evidence path from raw-byte validation.
- Every registry-based TBBO evidence type now fails closed unless it carries raw CSV and raw DBN hashes, or retry raw CSV and raw DBN hashes.
- The existing raw registry lookup, current raw DBN/CSV SHA256 checks, and raw CSV quote re-selection remain mandatory after those hashes are present.
- `tests/test_s27_v2_2023_test_mechanical_run.py` now covers a self-consistent standing retry selected-registry mutation that blanks `retry_raw_csv_sha256` and `retry_raw_dbn_sha256`, recomputes the selected row hash, and must fail closed.

Verification:

```text
python -m py_compile src\carver\spine\s27_v2_replay\test_mechanical_run.py tests\test_s27_v2_2023_test_mechanical_run.py
```

Result:

```text
passed
```

Passed:

```text
python -m pytest tests\test_s27_v2_2023_test_mechanical_run.py::test_2023_test_combined_tbbo_registry_rejects_source_selected_registry_drift tests\test_s27_v2_2023_test_mechanical_run.py::test_2023_test_combined_tbbo_registry_rejects_source_selected_registry_missing_raw_hashes -q
```

Result:

```text
2 passed in 2.23s
```

Passed:

```text
python -m pytest tests\test_s27_v2_2023_test_mechanical_run.py::test_2023_test_mechanical_run_fails_closed_without_result_claim -q
```

Result:

```text
1 passed in 184.26s
```

Post-remediation file hashes:

- `src/carver/spine/s27_v2_replay/test_mechanical_run.py`: `93924A3E50887EBE23E0B3CA1B28A4EB187B716D0032B935EB53E0C27058B459`
- `tests/test_s27_v2_2023_test_mechanical_run.py`: `B864EBB81DC18893EA0327B429262A619C0D98E64B21B896711032F9B0708F17`

Read-only hostile re-audit of this second remediation returned `PASS`, with P0 none, P1 none, and P2 none.

The re-audit confirmed:

- `_combined_market_tbbo_row()` calls `_validate_selected_tbbo_row_against_raw()` before selected registry rows can enter the combined registry.
- `_validate_selected_tbbo_row_against_raw()` exempts only `PREBOUND_ROW_*` evidence.
- All other registry-based TBBO evidence fails closed if raw CSV or DBN hashes are missing.
- When hashes are present, raw registry lookup, raw file path binding, current raw CSV/DBN SHA256 checks, and raw CSV quote re-selection still run.
- The missing raw-hash bypass regression directly blanks retry raw hashes, recomputes the selected-row hash, and expects fail-closed behavior.

Local continuation to the row-441 policy decision may proceed under the existing gate and non-authorization rules.

## Non-Authorizations Preserved

This gate did not authorize or perform:

- broad provider/API access;
- downloads or new data acquisition outside listed bounded TBBO quote windows;
- VALIDATION, OOS, Lockbox, or Forward access;
- result interpretation;
- PnL evaluation beyond mechanical row construction;
- tuning;
- adapter work;
- deployment;
- trading;
- promotion;
- Git staging, commit, push, or PR;
- GPT packet preparation;
- source-faithful evidence claims.

## Next Gate

The next blocker is row `441`, a SELL 3 market-order TBBO evidence gap where both the bounded initial request and one bounded retry returned no selected at-or-before-fill quote.

The next useful gate is a row-441 TBBO policy decision or a broader class-level policy for empty at-or-before-fill TBBO windows. Any such gate must remain local-only, explicitly labeled if engineering/not-book-explicit, and must not authorize result interpretation, tuning, protected-window access, Git, deployment, trading, promotion, or source-faithful evidence claims.
