# S27_V2 No-Cost Executable Metadata Local Audit Result

Date: 2026-06-09

Status:

```text
LOCAL_HOSTILE_AUDIT_PASS
```

## Scope

Local hostile audit of the `S27_V2` no-cost executable metadata surface for the audited `ZNM6` remediation pack.

Audited files included:

```text
src/carver/spine/s27_v2_replay/no_cost_executable.py
tests/test_s27_v2_no_cost_executable.py
src/carver/spine/s27_v2_replay/no_fill_executable.py
src/carver/spine/s27_v2_replay/costs.py
src/carver/spine/s27_v2_replay/cost_contract.py
src/carver/spine/s27_v2_replay/cost_input_contract.py
docs/process/CARVER_S27_ZN_V2_COST_EVIDENCE_COST_EXECUTABLE_PLANNING_GATE_2026-06-09.md
docs/process/CARVER_S27_ZN_V2_NO_COST_EXECUTABLE_METADATA_IMPLEMENTATION_RECORD_2026-06-09.md
docs/process/CARVER_S27_ZN_V2_TRUST_ROOT_DESIGN_CURRENT_STATE_AND_AUTHORIZATION_QUEUE_2026-06-06.md
```

## Verdict

Two independent local hostile-audit sidecars returned:

```text
PASS
P0 findings: none
P1 findings: none
P2 findings: none
P3 findings: none
```

## Confirmed

- caller-supplied no-fill bundles are not authority;
- bundle validation rebuilds active no-fill state from the audited remediation pack;
- no-cost metadata binds `NO_ORDER`, order quantity `0`, and `NO_POSITION_CHANGE_NO_ORDER`;
- no-cost metadata binds `fill_required = False` and `actual_fill_ledger_emitted = False`;
- no-cost metadata binds `cost_required = False` and `cost_rows_emitted = False`;
- actual commission, spread-cost, and cost ledger emission remain fail-closed;
- commission, spread, spread-cost, and total-cost amounts remain zero;
- total cost currency remains `NOT_APPLICABLE`;
- standalone no-cost row validation is non-authoritative and fails closed;
- self-consistent forged no-cost rows and hashes are rejected;
- forged positive cost amounts, cost provenance, cost currency, and downstream PnL/result/source-faithful flags are rejected;
- no package-root export leak was found;
- no provider/API, downloads, new data, OOS/Lockbox/Forward, backtest, Git, adapter, deployment, trading, promotion, result interpretation, PnL evaluation, or source-faithful evidence surface was introduced.

## Verification Basis

Focused verification passed before local audit:

```text
python -m py_compile src\carver\spine\s27_v2_replay\no_cost_executable.py tests\test_s27_v2_no_cost_executable.py
PASS

python -m pytest tests\test_s27_v2_no_cost_executable.py -q
23 passed in 50.04s

python -m pytest tests\test_s27_v2_no_fill_executable.py tests\test_s27_v2_no_cost_executable.py -q
42 passed in 164.52s
```

Emitted no-cost metadata hashes:

```text
bundle_hash = 5cd63d10bd15c494713b6635c75a9a123ef943e8805e4482b4c22fe7b93dab99
no_cost_row_hash = f8f07f2f218678a3be6d703025eae9bc643270735550cfba55dd58d0c1075193
no_fill_bundle_hash = 7752233b992fd25cd729c0422a385a24e6aee30dddfffc5c9b91ba4a7296fe5c
no_fill_row_hash = bf7c4f60c182035fdb2b651ab4c9b65bba49c77255eaec00a429875e68da7b97
```

## Non-Authorization

This local audit result does not authorize actual positive fill emission, actual commission/spread/cost ledger emission, PnL/result emission, result-scored runs, backtests, result interpretation, PnL evaluation, provider/API access, downloads, new data, OOS/Lockbox/Forward, Git actions, adapter work, deployment, trading, promotion, tuning, or source-faithful evidence claims.

## Next Step

Prepare a GPT/alternate external hostile-audit handoff packet for the locally passed no-cost executable metadata gate before moving to any PnL/backtest-readiness gate.
