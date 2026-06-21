# S27 ZN V2 PnL Contract Scaffolding Record

Date: 2026-06-07

Status:

```text
PROCESS_ONLY_S27_ZN_V2_PNL_CONTRACT_SCAFFOLDING_NOT_EXECUTION_OR_BACKTEST_AUTHORIZATION
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Authorization Boundary

Operator authorization received:

```text
Operator authorizes S27_V2 next narrow implementation slice scaffolding only, after cost_contract.py local audit PASS, no provider/API, no downloads, no parser/file replay execution, no diagnostics, no tests/backtests, no OOS/Lockbox/Forward, no git actions, no adapter work, no deployment, no trading, no promotion.
```

This record documents only a narrow inert PnL contract scaffolding slice.

It authorizes no provider/API calls, no downloads, no parser execution, no file replay, no diagnostics, no tests/backtests, no OOS, no Lockbox, no Forward, no Git actions, no adapter work, no deployment, no trading, no promotion, no result interpretation, and no source-faithful replay evidence claim.

## Gate Evidence

The prior cost contract scaffold local audit result is:

```text
docs/process/CARVER_S27_ZN_V2_COST_CONTRACT_SCAFFOLDING_LOCAL_AUDIT_RESULT_2026-06-07.md
```

That audit returned:

```text
PASS
```

## Implemented Scaffolding

Added inert module:

```text
src/carver/spine/s27_v2_replay/pnl_contract.py
```

The module defines:

```text
S27_V2_PNL_CONTRACT_ONLY_STATUS
PLANNED_PNL_COMPONENT_STATUS
REQUIRED_PNL_COMPONENT_FAMILIES
REQUIRED_PNL_PRICE_SOURCE_LABELS
REQUIRED_PNL_BRIDGE_LABELS
REQUIRED_PNL_INVARIANTS
PnlSourceBinding
PnlComponentContract
PnlPriceSourceContract
PnlBridgeContract
PnlInvariantContract
PnlContractBundle
```

## Purpose

This slice introduces a structural contract for future PnL construction without implementing PnL arithmetic.

It locks required PnL component families to:

```text
TRUST_ROOT_REFERENCE
TRANSITION_STATE_REFERENCE
POSITION_SOURCE_REFERENCE
CLOSE_ONLY_PRICE_SOURCE_POLICY
RAW_SYMBOL_CONTINUITY_OR_ROLL_BRIDGE
CONTRACT_MULTIPLIER_CURRENCY_POLICY
FILL_COST_APPLICATION
PNL_SUMMARY
```

It locks required PnL price-source labels to:

```text
CLOSE_ONLY
```

It locks required PnL bridge labels to:

```text
RAW_SYMBOL_CONTINUITY
ROLL_BRIDGE
```

It locks required PnL invariant proof labels to:

```text
TRUST_ROOT_HASH_BINDING
PREVIOUS_STEP_OR_INITIAL_STATE_HASH_BINDING
TRANSITION_AND_WORKING_STATE_HASH_BINDING
POSITION_SOURCE_HASH_BINDING
CLOSE_ONLY_START_END_PRICE_ROW_HASH_BINDING
RAW_SYMBOL_CONTINUITY_OR_ROLL_BRIDGE_HASH_BINDING
CONTRACT_MULTIPLIER_SOURCE_BINDING
CURRENCY_POLICY_OPTIONAL_FIELD_BINDING
FILL_HASH_SET_BINDING
COST_HASH_SET_BINDING
PNL_FORMULA_POLICY_BINDING
NO_TARGET_POSITION_SHORTCUT_PNL
NO_RESULT_INTERPRETATION_IN_PNL_CONTRACT
```

The scaffolding validates only supplied metadata:

- replay trust-root hash;
- source input manifest hash;
- transition ledger schema hash;
- fill ledger schema hash;
- cost ledger schema hash;
- PnL ledger schema hash;
- PnL source binding hash;
- PnL component input, definition, policy, planned-output, and contract hashes;
- price-source policy and contract hashes;
- bridge proof, policy, and contract hashes;
- invariant proof, policy, and contract hashes;
- PnL formula policy hash;
- close price source policy hash;
- cost application policy hash;
- contract multiplier policy hash;
- currency policy hash;
- target-position shortcut quarantine policy hash;
- PnL contract bundle hash;
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
- compute costs;
- compute PnL;
- compute returns;
- compute result metrics;
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

The next gate is a local hostile audit of this narrow PnL contract scaffolding slice.

That audit should be static/source-only unless the operator separately authorizes otherwise.

## Local Hostile Audit Result

The standing local hostile-audit pre-approval rule was applied to this narrow PnL contract scaffold. The audit result is:

```text
docs/process/CARVER_S27_ZN_V2_PNL_CONTRACT_SCAFFOLDING_LOCAL_AUDIT_RESULT_2026-06-07.md
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
35
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
NO_PNL_CONTRACT_EXPORT_FROM_PACKAGE_ROOT
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
