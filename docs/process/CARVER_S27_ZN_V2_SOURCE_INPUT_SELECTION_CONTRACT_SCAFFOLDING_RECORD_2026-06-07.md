# S27 ZN V2 Source Input Selection Contract Scaffolding Record

Date: 2026-06-07

Status:

```text
PROCESS_ONLY_S27_ZN_V2_SOURCE_INPUT_SELECTION_CONTRACT_SCAFFOLDING_RECORD_NOT_EXECUTION_AUTHORIZATION
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Authorization Boundary

Operator authorization received:

```text
Operator authorizes S27_V2 next narrow parser/file replay implementation slice scaffolding only, after source_row_batch_contract.py local audit PASS, no provider/API, no downloads, no parser/file replay execution, no diagnostics, no tests/backtests, no OOS/Lockbox/Forward, no git actions, no adapter work, no deployment, no trading, no promotion.
```

This record documents only inert parser/file replay scaffolding after the source row batch contract local audit PASS. It authorizes no provider/API access, no downloads, no parser execution, no file replay, no diagnostics, no tests/backtests, no OOS, no Lockbox, no Forward, no Git actions, no adapter work, no deployment, no trading, no promotion, no result interpretation, and no source-faithful replay evidence claim.

## Slice Purpose

This slice adds a contract-only source-input selection gate between future source-row batches and any later source-input manifest, level-compatibility, or runtime-history construction.

It locks that future parser/file replay metadata must prove:

- complete required source-input role coverage;
- one planned-only source-input role selection contract per required role;
- each role maps to the locked source-row batch family;
- selected row hashes and row-locator hashes are policy-bound metadata, not executable selection output;
- each role is bound to source-row batch family contract, source-row batch, row-selector policy, row-locator policy, selected-row timestamp policy, completed-bar policy, strict-prior policy, no-future-rows proof, and role contract hash;
- aggregate source-input selection set and source-input selection contract hashes are supplied before future replay can proceed.

## Added Code

Added inert module:

```text
src/carver/spine/s27_v2_replay/source_input_selection_contract.py
```

The module defines:

```text
S27_V2_SOURCE_INPUT_SELECTION_CONTRACT_ONLY_STATUS
PLANNED_SOURCE_INPUT_ROLE_STATUS
REQUIRED_SOURCE_INPUT_ROLES
REQUIRED_SOURCE_ROW_FAMILY_BY_INPUT_ROLE
SourceInputRoleSelectionContract
SourceInputSelectionContractBundle
```

The required source-row family tuple is imported from the already locked source-row batch family tuple:

```text
REQUIRED_SOURCE_ROW_BATCH_FAMILIES
```

The scaffold validates supplied metadata only. It does not open paths, enumerate directories, read files, hash files, parse rows, select rows, construct source-input manifest rows, build runtime rows, run replay, run diagnostics, call providers/APIs, download data, or run tests/backtests.

## Static Verification

Static text verification performed:

```text
Get-Content src/carver/spine/s27_v2_replay/source_input_selection_contract.py
rg -n "open\(|read_csv|to_csv|requests|urllib|http|databento|download\(|download |backtest\(|diagnostic\(|subprocess|argparse|if __name__|Path\(|glob\(|os\.|sys\.|socket|git|pytest|unittest|pandas|csv|parquet" src/carver/spine/s27_v2_replay/source_input_selection_contract.py
Select-String src/carver/spine/s27_v2_replay/__init__.py -Pattern "source_input_selection|SourceInputSelection"
rg -n "SourceInputSelection|SourceInputRoleSelection|S27_V2_SOURCE_INPUT_SELECTION|REQUIRED_SOURCE_INPUT_ROLES" src/carver/spine/s27_v2_replay
```

Observed static results:

```text
SOURCE_INPUT_SELECTION_CONTRACT_ONLY_MODULE_PRESENT
PACKAGE_ROOT_EXPORT_BOUNDARY_UNCHANGED
NO_FORBIDDEN_EXECUTION_PROVIDER_BACKTEST_DIAGNOSTIC_IMPORT_SURFACE_FOUND
NO_DOWNLOAD_EXECUTION_SURFACE_FOUND_ONLY_NO_DOWNLOAD_POLICY_TEXT_MATCHES
```

Python import, compile, unit-test, diagnostic, parser/file replay, and backtest execution were intentionally not run under this authorization.

## Local Hostile Audit

The standing local hostile-audit pre-approval rule was applied to this source input selection contract scaffold. The audit result is:

```text
docs/process/CARVER_S27_ZN_V2_SOURCE_INPUT_SELECTION_CONTRACT_SCAFFOLDING_LOCAL_AUDIT_RESULT_2026-06-07.md
```

The audit returned `PASS`: no P0/P1/P2/P3 findings.

## Next Gate

The next possible gate is a separately authorized next narrow parser/file replay implementation slice.

No next gate is opened by this scaffolding record or local audit result.
