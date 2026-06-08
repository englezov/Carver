# S27 ZN V2 Row Locator Contract Scaffolding Record

Date: 2026-06-06

Status:

```text
PROCESS_ONLY_S27_ZN_V2_ROW_LOCATOR_CONTRACT_SCAFFOLDING_NOT_EXECUTION_OR_BACKTEST_AUTHORIZATION
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

This record documents only a narrow inert row-locator contract scaffolding slice.

It authorizes no provider/API calls, no downloads, no parser execution, no file replay, no diagnostics, no tests/backtests, no OOS, no Lockbox, no Forward, no Git actions, no adapter work, no deployment, no trading, no promotion, no result interpretation, and no source-faithful replay evidence claim.

## Gate Evidence

The prior construction-contract scaffold local audit result is:

```text
docs/process/CARVER_S27_ZN_V2_PARSER_FILE_REPLAY_NEXT_IMPLEMENTATION_SLICE_SCAFFOLDING_LOCAL_AUDIT_RESULT_2026-06-06.md
```

That audit returned:

```text
PASS
```

## Implemented Scaffolding

Added inert module:

```text
src/carver/spine/s27_v2_replay/row_locator_contract.py
```

The module defines:

```text
S27_V2_ROW_LOCATOR_CONTRACT_ONLY_STATUS
PLANNED_ROW_LOCATOR_FAMILY_STATUS
REQUIRED_ROW_LOCATOR_FAMILIES
RowLocatorFieldBinding
SourceRowFamilyLocatorContract
SourceRowLocatorContractBundle
```

## Purpose

This slice introduces a structural contract for future source row locator construction without implementing construction, parsing, or file access.

It locks required source row locator families to:

```text
DAILY_CONTINUOUS_COMPLETED_BAR
DAILY_CURRENT_CONTRACT_COMPLETED_BAR
HOURLY_DECISION_COMPLETED_BAR
HOURLY_FILL_COMPLETED_BAR
SESSION_CALENDAR
ROLL_CALENDAR
COST_PARAMETER
```

The scaffolding validates only supplied metadata:

- row-family labels;
- raw-symbol family labels;
- locator component names;
- timestamp and trading-date locator component membership;
- raw-file declaration hashes;
- parser family plan hashes;
- completed-bar, strict-prior, duplicate, missing, no-future-row, canonical-serialization, and row-locator policy hashes;
- planned row-universe hashes;
- planned locator output hashes;
- bundle hash;
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

The next gate is a local hostile audit of this narrow row-locator contract scaffolding slice.

That audit should be static/source-only unless the operator separately authorizes otherwise.

## Local Hostile Audit Result

The standing local hostile-audit pre-approval rule was applied to audit this narrow row-locator contract scaffolding slice. The audit result is:

```text
docs/process/CARVER_S27_ZN_V2_ROW_LOCATOR_CONTRACT_SCAFFOLDING_LOCAL_AUDIT_RESULT_2026-06-06.md
```

The audit returned `PASS`: no P0/P1/P2/P3 findings. It confirmed `row_locator_contract.py` is inert structural scaffolding only, the package root remains fail-closed, no forbidden execution or IO surface was found, required row locator families are locked, no rows are constructed, and non-authorizations are preserved.

The next possible implementation slice still requires separate explicit operator authorization.

## Static Text-Only Verification

Static text-only verification performed:

```text
STATIC_TEXT_AND_FILE_INVENTORY_ONLY
```

Package file count after this slice:

```text
26
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
NO_ROW_LOCATOR_CONTRACT_EXPORT_FROM_PACKAGE_ROOT
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
