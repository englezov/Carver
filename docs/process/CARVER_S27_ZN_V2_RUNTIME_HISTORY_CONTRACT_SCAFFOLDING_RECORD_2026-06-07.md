# S27 ZN V2 Runtime History Contract Scaffolding Record

Date: 2026-06-07

Status:

```text
PROCESS_ONLY_S27_ZN_V2_RUNTIME_HISTORY_CONTRACT_SCAFFOLDING_NOT_EXECUTION_OR_BACKTEST_AUTHORIZATION
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Authorization Boundary

Operator authorization received:

```text
Operator authorizes S27_V2 next narrow implementation slice scaffolding only, no provider/API, no downloads, no parser/file replay execution, no diagnostics, no tests/backtests, no OOS/Lockbox/Forward, no git actions, no adapter work, no deployment, no trading, no promotion.
```

This record documents only a narrow inert runtime-history contract scaffolding slice.

It authorizes no provider/API calls, no downloads, no parser execution, no file replay, no diagnostics, no tests/backtests, no OOS, no Lockbox, no Forward, no Git actions, no adapter work, no deployment, no trading, no promotion, no result interpretation, and no source-faithful replay evidence claim.

## Gate Evidence

The prior level-compatibility contract scaffold patch re-audit result is:

```text
docs/process/CARVER_S27_ZN_V2_LEVEL_COMPATIBILITY_CONTRACT_SCAFFOLDING_PATCH_REAUDIT_RESULT_2026-06-06.md
```

That re-audit returned:

```text
PASS
```

## Implemented Scaffolding

Added inert module:

```text
src/carver/spine/s27_v2_replay/runtime_history_contract.py
```

The module defines:

```text
S27_V2_RUNTIME_HISTORY_CONTRACT_ONLY_STATUS
PLANNED_RUNTIME_HISTORY_STATE_STATUS
REQUIRED_RUNTIME_STATE_FAMILIES
REQUIRED_VQM_COMPONENTS
RuntimeHistorySourceBinding
RuntimeStateFamilyContract
VqmComponentContract
RuntimeHistoryContractBundle
```

## Purpose

This slice introduces a structural contract for future runtime-history construction without implementing EWMA, EWMAC, sigma, V/Q/M, forecast, or row-replay calculations.

It locks required runtime state families to:

```text
EWMA5_EQUILIBRIUM_STATE
EWMAC16_64_TREND_STATE
SIGMA_ESTIMATOR_STATE
VQM_HISTORY_STATE
```

It locks required V/Q/M components to:

```text
RELATIVE_VOLATILITY_V
EXPANDING_QUANTILE_Q
RAW_VOLATILITY_MULTIPLIER
EWMA10_MULTIPLIER_M
```

The scaffolding validates only supplied metadata:

- source input manifest hash;
- level-compatibility contract hash;
- daily continuous/current-contract row-family hashes;
- hourly decision row-family hash;
- completed-bar and strict-prior policy hashes;
- runtime state input hashes;
- runtime state definition and policy hashes;
- planned runtime state output hashes;
- V/Q/M component input, policy, planned output, and contract hashes;
- sigma estimator definition hash;
- sigma input-window and annualization policy hashes;
- runtime-history ledger schema hash;
- contract bundle hash;
- non-authorization tuple.

## Preserved Boundaries

The module does not:

- open files;
- read files;
- enumerate paths;
- glob directories;
- parse CSV/PDF/JSON;
- execute parser work;
- execute file replay;
- construct source rows;
- compute EWMA5;
- compute EWMAC16/64;
- compute sigma;
- compute V/Q/M;
- compute forecasts;
- compute strategy rows;
- run diagnostics;
- run tests/backtests;
- call providers/APIs;
- download data;
- start subprocesses;
- invoke Git;
- access OOS, Lockbox, or Forward;
- perform adapter work;
- deploy, trade, promote, or interpret results.

Package-root exports were intentionally not widened. The package root still exposes only the fail-closed runner boundary and non-authorization/status warning constants.

## Next Gate

The next gate is a local hostile audit of this narrow runtime-history contract scaffolding slice.

That audit should be static/source-only unless the operator separately authorizes otherwise.

## Local Hostile Audit Result

The standing local hostile-audit pre-approval rule was applied to this narrow runtime-history contract scaffold. The audit result is:

```text
docs/process/CARVER_S27_ZN_V2_RUNTIME_HISTORY_CONTRACT_SCAFFOLDING_LOCAL_AUDIT_RESULT_2026-06-07.md
```

The audit returned:

```text
PASS
```

Findings:

```text
P0: NONE
P1: NONE
P2: NONE
P3: NONE
```

The next possible implementation slice requires separate explicit operator authorization.

## Static Text-Only Verification

Static text-only verification performed:

```text
STATIC_TEXT_AND_FILE_INVENTORY_ONLY
```

Package file count after this slice:

```text
29
```

Forbidden-surface scan:

```text
rg -n "open\(|read_csv|to_csv|requests|urllib|http|databento|download\(|download |backtest\(|diagnostic\(|subprocess|argparse|if __name__|Path\(|glob\(|os\.|sys\.|socket|git|pytest|unittest" src\carver\spine\s27_v2_replay
```

Result:

```text
NO_MATCHES
```

Package-root export check:

```text
NO_RUNTIME_HISTORY_CONTRACT_EXPORT_FROM_PACKAGE_ROOT
```

No import, compile, test, parser execution, file replay, diagnostics, provider/API call, download, OOS, Lockbox, Forward, Git action, adapter work, deployment, trading, promotion, result interpretation, or source-faithful replay evidence claim was performed.

## Non-Authorizations

This record does not authorize:

- provider/API calls;
- downloads;
- credential use;
- parser execution;
- file replay;
- diagnostics;
- tests;
- backtests;
- OOS access;
- Lockbox access;
- Forward access;
- Git staging;
- Git commits;
- Git pushes;
- PRs;
- adapter work;
- deployment;
- trading;
- promotion;
- tuning after results;
- result interpretation;
- source-faithful replay evidence claims.

Any transition beyond this scaffolding slice requires separate explicit operator authorization.
