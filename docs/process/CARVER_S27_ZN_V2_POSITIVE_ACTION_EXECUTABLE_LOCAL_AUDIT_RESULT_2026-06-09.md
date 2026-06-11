# S27_V2 Positive-Action Executable Local Hostile Audit Result

Date: 2026-06-09

Status:

```text
LOCAL_HOSTILE_AUDIT_PASS_POSITIVE_ACTION_EXECUTABLE_NOT_BACKTEST_NOT_RESULT
```

## Scope

Audited scope:

```text
src/carver/spine/s27_v2_replay/positive_action_executable.py
tests/test_s27_v2_positive_action_executable.py
docs/researchops/s27_v2_local_replay_inputs/ZN/20260609_positive_action_recon_znm6_20260413T13_declared_pack
```

This audit was limited to the local-only positive-action development/reconciliation surface. It did not authorize or perform provider/API access, downloads, new data acquisition, OOS, Lockbox, Forward, backtests, result-scored runs, result interpretation, PnL evaluation, tuning, adapter work, deployment, trading, promotion, Git actions, or source-faithful evidence claims.

## Initial Findings And Patches

Initial local hostile audit found:

- P1: selected daily/hourly bars were byte-bound to the pack but not independently checked against declared source rows.
- P2: forged-bundle identity, non-authorization, bundle hash, manifest/source hash, and pack/source-row mismatch coverage needed hardening.

Patch result:

- selected daily continuous/current-contract rows are checked against the declared daily risk history source row;
- selected hourly decision/fill rows are checked against the declared hourly sanitized source rows;
- every manifest-declared source file path/hash is byte-bound, including `roll_plan`, `symbology`, and `vqm_daily_ledger`;
- tests now cover forged bundle identity fields, non-authorizations, bundle hash tampering, row-family hash forgery, every declared source hash forgery, hourly pack/source mismatch, and daily pack/source mismatch.

Focused verification after patches:

```text
python -m py_compile src\carver\spine\s27_v2_replay\positive_action_executable.py tests\test_s27_v2_positive_action_executable.py
python -m pytest tests\test_s27_v2_positive_action_executable.py -q
```

Result:

```text
39 passed
```

## External Audit P1 Patch

The first external GPT/alternate audit returned `FAIL` with:

```text
P1-001: Sigma and V/Q/M arithmetic are not fully source-row-bound.
```

The patch now requires:

- manifest `selected_sigma_percent_t` equals the active `sigma_runtime_ledger.sigma_percent_t` source-row value;
- manifest `selected_vqm_relative_volatility_v` equals the active `vqm_runtime_rows.relative_volatility_v` source-row value;
- manifest `selected_vqm_quantile_q` equals the active `vqm_runtime_rows.quantile_q` source-row value;
- manifest `selected_vqm_multiplier_m` equals the active `vqm_runtime_rows.vol_multiplier` source-row value.

The positive-action arithmetic now uses the active source-row sigma and V/Q/M values after those checks pass.

Focused verification after the GPT P1 patch:

```text
python -m py_compile src\carver\spine\s27_v2_replay\positive_action_executable.py tests\test_s27_v2_positive_action_executable.py
python -m pytest tests\test_s27_v2_positive_action_executable.py -q
```

Result:

```text
43 passed
```

## Final Local Hostile Re-Audit

Final subagent re-audit verdict:

```text
PASS
```

No P0/P1/P2/P3 findings were found.

The re-audit confirmed:

- prior P1/P2 findings are closed;
- selected daily/current/hourly decision/hourly fill pack rows are checked against declared source rows;
- manifest, row-family files, and declared source files are byte/hash/path bound;
- tests cover every declared source hash forgery;
- positive `SELL 1` from flat arithmetic is bound;
- actual limit order, market order, fill, cost, PnL, result, and source-faithful evidence surfaces are explicitly false/rejected;
- non-authorizations preserve provider/API, download, new data, OOS, Lockbox, Forward, backtest, Git, adapter/deployment/trading/promotion, tuning, result interpretation, PnL evaluation, and source-faithful evidence prohibitions.

## Current Hashes

Positive-action bundle hash:

```text
13771bb862a7687408453b1f96816c32ad32f78f800f08b949a0c47e50da2f26
```

Positive-action row hash:

```text
b56e0f40d004ca5b3bb4ad80a5c4f44d9b88db6ad8c0467e8b4a4e375011ffe1
```

Input manifest SHA256:

```text
c15f545b1a2d2bd046565fbca6d010660492c0ced02f6b35806fae88c81bf6c1
```

## Non-Authorization

This local audit does not claim external PASS. It does not authorize actual limit/market order emission, actual fill rows, actual cost rows, actual PnL rows, result rows, backtests, result interpretation, PnL evaluation, source-faithful evidence claims, provider/API access, downloads, new data, OOS/Lockbox/Forward access, Git actions, adapter work, deployment, trading, promotion, or tuning.
