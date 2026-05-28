# Clean Workspace Migration Record

Date: 2026-05-28

Status:

```text
PROCESS_ONLY_CARVER_CLEAN_WORKSPACE_MIGRATION_LOCAL_RECORD_NOT_PIPELINE_AUTHORIZATION
```

## Old Workspace

Old local workspace:

```text
C:\Users\openclaw\Desktop\QuantLab_v3
```

Disposition:

```text
ARCHIVED_OPERATIONAL_BLOB_DO_NOT_PIPELINE
```

Archive marker created:

```text
C:\Users\openclaw\Desktop\QuantLab_v3\ARCHIVED_WORKSPACE_DO_NOT_PIPELINE_2026-05-28.md
```

Latest known commit at archive time:

```text
1078ea8 Park ES VWAP reversion discovery lane
```

Old branch at archive time:

```text
codex/s23-acceleration-test-park-record
```

Old remote at archive time:

```text
origin https://github.com/englezov/QuantLab_v3.git
```

## New Workspace

Clean local workspace:

```text
C:\Users\openclaw\Desktop\Carver
```

This workspace starts as a mission shell only. It does not import old code, old adapters, old data-prep scripts, old data folders, old runtime state, or old pipeline state.

Local reference book:

```text
C:\Users\openclaw\Desktop\Carver\Carver.pdf
```

The PDF is local reference material and is ignored by Git.

## Migration Rule

Nothing from the old workspace becomes active authority unless it is deliberately selected, hash-bound, and reintroduced through a clean Carver artifact.

The old workspace may answer historical questions, but it must not be used to run pipelines.

## Next Clean Step

Recommended next clean step:

```text
CARVER_BOOK_STRATEGY_AND_PORTFOLIO_INVENTORY
```

That step should inspect the local book reference and produce a strategy/portfolio inventory without running data, code, tests, backtests, or adapters.
