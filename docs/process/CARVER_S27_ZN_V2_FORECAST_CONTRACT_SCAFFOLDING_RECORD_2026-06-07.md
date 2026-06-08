# S27 ZN V2 Forecast Contract Scaffolding Record

Date: 2026-06-07

Status:

```text
PROCESS_ONLY_S27_ZN_V2_FORECAST_CONTRACT_SCAFFOLDING_NOT_EXECUTION_OR_BACKTEST_AUTHORIZATION
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Authorization Boundary

Operator authorization received:

```text
Operator authorizes S27_V2 next narrow implementation slice scaffolding only, after runtime_history_contract.py local audit PASS, no provider/API, no downloads, no parser/file replay execution, no diagnostics, no tests/backtests, no OOS/Lockbox/Forward, no git actions, no adapter work, no deployment, no trading, no promotion.
```

This record documents only a narrow inert forecast contract scaffolding slice.

It authorizes no provider/API calls, no downloads, no parser execution, no file replay, no diagnostics, no tests/backtests, no OOS, no Lockbox, no Forward, no Git actions, no adapter work, no deployment, no trading, no promotion, no result interpretation, and no source-faithful replay evidence claim.

## Gate Evidence

The prior runtime-history contract scaffold local audit result is:

```text
docs/process/CARVER_S27_ZN_V2_RUNTIME_HISTORY_CONTRACT_SCAFFOLDING_LOCAL_AUDIT_RESULT_2026-06-07.md
```

That audit returned:

```text
PASS
```

## Implemented Scaffolding

Added inert module:

```text
src/carver/spine/s27_v2_replay/forecast_contract.py
```

The module defines:

```text
S27_V2_FORECAST_CONTRACT_ONLY_STATUS
PLANNED_FORECAST_COMPONENT_STATUS
REQUIRED_FORECAST_COMPONENT_FAMILIES
REQUIRED_FORECAST_DECISION_BRANCHES
REQUIRED_FORECAST_INVARIANTS
ForecastSourceBinding
ForecastComponentContract
ForecastDecisionBranchContract
ForecastInvariantContract
ForecastContractBundle
```

## Purpose

This slice introduces a structural contract for future forecast replay construction without implementing forecast arithmetic.

It locks required forecast component families to:

```text
RAW_MEAN_REVERSION_FORECAST
SIGMA_PRICE_BRIDGE
EWMAC16_64_TREND_GATE
VQM_MULTIPLIER_APPLICATION
SCALAR_AND_CAP_APPLICATION
DESIRED_POSITION_REFERENCE
```

It locks required forecast decision branches to:

```text
PERMIT_MEAN_REVERSION
ZERO_FORECAST_BY_TREND_VETO
FLAT_AT_EQUILIBRIUM
```

It locks required forecast invariant proof labels to:

```text
STRICT_PRIOR_RUNTIME_INPUTS
COMPLETED_BAR_FORECAST_TIMESTAMP
POSITIVE_SIGMA_AND_PRICE_INPUTS
ZERO_EQUILIBRIUM_FLAT_BRANCH
TREND_VETO_SIGN_GATE
POST_VETO_VQM_MULTIPLIER_BINDING
SCALAR_CAP_BINDING
DESIRED_POSITION_REFERENCE_BINDING
```

The scaffolding validates only supplied metadata:

- source input manifest hash;
- runtime-history contract bundle hash;
- runtime-history ledger schema hash;
- forecast ledger schema hash;
- completed-bar and strict-prior policy hashes;
- forecast component input, definition, policy, planned-output, and contract hashes;
- forecast decision-branch input, policy, planned-output, and contract hashes;
- forecast invariant proof, policy, and contract hashes;
- scalar source-lock hash;
- cap policy hash;
- desired-position link policy hash;
- forecast contract bundle hash;
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
- compute raw mean-reversion forecasts;
- compute trend-veto decisions;
- compute scalar application;
- compute capped forecasts;
- compute desired positions;
- compute orders, fills, costs, or PnL;
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

The next gate is a local hostile audit of this narrow forecast contract scaffolding slice.

That audit should be static/source-only unless the operator separately authorizes otherwise.

## Local Hostile Audit Result

The standing local hostile-audit pre-approval rule was applied to this narrow forecast contract scaffold. The audit result is:

```text
docs/process/CARVER_S27_ZN_V2_FORECAST_CONTRACT_SCAFFOLDING_LOCAL_AUDIT_RESULT_2026-06-07.md
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
30
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
NO_FORECAST_CONTRACT_EXPORT_FROM_PACKAGE_ROOT
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
