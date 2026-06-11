# CARVER S27_V2 Pre-2023 Broader Development/Reconciliation Run Local Hostile Audit Result

Date: 2026-06-11

Status:

```text
LOCAL_HOSTILE_AUDIT_PASS
```

Scope:

```text
tools/databento/carver_s27_v2_pre2023_broader_dev_recon_pack.py
src/carver/spine/s27_v2_replay/pre2023_broader_development_recon_run.py
tests/test_s27_v2_pre2023_broader_development_recon.py
docs/process/CARVER_S27_ZN_V2_PRE2023_BROADER_DEV_RECON_RUN_IMPLEMENTATION_2026-06-11.md
docs/researchops/s27_v2_local_replay_inputs/ZN/20260611_pre2023_broader_dev_recon_2022_first_session_declared_pack
docs/researchops/s27_v2_local_replay_runs/ZN/20260611_pre2023_broader_dev_recon_2022_first_session_run
```

## Verdict

```text
PASS
```

No P0, P1, or P2 blockers were found.

## Subagent Audit Results

Two read-only hostile-audit subagents reviewed the checkpoint.

Subagent 1 focus:

```text
governance/surface leaks
provider/API/download/new-data surfaces
protected-window access
package-root export containment
result/source-faithful boundary
```

Result:

```text
PASS
P0: none
P1: none
P2: none
```

Subagent 2 focus:

```text
artifact integrity
manifest/hash binding
selected timestamps
no 2023 rows
completed-bar ordering
state carry
order/fill/cost/PnL arithmetic
run/evidence/trusted bundle hashes
```

Result:

```text
PASS
P0: none
P1: none
P2: none
```

Subagent 2 recorded one P3 test-hardening note: forged-bundle coverage was present but narrow. This was patched by adding forged status, authorization, identity, path, and manifest-hash cases to `tests/test_s27_v2_pre2023_broader_development_recon.py`.

## Verification After P3 Cleanup

Command:

```powershell
python -m py_compile tools\databento\carver_s27_v2_pre2023_broader_dev_recon_pack.py src\carver\spine\s27_v2_replay\pre2023_broader_development_recon_run.py
python -m pytest tests\test_s27_v2_pre2023_broader_development_recon.py tests\test_s27_v2_pre2023_multi_row_development_recon.py -q
```

Result:

```text
36 passed
```

## Audit Evidence

The local hostile audits confirmed:

- the pack builder reads already-local files only;
- no provider/API/download/new-data path is introduced by the scoped broader pack/run;
- selected rows are all pre-2023 `ZNH2`;
- 2023 is preserved for TEST;
- no TEST, VALIDATION, OOS, Lockbox, or Forward selected rows are used;
- the pack manifest SHA256 is pinned to `0937B1F499A67C488B0F02B7CD998D21D1DD74797BB02001D0E8AFBB581CEC86`;
- row-family SHA256 bindings match current file bytes;
- completed-bar ordering is decision < fill < valuation mark for each row;
- state carries mechanically as `0 -> 8 -> 12 -> 14 -> 15`;
- all four limit orders fill under the one-hour close-only limit-fill rule;
- `no_market_order_ledger.csv` explicitly records no market-order requirement or emission;
- cumulative gross PnL is `-3359.375 USD`;
- cumulative commission is `34.5 USD`;
- cumulative spread cost is `0.0 USD`;
- cumulative net PnL is `-3393.875 USD`;
- run manifest, evidence manifest, trusted bundle, and SHA256 ledger bindings match current file bytes;
- the broader run function is not exported from the package root;
- result, backtest, PnL-evaluation, and source-faithful evidence gates remain fail-closed.

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

The next useful gate is a GPT 5.5 Extended Pro external hostile-audit packet for this locally passed broader pre-2023 Development/Reconciliation checkpoint.

That external audit should verify local-only pre-2023 source use, 2023 TEST preservation, no provider/API/download/new-data path, completed-bar ordering, state carry `0 -> 8 -> 12 -> 14 -> 15`, no-market metadata, mechanical cost/PnL arithmetic, hash binding, fail-closed result/backtest/source-faithful gates, stale-runner exclusion, and package-root containment.
