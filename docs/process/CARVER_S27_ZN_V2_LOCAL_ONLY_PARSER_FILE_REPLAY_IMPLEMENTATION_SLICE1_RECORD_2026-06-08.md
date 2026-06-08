# S27 ZN V2 Local-Only Parser/File Replay Implementation Slice 1 Record

Date: 2026-06-08

Status:

```text
PROCESS_ONLY_S27_V2_LOCAL_ONLY_PARSER_FILE_REPLAY_IMPLEMENTATION_SLICE1_RECORD_NOT_SOURCE_FAITHFUL_REPLAY_EVIDENCE
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Authorization

The operator authorized `S27_V2_LOCAL_ONLY_PARSER_FILE_REPLAY_IMPLEMENTATION_SLICE_1`, limited to controlled local-only implementation code and local verification for declared S27 V2 ZN input files under the audited construction-interface and implementation-boundary scaffolds.

This record does not broaden that authorization.

## Implemented Scope

The first implementation slice added:

```text
src/carver/spine/s27_v2_replay/local_replay.py
```

The module provides a bounded local-only construction path for declared files:

- validates `ReplayInputDirectoryDeclaration`;
- reads only raw files declared by `ReplayInputDirectoryDeclaration.raw_source_files`;
- resolves relative declarations under `ReplayInputDirectoryDeclaration.declared_path`;
- rejects declared paths that escape the declared input directory;
- computes SHA256 over the exact declared local file bytes;
- fails closed on declared SHA mismatch;
- parses locked CSV headers into existing structural source-row dataclasses;
- computes deterministic content-bound row and batch hashes;
- constructs early local replay artifacts only:
  - `RawSourceFileHashSetContract`;
  - `ParserOutputBatchSetContract`;
  - `SourceRowBatchSetContract`.

The implementation does not call providers, download data, run backtests, score results, access OOS/Lockbox/Forward, stage/commit/push Git changes, or claim source-faithful replay evidence.

## Local Verification

The local verification file is:

```text
tests/test_s27_v2_local_replay_slice1.py
```

The verification uses temporary synthetic CSV files only. It does not read repo research data, provider files, OOS, Lockbox, or Forward data.

Verified behavior:

- declared byte SHA matching for local files;
- parsing of all locked row families into structural source-row dataclasses;
- construction of raw-file hash, parser-output, and source-row-batch contracts;
- fail-closed behavior when a declared file is modified after declaration.

Commands run:

```text
python -m py_compile src\carver\spine\s27_v2_replay\local_replay.py tests\test_s27_v2_local_replay_slice1.py
python -m pytest tests\test_s27_v2_local_replay_slice1.py -q
```

Observed local verification result:

```text
17 passed
```

## Local Audit Finding Patch

The first local hostile audit found two scoped P2 issues:

- declared CSV rows with extra trailing cells could pass header validation and be parsed while ignoring the extra cell;
- the first-slice input authority checks did not require the computed raw-file hash-set authority to match the declared raw-file hash-set authority used by source-universe and row-locator contracts.

The patch tightened the local-only implementation:

- CSV row width must now match the locked row-family columns exactly;
- missing row fields fail closed;
- malformed timestamps and numeric fields now raise `CarverBlocked`;
- input declarations, row-locator contract, source-universe contract, and canonical policy must bind consistently;
- the computed raw-file hash set must match `ReplayInputDirectoryDeclaration.raw_file_hash_set_hash`;
- regression tests cover extra trailing CSV cells and stale raw-file hash-set authority.

The first local hostile re-audit confirmed the row-width patch and top-level raw-file hash-set patch, but found that lower-level public builders still accepted stale upstream contracts if called directly. A second patch added active-input binding checks to:

- `build_parser_output_contract`;
- `build_source_row_batch_contract`.

Regression tests now cover direct stale raw-file-hash and parser-output contract calls.

The second local hostile re-audit found that helper-level top fields were bound but internally stale child contracts could still be accepted. A third patch now requires public lower-level builders to compare supplied upstream contracts against deterministic contracts regenerated from active inputs and parsed rows. Regression tests cover internally stale raw-file hash bindings and parser-output family contracts.

The third local hostile re-audit found the remaining stale-child path in row-locator and source-universe input bundles. A fourth patch added deterministic content-bound checks for row-locator family hashes, row-locator bundle hash, source-universe family hashes, and source-universe bundle hash before those upstream child hashes can be consumed by this slice. Regression tests cover internally stale row-locator and source-universe family contracts with unchanged top-level bundle hashes.

The fourth local hostile re-audit found that public lower-level builders still accepted caller-forged `ParsedDeclaredSourceFile` objects if those objects were internally consistent. A fifth patch requires lower-level public builders to re-read the declared local files and reject parsed-file tuples that do not exactly match the declared bytes. Regression tests cover forged parsed rows passed directly to parser-output and source-row-batch builders.

The fifth local hostile re-audit found the same declared-byte proof gap in `build_raw_file_hash_set_contract`. A sixth patch applies the declared-byte proof to the raw-file-hash builder as well. Regression tests now cover forged parsed rows passed directly to raw-file-hash, parser-output, and source-row-batch builders.

The sixth local hostile re-audit confirmed the six prior P2s were closed, then found two remaining authority-binding gaps: parser-plan hashes were not content-bound, and source-universe family contracts could self-consistently bind the wrong row-locator family. A seventh patch added parser family-plan and parser-plan-bundle content checks, plus a locked source-universe-family to row-locator-family mapping check. Regression tests cover stale parser-plan internals and wrong source-universe locator-family mappings with recomputed hashes.

The seventh local hostile re-audit found that direct calls to `build_raw_file_hash_set_contract` still accepted internally stale parser-plan bundles. An eighth patch applies parser-plan content-bound validation inside the raw-file-hash builder itself. Regression tests cover direct raw-file-hash construction with stale parser-plan internals.

## Current Boundary

This slice reaches only the early parser/file replay construction boundary:

```text
declared local files -> byte hashes -> structural source rows -> raw/parser/source-row-batch contracts
```

The following downstream artifact construction remains future work unless separately authorized and audited:

- source-row-selection authority outputs;
- source-input manifest;
- level compatibility;
- runtime history;
- forecast;
- desired position;
- order/transition/fill;
- cost;
- PnL;
- validation/provenance/evidence manifest;
- trusted replay bundle.

## Non-Authorizations

This record authorizes no provider/API access, no downloads, no new data acquisition, no OOS/Lockbox/Forward access, no backtests, no result-scored runs, no diagnostics outside local implementation verification, no result interpretation, no PnL/result evaluation, no tuning, no adapter work, no deployment, no trading, no promotion, no Git staging/commit/push/PR, and no source-faithful replay evidence claim.
