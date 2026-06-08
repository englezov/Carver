# S27 ZN V2 Source-Row-Batch Parser-Output Authority Routing Scaffold Record

Date: 2026-06-07

Status:

```text
PROCESS_ONLY_S27_ZN_V2_SOURCE_ROW_BATCH_PARSER_OUTPUT_AUTHORITY_ROUTING_SCAFFOLD_RECORD_NOT_EXECUTION_AUTHORIZATION
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Operator Gate

The operator authorized the next narrow S27_V2 parser/file replay implementation scaffold slice only, after active-trust routing external re-audit `PASS`.

Still excluded:

```text
provider/API
downloads
parser/file replay execution
diagnostics
tests/backtests
OOS/Lockbox/Forward
git actions
adapter work
deployment
trading
promotion
result interpretation
source-faithful replay evidence claim
```

## Slice

This slice routes parser-output authority into the source-row-batch contract scaffold without executing a parser or replaying files.

Patched file:

```text
src/carver/spine/s27_v2_replay/source_row_batch_contract.py
```

## Patch Summary

Changed:

```text
SourceRowBatchSetContract.validate()
```

The no-argument validator now fails closed:

```text
S27 v2 source row batch contract requires parser-output authority
```

Added:

```text
SourceRowBatchSetContract.validate_against_parser_output_authority(
    parser_output_contract,
)
```

The authority-aware route:

```text
validates ParserOutputBatchSetContract
validates the source-row-batch contract-only shape
binds parser_output_contract_hash to the cited ParserOutputBatchSetContract
binds parsed_output_batch_set_hash to the cited ParserOutputBatchSetContract
binds each source-row-batch family parser_output_family_contract_hash to the matching parser-output family contract hash
binds each source-row-batch family parser_output_batch_hash to the matching parser-output planned_row_batch_hash
```

## Design Constraint

The patch did not add `ParserOutputBatchSetContract` as a stored field on `SourceRowBatchSetContract`.

This preserves the anti-self-authentication pattern: parser-output authority is passed through an explicit validation path rather than hidden as a caller-supplied peer field.

## Non-Execution

No parser, file replay, diagnostics, tests, backtests, OOS, Lockbox, Forward, provider/API, downloads, git actions, adapter work, deployment, trading, promotion, result interpretation, or source-faithful evidence claim were performed or authorized by this patch.

## Next Gate

The next step requires separate explicit operator authorization for local hostile audit of this source-row-batch parser-output authority routing scaffold.
