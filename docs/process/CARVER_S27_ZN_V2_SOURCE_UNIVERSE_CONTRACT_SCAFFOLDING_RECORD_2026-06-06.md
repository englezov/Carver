# S27 ZN V2 Source Universe Contract Scaffolding Record

Date: 2026-06-06

Status:

```text
PROCESS_ONLY_S27_ZN_V2_SOURCE_UNIVERSE_CONTRACT_SCAFFOLDING_NOT_EXECUTION_OR_BACKTEST_AUTHORIZATION
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

This record documents only a narrow inert source-universe contract scaffolding slice.

It authorizes no provider/API calls, no downloads, no parser execution, no file replay, no diagnostics, no tests/backtests, no OOS, no Lockbox, no Forward, no Git actions, no adapter work, no deployment, no trading, no promotion, no result interpretation, and no source-faithful replay evidence claim.

## Gate Evidence

The prior row-locator contract scaffold local audit result is:

```text
docs/process/CARVER_S27_ZN_V2_ROW_LOCATOR_CONTRACT_SCAFFOLDING_LOCAL_AUDIT_RESULT_2026-06-06.md
```

That audit returned:

```text
PASS
```

## Implemented Scaffolding

Added inert module:

```text
src/carver/spine/s27_v2_replay/source_universe_contract.py
```

The module defines:

```text
S27_V2_SOURCE_UNIVERSE_CONTRACT_ONLY_STATUS
PLANNED_SOURCE_UNIVERSE_FAMILY_STATUS
REQUIRED_SOURCE_UNIVERSE_FAMILIES
SourceUniverseInclusionRule
SourceUniverseFamilyContract
SourceUniverseContractBundle
```

## Purpose

This slice introduces a structural contract for future source-universe construction without implementing construction, parsing, filtering, or file access.

It locks required source-universe families to:

```text
INSTRUMENT_UNIVERSE
RAW_SYMBOL_UNIVERSE
DAILY_ROW_UNIVERSE
HOURLY_DECISION_FILL_ROW_UNIVERSE
SESSION_ROW_UNIVERSE
ROLL_ROW_UNIVERSE
COST_PARAMETER_ROW_UNIVERSE
```

The scaffolding validates only supplied metadata:

- strategy id `S27_V2_ZN`;
- lane `SOURCE_NATIVE_FUTURES`;
- instrument `ZN`;
- requested start/end date shape and order;
- raw file hash-set hash;
- row locator contract bundle hash;
- strict-prior candidate-set hash;
- canonical row-locator serialization hash;
- inclusion/exclusion reason-code hashes;
- duplicate, missing, repair/rejection, and no-future-row policy hashes;
- planned universe hashes;
- family contract hashes;
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
- construct source universes;
- filter rows;
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

The next gate is a local hostile audit of this narrow source-universe contract scaffolding slice.

That audit should be static/source-only unless the operator separately authorizes otherwise.

## Local Hostile Audit Result

The standing local hostile-audit pre-approval rule was applied to audit this narrow source-universe contract scaffolding slice. The audit result is:

```text
docs/process/CARVER_S27_ZN_V2_SOURCE_UNIVERSE_CONTRACT_SCAFFOLDING_LOCAL_AUDIT_RESULT_2026-06-06.md
```

The audit returned `PASS`: no P0/P1/P2/P3 findings. It confirmed `source_universe_contract.py` is inert structural scaffolding only, the package root remains fail-closed, no forbidden execution or IO surface was found, required source-universe families are locked, no rows or universes are constructed, and non-authorizations are preserved.

The next possible implementation slice still requires separate explicit operator authorization.

## Static Text-Only Verification

Static text-only verification performed:

```text
STATIC_TEXT_AND_FILE_INVENTORY_ONLY
```

Package file count after this slice:

```text
27
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
NO_SOURCE_UNIVERSE_CONTRACT_EXPORT_FROM_PACKAGE_ROOT
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
