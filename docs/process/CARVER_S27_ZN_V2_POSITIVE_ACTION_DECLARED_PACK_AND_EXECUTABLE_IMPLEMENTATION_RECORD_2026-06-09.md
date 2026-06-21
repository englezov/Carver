# S27_V2 Positive-Action Declared Pack And Executable Implementation Record

Date: 2026-06-09

Status:

```text
LOCAL_POSITIVE_ACTION_DEVELOPMENT_RECON_IMPLEMENTED_NOT_BACKTEST_NOT_RESULT
```

## Scope

Under the consolidated positive-action replay completion authorization, this slice created the first local-only S27_V2 ZN positive-action development/reconciliation input pack and a narrow executable metadata surface around it.

This is not a backtest, not a result-scored run, not result interpretation, not PnL evaluation, and not a source-faithful evidence claim.

## Declared Input Pack

Pack:

```text
docs/researchops/s27_v2_local_replay_inputs/ZN/20260609_positive_action_recon_znm6_20260413T13_declared_pack
```

Selected decision row:

```text
2026-04-13T13:00:00Z
```

Selected fill-candidate row:

```text
2026-04-13T14:00:00Z
```

Selected previous completed daily row:

```text
2026-04-12T00:00:00Z
```

Selected raw symbol:

```text
ZNM6
```

Manifest SHA256:

```text
c15f545b1a2d2bd046565fbca6d010660492c0ced02f6b35806fae88c81bf6c1
```

The pack uses already-local ZN source files only. No provider/API access, downloads, new data acquisition, OOS, Lockbox, Forward, backtest, Git action, adapter work, deployment, trading, promotion, tuning, result interpretation, PnL evaluation, or source-faithful evidence claim was performed.

## Executable Surface

Added:

```text
src/carver/spine/s27_v2_replay/positive_action_executable.py
tests/test_s27_v2_positive_action_executable.py
```

The executable surface rebuilds the active row from the declared pack and locked local source files, verifies declared row-family byte hashes, recomputes EWMA5, sigma-price bridge, EWMAC(16,64) veto, V/Q/M attenuation, S27 scalar/cap, base position, desired position, and first-row order intent.

It emits metadata for:

- desired-position row;
- order-intent row;
- order-transition metadata row;
- validation/provenance/trusted-bundle metadata flags.

It does not emit actual limit order rows, market order rows, fill rows, cost rows, PnL rows, result rows, backtests, or source-faithful evidence claims.

## Positive-Action Row

Emitted bundle hash:

```text
13771bb862a7687408453b1f96816c32ad32f78f800f08b949a0c47e50da2f26
```

Emitted positive-action row hash:

```text
b56e0f40d004ca5b3bb4ad80a5c4f44d9b88db6ad8c0467e8b4a4e375011ffe1
```

Key row values:

```text
capped_forecast = -0.35105404856990824
desired_unrounded_contracts = -0.5016120637629121
desired_rounded_position = -1
current_position_before_order = 0
position_change_contracts = -1
order_required = True
order_side = SELL
order_quantity = 1
```

Execution status:

```text
adjacent_limit_order_policy_status = FAIL_CLOSED_EXECUTION_POLICY_UNRESOLVED_NOT_EMITTED
tick_rounding_policy_status = FAIL_CLOSED_EXECUTION_POLICY_UNRESOLVED_NOT_EMITTED
working_order_lifecycle_status = FAIL_CLOSED_EXECUTION_POLICY_UNRESOLVED_NOT_EMITTED
actual_fill_ledger_status = FAIL_CLOSED_ACTUAL_FILL_LEDGER_NOT_EMITTED
actual_cost_ledger_status = FAIL_CLOSED_ACTUAL_COST_LEDGER_NOT_EMITTED
actual_pnl_ledger_status = FAIL_CLOSED_ACTUAL_PNL_LEDGER_NOT_EMITTED
```

## GPT P1 External-Audit Patch

The first external GPT/alternate audit returned `FAIL` with one P1:

```text
P1-001: Sigma and V/Q/M arithmetic are not fully source-row-bound.
```

Patch:

- `selected_sigma_percent_t` is compared against the active `sigma_runtime_ledger.sigma_percent_t` source-row value before arithmetic;
- `selected_vqm_relative_volatility_v`, `selected_vqm_quantile_q`, and `selected_vqm_multiplier_m` are compared against the active `vqm_runtime_rows` source-row values before arithmetic;
- arithmetic now uses the source-row sigma/V/Q/M values after the manifest/source equivalence checks pass;
- focused tests reject self-consistent manifest history-evidence mutation while source rows remain unchanged.

## Verification

Focused local verification passed:

```text
python -m py_compile src\carver\spine\s27_v2_replay\positive_action_executable.py tests\test_s27_v2_positive_action_executable.py
python -m pytest tests\test_s27_v2_positive_action_executable.py -q
```

Original pytest result:

```text
22 passed
```

After local hostile-audit and GPT P1 hardening:

```text
python -m py_compile src\carver\spine\s27_v2_replay\positive_action_executable.py tests\test_s27_v2_positive_action_executable.py
python -m pytest tests\test_s27_v2_positive_action_executable.py -q
```

Pytest result:

```text
43 passed
```

## Cost Policy

Book/source costs remain primary. This slice does not unlock actual cost ledger emission. If the book/source does not specify enough cost assumptions, later cost work must use a clearly labeled source-native retail futures inferred cost model and must not use prop-firm, CFD, adapter, or personal trading costs.

## Non-Authorization

This record does not authorize provider/API access, downloads, new data acquisition, OOS, Lockbox, Forward, backtests, result-scored runs, result interpretation, PnL evaluation, tuning, adapter work, deployment, trading, promotion, Git staging/commit/push/PR, or source-faithful evidence claims.
