# S27 ZN V2 Source Input Manifest Contract Scaffolding Record

Date: 2026-06-07

Status:

```text
PROCESS_ONLY_S27_ZN_V2_SOURCE_INPUT_MANIFEST_CONTRACT_SCAFFOLDING_RECORD_NOT_EXECUTION_AUTHORIZATION
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Authorization Boundary

Operator authorization received:

```text
Operator authorizes S27_V2 next narrow parser/file replay implementation slice scaffolding only, after source_input_selection_contract.py local audit PASS, no provider/API, no downloads, no parser/file replay execution, no diagnostics, no tests/backtests, no OOS/Lockbox/Forward, no git actions, no adapter work, no deployment, no trading, no promotion.
```

This record documents only inert parser/file replay scaffolding after the source input selection contract local audit PASS. It authorizes no provider/API access, no downloads, no parser execution, no file replay, no diagnostics, no tests/backtests, no OOS, no Lockbox, no Forward, no Git actions, no adapter work, no deployment, no trading, no promotion, no result interpretation, and no source-faithful replay evidence claim.

## Slice Purpose

This slice adds a contract-only source-input manifest gate between future source-input role selections and any later level-compatibility, runtime-history, or source-input manifest construction.

It locks that future parser/file replay metadata must prove:

- complete required source-input manifest field coverage;
- one planned-only manifest field contract per required field;
- each manifest field maps to the locked source-input role;
- each field is bound to source-input role contract, selected row hash, selected row locator hash, field policy, canonical field serialization, completed-bar policy, strict-prior policy, no-future-rows proof, and field contract hash;
- aggregate source-input manifest schema, manifest, and manifest contract hashes are supplied before future replay can proceed.

## Added Code

Added inert module:

```text
src/carver/spine/s27_v2_replay/source_input_manifest_contract.py
```

The module defines:

```text
S27_V2_SOURCE_INPUT_MANIFEST_CONTRACT_ONLY_STATUS
PLANNED_SOURCE_INPUT_MANIFEST_FIELD_STATUS
REQUIRED_SOURCE_INPUT_MANIFEST_FIELDS
REQUIRED_SOURCE_INPUT_ROLE_BY_MANIFEST_FIELD
SourceInputManifestFieldContract
SourceInputManifestContractBundle
```

The required source-input role tuple is imported from the already locked source-input selection tuple:

```text
REQUIRED_SOURCE_INPUT_ROLES
```

The scaffold validates supplied metadata only. It does not open paths, enumerate directories, read files, hash files, parse rows, select rows, construct source-input manifest rows, build runtime rows, run replay, run diagnostics, call providers/APIs, download data, or run tests/backtests.

## Static Verification

Static text verification performed:

```text
Get-Content src/carver/spine/s27_v2_replay/source_input_manifest_contract.py
rg -n "open\(|read_csv|to_csv|requests|urllib|http|databento|download\(|download |backtest\(|diagnostic\(|subprocess|argparse|if __name__|Path\(|glob\(|os\.|sys\.|socket|git|pytest|unittest|pandas|csv|parquet" src/carver/spine/s27_v2_replay/source_input_manifest_contract.py
Select-String src/carver/spine/s27_v2_replay/__init__.py -Pattern "source_input_manifest_contract|SourceInputManifestContract"
rg -n "SourceInputManifestContract|SourceInputManifestField|S27_V2_SOURCE_INPUT_MANIFEST|REQUIRED_SOURCE_INPUT_MANIFEST" src/carver/spine/s27_v2_replay
```

Observed static results:

```text
SOURCE_INPUT_MANIFEST_CONTRACT_ONLY_MODULE_PRESENT
PACKAGE_ROOT_EXPORT_BOUNDARY_UNCHANGED
NO_FORBIDDEN_EXECUTION_PROVIDER_BACKTEST_DIAGNOSTIC_IMPORT_SURFACE_FOUND
NO_DOWNLOAD_EXECUTION_SURFACE_FOUND_ONLY_NO_DOWNLOAD_POLICY_TEXT_MATCHES
```

Python import, compile, unit-test, diagnostic, parser/file replay, and backtest execution were intentionally not run under this authorization.

## Local Hostile Audit

The standing local hostile-audit pre-approval rule was applied to this source input manifest contract scaffold. The audit result is:

```text
docs/process/CARVER_S27_ZN_V2_SOURCE_INPUT_MANIFEST_CONTRACT_SCAFFOLDING_LOCAL_AUDIT_RESULT_2026-06-07.md
```

The audit returned `PASS`: no P0/P1/P2/P3 findings.

## Next Gate

The next possible gate is a separately authorized next narrow parser/file replay implementation slice.

No next gate is opened by this scaffolding record or local audit result.
