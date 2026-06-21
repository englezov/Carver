# S27_V2 Controlled Local Replay Construction Run Blocked On Declared Inputs

Date: 2026-06-08

Status:

```text
CONTROLLED_LOCAL_REPLAY_CONSTRUCTION_RUN_FAIL_CLOSED_NO_DECLARED_S27_V2_ZN_INPUT_PACK
```

Lane:

```text
SOURCE_NATIVE_FUTURES
```

## Operator Authorization

The operator authorized a controlled local-only replay construction run on declared ZN input files only, using the externally passed and pushed S27_V2 local-only parser/file replay construction machinery.

The authorization allowed:

- reading only files declared by `ReplayInputDirectoryDeclaration`;
- computing SHA256 hashes for those declared files;
- parsing declared local daily/hourly/session/roll/cost rows;
- constructing deterministic local replay ledgers/artifacts;
- focused local verification tests;
- process/current-state records;
- local hostile audit of produced replay artifacts.

The authorization did not allow provider/API access, downloads, new data acquisition, OOS, Lockbox, Forward, backtests, result-scored runs, result interpretation, PnL/result evaluation, tuning, adapter work, deployment, trading, promotion, Git actions, or source-faithful evidence claims.

## Oldest-Data Rule

The operator directed that development tests should use the oldest possible suitable data.

This run therefore required the oldest available local ZN files that already satisfy the audited S27_V2 declared-input row-family contract.

## Required Declared Input Families

The current audited parser/file replay construction path requires a `ReplayInputDirectoryDeclaration` covering these locked row-family CSVs:

```text
DAILY_CONTINUOUS_COMPLETED_BAR
DAILY_CURRENT_CONTRACT_COMPLETED_BAR
HOURLY_DECISION_COMPLETED_BAR
HOURLY_FILL_COMPLETED_BAR
SESSION_CALENDAR
ROLL_CALENDAR
COST_PARAMETER
```

Those files must use the locked columns in `src/carver/spine/s27_v2_replay/local_replay.py` and must bind expected SHA256 hashes before parsing.

## Declaration Boundary Result

No existing real S27_V2-normalized ZN input pack was found in the workspace matching the locked row-family names/statuses:

```text
DAILY_CONTINUOUS_COMPLETED_BAR
HOURLY_DECISION_COMPLETED_BAR
READY_COMPLETED_BAR
READY_SESSION_CALENDAR
READY_COST_PARAMETERS
annual_percentage_sigma
```

Occurrences found were limited to code, tests, and process documentation, not a real declared local ZN replay input directory.

Existing historical S26/S27 researchops artifacts are not a substitute for this input pack. They are old backtest, runtime, provider, lineage, or diagnostic artifacts with different schemas and authority status. Adapting them into the S27_V2 declared row-family shape would be a separate normalization/input-declaration gate, not part of this controlled replay construction run.

## Run Decision

The controlled local replay construction run failed closed before constructing a `ReplayInputDirectoryDeclaration` for real data and before invoking the S27_V2 replay construction builders on real input files.

No replay ledgers, fills, costs, PnL rows, scored outputs, or source-faithful evidence artifacts were produced.

## Focused Verification

The existing focused local verification for the externally passed construction machinery remains:

```text
python -m pytest tests\test_s27_v2_local_replay_slice1.py -q
```

Result from the pushed checkpoint:

```text
49 passed
```

## Next Required Gate

The next useful gate is not a backtest and not a replay-result gate.

The next useful gate is:

```text
S27_V2_OLDEST_LOCAL_ZN_INPUT_DECLARATION_AND_NORMALIZATION_GATE
```

That gate should authorize:

- identifying the oldest suitable local ZN source files;
- reading only those explicitly named local source files;
- normalizing them into the seven S27_V2 row-family CSVs;
- writing the declared input pack under a new S27_V2 local replay input directory;
- computing and recording SHA256 hashes;
- proving the row-family contract before any replay construction run.

It should still exclude provider/API access, downloads, OOS, Lockbox, Forward, backtests, result-scored runs, result interpretation, tuning, adapter work, deployment, trading, promotion, Git actions, and source-faithful evidence claims.

## Non-Authorization

This record does not authorize provider/API access, downloads, new data acquisition, OOS, Lockbox, Forward, backtests, result-scored runs, result interpretation, PnL/result evaluation, tuning, adapter work, deployment, trading, promotion, Git staging, Git commit, Git push, PRs, or source-faithful replay evidence claims.
