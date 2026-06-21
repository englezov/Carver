# CARVER S27 ZN V2 2023 TEST Row 1378 Local Audit Remediation

Date: 2026-06-21

Status: LOCAL_AUDIT_REMEDIATION_ROW1378_PACK_EXHAUSTION_ACTIVE_ARTIFACT_RESTORED_NOT_RESULT

## Audit Finding Summary

Local hostile audit found three blockers:

- Active TEST artifacts had drifted to a 1390-row run after a proof-style test rewrote the mutable pack/run directories.
- Focused mechanical-run tests still pinned the pre-row-1378 combined TBBO registry hash.
- The row-1378 DataBento acquisition helper was visible in the repo and needed explicit quarantine as prior bounded evidence tooling, not post-fill completion runtime.

## Remediation

The 2023 TEST pack builder now has an explicit authorized declared-pack row limit of `1378`. When the limit is reached and the final row is formula-supported, the manifest records:

- `selected_slice_rule = CONTROLLED_LOCAL_ONLY_2023_TEST_COMPLETED_ROWS_TO_AUTHORIZED_DECLARED_PACK_LIMIT`
- `test_window_end_status = DECLARED_PACK_EXHAUSTED_NO_FAIL_CLOSED_BLOCKER_NOT_RESULT`
- `supported_mechanical_row_count = 1378`
- `fail_closed_blocker.row_index = 0`
- `fail_closed_blocker.formula_status = NO_FAIL_CLOSED_BLOCKER_DECLARED_PACK_EXHAUSTED_NOT_RESULT`

Active artifacts were rebuilt after the patch and now report:

- PACK `1378 1378 DECLARED_PACK_EXHAUSTED_NO_FAIL_CLOSED_BLOCKER_NOT_RESULT 0 NO_FAIL_CLOSED_BLOCKER_DECLARED_PACK_EXHAUSTED_NOT_RESULT`
- RUN `1378 1378 0 NO_FAIL_CLOSED_BLOCKER_DECLARED_PACK_EXHAUSTED_NOT_RESULT 3`

Focused mechanical tests were updated to assert the pack-exhausted contract and to bind cost rows to the active combined TBBO registry bytes rather than the stale pre-row-1378 registry hash.

## Provider Tool Quarantine

`tools/databento/carver_s27_v2_2023_test_row1378_market_spread_tbbo_acquisition.py` is classified as prior-gate bounded evidence acquisition tooling from the row-1378 primary/retry TBBO evidence gate. It is not part of the post-fill engineering convention binding runtime, not imported by package-root code, not exported from `src/carver/spine/s27_v2_replay`, and not authorized for execution under the pack-exhaustion completion gate.

The post-fill binding tool `tools/databento/carver_s27_v2_2023_test_row1378_tbbo_engineering_convention_binding.py` consumes only already-acquired local evidence and performs no provider/API access or download.

## Non-Authorizations

This remediation does not authorize provider/API access, downloads, new data acquisition, broader TEST pack expansion, VALIDATION, OOS, Lockbox, Forward, result interpretation, PnL evaluation beyond mechanical construction, tuning, adapter/deployment/trading/promotion, Git actions, GPT packet preparation, or source-faithful evidence claims.
