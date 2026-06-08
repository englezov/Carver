# S27 ZN V2 Fill Contract Scaffolding Record

Date: 2026-06-07

Status:

```text
PROCESS_ONLY_S27_ZN_V2_FILL_CONTRACT_SCAFFOLDING_NOT_EXECUTION_OR_BACKTEST_AUTHORIZATION
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Authorization Boundary

Operator authorization received:

```text
Operator authorizes S27_V2 next narrow implementation slice scaffolding only, after order_contract.py local audit PASS, no provider/API, no downloads, no parser/file replay execution, no diagnostics, no tests/backtests, no OOS/Lockbox/Forward, no git actions, no adapter work, no deployment, no trading, no promotion.
```

This record documents only a narrow inert fill contract scaffolding slice.

It authorizes no provider/API calls, no downloads, no parser execution, no file replay, no diagnostics, no tests/backtests, no OOS, no Lockbox, no Forward, no Git actions, no adapter work, no deployment, no trading, no promotion, no result interpretation, and no source-faithful replay evidence claim.

## Gate Evidence

The prior order contract scaffold local audit result is:

```text
docs/process/CARVER_S27_ZN_V2_ORDER_CONTRACT_SCAFFOLDING_LOCAL_AUDIT_RESULT_2026-06-07.md
```

That audit returned:

```text
PASS
```

## Implemented Scaffolding

Added inert module:

```text
src/carver/spine/s27_v2_replay/fill_contract.py
```

The module defines:

```text
S27_V2_FILL_CONTRACT_ONLY_STATUS
PLANNED_FILL_COMPONENT_STATUS
REQUIRED_FILL_COMPONENT_FAMILIES
REQUIRED_FILL_PRICE_PROVENANCE_LABELS
REQUIRED_FILL_BRANCH_LABELS
REQUIRED_FILL_INVARIANTS
FillSourceBinding
FillComponentContract
FillPriceProvenanceContract
FillBranchContract
FillInvariantContract
FillContractBundle
```

## Purpose

This slice introduces a structural contract for future fill construction without implementing fill execution.

It locks required fill component families to:

```text
ORDER_PLAN_REFERENCE
WORKING_ORDER_TRANSITION_REFERENCE
NEXT_COMPLETED_HOURLY_FILL_ROW
LIMIT_FILL_PRICE_PROVENANCE
MARKET_FILL_PRICE_PROVENANCE
FILL_QUANTITY_AND_SIDE_BINDING
```

It locks required fill price provenance labels to:

```text
LIMIT_ORDER_PRICE_FROM_FILLED_ORDER
MARKET_PRICE_FROM_NEXT_COMPLETED_CLOSE
```

It locks required fill branch labels to:

```text
LIMIT_FILL
MARKET_FILL
```

It locks required fill invariant proof labels to:

```text
ORDER_CONTRACT_BUNDLE_HASH_BINDING
TRANSITION_HASH_BINDING
EXACT_NEXT_COMPLETED_HOURLY_ROW_BINDING
FILL_TIMESTAMP_IDENTITY_BINDING
LIMIT_FILL_PRICE_EQUALS_SUBMITTED_LIMIT
MARKET_FILL_PRICE_FROM_NEXT_COMPLETED_CLOSE
NO_COST_ACCOUNTING_IN_FILL_CONTRACT
```

The scaffolding validates only supplied metadata:

- source input manifest hash;
- order contract bundle hash;
- limit-order ledger schema hash;
- market-order ledger schema hash;
- working-order transition schema hash;
- fill ledger schema hash;
- completed-bar and strict-prior policy hashes;
- fill component input, definition, policy, planned-output, and contract hashes;
- fill price provenance policy and contract hashes;
- fill branch input, policy, planned-output, and contract hashes;
- fill invariant proof, policy, and contract hashes;
- one-hour lag policy hash;
- session-gap policy hash;
- fill contract bundle hash;
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
- advance working-order state;
- execute fills;
- compute fill prices;
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

The next gate is a local hostile audit of this narrow fill contract scaffolding slice.

That audit should be static/source-only unless the operator separately authorizes otherwise.

## Local Hostile Audit Result

The standing local hostile-audit pre-approval rule was applied to this narrow fill contract scaffold. The audit result is:

```text
docs/process/CARVER_S27_ZN_V2_FILL_CONTRACT_SCAFFOLDING_LOCAL_AUDIT_RESULT_2026-06-07.md
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
33
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
NO_FILL_CONTRACT_EXPORT_FROM_PACKAGE_ROOT
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
