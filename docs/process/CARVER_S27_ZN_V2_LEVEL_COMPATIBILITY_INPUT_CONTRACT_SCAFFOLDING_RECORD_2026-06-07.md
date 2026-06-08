# S27 ZN V2 Level Compatibility Input Contract Scaffolding Record

Date: 2026-06-07

Status:

```text
PROCESS_ONLY_S27_ZN_V2_LEVEL_COMPATIBILITY_INPUT_CONTRACT_SCAFFOLDING_RECORD_NOT_EXECUTION_AUTHORIZATION
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Authorization Boundary

Operator authorization received:

```text
Operator authorizes S27_V2 next narrow parser/file replay implementation slice scaffolding only, after source_input_manifest_contract.py local audit PASS, no provider/API, no downloads, no parser/file replay execution, no diagnostics, no tests/backtests, no OOS/Lockbox/Forward, no git actions, no adapter work, no deployment, no trading, no promotion.
```

This record documents only inert parser/file replay scaffolding after the source input manifest contract local audit PASS. It authorizes no provider/API access, no downloads, no parser execution, no file replay, no diagnostics, no tests/backtests, no OOS, no Lockbox, no Forward, no Git actions, no adapter work, no deployment, no trading, no promotion, no result interpretation, and no source-faithful replay evidence claim.

## Slice Purpose

This slice adds a contract-only level-compatibility input gate between the future source-input manifest and any later daily/hourly level-compatibility proof construction.

It locks that future parser/file replay metadata must prove:

- complete required level-compatibility input coverage;
- one planned-only input field contract per required level-compatibility input;
- each input maps to the locked source-input manifest field and source-input role;
- each input is bound to manifest field contract hash, selected row hash, selected row locator hash, level-compatibility input policy, price-level-space policy, completed-bar policy, strict-prior policy, no-future-rows proof, and input field contract hash;
- each locked level-compatibility proof label maps to the exact required input labels and input field contract hashes;
- aggregate level-compatibility input set and input contract hashes are supplied before future level-compatibility proof construction can proceed.

## Added Code

Added inert module:

```text
src/carver/spine/s27_v2_replay/level_compatibility_input_contract.py
```

The module defines:

```text
S27_V2_LEVEL_COMPATIBILITY_INPUT_CONTRACT_ONLY_STATUS
PLANNED_LEVEL_COMPATIBILITY_INPUT_STATUS
REQUIRED_LEVEL_COMPATIBILITY_INPUTS
REQUIRED_MANIFEST_FIELD_BY_LEVEL_COMPATIBILITY_INPUT
REQUIRED_LEVEL_COMPATIBILITY_INPUTS_BY_PROOF
LevelCompatibilityInputFieldContract
LevelCompatibilityProofInputBindingContract
LevelCompatibilityInputContractBundle
```

The required source-input manifest field tuple, source-input role tuple, and required level-compatibility proof tuple are imported from the already locked contracts:

```text
REQUIRED_SOURCE_INPUT_MANIFEST_FIELDS
REQUIRED_SOURCE_INPUT_ROLES
REQUIRED_LEVEL_COMPATIBILITY_PROOFS
```

The scaffold validates supplied metadata only. It does not open paths, enumerate directories, read files, hash files, parse rows, select rows, compare price levels, construct compatibility proofs, build runtime rows, run replay, run diagnostics, call providers/APIs, download data, or run tests/backtests.

## Static Verification

Static text verification performed:

```text
Get-Content src/carver/spine/s27_v2_replay/level_compatibility_input_contract.py
rg -n "open\(|read_csv|to_csv|requests|urllib|http|databento|download\(|download |backtest\(|diagnostic\(|subprocess|argparse|if __name__|Path\(|glob\(|os\.|sys\.|socket|git|pytest|unittest|pandas|csv|parquet" src/carver/spine/s27_v2_replay/level_compatibility_input_contract.py
Select-String src/carver/spine/s27_v2_replay/__init__.py -Pattern "level_compatibility_input|LevelCompatibilityInput"
rg -n "LevelCompatibilityInput|S27_V2_LEVEL_COMPATIBILITY_INPUT|REQUIRED_LEVEL_COMPATIBILITY_INPUT" src/carver/spine/s27_v2_replay
```

Observed static results:

```text
LEVEL_COMPATIBILITY_INPUT_CONTRACT_ONLY_MODULE_PRESENT
PACKAGE_ROOT_EXPORT_BOUNDARY_UNCHANGED
NO_FORBIDDEN_EXECUTION_PROVIDER_BACKTEST_DIAGNOSTIC_IMPORT_SURFACE_FOUND
NO_DOWNLOAD_EXECUTION_SURFACE_FOUND_ONLY_NO_DOWNLOAD_POLICY_TEXT_MATCHES
```

Python import, compile, unit-test, diagnostic, parser/file replay, and backtest execution were intentionally not run under this authorization.

## Next Gate

The standing local hostile-audit pre-approval rule was applied to this level compatibility input contract scaffold. The audit result is:

```text
docs/process/CARVER_S27_ZN_V2_LEVEL_COMPATIBILITY_INPUT_CONTRACT_SCAFFOLDING_LOCAL_AUDIT_RESULT_2026-06-07.md
```

The audit returned `PASS`: no P0/P1/P2/P3 findings.

The next possible gate is a separately authorized next narrow parser/file replay implementation slice.

No next gate is opened by this scaffolding record or local audit result.
