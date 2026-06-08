# S27 ZN V2 Raw File Hash Contract Scaffolding Record

Date: 2026-06-07

Status:

```text
PROCESS_ONLY_S27_ZN_V2_RAW_FILE_HASH_CONTRACT_SCAFFOLDING_RECORD_NOT_EXECUTION_AUTHORIZATION
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Authorization Boundary

Operator authorization received:

```text
Operator authorizes S27_V2 next narrow parser/file replay implementation slice scaffolding only, no provider/API, no downloads, no parser/file replay execution, no diagnostics, no tests/backtests, no OOS/Lockbox/Forward, no git actions, no adapter work, no deployment, no trading, no promotion.
```

This record documents only inert parser/file replay scaffolding. It authorizes no provider/API access, no downloads, no parser execution, no file replay, no diagnostics, no tests/backtests, no OOS, no Lockbox, no Forward, no Git actions, no adapter work, no deployment, no trading, no promotion, no result interpretation, and no source-faithful replay evidence claim.

## Slice Purpose

This slice adds a contract-only raw source file hash-set gate between local file declarations and future parser/file replay execution.

It locks that future replay metadata must prove:

- complete required raw source file family coverage;
- one hash-bound file declaration per required family;
- no duplicate raw file families;
- each family remains planned-only;
- each binding asserts `NO_PROVIDER_API_NO_DOWNLOAD`;
- expected parser output family matches the locked file family;
- the aggregate raw file hash-set hash is supplied before future replay can proceed.

## Added Code

Added inert module:

```text
src/carver/spine/s27_v2_replay/raw_file_hash_contract.py
```

The module defines:

```text
S27_V2_RAW_FILE_HASH_CONTRACT_ONLY_STATUS
PLANNED_RAW_FILE_HASH_FAMILY_STATUS
REQUIRED_RAW_SOURCE_FILE_FAMILIES
RawSourceFileHashBinding
RawSourceFileHashSetContract
```

The required raw source file family tuple is imported from the already locked row-locator family tuple:

```text
REQUIRED_ROW_LOCATOR_FAMILIES
```

The scaffold validates supplied metadata only. It does not open paths, enumerate directories, read files, hash files, parse rows, construct row locators, run replay, run diagnostics, call providers/APIs, download data, or run tests/backtests.

## Static Verification

Static text verification performed:

```text
Get-Content src/carver/spine/s27_v2_replay/raw_file_hash_contract.py
rg -n "open\(|read_csv|to_csv|requests|urllib|http|databento|download\(|download |backtest\(|diagnostic\(|subprocess|argparse|if __name__|Path\(|glob\(|os\.|sys\.|socket|git|pytest|unittest|pandas|csv|parquet" src/carver/spine/s27_v2_replay/raw_file_hash_contract.py
Select-String src/carver/spine/s27_v2_replay/__init__.py -Pattern "raw_file|RawSource|HashSet|raw_file_hash_contract"
rg -n "RawSourceFileHash|S27_V2_RAW_FILE_HASH|REQUIRED_RAW_SOURCE_FILE_FAMILIES" src/carver/spine/s27_v2_replay
```

Observed static results:

```text
RAW_FILE_HASH_CONTRACT_ONLY_MODULE_PRESENT
PACKAGE_ROOT_EXPORT_BOUNDARY_UNCHANGED
NO_FORBIDDEN_EXECUTION_PROVIDER_BACKTEST_DIAGNOSTIC_IMPORT_SURFACE_FOUND
NO_DOWNLOAD_EXECUTION_SURFACE_FOUND_ONLY_NO_DOWNLOAD_POLICY_TEXT_MATCHES
```

Python import, compile, unit-test, diagnostic, parser/file replay, and backtest execution were intentionally not run under this authorization.

## Next Gate

The next gate is a narrow local hostile audit of this raw file hash contract scaffold under the standing local hostile-audit pre-approval rule.

That audit must remain static/read-only and must not run parser/file replay, diagnostics, tests/backtests, provider/API calls, downloads, OOS, Lockbox, Forward, Git actions, adapter work, deployment, trading, promotion, result interpretation, or source-faithful replay evidence claims.
