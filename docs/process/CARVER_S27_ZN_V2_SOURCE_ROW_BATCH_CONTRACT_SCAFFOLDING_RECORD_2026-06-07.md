# S27 ZN V2 Source Row Batch Contract Scaffolding Record

Date: 2026-06-07

Status:

```text
PROCESS_ONLY_S27_ZN_V2_SOURCE_ROW_BATCH_CONTRACT_SCAFFOLDING_RECORD_NOT_EXECUTION_AUTHORIZATION
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Authorization Boundary

Operator authorization received:

```text
Operator authorizes S27_V2 next narrow parser/file replay implementation slice scaffolding only, after parser_output_contract.py local audit PASS, no provider/API, no downloads, no parser/file replay execution, no diagnostics, no tests/backtests, no OOS/Lockbox/Forward, no git actions, no adapter work, no deployment, no trading, no promotion.
```

This record documents only inert parser/file replay scaffolding after the parser output contract local audit PASS. It authorizes no provider/API access, no downloads, no parser execution, no file replay, no diagnostics, no tests/backtests, no OOS, no Lockbox, no Forward, no Git actions, no adapter work, no deployment, no trading, no promotion, no result interpretation, and no source-faithful replay evidence claim.

## Slice Purpose

This slice adds a contract-only source-row batch gate between future parser-output row batches and any later runtime/source-input construction.

It locks that future parser/file replay metadata must prove:

- complete required source-row batch family coverage;
- one planned-only source-row batch family contract per required family;
- source-row schema labels match the locked row family;
- readiness status labels match the locked row family;
- each family is bound to parser-output family contract, parser-output batch, source-row schema hash, readiness-status policy hash, source-universe family contract, row-locator family contract, row-locator policy, row-hash schema, row-ordering policy, duplicate policy, missing policy, completed-bar policy, strict-prior policy, no-future-rows proof, row-count manifest, first/last row-locator manifest, and source-row batch hash;
- aggregate source-row batch-set and source-row batch contract hashes are supplied before future replay can proceed.

## Added Code

Added inert module:

```text
src/carver/spine/s27_v2_replay/source_row_batch_contract.py
```

The module defines:

```text
S27_V2_SOURCE_ROW_BATCH_CONTRACT_ONLY_STATUS
PLANNED_SOURCE_ROW_BATCH_FAMILY_STATUS
REQUIRED_SOURCE_ROW_BATCH_FAMILIES
REQUIRED_SOURCE_ROW_SCHEMA_BY_FAMILY
REQUIRED_READINESS_STATUS_BY_FAMILY
SourceRowBatchFamilyContract
SourceRowBatchSetContract
```

The required source-row batch family tuple is imported from the already locked parser-output family tuple:

```text
REQUIRED_PARSER_OUTPUT_ROW_FAMILIES
```

The scaffold validates supplied metadata only. It does not open paths, enumerate directories, read files, hash files, parse rows, construct source-row objects, build row batches, run replay, run diagnostics, call providers/APIs, download data, or run tests/backtests.

## Static Verification

Static text verification performed:

```text
Get-Content src/carver/spine/s27_v2_replay/source_row_batch_contract.py
rg -n "open\(|read_csv|to_csv|requests|urllib|http|databento|download\(|download |backtest\(|diagnostic\(|subprocess|argparse|if __name__|Path\(|glob\(|os\.|sys\.|socket|git|pytest|unittest|pandas|csv|parquet" src/carver/spine/s27_v2_replay/source_row_batch_contract.py
Select-String src/carver/spine/s27_v2_replay/__init__.py -Pattern "source_row_batch|SourceRowBatch"
rg -n "SourceRowBatch|S27_V2_SOURCE_ROW_BATCH|REQUIRED_SOURCE_ROW_BATCH" src/carver/spine/s27_v2_replay
```

Observed static results:

```text
SOURCE_ROW_BATCH_CONTRACT_ONLY_MODULE_PRESENT
PACKAGE_ROOT_EXPORT_BOUNDARY_UNCHANGED
NO_FORBIDDEN_EXECUTION_PROVIDER_BACKTEST_DIAGNOSTIC_IMPORT_SURFACE_FOUND
NO_DOWNLOAD_EXECUTION_SURFACE_FOUND_ONLY_NO_DOWNLOAD_POLICY_TEXT_MATCHES
```

Python import, compile, unit-test, diagnostic, parser/file replay, and backtest execution were intentionally not run under this authorization.

## Local Hostile Audit

The standing local hostile-audit pre-approval rule was applied to this source row batch contract scaffold. The audit result is:

```text
docs/process/CARVER_S27_ZN_V2_SOURCE_ROW_BATCH_CONTRACT_SCAFFOLDING_LOCAL_AUDIT_RESULT_2026-06-07.md
```

The audit returned `PASS`: no P0/P1/P2/P3 findings.

## Next Gate

The next possible gate is a separately authorized next narrow parser/file replay implementation slice.

No next gate is opened by this scaffolding record or local audit result.
