# S27 ZN V2 Cost Contract Scaffolding Record

Date: 2026-06-07

Status:

```text
PROCESS_ONLY_S27_ZN_V2_COST_CONTRACT_SCAFFOLDING_NOT_EXECUTION_OR_BACKTEST_AUTHORIZATION
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Authorization Boundary

Operator authorization received:

```text
Operator authorizes S27_V2 next narrow implementation slice scaffolding only, after fill_contract.py local audit PASS, no provider/API, no downloads, no parser/file replay execution, no diagnostics, no tests/backtests, no OOS/Lockbox/Forward, no git actions, no adapter work, no deployment, no trading, no promotion.
```

This record documents only a narrow inert cost contract scaffolding slice.

It authorizes no provider/API calls, no downloads, no parser execution, no file replay, no diagnostics, no tests/backtests, no OOS, no Lockbox, no Forward, no Git actions, no adapter work, no deployment, no trading, no promotion, no result interpretation, and no source-faithful replay evidence claim.

## Gate Evidence

The prior fill contract scaffold local audit result is:

```text
docs/process/CARVER_S27_ZN_V2_FILL_CONTRACT_SCAFFOLDING_LOCAL_AUDIT_RESULT_2026-06-07.md
```

That audit returned:

```text
PASS
```

## Implemented Scaffolding

Added inert module:

```text
src/carver/spine/s27_v2_replay/cost_contract.py
```

The module defines:

```text
S27_V2_COST_CONTRACT_ONLY_STATUS
PLANNED_COST_COMPONENT_STATUS
REQUIRED_COST_COMPONENT_FAMILIES
REQUIRED_COST_BRANCH_LABELS
REQUIRED_SPREAD_SPACE_LABELS
REQUIRED_COST_INVARIANTS
CostSourceBinding
CostComponentContract
CostBranchContract
SpreadSpaceContract
CostInvariantContract
CostContractBundle
```

## Purpose

This slice introduces a structural contract for future cost construction without implementing cost arithmetic.

It locks required cost component families to:

```text
FILL_LEDGER_REFERENCE
COMMISSION_POLICY
LIMIT_FILL_COMMISSION_ONLY_BRANCH
MARKET_FILL_SPREAD_COST_BRANCH
SPREAD_SPACE_POLICY
CONTRACT_MULTIPLIER_CURRENCY_POLICY
TOTAL_COST_SUMMARY
```

It locks required cost branch labels to:

```text
LIMIT_COMMISSION_ONLY
MARKET_COMMISSION_PLUS_SPREAD
```

It locks required spread-space labels to:

```text
PRICE_SPACE
CURRENCY_SPACE
```

It locks required cost invariant proof labels to:

```text
FILL_CONTRACT_BUNDLE_HASH_BINDING
COMMISSION_PER_CONTRACT_TIMES_QUANTITY_BINDING
LIMIT_FILL_ZERO_SPREAD_BINDING
MARKET_FILL_POSITIVE_SPREAD_BINDING
PRICE_SPACE_SPREAD_MULTIPLIER_BINDING
CURRENCY_SPACE_SPREAD_DIRECT_AMOUNT_BINDING
TOTAL_COST_EQUALS_COMMISSION_PLUS_SPREAD_BINDING
NO_PNL_ACCOUNTING_IN_COST_CONTRACT
```

The scaffolding validates only supplied metadata:

- source input manifest hash;
- fill contract bundle hash;
- fill ledger schema hash;
- commission ledger schema hash;
- spread-cost ledger schema hash;
- cost ledger schema hash;
- cost component input, definition, policy, planned-output, and contract hashes;
- cost branch input, policy, planned-output, and contract hashes;
- spread-space policy and contract hashes;
- cost invariant proof, policy, and contract hashes;
- commission policy hash;
- spread policy hash;
- cost calculation policy hash;
- contract multiplier policy hash;
- currency conversion policy hash;
- deflation policy hash;
- cost contract bundle hash;
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
- execute fills;
- compute commission amounts;
- compute spread costs;
- compute total costs;
- compute PnL;
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

The next gate is a local hostile audit of this narrow cost contract scaffolding slice.

That audit should be static/source-only unless the operator separately authorizes otherwise.

## Local Hostile Audit Result

The standing local hostile-audit pre-approval rule was applied to this narrow cost contract scaffold. The audit result is:

```text
docs/process/CARVER_S27_ZN_V2_COST_CONTRACT_SCAFFOLDING_LOCAL_AUDIT_RESULT_2026-06-07.md
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
34
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
NO_COST_CONTRACT_EXPORT_FROM_PACKAGE_ROOT
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
