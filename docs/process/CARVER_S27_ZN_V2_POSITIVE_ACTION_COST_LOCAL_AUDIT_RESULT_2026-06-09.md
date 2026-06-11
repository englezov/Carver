# S27_V2 Positive-Action Cost Local Hostile Audit Result

Date: 2026-06-09

Status:

```text
LOCAL_HOSTILE_AUDIT_PASS_NO_P0_P1_P2_P3
```

## Scope

The local hostile audit covered the S27_V2 positive-action cost-policy evidence surface only:

```text
src/carver/spine/s27_v2_replay/positive_action_cost_executable.py
tests/test_s27_v2_positive_action_cost_executable.py
src/carver/spine/s27_v2_replay/positive_action_fill_executable.py
src/carver/spine/s27_v2_replay/__init__.py
docs/process/CARVER_S27_ZN_V2_POSITIVE_ACTION_COST_IMPLEMENTATION_RECORD_2026-06-09.md
docs/process/CARVER_S27_ZN_BOOK_SOURCE_LOCK_2026-06-05.md
docs/researchops/s27_v2_local_replay_inputs/ZN/20260609_positive_action_recon_znm6_20260413T13_declared_pack/cost_parameter.csv
```

## Result

Two independent local hostile audits returned PASS with no P0, P1, P2, or P3 findings.

The audits confirmed:

- active positive-action fill bundle re-derivation before cost evidence acceptance;
- `cost_parameter.csv` byte SHA256 and active row hash binding;
- source-lock treatment that all orders incur commissions;
- limit-fill commission-only treatment with no market spread cost;
- numeric ZN commission policy remains fail-closed;
- no inferred retail futures cost assumption is used;
- prop-firm, CFD, adapter, and personal trading costs are rejected;
- standalone cost evidence rows are non-authoritative;
- self-consistent forged cost row, forged bundle hash, promoted numeric cost emission, fake commission amount, stale fill bundle, and downstream flag mutations are rejected;
- package-root exports do not leak the cost executable surface;
- no provider/API, download, new data, OOS, Lockbox, Forward, backtest, PnL/result, Git, adapter, deployment, trading, promotion, tuning, or source-faithful evidence surface was introduced.

## Verification

Focused local verification passed before the hostile audit:

```text
python -m py_compile src\carver\spine\s27_v2_replay\positive_action_cost_executable.py -> PASS
python -m pytest tests\test_s27_v2_positive_action_cost_executable.py -q -> 32 passed
python -m pytest tests\test_s27_v2_positive_action_fill_executable.py tests\test_s27_v2_positive_action_cost_executable.py -q -> 64 passed
```

## Active Hashes

```text
bundle_hash = 3750336bcf1085a8eefd685a7c271dc5c0d2699d5790b56a263a7508c83ab2b9
cost_evidence_row_hash = b44e2e559507291e4e44b0fed1b2790b6c4ab56ed26c0b5dfbb50918f7e15a9b
source_cost_treatment_hash = 4312881082e6cfb70a17524b84746618c8235201f40e5eed76b1ea990360395a
limit_fill_cost_treatment_hash = 9bff953de99c51ca4aa1e2ff4c49e0c3c02ce8c104a9a345e1cc6ef48db58754
prop_cfd_adapter_cost_rejection_hash = 6e64ae92aa4ac4ec23220c920a36837d13df11cb2fa64927966f473fa729dad9
cost_parameter_file_hash = e6b7c69a712fd7a5effbabbd4c809f24c1a6dfabbfb1ce317b387c923ac7f098
cost_parameter_row_hash = 069f25beb5c42bb030081883f3b16298c1aa610cd3ecccb94ab887bdf271513c
fill_bundle_hash = 196328c2cd7471999f249bda21064f09c1fd7efd5252437d6122541df2cbf211
limit_fill_row_hash = 2a0870fc368c839a337aac47865bdb19df5315d57a6c894e047b44819ddfe801
```

## Boundary

This local PASS does not authorize actual numeric cost rows, PnL rows, result rows, backtests, result interpretation, PnL evaluation, source-faithful evidence claims, provider/API access, downloads, new data, OOS/Lockbox/Forward access, Git actions, adapter/deployment/trading/promotion, or tuning.

The next useful gate is a GPT/alternate external hostile-audit handoff for this locally passed positive-action cost-policy evidence surface.
