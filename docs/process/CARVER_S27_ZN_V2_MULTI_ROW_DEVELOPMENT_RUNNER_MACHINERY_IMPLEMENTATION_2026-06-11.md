# CARVER S27 ZN V2 Multi-Row Development Runner Machinery Implementation

Date: 2026-06-11

Status: S27_V2_MULTI_ROW_DEVELOPMENT_RUNNER_MACHINERY_PRE_RUN_NOT_EXECUTED

Authorization:

```text
S27_V2 generalized multi-row controlled local-only development backtest-runner machinery gate
```

## Scope

This implementation responds to the GPT 5.5 pre-run audit finding that the
single-row positive-action checkpoint did not prove a generalized multi-row
controlled local-only Development/Reconciliation runner.

The patch adds pre-run machinery only:

- locked local ZN declared-input-pack root;
- oldest suitable post-warmup Development/Reconciliation window requirement;
- completed-bar-only and strict-prior-per-row iteration gates;
- deterministic run artifact-family plan;
- stale/diagnostic runner exclusion proof;
- active positive-action actual-PnL closure checkpoint binding;
- explicit execution entrypoint that remains fail-closed until separate
  operator run authorization.

## Files Added

- `src/carver/spine/s27_v2_replay/multi_row_development_runner.py`
- `tests/test_s27_v2_multi_row_development_runner.py`

## Key Boundaries

The new machinery is not a backtest run.

It does not emit:

- backtest rows;
- result-scored runs;
- result interpretation;
- PnL evaluation beyond mechanical row construction;
- source-faithful evidence claims.

The execution entrypoint
`execute_s27_v2_multi_row_development_backtest()` raises
`ReplayExecutionBlocked` and requires separate operator run authorization.

The module is not exported from `src/carver/spine/s27_v2_replay/__init__.py`.

## Stale-Runner Exclusion

The runner machinery records the following stale/diagnostic S27 paths as
forbidden import targets for the S27_V2 run path:

- `tools/databento/carver_s27_zn_2024_corrected_validation_backtest.py`
- `tools/databento/carver_s27_zn_2024_corrected_full_ladder_validation_backtest.py`
- `tools/databento/carver_s27_zn_2025_2026_corrected_test3_backtest.py`
- `tools/databento/carver_s27_zn_m1_ladder_dev_recon_backtest.py`
- `tools/audit/carver_s27_zn_ladder_attribution.py`
- `tools/audit/carver_s27_zn_lockbox_readiness.py`

The proof requires a package-root export check and repo-wide stale-runner scan
before any future run authorization.

## Verification

Focused verification executed:

```text
pytest tests/test_s27_v2_multi_row_development_runner.py
30 passed
```

Adjacent integration verification executed:

```text
pytest tests/test_s27_v2_multi_row_development_runner.py tests/test_s27_v2_positive_action_actual_pnl_closure.py
85 passed
```

## Local Audit Finding Patch

Initial local hostile audit found two P2 issues and one P3 hardening note:

- P2: the runner non-authorization tuple did not carry forward credential,
  parser execution, file replay, and diagnostics prohibitions from the current
  governing record;
- P2: the pre-run runner machinery rebuilt the positive-action actual-PnL
  closure bundle during validation, which leaked into the local data/PnL
  execution chain inside a pre-run/not-executed gate;
- P3: stale-runner exclusion tests only checked literal static import syntax.

Patch response:

- added `NO_CREDENTIAL_USE`, `NO_PARSER_EXECUTION`, `NO_FILE_REPLAY`, and
  `NO_DIAGNOSTICS` to the enforced runner non-authorization tuple;
- replaced active positive-action closure rebuilding with recorded checkpoint
  binding to closure bundle hash
  `5eb846c4fd83879c6648e9d4132d60f4fdc59ed8626453c9121496e307cacd9e` and
  process record
  `docs/process/CARVER_S27_ZN_V2_POSITIVE_ACTION_ACTUAL_PNL_CLOSURE_IMPLEMENTATION_2026-06-11.md`;
- expanded stale-runner leakage tests to reject dynamic import/execution
  surfaces including `importlib`, `__import__`, `runpy`, `SourceFileLoader`,
  and `subprocess`.

Post-patch focused verification:

```text
pytest tests/test_s27_v2_multi_row_development_runner.py tests/test_s27_v2_positive_action_actual_pnl_closure.py
85 passed
```

## Non-Authorization

This record does not authorize:

- provider/API access;
- downloads or new data acquisition;
- credential use;
- parser execution;
- file replay;
- diagnostics;
- OOS, Lockbox, or Forward access;
- actual backtest execution;
- result-scored runs;
- result interpretation;
- PnL evaluation beyond mechanical row construction;
- tuning;
- adapter work;
- deployment, trading, or promotion;
- Git actions;
- source-faithful evidence claims.
