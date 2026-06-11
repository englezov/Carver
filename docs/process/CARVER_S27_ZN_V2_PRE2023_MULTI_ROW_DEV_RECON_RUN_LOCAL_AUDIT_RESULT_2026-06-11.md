# CARVER S27_V2 Pre-2023 Multi-Row Development/Reconciliation Run Local Hostile Audit Result

Date: 2026-06-11

Status: `LOCAL_HOSTILE_AUDIT_PASS`

Scope:

- `tools/databento/carver_s27_v2_pre2023_multi_row_pack.py`
- `src/carver/spine/s27_v2_replay/pre2023_multi_row_development_recon_run.py`
- `tests/test_s27_v2_pre2023_multi_row_development_recon.py`
- `docs/researchops/s27_v2_local_replay_inputs/ZN/20260611_pre2023_multi_row_dev_recon_2022_minimum_declared_pack`
- `docs/researchops/s27_v2_local_replay_runs/ZN/20260611_pre2023_multi_row_dev_recon_2022_minimum_run`

## Verdict

PASS.

No P0, P1, or P2 blockers were found in the scoped read-only local hostile audit.

## Findings

P0: None.

P1: None.

P2: None.

P3: The focused tests call `run_pre2023_multi_row_development_recon()` in a module fixture and therefore regenerate run artifacts before asserting them. The tests do cover hard-coded timestamps, state carry, PnL arithmetic, locked paths, non-authorizations, forged bundle rejection, and package-root export leakage, but they are not a pure committed-artifact-only audit. This is non-blocking because the local hostile audit separately inspected the generated pack and run artifacts in read-only mode.

## Audit Evidence

The local hostile audit confirmed:

- local-only/pre-2023 boundary holds;
- no date at or after `2023-01-01` appears in the selected pack/run surface;
- no TEST, VALIDATION, OOS, Lockbox, or Forward selected data is used;
- pack manifest hash matches the runner pin `362A9C7F9E06737169703383C868C11682A41C3310FAFC917097ADA46806268F`;
- row-family SHA bindings match current file bytes;
- run manifest, evidence manifest, trusted bundle, and SHA256 ledger bindings match current file bytes;
- completed-bar ordering is decision < fill < valuation mark for each row;
- all decision/fill/valuation rows are `ZNH2`;
- position state carries mechanically as `0 -> 8 -> 12`;
- gross PnL, commission, spread, and net PnL arithmetic match the emitted ledgers;
- the scoped runner has no provider/API/download import surface;
- the pack builder reads local files only;
- `run_pre2023_multi_row_development_recon` is not exported from the S27_V2 package root;
- result/backtest/source-faithful evidence gates remain fail-closed in run manifest, trusted bundle, PnL ledger, and validation ledger.

## Non-Authorization Preservation

This audit does not authorize and did not perform:

- provider/API access;
- downloads;
- new data acquisition;
- TEST access;
- VALIDATION access;
- OOS access;
- Lockbox access;
- Forward access;
- result-scored runs;
- result interpretation;
- PnL evaluation beyond mechanical row construction;
- tuning;
- adapter work;
- deployment;
- trading;
- promotion;
- Git actions;
- source-faithful evidence claims.

## Next Gate

The next useful gate is a GPT 5.5 Extended Pro external hostile audit packet for this locally passed pre-2023 two-row Development/Reconciliation multi-row pack and executable runner.

That packet should verify the local-only pre-2023 boundary, 2023 TEST preservation, completed-bar ordering, state carry, mechanical ledger arithmetic, hash binding, fail-closed result/source-faithful gates, stale-runner exclusion, and package-root containment.
