# S27 ZN V2 Order Contract Scaffolding Record

Date: 2026-06-07

Status:

```text
PROCESS_ONLY_S27_ZN_V2_ORDER_CONTRACT_SCAFFOLDING_NOT_EXECUTION_OR_BACKTEST_AUTHORIZATION
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Authorization Boundary

Operator authorization received:

```text
Operator authorizes S27_V2 next narrow implementation slice scaffolding only, after position_contract.py local audit PASS, no provider/API, no downloads, no parser/file replay execution, no diagnostics, no tests/backtests, no OOS/Lockbox/Forward, no git actions, no adapter work, no deployment, no trading, no promotion.
```

This record documents only a narrow inert order contract scaffolding slice.

It authorizes no provider/API calls, no downloads, no parser execution, no file replay, no diagnostics, no tests/backtests, no OOS, no Lockbox, no Forward, no Git actions, no adapter work, no deployment, no trading, no promotion, no result interpretation, and no source-faithful replay evidence claim.

## Gate Evidence

The prior position contract scaffold local audit result is:

```text
docs/process/CARVER_S27_ZN_V2_POSITION_CONTRACT_SCAFFOLDING_LOCAL_AUDIT_RESULT_2026-06-07.md
```

That audit returned:

```text
PASS
```

## Implemented Scaffolding

Added inert module:

```text
src/carver/spine/s27_v2_replay/order_contract.py
```

The module defines:

```text
S27_V2_ORDER_CONTRACT_ONLY_STATUS
PLANNED_ORDER_COMPONENT_STATUS
REQUIRED_ORDER_COMPONENT_FAMILIES
REQUIRED_ORDER_KIND_LABELS
REQUIRED_ORDER_TRANSITION_KIND_LABELS
REQUIRED_ORDER_INVARIANTS
OrderSourceBinding
OrderComponentContract
OrderKindContract
OrderTransitionKindContract
OrderInvariantContract
OrderContractBundle
```

## Purpose

This slice introduces a structural contract for future order-plan construction without implementing order generation or fill execution.

It locks required order component families to:

```text
LIMIT_ORDER_PLAN
MARKET_ORDER_PLAN
ADJACENT_POSITION_LIMIT_LADDER
TICK_ROUNDING_POLICY
WORKING_ORDER_STATE_REFERENCE
TRANSITION_KIND_REFERENCE
```

It locks required order kind labels to:

```text
LIMIT
MARKET
```

It locks required working-order transition kind labels to:

```text
NORMAL_ONE_HOUR_LAG
EOD_OVERNIGHT_RECOMPUTE
ROLL_BOUNDARY
```

It locks required order invariant proof labels to:

```text
DESIRED_POSITION_LEDGER_HASH_BINDING
CURRENT_POSITION_STATE_HASH_BINDING
ADJACENT_LIMIT_SINGLE_LOT_BINDING
MARKET_ORDER_DELTA_QUANTITY_BINDING
TICK_ROUNDING_POLICY_BINDING
NO_FILL_EXECUTION_IN_ORDER_CONTRACT
```

The scaffolding validates only supplied metadata:

- source input manifest hash;
- position contract bundle hash;
- desired-position ledger schema hash;
- limit-order ledger schema hash;
- market-order ledger schema hash;
- working-order transition schema hash;
- completed-bar and strict-prior policy hashes;
- order component input, definition, policy, planned-output, and contract hashes;
- order kind policy and contract hashes;
- transition kind policy and contract hashes;
- order invariant proof, policy, and contract hashes;
- tick-rounding policy hash;
- working-limit lifecycle policy hash;
- overnight recompute policy hash;
- roll-boundary policy hash;
- order contract bundle hash;
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
- compute forecasts;
- compute positions;
- generate orders;
- price limit orders;
- round ticks;
- advance working-order state;
- execute fills;
- compute costs or PnL;
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

The next gate is a local hostile audit of this narrow order contract scaffolding slice.

That audit should be static/source-only unless the operator separately authorizes otherwise.

## Local Hostile Audit Result

The standing local hostile-audit pre-approval rule was applied to this narrow order contract scaffold. The audit result is:

```text
docs/process/CARVER_S27_ZN_V2_ORDER_CONTRACT_SCAFFOLDING_LOCAL_AUDIT_RESULT_2026-06-07.md
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
32
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
NO_ORDER_CONTRACT_EXPORT_FROM_PACKAGE_ROOT
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
